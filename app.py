import streamlit as st

st.set_page_config(
    page_title="Μάριος & Αγγελική — Wedding Memories",
    page_icon="🤍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Dropbox File Request
UPLOAD_URL = "https://www.dropbox.com/request/pl6labude2rxsoafh5e0"


def inject_css():
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

html, body, [class*="css"] {
    font-family: "Noto Sans", Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(255,255,255,.95),
            transparent 30rem
        ),
        radial-gradient(
            circle at 85% 90%,
            rgba(220,205,185,.28),
            transparent 28rem
        ),
        linear-gradient(
            180deg,
            var(--paper2),
            var(--paper)
        );

    color: var(--ink);
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 780px;
    padding-top: 1.6rem;
    padding-bottom: 4rem;
}


/* HERO */

.ma-hero {
    text-align: center;
    padding: 1.2rem .8rem .6rem;
}

.ma-eyebrow {
    font-family: "Noto Sans", Arial, sans-serif !important;

    font-size: .67rem !important;
    font-weight: 400 !important;

    letter-spacing: .38em !important;
    text-transform: uppercase;

    color: var(--muted);

    margin-bottom: 1.7rem;
}

.ma-names {
    font-family:
        "GFS Neohellenic",
        "Trebuchet MS",
        sans-serif !important;

    font-size:
        clamp(2.35rem, 6vw, 3.65rem) !important;

    line-height: 1.02 !important;

    font-weight: 500 !important;

    letter-spacing: -.025em !important;

    text-align: center !important;

    color: var(--ink) !important;

    margin: 0 auto !important;

    white-space: nowrap;
}

.ma-amp {
    display: inline-block;

    font-family:
        "GFS Neohellenic",
        "Trebuchet MS",
        sans-serif !important;

    font-style: normal !important;
    font-weight: 400 !important;

    font-size: .68em !important;

    padding: 0 .14em;

    transform: translateY(-.03em);
}

.ma-subtitle {
    font-family:
        "GFS Neohellenic",
        "Trebuchet MS",
        sans-serif !important;

    font-size:
        clamp(1.05rem, 2.7vw, 1.35rem) !important;

    line-height: 1.1 !important;

    font-style: italic !important;
    font-weight: 400 !important;

    color: var(--muted) !important;

    margin-top: .9rem !important;
}


/* DIVIDER */

.ma-rule {
    width: 76%;
    height: 1px;

    background: var(--line);

    margin: 1.6rem auto 2rem;
}


/* COPY */

.ma-copy {
    text-align: center;

    color: var(--muted);

    font-size: .94rem;
    line-height: 1.65;

    margin-bottom: 1.25rem;
}


/* STREAMLIT LINK BUTTON */

div[data-testid="stLinkButton"] > a {
    width: 100%;

    min-height: 3.55rem;

    border-radius: 999px !important;

    border:
        1px solid var(--ink) !important;

    background:
        var(--ink) !important;

    color:
        #ffffff !important;

    font-family:
        "Noto Sans",
        Arial,
        sans-serif !important;

    font-size:
        .78rem !important;

    font-weight:
        600 !important;

    letter-spacing:
        .10em !important;

    text-transform:
        uppercase !important;

    display:
        flex !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    text-decoration:
        none !important;

    transition:
        all .2s ease;
}

div[data-testid="stLinkButton"] > a:hover {
    background:
        transparent !important;

    color:
        var(--ink) !important;

    border-color:
        var(--ink) !important;
}


/* NOTE */

.ma-upload-note {
    text-align: center;

    color: var(--muted);

    font-size: .76rem;
    line-height: 1.55;

    margin-top: .9rem;
}


/* LARGE VIDEO */

.ma-large-title {
    text-align: center;

    font-family:
        "GFS Neohellenic",
        "Trebuchet MS",
        sans-serif !important;

    font-size:
        1.5rem !important;

    font-style:
        italic;

    color:
        var(--ink);

    margin-top:
        2.7rem;

    margin-bottom:
        .2rem;
}

.ma-large-copy {
    text-align: center;

    color:
        var(--muted);

    font-size:
        .8rem;

    line-height:
        1.55;

    margin-bottom:
        .9rem;
}


/* FOOTER */

.ma-privacy {
    text-align: center;

    font-size:
        .76rem;

    color:
        var(--muted);

    line-height:
        1.55;

    margin-top:
        2.8rem;
}


/* MOBILE */

@media(max-width: 640px) {

    .block-container {
        padding:
            1rem .9rem 3rem;
    }

    .ma-names {
        font-size:
            clamp(
                1.95rem,
                9.2vw,
                2.65rem
            ) !important;

        line-height:
            1.05 !important;

        white-space:
            nowrap;
    }

    .ma-amp {
        display:
            inline-block;

        padding:
            0 .10em;

        margin:
            0;

        font-size:
            .68em !important;
    }

    .ma-subtitle {
        font-size:
            1.02rem !important;

        line-height:
            1.25 !important;

        margin-top:
            .8rem !important;

        padding:
            0 .8rem;
    }
}

</style>
""",
        unsafe_allow_html=True,
    )


def main():

    inject_css()

    # HERO
    st.markdown(
        """
<div class="ma-hero">
    <div class="ma-eyebrow">
        M &amp; A · WEDDING
    </div>

    <div class="ma-names">
        Μάριος
        <span class="ma-amp">&amp;</span>
        Αγγελική
    </div>

    <div class="ma-subtitle">
        Οι πιο όμορφες στιγμές, μέσα από τα μάτια σας
    </div>
</div>

<div class="ma-rule"></div>

<div class="ma-copy">
    Ανέβασε τις φωτογραφίες και τα βίντεο
    που τράβηξες σήμερα.
</div>
""",
        unsafe_allow_html=True,
    )

    # DIRECT DROPBOX FILE REQUEST
    st.link_button(
        "ΑΝΕΒΑΣΕ ΦΩΤΟΓΡΑΦΙΕΣ & ΒΙΝΤΕΟ",
        UPLOAD_URL,
        use_container_width=True,
    )

    st.markdown(
        """
<div class="ma-upload-note">
    Μπορείς να επιλέξεις πολλές φωτογραφίες
    και βίντεο μαζί.
</div>

<div class="ma-large-title">
    Έχεις πολύ μεγάλο βίντεο;
</div>

<div class="ma-large-copy">
    Ανέβασέ το απευθείας στο Dropbox.
</div>
""",
        unsafe_allow_html=True,
    )

    # SAME DIRECT DROPBOX FILE REQUEST
    st.link_button(
        "ΑΝΕΒΑΣΕ ΤΟ ΒΙΝΤΕΟ",
        UPLOAD_URL,
        use_container_width=True,
    )

    st.markdown(
        """
<div class="ma-privacy">
    Οι αναμνήσεις σας, το καλύτερο δώρο μας. ♡
</div>
""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
