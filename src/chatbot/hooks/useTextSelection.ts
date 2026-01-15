/**
 * Text Selection Hook
 *
 * Detects text selection on the page and provides
 * "Ask about selection" functionality.
 */

import { useState, useEffect, useCallback } from 'react';

interface UseTextSelectionResult {
  selectedText: string;
  hasSelection: boolean;
  clearSelection: () => void;
}

export function useTextSelection(): UseTextSelectionResult {
  const [selectedText, setSelectedText] = useState('');
  const [hasSelection, setHasSelection] = useState(false);

  // Get current selection
  const getSelection = useCallback((): string => {
    if (typeof window === 'undefined' || !window.getSelection) {
      return '';
    }

    const selection = window.getSelection();
    if (!selection) {
      return '';
    }

    return selection.toString().trim();
  }, []);

  // Clear selection
  const clearSelection = useCallback(() => {
    if (typeof window === 'undefined' || !window.getSelection) {
      return;
    }

    const selection = window.getSelection();
    if (selection) {
      selection.removeAllRanges();
    }

    setSelectedText('');
    setHasSelection(false);
  }, []);

  // Handle selection change
  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    const handleSelectionChange = () => {
      const selection = getSelection();

      if (selection.length > 0) {
        setSelectedText(selection);
        setHasSelection(true);
      } else {
        setSelectedText('');
        setHasSelection(false);
      }
    };

    // Listen for selection changes
    document.addEventListener('selectionchange', handleSelectionChange);
    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('touchend', handleSelectionChange);

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('touchend', handleSelectionChange);
    };
  }, [getSelection]);

  return {
    selectedText,
    hasSelection,
    clearSelection,
  };
}

/**
 * Get the current page URL for context
 */
export function getCurrentPageUrl(): string {
  if (typeof window === 'undefined') {
    return '';
  }
  return window.location.pathname;
}

/**
 * Check if selection is within content area (not UI elements)
 */
export function isSelectionInContent(): boolean {
  if (typeof window === 'undefined' || !window.getSelection) {
    return false;
  }

  const selection = window.getSelection();
  if (!selection || selection.rangeCount === 0) {
    return false;
  }

  const range = selection.getRangeAt(0);
  const container = range.commonAncestorContainer;

  // Check if selection is within a content element
  // Exclude chatbot UI, navigation, etc.
  const element = container instanceof HTMLElement ? container : container.parentElement;

  if (!element) {
    return false;
  }

  // Walk up the tree to check for exclusions
  let current: HTMLElement | null = element;
  while (current) {
    // Exclude chatbot UI
    if (current.classList.contains('chatbot-sidebar') ||
        current.classList.contains('chatbot-toggle') ||
        current.getAttribute('role') === 'complementary' ||
        current.closest('[role="complementary"]')) {
      return false;
    }

    // Exclude navigation elements
    if (current.tagName === 'NAV' ||
        current.classList.contains('navbar') ||
        current.getAttribute('role') === 'navigation') {
      return false;
    }

    current = current.parentElement;
  }

  return true;
}
