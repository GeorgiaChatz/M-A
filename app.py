import streamlit as st
import dropbox

st.set_page_config(
    page_title="Dropbox Refresh Token Helper",
    page_icon="🔐",
    layout="centered",
)

st.title("Dropbox Refresh Token Helper")
st.write("Use this one-time page to create a Dropbox refresh token for your wedding upload app.")
st.warning("Do not share your App Secret, authorization code, or refresh token with anyone.")

app_key = st.text_input("Dropbox App Key")
app_secret = st.text_input("Dropbox App Secret", type="password")

if "auth_url" not in st.session_state:
    st.session_state.auth_url = None
if "oauth_flow" not in st.session_state:
    st.session_state.oauth_flow = None

if st.button("Create Dropbox authorization link", use_container_width=True):
    if not app_key or not app_secret:
        st.error("Enter both the App Key and App Secret first.")
    else:
        flow = dropbox.DropboxOAuth2FlowNoRedirect(
            app_key,
            app_secret,
            token_access_type="offline",
        )
        authorize_url = flow.start()
        st.session_state.oauth_flow = flow
        st.session_state.auth_url = authorize_url

if st.session_state.auth_url:
    st.success("Step 1: Open Dropbox and approve the app.")
    st.link_button(
        "Open Dropbox authorization",
        st.session_state.auth_url,
        use_container_width=True,
    )

    st.write(
        "After you click **Allow**, Dropbox will show you an authorization code. "
        "Copy that code and paste it below."
    )

    auth_code = st.text_input("Authorization code")

    if st.button("Generate refresh token", use_container_width=True):
        if not auth_code:
            st.error("Paste the authorization code first.")
        elif st.session_state.oauth_flow is None:
            st.error("Create the authorization link again first.")
        else:
            try:
                result = st.session_state.oauth_flow.finish(auth_code.strip())
                refresh_token = getattr(result, "refresh_token", None)

                if not refresh_token:
                    st.error(
                        "Dropbox did not return a refresh token. "
                        "Create a new authorization link and try again."
                    )
                else:
                    st.success("Done. Your refresh token is below.")
                    st.code(refresh_token, language=None)

                    st.markdown("### Put this in Streamlit Secrets")
                    secrets_text = (
                        'DROPBOX_APP_KEY = "' + app_key + '"\n'
                        'DROPBOX_APP_SECRET = "' + app_secret + '"\n'
                        'DROPBOX_REFRESH_TOKEN = "' + refresh_token + '"'
                    )
                    st.code(secrets_text, language="toml")

                    st.info(
                        "Save these three values in your wedding app's Streamlit Secrets, "
                        "remove the old DROPBOX_ACCESS_TOKEN line, and reboot the app."
                    )

            except Exception as exc:
                st.error("Dropbox could not complete the authorization.")
                with st.expander("Technical details"):
                    st.code(str(exc))
