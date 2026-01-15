/**
 * Chat Hook
 *
 * React hook for managing chat state and API communication.
 * Maintains sliding window context for conversational memory.
 */

import { useState, useCallback, useRef } from 'react';
import type { ChatMessage, CitationReference, ChatResponse, ChatError, ChatSession } from '../types';

const CONTEXT_WINDOW_SIZE = 10; // Keep last 10 message IDs for context

interface UseChatOptions {
  apiUrl?: string;
  enableCache?: boolean;
}

interface UseChatResult {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  sendQuestion: (question: string, selectedText?: string) => Promise<void>;
  clearError: () => void;
  clearMessages: () => void;
}

export function useChat(options: UseChatOptions = {}): UseChatResult {
  const { apiUrl = '/chat', enableCache = true } = options;

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [contextWindow, setContextWindow] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const requestQueueRef = useRef<Map<string, Promise<ChatResponse>>>(new Map());

  // Load session from localStorage on mount
  useState(() => {
    loadSession();
  });

  const loadSession = () => {
    try {
      const sessionData = localStorage.getItem('chatSession');
      if (sessionData) {
        const session: ChatSession = JSON.parse(sessionData);
        // Check if session is expired (24 hours)
        const sessionAge = Date.now() - session.createdAt;
        if (sessionAge < 24 * 60 * 60 * 1000) {
          setMessages(session.messages || []);
          setContextWindow(session.contextWindow || []);
        } else {
          // Clear expired session
          clearSession();
        }
      }
    } catch (err) {
      console.error('Failed to load session:', err);
    }
  };

  const saveSession = (newMessages: ChatMessage[], newContextWindow: string[]) => {
    try {
      const sessionData: ChatSession = {
        sessionId: getOrCreateSessionId(),
        createdAt: Date.now(),
        messages: newMessages,
        contextWindow: newContextWindow,
      };
      localStorage.setItem('chatSession', JSON.stringify(sessionData));
    } catch (err) {
      console.error('Failed to save session:', err);
    }
  };

  const updateContextWindow = (messageId: string): string[] => {
    const newWindow = [...contextWindow, messageId].slice(-CONTEXT_WINDOW_SIZE);
    setContextWindow(newWindow);
    return newWindow;
  };

  const clearSession = () => {
    localStorage.removeItem('chatSession');
    localStorage.removeItem('chatSessionId');
    setContextWindow([]);
  };

  const getOrCreateSessionId = (): string => {
    let sessionId = localStorage.getItem('chatSessionId');
    if (!sessionId) {
      sessionId = crypto.randomUUID?.() || `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('chatSessionId', sessionId);
    }
    return sessionId;
  };

  const getCachedResponse = async (question: string, selectedText?: string): Promise<ChatResponse | null> => {
    if (!enableCache) return null;

    try {
      const cacheKey = generateCacheKey(question, selectedText);
      const cached = localStorage.getItem(`cache_${cacheKey}`);

      if (cached) {
        const cachedData = JSON.parse(cached);
        // Check TTL (24 hours)
        const cacheAge = Date.now() - cachedData.createdAt;
        if (cacheAge < 24 * 60 * 60 * 1000) {
          // Increment hit count
          cachedData.hitCount = (cachedData.hitCount || 0) + 1;
          localStorage.setItem(`cache_${cacheKey}`, JSON.stringify(cachedData));
          return cachedData;
        } else {
          // Remove expired cache
          localStorage.removeItem(`cache_${cacheKey}`);
        }
      }
    } catch (err) {
      console.error('Failed to get cached response:', err);
    }

    return null;
  };

  const cacheResponse = async (question: string, response: ChatResponse, selectedText?: string) => {
    if (!enableCache) return;

    try {
      const cacheKey = generateCacheKey(question, selectedText);
      const cacheData = {
        ...response,
        createdAt: Date.now(),
        hitCount: 1,
      };
      localStorage.setItem(`cache_${cacheKey}`, JSON.stringify(cacheData));
    } catch (err) {
      console.error('Failed to cache response:', err);
    }
  };

  const generateCacheKey = (question: string, selectedText?: string): string => {
    const content = question.toLowerCase().trim();
    const selection = selectedText ? `|${selectedText.toLowerCase().trim()}` : '';
    // Simple hash function
    let hash = 0;
    const str = content + selection;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return `cache_${Math.abs(hash).toString(36)}`;
  };

  const sendQuestion = useCallback(async (question: string, selectedText?: string) => {
    if (!question.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);

    // Get context messages from context window (last 10 message IDs)
    const contextMessages = messages.filter(m => contextWindow.includes(m.messageId));

    // Add user message
    const userMessage: ChatMessage = {
      messageId: `msg_${Date.now()}_user`,
      messageType: 'user',
      content: question,
      createdAt: Date.now(),
    };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);

    try {
      // Check cache first
      const cached = await getCachedResponse(question, selectedText);
      let response: ChatResponse;

      if (cached) {
        response = cached;
      } else {
        // Build request with context messages
        const requestBody: any = {
          question,
          sessionId: getOrCreateSessionId(),
          contextMessages: contextMessages,
        };

        const endpoint = selectedText ? '/chat/selection' : '/chat';

        if (selectedText) {
          requestBody.selectedText = selectedText;
          requestBody.pageUrl = window.location.pathname;
        }

        // Deduplicate concurrent requests
        const requestKey = JSON.stringify(requestBody);
        const existingRequest = requestQueueRef.current.get(requestKey);

        if (existingRequest) {
          response = await existingRequest;
        } else {
          const requestPromise = fetch(apiUrl + endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody),
          })
            .then(async (res) => {
              if (!res.ok) {
                const err = await res.json();
                throw new Error(err.message || 'Request failed');
              }
              return res.json();
            });

          requestQueueRef.current.set(requestKey, requestPromise);

          try {
            response = await requestPromise;
          } finally {
            requestQueueRef.current.delete(requestKey);
          }

          // Cache the response
          await cacheResponse(question, response, selectedText);
        }
      }

      // Add assistant message
      const assistantMessage: ChatMessage = {
        messageId: `msg_${Date.now()}_assistant`,
        messageType: 'assistant',
        content: response.answer,
        citations: response.citations,
        createdAt: Date.now(),
        isCached: response.isCached || cached !== null,
      };

      const finalMessages = [...newMessages, assistantMessage];
      setMessages(finalMessages);

      // Update context window with both messages
      const newContextWindow = updateContextWindow(userMessage.messageId);
      updateContextWindow(assistantMessage.messageId);

      saveSession(finalMessages, newContextWindow);

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send question';
      setError(errorMessage);

      // Remove user message on error
      setMessages(newMessages);
    } finally {
      setIsLoading(false);
    }
  }, [messages, contextWindow, isLoading, apiUrl, enableCache]);

  const clearError = () => {
    setError(null);
  };

  const clearMessages = () => {
    setMessages([]);
    clearSession();
  };

  return {
    messages,
    isLoading,
    error,
    sendQuestion,
    clearError,
    clearMessages,
  };
}

function generateCacheKey(question: string, selectedText?: string): string {
  const content = question.toLowerCase().trim();
  const selection = selectedText ? `|${selectedText.toLowerCase().trim()}` : '';
  // Simple hash
  let hash = 0;
  const str = content + selection;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return `cache_${Math.abs(hash).toString(36)}`;
}
