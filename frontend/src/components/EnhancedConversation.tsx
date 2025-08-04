import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Box,
  Typography,
  IconButton,
  Fab,
  CircularProgress,
  Alert,
  Container,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import {
  Mic,
  Stop,
  Send,
  VolumeUp,
  Clear,
  SmartToy,
  TrendingUp,
  AccountCircle,
} from '@mui/icons-material';
import { Message, ConversationState } from '../types/conversation';
import { ApiService } from '../services/api';
import AnimatedMessageBubble from './AnimatedMessageBubble';
import AnimatedAudioRecorder from './AnimatedAudioRecorder';
import TradingHeader from './TradingHeader';
import AnimatedBackground from './AnimatedBackground';

const EnhancedConversation: React.FC = () => {
  const [conversation, setConversation] = useState<ConversationState>({
    messages: [],
    isLoading: false,
    error: null,
  });

  const [isConversationActive, setIsConversationActive] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const audioPlayerRef = useRef<HTMLAudioElement>(null);

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
      // Use real API call
      const response = await ApiService.sendTextMessage(content);
      
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
      if (response.audio_url && audioPlayerRef.current) {
        audioPlayerRef.current.src = response.audio_url;
        audioPlayerRef.current.play();
      }

    } catch (error) {
      setConversation(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'An error occurred',
      }));
    }
  };

  const handleProcessRecording = async (audioBlob: Blob) => {
    setConversation(prev => ({
      ...prev,
      isLoading: true,
      error: null,
    }));

    try {
      // Use real API call for audio processing
      const response = await ApiService.sendAudioMessage(audioBlob);
      
      const userMessage: Message = {
        role: 'user',
        content: `[Voice Message]`,
        timestamp: new Date(),
      };

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.text,
        timestamp: new Date(),
      };

      setConversation(prev => ({
        ...prev,
        messages: [...prev.messages, userMessage, assistantMessage],
        isLoading: false,
      }));

      // Play audio response if available
      if (response.audio_url && audioPlayerRef.current) {
        audioPlayerRef.current.src = response.audio_url;
        audioPlayerRef.current.play();
      }

    } catch (error) {
      setConversation(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'An error occurred',
      }));
    }
  };

  // Remove the simulated API calls since we're using real ones now
  // const simulateApiCall = async (text: string): Promise<{ text: string; audioUrl?: string }> => {
  //   await new Promise(resolve => setTimeout(resolve, 1000));
  //   return {
  //     text: `This is a simulated response to: "${text}". In a real implementation, this would be the AI's response.`,
  //     audioUrl: undefined,
  //   };
  // };

  // const simulateAudioApiCall = async (audioBlob: Blob): Promise<{ text: string }> => {
  //   await new Promise(resolve => setTimeout(resolve, 1500));
  //   return {
  //     text: "This is a simulated response to your voice message. The audio was processed and converted to text.",
  //   };
  // };

  return (
    <>
      <AnimatedBackground />
      <Container maxWidth="lg" sx={{ height: '100vh', py: 2, position: 'relative', zIndex: 1 }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Card
            sx={{
              height: '100%',
              background: 'linear-gradient(135deg, rgba(26, 31, 46, 0.9) 0%, rgba(42, 47, 62, 0.9) 100%)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <TradingHeader />
            <Box sx={{ flex: 1, overflow: 'auto', p: 3, position: 'relative' }}>
              <AnimatePresence>
                {!isConversationActive ? (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5 }}
                    style={{ textAlign: 'center', padding: '4rem 2rem' }}
                  >
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.2 }}
                    >
                      <Typography
                        variant="h3"
                        sx={{
                          background: 'linear-gradient(135deg, #00d4ff 0%, #ff6b35 100%)',
                          WebkitBackgroundClip: 'text',
                          WebkitTextFillColor: 'transparent',
                          backgroundClip: 'text',
                          fontWeight: 700,
                          mb: 2,
                        }}
                      >
                        Welcome to Synapse Trader
                      </Typography>
                    </motion.div>
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.4 }}
                    >
                      <Typography
                        variant="h6"
                        sx={{
                          color: '#b0b8c1',
                          mb: 4,
                          fontWeight: 400,
                        }}
                      >
                        Your AI-powered trading assistant
                      </Typography>
                    </motion.div>
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.6 }}
                    >
                      <Fab
                        variant="extended"
                        size="large"
                        onClick={handleStartConversation}
                        sx={{
                          background: 'linear-gradient(135deg, #00d4ff 0%, #ff6b35 100%)',
                          color: 'white',
                          px: 4,
                          py: 2,
                          fontSize: '1.1rem',
                          fontWeight: 600,
                          '&:hover': {
                            background: 'linear-gradient(135deg, #00b8e6 0%, #e55a2b 100%)',
                            transform: 'translateY(-2px)',
                            boxShadow: '0 8px 25px rgba(0, 212, 255, 0.3)',
                          },
                        }}
                      >
                        <Mic sx={{ mr: 1 }} />
                        Start Conversation
                      </Fab>
                    </motion.div>
                  </motion.div>
                ) : (
                  <>
                    <Box sx={{ mb: 3 }}>
                      {conversation.messages.map((message, index) => (
                        <AnimatedMessageBubble
                          key={index}
                          message={message}
                          index={index}
                        />
                      ))}
                      {conversation.isLoading && (
                        <motion.div
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          style={{ display: 'flex', justifyContent: 'center', margin: '2rem 0' }}
                        >
                          <CircularProgress
                            sx={{
                              color: '#00d4ff',
                              '& .MuiCircularProgress-circle': {
                                strokeLinecap: 'round',
                              },
                            }}
                          />
                        </motion.div>
                      )}
                      {conversation.error && (
                        <motion.div
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          style={{ margin: '1rem 0' }}
                        >
                          <Alert severity="error" sx={{ borderRadius: 2 }}>
                            {conversation.error}
                          </Alert>
                        </motion.div>
                      )}
                    </Box>
                    <div ref={messagesEndRef} />
                  </>
                )}
              </AnimatePresence>
            </Box>
            <audio ref={audioPlayerRef} style={{ display: 'none' }} />
            {isConversationActive && (
              <Box
                sx={{
                  p: 3,
                  borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                  background: 'rgba(26, 31, 46, 0.5)',
                }}
              >
                <AnimatedAudioRecorder
                  onProcessRecording={handleProcessRecording}
                  isLoading={conversation.isLoading}
                />
              </Box>
            )}
          </Card>
        </motion.div>
      </Container>
    </>
  );
};

export default EnhancedConversation; 