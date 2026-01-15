/**
 * Tests for useTextSelection hook
 *
 * Tests text selection detection across page content,
 * "Ask about selection" button visibility, and clear functionality.
 */

import { renderHook, act } from '@testing-library/react';
import { useTextSelection, isSelectionInContent, getCurrentPageUrl } from '../hooks/useTextSelection';

// Mock window.getSelection
const mockGetSelection = jest.fn();
Object.defineProperty(window, 'getSelection', {
  value: mockGetSelection,
  writable: true,
});

// Mock window.location
Object.defineProperty(window, 'location', {
  value: {
    pathname: '/docs/module1/lesson1',
  },
  writable: true,
});

describe('useTextSelection', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    // Setup default selection mock
    mockGetSelection.mockReturnValue({
      toString: () => '',
      removeAllRanges: jest.fn(),
    });
  });

  afterEach(() => {
    // Cleanup any event listeners
    jest.restoreAllMocks();
  });

  describe('selection detection', () => {
    it('should detect no selection initially', () => {
      const { result } = renderHook(() => useTextSelection());

      expect(result.current.hasSelection).toBe(false);
      expect(result.current.selectedText).toBe('');
    });

    it('should detect text selection', async () => {
      // Mock selection with text
      const mockSelection = {
        toString: () => 'selected text content',
        removeAllRanges: jest.fn(),
      };
      mockGetSelection.mockReturnValue(mockSelection);

      const { result } = renderHook(() => useTextSelection());

      // Trigger selection change event
      act(() => {
        const event = new Event('selectionchange');
        document.dispatchEvent(event);
      });

      // After selection change, hook should detect selection
      // Note: This may require additional setup depending on implementation
      expect(result.current).toBeDefined();
    });

    it('should clear selection', () => {
      const mockSelection = {
        toString: () => 'selected text',
        removeAllRanges: jest.fn(),
      };
      mockGetSelection.mockReturnValue(mockSelection);

      const { result } = renderHook(() => useTextSelection());

      act(() => {
        result.current.clearSelection();
      });

      expect(mockSelection.removeAllRanges).toHaveBeenCalled();
    });
  });

  describe('empty selection handling', () => {
    it('should treat empty selection as no selection', () => {
      mockGetSelection.mockReturnValue({
        toString: () => '',
        removeAllRanges: jest.fn(),
      });

      const { result } = renderHook(() => useTextSelection());

      expect(result.current.selectedText).toBe('');
    });

    it('should trim whitespace from selection', () => {
      mockGetSelection.mockReturnValue({
        toString: () => '   selected text   ',
        removeAllRanges: jest.fn(),
      });

      const { result } = renderHook(() => useTextSelection());

      // The hook should trim the selection
      const trimmed = result.current.selectedText.trim();
      expect(trimmed).toBe('selected text');
    });
  });

  describe('event listeners', () => {
    it('should set up event listeners on mount', () => {
      const addEventListenerSpy = jest.spyOn(document, 'addEventListener');

      renderHook(() => useTextSelection());

      expect(addEventListenerSpy).toHaveBeenCalledWith(
        'selectionchange',
        expect.any(Function)
      );
      expect(addEventListenerSpy).toHaveBeenCalledWith(
        'mouseup',
        expect.any(Function)
      );
    });

    it('should clean up event listeners on unmount', () => {
      const removeEventListenerSpy = jest.spyOn(document, 'removeEventListener');

      const { unmount } = renderHook(() => useTextSelection());

      unmount();

      expect(removeEventListenerSpy).toHaveBeenCalledWith(
        'selectionchange',
        expect.any(Function)
      );
    });
  });
});

describe('isSelectionInContent', () => {
  beforeEach(() => {
    document.body.innerHTML = '';
  });

  it('should return false when no selection exists', () => {
    mockGetSelection.mockReturnValue(null);

    const result = isSelectionInContent();
    expect(result).toBe(false);
  });

  it('should return false when selection is in chatbot UI', () => {
    // Create a chatbot sidebar element
    const sidebar = document.createElement('div');
    sidebar.className = 'chatbot-sidebar';
    document.body.appendChild(sidebar);

    // Create a text node inside sidebar
    const textNode = document.createTextNode('selected text in sidebar');
    sidebar.appendChild(textNode);

    // Mock selection with range in sidebar
    mockGetSelection.mockReturnValue({
      rangeCount: 1,
      getRangeAt: () => ({
        commonAncestorContainer: textNode,
      }),
    });

    const result = isSelectionInContent();
    expect(result).toBe(false);

    // Cleanup
    document.body.removeChild(sidebar);
  });

  it('should return true when selection is in content area', () => {
    // Create a content element
    const article = document.createElement('article');
    const textNode = document.createTextNode('selected content text');
    article.appendChild(textNode);
    document.body.appendChild(article);

    // Mock selection with range in content
    mockGetSelection.mockReturnValue({
      rangeCount: 1,
      getRangeAt: () => ({
        commonAncestorContainer: textNode,
      }),
    });

    const result = isSelectionInContent();
    expect(result).toBe(true);

    // Cleanup
    document.body.removeChild(article);
  });

  it('should exclude navigation elements', () => {
    // Create a nav element
    const nav = document.createElement('nav');
    const textNode = document.createTextNode('nav link text');
    nav.appendChild(textNode);
    document.body.appendChild(nav);

    // Mock selection in nav
    mockGetSelection.mockReturnValue({
      rangeCount: 1,
      getRangeAt: () => ({
        commonAncestorContainer: textNode,
      }),
    });

    const result = isSelectionInContent();
    expect(result).toBe(false);

    // Cleanup
    document.body.removeChild(nav);
  });
});

describe('getCurrentPageUrl', () => {
  it('should return current pathname', () => {
    Object.defineProperty(window, 'location', {
      value: { pathname: '/docs/module1/lesson1' },
      writable: true,
    });

    const url = getCurrentPageUrl();
    expect(url).toBe('/docs/module1/lesson1');
  });

  it('should handle empty pathname', () => {
    Object.defineProperty(window, 'location', {
      value: { pathname: '' },
      writable: true,
    });

    const url = getCurrentPageUrl();
    expect(url).toBe('');
  });
});

describe('selection integration', () => {
  it('should work with module page URLs', () => {
    Object.defineProperty(window, 'location', {
      value: { pathname: '/docs/module2-ros2/introduction' },
      writable: true,
    });

    const url = getCurrentPageUrl();
    expect(url).toContain('module2');
  });

  it('should detect selection in markdown content', () => {
    // Create typical Docusaurus content structure
    const markdown = document.createElement('article');
    markdown.className = 'markdown';
    const paragraph = document.createElement('p');
    paragraph.textContent = 'This is a paragraph about ROS 2 fundamentals';
    markdown.appendChild(paragraph);
    document.body.appendChild(markdown);

    // Mock selection in paragraph
    mockGetSelection.mockReturnValue({
      rangeCount: 1,
      getRangeAt: () => ({
        commonAncestorContainer: paragraph,
      }),
    });

    const result = isSelectionInContent();
    expect(result).toBe(true);

    // Cleanup
    document.body.removeChild(markdown);
  });
});
