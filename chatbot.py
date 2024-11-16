import streamlit as st
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
st.set_page_config(page_title="Maternal Nutritional Planner", page_icon="🍎", layout="wide")

load_dotenv() 


genai.configure(api_key="AIzaSyCa7OkEgJEAx0uq9IBa83jWVzOmaHimY5U")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

def GenerateResponse(input_text):
    response = model.generate_content([
    "input: hey can you be my assistant for a while",
    "output: ",
    f"input : {input_text}",
    "output : "
    ])

    return response.text


if "messages" not in st.session_state:
    st.session_state.messages = []

def handle_input():
    user_message = st.session_state.user_input
    if user_message:
        st.session_state.messages.append({"role": "user", "text": user_message})
        bot_response = GenerateResponse(user_message)
        st.session_state.messages.append({"role": "bot", "text": bot_response})
        st.session_state.user_input = ""

st.title("Talk to Janma Mitra, our AI chatbot")

for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['text']}")
    else:
        st.write(f"**Janma Mitra:** {message['text']}")

st.text_input("Type away:", key="user_input", on_change=handle_input)

if st.button("Reset Chat"):
    st.session_state.messages = []
