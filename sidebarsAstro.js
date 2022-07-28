/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation
 The sidebars can be generated from the filesystem, or explicitly defined here.
 Create as many sidebars as you want.
 */

module.exports = {
  cloud: [
    {
      type: 'doc',
      label: 'Overview',
      id: 'overview'
    },
    {
      type: 'category',
      label: 'Get started',
      items: [
        'log-in-to-astro',
        'create-project',
        'create-deployment',
      ],
    },
    {
      type: 'category',
      label: 'Develop',
      items: [
        'develop-project',
        {
          type: 'category',
          label: 'Write DAGs',
          items: [
            'deferrable-operators',
            'kubepodoperator-local',
            'kubernetespodoperator',
          ],
        },
        'upgrade-runtime',
        'airflow-api',
        'test-and-troubleshoot-locally',
      ],
    },
    {
      type: 'category',
      label: 'Deploy',
      items: [
        'deploy-code',
        'ci-cd',
      ],
    },
    {
      type: 'category',
      label: 'Manage Deployments',
      items: [
        'configure-deployment-resources',
        'api-keys',
        'environment-variables',
        'secrets-backend',
      ],
    },
    {
      type: 'category',
      label: 'Observability',
      items: [
        'view-logs',
        'deployment-metrics',
        {
          type: 'category',
          label: 'Data lineage',
          items: [
            'set-up-data-lineage',
            'data-lineage',
          ],
        },
        'airflow-alerts',
      ],
    },
    {
      type: 'category',
      label: 'Administration',
      items: [
        {
          type: 'category',
          label: 'Install Astro',
          items: [
            'install-aws',
            'install-azure',
            'install-gcp',
          ],
        },
        'manage-workspaces',
        {
          type: 'category',
          label: 'User access',
          items: [
            'add-user',
            'user-permissions',
            'configure-idp',
          ],
        },
        {
          type: 'category',
          label: 'Manage Clusters',
          items: [
            'view-clusters',
            'create-cluster',
            'modify-cluster',
            'connect-external-services',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Release notes',
      items: [
        'release-notes',
        'runtime-release-notes',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: [
        'known-limitations',
        'runtime-image-architecture',
        'runtime-version-lifecycle-policy',
        'astro-support',
        {
          type: 'category',
          label: 'Cloud configuration reference',
          items: [
            'resource-reference-aws',
            'resource-reference-azure',
            'resource-reference-gcp',
          ],
        },
        'platform-variables',
        'data-plane-activation',
        {
          type: 'category',
          label: 'Data lineage',
          items: [
            'data-lineage-support-and-compatibility',
            'data-lineage-concepts',],
        },
        {
          type: 'category',
          label: 'Security',
          link: { type: 'doc', id: 'security' },
          items: [
            'shared-responsibility-model',
            'resilience',
            'disaster-recovery',
            'data-protection',
            'gdpr-compliance',
            'secrets-management',],
        },
      ],
    },
  ],
  cli: [
      {
        type: 'doc',
        label: 'CLI overview',
        id: 'cli/overview'
      },
      {
        type: 'doc',
        label: 'Get started',
        id: 'cli/get-started'
      },
    {
      type: 'doc',
      label: 'Configure the CLI',
      id: 'cli/configure-cli'
    },
    {
      type: 'doc',
      label: 'Release notes',
      id: 'cli/release-notes'
    },
    {
    type: 'category',
    label: 'Command reference',
    link: { type: 'doc', id: 'cli/reference' },
    items: [
      'cli/astro-login',
      'cli/astro-logout',
      'cli/astro-completion',
      'cli/astro-config-get',
      'cli/astro-config-set',
      'cli/astro-context-delete',
      'cli/astro-context-list',
      'cli/astro-context-switch',
      'cli/astro-completion',
      'cli/astro-deploy',
      'cli/astro-deployment-create',
      'cli/astro-deployment-delete',
      'cli/astro-deployment-list',
      'cli/astro-deployment-logs',
      'cli/astro-deployment-update',
      'cli/astro-deployment-variable-create',
      'cli/astro-deployment-variable-list',
      'cli/astro-deployment-variable-update',
      'cli/astro-dev-init',
      'cli/astro-dev-kill',
      'cli/astro-dev-logs',
      'cli/astro-dev-parse',
      'cli/astro-dev-ps',
      'cli/astro-dev-pytest',
      'cli/astro-dev-run',
      'cli/astro-dev-start',
      'cli/astro-dev-stop',
      'cli/astro-dev-restart',
      'cli/astro-login',
      'cli/astro-logout',
      'cli/astro-version',
      'cli/astro-workspace-list',
      'cli/astro-workspace-switch',],
  },
  ],
};
