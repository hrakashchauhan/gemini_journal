import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# This block now uses the correct model name confirmed to be available for your API key.
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    # Initialize the Gemini model with the exact name from your list
    model = genai.GenerativeModel('models/gemini-pro-latest')
except Exception as e:
    st.error(f"Error configuring the API. Make sure your GOOGLE_API_KEY is set correctly in the .env file. Error: {e}")
    st.stop()


# --- Helper Function to get AI response ---
def get_gemini_response(prompt):
    """
    Sends a prompt to the Gemini model and returns the response.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# --- Streamlit Web App Interface ---

st.set_page_config(page_title="AI Journaling Companion", page_icon="✍️", layout="centered")

st.title("AI Journaling Companion ✍️")
st.write("Your personal guide for the Integrated Journaling Practice.")

# Dropdown for selecting the journaling mode
journal_mode = st.selectbox(
    "Choose your journaling session:",
    (
        "Morning: Mind-Clear & Daily Intention",
        "Evening: Daily Log & Reflection",
        "Weekly: Review & Plan",
        "Deep Dive: Unsent Letter"
    )
)

# Text area for user input
user_input = st.text_area("Write your thoughts here...", height=200)

# Button to submit
submit_button = st.button("Get AI Guidance")


# --- Main Logic ---
if submit_button and user_input:
    # 1. Craft a specific prompt based on the selected mode
    prompt = ""
    if journal_mode == "Morning: Mind-Clear & Daily Intention":
        prompt = f"""
        Act as a calm and focused mindset coach. The user is doing their morning mind-clear.
        Based on their thoughts below, help them formulate one clear, positive, and actionable intention for the day.
        
        User's thoughts: "{user_input}"
        
        Your guidance:
        """
    elif journal_mode == "Evening: Daily Log & Reflection":
        prompt = f"""
        Act as a compassionate and insightful journal guide. The user is reflecting on their day.
        Based on their daily log below, ask one deep, open-ended reflective question that helps them find a key insight or lesson.
        
        User's log: "{user_input}"
        
        Your reflective question:
        """
    elif journal_mode == "Weekly: Review & Plan":
        prompt = f"""
        Act as a strategic personal coach. The user is reviewing their past week to plan the next one.
        Based on their weekly summary below, identify one major theme or recurring obstacle and suggest one small, concrete action they can take next week to address it.
        
        User's weekly review: "{user_input}"
        
        Your strategic suggestion:
        """
    elif journal_mode == "Deep Dive: Unsent Letter":
        prompt = f"""
        Act as a wise and empathetic listener. The user is writing an 'unsent letter' to process their emotions.
        Read the letter below. Your role is NOT to give advice, but to validate their feelings and reflect their core emotion back to them in a single, supportive sentence.
        
        User's letter: "{user_input}"
        
        Your supportive reflection:
        """

    # 2. Get the response from Gemini
    with st.spinner("Your AI companion is thinking..."):
        ai_response = get_gemini_response(prompt)
        st.markdown("### AI Companion's Guidance:")
        st.write(ai_response)
else:
    if submit_button:
        st.warning("Please enter your thoughts before getting guidance.")