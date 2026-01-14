// @ts-check
/** @type {import('@docusaurus/types').Config} */

import {themes as prismThemes} from 'prism-react-renderer';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'AI Systems in the Physical World - Embodied Intelligence',
  favicon: 'img/favicon.ico',

  // Future flags for Docusaurus v4 compatibility
  future: {
    v4: true,
  },

  // Production URL - update with actual GitHub Pages URL
  url: 'https://your-org.github.io',
  baseUrl: '/',

  // GitHub Pages deployment config
  organizationName: 'your-org', // Update with your GitHub org/user
  projectName: 'Physical_AI_Humanoid_Robotics_Textbook', // Update with repo name

  onBrokenLinks: 'throw',
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // Internationalization (Urdu translation in Phase 2)
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/your-org/Physical_AI_Humanoid_Robotics_Textbook/tree/main/',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl: 'https://github.com/your-org/Physical_AI_Humanoid_Robotics_Textbook/tree/main/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  // Mermaid theme for diagrams
  themes: ['@docusaurus/theme-mermaid'],

  // KaTeX CSS from CDN
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css',
      type: 'text/css',
      integrity: 'sha384-6paTAw +3W8W7Mp5M4qS/qhcH4kvMnq0K4VmPQRNFs9rYzO6cW5W4zcc+D',
      crossorigin: 'anonymous',
    },
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg',
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Physical AI Textbook',
        logo: {
          alt: 'Physical AI Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'mainSidebar',
            position: 'left',
            label: 'Course Content',
          },
          {to: '/blog', label: 'Announcements', position: 'left'},
          {to: '/docs/intro/prerequisites', label: 'Prerequisites', position: 'left'},
          {to: '/docs/intro/hardware-guide', label: 'Hardware Guide', position: 'left'},
          {
            href: 'https://github.com/your-org/Physical_AI_Humanoid_Robotics_Textbook',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Course',
            items: [
              {label: 'Introduction', to: '/docs/intro'},
              {label: 'Module 1: Physical AI', to: '/docs/module1-intro/what-is-physical-ai'},
              {label: 'Module 2: ROS 2', to: '/docs/module2-ros2/introduction-to-ros2'},
            ],
          },
          {
            title: 'Resources',
            items: [
              {label: 'Prerequisites', to: '/docs/intro/prerequisites'},
              {label: 'Hardware Guide', to: '/docs/intro/hardware-guide'},
              {label: 'ROS 2 Cheat Sheet', to: '/docs/appendices/ros2-cheat-sheet'},
              {label: 'Troubleshooting', to: '/docs/appendices/troubleshooting'},
            ],
          },
          {
            title: 'Community',
            items: [
              {label: 'Blog', to: '/blog'},
              {
                label: 'GitHub',
                href: 'https://github.com/your-org/Physical_AI_Humanoid_Robotics_Textbook',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
      },
      // Prism code highlighting with Palenight (dark) and GitHub (light)
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.palenight,
        additionalLanguages: ['bash', 'cpp', 'yaml', 'python'],
      },
    }),
};

export default config;
