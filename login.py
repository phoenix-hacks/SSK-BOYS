import streamlit as st

users = {
    "admin": "password123",
    "user1": "pass123",
    "user2": "mypassword"
}

def check_login(username, password):
    return username in users and users[username] == password


def reset_fields():
    
    if 'username' in st.session_state:
        st.session_state['username'] = ''
    if 'password' in st.session_state:
        st.session_state['password'] = ''
    
    st.session_state.authenticated = False


if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'reload' not in st.session_state:
    st.session_state.reload = False

if st.session_state.reload:
    
    st.session_state.reload = False
    st.experimental_set_query_params()

def login():
    st.title("🔒 Login Page")
    st.write("Please enter your username and password to log in.")


    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")


    col1, col2 = st.columns(2)


    if col1.button("Login"):
        if check_login(username, password):
            st.session_state.authenticated = True
            st.success(f"Welcome, {username}!")
        else:
            st.error("Incorrect username or password")


    if col2.button("Reset"):
        reset_fields()


    if st.session_state.authenticated:
        st.write("🎉 You are successfully logged in! Access your protected content here.")

        
        if st.button("Logout"):
            reset_fields()
            
