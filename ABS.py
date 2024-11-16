import streamlit as st
import json
import os
st.set_page_config(page_title="Maternal Nutritional Planner", page_icon="🍎", layout="wide")


def load_json():
    with open("Database/audiobooks/data.json", "r") as f:
        return json.load(f)

def file_exists(filepath):
    return os.path.exists(filepath)

def load_audio_file(file_path):
    with open(file_path, "rb") as audio_file:
        return audio_file.read()

data = load_json()

if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'selected_album' not in st.session_state:
    st.session_state.selected_album = None
    
if 'playing_track_id' not in st.session_state:
    st.session_state.playing_track_id = None
if 'audio_player' not in st.session_state:
    st.session_state.audio_player = None

def display_home_page():
    st.title("Audiobooks Collection")
    for album in data["albums"]:
        cover_path = os.path.join("Database/audiobooks", album["cover"])
        
        if file_exists(cover_path):
            st.image(cover_path, width=200)
            
            if st.button(album["title"], key=f"album_{album['id']}"):
                st.session_state.selected_album = album
                st.session_state.current_page = "details"
        else:
            st.error(f"Cover not found for {album['title']}")
        st.divider()  


def display_album_details(album):
    st.title(album["title"])
    
    cover_path = os.path.join("Database/audiobooks", album["cover"])
    if file_exists(cover_path):
        st.image(cover_path, width=200)

    if st.button("⬅️ Back"):
        st.session_state.current_page = "home"
        
    st.subheader("Tracks")

    for track in album["tracks"]:
        st.write(f"🎵 {track['title']}")
        audio_path = os.path.join("Database/audiobooks", track["file_path"])
        
        if file_exists(audio_path):
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                st.write(f"Track: {track['title']}")
            with col2:
                
                if st.button("▶️ Play", key=f"play_{track['id']}"):
                    if st.session_state.playing_track_id != track['id']:
                        
                        st.session_state.playing_track_id = track['id']
                        st.session_state.audio_player = track['id']  
                
                if st.button("⏸️ Pause", key=f"pause_{track['id']}"):
                    if st.session_state.playing_track_id == track['id']:
                        
                        st.session_state.playing_track_id = None
                        st.session_state.audio_player = None  

            
            if st.session_state.playing_track_id == track['id']:
                st.success(f"Playing: {track['title']}")
                audio_bytes = load_audio_file(audio_path)
                st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                st.session_state.audio_player = None  
        else:
            st.error(f"Audio file not found: {track['file_path']}")
   

if st.session_state.current_page == "home":
    display_home_page()
elif st.session_state.current_page == "details" and st.session_state.selected_album:
    display_album_details(st.session_state.selected_album)
