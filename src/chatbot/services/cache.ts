/**
 * IndexedDB Cache Service
 *
 * Manages local caching of chat responses for offline fallback.
 */

import type { CachedResponse, CitationReference } from '../types';

const CACHE_NAME = 'chatbotCache';
const CACHE_STORE = 'responses';
const CACHE_VERSION = 1;

/**
 * Initialize IndexedDB cache database.
 */
function openCache(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(CACHE_NAME, CACHE_VERSION);

    request.onerror = () => {
      reject(new Error('Failed to open cache database'));
    };

    request.onsuccess = () => {
      resolve(request.result);
    };

    request.onupgradeneeded = (event: IDBVersionChangeEvent) => {
      const db = (event.target as IDBOpenDBRequest).result;

      // Create object store for cached responses
      if (!db.objectStoreNames.contains(CACHE_STORE)) {
        const store = db.createObjectStore(CACHE_STORE, { keyPath: 'cacheKey' });

        // Create indexes
        store.createIndex('createdAt', 'createdAt', { expires: false });
        store.createIndex('hitCount', 'hitCount', { expires: false });
      }
    };
  });
}

/**
 * Get a cached response by key.
 */
export async function getCachedResponse(cacheKey: string): Promise<CachedResponse | null> {
  try {
    const db = await openCache();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([CACHE_STORE], 'readonly');
      const store = transaction.objectStore(CACHE_STORE);
      const request = store.get(cacheKey);

      request.onsuccess = () => {
        const result = request.result;
        if (!result) {
          resolve(null);
          return;
        }

        // Check TTL (24 hours)
        const age = Date.now() - result.createdAt;
        if (age > 24 * 60 * 60 * 1000) {
          // Expired - delete it
          deleteCachedResponse(cacheKey);
          resolve(null);
          return;
        }

        resolve(result as CachedResponse);
      };

      request.onerror = () => {
        reject(new Error('Failed to get cached response'));
      };
    });
  } catch (error) {
    console.error('Failed to get cached response:', error);
    return null;
  }
}

/**
 * Save a response to cache.
 */
export async function saveCachedResponse(response: CachedResponse): Promise<void> {
  try {
    const db = await openCache();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([CACHE_STORE], 'readwrite');
      const store = transaction.objectStore(CACHE_STORE);
      const request = store.put(response);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(new Error('Failed to save cached response'));
    });
  } catch (error) {
    console.error('Failed to save cached response:', error);
  }
}

/**
 * Delete a cached response.
 */
export async function deleteCachedResponse(cacheKey: string): Promise<void> {
  try {
    const db = await openCache();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([CACHE_STORE], 'readwrite');
      const store = transaction.objectStore(CACHE_STORE);
      const request = store.delete(cacheKey);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(new Error('Failed to delete cached response'));
    });
  } catch (error) {
    console.error('Failed to delete cached response:', error);
  }
}

/**
 * Clear all cached responses.
 */
export async function clearCache(): Promise<void> {
  try {
    const db = await openCache();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([CACHE_STORE], 'readwrite');
      const store = transaction.objectStore(CACHE_STORE);
      const request = store.clear();

      request.onsuccess = () => resolve();
      request.onerror = () => reject(new Error('Failed to clear cache'));
    });
  } catch (error) {
    console.error('Failed to clear cache:', error);
  }
}

/**
 * Generate cache key from question and optional context.
 */
export function generateCacheKey(question: string, selectedText?: string): string {
  const content = question.toLowerCase().trim();
  const selection = selectedText ? `|${selectedText.toLowerCase().trim()}` : '';

  // Simple hash function
  let hash = 0;
  const str = content + selection;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }

  return `cache_${Math.abs(hash).toString(36)}`;
}

/**
 * Find semantically similar cached responses.
 * This is a simplified implementation - for production, use vector similarity.
 */
export async function findSimilarCachedResponse(
  question: string,
  threshold: number = 0.85
): Promise<CachedResponse | null> {
  // For now, this is a placeholder. In a full implementation,
  // you would:
  // 1. Generate embedding for the question
  // 2. Compare with embeddings of cached questions
  // 3. Return the most similar cached response if above threshold

  // Simple fallback: check for exact word overlap
  const questionWords = new Set(question.toLowerCase().split(/\s+/));

  const db = await openCache();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction([CACHE_STORE], 'readonly');
    const store = transaction.objectStore(CACHE_STORE);
    const request = store.openCursor();

    const results: Array<{ cached: CachedResponse; score: number }> = [];

    request.onsuccess = () => {
      const cursor = request.result;
      if (cursor) {
        const cached = cursor.value as CachedResponse;
        // Extract question from cached answer (simplified)
        const cachedWords = new Set(
          cached.answer.toLowerCase().split(/\s+/).slice(0, 20)
        );

        // Calculate Jaccard similarity
        const intersection = new Set([...questionWords].filter(x => cachedWords.has(x)));
        const union = new Set([...questionWords, ...cachedWords]);
        const similarity = intersection.size / union.size;

        if (similarity >= threshold) {
          results.push({ cached, score: similarity });
        }

        cursor.continue();
      } else {
        // Done - return best match
        results.sort((a, b) => b.score - a.score);
        resolve(results.length > 0 ? results[0].cached : null);
      }
    };

    request.onerror = () => reject(new Error('Failed to find similar cached response'));
  });
}
