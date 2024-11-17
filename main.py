import streamlit as st
import importlib

st.set_page_config(page_title="MeternalEase", layout="wide")

users = {
    "admin": "password123",
    "user1": "pass123",
    "user2": "mypassword"
}

def check_login(username, password):
    return username in users and users[username] == password

def load_dashboard_page(page_name):
    try:
        page_module = importlib.import_module(f"dashboard.{page_name}")
        if hasattr(page_module, 'run'):
            page_module.run()
        else:
            st.error(f"The module '{page_name}' does not have a 'run()' function.")
    except ModuleNotFoundError:
        st.error(f"Page '{page_name}' not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = None

    if st.session_state.logged_in:
        dashboard_page()
    else:
        login_page()

def login_page():
    st.title("🔒 Login Page")

    # Center the logo on the page using st.image
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center;">
        """, 
        unsafe_allow_html=True
    )
    st.image("logo.png", width=250)  # Use st.image to display logo
    st.markdown("</div>", unsafe_allow_html=True)

    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")

    if st.button("Login", key="login"):
        username = st.session_state.username
        password = st.session_state.password
        if check_login(username, password):
            st.session_state.logged_in = True
            st.session_state.selected_page = None
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials")

    st.markdown(
    """
    <div style="
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
        line-height: 1.6;">
        <h2 style="text-align: center; color: #2b7a78;">Welcome to <strong>MaternEase</strong>!</h2>
        <p style="color: #555; font-size: 16px; text-align: justify;">
            MaternEase is a revolutionary healthcare platform designed to support pregnant women throughout their entire journey. From prenatal care to postpartum recovery, our app offers a comprehensive suite of features including:
        </p>
        <ul style="color: #555; font-size: 16px;">
            <li>🌟 Expert guidance tailored to your needs.</li>
            <li>📈 Baby growth tracking tools.</li>
            <li>📚 Informative and engaging articles.</li>
            <li>💻 Live video consultations with healthcare professionals.</li>
            <li>📅 Easy and convenient appointment booking.</li>
            <li>🔒 Secure document storage for peace of mind.</li>
            <li>🤝 A supportive community to connect with other mothers.</li>
        </ul>
        <p style="color: #555; font-size: 16px; text-align: justify;">
            MaternEase is more than just an app; it's your trusted partner in ensuring a healthy and happy pregnancy.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

def dashboard_page():
    st.session_state.selected_page = "appointments"

    with st.sidebar:
        st.divider()
        profile_expander = st.expander(f"👤 Hello User", expanded=False)
        with profile_expander:
            if st.button("Professional Validation", key="prof_validation", use_container_width=True):
                st.session_state.selected_page = "professionalValidation"
            
            if st.button("Logout", key="logout", use_container_width=True):
                logout()
        st.divider()

    if st.sidebar.button("Appointments", use_container_width=True):
        st.session_state.selected_page = "appointments"
    if st.sidebar.button("Calendar", use_container_width=True):
        st.session_state.selected_page = "calendar"
    if st.sidebar.button("Nutritional Info", use_container_width=True):
        st.session_state.selected_page = "Nutritional"
    if st.sidebar.button("Forum", use_container_width=True):
        st.session_state.selected_page = "forum"
    if st.sidebar.button("Chatbot", use_container_width=True):
        st.session_state.selected_page = "chatbot"
    if st.sidebar.button("AudioBooks", use_container_width=True):
        st.session_state.selected_page = "ABS"
    if st.sidebar.button("PreNet", use_container_width=True):
        st.session_state.selected_page = "PreNet"
    if st.sidebar.button("PostNet", use_container_width=True):
        st.session_state.selected_page = "postnatal"

    if st.session_state.selected_page:
        load_dashboard_page(st.session_state.selected_page)

    if st.button("Back to Dashboard"):
        st.session_state.selected_page = None

def logout():
    st.session_state.logged_in = False
    st.session_state.selected_page = None
    st.rerun()

if __name__ == "__main__":
    main()
