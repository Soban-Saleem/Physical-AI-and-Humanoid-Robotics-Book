/**
 * Custom Layout Wrapper
 *
 * Swizzled Layout component that injects the SidebarChatbot
 * into all documentation pages.
 */

import React from 'react';
import Layout from '@theme-original/Layout';
import SidebarChatbot from '@site/src/chatbot/SidebarChatbot';

export default function LayoutWrapper(props) {
  // Use production API URL or fall back to local for development
  const apiUrl = typeof window !== 'undefined' && window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8003/chat'
    : 'https://api.your-domain.com/chat';  // Replace with your actual VPS domain

  return (
    <>
      <Layout {...props} />
      <SidebarChatbot apiUrl={apiUrl} />
    </>
  );
}
