import { ChatRequest, ChatResponse } from '../types/conversation';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export class ApiService {
  private static async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  static async sendTextMessage(text: string): Promise<ChatResponse> {
    return this.makeRequest<ChatResponse>('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
  }

  static async sendAudioMessage(audioBlob: Blob): Promise<ChatResponse> {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');

    const response = await fetch(`${API_BASE_URL}/api/speech-to-text`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Audio processing failed: ${response.statusText}`);
    }

    return response.json();
  }

  static async getConversationHistory(): Promise<any[]> {
    return this.makeRequest<any[]>('/api/conversation-history');
  }

  static async textToSpeech(text: string): Promise<Blob> {
    const response = await fetch(`${API_BASE_URL}/api/text-to-speech`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`Text-to-speech failed: ${response.statusText}`);
    }

    return response.blob();
  }
} 