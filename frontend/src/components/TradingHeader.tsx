import React from 'react';
import { motion } from 'framer-motion';
import {
  Box,
  Typography,
  Chip,
  IconButton,
  Avatar,
  Badge,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  SignalCellularAlt,
  AccountCircle,
  Notifications,
} from '@mui/icons-material';
import CountUp from 'react-countup';

const TradingHeader: React.FC = () => {
  const marketData = [
    { symbol: 'USD/GBP', price: 1.2845, change: 0.0023, trend: 'up' },
    { symbol: 'EUR/USD', price: 1.0923, change: -0.0018, trend: 'down' },
    { symbol: 'GBP/EUR', price: 0.8512, change: 0.0009, trend: 'up' },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Box
        sx={{
          background: 'linear-gradient(135deg, rgba(26, 31, 46, 0.9) 0%, rgba(42, 47, 62, 0.9) 100%)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: 3,
          p: 3,
          mb: 3,
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '2px',
            background: 'linear-gradient(90deg, #00d4ff 0%, #ff6b35 50%, #00d4ff 100%)',
            animation: 'shimmer 2s linear infinite',
          },
          '@keyframes shimmer': {
            '0%': { transform: 'translateX(-100%)' },
            '100%': { transform: 'translateX(100%)' },
          },
        }}
      >
        {/* Header Content */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <Typography variant="h4" sx={{ mb: 1 }}>
                🤖 Synapse Trader
              </Typography>
              <Typography variant="body2" color="text.secondary">
                AI-Powered Trading Assistant
              </Typography>
            </motion.div>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 }}
            >
              <Chip
                icon={<SignalCellularAlt />}
                label="LIVE"
                color="success"
                sx={{
                  background: 'linear-gradient(135deg, #00ff88 0%, #00cc6a 100%)',
                  color: '#000',
                  fontWeight: 600,
                }}
              />
            </motion.div>

            <IconButton
              sx={{
                background: 'rgba(255, 255, 255, 0.1)',
                '&:hover': { background: 'rgba(255, 255, 255, 0.2)' },
              }}
            >
              <Badge badgeContent={3} color="error">
                <Notifications />
              </Badge>
            </IconButton>

            <Avatar
              sx={{
                background: 'linear-gradient(135deg, #00d4ff 0%, #ff6b35 100%)',
                cursor: 'pointer',
              }}
            >
              <AccountCircle />
            </Avatar>
          </Box>
        </Box>

        {/* Market Data Ticker */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            {marketData.map((data, index) => (
              <motion.div
                key={data.symbol}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.8 + index * 0.1 }}
              >
                <Box
                  sx={{
                    background: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: 2,
                    p: 1.5,
                    minWidth: 120,
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1,
                  }}
                >
                  <Box>
                    <Typography variant="caption" color="text.secondary">
                      {data.symbol}
                    </Typography>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      <CountUp
                        end={data.price}
                        decimals={4}
                        duration={1}
                        separator=","
                      />
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                    {data.trend === 'up' ? (
                      <TrendingUp sx={{ color: '#00ff88', fontSize: 16 }} />
                    ) : (
                      <TrendingDown sx={{ color: '#ff4757', fontSize: 16 }} />
                    )}
                    <Typography
                      variant="caption"
                      sx={{
                        color: data.trend === 'up' ? '#00ff88' : '#ff4757',
                        fontWeight: 600,
                      }}
                    >
                      {data.trend === 'up' ? '+' : ''}
                      <CountUp
                        end={data.change}
                        decimals={4}
                        duration={1}
                        separator=","
                      />
                    </Typography>
                  </Box>
                </Box>
              </motion.div>
            ))}
          </Box>
        </motion.div>
      </Box>
    </motion.div>
  );
};

export default TradingHeader; 