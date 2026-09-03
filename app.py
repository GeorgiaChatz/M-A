import re
import uuid
from datetime import datetime, timezone
from pathlib import PurePosixPath

import dropbox
import streamlit as st
from dropbox.files import CommitInfo, UploadSessionCursor, WriteMode

DROPBOX_FOLDER = "/M&A Wedding"
CHUNK_SIZE = 8 * 1024 * 1024
LARGE_FILE_WARNING_MB = 700
VERY_LARGE_FILE_MB = 1000

st.set_page_config(
    page_title="Marios & Aggeliki — Wedding Memories",
    page_icon="🤍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def inject_css():
    st.markdown(
        '''
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Montserrat:wght@400;500;600&display=swap');

        :root {
            --paper: #f5efe5;
            --paper2: #fbf8f3;
            --ink: #23201e;
            --muted: #7d7268;
            --line: rgba(35,32,30,.17);
        }

        .stApp {
            background:
                radial-gradient(circle at 14% 12%, rgba(255,255,255,.96), transparent 30rem),
                radial-gradient(circle at 84% 86%, rgba(221,207,188,.28), transparent 30rem),
                linear-gradient(180deg, var(--paper2), var(--paper));
            color: var(--ink);
        }

        html, body, [class*="css"] {
            font-family: "Montserrat", system-ui, sans-serif;
        }

        header[data-testid="stHeader"] { background: transparent; }
        #MainMenu, footer { visibility: hidden; }

        .block-container {
            max-width: 760px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .hero {
            text-align: center;
            padding: 1.5rem .8rem .8rem;
        }

        .eyebrow {
            font-size: .68rem;
            letter-spacing: .34em;
            color: var(--muted);
            margin-bottom: 1.55rem;
        }

        .names {
            font-family: "Cormorant Garamond", Georgia, serif;
            font-size: clamp(4rem, 13vw, 7.4rem);
            line-height: .84;
            font-weight: 500;
            letter-spacing: -.05em;
            margin: 0;
            text-align: center;
        }

        .amp {
            display: block;
            font-style: italic;
            font-weight: 400;
            font-size: .48em;
            line-height: .82;
            margin: .12em 0 .08em;
        }

        .subtitle {
            font-family: "Cormorant Garamond", Georgia, serif;
            font-style: italic;
            font-size: clamp(1.55rem, 5vw, 2rem);
            color: var(--muted);
            margin-top: 1.8rem;
        }

        .rule {
            width: 78%;
            height: 1px;
            background: var(--line);
            margin: 1.4rem auto 2rem;
        }

        .upload-copy {
            text-align: center;
            color: var(--muted);
            line-height: 1.7;
            margin-bottom: 1.2rem;
        }

        [data-testid="stFileUploader"] {
            background: rgba(255,255,255,.5);
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: .4rem;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: rgba(255,255,255,.34);
            border: 1px dashed rgba(35,32,30,.22);
            border-radius: 20px;
            min-height: 150px;
        }

        div.stButton > button {
            width: 100%;
            min-height: 3.5rem;
            border-radius: 999px;
            border: 1px solid var(--ink);
            background: var(--ink);
            color: white;
            font-weight: 600;
            letter-spacing: .1em;
            text-transform: uppercase;
        }

        div.stButton > button:hover {
            background: transparent;
            color: var(--ink);
            border-color: var(--ink);
        }

        .file-summary {
            background: rgba(255,255,255,.38);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: .9rem 1rem;
            margin: .8rem 0 1rem;
        }

        .thankyou {
            text-align: center;
            padding: 2.2rem 1.4rem;
            border: 1px solid var(--line);
            border-radius: 26px;
            background: rgba(255,255,255,.48);
            margin-top: 1.2rem;
        }

        .thankyou h3 {
            font-family: "Cormorant Garamond", Georgia, serif;
            font-size: 2.35rem;
            font-weight: 500;
            margin: 0 0 .45rem;
        }

        .privacy {
            text-align: center;
            font-size: .77rem;
            color: var(--muted);
            margin-top: 1.3rem;
            line-height: 1.55;
        }

        @media (max-width: 640px) {
            .block-container { padding: 1.1rem .95rem 3rem; }
            .names { font-size: clamp(3.7rem, 19vw, 6.2rem); }
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
    name = re.sub(r'[<>:"/\\\\|?*]+', "_", name)
    return name.strip(" .") or "upload"

def destination_path(original_name):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    short_id = uuid.uuid4().hex[:6]
    return f"{DROPBOX_FOLDER.rstrip('/')}/{stamp}_{short_id}_{safe_filename(original_name)}"

def upload_to_dropbox(dbx, uploaded_file, path):
    uploaded_file.seek(0, 2)
    size = uploaded_file.tell()
    uploaded_file.seek(0)

    if size <= CHUNK_SIZE:
        dbx.files_upload(
            uploaded_file.read(),
            path,
            mode=WriteMode.add,
            autorename=True,
            mute=True,
        )
        return

    first_chunk = uploaded_file.read(CHUNK_SIZE)
    session = dbx.files_upload_session_start(first_chunk)
    cursor = UploadSessionCursor(session_id=session.session_id, offset=len(first_chunk))
    commit = CommitInfo(path=path, mode=WriteMode.add, autorename=True, mute=True)

    while cursor.offset < size:
        remaining = size - cursor.offset
        chunk = uploaded_file.read(min(CHUNK_SIZE, remaining))
        if not chunk:
            raise IOError("Upload ended unexpectedly.")

        if cursor.offset + len(chunk) >= size:
            dbx.files_upload_session_finish(chunk, cursor, commit)
        else:
            dbx.files_upload_session_append_v2(chunk, cursor)
            cursor.offset += len(chunk)

def main():
    inject_css()

    st.markdown(
        '''
        <section class="hero">
            <div class="eyebrow">M &amp; A · WEDDING</div>
            <h1 class="names">
                Marios
                <span class="amp">&amp;</span>
                Aggeliki
            </h1>
            <div class="subtitle">Share the memories with us</div>
        </section>
        <div class="rule"></div>
        <div class="upload-copy">
            Upload the photos and videos you captured today.<br>
            You can select many files at once.
        </div>
        ''',
        unsafe_allow_html=True,
    )

    uploads = st.file_uploader(
        "Photos & videos",
        type=["jpg", "jpeg", "png", "heic", "webp", "mp4", "mov", "m4v", "avi", "webm"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploads:
        total_mb = sum(getattr(f, "size", 0) for f in uploads) / (1024 * 1024)
        st.markdown(
            f'<div class="file-summary"><strong>{len(uploads)} file(s) selected</strong><br>Total size: {total_mb:,.1f} MB</div>',
            unsafe_allow_html=True,
        )

        large = [f for f in uploads if getattr(f, "size", 0) / (1024 * 1024) >= LARGE_FILE_WARNING_MB]
        very_large = [f for f in uploads if getattr(f, "size", 0) / (1024 * 1024) >= VERY_LARGE_FILE_MB]

        if large and not very_large:
            st.info("Large video selected. Keep this page open until the upload finishes.")
        if very_large:
            st.warning("One or more files are around 1 GB or larger. If one fails, upload that video separately.")

    if st.button("Share memories", disabled=not uploads, use_container_width=True):
        try:
            dbx = get_dropbox_client()
            progress = st.progress(0, text="Preparing your memories…")
            errors = []

            for i, f in enumerate(uploads, start=1):
                size_mb = getattr(f, "size", 0) / (1024 * 1024)
                progress.progress((i - 1) / len(uploads), text=f"Uploading {i} of {len(uploads)} · {f.name} · {size_mb:,.1f} MB")
                try:
                    upload_to_dropbox(dbx, f, destination_path(f.name))
                except Exception as exc:
                    errors.append((f.name, str(exc)))
                progress.progress(i / len(uploads), text=f"Finished {i} of {len(uploads)}")

            ok = len(uploads) - len(errors)

            if errors:
                st.warning(f"{ok} file(s) uploaded successfully, but {len(errors)} failed.")
                with st.expander("Show upload errors"):
                    for filename, error in errors:
                        st.write(f"**{filename}**")
                        st.code(error)
            else:
                st.balloons()
                st.markdown(
                    '<div class="thankyou"><h3>Thank you 🤍</h3><div>Your memories are now part of our day.</div></div>',
                    unsafe_allow_html=True,
                )
                st.success("All files were uploaded successfully.")

        except Exception as exc:
            st.error("We couldn't connect to the wedding album right now. Please try again.")
            with st.expander("Technical details"):
                st.code(str(exc))

    st.markdown(
        '<div class="privacy">Your files are uploaded to our private wedding folder.<br>Other guests cannot see what you share.</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
