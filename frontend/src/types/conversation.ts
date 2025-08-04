export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface ConversationState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
}

export interface AudioResponse {
  audioUrl: string;
  text: string;
}

export interface ChatRequest {
  audioBlob?: Blob;
  text?: string;
}

export interface ChatResponse {
  text: string;
  audio_url?: string;
} 