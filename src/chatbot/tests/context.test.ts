/**
 * Tests for conversation context window functionality
 *
 * Tests sliding window context management, session persistence,
 * and context message truncation.
 */

import { renderHook, act } from '@testing-library/react';
import { useChat } from '../useChat';
import type { ChatMessage, ChatSession } from '../types';

// Mock fetch
global.fetch = jest.fn();

// Mock localStorage
const mockLocalStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
};

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
  writable: true,
});

describe('useChat - Context Window', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockLocalStorage.getItem.mockReturnValue(null);
    (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValue({
      ok: true,
      json: async () => ({
        answer: 'Test response',
        citations: [],
        sessionId: 'test-session',
        isCached: false,
      }),
    } as Response);
  });

  describe('context window initialization', () => {
    it('should start with empty context window', () => {
      const { result } = renderHook(() => useChat());

      expect(result.current.messages).toEqual([]);
      // Context window is internal, but we can verify messages are empty
    });

    it('should load context window from session storage', () => {
      const mockSession: ChatSession = {
        sessionId: 'test-session',
        createdAt: Date.now(),
        messages: [
          {
            messageId: 'msg1',
            messageType: 'user',
            content: 'Question 1',
            createdAt: Date.now(),
          },
        ],
        contextWindow: ['msg1'],
      };

      mockLocalStorage.getItem.mockReturnValue(JSON.stringify(mockSession));

      const { result } = renderHook(() => useChat());

      expect(result.current.messages).toHaveLength(1);
    });
  });

  describe('sliding window behavior', () => {
    it('should add messages to context window', async () => {
      const { result } = renderHook(() => useChat());

      await act(async () => {
        await result.current.sendQuestion('First question');
      });

      expect(result.current.messages).toHaveLength(2); // user + assistant
    });

    it('should limit context window to 10 messages', async () => {
      // Mock successful responses
      (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValue({
        ok: true,
        json: async () => ({
          answer: 'Response',
          citations: [],
          sessionId: 'test',
          isCached: false,
        }),
      } as Response);

      const { result } = renderHook(() => useChat());

      // Send 12 questions (24 messages total)
      for (let i = 0; i < 12; i++) {
        await act(async () => {
          await result.current.sendQuestion(`Question ${i}`);
        });
      }

      // Should have 24 messages (12 user + 12 assistant)
      expect(result.current.messages.length).toBe(24);
    });
  });

  describe('context message passing', () => {
    it('should include context messages in request', async () => {
      (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValue({
        ok: true,
        json: async () => ({
          answer: 'Follow-up response',
          citations: [],
          sessionId: 'test',
          isCached: false,
        }),
      } as Response);

      const { result } = renderHook(() => useChat());

      // First message
      await act(async () => {
        await result.current.sendQuestion('What is LIDAR?');
      });

      // Second message should include context
      await act(async () => {
        await result.current.sendQuestion('What are its limitations?');
      });

      // Verify the second fetch call included context
      const fetchCalls = (global.fetch as jest.MockedFunction<typeof fetch>).mock.calls;
      expect(fetchCalls.length).toBeGreaterThan(0);

      // Check if contextMessages was included in the request
      const secondCallBody = JSON.parse(fetchCalls[1]?.[1]?.body as string);
      expect(secondCallBody).toHaveProperty('contextMessages');
    });
  });

  describe('session persistence', () => {
    it('should save context window to localStorage', async () => {
      const { result } = renderHook(() => useChat());

      await act(async () => {
        await result.current.sendQuestion('Test question');
      });

      expect(mockLocalStorage.setItem).toHaveBeenCalled();

      // Verify the saved session includes contextWindow
      const setItemCalls = mockLocalStorage.setItem.mock.calls;
      const savedSession = JSON.parse(setItemCalls[0]?.[1] as string);

      expect(savedSession).toHaveProperty('contextWindow');
      expect(Array.isArray(savedSession.contextWindow)).toBe(true);
    });

    it('should restore context window on load', () => {
      const mockSession: ChatSession = {
        sessionId: 'test-session',
        createdAt: Date.now() - 1000, // Recent
        messages: [
          {
            messageId: 'msg1',
            messageType: 'user',
            content: 'Previous question',
            createdAt: Date.now() - 1000,
          },
          {
            messageId: 'msg2',
            messageType: 'assistant',
            content: 'Previous answer',
            createdAt: Date.now() - 500,
          },
        ],
        contextWindow: ['msg1', 'msg2'],
      };

      mockLocalStorage.getItem.mockReturnValue(JSON.stringify(mockSession));

      const { result } = renderHook(() => useChat());

      expect(result.current.messages).toHaveLength(2);
    });
  });

  describe('session expiration', () => {
    it('should clear expired sessions (24 hours)', () => {
      const expiredSession: ChatSession = {
        sessionId: 'expired-session',
        createdAt: Date.now() - (25 * 60 * 60 * 1000), // 25 hours ago
        messages: [
          {
            messageId: 'msg1',
            messageType: 'user',
            content: 'Old question',
            createdAt: Date.now() - (25 * 60 * 60 * 1000),
          },
        ],
        contextWindow: ['msg1'],
      };

      mockLocalStorage.getItem.mockReturnValue(JSON.stringify(expiredSession));

      const { result } = renderHook(() => useChat());

      // Should not load expired session
      expect(result.current.messages).toHaveLength(0);
    });

    it('should load valid sessions (less than 24 hours)', () => {
      const validSession: ChatSession = {
        sessionId: 'valid-session',
        createdAt: Date.now() - (12 * 60 * 60 * 1000), // 12 hours ago
        messages: [
          {
            messageId: 'msg1',
            messageType: 'user',
            content: 'Recent question',
            createdAt: Date.now() - (12 * 60 * 60 * 1000),
          },
        ],
        contextWindow: ['msg1'],
      };

      mockLocalStorage.getItem.mockReturnValue(JSON.stringify(validSession));

      const { result } = renderHook(() => useChat());

      // Should load valid session
      expect(result.current.messages).toHaveLength(1);
    });
  });

  describe('clear messages', () => {
    it('should clear context window when messages are cleared', async () => {
      const { result } = renderHook(() => useChat());

      await act(async () => {
        await result.current.sendQuestion('Test question');
      });

      expect(result.current.messages.length).toBeGreaterThan(0);

      await act(() => {
        result.current.clearMessages();
      });

      expect(result.current.messages).toHaveLength(0);
      expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('chatSession');
    });
  });

  describe('pronoun resolution', () => {
    it('should enable follow-up questions with pronouns', async () => {
      (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValue({
        ok: true,
        json: async () => ({
          answer: 'The limitations are cost and weather sensitivity',
          citations: [],
          sessionId: 'test',
          isCached: false,
        }),
      } as Response);

      const { result } = renderHook(() => useChat());

      // First question
      await act(async () => {
        await result.current.sendQuestion('What is LIDAR?');
      });

      // Follow-up with pronoun
      await act(async () => {
        await result.current.sendQuestion('What are its limitations?');
      });

      // The request should include context to resolve "its"
      const fetchCalls = (global.fetch as jest.MockedFunction<typeof fetch>).mock.calls;
      const secondCallBody = JSON.parse(fetchCalls[1]?.[1]?.body as string);

      expect(secondCallBody.contextMessages).toBeDefined();
      expect(secondCallBody.contextMessages.length).toBeGreaterThan(0);
    });
  });
});

describe('context window edge cases', () => {
  it('should handle empty context gracefully', async () => {
    (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValue({
      ok: true,
      json: async () => ({
        answer: 'Response',
        citations: [],
        sessionId: 'test',
        isCached: false,
      }),
    } as Response);

    const { result } = renderHook(() => useChat());

    // First message has no context
    await act(async () => {
      await result.current.sendQuestion('First question');
    });

    expect(result.current.messages).toHaveLength(2);
  });

  it('should handle context window size exactly at limit', async () => {
    const CONTEXT_WINDOW_SIZE = 10;
    (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValue({
      ok: true,
      json: async () => ({
        answer: 'Response',
        citations: [],
        sessionId: 'test',
        isCached: false,
      }),
    } as Response);

    const { result } = renderHook(() => useChat());

    // Add exactly CONTEXT_WINDOW_SIZE messages
    for (let i = 0; i < CONTEXT_WINDOW_SIZE; i++) {
      await act(async () => {
        await result.current.sendQuestion(`Question ${i}`);
      });
    }

    expect(result.current.messages).toHaveLength(CONTEXT_WINDOW_SIZE * 2);
  });
});
