/**
 * Chatbot Bootstrap Module
 *
 * Client module entry point for Docusaurus integration.
 * Injects the SidebarChatbot component into all documentation pages.
 */

import SidebarChatbot from './SidebarChatbot';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

export default function (context) {
  const { router } = context;

  // Only run on client side
  if (ExecutionEnvironment.canUseDOM) {
    // We'll use a lifecycle hook to inject the chatbot
    return {
      name: 'chatbot-plugin',

      // Inject the chatbot component on all routes
      onRouteDidUpdate: ({ location, previousLocation }) => {
        // Only re-render if the path changed
        if (location.pathname !== previousLocation?.pathname) {
          // The chatbot is already mounted via the Layout component
          // This hook can be used for analytics or page-specific initialization
        }
      },
    };
  }

  return {
    name: 'chatbot-plugin',
  };
}

// Export the component for direct use in Layout
export { SidebarChatbot };
