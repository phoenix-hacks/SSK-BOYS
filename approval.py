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

def update_status(index, new_status):
    validation_data = load_validation_data()
    validation_data.loc[index, "Status"] = new_status
    save_validation_data(validation_data)

st.title("Admin Application Approval")

st.header("Applications:")
validation_data = load_validation_data()

if validation_data.empty:
    st.info("No applications to review.")
else:
    pending_applications = validation_data[validation_data["Status"] == "Pending"]
    
    if pending_applications.empty:
        st.info("No pending applications.")
    else:
        for index, row in pending_applications.iterrows():
            st.write(f"**Name:** {row['Name']} | **Role:** {row['Role']} | **License:** {row['Practitioner License']}")
            st.write(f"**Contact:** {row['Contact']} | **Status:** {row['Status']}")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("Approve", key=f"approve_{index}"):
                    update_status(index, "Approved")
                    st.success(f"Approved application for {row['Name']}.")
                    st.rerun()
            
            with col2:
                if st.button("Reject", key=f"reject_{index}"):
                    update_status(index, "Rejected")
                    st.warning(f"Rejected application for {row['Name']}.")
                    st.rerun()
