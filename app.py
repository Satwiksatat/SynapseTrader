"""
Main entry point for the Synapse Trader application.
Handles UI rendering and orchestrates the workflow between user input and AI responses.
"""

import streamlit as st
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from agent import process_user_input
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------------------------------------------------------------------------
# ElevenLabs client
# ---------------------------------------------------------------------------

eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")

def initialize_session_state():
    """Initialize session state variables."""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def generate_and_play_audio(text: str):
    """Generate TTS via ElevenLabs SDK and play inside Streamlit."""
    try:
        # The official SDK returns raw bytes.
        result = eleven_client.text_to_speech.convert(
            text=text,
            voice_id=DEFAULT_VOICE_ID,
            model_id=DEFAULT_MODEL_ID,
            output_format="mp3_44100_128",
        )
        # The SDK may return bytes *or* a generator of bytes depending on size/model.
        if isinstance(result, (bytes, bytearray)):
            audio_bytes = result
        else:
            # Assume it's an iterator / generator of byte chunks
            audio_bytes = b"".join(result)

        # Persist to a deterministic path so Streamlit can reload between reruns
        os.makedirs("audio_outputs", exist_ok=True)
        audio_path = "audio_outputs/response.mp3"
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        # Optionally play through local speakers (during dev only)
        try:
            play(audio_bytes)
        except Exception:
            # Ignore playback errors (e.g., server environment)
            pass

        # Streamlit audio component
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