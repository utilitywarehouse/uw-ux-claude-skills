import { visit } from 'unist-util-visit';

// Astro's `base` config only rewrites links Astro/Starlight generate
// themselves (the sidebar, pagination). A plain markdown link written in
// content — [text](/knowledge-base/foo/) — is left exactly as written, so
// every internal cross-link across every page 404s once the site is
// deployed under a subpath. This walks the markdown tree and prepends
// `base` to any link that's root-relative (starts with `/`, not `//`),
// leaving anchors, relative links, and external URLs untouched.
export function remarkBaseLinks(base) {
  const prefix = base.replace(/\/$/, '');
  return () => (tree) => {
    visit(tree, 'link', (node) => {
      if (node.url && node.url.startsWith('/') && !node.url.startsWith('//')) {
        node.url = prefix + node.url;
      }
    });
  };
}
