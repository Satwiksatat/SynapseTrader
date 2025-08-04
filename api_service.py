"""
API Service module for handling audio processing and API calls.
"""

import os
import io
import base64
import tempfile
from typing import Optional, Dict, Any
from fastapi import HTTPException
from elevenlabs.client import ElevenLabs

class APIService:
    def __init__(self):
        self.eleven_client = None
        self.initialize_elevenlabs()
        
        # Constants
        self.DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
        self.DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
        self.STT_MODEL_ID = os.getenv("STT_MODEL_ID", "scribe_v1")
    
    def initialize_elevenlabs(self):
        """Initialize ElevenLabs client."""
        try:
            api_key = os.getenv("ELEVENLABS_API_KEY")
            if not api_key:
                print("Warning: ELEVENLABS_API_KEY not found in environment variables")
                return
                
            self.eleven_client = ElevenLabs(api_key=api_key)
            print("ElevenLabs client initialized successfully")
        except Exception as e:
            print(f"Error initializing ElevenLabs client: {e}")
            self.eleven_client = None
    
    def process_audio_to_text(self, audio_bytes: bytes) -> str:
        """
        Convert audio bytes to text using ElevenLabs API.
        
        Args:
            audio_bytes: Raw audio data
            
        Returns:
            str: Transcribed text
        """
        if not self.eleven_client:
            raise HTTPException(status_code=500, detail="ElevenLabs client not initialized")
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_bytes)
                temp_path = temp_file.name
            
            # Process with ElevenLabs
            with open(temp_path, "rb") as f:
                response = self.eleven_client.speech_to_text.convert(
                    file=f, 
                    model_id=self.STT_MODEL_ID
                )
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return response.text
            
        except Exception as e:
            # Clean up temp file if it exists
            if 'temp_path' in locals():
                try:
                    os.unlink(temp_path)
                except:
                    pass
            
            raise HTTPException(status_code=500, detail=f"Error in speech-to-text: {str(e)}")
    
    def process_text_to_speech(self, text: str) -> bytes:
        """
        Convert text to speech using ElevenLabs API.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            bytes: Audio data
        """
        if not self.eleven_client:
            raise HTTPException(status_code=500, detail="ElevenLabs client not initialized")
        
        try:
            # Generate audio
            audio_stream = self.eleven_client.text_to_speech.convert(
                text=text,
                voice_id=self.DEFAULT_VOICE_ID,
                model_id=self.DEFAULT_MODEL_ID,
                output_format="mp3_44100_128",
            )
            
            # Convert to bytes
            audio_bytes = b"".join(audio_stream)
            return audio_bytes
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in text-to-speech: {str(e)}")
    
    def create_audio_data_url(self, audio_bytes: bytes) -> str:
        """
        Create a data URL for audio bytes.
        
        Args:
            audio_bytes: Raw audio data
            
        Returns:
            str: Data URL
        """
        try:
            base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
            return f"data:audio/mpeg;base64,{base64_audio}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating audio data URL: {str(e)}")
    
    def validate_audio_file(self, audio_bytes: bytes, max_size: int = 10 * 1024 * 1024) -> bool:
        """
        Validate audio file size and format.
        
        Args:
            audio_bytes: Raw audio data
            max_size: Maximum file size in bytes (default: 10MB)
            
        Returns:
            bool: True if valid
        """
        if len(audio_bytes) > max_size:
            raise HTTPException(status_code=400, detail=f"Audio file too large. Maximum size: {max_size} bytes")
        
        if len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        return True
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get API service health status.
        
        Returns:
            Dict containing health information
        """
        return {
            "elevenlabs_connected": self.eleven_client is not None,
            "voice_id": self.DEFAULT_VOICE_ID,
            "tts_model_id": self.DEFAULT_MODEL_ID,
            "stt_model_id": self.STT_MODEL_ID,
        }

# Global API service instance
api_service = APIService() 