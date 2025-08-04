import React from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { tradingTheme } from './theme/tradingTheme';
import EnhancedConversation from './components/EnhancedConversation';

function App() {
  return (
    <ThemeProvider theme={tradingTheme}>
      <CssBaseline />
      <EnhancedConversation />
    </ThemeProvider>
  );
}

export default App;
