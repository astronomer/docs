/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation
 The sidebars can be generated from the filesystem, or explicitly defined here.
 Create as many sidebars as you want.
 */

module.exports = {
  software: [
    {
      type: 'doc',
      id: 'overview',
      label: 'Overview',
    },
    {
      type: 'category',
      label: 'Get started',
      items: [
        'documentation-overview',
        'log-in-to-software',
        'create-project',
      ],
    },
    {
      type: 'category',
      label: 'Develop',
      items: [
        'customize-image',
        'upgrade-to-airflow-2',
        'access-airflow-database',
        'airflow-api',
        {
          type: 'category',
          label: 'Write DAGs',
          items: [
            'kubepodoperator',
            'kubernetes-executor',
          ],
        },
        'upgrade-astro-cli',
      ],
    },
    {
      type: 'category',
      label: 'Administration',
      items: [
        {
          type: 'category',
          label: 'Install',
          link: {
            type: 'generated-index',
            title: 'Install Astronomer Software',
            description: 'Install the Astro platform in your cloud.'
          },
          items: [
            'install-aws',
            'install-azure',
            'install-gcp',
            'install-airgapped',
          ],
        },
        'upgrade-astronomer',
        'apply-platform-config',
        {
          type: 'category',
          label: 'Manage platform resources',
          items: [
            'registry-backend',
            'namespace-pools',
            'configure-platform-resources',
            'cluster-resource-provisioning',
          ],
        },
        {
        type: 'category',
        label: 'Manage Deployments',
        items: [
          'configure-deployment',
          'create-deployment',
          'deployment-resources',
          'clean-up-and-delete-deployment',
          'environment-variables',
          'customize-resource-usage',
          {
            type: 'category',
            label: 'Deploy options',
            items: [
            'deploy-code-overview',
            'deploy-cli',
            'deploy-dags',
            'deploy-git-sync',
            'deploy-nfs',
              ],
            },
          ],
        },
        {
          type: 'category',
          label: 'CI/CD and automation',
          items: [
            'ci-cd',
            'houston-api',
            'deploy-git-sync',
            'deploy-nfs',
          ],
        },
        {
          type: 'category',
          label: 'CI/CD and automation',
          items: [
            'ci-cd',
            {
              type: 'category',
              label: 'Houston API',
              items: [
                'houston-api',
                'houston-api-examples',
              ],
            },
            'deploy-git-sync',
            'deploy-nfs',
          ],
        },
        {
          type: 'category',
          label: 'Security and compliance',
          items: [
            'secrets-backend',
            'custom-image-registry',
            'third-party-ingress-controllers',
            'self-signed-certificate',
            'renew-tls-cert',
          ],
        },
        {
          type: 'category',
          label: 'User access and management',
          items: [
            'integrate-auth-system',
            'import-idp-groups',
            'manage-workspaces',
            'workspace-permissions',
            'manage-platform-users',
            'integrate-iam',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Observability',
      items: [
        'deployment-logs',
        'airflow-alerts',
      ],
    },
    {
      type: 'category',
      label: 'Astro Runtime',
      items: [
        'manage-airflow-versions',
        'runtime-image-architecture',
        'migrate-to-runtime',
        'runtime-version-lifecycle-policy',
      ],
    },
    {
      type: 'category',
      label: 'Troubleshoot',
      items: [
        'kubectl',
        'debug-install',
        'disaster-recovery',
      ],
    },
    {
      type: 'category',
      label: 'Release notes',
      items: [
        'release-notes',
        {
          type: 'link',
          label: 'Astro CLI',
          href: 'https://www.astronomer.io/docs/astro/cli/release-notes',
        },
        {
          type: 'link',
          label: 'Astro Runtime',
          href: 'https://www.astronomer.io/docs/astro/runtime-release-notes',
        },
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: [
        {
          type: 'link',
          label: 'Astro CLI command reference',
          href: 'https://www.astronomer.io/docs/astro/cli/reference',
        },
        {
          type: 'category',
          label: 'Astronomer Certified (Deprecated)',
          items: [
            'single-node-install',
            'image-architecture',
            'install-packages',
            'upgrade-ac',
            'ac-cve',
            'ac-support-policy',
          ],
        },
        'role-permission-reference',
        'system-components',
        'support',
        'version-compatibility-reference',
        'release-lifecycle-policy',
        'faq',
        'documentation-archive',
      ],
    },
  ],
};
