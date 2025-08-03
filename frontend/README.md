# Synapse Trader Frontend

A React TypeScript application for the Synapse Trader AI trading assistant with voice capabilities.

## Features

- 🎤 **Voice Recording**: Record audio using Web Audio API
- 💬 **Chat Interface**: Professional chat UI with Material-UI
- 🔊 **Audio Playback**: Play AI responses with text-to-speech
- 📱 **Responsive Design**: Works on desktop and mobile
- 🎨 **Modern UI**: Clean, professional interface

## Technology Stack

- **React 18** with TypeScript
- **Material-UI** for components and theming
- **Web Audio API** for audio recording
- **HTML5 Audio** for playback

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
├── components/
│   ├── Conversation.tsx      # Main conversation component
│   └── MessageBubble.tsx     # Individual message display
├── hooks/
│   └── useAudioRecorder.ts   # Audio recording hook
├── services/
│   └── api.ts               # API service for backend communication
├── types/
│   └── conversation.ts       # TypeScript interfaces
└── App.tsx                  # Main app component
```

## Usage

1. **Start Conversation**: Click the "Start Conversation" button
2. **Record Audio**: Click the microphone button to start recording
3. **Send Message**: Click the send button to process the recording
4. **View Responses**: AI responses appear in the chat interface
5. **End Conversation**: Click "End Conversation" to reset

## Backend Integration

The frontend is designed to work with a FastAPI backend. API endpoints expected:

- `POST /api/chat` - Send text messages
- `POST /api/speech-to-text` - Process audio recordings
- `POST /api/text-to-speech` - Generate audio from text
- `GET /api/conversation-history` - Get chat history

## Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## Browser Compatibility

- Chrome 66+
- Firefox 60+
- Safari 11.1+
- Edge 79+

## Audio Format

The application records audio in WebM format with Opus codec for optimal quality and file size.

## Development Notes

- Audio recording requires HTTPS in production (browser security)
- Web Audio API requires user permission for microphone access
- The app includes simulated API calls for development/testing
