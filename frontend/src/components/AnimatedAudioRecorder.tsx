import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Box,
  Typography,
  IconButton,
  Card,
  CardContent,
  LinearProgress,
} from '@mui/material';
import {
  Mic,
  Stop,
  Send,
  Clear,
  VolumeUp,
  Pause,
  PlayArrow,
} from '@mui/icons-material';
import { useAudioRecorder } from '../hooks/useAudioRecorder';

interface AnimatedAudioRecorderProps {
  onProcessRecording: (audioBlob: Blob) => void;
  isLoading?: boolean;
}

const AnimatedAudioRecorder: React.FC<AnimatedAudioRecorderProps> = ({
  onProcessRecording,
  isLoading = false,
}) => {
  const {
    isRecording,
    audioBlob,
    audioUrl,
    error: recordingError,
    startRecording,
    stopRecording,
    clearRecording,
  } = useAudioRecorder();

  const handleRecordingToggle = async () => {
    if (isRecording) {
      stopRecording();
    } else {
      await startRecording();
    }
  };

  const handleProcessRecording = () => {
    if (audioBlob) {
      onProcessRecording(audioBlob);
      clearRecording();
    }
  };

  return (
    <Box sx={{ position: 'relative' }}>
      {/* Recording Button */}
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            mb: 2,
          }}
        >
          <motion.div
            animate={{
              scale: isRecording ? [1, 1.1, 1] : 1,
              boxShadow: isRecording 
                ? ['0 0 0 0 rgba(255, 107, 53, 0.4)', '0 0 0 10px rgba(255, 107, 53, 0)', '0 0 0 0 rgba(255, 107, 53, 0)']
                : '0 4px 15px rgba(0, 212, 255, 0.3)',
            }}
            transition={{
              scale: { duration: 0.5, repeat: isRecording ? Infinity : 0 },
              boxShadow: { duration: 1, repeat: isRecording ? Infinity : 0 },
            }}
          >
            <IconButton
              onClick={handleRecordingToggle}
              disabled={isLoading}
              sx={{
                width: 80,
                height: 80,
                background: isRecording
                  ? 'linear-gradient(135deg, #ff6b35 0%, #e65100 100%)'
                  : 'linear-gradient(135deg, #00d4ff 0%, #0099cc 100%)',
                color: '#ffffff',
                '&:hover': {
                  background: isRecording
                    ? 'linear-gradient(135deg, #ff8a65 0%, #ff6b35 100%)'
                    : 'linear-gradient(135deg, #4ddbff 0%, #00d4ff 100%)',
                },
                '&:disabled': {
                  opacity: 0.6,
                },
              }}
            >
              {isRecording ? <Stop /> : <Mic />}
            </IconButton>
          </motion.div>
        </Box>
      </motion.div>

      {/* Recording Status */}
      <AnimatePresence>
        {isRecording && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Box sx={{ textAlign: 'center', mb: 2 }}>
              <motion.div
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1, repeat: Infinity }}
              >
                <Typography
                  variant="body2"
                  sx={{
                    color: '#ff6b35',
                    fontWeight: 600,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: 1,
                  }}
                >
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.5, repeat: Infinity }}
                  >
                    ●
                  </motion.div>
                  Recording... Click to stop
                </Typography>
              </motion.div>
              
              <LinearProgress
                sx={{
                  mt: 1,
                  height: 4,
                  borderRadius: 2,
                  background: 'rgba(255, 107, 53, 0.2)',
                  '& .MuiLinearProgress-bar': {
                    background: 'linear-gradient(90deg, #ff6b35 0%, #ff8a65 100%)',
                  },
                }}
              />
            </Box>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error Display */}
      <AnimatePresence>
        {recordingError && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Typography
              variant="body2"
              sx={{
                color: '#ff4757',
                textAlign: 'center',
                mb: 2,
                p: 1,
                background: 'rgba(255, 71, 87, 0.1)',
                borderRadius: 1,
                border: '1px solid rgba(255, 71, 87, 0.3)',
              }}
            >
              {recordingError}
            </Typography>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Audio Preview */}
      <AnimatePresence>
        {audioUrl && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.95 }}
            transition={{ duration: 0.4 }}
          >
            <Card
              sx={{
                background: 'linear-gradient(135deg, rgba(26, 31, 46, 0.9) 0%, rgba(42, 47, 62, 0.9) 100%)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                mb: 2,
              }}
            >
              <CardContent>
                <Typography
                  variant="subtitle2"
                  sx={{
                    color: '#ffffff',
                    mb: 2,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1,
                  }}
                >
                  <VolumeUp sx={{ color: '#00d4ff' }} />
                  Recorded Audio
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  <audio
                    controls
                    src={audioUrl}
                    style={{
                      flex: 1,
                      height: 40,
                      borderRadius: 8,
                    }}
                  />
                </Box>
                
                <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center' }}>
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                    <IconButton
                      onClick={handleProcessRecording}
                      disabled={isLoading}
                      sx={{
                        background: 'linear-gradient(135deg, #00d4ff 0%, #0099cc 100%)',
                        color: '#ffffff',
                        '&:hover': {
                          background: 'linear-gradient(135deg, #4ddbff 0%, #00d4ff 100%)',
                        },
                        '&:disabled': {
                          opacity: 0.6,
                        },
                      }}
                    >
                      <Send />
                    </IconButton>
                  </motion.div>
                  
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                    <IconButton
                      onClick={clearRecording}
                      sx={{
                        background: 'rgba(255, 255, 255, 0.1)',
                        color: '#ff4757',
                        '&:hover': {
                          background: 'rgba(255, 71, 87, 0.2)',
                        },
                      }}
                    >
                      <Clear />
                    </IconButton>
                  </motion.div>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </Box>
  );
};

export default AnimatedAudioRecorder; 