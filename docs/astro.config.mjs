// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// This site is published via GitHub Pages from the utilitywarehouse/uw-ux-claude-skills repo.
// Pages serves project sites at https://<org>.github.io/<repo>/, so `base` must match the repo name.
export default defineConfig({
  site: 'https://utilitywarehouse.github.io',
  base: '/uw-ux-claude-skills',
  integrations: [
    starlight({
      title: 'UW UX Claude Skills',
      description: "The UW UX team's knowledge base and the Claude Code Skills that run it.",
      logo: {
        light: './src/assets/wordmark-purple.svg',
        dark: './src/assets/wordmark-warm-white.svg',
        alt: 'Utility Warehouse',
        replacesTitle: true,
      },
      customCss: ['./src/styles/uw-brand.css'],
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/utilitywarehouse/uw-ux-claude-skills',
        },
      ],
      editLink: {
        baseUrl: 'https://github.com/utilitywarehouse/uw-ux-claude-skills/edit/main/docs/',
      },
      sidebar: [
        {
          label: 'UX AI Operating System',
          items: [{ label: 'UX AI Operating System', link: '/' }],
        },
        {
          label: 'Concepts',
          items: [
            { label: 'Claude Chat, Cowork, and Code', link: '/concepts/claude-products/' },
            { label: 'Terminal basics', link: '/concepts/terminal-basics/' },
            { label: 'Git and GitHub', link: '/concepts/git-and-github/' },
            { label: 'What is a knowledge base?', link: '/concepts/what-is-a-knowledge-base/' },
            { label: 'Plugins and Skills', link: '/concepts/plugins-and-skills/' },
          ],
        },
        {
          label: 'Install',
          items: [
            { label: 'Install the plugin', link: '/install/' },
            { label: 'Before you start', link: '/install/before-you-start/' },
          ],
        },
        {
          label: 'Your knowledge base',
          items: [
            { label: 'Your knowledge base', link: '/knowledge-base/' },
            { label: 'Folder structure', link: '/knowledge-base/folder-structure/' },
            { label: 'CLAUDE.md and memory', link: '/knowledge-base/claude-md-and-memory/' },
            {
              label: 'Worked example: Design System',
              link: '/knowledge-base/worked-example-design-system/',
            },
            { label: 'Research Repository', link: '/knowledge-base/research-repository/' },
            { label: 'FAQ', link: '/knowledge-base/faq/' },
          ],
        },
        {
          label: 'The skills',
          items: [
            { label: 'Overview', link: '/skills/' },
            { label: 'setup-my-knowledge-base', link: '/skills/setup-my-knowledge-base/' },
            { label: 'new-project-setup', link: '/skills/new-project-setup/' },
            { label: 'research-transcript-cleaner', link: '/skills/research-transcript-cleaner/' },
            { label: 'research-transcript-coder', link: '/skills/research-transcript-coder/' },
            { label: 'study-writeup', link: '/skills/study-writeup/' },
            { label: 'knowledgebase-health-check', link: '/skills/knowledgebase-health-check/' },
            { label: 'end-session', link: '/skills/end-session/' },
            { label: 'propose-skill', link: '/skills/propose-skill/' },
            {
              label: 'contribute-to-shared-knowledgebase',
              link: '/skills/contribute-to-shared-knowledgebase/',
            },
            { label: 'figma-craft', link: '/skills/figma-craft/' },
            { label: 'figma-dev-handoff', link: '/skills/figma-dev-handoff/' },
          ],
        },
        {
          label: 'Contribute',
          items: [{ label: 'Contribute', link: '/contribute/' }],
        },
      ],
    }),
  ],
});
