/** @type {import('@docusaurus/types').DocusaurusConfig} */

module.exports = {
  title: 'Astronomer Documentation',
  tagline: 'Learn how to use Astro, the next-generation data orchestration platform.',
  url: 'https://docs.astronomer.io/',
  baseUrl: '/',
  noIndex: false,
  onBrokenLinks: 'error',
  onBrokenMarkdownLinks: 'error',
  favicon: 'img/favicon.svg',
  organizationName: 'astronomer', // Usually your GitHub org/user name.
  projectName: 'docs', // Usually your repo name.
  themeConfig: {
    image: 'img/meta.png',
    autoCollapseSidebarCategories: true,
    algolia: {
      apiKey: '99354995bfad26ed950bdb701bc56b6b',
      indexName: 'published-docs',
      // Optional: see doc section below
      contextualSearch: true,

      // Optional: see doc section below
      appId: 'TTRQ0VJY4D',
      inputSelector: '.DocSearch',
      // Optional: Algolia search parameters
      searchParameters: {
      },

      //... other Algolia params
    },
    colorMode: {
      disableSwitch: false,
    },
    navbar: {
      title: 'Docs',
      logo: {
        alt: 'Astronomer',
        src: 'img/LogoPrimaryDarkMode.svg',
        href: 'https://docs.astronomer.io/astro',
        target: '_self',
      },
      items: [
        {
          to: 'astro',
          label: 'Astro',
          position: 'left',
        },
        {
          type: 'dropdown',
          label: 'Software',
          to: 'software/',
          activeBaseRegex: 'software',
          position: 'left',
          activeClassName: 'navbar__link--active',
          items: [
            {
              label: '0.28 (Latest)',
              to: '/software/',
            },
            {
              label: '0.27',
              to: '/software/0.27/overview',
            },
            {
              label: '0.26',
              to: '/software/0.26/overview',
            },
            {
              label: '0.25',
              to: '/software/0.25/overview'
            },
            {
              label: '0.23',
              to: '/software/0.23/overview'
            },
            {
              label: '0.16 (Deprecated)',
              to: '/software/0.16/overview'
            },
          ],
        },
      ],
    },
    footer: {
      links: [
        {
          title: 'Astro',
          items: [
            {
              label: 'Log In',
              href: 'https://cloud.astronomer.io/login',
            },
            {
              label: 'Install Astro',
              to: 'astro/install-aws',
            },
            {
              label: 'Install the CLI',
              to: 'astro/install-cli',
            },
            {
              label: 'Create a Project',
              to: 'astro/create-project',
            },
            {
              label: 'Deploy Code',
              to: 'astro/deploy-code',
            },
          ],
        },
        {
          title: 'Astronomer Software',
          items: [
            {
              label: 'Overview',
              to: 'software/',
            },
            {
              label: 'Install on AWS',
              to: 'software/install-aws',
            },
            {
              label: 'Release Notes',
              to: 'software/release-notes',
            },
          ],
        },
        {
          title: 'Product Resources',
          items: [
            {
              label: 'Support',
              href: 'https://support.astronomer.io',
            },
            {
              label: 'Status',
              href: 'https://cloud-status.astronomer.io',
            },
            {
              label: 'Astronomer Registry',
              to: 'https://registry.astronomer.io/',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Astronomer Homepage',
              to: 'https://www.astronomer.io',
            },
            {
              label: 'Airflow Guides',
              href: 'https://www.astronomer.io/guides/',
            },
            {
              label: 'Docs on GitHub',
              href: 'https://github.com/astronomer/docs',
            },
          ],
        },
      ],
      copyright: '© Astronomer',
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebarsAstro.js'),
          editUrl: ({ docPath }) =>
            `https://github.com/astronomer/docs/blob/main/astro/${docPath}`,
          editLocalizedFiles: true,
          routeBasePath: 'astro',
          path: 'astro',
          admonitions: {
          },
        },
        gtag: {
          trackingID: 'G-DKTB1B78FV',
          anonymizeIP: true,
        },
        googleAnalytics: {
          trackingID: 'UA-54102728-4',
          anonymizeIP: true,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
        sitemap: {
          changefreq: 'hourly',
          priority: 0.5,
        },
      },
    ],
  ],
  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'software',
        routeBasePath: 'software',
        editUrl: ({ docPath }) =>
          `https://github.com/astronomer/docs/blob/main/software/${docPath}`,
        editCurrentVersion: true,
        sidebarPath: require.resolve('./sidebarsSoftware.js'),
        path: 'software',
        lastVersion: 'current',
        versions: {
        current: {
          label: '0.28',
          path: '',
          banner: 'none',
         },
       },
      },
    ],
  ],
};
