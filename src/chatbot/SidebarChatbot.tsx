/**
 * Sidebar Chatbot Component
 *
 * Collapsible right sidebar panel containing the chat interface.
 * Mobile responsive with full-screen overlay mode.
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import ChatInterface from './ChatInterface';
import { useTextSelection, isSelectionInContent, getCurrentPageUrl } from './hooks/useTextSelection';
import type { CitationReference } from './types';

interface SidebarChatbotProps {
  apiUrl?: string;
}

export default function SidebarChatbot({ apiUrl = '/chat' }: SidebarChatbotProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [selectionMode, setSelectionMode] = useState(false);
  const sidebarRef = useRef<HTMLDivElement>(null);
  const toggleButtonRef = useRef<HTMLButtonElement>(null);

  // Use text selection hook
  const { hasSelection, clearSelection } = useTextSelection();

  // Detect mobile breakpoint
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Handle escape key to close sidebar
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        handleClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen]);

  // Handle focus management
  useEffect(() => {
    if (isOpen && !isMobile && toggleButtonRef.current) {
      // Return focus to toggle button when sidebar closes
      toggleButtonRef.current.focus();
    }
  }, [isOpen, isMobile]);

  const handleToggle = () => {
    setIsOpen((prev) => !prev);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleClearHistory = () => {
    if (window.confirm('Clear chat history?')) {
      localStorage.removeItem('chatSession');
      // Force reload to reset state
      window.location.reload();
    }
  };

  // Handle asking about selection
  const handleAskAboutSelection = useCallback(() => {
    const selection = window.getSelection()?.toString().trim();
    if (selection && isSelectionInContent()) {
      setSelectedText(selection);
      setSelectionMode(true);
      setIsOpen(true); // Open sidebar
    }
  }, []);

  // Clear selection mode
  const handleClearSelection = useCallback(() => {
    setSelectedText('');
    setSelectionMode(false);
    clearSelection();
  }, [clearSelection]);

  // Handle send message with optional selection
  const handleSendMessage = async (question: string, sessionId: string) => {
    const endpoint = selectionMode ? `${apiUrl}/selection` : apiUrl;
    const body: any = {
      question,
      sessionId,
    };

    if (selectionMode) {
      body.selectedText = selectedText;
      body.pageUrl = getCurrentPageUrl();
    }

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to get response');
    }

    return await response.json();
  };

  // Mobile overlay or sidebar
  if (isMobile) {
    return (
      <>
        {/* Floating toggle button for mobile */}
        {!isOpen && (
          <>
            <button
              ref={toggleButtonRef}
              onClick={handleToggle}
              className="chatbot-toggle-fixed fixed bottom-4 right-4 z-50 bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700"
              aria-label="Open chat assistant"
              type="button"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </button>

            {/* "Ask about selection" button */}
            {hasSelection && isSelectionInContent() && (
              <button
                onClick={handleAskAboutSelection}
                className="fixed bottom-20 right-4 z-50 bg-purple-600 text-white px-4 py-3 rounded-full shadow-lg hover:bg-purple-700 flex items-center gap-2 max-w-[200px]"
                aria-label="Ask about selected text"
                type="button"
              >
                <svg
                  className="w-5 h-5 flex-shrink-0"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span className="text-sm font-medium truncate">Ask about selection</span>
              </button>
            )}
          </>
        )}

        {/* Full-screen overlay for mobile */}
        {isOpen && (
          <div
            className="chatbot-overlay fixed inset-0 z-50 bg-white"
            role="complementary"
            aria-label="Course assistant chatbot"
          >
            {/* Close button */}
            <button
              onClick={handleClose}
              className="absolute top-4 right-4 z-10 p-2 text-gray-500 hover:text-gray-700"
              aria-label="Close chat"
              type="button"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>

            <ChatInterface
              sessionId={getOrCreateSessionId()}
              onSendMessage={handleSendMessage}
              onClearHistory={handleClearHistory}
              selectionMode={selectionMode}
              selectedText={selectedText}
              onClearSelection={handleClearSelection}
            />
          </div>
        )}
      </>
    );
  }

  // Desktop sidebar
  return (
    <>
      {/* Toggle button */}
      <button
        ref={toggleButtonRef}
        onClick={handleToggle}
        className="chatbot-toggle"
        aria-label={isOpen ? 'Close chat assistant' : 'Open chat assistant'}
        type="button"
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          {isOpen ? (
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          ) : (
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          )}
        </svg>
      </button>

      {/* "Ask about selection" floating button */}
      {hasSelection && isSelectionInContent() && !isOpen && (
        <button
          onClick={handleAskAboutSelection}
          className="chatbot-ask-selection fixed bottom-8 right-20 z-40 bg-purple-600 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-purple-700 flex items-center gap-2 transition-opacity"
          aria-label="Ask about selected text"
          type="button"
        >
          <svg
            className="w-4 h-4 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <span className="text-sm font-medium">Ask about selection</span>
        </button>
      )}

      {/* Collapsible sidebar */}
      <div
        ref={sidebarRef}
        className={`chatbot-sidebar ${isOpen ? 'open' : 'closed'}`}
        role="complementary"
        aria-label="Course assistant chatbot"
        aria-hidden={!isOpen}
      >
        <ChatInterface
          sessionId={getOrCreateSessionId()}
          onSendMessage={handleSendMessage}
          onClearHistory={handleClearHistory}
          selectionMode={selectionMode}
          selectedText={selectedText}
          onClearSelection={handleClearSelection}
        />
      </div>

      <style>{`
        .chatbot-sidebar {
          position: fixed;
          top: 0;
          right: 0;
          width: 400px;
          height: 100vh;
          background: white;
          border-left: 1px solid #e5e7eb;
          transition: transform 0.3s ease;
          z-index: 40;
        }

        .chatbot-sidebar.closed {
          transform: translateX(100%);
        }

        .chatbot-sidebar.open {
          transform: translateX(0);
        }

        .chatbot-toggle {
          position: fixed;
          top: 1rem;
          right: 1rem;
          z-index: 41;
          padding: 0.5rem;
          background: #f3f4f6;
          border: 1px solid #d1d5db;
          border-radius: 0.375rem;
          cursor: pointer;
        }

        .chatbot-toggle:hover {
          background: #e5e7eb;
        }

        /* Focus trap when sidebar is open */
        .chatbot-sidebar.open *:focus {
          outline: 2px solid #3b82f6;
          outline-offset: 2px;
        }
      `}</style>
    </>
  );
}

function getOrCreateSessionId(): string {
  // Check if we're in a browser environment
  if (typeof window === 'undefined' || typeof localStorage === 'undefined') {
    return ''; // Return empty string during SSR
  }

  let sessionId = localStorage.getItem('chatSessionId');
  if (!sessionId) {
    sessionId = crypto.randomUUID?.() || `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('chatSessionId', sessionId);
  }
  return sessionId;
}
