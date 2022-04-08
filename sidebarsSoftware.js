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
      label: 'Get Started',
      items: [
      'cli-quickstart',
      'create-project',
      ],
    },
    {
      type: 'category',
      label: 'Develop',
      items: [
      'customize-image',
      'manage-airflow-versions',
      'access-airflow-database',
      'airflow-api',
      {
      type: 'category',
      label: 'Write DAGs',
      items: [
      'kubepodoperator',
      'kubepodoperator-local',
      'kubernetes-executor',
        ],
      },
      'cli-podman',
    ],
    },
    {
      type: 'category',
      label: 'Deploy',
      items: [
      'deploy-cli',
      'ci-cd',
      ],
    },
    {
      type: 'category',
      label: 'Administration',
      items: [
        {
        type: 'category',
        label: 'Install',
        items: [
        'install-aws',
        'install-azure',
        'install-gcp',
        'install-airgapped',
          ],
        },
        {
        type: 'category',
        label: 'Platform Setup',
        items: [
        'integrate-auth-system',
        'logs-to-s3',
        'registry-backend',
        'renew-tls-cert',
        'namespace-pools',
        'third-party-ingress-controllers',
          ],
        },
        {
        type: 'category',
        label: 'Platform Management',
        items: [
        'apply-platform-config',
        'upgrade-astronomer-stable',
        'houston-api',
        'configure-platform-resources',
          ],
        },
        {
          type: 'category',
          label: 'Deployment Management',
          items: [
          'configure-deployment',
          'secrets-backend',
          'environment-variables',
          'deploy-git-sync',
          'deploy-nfs',
          ],
        },
        {
        type: 'category',
        label: 'User Access',
        items: [
        'manage-workspaces',
        'import-idp-groups',
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
      'grafana-metrics',
      'kibana-logging',
      'airflow-alerts',
      'platform-alerts',
      ],
    },
    {
      type: 'category',
      label: 'Astronomer Certified',
      items: [
      'image-architecture',
      'single-node-install',
      'install-packages',
      'upgrade-ac',
      'ac-cve',
      'ac-support-policy',
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
    label: 'Release Notes',
    items: [
      'release-notes',
      'cli-release-notes',
    ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: [
      'system-components',
      'support',
      'cli-reference',
      'version-compatibility-reference',
      'release-lifecycle-policy',
      ],
    },
  ],
};
