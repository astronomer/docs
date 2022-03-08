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
      label: 'Getting Started',
      items: [
        'install-aws',
        'install-cli',
      ],
    },
    {
      type: 'category',
      label: 'Develop',
      items: [
        'create-project',
        'develop-project',
        'deploy-code',
        'airflow-api',
        'airflow-alerts',
        'kubernetespodoperator',
        'deferrable-operators',
        'test-and-troubleshoot-locally',
      ],
    },
    {
      type: 'category',
      label: 'Manage Deployments',
      items: [
        'configure-deployment',
        'api-keys',
        'ci-cd',
        'deployment-metrics',
        'scheduler-logs',
        'environment-variables',
        'secrets-backend',
      ],
    },
    {
      type: 'category',
      label: 'Administration',
      items: [
        'create-cluster',
        'configure-idp',
        'manage-workspaces',
        'add-user',
        'user-permissions',
        'modify-cluster',
      ],
    },
    {
      type: 'category',
      label: 'Astronomer Runtime',
      items: [
        'upgrade-runtime',
        'runtime-version-lifecycle-policy',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: [
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
          label: 'CLI Command Reference',
          link: {type: 'doc', id: 'cli-reference'},
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
            'cli-reference/astrocloud-workspace-switch',          ],
        },
        'known-limitations',
        'resource-reference-aws',
        'platform-variables',
        {
          type: 'category',
          label: 'Security',
          link: {type: 'doc', id: 'security'},
          items: [
            'shared-responsibility-model',
            'resilience',
            'disaster-recovery',
            'data-protection',
            'secrets-management',  ],
        },
      ],
    },
  ],
};
