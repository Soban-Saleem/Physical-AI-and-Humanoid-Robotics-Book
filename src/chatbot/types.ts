/**
 * TypeScript type definitions for RAG Chatbot
 */

/**
 * Citation reference linking a response to source material
 */
export interface CitationReference {
  citationId: string;
  moduleId: string;
  lessonTitle: string;
  sectionHeading: string | null;
  urlAnchor: string;
  relevanceScore: number; // 0.0 - 1.0
}

/**
 * Chat message types
 */
export type MessageType = 'user' | 'assistant';

/**
 * Single message in a conversation
 */
export interface ChatMessage {
  messageId: string;
  messageType: MessageType;
  content: string;
  citations?: CitationReference[];
  createdAt: number; // Unix timestamp
  isCached?: boolean;
}

/**
 * Sliding window context for conversation memory
 */
export interface ChatSession {
  sessionId: string;
  createdAt: number; // Unix timestamp
  messages: ChatMessage[];
  contextWindow: string[]; // Last 10 message IDs
}

/**
 * Cached response for offline fallback
 */
export interface CachedResponse {
  cacheKey: string; // SHA-256 hash
  answer: string;
  citations: CitationReference[];
  createdAt: number;
  ttl: number; // 86400000 (24 hours)
  hitCount: number;
}

/**
 * Chat API request payload
 */
export interface ChatRequest {
  question: string;
  contextMessages?: ChatMessage[];
  sessionId?: string;
}

/**
 * Chat API response payload
 */
export interface ChatResponse {
  answer: string;
  citations: CitationReference[];
  sessionId: string;
  isCached: boolean;
}

/**
 * Text selection mode request
 */
export interface ChatSelectionRequest extends ChatRequest {
  selectedText: string;
  pageUrl: string;
}

/**
 * Chat API error response
 */
export interface ChatError {
  error: string;
  message: string;
  retryAfter?: number; // seconds to wait before retry
  type?: 'unavailable' | 'rate_limited' | 'no_results';
}

/**
 * Health check response
 */
export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  services: {
    qdrant: boolean;
    openai: boolean;
    neon: boolean;
  };
  timestamp: number;
}
