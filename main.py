"""
FastAPI backend for Synapse Trader application.
Handles API endpoints for chat, speech-to-text, and text-to-speech.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import io
import json
from datetime import datetime
from dotenv import load_dotenv

# Import existing modules
from agent import process_user_input
from api_service import api_service

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Synapse Trader API",
    description="AI-powered trading assistant API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    text: str
    audio_url: Optional[str] = None

class SpeechToTextResponse(BaseModel):
    text: str

class TextToSpeechRequest(BaseModel):
    text: str

class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ConversationHistoryResponse(BaseModel):
    messages: List[Message]

# In-memory conversation storage (replace with database in production)
conversation_history = []

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Synapse Trader API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process text message and return AI response.
    """
    try:
        # Add user message to history
        user_message = {
            "role": "user",
            "content": request.text,
            "timestamp": datetime.now().isoformat()
        }
        conversation_history.append(user_message)
        
        # Process with AI agent
        response_text = process_user_input(request.text)
        
        # Add assistant message to history
        assistant_message = {
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        }
        conversation_history.append(assistant_message)
        
        # Generate audio response
        audio_url = None
        try:
            audio_bytes = api_service.process_text_to_speech(response_text)
            audio_url = api_service.create_audio_data_url(audio_bytes)
        except Exception as e:
            print(f"Error generating audio: {e}")
        
        return ChatResponse(
            text=response_text,
            audio_url=audio_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/api/speech-to-text", response_model=SpeechToTextResponse)
async def speech_to_text_endpoint(audio: UploadFile = File(...)):
    """
    Convert audio to text using ElevenLabs API.
    """
    try:
        # Read audio file
        audio_bytes = await audio.read()
        
        # Validate audio file
        api_service.validate_audio_file(audio_bytes)
        
        # Process audio to text
        transcribed_text = api_service.process_audio_to_text(audio_bytes)
        
        return SpeechToTextResponse(text=transcribed_text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in speech-to-text: {str(e)}")

@app.post("/api/text-to-speech")
async def text_to_speech_endpoint(request: TextToSpeechRequest):
    """
    Convert text to speech using ElevenLabs API.
    """
    try:
        # Generate audio
        audio_bytes = api_service.process_text_to_speech(request.text)
        
        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in text-to-speech: {str(e)}")

@app.post("/api/audio-chat", response_model=ChatResponse)
async def audio_chat_endpoint(audio: UploadFile = File(...)):
    """
    Process audio input and return AI response with audio.
    This combines speech-to-text and chat functionality.
    """
    try:
        # Read and validate audio file
        audio_bytes = await audio.read()
        api_service.validate_audio_file(audio_bytes)
        
        # Convert audio to text
        transcribed_text = api_service.process_audio_to_text(audio_bytes)
        
        # Add user message to history
        user_message = {
            "role": "user",
            "content": transcribed_text,
            "timestamp": datetime.now().isoformat()
        }
        conversation_history.append(user_message)
        
        # Process with AI agent
        response_text = process_user_input(transcribed_text)
        
        # Add assistant message to history
        assistant_message = {
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        }
        conversation_history.append(assistant_message)
        
        # Generate audio response
        audio_url = None
        try:
            audio_bytes = api_service.process_text_to_speech(response_text)
            audio_url = api_service.create_audio_data_url(audio_bytes)
        except Exception as e:
            print(f"Error generating audio: {e}")
        
        return ChatResponse(
            text=response_text,
            audio_url=audio_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio chat: {str(e)}")

@app.get("/api/conversation-history", response_model=ConversationHistoryResponse)
async def get_conversation_history():
    """
    Get conversation history.
    """
    try:
        messages = []
        for msg in conversation_history:
            messages.append(Message(
                role=msg["role"],
                content=msg["content"],
                timestamp=msg.get("timestamp")
            ))
        
        return ConversationHistoryResponse(messages=messages)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting conversation history: {str(e)}")

@app.delete("/api/conversation-history")
async def clear_conversation_history():
    """
    Clear conversation history.
    """
    try:
        conversation_history.clear()
        return {"message": "Conversation history cleared"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing conversation history: {str(e)}")

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.
    """
    try:
        api_health = api_service.get_health_status()
        return {
            "status": "healthy",
            "conversation_count": len(conversation_history),
            "api_service": api_health
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "conversation_count": len(conversation_history)
        }

@app.get("/api/status")
async def status_endpoint():
    """
    Detailed status endpoint.
    """
    return {
        "service": "Synapse Trader API",
        "version": "1.0.0",
        "status": "running",
        "features": {
            "chat": True,
            "speech_to_text": True,
            "text_to_speech": True,
            "conversation_history": True
        },
        "endpoints": {
            "chat": "/api/chat",
            "speech_to_text": "/api/speech-to-text",
            "text_to_speech": "/api/text-to-speech",
            "audio_chat": "/api/audio-chat",
            "conversation_history": "/api/conversation-history",
            "health": "/api/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 