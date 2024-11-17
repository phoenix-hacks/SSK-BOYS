import streamlit as st
import pandas as pd
import os

# File to store validation requests
VALIDATION_FILE = "validation_requests.csv"

# Load existing validation data
def load_validation_data():
    if os.path.exists(VALIDATION_FILE):
        return pd.read_csv(VALIDATION_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Contact", "Practitioner License", "Role", "Status"])

# Save data to CSV
def save_validation_data(data):
    data.to_csv(VALIDATION_FILE, index=False)

# Add a new validation request
def add_validation_request(name, contact, license_no, role):
    validation_data = load_validation_data()

    # Check for duplicate license number
    if license_no in validation_data["Practitioner License"].values:
        st.warning("An application with this license number already exists.")
        return

    new_request = pd.DataFrame([[name, contact, license_no, role, "Pending"]],
                                columns=["Name", "Contact", "Practitioner License", "Role", "Status"])
    validation_data = pd.concat([validation_data, new_request], ignore_index=True)
    save_validation_data(validation_data)

# Main function to run the Streamlit app
def run():
    st.title("🔍 Professional Validation Portal")

    # Tabs for submission and viewing applications
    tab1, tab2 = st.tabs(["➕ Submit Application", "📋 View Applications"])

    # Tab 1: Submit Application
    with tab1:
        st.header("Submit Your Application")
        
        # Input fields
        name = st.text_input("Name")
        contact = st.text_input("Contact Number")
        license_no = st.text_input("Practitioner License Number")
        role = st.selectbox("Role", ["Doctor", "Midwife"])

        # Submit button
        if st.button("Submit Application", key="submit_application_button"):
            if name.strip() and contact.strip() and license_no.strip() and role.strip():
                add_validation_request(name, contact, license_no, role)
                st.success(f"Application submitted for {name}. Awaiting approval.")
            else:
                st.error("Please fill in all fields.")
    
    # Tab 2: View Applications
    with tab2:
        st.header("Check Status")
        validation_data = load_validation_data()

        # Refresh button to reload data
        if st.button("🔄 Refresh"):
            validation_data = load_validation_data()

        if validation_data.empty:
            st.info("No applications found")
        else:
            st.write("### Applications List:")
            st.dataframe(validation_data)

if __name__ == "__main__":
    run()
