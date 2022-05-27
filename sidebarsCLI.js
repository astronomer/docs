module.exports = {
  cli: [
      {
        type: 'doc',
        label: 'CLI Overview',
        id: 'cli/overview'
      },
      {
        type: 'doc',
        label: 'Quickstart',
        id: 'cli/cli-quickstart'
      },
      {
      type: 'category',
      label: 'CLI Command Reference',
      link: { type: 'doc', id: 'reference' },
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
        'cli/astro-version',
        'cli/astro-workspace-list',
        'cli/astro-workspace-switch',],
    },
    {
      type: 'doc',
      label: 'Release Notes',
      id: 'cli/cli-release-notes'
    },
  ],
};
