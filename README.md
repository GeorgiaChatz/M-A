# M&A Wedding — Guest Photo & Video Upload

A mobile-first Streamlit page for wedding guests to upload photos and videos directly to a private Dropbox folder.

## What guests see

QR code → elegant **Marios & Aggeliki** page → choose photos/videos → **Share memories** → files land in Dropbox.

Guests do **not** need a Dropbox account and they do not see the Dropbox folder.

## 1. Create a Dropbox app

Go to the Dropbox App Console and create an app.

Choose the access type that gives the app access to the folder you want to use. In the app permissions, enable at least:

- `files.content.write`
- `files.metadata.read` is useful for testing/troubleshooting

If you use **App Folder** access, your Dropbox path is relative to that app's own folder.  
If you want to write into an existing normal Dropbox folder named `/M&A Wedding`, choose the Dropbox access model that allows that folder to be addressed by the app.

Create the `/M&A Wedding` folder in Dropbox if it does not already exist.

## 2. Get credentials

### Recommended: refresh token

A refresh token is better for the actual wedding because access tokens can expire.

On your computer:

```bash
pip install dropbox
python scripts/get_dropbox_refresh_token.py
```

Before running the helper, either edit its `APP_KEY` and `APP_SECRET` placeholders or provide environment variables.

It prints an authorization URL. Approve it, paste the authorization code, and copy the resulting refresh token.

### Quick test only

The app also supports a `DROPBOX_ACCESS_TOKEN` Streamlit secret for a fast first test.

## 3. Push this project to GitHub

Your repository should look like:

```text
ma-wedding-upload/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
└── scripts/
    └── get_dropbox_refresh_token.py
```

**Never upload a real `.streamlit/secrets.toml` to GitHub.**

## 4. Deploy on Streamlit Community Cloud

Create a new app from your GitHub repository and use:

```text
app.py
```

as the main file.

Then open your app's **Settings → Secrets** and paste:

```toml
DROPBOX_APP_KEY = "..."
DROPBOX_APP_SECRET = "..."
DROPBOX_REFRESH_TOKEN = "..."
```

For a quick test, the app also accepts:

```toml
DROPBOX_ACCESS_TOKEN = "..."
```

## 5. Customize the wedding text

At the top of `app.py`, edit:

```python
COUPLE_NAMES = "Marios & Aggeliki"
EYEBROW = "M & A · WEDDING"
SUBTITLE = "Share the memories with us"
DROPBOX_FOLDER = "/M&A Wedding"
```

The large heading in the included design already says **Marios & Aggeliki**.

## 6. File size

This repo sets Streamlit's uploader to **1000 MB per file** in `.streamlit/config.toml`.

Dropbox's simple upload route should not be used for files above 150 MiB, so the code automatically switches to an upload session for larger files.

Important: very large videos still pass through the Streamlit server before Dropbox. For normal guest photos and short phone videos this is convenient, but for multi-GB/long 4K videos a direct-to-storage upload architecture is more robust than Streamlit Community Cloud.

## 7. QR code

After the Streamlit app is live, copy its public URL.

That URL — **not the Dropbox URL** — is the one you should put into the QR code in your Canva print design.

Test the final printed QR from:
- iPhone Safari
- Android Chrome
- Wi-Fi
- mobile data

before printing the full batch.
