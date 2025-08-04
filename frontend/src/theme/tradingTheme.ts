import { createTheme } from '@mui/material/styles';

export const tradingTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00d4ff',
      light: '#4ddbff',
      dark: '#0099cc',
    },
    secondary: {
      main: '#ff6b35',
      light: '#ff8a65',
      dark: '#e65100',
    },
    background: {
      default: '#0a0e1a',
      paper: '#1a1f2e',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b0b8c1',
    },
    success: {
      main: '#00ff88',
      light: '#4dffaa',
      dark: '#00cc6a',
    },
    error: {
      main: '#ff4757',
      light: '#ff6b7a',
      dark: '#cc3745',
    },
    warning: {
      main: '#ffa502',
      light: '#ffb84d',
      dark: '#cc8401',
    },
    info: {
      main: '#3742fa',
      light: '#5f6bff',
      dark: '#2c35c7',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      background: 'linear-gradient(135deg, #00d4ff 0%, #ff6b35 100%)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundClip: 'text',
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
      background: 'linear-gradient(135deg, #00d4ff 0%, #ff6b35 100%)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundClip: 'text',
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.5rem',
      color: '#ffffff',
    },
    h4: {
      fontWeight: 500,
      fontSize: '1.25rem',
      color: '#ffffff',
    },
    h5: {
      fontWeight: 500,
      fontSize: '1.125rem',
      color: '#ffffff',
    },
    h6: {
      fontWeight: 500,
      fontSize: '1rem',
      color: '#ffffff',
    },
    body1: {
      fontSize: '1rem',
      color: '#b0b8c1',
    },
    body2: {
      fontSize: '0.875rem',
      color: '#8a94a6',
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 100%)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 100%)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 25px rgba(0, 212, 255, 0.15)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            transform: 'translateY(-1px)',
            boxShadow: '0 4px 15px rgba(0, 212, 255, 0.3)',
          },
        },
        contained: {
          background: 'linear-gradient(135deg, #00d4ff 0%, #0099cc 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #4ddbff 0%, #00d4ff 100%)',
          },
        },
        outlined: {
          border: '2px solid #00d4ff',
          color: '#00d4ff',
          '&:hover': {
            background: 'rgba(0, 212, 255, 0.1)',
          },
        },
      },
    },
    MuiFab: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, #00d4ff 0%, #0099cc 100%)',
          boxShadow: '0 4px 15px rgba(0, 212, 255, 0.3)',
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            transform: 'scale(1.05)',
            boxShadow: '0 6px 20px rgba(0, 212, 255, 0.4)',
          },
        },
        secondary: {
          background: 'linear-gradient(135deg, #ff6b35 0%, #e65100 100%)',
          boxShadow: '0 4px 15px rgba(255, 107, 53, 0.3)',
          '&:hover': {
            background: 'linear-gradient(135deg, #ff8a65 0%, #ff6b35 100%)',
            boxShadow: '0 6px 20px rgba(255, 107, 53, 0.4)',
          },
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            transform: 'scale(1.1)',
            background: 'rgba(0, 212, 255, 0.1)',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(255, 107, 53, 0.2) 100%)',
          border: '1px solid rgba(0, 212, 255, 0.3)',
          color: '#ffffff',
        },
      },
    },
  },
}); 