import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

EVENTS_FILE = "seminars_events.csv"
APPOINTMENTS_FILE = "appointments.csv"

def load_events():
    if os.path.exists(EVENTS_FILE):
        return pd.read_csv(EVENTS_FILE, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Title", "Description", "Date"])

def load_appointments():
    if os.path.exists(APPOINTMENTS_FILE):
        return pd.read_csv(APPOINTMENTS_FILE, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Doctor", "Session", "Date"])

def save_appointments(appointments):
    appointments.to_csv(APPOINTMENTS_FILE, index=False)

def add_appointment(doctor, session, date):
    new_appointment = pd.DataFrame([[doctor, session, date]], columns=["Doctor", "Session", "Date"])
    appointments = load_appointments()
    appointments = pd.concat([appointments, new_appointment], ignore_index=True)
    save_appointments(appointments)


def run():
    st.markdown(
        """
        <style>
        .fixed-right {
            position: fixed;
            top: 100px;
            right: 20px;
            width: 20%;
        }
        .main-content {
            margin-right: 30%;
        }
        a {
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("📚 Postnatal Care Resources")

    col1, col2 = st.columns([3, 1]) 
    with col2:
        st.markdown(
            """
            <div class="fixed-right">
                <h2>📖 Educational Resources</h2>
                <ul>
                    <li><a href="https://www.who.int/">WHO Guidelines on Postnatal Care</a>
                    <li><a href="https://www.cdc.gov/">CDC Postpartum Care Guide</a>
                    <li><a href="https://www.nutrition.org/">Nutrition Tips for New Mothers</a>
                    <li><a href="https://www.mentalhealth.gov/">Mental Health Resources for Postpartum Support</a>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col1:
        st.markdown("---")
        tab1, tab2 = st.tabs(["🎉 Seminars and Events", "👩‍⚕️ Doctor Appointments"])

        with tab1:
            st.markdown("### 🎉 Upcoming Seminars and Events")
            events = load_events()

            if events.empty:
                st.info("No upcoming seminars or events at the moment. Stay tuned!")
            else:
                events = events.sort_values(by="Date").reset_index(drop=True)
                for _, event in events.iterrows():
                    formatted_date = event["Date"].strftime("%A, %d %B %Y at %I:%M %p")
                    st.write(f"**{event['Title']}** - {event['Description']} on {formatted_date}")
                    st.info("📅 Don't forget to attend this event!")

        with tab2:
            st.markdown("### 👩‍⚕️ Book a Doctor's Appointment")

            appointments = load_appointments()

            if appointments.empty:
                st.info("No Appointments Scheduled.")
            else:
                st.write("#### Scheduled Appointments:")
                for _, appointment in appointments.iterrows():
                    formatted_date = appointment["Date"].strftime("%A, %d %B %Y at %I:%M %p")
                    st.write(f"**{appointment['Doctor']}** - {appointment['Session']} on {formatted_date}")

            st.markdown("---")
            st.subheader("Book an Appointment")

            doctor = st.selectbox("Choose Doctor", ["Dr. Gayathri", "Dr. Veena", "Dr. Rashmi", "Dr. Radhika"])
            session = st.selectbox("Choose Session", ["Consultation", "Follow-up", "Emergency"])
            date = st.date_input("Appointment Date", min_value=datetime.now().date())
            time = st.time_input("Appointment Time", value=datetime.strptime("09:00:00", "%H:%M:%S").time())

            if st.button("Book Appointment"):
                if doctor.strip() and session.strip():
                    appointment_datetime = datetime.combine(date, time)
                    add_appointment(doctor, session, appointment_datetime)
                    st.success(f"Appointment with Dr. {doctor} scheduled for {appointment_datetime.strftime('%A, %d %B %Y at %I:%M %p')}.")
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")
