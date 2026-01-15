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
  // Use environment variable or default to local backend
  const apiUrl = process.env.REACT_APP_CHAT_API_URL || 'http://127.0.0.1:8003/chat';

  return (
    <>
      <Layout {...props} />
      <SidebarChatbot apiUrl={apiUrl} />
    </>
  );
}
