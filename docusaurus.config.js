/** @type {import('@docusaurus/types').DocusaurusConfig} */
const versions = require('./software_versions.json')
module.exports = {
  title: 'Astronomer Documentation',
  tagline: 'Learn how to use Astro, the next-generation data orchestration platform.',
  url: 'https://docs.astronomer.io',
  baseUrl: '/',
  trailingSlash: false,
  noIndex: false,
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.svg',
  organizationName: 'astronomer', // Usually your GitHub org/user name.
  projectName: 'docs', // Usually your repo name.
  themeConfig: {
    image: 'img/meta.png',
    docs: {
      sidebar: {
        autoCollapseCategories: true,
      },
    },
    algolia: {
      apiKey: '99354995bfad26ed950bdb701bc56b6b',
      indexName: 'published-docs',
      // Optional: see doc section below
      contextualSearch: true,

      // Optional: see doc section below
      appId: 'TTRQ0VJY4D',
      inputSelector: '.DocSearch',      // Optional: Algolia search parameters
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
          type: 'dropdown',
          to: '/astro/',
          label: 'Astro',
          position: 'left',
          activeClassName: 'navbar__link--active',
          items: [
            {
              label: 'Cloud',
              to: '/astro/',
              activeBaseRegex: 'astro(?!\/cli)',
            },
            {
              label: 'Astro CLI',
              to: 'astro/cli/overview',
              activeBaseRegex: 'astro/cli+',
            },
          ],
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
              label: '0.29 (Latest)',
              to: '/software/',
              activeBaseRegex: `software(?!(\/${versions.join('|\\/')}))`,
            },
            {
              label: '0.28',
              to: '/software/0.28/overview',
              activeBaseRegex: '(software\/0.28)+',
            },
            {
              label: '0.25',
              to: '/software/0.25/overview',
              activeBaseRegex: '(software\/0.25)+',
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
              label: 'Install on AWS',
              to: 'astro/install-aws',
            },
            {
              label: 'Install on GCP',
              to: 'astro/install-gcp',
            },
            {
              label: 'Install the CLI',
              to: 'astro/cli/get-started',
            },
            {
              label: 'Create a project',
              to: 'astro/create-project',
            },
            {
              label: 'Deploy code',
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
            {
              label: 'Privacy Policy',
              to: 'https://www.astronomer.io/privacy/',
            },
            {
              label: 'Cookie Preferences',
              to: '#',
              id: 'cookiePref',
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
            tag: ':::',
            keywords: [
              'caution',
              'warning',
              'info',
              'tip',
              'cli',
            ],
          },
        },
        sitemap: {
        id: 'default',
        changefreq: 'daily',
        ignorePatterns: ['/software/0.28/**','/software/0.27/**','/software/0.26/**','/software/0.25/**','/software/0.23/**','/software/0.16/**'],
        filename: 'sitemap.xml',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
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
            label: '0.29',
            path: '',
            banner: 'none',
          },
        },
      },
    ],
    [
      '@docusaurus/plugin-sitemap',
      {
       id: 'software',
       changefreq: 'daily',
       ignorePatterns: ['/software/0.28/**','/software/0.27/**','/software/0.26/**','/software/0.25/**','/software/0.23/**','/software/0.16/**'],
       filename: 'sitemap.xml',
      },
    ]
  ],
  scripts: [
    {
      src: './scripts/segment.js',
      defer: true,
    },
    {
      src: './scripts/consent-manager.js',
      defer: true,
    },
    {
      src: './scripts/consent-manager-config.js',
    },
    {
      src: 'https://docs.astronomer.io/js/script.outbound-links.js',
      "data-domain": 'docs.astronomer.io',
      defer: true,
    }
  ],
};
