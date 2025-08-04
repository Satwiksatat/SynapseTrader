# Synapse Trader

An AI-powered trading assistant with voice interaction capabilities.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- ElevenLabs API key

### 1. Backend Setup

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory with:
   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ELEVENLABS_VOICE_ID=JBFqnCBsd6RMkjVDRZzb
   ELEVENLABS_MODEL_ID=eleven_multilingual_v2
   STT_MODEL_ID=scribe_v1
   ```

4. **Start the FastAPI backend:**
   ```bash
   python start_backend.py
   ```
   
   Or directly with uvicorn:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The backend will be available at:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

### 2. Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```

   The frontend will be available at: http://localhost:3000

## 📁 Project Structure

```
SynapseTrader/
├── main.py                 # FastAPI backend
├── api_service.py          # API service utilities
├── agent.py               # AI agent logic
├── tools.py               # Trading tools
├── start_backend.py       # Backend startup script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   ├── hooks/         # Custom hooks
│   │   └── types/         # TypeScript types
│   └── package.json
└── venv/                  # Python virtual environment
```

## 🔧 API Endpoints

### Chat & Voice
- `POST /api/chat` - Send text message
- `POST /api/audio-chat` - Send audio message (combines STT + chat + TTS)
- `POST /api/speech-to-text` - Convert audio to text
- `POST /api/text-to-speech` - Convert text to speech

### Conversation Management
- `GET /api/conversation-history` - Get conversation history
- `DELETE /api/conversation-history` - Clear conversation history

### System
- `GET /api/health` - Health check
- `GET /api/status` - Detailed status
- `GET /` - API information

## 🎯 Features

### Backend (FastAPI)
- ✅ AI-powered chat responses
- ✅ Speech-to-Text conversion
- ✅ Text-to-Speech generation
- ✅ Conversation history management
- ✅ Audio processing and validation
- ✅ CORS support for frontend
- ✅ Comprehensive error handling
- ✅ API documentation (Swagger UI)

### Frontend (React)
- ✅ Modern, professional trading UI
- ✅ Real-time voice recording
- ✅ Animated components and gradients
- ✅ Responsive design
- ✅ Audio playback
- ✅ Conversation management
- ✅ Material-UI components

## 🔍 Troubleshooting

### Backend Issues
1. **Missing dependencies:** Run `pip install -r requirements.txt`
2. **Environment variables:** Ensure `.env` file exists with required keys
3. **Port conflicts:** Change port in `start_backend.py` or use different port
4. **ElevenLabs errors:** Check API key and internet connection

### Frontend Issues
1. **Dependencies:** Run `npm install` in frontend directory
2. **Port conflicts:** React will automatically suggest alternative ports
3. **API connection:** Ensure backend is running on http://localhost:8000
4. **Audio issues:** Check browser permissions for microphone access

### Common Commands

**Start both services:**
```bash
# Terminal 1 - Backend
source venv/bin/activate
python start_backend.py

# Terminal 2 - Frontend
cd frontend
npm start
```

**Check if services are running:**
```bash
# Backend health check
curl http://localhost:8000/api/health

# Frontend (should show React app)
curl http://localhost:3000
```

## 🛠️ Development

### Backend Development
- The backend uses FastAPI with automatic reload
- API documentation is available at http://localhost:8000/docs
- All endpoints are tested and documented

### Frontend Development
- React with TypeScript
- Material-UI for components
- Framer Motion for animations
- Web Audio API for recording

## 📝 Environment Variables

Required in `.env` file:
```
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=JBFqnCBsd6RMkjVDRZzb
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
STT_MODEL_ID=scribe_v1
```

## 🎉 Usage

1. Start both backend and frontend
2. Open http://localhost:3000 in your browser
3. Click "Start Conversation" to begin
4. Use the microphone button to record voice messages
5. The AI will respond with both text and audio

The application is now ready for AI-powered trading conversations with voice interaction!
