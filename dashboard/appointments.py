import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

DATA_FILE = "appointments.csv"

# Load existing appointments
def load_appointments():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Doctor", "Session", "Date"])

# Save appointments to the file
def save_appointments(appointments):
    appointments.to_csv(DATA_FILE, index=False)

# Add a new appointment
def add_appointment(doctor, session, date):
    appointments = load_appointments()
    
    # Check if an appointment already exists at the same time for the doctor
    if not appointments[(appointments['Doctor'] == doctor) & (appointments['Date'] == date)].empty:
        st.error(f"An appointment with Dr. {doctor} already exists at this time!")
        return False
    
    new_appointment = pd.DataFrame([[doctor, session, date]], columns=["Doctor", "Session", "Date"])
    appointments = pd.concat([appointments, new_appointment], ignore_index=True)
    save_appointments(appointments)
    return True

# Delete an appointment
def delete_appointment(index):
    appointments = load_appointments()
    appointments = appointments.drop(index).reset_index(drop=True)
    save_appointments(appointments)

# Display existing appointments
def display_appointments():
    appointments = load_appointments()
    if appointments.empty:
        st.info("No Appointments Scheduled.")
    else:
        st.write("#### Upcoming Appointments:")
        for index, appointment in appointments.iterrows():
            formatted_date = appointment['Date'].strftime("%A, %d %B %Y at %I:%M %p")

            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Styling the card-like format without custom colors
                st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <h4>{appointment['Doctor']} - {appointment['Session']}</h4>
                        <p>{formatted_date}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Delete", key=f"delete_{index}", use_container_width=True):
                    delete_appointment(index)
                    st.success(f"Deleted appointment for Dr. {appointment['Doctor']}")

# Custom CSS styles for the app
st.markdown("""
    <style>
    .header {
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-top: 50px;
    }
    .subheader {
        font-size: 30px;
        font-weight: bold;
        color: #333;
    }
    .button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 16px;
    }
    .button:hover {
        background-color: #45a049;
    }
    .appointment-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }
    .appointment-title {
        font-size: 18px;
        font-weight: bold;
        color: #333;
    }
    .appointment-date {
        font-size: 14px;
        color: #777;
    }
    .success-message {
        color: #4CAF50;
    }
    .error-message {
        color: #e74c3c;
    }
    </style>
""", unsafe_allow_html=True)

# Main function to display the app
def run():
    st.title("📅 Schedule Appointment")

    # Customizing the tab titles with icons
    tab1, tab2 = st.tabs(["📋 View Appointments", "➕ Book Appointment"])

    with tab1:
        display_appointments()

    with tab2:
        st.header("Book an Appointment")
        
        # Doctor and Session options
        doctor = st.selectbox("Choose Doctor", ["Dr. Gayathri", "Dr. Veena", "Dr. Rashmi", "Dr. Radhika"], key="doctor")
        session = st.selectbox("Choose Session", ["Consultation", "Follow-up", "Emergency"], key="session")
        
        # Appointment Date and Time
        date = st.date_input("Appointment Date", min_value=datetime.now().date(), key="date")
        time = st.time_input("Appointment Time", value=datetime.strptime("09:00:00", "%H:%M:%S").time(), key="time")

        # Button to schedule the appointment
        if st.button("Schedule Appointment", key="schedule", use_container_width=True):
            if doctor.strip() and session.strip():
                appointment_datetime = datetime.combine(date, time)
                
                if add_appointment(doctor, session, appointment_datetime):
                    st.success(f"Appointment with Dr. {doctor} scheduled for {appointment_datetime.strftime('%A, %d %B %Y at %I:%M %p')}.")
                else:
                    st.error(f"Failed to schedule appointment with Dr. {doctor}.")

# Run the app
if __name__ == "__main__":
    run()
