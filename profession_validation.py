import streamlit as st
import pandas as pd
import os

VALIDATION_FILE = "validation_requests.csv"

def load_validation_data():
    if os.path.exists(VALIDATION_FILE):
        return pd.read_csv(VALIDATION_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Contact", "Practitioner License", "Role", "Status"])

def save_validation_data(data):
    data.to_csv(VALIDATION_FILE, index=False)

def add_validation_request(name, contact, license_no, role):
    new_request = pd.DataFrame([[name, contact, license_no, role, "Pending"]],
                                columns=["Name", "Contact", "Practitioner License", "Role", "Status"])
    validation_data = load_validation_data()
    validation_data = pd.concat([validation_data, new_request], ignore_index=True)
    save_validation_data(validation_data)

st.title("Get Validated")

tab1, tab2 = st.tabs(["➕ Submit Application", "📋 View Applications"])

with tab1:
    st.header("Submit Your Application")
    
    name = st.text_input("Name")
    contact = st.text_input("Contact Number")
    license_no = st.text_input("Practitioner License Number")
    role = st.selectbox("Role", ["Doctor", "Midwife"])

    col1, col = st.columns([8,2]) 
    with col:
        if st.button("Submit Application", key="submit_application_button"):
            if name.strip() and contact.strip() and license_no.strip() and role.strip():
                add_validation_request(name, contact, license_no, role)
                st.success(f"Application submitted for {name}. Awaiting approval.")
            else:
                st.error("Please fill in all fields.")

with tab2:
    st.header("Check Status")
    validation_data = load_validation_data()
    
    if validation_data.empty:
        st.info("No applications found")
    else:
        st.write("### Applications List:")
        st.dataframe(validation_data)
