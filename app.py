import re
import uuid
from datetime import datetime, timezone
from pathlib import PurePosixPath

import dropbox
import streamlit as st
from dropbox.files import CommitInfo, UploadSessionCursor, WriteMode


# -----------------------------
# EDIT THESE 4 LINES
# -----------------------------
COUPLE_NAMES = "Marios & Aggeliki"
EYEBROW = "M & A · WEDDING"
SUBTITLE = "Share the memories with us"
DROPBOX_FOLDER = "/M&A Wedding"

# 8 MiB chunks keep each Dropbox request comfortably below its 150 MiB limit.
CHUNK_SIZE = 8 * 1024 * 1024


st.set_page_config(
    page_title=f"{COUPLE_NAMES} — Wedding Memories",
    page_icon="🤍",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --paper: #f6f1e8;
            --ink: #24211f;
            --muted: #746e68;
            --line: rgba(36,33,31,.18);
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 15% 15%, rgba(255,255,255,.92), transparent 31rem),
                radial-gradient(circle at 85% 88%, rgba(226,214,195,.42), transparent 28rem),
                var(--paper);
            color: var(--ink);
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 720px;
            padding-top: 3.2rem;
            padding-bottom: 4rem;
        }

        .hero {
            text-align: center;
            padding: 2rem .8rem 1.15rem;
        }

        .eyebrow {
            font-size: .72rem;
            letter-spacing: .34em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 1.35rem;
        }

        .names {
            font-family: Georgia, "Times New Roman", serif;
            font-size: clamp(3.05rem, 11vw, 6.4rem);
            line-height: .92;
            font-weight: 400;
            letter-spacing: -.045em;
            margin: 0;
        }

        .amp {
            display: block;
            font-style: italic;
            font-size: .58em;
            line-height: .86;
            margin: .12em 0;
        }

        .subtitle {
            font-family: Georgia, "Times New Roman", serif;
            font-style: italic;
            font-size: clamp(1.15rem, 4vw, 1.55rem);
            margin-top: 1.6rem;
            color: var(--muted);
        }

        .rule {
            height: 1px;
            background: var(--line);
            margin: 1.2rem auto 2rem;
            width: 82%;
        }

        .upload-copy {
            text-align: center;
            color: var(--muted);
            margin-bottom: 1.2rem;
            line-height: 1.65;
        }

        [data-testid="stFileUploader"] {
            background: rgba(255,255,255,.50);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: .35rem;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: rgba(255,255,255,.34);
            border: 1px dashed rgba(36,33,31,.26);
            border-radius: 18px;
            min-height: 145px;
        }

        div.stButton > button {
            width: 100%;
            min-height: 3.35rem;
            border-radius: 999px;
            border: 1px solid var(--ink);
            background: var(--ink);
            color: #fff;
            font-weight: 600;
            letter-spacing: .08em;
            text-transform: uppercase;
            transition: all .2s ease;
        }

        div.stButton > button:hover {
            background: transparent;
            color: var(--ink);
            border-color: var(--ink);
        }

        .privacy {
            text-align: center;
            font-size: .78rem;
            color: var(--muted);
            margin-top: 1.1rem;
            line-height: 1.55;
        }

        .thankyou {
            text-align: center;
            padding: 2.1rem 1.3rem;
            border: 1px solid var(--line);
            border-radius: 24px;
            background: rgba(255,255,255,.46);
            margin-top: 1rem;
        }

        .thankyou h3 {
            font-family: Georgia, "Times New Roman", serif;
            font-size: 2rem;
            font-weight: 400;
            margin: 0 0 .5rem;
        }

        @media (max-width: 640px) {
            .block-container {
                padding: 1.4rem 1rem 3rem;
            }
            .hero {
                padding-top: 1.4rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def get_dropbox_client():
    """Use a refresh token when available; access_token is supported for quick testing."""
    secrets = st.secrets

    if all(k in secrets for k in ("DROPBOX_APP_KEY", "DROPBOX_APP_SECRET", "DROPBOX_REFRESH_TOKEN")):
        return dropbox.Dropbox(
            app_key=secrets["DROPBOX_APP_KEY"],
            app_secret=secrets["DROPBOX_APP_SECRET"],
            oauth2_refresh_token=secrets["DROPBOX_REFRESH_TOKEN"],
            timeout=900,
        )

    if "DROPBOX_ACCESS_TOKEN" in secrets:
        return dropbox.Dropbox(
            oauth2_access_token=secrets["DROPBOX_ACCESS_TOKEN"],
            timeout=900,
        )

    raise RuntimeError(
        "Dropbox secrets are missing. Add a refresh token setup "
        "(recommended) or DROPBOX_ACCESS_TOKEN in Streamlit Secrets."
    )


def safe_filename(name: str) -> str:
    """Keep filenames readable while removing path/control characters."""
    name = PurePosixPath(name).name
    name = re.sub(r"[\x00-\x1f\x7f]+", "", name)
    name = re.sub(r'[<>:"/\\\\|?*]+', "_", name)
    name = name.strip(" .")
    return name or "upload"


def destination_path(original_name: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    short_id = uuid.uuid4().hex[:8]
    filename = safe_filename(original_name)
    return f"{DROPBOX_FOLDER.rstrip('/')}/{stamp}_{short_id}_{filename}"


def upload_to_dropbox(dbx: dropbox.Dropbox, uploaded_file, path: str) -> None:
    """
    Stream the Streamlit UploadedFile into Dropbox.

    Small files use files_upload.
    Larger files use an upload session so videos >150 MiB are supported
    on the Dropbox side.
    """
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
            raise IOError("Upload ended unexpectedly before the whole file was read.")

        if cursor.offset + len(chunk) >= size:
            dbx.files_upload_session_finish(chunk, cursor, commit)
        else:
            dbx.files_upload_session_append_v2(chunk, cursor)
            cursor.offset += len(chunk)


def main():
    inject_css()

    st.markdown(
        f"""
        <section class="hero">
            <div class="eyebrow">{EYEBROW}</div>
            <h1 class="names">
                Marios
                <span class="amp">&amp;</span>
                Aggeliki
            </h1>
            <div class="subtitle">{SUBTITLE}</div>
        </section>
        <div class="rule"></div>
        <div class="upload-copy">
            Upload the photos and videos you captured today.<br>
            Select as many as you like, then tap <strong>Share memories</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploads = st.file_uploader(
        "Photos & videos",
        type=[
            "jpg", "jpeg", "png", "heic", "webp",
            "mp4", "mov", "m4v", "avi", "webm",
        ],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="You can choose multiple photos and videos at once.",
    )

    if uploads:
        total_mb = sum(getattr(f, "size", 0) for f in uploads) / (1024 * 1024)
        st.caption(f"{len(uploads)} file(s) selected · {total_mb:,.1f} MB")

    clicked = st.button(
        "Share memories",
        type="primary",
        disabled=not uploads,
        use_container_width=True,
    )

    if clicked and uploads:
        try:
            dbx = get_dropbox_client()
            progress = st.progress(0, text="Preparing your memories…")
            errors = []

            for index, uploaded_file in enumerate(uploads, start=1):
                progress.progress(
                    (index - 1) / len(uploads),
                    text=f"Uploading {index} of {len(uploads)} · {uploaded_file.name}",
                )
                try:
                    upload_to_dropbox(
                        dbx,
                        uploaded_file,
                        destination_path(uploaded_file.name),
                    )
                except Exception as exc:
                    errors.append((uploaded_file.name, str(exc)))

                progress.progress(
                    index / len(uploads),
                    text=f"Uploaded {index} of {len(uploads)}",
                )

            if errors:
                st.warning(
                    f"{len(uploads) - len(errors)} file(s) uploaded, "
                    f"but {len(errors)} could not be uploaded."
                )
                with st.expander("Show upload errors"):
                    for filename, error in errors:
                        st.write(f"**{filename}** — {error}")
            else:
                st.balloons()
                st.markdown(
                    """
                    <div class="thankyou">
                        <h3>Thank you 🤍</h3>
                        <div>Your memories are now part of our day.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.success("All files were uploaded successfully.")

        except Exception as exc:
            st.error(
                "We couldn't connect to the wedding album right now. "
                "Please try again in a moment."
            )
            with st.expander("Technical details"):
                st.code(str(exc))

    st.markdown(
        """
        <div class="privacy">
            Your files are sent directly to our private wedding folder.<br>
            Other guests cannot see what you upload.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
