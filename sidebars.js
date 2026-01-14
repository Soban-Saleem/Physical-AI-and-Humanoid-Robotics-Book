// @ts-check

/**
 * Sidebar configuration for Physical AI & Humanoid Robotics Textbook
 * Organized by module with categorized structure
 *
 * @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  mainSidebar: [
    // Introduction / Front Matter
    {
      type: 'category',
      label: 'Introduction',
      collapsible: true,
      collapsed: false,
      items: [
        'intro',
        'intro/about',
        'intro/prerequisites',
        'intro/hardware-guide',
      ],
    },
    // Module 1: Introduction to Physical AI (Weeks 1-2)
    {
      type: 'category',
      label: 'Module 1: Introduction to Physical AI',
      collapsible: true,
      collapsed: false,
      items: [
        'module1-intro/what-is-physical-ai',
        'module1-intro/sensors-and-actuators',
        'module1-intro/the-embodiment-gap',
      ],
    },
    // Module 2: ROS 2 Fundamentals (Weeks 3-5)
    {
      type: 'category',
      label: 'Module 2: ROS 2 Fundamentals',
      collapsible: true,
      collapsed: true,
      items: [
        'module2-ros2/introduction-to-ros2',
        'module2-ros2/nodes-and-topics',
        'module2-ros2/services-and-actions',
        'module2-ros2/urdf-and-robot-models',
      ],
    },
    // Appendices - Reference Materials
    {
      type: 'category',
      label: 'Appendices',
      collapsible: true,
      collapsed: true,
      items: [
        'appendices/ros2-cheat-sheet',
        'appendices/troubleshooting',
        'appendices/glossary',
        'appendices/references',
      ],
    },
  ],
};

export default sidebars;
