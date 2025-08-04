import React from 'react';
import { motion } from 'framer-motion';
import {
  Box,
  Typography,
  IconButton,
  Chip,
  Avatar,
} from '@mui/material';
import {
  VolumeUp,
  TrendingUp,
  TrendingDown,
  AccountCircle,
  SmartToy,
} from '@mui/icons-material';
import { Message } from '../types/conversation';

interface AnimatedMessageBubbleProps {
  message: Message;
  index: number;
}

const AnimatedMessageBubble: React.FC<AnimatedMessageBubbleProps> = ({ message, index }) => {
  const isUser = message.role === 'user';
  
  const formatTime = (timestamp?: Date) => {
    if (!timestamp) return '';
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getMessageGradient = () => {
    if (isUser) {
      return 'linear-gradient(135deg, #00d4ff 0%, #0099cc 100%)';
    }
    return 'linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 100%)';
  };

  const getBorderGradient = () => {
    if (isUser) {
      return 'linear-gradient(135deg, #00d4ff 0%, #4ddbff 100%)';
    }
    return 'linear-gradient(135deg, #ff6b35 0%, #ff8a65 100%)';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{
        duration: 0.4,
        delay: index * 0.1,
        ease: 'easeOut',
      }}
      whileHover={{ scale: 1.02 }}
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: isUser ? 'flex-end' : 'flex-start',
          mb: 2,
          alignItems: 'flex-start',
          gap: 1,
        }}
      >
        {/* Avatar */}
        {!isUser && (
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 + 0.2 }}
          >
            <Avatar
              sx={{
                background: 'linear-gradient(135deg, #ff6b35 0%, #e65100 100%)',
                width: 40,
                height: 40,
                mt: 1,
              }}
            >
              <SmartToy />
            </Avatar>
          </motion.div>
        )}

        {/* Message Content */}
        <Box sx={{ maxWidth: '70%', position: 'relative' }}>
          <motion.div
            initial={{ opacity: 0, x: isUser ? 20 : -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 + 0.1 }}
          >
            <Box
              sx={{
                position: 'relative',
                background: getMessageGradient(),
                borderRadius: 3,
                p: 2,
                border: `2px solid transparent`,
                backgroundClip: 'padding-box',
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  borderRadius: 3,
                  padding: '2px',
                  background: getBorderGradient(),
                  WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
                  WebkitMaskComposite: 'xor',
                  maskComposite: 'exclude',
                },
                boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
              }}
            >
              {/* Message Header */}
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <Chip
                  label={isUser ? 'You' : 'Synapse AI'}
                  size="small"
                  sx={{
                    background: isUser 
                      ? 'linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(0, 153, 204, 0.2) 100%)'
                      : 'linear-gradient(135deg, rgba(255, 107, 53, 0.2) 0%, rgba(230, 81, 0, 0.2) 100%)',
                    color: '#ffffff',
                    fontWeight: 600,
                    fontSize: '0.75rem',
                  }}
                />
                {message.timestamp && (
                  <Typography
                    variant="caption"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontSize: '0.7rem',
                    }}
                  >
                    {formatTime(message.timestamp)}
                  </Typography>
                )}
              </Box>

              {/* Message Text */}
              <Typography
                variant="body1"
                sx={{
                  color: '#ffffff',
                  wordBreak: 'break-word',
                  lineHeight: 1.5,
                  fontWeight: 400,
                }}
              >
                {message.content}
              </Typography>

              {/* Action Buttons */}
              {!isUser && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: index * 0.1 + 0.3 }}
                >
                  <Box sx={{ display: 'flex', gap: 1, mt: 1, pt: 1, borderTop: '1px solid rgba(255, 255, 255, 0.1)' }}>
                    <IconButton
                      size="small"
                      sx={{
                        background: 'rgba(255, 255, 255, 0.1)',
                        color: '#00d4ff',
                        '&:hover': {
                          background: 'rgba(0, 212, 255, 0.2)',
                          transform: 'scale(1.1)',
                        },
                        transition: 'all 0.2s ease-in-out',
                      }}
                      onClick={() => {
                        // TODO: Implement text-to-speech playback
                        console.log('Play audio for:', message.content);
                      }}
                    >
                      <VolumeUp fontSize="small" />
                    </IconButton>
                    
                    <IconButton
                      size="small"
                      sx={{
                        background: 'rgba(255, 255, 255, 0.1)',
                        color: '#00ff88',
                        '&:hover': {
                          background: 'rgba(0, 255, 136, 0.2)',
                          transform: 'scale(1.1)',
                        },
                        transition: 'all 0.2s ease-in-out',
                      }}
                    >
                      <TrendingUp fontSize="small" />
                    </IconButton>
                  </Box>
                </motion.div>
              )}
            </Box>
          </motion.div>
        </Box>

        {/* User Avatar */}
        {isUser && (
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 + 0.2 }}
          >
            <Avatar
              sx={{
                background: 'linear-gradient(135deg, #00d4ff 0%, #0099cc 100%)',
                width: 40,
                height: 40,
                mt: 1,
              }}
            >
              <AccountCircle />
            </Avatar>
          </motion.div>
        )}
      </Box>
    </motion.div>
  );
};

export default AnimatedMessageBubble; 