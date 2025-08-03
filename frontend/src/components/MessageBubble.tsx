import React from 'react';
import { Box, Typography, Paper, IconButton } from '@mui/material';
import { VolumeUp } from '@mui/icons-material';
import { Message } from '../types/conversation';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  const formatTime = (timestamp?: Date) => {
    if (!timestamp) return '';
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        mb: 2,
      }}
    >
      <Paper
        elevation={1}
        sx={{
          maxWidth: '70%',
          p: 2,
          backgroundColor: isUser ? 'primary.main' : 'grey.100',
          color: isUser ? 'white' : 'text.primary',
          borderRadius: 2,
          position: 'relative',
        }}
      >
        <Typography variant="body1" sx={{ wordBreak: 'break-word' }}>
          {message.content}
        </Typography>
        
        {message.timestamp && (
          <Typography
            variant="caption"
            sx={{
              display: 'block',
              mt: 1,
              opacity: 0.7,
              fontSize: '0.75rem',
            }}
          >
            {formatTime(message.timestamp)}
          </Typography>
        )}
        
        {!isUser && (
          <IconButton
            size="small"
            sx={{
              position: 'absolute',
              top: 4,
              right: 4,
              color: 'primary.main',
            }}
            onClick={() => {
              // TODO: Implement text-to-speech playback
              console.log('Play audio for:', message.content);
            }}
          >
            <VolumeUp fontSize="small" />
          </IconButton>
        )}
      </Paper>
    </Box>
  );
};

export default MessageBubble; 