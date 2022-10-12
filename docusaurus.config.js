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
        src: 'img/AstroMonogram.svg',
        href: 'https://www.astronomer.io/',
        target: '_self',
      },
      items: [
        {
          to: '/',
          label: 'Home',
          position: 'left',
          activeClassName: 'navbar__link--active',
          activeBaseRegex: '(?!)',
        },
        {
          to: '/astro/',
          label: 'Astro',
          position: 'left',
          activeClassName: 'navbar__link--active',
          activeBaseRegex: 'astro(?!\/cli)',
        },
        {
          to: '/astro/cli/overview',
          label: 'Astro CLI',
          position: 'left',
          activeClassName: 'navbar__link--active',
          activeBaseRegex: 'astro/cli+',
        },
        {
          label: 'Software',
          to: 'software/',
          activeBaseRegex: 'software',
          position: 'left',
          activeClassName: 'navbar__link--active',
        },
        {
          to: '/learn/',
          label: 'Learn',
          position: 'left',
          activeClassName: 'navbar__link--active',
        },
      ],
    },
    astroCallToAction: {
      title: "What is Astro?",
      description: "Astro is a cloud solution that helps you focus on your data pipelines and spend less time managing Apache Airflow, with capabilities enabling you to build, run and observe data all in one place.",
      buttons: [
        {
          label: "Try Astro",
          href: "https://www.astronomer.io/get-started?utm_source=docs-what-astro-banner"
        },
        {
          label: "LEARN ABOUT ASTRONOMER",
          href: "https://www.astronomer.io/?utm_source=docs-what-astro-banner"
        }
      ]
    },
    softwareNav: {
      items: [
        {
          label: '0.30 (Latest)',
          to: '/software/',
          activeBaseRegex: `software(?!(\/${versions.join('|\\/')}))`,
        },
        {
          label: '0.29',
          to: '/software/0.29/overview',
          activeBaseRegex: '(software\/0.29)+',
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
    sidebarNav: {
      bottomNav: {
        items: [
          {
            label: 'Get a demo',
            href: 'https://www.astronomer.io/events/weekly-demo/?utm_source=docs-sidebar',
          },
          {
            label: 'Watch a webinar',
            href: 'https://www.astronomer.io/events/webinars/?utm_source=docs-sidebar',
          },
          {
            label: 'Astro status',
            href: 'https://status.astronomer.io/?utm_source=docs-sidebar',
          }
        ]
      }
    },
    footer: {
      logo: {
        alt: "Astronomer logo",
        src: "img/monogram-light.png",
        href: "https://www.astronomer.io/",
        width: 48,
      },
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
              href: 'https:/docs.astronomer.io/learn/',
            },
            {
              label: 'Docs on GitHub',
              href: 'https://github.com/astronomer/docs',
            },
          ],
        },
      ],
      copyright: '© Astronomer 2022. Various trademarks held by their respective owners.',
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
          ignorePatterns: ['/software/0.29/**', '/software/0.28/**', '/software/0.27/**', '/software/0.26/**', '/software/0.25/**', '/software/0.23/**', '/software/0.16/**'],
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
            label: '0.30',
            path: '',
            banner: 'none',
          },
        },
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'learn',
        routeBasePath: 'learn',
        editUrl: ({ docPath }) =>
          `https://github.com/astronomer/docs/blob/main/learn/${docPath}`,
        editCurrentVersion: true,
        sidebarPath: require.resolve('./sidebarsLearn.js'),
        path: 'learn',
      },
    ],
    [
      '@docusaurus/plugin-sitemap',
      {
        id: 'learn',
        changefreq: 'daily',
        ignorePatterns: ['/software/0.29/**', '/software/0.28/**', '/software/0.27/**', '/software/0.26/**', '/software/0.25/**', '/software/0.23/**', '/software/0.16/**'],
        filename: 'sitemap.xml',
      },
    ],
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
      src: "/scripts/set-tab.js",
      async: true,
      defer: true,
    },
    {
      src: 'https://docs.astronomer.io/js/script.outbound-links.js',
      "data-domain": 'docs.astronomer.io',
      defer: true,
    }
  ],
};
