import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  IconButton,
  Fab,
  CircularProgress,
  Alert,
  Container,
  Card,
  CardContent,
  Divider,
} from '@mui/material';
import {
  Mic,
  Stop,
  PlayArrow,
  Send,
  VolumeUp,
  Clear,
} from '@mui/icons-material';
import { useAudioRecorder } from '../hooks/useAudioRecorder';
import { Message, ConversationState } from '../types/conversation';
import MessageBubble from './MessageBubble';

const Conversation: React.FC = () => {
  const [conversation, setConversation] = useState<ConversationState>({
    messages: [],
    isLoading: false,
    error: null,
  });

  const [isConversationActive, setIsConversationActive] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const audioPlayerRef = useRef<HTMLAudioElement>(null);

  const {
    isRecording,
    audioBlob,
    audioUrl,
    error: recordingError,
    startRecording,
    stopRecording,
    clearRecording,
  } = useAudioRecorder();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversation.messages]);

  const handleStartConversation = () => {
    setIsConversationActive(true);
  };

  const handleEndConversation = () => {
    setIsConversationActive(false);
    setConversation(prev => ({ ...prev, messages: [] }));
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setConversation(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    try {
      // TODO: Replace with actual API call
      const response = await simulateApiCall(content);
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.text,
        timestamp: new Date(),
      };

      setConversation(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        isLoading: false,
      }));

      // Play audio response if available
      if (response.audioUrl && audioPlayerRef.current) {
        audioPlayerRef.current.src = response.audioUrl;
        audioPlayerRef.current.play();
      }

    } catch (error) {
      setConversation(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to send message',
      }));
    }
  };

  const handleAudioRecording = async () => {
    if (isRecording) {
      stopRecording();
    } else {
      await startRecording();
    }
  };

  const handleProcessRecording = async () => {
    if (!audioBlob) return;

    try {
      setConversation(prev => ({ ...prev, isLoading: true, error: null }));

      // TODO: Replace with actual API call
      const response = await simulateAudioApiCall(audioBlob);
      
      const userMessage: Message = {
        role: 'user',
        content: response.text,
        timestamp: new Date(),
      };

      const assistantMessage: Message = {
        role: 'assistant',
        content: 'This is a simulated response. Backend integration pending.',
        timestamp: new Date(),
      };

      setConversation(prev => ({
        ...prev,
        messages: [...prev.messages, userMessage, assistantMessage],
        isLoading: false,
      }));

      clearRecording();

    } catch (error) {
      setConversation(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to process audio',
      }));
    }
  };

  // Temporary simulation functions - will be replaced with actual API calls
  const simulateApiCall = async (text: string): Promise<{ text: string; audioUrl?: string }> => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return {
      text: `Simulated response to: "${text}". Backend integration pending.`,
    };
  };

  const simulateAudioApiCall = async (audioBlob: Blob): Promise<{ text: string }> => {
    await new Promise(resolve => setTimeout(resolve, 1500));
    return {
      text: 'Simulated transcribed audio. Backend integration pending.',
    };
  };

  return (
    <Container maxWidth="md" sx={{ height: '100vh', py: 2 }}>
      <Paper elevation={3} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Typography variant="h5" component="h1" gutterBottom>
            🤖 Synapse Trader
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Your AI Trading Co-Pilot
          </Typography>
        </Box>

        {/* Conversation Area */}
        <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
          {!isConversationActive ? (
            <Box sx={{ textAlign: 'center', py: 8 }}>
              <Typography variant="h6" gutterBottom>
                Welcome to Synapse Trader
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Start a conversation to begin trading assistance
              </Typography>
              <Fab
                variant="extended"
                color="primary"
                onClick={handleStartConversation}
                sx={{ mt: 2 }}
              >
                <Mic sx={{ mr: 1 }} />
                Start Conversation
              </Fab>
            </Box>
          ) : (
            <>
              {/* Messages */}
              <Box sx={{ mb: 2 }}>
                {conversation.messages.map((message, index) => (
                  <MessageBubble key={index} message={message} />
                ))}
                {conversation.isLoading && (
                  <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
                    <CircularProgress size={24} />
                  </Box>
                )}
                <div ref={messagesEndRef} />
              </Box>

              {/* Error Display */}
              {(conversation.error || recordingError) && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {conversation.error || recordingError}
                </Alert>
              )}

              {/* Audio Recording Display */}
              {audioUrl && (
                <Card sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>
                      Recorded Audio
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <audio controls src={audioUrl} style={{ flex: 1 }} />
                      <IconButton
                        color="primary"
                        onClick={handleProcessRecording}
                        disabled={conversation.isLoading}
                      >
                        <Send />
                      </IconButton>
                      <IconButton onClick={clearRecording}>
                        <Clear />
                      </IconButton>
                    </Box>
                  </CardContent>
                </Card>
              )}
            </>
          )}
        </Box>

        {/* Audio Player */}
        <audio ref={audioPlayerRef} style={{ display: 'none' }} />

        {/* Controls */}
        {isConversationActive && (
          <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
              <Fab
                color={isRecording ? 'error' : 'primary'}
                onClick={handleAudioRecording}
                disabled={conversation.isLoading}
              >
                {isRecording ? <Stop /> : <Mic />}
              </Fab>
              
              <Fab
                variant="extended"
                color="secondary"
                onClick={handleEndConversation}
                disabled={conversation.isLoading}
              >
                End Conversation
              </Fab>
            </Box>
            
            {isRecording && (
              <Box sx={{ textAlign: 'center', mt: 1 }}>
                <Typography variant="caption" color="error">
                  Recording... Click to stop
                </Typography>
              </Box>
            )}
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default Conversation; 