import re
import uuid
from datetime import datetime, timezone
from pathlib import PurePosixPath

import dropbox
import streamlit as st
from dropbox.files import CommitInfo, UploadSessionCursor, WriteMode

DROPBOX_FOLDER = "/M&A Wedding"
LARGE_VIDEO_URL = "https://www.dropbox.com/request/pl6labude2rxsoafh5e0"

SIMPLE_UPLOAD_LIMIT = 150 * 1024 * 1024
CHUNK_SIZE = 8 * 1024 * 1024
LARGE_FILE_WARNING_MB = 700

st.set_page_config(
    page_title="Μάριος & Αγγελική — Wedding Memories",
    page_icon="🤍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def inject_css():
    st.markdown(
        '''
        <style>
        @import url('https://fonts.googleapis.com/css2?family=GFS+Neohellenic:ital,wght@0,400;0,700;1,400&family=Noto+Sans:wght@400;500;600&display=swap');

        :root{
            --paper:#f7f1e8;
            --paper2:#fcfaf6;
            --ink:#26211d;
            --muted:#8b7768;
            --line:rgba(38,33,29,.16);
        }

        html, body, [class*="css"]{
            font-family:"Noto Sans", Arial, sans-serif;
        }

        .stApp{
            background:
              radial-gradient(circle at 15% 10%, rgba(255,255,255,.95), transparent 30rem),
              radial-gradient(circle at 85% 90%, rgba(220,205,185,.28), transparent 28rem),
              linear-gradient(180deg,var(--paper2),var(--paper));
            color:var(--ink);
        }

        header[data-testid="stHeader"]{background:transparent;}
        #MainMenu, footer{visibility:hidden;}

        .block-container{
            max-width:780px;
            padding-top:1.6rem;
            padding-bottom:4rem;
        }

        .ma-hero{
            text-align:center;
            padding:1.2rem .8rem .6rem;
        }

        .ma-eyebrow{
            font-family:"Noto Sans",Arial,sans-serif !important;
            font-size:.67rem !important;
            font-weight:400 !important;
            letter-spacing:.38em !important;
            text-transform:uppercase;
            color:var(--muted);
            margin-bottom:1.7rem;
        }

        .ma-names{
            font-family:"GFS Neohellenic","Trebuchet MS",sans-serif !important;
            font-size:clamp(2.35rem,6vw,3.65rem) !important;
            line-height:1.02 !important;
            font-weight:500 !important;
            letter-spacing:-.025em !important;
            text-align:center !important;
            color:var(--ink) !important;
            margin:0 auto !important;
            white-space:nowrap;
        }

        .ma-amp{
            display:inline-block;
            font-family:"GFS Neohellenic","Trebuchet MS",sans-serif !important;
            font-style:normal !important;
            font-weight:400 !important;
            font-size:.68em !important;
            padding:0 .14em;
            transform:translateY(-.03em);
        }

        .ma-subtitle{
            font-family:"GFS Neohellenic","Trebuchet MS",sans-serif !important;
            font-size:clamp(1.05rem,2.7vw,1.35rem) !important;
            line-height:1.1 !important;
            font-style:italic !important;
            font-weight:400 !important;
            color:var(--muted) !important;
            margin-top:.9rem !important;
        }

        .ma-rule{
            width:76%;
            height:1px;
            background:var(--line);
            margin:1.6rem auto 2rem;
        }

        .ma-copy{
            text-align:center;
            color:var(--muted);
            font-size:.94rem;
            line-height:1.65;
            margin-bottom:1.15rem;
        }

        [data-testid="stFileUploader"]{
            background:rgba(255,255,255,.46);
            border:1px solid var(--line);
            border-radius:24px;
            padding:.4rem;
        }

        [data-testid="stFileUploaderDropzone"]{
            background:rgba(255,255,255,.26);
            border:1px dashed rgba(38,33,29,.22);
            border-radius:20px;
            min-height:145px;
        }

        div.stButton > button{
            width:100%;
            min-height:3.55rem;
            border-radius:999px;
            border:1px solid var(--ink);
            background:var(--ink);
            color:#fff;
            font-family:"Noto Sans",Arial,sans-serif;
            font-size:.82rem;
            font-weight:600;
            letter-spacing:.12em;
            text-transform:uppercase;
        }

        div.stButton > button:hover{
            background:transparent;
            color:var(--ink);
            border-color:var(--ink);
        }

        div[data-testid="stLinkButton"] > a {
            width:72%;
            margin-left:auto;
            margin-right:auto;
            min-height:3.35rem;
            border-radius:999px !important;
            border:1px solid var(--ink) !important;
            background:transparent !important;
            color:var(--ink) !important;
            font-family:"Noto Sans",Arial,sans-serif !important;
            font-size:.78rem !important;
            font-weight:600 !important;
            letter-spacing:.1em !important;
            text-transform:uppercase !important;
            display:flex !important;
            align-items:center !important;
            justify-content:center !important;
            text-decoration:none !important;
        }

        div[data-testid="stLinkButton"] > a:hover {
            background:var(--ink) !important;
            color:#fff !important;
        }

        .ma-large-title{
            text-align:center;
            font-family:"GFS Neohellenic","Trebuchet MS",sans-serif !important;
            font-size:1.5rem !important;
            font-style:italic;
            color:var(--ink);
            margin-top:1.65rem;
            margin-bottom:.2rem;
        }

        .ma-large-copy{
            text-align:center;
            color:var(--muted);
            font-size:.8rem;
            line-height:1.55;
            margin-bottom:.7rem;
        }

        .ma-summary{
            background:rgba(255,255,255,.42);
            border:1px solid var(--line);
            border-radius:18px;
            padding:.9rem 1rem;
            margin:.8rem 0 1rem;
        }

        .ma-thanks{
            text-align:center;
            padding:2rem 1.3rem;
            border:1px solid var(--line);
            border-radius:24px;
            background:rgba(255,255,255,.48);
            margin-top:1rem;
        }

        .ma-thanks-title{
            font-family:"GFS Neohellenic","Trebuchet MS",sans-serif !important;
            font-size:2.4rem !important;
            font-weight:500 !important;
            margin-bottom:.25rem;
        }

        .ma-privacy{
            text-align:center;
            font-size:.76rem;
            color:var(--muted);
            line-height:1.55;
            margin-top:1.2rem;
        }

        @media(max-width:640px){
            .block-container{padding:1rem .9rem 3rem;}
            .ma-names{
                font-size:clamp(1.95rem,9.2vw,2.65rem) !important;
                line-height:1.05 !important;
                white-space:nowrap;
            }
            .ma-amp{
                display:inline-block;
                padding:0 .10em;
                margin:0;
                font-size:.68em !important;
            }
            .ma-subtitle{
                font-size:1.02rem !important;
                line-height:1.25 !important;
                margin-top:.8rem !important;
                padding:0 .8rem;
            }
        }
        </style>
        ''',
        unsafe_allow_html=True,
    )

def get_dropbox_client():
    if all(k in st.secrets for k in ("DROPBOX_APP_KEY", "DROPBOX_APP_SECRET", "DROPBOX_REFRESH_TOKEN")):
        return dropbox.Dropbox(
            app_key=st.secrets["DROPBOX_APP_KEY"],
            app_secret=st.secrets["DROPBOX_APP_SECRET"],
            oauth2_refresh_token=st.secrets["DROPBOX_REFRESH_TOKEN"],
            timeout=900,
        )

    if "DROPBOX_ACCESS_TOKEN" in st.secrets:
        return dropbox.Dropbox(
            oauth2_access_token=st.secrets["DROPBOX_ACCESS_TOKEN"],
            timeout=900,
        )

    raise RuntimeError("Dropbox credentials are missing.")

def safe_filename(name):
    name = PurePosixPath(name).name
    name = re.sub(r"[\x00-\x1f\x7f]+", "", name)
    name = re.sub(r'[<>:"/\\|?*]+', "_", name)
    return name.strip(" .") or "upload"

def destination_path(original_name):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    short_id = uuid.uuid4().hex[:6]
    return f"{DROPBOX_FOLDER.rstrip('/')}/{stamp}_{short_id}_{safe_filename(original_name)}"

def upload_to_dropbox(dbx, uploaded_file, path):
    uploaded_file.seek(0, 2)
    size = uploaded_file.tell()
    uploaded_file.seek(0)

    if size <= SIMPLE_UPLOAD_LIMIT:
        dbx.files_upload(
            uploaded_file.read(),
            path,
            mode=WriteMode.add,
            autorename=True,
            mute=True,
        )
        return

    first_chunk = uploaded_file.read(CHUNK_SIZE)
    start_result = dbx.files_upload_session_start(first_chunk)

    cursor = UploadSessionCursor(
        session_id=start_result.session_id,
        offset=len(first_chunk),
    )

    commit = CommitInfo(
        path=path,
        mode=WriteMode.add,
        autorename=True,
        mute=True,
    )

    while cursor.offset < size:
        remaining = size - cursor.offset
        chunk = uploaded_file.read(min(CHUNK_SIZE, remaining))

        if not chunk:
            raise IOError("Upload ended unexpectedly before Dropbox received the full file.")

        next_offset = cursor.offset + len(chunk)
        is_last_chunk = next_offset == size

        if is_last_chunk:
            dbx.files_upload_session_finish(
                chunk,
                cursor,
                commit,
            )
            cursor.offset = next_offset
        else:
            dbx.files_upload_session_append_v2(
                chunk,
                cursor,
            )
            cursor.offset = next_offset

def main():
    inject_css()

    st.markdown(
        '''
        <div class="ma-hero">
            <div class="ma-eyebrow">M &amp; A · WEDDING</div>
            <div class="ma-names">Μάριος <span class="ma-amp">&amp;</span> Αγγελική</div>
            <div class="ma-subtitle">Οι πιο όμορφες στιγμές, μέσα από τα μάτια σας</div>
        </div>
        <div class="ma-rule"></div>
        <div class="ma-copy">
            Ανέβασε τις φωτογραφίες και τα βίντεο που τράβηξες σήμερα.
        </div>
        ''',
        unsafe_allow_html=True,
    )
    st.link_button(
        "ΜΟΙΡΑΣΟΥ ΤΙΣ ΣΤΙΓΜΕΣ",
        LARGE_VIDEO_URL,
        use_container_width=True,
    )

    st.markdown(
        '''
        <div class="ma-large-title">Έχεις πολύ μεγάλο βίντεο;</div>
        <div class="ma-large-copy">
            Για βίντεο πάνω από 1 GB, χρησιμοποίησε την επιλογή παρακάτω.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st.link_button(
        "ΑΝΕΒΑΣΕ ΤΟ ΒΙΝΤΕΟ",
        LARGE_VIDEO_URL,
        use_container_width=True,
    )

    st.markdown(
        '''
        <div class="ma-privacy">
            Οι αναμνήσεις σας, το καλύτερο δώρο μας. ♡
        </div>
        ''',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
