/**
 * API Client for Chatbot Backend
 *
 * Handles communication with the backend chat API.
 */

import type { ChatRequest, ChatResponse, ChatSelectionRequest } from '../types';

const DEFAULT_API_URL = '/chat';
const RETRY_DELAYS = [100, 200, 400]; // Exponential backoff delays in ms
const MAX_RETRIES = 3;
const CIRCUIT_BREAKER_THRESHOLD = 5;

// Circuit breaker state
let consecutiveFailures = 0;
let circuitOpenUntil = 0;

interface ApiClientOptions {
  apiUrl?: string;
  timeout?: number;
}

/**
 * Send a chat question to the backend.
 */
export async function chat(
  request: ChatRequest,
  options: ApiClientOptions = {}
): Promise<ChatResponse> {
  const { apiUrl = DEFAULT_API_URL, timeout = 30000 } = options;

  // Check circuit breaker
  if (Date.now() < circuitOpenUntil) {
    throw new Error('Service temporarily unavailable (circuit breaker)');
  }

  return fetchWithRetry(`${apiUrl}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
    signal: AbortSignal.timeout(timeout),
  });
}

/**
 * Send a chat question with selected text context.
 */
export async function chatSelection(
  request: ChatSelectionRequest,
  options: ApiClientOptions = {}
): Promise<ChatResponse> {
  const { apiUrl = DEFAULT_API_URL } = options;

  // Check circuit breaker
  if (Date.now() < circuitOpenUntil) {
    throw new Error('Service temporarily unavailable (circuit breaker)');
  }

  return fetchWithRetry(`${apiUrl}/selection`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
    signal: AbortSignal.timeout(30000),
  });
}

/**
 * Fetch with exponential backoff retry logic.
 */
async function fetchWithRetry(
  url: string,
  init: RequestInit,
  attempt: number = 0
): Promise<any> {
  try {
    const response = await fetch(url, init);

    // Reset circuit breaker on success
    if (response.ok) {
      consecutiveFailures = 0;
      circuitOpenUntil = 0;
      return await response.json();
    }

    // Don't retry on client errors (4xx)
    if (response.status >= 400 && response.status < 500) {
      const error = await response.json();
      throw new Error(error.message || 'Request failed');
    }

    // Retry on server errors (5xx)
    if (attempt < MAX_RETRIES) {
      const delay = RETRY_DELAYS[attempt] || RETRY_DELAYS[RETRY_DELAYS.length - 1];
      await sleep(delay);
      return fetchWithRetry(url, init, attempt + 1);
    }

    throw new Error(`Request failed with status ${response.status}`);

  } catch (error) {
    // Check if aborted
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timeout');
    }

    // Retry on network errors
    if (attempt < MAX_RETRIES && !isCircuitBreakerError(error)) {
      const delay = RETRY_DELAYS[attempt] || RETRY_DELAYS[RETRY_DELAYS.length - 1];
      await sleep(delay);
      return fetchWithRetry(url, init, attempt + 1);
    }

    // Increment circuit breaker
    consecutiveFailures++;
    if (consecutiveFailures >= CIRCUIT_BREAKER_THRESHOLD) {
      // Open circuit for 60 seconds
      circuitOpenUntil = Date.now() + 60000;
    }

    throw error;
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function isCircuitBreakerError(error: unknown): boolean {
  // Don't retry certain errors
  if (error instanceof Error) {
    return error.message.includes('circuit breaker');
  }
  return false;
}

/**
 * Reset the circuit breaker (for manual recovery).
 */
export function resetCircuitBreaker(): void {
  consecutiveFailures = 0;
  circuitOpenUntil = 0;
}

/**
 * Check if the service is available.
 */
export function isServiceAvailable(): boolean {
  return Date.now() >= circuitOpenUntil;
}
