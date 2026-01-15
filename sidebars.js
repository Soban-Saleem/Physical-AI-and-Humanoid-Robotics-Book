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
    // Module 3: Robot Simulation (Weeks 6-7)
    {
      type: 'category',
      label: 'Module 3: Robot Simulation',
      collapsible: true,
      collapsed: true,
      items: [
        'module3-simulation/introduction-to-simulation',
        'module3-simulation/physics-engines',
        'module3-simulation/sensor-simulation',
        'module3-simulation/creating-worlds',
      ],
    },
    // Module 4: NVIDIA Isaac Platform (Weeks 8-10)
    {
      type: 'category',
      label: 'Module 4: NVIDIA Isaac Platform',
      collapsible: true,
      collapsed: true,
      items: [
        'module4-isaac/isaac-sim-introduction',
        'module4-isaac/isaac-ros-gpu',
        'module4-isaac/vslam-navigation',
        'module4-isaac/reinforcement-learning',
      ],
    },
    // Module 5: Humanoid Development (Weeks 11-12)
    {
      type: 'category',
      label: 'Module 5: Humanoid Development',
      collapsible: true,
      collapsed: true,
      items: [
        'module5-humanoid/kinematics',
        'module5-humanoid/bipedal-locomotion',
        'module5-humanoid/manipulation',
        'module5-humanoid/human-robot-interaction',
      ],
    },
    // Module 6: Conversational Robotics (Week 13)
    {
      type: 'category',
      label: 'Module 6: Conversational Robotics',
      collapsible: true,
      collapsed: true,
      items: [
        'module6-conversational/voice-commands',
        'module6-conversational/gpt-integration',
        'module6-conversational/vla-models',
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
