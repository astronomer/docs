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
      label: 'Get Started',
      items: [
        'install-cli',
        'create-project',
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
        'configure-deployment',
        'api-keys',
        'environment-variables',
        'secrets-backend',
      ],
    },
    {
      type: 'category',
      label: 'Observability',
      items: [
        'deployment-metrics',
        'scheduler-logs',
        'airflow-alerts',
      ],
    },
    {
      type: 'category',
      label: 'Administration',
      items: [
        'install-aws',
        'manage-workspaces',
        {
          type: 'category',
          label: 'User Access',
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
            'create-cluster',
            'modify-cluster',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Release Notes',
      items: [
        'release-notes',
        'cli-release-notes',
        'runtime-release-notes',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: [
        {
          type: 'category',
          label: 'CLI Command Reference',
          link: { type: 'doc', id: 'cli-reference' },
          items: [
            'cli-reference/astrocloud-auth-login',
            'cli-reference/astrocloud-auth-logout',
            'cli-reference/astrocloud-completion',
            'cli-reference/astrocloud-deploy',
            'cli-reference/astrocloud-deployment-create',
            'cli-reference/astrocloud-deployment-delete',
            'cli-reference/astrocloud-deployment-list',
            'cli-reference/astrocloud-deployment-logs',
            'cli-reference/astrocloud-deployment-update',
            'cli-reference/astrocloud-dev-init',
            'cli-reference/astrocloud-dev-kill',
            'cli-reference/astrocloud-dev-logs',
            'cli-reference/astrocloud-dev-parse',
            'cli-reference/astrocloud-dev-ps',
            'cli-reference/astrocloud-dev-pytest',
            'cli-reference/astrocloud-dev-run',
            'cli-reference/astrocloud-dev-start',
            'cli-reference/astrocloud-dev-stop',
            'cli-reference/astrocloud-dev-restart',
            'cli-reference/astrocloud-version',
            'cli-reference/astrocloud-workspace-list',
            'cli-reference/astrocloud-workspace-switch',],
        },
        'known-limitations',
        'runtime-version-lifecycle-policy',
        'resource-reference-aws',
        'platform-variables',
        'data-plane-activation',
        'data-lineage-support-and-compatibility',
        {
          type: 'category',
          label: 'Security',
          link: { type: 'doc', id: 'security' },
          items: [
            'shared-responsibility-model',
            'resilience',
            'disaster-recovery',
            'data-protection',
            'secrets-management',],
        },
      ],
    },
  ],
};
