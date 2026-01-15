/**
 * Browser Storage Service
 *
 * Manages localStorage for chat session persistence.
 */

import type { ChatSession, ChatMessage } from '../types';

const SESSION_KEY = 'chatSession';
const SESSION_ID_KEY = 'chatSessionId';

const SESSION_TTL = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

/**
 * Get or create session ID.
 */
export function getOrCreateSessionId(): string {
  let sessionId = localStorage.getItem(SESSION_ID_KEY);
  if (!sessionId) {
    sessionId = generateSessionId();
    localStorage.setItem(SESSION_ID_KEY, sessionId);
  }
  return sessionId;
}

/**
 * Load chat session from localStorage.
 */
export function loadSession(): ChatSession | null {
  try {
    const sessionData = localStorage.getItem(SESSION_KEY);
    if (!sessionData) {
      return null;
    }

    const session: ChatSession = JSON.parse(sessionData);

    // Check if session is expired
    const sessionAge = Date.now() - session.createdAt;
    if (sessionAge > SESSION_TTL) {
      clearSession();
      return null;
    }

    return session;
  } catch (error) {
    console.error('Failed to load session:', error);
    return null;
  }
}

/**
 * Save chat session to localStorage.
 */
export function saveSession(session: ChatSession): void {
  try {
    // Limit messages to prevent localStorage overflow
    const maxMessages = 50;
    const messagesToSave = session.messages.slice(-maxMessages);

    const sessionToSave: ChatSession = {
      ...session,
      messages: messagesToSave,
    };

    localStorage.setItem(SESSION_KEY, JSON.stringify(sessionToSave));
  } catch (error) {
    console.error('Failed to save session:', error);
  }
}

/**
 * Clear chat session from localStorage.
 */
export function clearSession(): void {
  localStorage.removeItem(SESSION_KEY);
  localStorage.removeItem(SESSION_ID_KEY);
}

/**
 * Add a message to the session.
 */
export function addMessageToSession(message: ChatMessage): ChatSession | null {
  const session = loadSession();
  if (!session) {
    return null;
  }

  const updatedSession: ChatSession = {
    ...session,
    messages: [...session.messages, message],
    contextWindow: [...(session.contextWindow || []), message.messageId].slice(-10),
  };

  saveSession(updatedSession);
  return updatedSession;
}

/**
 * Check if session exists and is valid.
 */
export function hasSession(): boolean {
  return loadSession() !== null;
}

/**
 * Get session age in milliseconds.
 */
export function getSessionAge(): number | null {
  const session = loadSession();
  if (!session) {
    return null;
  }
  return Date.now() - session.createdAt;
}

/**
 * Generate a new session ID.
 */
function generateSessionId(): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  // Fallback for older browsers
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}
