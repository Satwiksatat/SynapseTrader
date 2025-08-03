"""
Main entry point for the Synapse Trader application.
Handles UI rendering and orchestrates the workflow between user input and AI responses.
"""

from csv import Error
import streamlit as st
from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv
from agent import process_user_input
from streamlit_mic_recorder import mic_recorder
import io

# Load environment variables
load_dotenv()

# --- ElevenLabs client initialization ---
try:
    eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
except Exception as e:
    st.error(f"Error initializing ElevenLabs client: {e}")
    st.stop()

DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
STT_MODEL_ID = os.getenv("STT_MODEL_ID", "scribe_v1")

def initialize_session_state():
    """Initialize session state variables."""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'conversation_active' not in st.session_state:
        st.session_state.conversation_active = False
    if 'last_audio_id' not in st.session_state:
        st.session_state.last_audio_id = None
    if 'audio_to_play' not in st.session_state:
        st.session_state.audio_to_play = None

def generate_speech(text: str):
    """Generate TTS via ElevenLabs SDK and store it in session state."""
    try:
        audio_stream = eleven_client.text_to_speech.convert(
            text=text,
            voice_id=DEFAULT_VOICE_ID,
            model_id=DEFAULT_MODEL_ID,
            output_format="mp3_44100_128",
        )
        
        # Convert the audio stream to bytes
        audio_bytes = b"".join(audio_stream)
        
        st.session_state.audio_to_play = audio_bytes
        
    except Exception as e:
        print(e)
        st.error(f"Error generating audio: {str(e)}")

def speech_to_text(audio_bytes):
    """Transcribe audio to text using ElevenLabs API."""
    try:
        audio_path = "audio_inputs/recorded_audio.wav"
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)
        
        with open(audio_path, "rb") as f:
            response = eleven_client.speech_to_text.convert(file=f, model_id=STT_MODEL_ID)
        
        return response.text
    except Exception as e:
        st.error(f"Error in speech-to-text conversion: {e}")
        return None

def process_voice_input(audio_bytes):
    """Record, transcribe, process, and play response."""
    transcribed_text = speech_to_text(audio_bytes)
    if transcribed_text:
        st.session_state.conversation_history.append({"role": "user", "content": transcribed_text})
        
        with st.spinner("Processing your query..."):
            response = process_user_input(transcribed_text)
        
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        
        generate_speech(response)
        st.rerun()

def main():
    st.set_page_config(
        page_title="Synapse Trader",
        page_icon="🤖"
    )

    st.title("🤖 Synapse Trader")
    st.subheader("Your AI Trading Co-Pilot")

    # Placeholder for the audio player
    audio_placeholder = st.empty()

    initialize_session_state()

    if st.session_state.audio_to_play:
        audio_placeholder.audio(st.session_state.audio_to_play, autoplay=True)
        st.session_state.audio_to_play = None

    # Display conversation history
    st.subheader("Conversation History")
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if not st.session_state.conversation_active:
        if st.button("Start Conversation"):
            st.session_state.conversation_active = True
            st.rerun()

    if st.session_state.conversation_active:
        audio = mic_recorder(start_prompt="Click to record", stop_prompt="Click to stop", key='recorder')
        if audio and audio['id'] != st.session_state.last_audio_id:
            st.session_state.last_audio_id = audio['id']
            process_voice_input(audio['bytes'])

        if st.button("End Conversation"):
            st.session_state.conversation_active = False
            st.rerun()

if __name__ == "__main__":
    os.makedirs("audio_inputs", exist_ok=True)
    os.makedirs("audio_outputs", exist_ok=True)
    main()
