import React from 'react';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Conversation from './components/Conversation';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Conversation />
    </ThemeProvider>
  );
}

export default App;
