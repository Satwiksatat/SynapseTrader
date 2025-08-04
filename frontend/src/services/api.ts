import { ChatResponse } from '../types/conversation';

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
      const errorText = await response.text();
      throw new Error(`API request failed: ${response.statusText} - ${errorText}`);
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

    const response = await fetch(`${API_BASE_URL}/api/audio-chat`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Audio processing failed: ${response.statusText} - ${errorText}`);
    }

    return response.json();
  }

  static async speechToText(audioBlob: Blob): Promise<{ text: string }> {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');

    const response = await fetch(`${API_BASE_URL}/api/speech-to-text`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Speech-to-text failed: ${response.statusText} - ${errorText}`);
    }

    return response.json();
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
      const errorText = await response.text();
      throw new Error(`Text-to-speech failed: ${response.statusText} - ${errorText}`);
    }

    return response.blob();
  }

  static async getConversationHistory(): Promise<any[]> {
    return this.makeRequest<any[]>('/api/conversation-history');
  }

  static async clearConversationHistory(): Promise<{ message: string }> {
    return this.makeRequest<{ message: string }>('/api/conversation-history', {
      method: 'DELETE',
    });
  }

  static async getHealthStatus(): Promise<any> {
    return this.makeRequest<any>('/api/health');
  }

  static async getApiStatus(): Promise<any> {
    return this.makeRequest<any>('/api/status');
  }

  // Helper method to create audio URL from base64 data
  static createAudioUrlFromDataUrl(dataUrl: string): string {
    return dataUrl;
  }

  // Helper method to play audio from blob
  static async playAudioFromBlob(audioBlob: Blob): Promise<void> {
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    
    return new Promise((resolve, reject) => {
      audio.onended = () => {
        URL.revokeObjectURL(audioUrl);
        resolve();
      };
      audio.onerror = (event) => {
        URL.revokeObjectURL(audioUrl);
        reject(new Error('Audio playback failed'));
      };
      audio.play().catch(reject);
    });
  }

  // Helper method to play audio from data URL
  static async playAudioFromDataUrl(dataUrl: string): Promise<void> {
    const audio = new Audio(dataUrl);
    
    return new Promise((resolve, reject) => {
      audio.onended = () => resolve();
      audio.onerror = () => reject(new Error('Audio playback failed'));
      audio.play().catch(reject);
    });
  }
} 