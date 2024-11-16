import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

DATA_FILE = "appointments.csv"

def load_appointments():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Doctor","Session","Date"])
    
def save_appointments(appointments):
    appointments.to_csv(DATA_FILE, index=False)

def add_appointment(doctor,session,date):
    new_appointment = pd.DataFrame([[doctor,session,date]],columns=["Doctor","Session","Date"])
    appointments = load_appointments()
    appointments = pd.concat([appointments,new_appointment],ignore_index=True)
    save_appointments(appointments)

def delete_appointment(index):
    appointments = load_appointments()
    appointments = appointments.drop(index).reset_index(drop=True)
    save_appointments(appointments)

def display_appointments():
    appointments = load_appointments()
    if appointments.empty:
        st.info("No Appointments Scheduled.")
    else:
        st.write("#### Appointments:")
        for index,appointment in appointments.iterrows():
            formatted_date = appointment['Date'].strftime("%A, %d %B %Y at %I:%M %p")

            col1, col2 = st.columns([4, 1]) 
            
            with col1:
                st.write(f"{appointment['Doctor']} - {appointment['Session']} on {formatted_date}")
            
            with col2:
                if st.button("Delete", key=f"delete_{index}"):
                    delete_appointment(index)
                    st.success(f"Deleted appointment for Dr. {appointment['Doctor']}")
                    st.rerun()

st.title("Schedule Appointment")

tab1, tab2 = st.tabs(["📋 View Appointments", "➕ Book Appointment"])

with tab1:
    display_appointments()

with tab2:
    st.header("Book an Appointment")
    
    doctor = st.selectbox("Choose Doctor", ["Dr. Gayathri", "Dr. Veena", "Dr. Rashmi", "Dr. Radhika"])
    session = st.selectbox("Choose Session", ["Consultation", "Follow-up", "Emergency"])
    date = st.date_input("Appointment Date", min_value=datetime.now().date())
    time = st.time_input("Appointment Time", value=datetime.strptime("09:00:00", "%H:%M:%S").time())

    if st.button("Schedule Appointment"):
        if doctor.strip() and session.strip():
            appointment_datetime = datetime.combine(date, time)
        
            add_appointment(doctor, session, appointment_datetime)
            st.success(f"Appointment with Dr. {doctor} scheduled for {appointment_datetime.strftime('%A, %d %B %Y at %I:%M %p')}.")
            st.rerun()
        else:
            st.error("Please fill in all fields.")