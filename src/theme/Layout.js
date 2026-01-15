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
  return (
    <>
      <Layout {...props} />
      <SidebarChatbot apiUrl="/chat" />
    </>
  );
}
