/**
 * Chat Interface Component
 *
 * Displays the chat conversation with messages, input field, and controls.
 */

import React, { useState, useRef, useEffect } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { v4 as uuidv4 } from 'uuid';

import type { ChatMessage, CitationReference } from '../types';

interface ChatInterfaceProps {
  sessionId: string;
  onSendMessage: (question: string, sessionId: string) => Promise<{
    answer: string;
    citations: CitationReference[];
  }>;
  onClearHistory: () => void;
  selectionMode?: boolean;
  selectedText?: string;
  onClearSelection?: () => void;
}

export default function ChatInterface({
  sessionId,
  onSendMessage,
  onClearHistory,
  selectionMode = false,
  selectedText,
  onClearSelection,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const question = input.trim();
    if (!question || isLoading) return;

    // Add user message
    const userMessage: ChatMessage = {
      messageId: uuidv4(),
      messageType: 'user',
      content: question,
      createdAt: Date.now(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setError(null);
    setIsLoading(true);

    try {
      const response = await onSendMessage(question, sessionId);

      // Add assistant message
      const assistantMessage: ChatMessage = {
        messageId: uuidv4(),
        messageType: 'assistant',
        content: response.answer,
        citations: response.citations,
        createdAt: Date.now(),
        isCached: response.isCached,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const formatCitations = (citations: CitationReference[]) => {
    if (citations.length === 0) return null;

    return (
      <div className="chat-citations">
        <p className="text-xs text-gray-500 mt-2">Sources:</p>
        <ul className="text-sm space-y-1">
          {citations.slice(0, 3).map((citation) => (
            <li key={citation.citationId}>
              <a
                href={citation.urlAnchor}
                className="text-blue-600 hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                {citation.lessonTitle}
                {citation.sectionHeading && ` (${citation.sectionHeading})`}
              </a>
              <span className="text-xs text-gray-400 ml-1">
                ({Math.round(citation.relevanceScore * 100)}%)
              </span>
            </li>
          ))}
        </ul>
        {citations.length > 3 && (
          <p className="text-xs text-gray-400 italic">
            ...and {citations.length - 3} more sources
          </p>
        )}
      </div>
    );
  };

  const renderCodeBlock = (text: string, language?: string) => {
    // Simple code block detection
    const codeBlockRegex = /```(\w*)\n([\s\S]*?)```/g;
    const parts: Array<{ type: 'text' | 'code'; content: string; language?: string }> = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(text)) !== null) {
      // Add text before code block
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: text.slice(lastIndex, match.index),
        });
      }
      // Add code block
      parts.push({
        type: 'code',
        content: match[2],
        language: match[1] || 'text',
      });
      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < text.length) {
      parts.push({
        type: 'text',
        content: text.slice(lastIndex),
      });
    }

    if (parts.length === 0) {
      parts.push({ type: 'text', content: text });
    }

    return parts.map((part, i) => {
      if (part.type === 'code') {
        return (
          <SyntaxHighlighter
            key={i}
            language={part.language}
            className="rounded-md my-2"
          >
            {part.content}
          </SyntaxHighlighter>
        );
      }
      return <p key={i} className="whitespace-pre-wrap my-2">{part.content}</p>;
    });
  };

  return (
    <div className="chat-interface flex flex-col h-full">
      {/* Header */}
      <div className="chat-header border-b p-3 flex justify-between items-center bg-gray-50">
        <div>
          <h3 className="font-semibold text-gray-700">Course Assistant</h3>
          {selectionMode && (
            <span className="text-xs text-blue-600 ml-2">
              (Selection Mode)
            </span>
          )}
        </div>
        <button
          onClick={onClearHistory}
          className="text-xs text-gray-500 hover:text-gray-700 underline"
          type="button"
        >
          Clear History
        </button>
      </div>

      {/* Messages */}
      <div className="messages flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-400 mt-8">
            <p className="mb-2">👋 Hi! I'm your course assistant.</p>
            <p>Ask me anything about the Physical AI textbook content.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.messageId}
              className={`message ${message.messageType === 'user' ? 'user-message' : 'assistant-message'}`}
            >
              <div
                className={`inline-block max-w-[85%] rounded-lg px-4 py-2 ${
                  message.messageType === 'user'
                    ? 'bg-blue-600 text-white ml-auto'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {message.isCached && (
                  <span className="text-xs opacity-70 block mb-1">From cache</span>
                )}
                {renderCodeBlock(message.content)}
                {message.citations && formatCitations(message.citations)}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message assistant-message">
            <div className="inline-block bg-gray-100 rounded-lg px-4 py-2">
              <div className="flex items-center space-x-2">
                <div className="animate-spin w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full"></div>
                <span className="text-gray-500 text-sm">Thinking...</span>
              </div>
            </div>
          </div>
        )}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 rounded-lg p-3 text-sm">
            {error}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Selection Mode Indicator */}
      {selectionMode && selectedText && (
        <div className="selection-indicator bg-blue-50 text-blue-700 text-xs px-3 py-2 border-t flex items-center justify-between">
          <div className="flex-1 min-w-0">
            <span className="font-medium">Constraining to selection:</span>{' '}
            <span className="italic truncate inline-block max-w-[200px]" title={selectedText}>
              "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"
            </span>
          </div>
          {onClearSelection && (
            <button
              onClick={onClearSelection}
              className="ml-2 text-blue-600 hover:text-blue-800 underline flex-shrink-0"
              type="button"
            >
              Clear
            </button>
          )}
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="input-area border-t p-3">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about the course..."
            disabled={isLoading}
            maxLength={5000}
            className="flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
