import streamlit as st
import os
import importlib
from login import login

# Users dictionary for login
users = {
    "admin": "password123",
    "user1": "pass123",
    "user2": "mypassword"
}

# Function to check login credentials
def check_login(username, password):
    return username in users and users[username] == password

# Function to load the dashboard page dynamically
def load_dashboard_page(page_name):
    try:
        page_module = importlib.import_module(f"dashboard.{page_name}")
        page_module.run()  # Ensure each module has a `run` function
    except ModuleNotFoundError:
        st.error("Page not found.")

# Main function to control page flow
def main():
    # Check if the user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        # If logged in, automatically go to the dashboard page
        dashboard_page()
    else:
        # Show login page if not logged in
        login_page()

# Login page function
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True  # Mark the user as logged in
            st.session_state.username = username  # Store the username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials")

# Dashboard page function
def dashboard_page():
    st.title("Dashboard")
    page_option = st.selectbox("Select a Dashboard Page", ["Appointments", "Calendar", "Nutritional Info"])

    # Dynamically load the selected page
    if page_option == "Appointments":
        load_dashboard_page("appointments")
    elif page_option == "Calendar":
        load_dashboard_page("calendar")
    elif page_option == "Nutritional Info":
        load_dashboard_page("Nutritional")

# Forum page function
def forum_page():
    st.title("Forum")
    st.write("This is the forum page where users can interact.")

# Chatbot page function
def chatbot_page():
    st.title("Chatbot")
    st.write("This is the chatbot page where users can interact with the chatbot.")
    import chatbot
    chatbot.run()  # Assuming you have a run() function in chatbot.py that handles interactions

if __name__ == "__main__":
    main()
