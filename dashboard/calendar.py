import streamlit as st
import pandas as pd
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

DATA_FILE = "calendar_events.csv"

def load_events():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Title", "Description", "Date"])

def save_events(events):
    events.to_csv(DATA_FILE, index=False)

def add_event(title, description, date):
    new_event = pd.DataFrame([[title, description, date]], columns=["Title", "Description", "Date"])
    events = load_events()
    events = pd.concat([events, new_event], ignore_index=True)
    save_events(events)

def delete_event(row_index):
    events = load_events()
    events = events.drop(events.index[row_index]).reset_index(drop=True)
    save_events(events)

def notify(title, description):
    st.warning(f"🔔 Reminder: {title} - {description}")

def schedule_notifications(events):
    scheduler = BackgroundScheduler()
    scheduler.start()
    for _, event in events.iterrows():
        trigger = DateTrigger(run_date=event["Date"])
        scheduler.add_job(notify, trigger=trigger, args=[event["Title"], event["Description"]])

def run():
    st.title("📅 Let's Keep You Up-To-Date")

    tab1, tab2 = st.tabs(["📋 View Events", "➕ Add Event"])

    with tab1:
        st.header("Upcoming Events")
        events = load_events()

        if events.empty:
            st.info("No upcoming events.")
        else:
            events["Date"] = pd.to_datetime(events["Date"])
            events = events.sort_values(by="Date").reset_index(drop=True)

            selected_date = st.date_input("Select a date to view events", min_value=events["Date"].min().date())
            day_events = events[events["Date"].dt.date == selected_date]

        if day_events.empty:
            st.info(f"No events on {selected_date}.")
        else:
            for row_index, event in day_events.iterrows():
                formatted_date = event['Date'].strftime("%A, %d %B %Y")
                st.write(f"**{event['Title']}**: {event['Description']} on {formatted_date}")
                if st.button("Delete", key=f"delete_{row_index}"):
                    delete_event(row_index)
                    st.success(f"Deleted event: {event['Title']}")
                    st.rerun()

    with tab2:
        st.header("Add a New Event")
        title = st.text_input("Event Title")
        description = st.text_area("Event Description")
        date = st.date_input("Event Date", min_value=datetime.now().date())
        time = st.time_input("Event Time", value=datetime.strptime("09:00:00", "%H:%M:%S").time(), key="time")

        if st.button("Add Event"):
            if title.strip() and description.strip():
                event_datetime = datetime.combine(date, time)
                add_event(title, description, event_datetime)
                st.success(f"Event '{title}' added for {event_datetime}.")
            else:
                st.error("Please fill in all fields.")

    # Scheduling notifications for all events
    events = load_events()
    schedule_notifications(events)

if __name__ == "__main__":
    run()
