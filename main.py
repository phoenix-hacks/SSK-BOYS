import streamlit as st
import importlib

st.set_page_config(page_title="MeternalEase", layout="wide")

# Users dictionary for login
users = {
    "admin": "password123",
    "user1": "pass123",
    "user2": "mypassword"
}

# Function to check login credentials
def check_login(username, password):
    return username in users and users[username] == password

# Function to load a page dynamically
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

# Main function to control page flow
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = None

    if st.session_state.logged_in:
        dashboard_page()
    else:
        login_page()

# Login page function
def login_page():
    st.title("🔒 Login Page")

    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    # Login button
    if st.button("Login", key="login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.selected_page = None
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials")

# Dashboard page with left sidebar navigation (buttons)
def dashboard_page():
    st.title("📊 Dashboard")

    # Sidebar navigation using buttons
    st.sidebar.title("Navigation")
    st.sidebar.markdown("### Select a page:")

    # Sidebar buttons (with full width using `use_container_width`)
    if st.sidebar.button("Appointments", use_container_width=True):
        st.session_state.selected_page = "appointments"
    elif st.sidebar.button("Calendar", use_container_width=True):
        st.session_state.selected_page = "calendar"
    elif st.sidebar.button("Nutritional Info", use_container_width=True):
        st.session_state.selected_page = "Nutritional"
    elif st.sidebar.button("Forum", use_container_width=True):
        st.session_state.selected_page = "forum"
    elif st.sidebar.button("Chatbot", use_container_width=True):
        st.session_state.selected_page = "chatbot"
    elif st.sidebar.button("AudioBooks", use_container_width=True):
        st.session_state.selected_page = "ABS"
    elif st.sidebar.button("PreNet", use_container_width=True):
        st.session_state.selected_page = "PreNet"
    elif st.sidebar.button("PostNet", use_container_width=True):
        st.session_state.selected_page = "postnatal"

    # Load the selected page if a button was clicked
    if st.session_state.selected_page:
        load_dashboard_page(st.session_state.selected_page)

    # Back button to return to dashboard
    if st.button("Back to Dashboard"):
        st.session_state.selected_page = None

    # Add a logout button in the sidebar
    if st.sidebar.button("Logout", key="logout", use_container_width=True):
        logout()

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.selected_page = None
    st.experimental_rerun()

if __name__ == "__main__":
    main()
