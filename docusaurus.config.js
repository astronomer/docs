/** @type {import('@docusaurus/types').DocusaurusConfig} */
const versions = require('./software_versions.json')
module.exports = {
  title: 'Astronomer Documentation',
  tagline: 'Learn how to use Astro, the next-generation data orchestration platform.',
  url: 'https://www.astronomer.io',
  baseUrl: '/docs',
  trailingSlash: false,
  noIndex: false,
  onBrokenLinks: 'throw', // 'warn' for drafts, 'throw' for prod
  onBrokenMarkdownLinks: 'throw',
  onBrokenAnchors: 'warn',
  markdown: {
    mermaid: true,
    preprocessor: ({ filePath, fileContent }) => {
      function updateValues() {
        var mapObj = {
          '{{CLI_VER_LATEST}}': "1.27.1",
          '{{CLI_VER_2}}': "1.26.0",
          '{{CLI_VER_3}}': "1.25.0",
          '{{RUNTIME_VER}}': "11.6.0",
        };
        var re = new RegExp(Object.keys(mapObj).join("|"), "gi");
        return fileContent.replaceAll(re, function (matched) {
          return mapObj[matched];
        });
      }
      return updateValues();
    },
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
      additionalLanguages: ["bash", "json", "docker", "python"],
    },
    colorMode: {
      disableSwitch: false,
    },
    mermaid: {
      theme: { dark: 'neutral' },
    },
    navbar: {
      title: 'Docs',
      logo: {
        alt: 'Astronomer',
        src: 'img/AstroMonogram.svg',
        href: 'https://www.astronomer.io',
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
          to: '/software/',
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
          href: "https://www.astronomer.io/try-astro/?referral=docs-what-astro-banner&utm_medium=docs&utm_content=astr&utm_source=body"
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
    promoBanner: {
      text: "Don't miss the biggest Airflow event of the year: Airflow Summit 2023, Sept 19-21",
      buttonText: "Join Us →",
      url: "https://www.astronomer.io/events/airflow-summit-2023/"
    },
    feedbackWidget: {
      question: "Was this page helpful?",
      thanksText: "Thank you for your feedback!",
    },
    softwareNav: {
      items: [
        {
          label: '0.35 (Latest)',
          to: '/docs/software/',
          activeBaseRegex: `software(?!(\/${versions.join('|\\/')}))`,
        },
        {
          label: '0.34',
          to: '/docs/software/0.34/',
          activeBaseRegex: `(software\/0.34)+`,
        },
        {
          label: '0.33',
          to: '/docs/software/0.33/',
          activeBaseRegex: `(software\/0.33)+`,
        },
        {
          label: '0.32',
          to: '/docs/software/0.32/',
          activeBaseRegex: `(software\/0.32)+`,
        },
        {
          label: '0.30',
          to: '/docs/software/0.30/',
          activeBaseRegex: '(software\/0.30)+',
        },
        {
          label: 'Archive',
          to: '/docs/software/documentation-archive',
          activeBaseRegex: `software(?!(\/${versions.join('|\\/')}))`,
        },
      ],
    },
    sidebarNav: {
      bottomNav: {
        items: [
          {
            label: 'Support Knowledge Base',
            href: 'https://support.astronomer.io/hc/en-us',
          },
          {
            label: 'Office Hours',
            href: 'https://calendly.com/d/yy2-tvp-xtv/astro-data-engineering-office-hours-ade',
          },
          {
            label: 'Webinars',
            href: 'https://www.astronomer.io/events/webinars/?referral=docs-sidebar',
          },
          {
            label: 'Astro Status',
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
      copyright: '© Astronomer 2024. Various trademarks held by their respective owners.',
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
            keywords: [
              'caution',
              'danger',
              'info',
              'tip',
              'cli',
              'highlight',
              'privatepreview',
              'publicpreview',
              'cliastroonly',
              'clisoftwareonly',
              'cliastroandsoftware'
            ],
            extendDefaults: true,
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
    [
      'redocusaurus',
      {
        // Plugin Options for loading OpenAPI files
        specs: [
          {
            id: 'platform',
            spec: 'https://api.astronomer.io/spec/platform/v1beta1',
          },
          {
            id: 'iam',
            spec: 'https://api.astronomer.io/spec/iam/v1beta1',
          },
          {
            id: 'using-remote-url',
            // Remote File
            spec: 'https://redocly.github.io/redoc/openapi.yaml',
            route: '/examples/using-remote-url/',
          },
        ],
        // Theme Options for modifying how redoc renders them
        theme: {
          // Change with your site colors
          primaryColor: '#7352ba',
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
            label: '0.35',
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
      src: '/docs/scripts/segment.js',
      defer: true,
    },
    {
      src: '/docs/scripts/consent-manager.js',
      defer: true,
    },
    {
      src: '/docs/scripts/consent-manager-config.js',
    },
    {
      src: "/docs/scripts/set-tab.js",
      async: true,
      defer: true,
    },
    {
      src: '/docs/scripts/remix-redocly.js',
      async: true,
      defer: true,
    },
  ],
  clientModules: [
    require.resolve('./segment-page.mjs'),
  ],
};
