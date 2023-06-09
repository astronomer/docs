/** @type {import('@docusaurus/types').DocusaurusConfig} */
const versions = require('./software_versions.json')
module.exports = {
  title: 'Astronomer Documentation',
  tagline: 'Learn how to use Astro, the next-generation data orchestration platform.',
  url: 'https://docs.astronomer.io',
  baseUrl: '/',
  trailingSlash: false,
  noIndex: false,
  onBrokenLinks: 'warn', // 'warn' for drafts, 'throw' for prod
  onBrokenMarkdownLinks: 'warn',
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
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
    prism: {
      additionalLanguages: ['docker'],
    },
    colorMode: {
      disableSwitch: false,
    },
    navbar: {
      title: 'Docs',
      logo: {
        alt: 'Astronomer',
        src: 'img/AstroMonogram.svg',
        href: 'https://docs.astronomer.io',
        target: '_self',
      },
      items: [
        {
          to: '/',
          label: 'Home',
          position: 'left',
          activeClassName: 'navbar__link--active',
          activeBaseRegex: '^[\/]+$',
        },
        {
          to: '/astro/',
          label: 'Astro',
          position: 'left',
          activeClassName: 'navbar__link--active',
          activeBaseRegex: '^(\/astro)(?!(\/cli))',
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
    astroCard: {
      title: "What is Astro?",
      description: "Astro is a cloud solution that helps you focus on your data pipelines and spend less time managing Apache Airflow, with capabilities enabling you to build, run, and observe data all in one place.",
      buttons: {
        primary: {
          label: "Try Astro",
          href: "https://www.astronomer.io/try-astro/?referral=docs-what-astro-banner"
        },
        secondary: {
          label: "Learn about Astronomer",
          href: "https://www.astronomer.io/?referral=docs-what-astro-banner"
        }
      }
    },
    newsletterForm: {
      title: "Sign up for Developer Updates",
      buttonText: "Submit",
      successMessage: "Success! ✓",
      errorMessage: "Sorry, there was issue sending your email. Please try again.",
    },
    softwareNav: {
      items: [
        {
          label: '0.32 (Latest)',
          to: '/software/',
          activeBaseRegex: `software(?!(\/${versions.join('|\\/')}))`,
        },
        {
          label: '0.30',
          to: '/software/0.30/',
          activeBaseRegex: '(software\/0.30)+',
        },
        {
          label: 'Archive',
          to: '/software/documentation-archive',
          activeBaseRegex: `software(?!(\/${versions.join('|\\/')}))`,
        },
      ],
    },
    sidebarNav: {
      bottomNav: {
        items: [
          {
            label: 'Book Office Hours',
            href: 'https://calendly.com/d/yy2-tvp-xtv/astro-data-engineering-office-hours-ade',
          },
          {
            label: 'Watch a webinar',
            href: 'https://www.astronomer.io/events/webinars/?referral=docs-sidebar',
          },
          {
            label: 'Astro status',
            href: 'https://status.astronomer.io/?referral=docs-sidebar',
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
          label: 'Legal',
          href: 'https://www.astronomer.io/legal/',
        },
        {
          label: 'Privacy',
          href: 'https://www.astronomer.io/privacy/',
        },
        {
          label: 'Security',
          href: 'https://www.astronomer.io/security/',
        },
        {
          label: 'Cookie Preferences',
          to: '#',
          id: 'cookiePref',
        },
      ],
      copyright: '© Astronomer 2023. Various trademarks held by their respective owners.',
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
              'highlight'
            ],
          },
        },
        sitemap: {
          id: 'default',
          changefreq: 'daily',
          filename: 'sitemap.xml',
          ignorePatterns: ['/astro/kubernetes-executor', '/astro/cli/sql-cli', '/astro/cross-account-role-setup']
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
            label: '0.32',
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
        filename: 'sitemap.xml',
        ignorePatterns: ['/astro/kubernetes-executor', '/astro/cli/sql-cli', '/astro/cross-account-role-setup']
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
  clientModules: [
    require.resolve('./segment-page.mjs'),
  ],
};
