/** @type {import('@docusaurus/types').DocusaurusConfig} */

module.exports = {
  title: 'Astronomer Cloud',
  tagline: 'Get Started with the Next Generation of Astronomer Cloud',
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
    algolia: {
      apiKey: '99354995bfad26ed950bdb701bc56b6b',
      indexName: 'published-docs',

      // Optional: see doc section below
      contextualSearch: true,

      // Optional: see doc section below
      appId: 'TTRQ0VJY4D',
      inputSelector:'.DocSearch',
      // Optional: Algolia search parameters
      searchParameters: {
      },

      //... other Algolia params
    },
    colorMode: {
      disableSwitch: false,
      switchConfig: {
        darkIcon: '☾',
        darkIconStyle: {
          marginLeft: '1px',
        },
        lightIcon: '☼',
        lightIconStyle: {
          marginLeft: '1px',
        },
      },
    },
    navbar: {
      title: 'Docs',
      logo: {
        alt: 'Astronomer',
        src: 'img/LogoPrimaryDarkMode.svg',
        href: 'https://www.astronomer.io/',
      },
      items: [
        {
          to: 'cloud',
          label: 'Cloud',
          position: 'left',
        },
        {
          type: 'dropdown',
          label: 'Enterprise',
          to: 'enterprise/overview',
          activeBaseRegex: 'enterprise',
          position: 'left',
          activeClassName: 'navbar__link--active',
          items: [
            {
              label: '0.27 (Latest)',
              to: '/enterprise/overview',
            },
            {
              label: '0.26',
              to: '/enterprise/0.26/overview',
            },
            {
              label: '0.25',
              to: '/enterprise/0.25/overview'
            },
            {
              label: '0.23',
              to: '/enterprise/0.23/overview'
            },
            {
              label: '0.16',
              to: '/enterprise/0.16/overview'
            },
          ],
        },
      ],
    },
    footer: {
      links: [
        {
          title: 'Astronomer Cloud',
          items: [
            {
              label: 'Install Astronomer Cloud',
              to: 'cloud/install-aws',
            },
            {
              label: 'Install the CLI',
              to: 'cloud/install-cli',
            },
            {
              label: 'Create a Project',
              to: 'cloud/create-project',
            },
            {
              label: 'Deploy Code',
              to: 'cloud/deploy-code',
            },
          ],
        },
        {
          title: 'Astronomer Enterprise',
          items: [
            {
              label: 'Overview',
              to: 'enterprise/overview',
            },
            {
              label: 'Install on AWS',
              to: 'enterprise/install-aws',
            },
            {
              label: 'Release Notes',
              to: 'enterprise/release-notes',
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
          sidebarPath: require.resolve('./sidebarsCloud.js'),
          editUrl: ({ docPath }) =>
            `https://github.com/astronomer/docs/blob/main/cloud/${docPath}`,
          editLocalizedFiles: true,
          routeBasePath: 'cloud',
          path: 'cloud',
          admonitions: {
          },
        },
        gtag: {
          trackingID: 'G-W97HK48NPT',
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
        id: 'enterprise',
        routeBasePath: 'enterprise',
        editUrl: ({ docPath }) =>
            `https://github.com/astronomer/docs/blob/main/enterprise/${docPath}`,
        editCurrentVersion: true,
        sidebarPath: require.resolve('./sidebarsEnterprise.js'),
        path: 'enterprise',
        lastVersion: 'current',
        versions: {
        current: {
          label: '0.27',
          path: '',
          banner: 'none',
         },
       },
      },
    ],
  ],
};
