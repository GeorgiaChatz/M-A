import streamlit as st

st.set_page_config(
    page_title="Μάριος & Αγγελική — Wedding Memories",
    page_icon="🤍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

UPLOAD_URL = "https://www.dropbox.com/request/pl6labude2rxsoafh5e0"


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=GFS+Neohellenic:ital,wght@0,400;0,700;1,400&family=Noto+Sans:wght@400;500;600&display=swap');

:root {
    --paper: #f7f1e8;
    --paper2: #fcfaf6;
    --ink: #26211d;
    --muted: #8b7768;
    --line: rgba(38,33,29,.16);
}

.stApp {
    background:
        radial-gradient(circle at 15% 10%,
        rgba(255,255,255,.95), transparent 30rem),
        radial-gradient(circle at 85% 90%,
        rgba(220,205,185,.28), transparent 28rem),
        linear-gradient(180deg, var(--paper2), var(--paper));

    color: var(--ink);
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 780px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

html, body, [class*="css"] {
    font-family: "Noto Sans", Arial, sans-serif;
}


/* MARKDOWN TEXT */

.ma-eyebrow {
    text-align: center;
    font-size: .67rem;
    letter-spacing: .38em;
    color: var(--muted);
    margin-bottom: 1.4rem;
}

.ma-names {
    text-align: center;
    font-family: "GFS Neohellenic", sans-serif;
    font-size: clamp(2.35rem, 6vw, 3.65rem);
    font-weight: 500;
    line-height: 1.05;
    letter-spacing: -.025em;
    color: var(--ink);
    white-space: nowrap;
}

.ma-amp {
    font-size: .68em;
    font-weight: 400;
    padding: 0 .12em;
}

.ma-subtitle {
    text-align: center;
    font-family: "GFS Neohellenic", sans-serif;
    font-size: 1.15rem;
    font-style: italic;
    color: var(--muted);
    margin-top: .7rem;
}

.ma-rule {
    width: 76%;
    height: 1px;
    background: var(--line);
    margin: 1.8rem auto 2rem;
}

.ma-copy {
    text-align: center;
    color: var(--muted);
    font-size: .94rem;
    line-height: 1.6;
    margin-bottom: 1.2rem;
}

.ma-note {
    text-align: center;
    color: var(--muted);
    font-size: .76rem;
    margin-top: .8rem;
}

.ma-large-title {
    text-align: center;
    font-family: "GFS Neohellenic", sans-serif;
    font-size: 1.5rem;
    font-style: italic;
    color: var(--ink);
    margin-top: 2.8rem;
}

.ma-large-copy {
    text-align: center;
    color: var(--muted);
    font-size: .8rem;
    margin-top: .25rem;
    margin-bottom: .8rem;
}

.ma-footer {
    text-align: center;
    color: var(--muted);
    font-size: .76rem;
    margin-top: 2.8rem;
}


/* NATIVE STREAMLIT LINK BUTTONS */

div[data-testid="stLinkButton"] > a {
    width: 100%;
    min-height: 3.55rem;

    border-radius: 999px !important;
    border: 1px solid var(--ink) !important;

    background: var(--ink) !important;
    color: white !important;

    font-family: "Noto Sans", Arial, sans-serif !important;
    font-size: .78rem !important;
    font-weight: 600 !important;

    letter-spacing: .10em !important;
    text-transform: uppercase !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    text-decoration: none !important;
}

div[data-testid="stLinkButton"] > a:hover {
    background: transparent !important;
    color: var(--ink) !important;
}


/* MOBILE */

@media(max-width: 640px) {

    .block-container {
        padding: 1.2rem .9rem 3rem;
    }

    .ma-names {
        font-size: clamp(1.95rem, 9vw, 2.65rem);
        white-space: nowrap;
    }

    .ma-subtitle {
        font-size: 1.02rem;
        padding: 0 .6rem;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ---------- HEADER ----------

st.markdown(
    '<p class="ma-eyebrow">M &amp; A · WEDDING</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="ma-names">Μάριος <span class="ma-amp">&amp;</span> Αγγελική</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="ma-subtitle">Οι πιο όμορφες στιγμές, μέσα από τα μάτια σας</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="ma-rule"></div>',
    unsafe_allow_html=True,
)


# ---------- MAIN UPLOAD ----------

st.markdown(
    '<p class="ma-copy">Ανέβασε τις φωτογραφίες και τα βίντεο που τράβηξες σήμερα.</p>',
    unsafe_allow_html=True,
)

st.link_button(
    "ΑΝΕΒΑΣΕ ΦΩΤΟΓΡΑΦΙΕΣ & ΒΙΝΤΕΟ",
    UPLOAD_URL,
    use_container_width=True,
)

st.markdown(
    '<p class="ma-note">Μπορείς να επιλέξεις πολλές φωτογραφίες και βίντεο μαζί.</p>',
    unsafe_allow_html=True,
)


# ---------- LARGE VIDEO ----------

st.markdown(
    '<p class="ma-large-title">Έχεις πολύ μεγάλο βίντεο;</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="ma-large-copy">Ανέβασέ το απευθείας στο Dropbox.</p>',
    unsafe_allow_html=True,
)

st.link_button(
    "ΑΝΕΒΑΣΕ ΤΟ ΒΙΝΤΕΟ",
    UPLOAD_URL,
    use_container_width=True,
)


# ---------- FOOTER ----------

st.markdown(
    '<p class="ma-footer">Οι αναμνήσεις σας, το καλύτερο δώρο μας. ♡</p>',
    unsafe_allow_html=True,
)
