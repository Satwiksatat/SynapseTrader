"""
Main entry point for the Synapse Trader application.
Handles UI rendering and orchestrates the workflow between user input and AI responses.
"""

import streamlit as st
from elevenlabs import generate, play
from agent import process_user_input
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_session_state():
    """Initialize session state variables."""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def generate_and_play_audio(text):
    """Generate and play audio response using ElevenLabs."""
    try:
        audio = generate(
            text=text,
            api_key=os.getenv('ELEVENLABS_API_KEY')
        )
        # Save audio to file
        audio_path = "audio_outputs/response.mp3"
        with open(audio_path, "wb") as f:
            f.write(audio)
        # Play the audio
        st.audio(audio_path)
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")

def main():
    st.set_page_config(
        page_title="Synapse Trader",
        page_icon="assets/logo.png"
    )

    st.title("🤖 Synapse Trader")
    st.subheader("Your AI Trading Co-Pilot")

    # Initialize session state
    initialize_session_state()

    # User input section
    user_input = st.text_input("Enter your trading query:", key="user_input")
    
    if st.button("Submit"):
        if user_input:
            # Add user message to history
            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            
            # Process user input through the AI agent
            response = process_user_input(user_input)
            
            # Add AI response to history
            st.session_state.conversation_history.append({"role": "assistant", "content": response})
            
            # Generate and play audio response
            generate_and_play_audio(response)

    # Display conversation history
    st.subheader("Conversation History")
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.write("You: " + message["content"])
        else:
            st.write("Assistant: " + message["content"])

if __name__ == "__main__":
    main()