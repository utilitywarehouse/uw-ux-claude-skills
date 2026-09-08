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
      description:
        "Docs for the UX team's Claude Code skills — a self-development project, not an official UW product.",
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
          label: 'Start here',
          items: [{ label: 'Start here', link: '/' }],
        },
        {
          label: 'Install',
          items: [{ label: 'Install the plugin', link: '/install/' }],
        },
        {
          label: 'Your knowledge base',
          items: [{ label: 'Your knowledge base', link: '/knowledge-base/' }],
        },
        {
          label: 'The skills',
          items: [
            { label: 'Overview', link: '/skills/' },
            { label: 'setup-my-knowledge-base', link: '/skills/setup-my-knowledge-base/' },
            { label: 'new-project-setup', link: '/skills/new-project-setup/' },
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
