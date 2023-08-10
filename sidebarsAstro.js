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
      type: 'category',
      label: 'Overview',
      link: { type: 'doc', id: 'overview' },
      items: [
        'astro-architecture',
        'features',
      ],
    },
    {
      type: "category",
      label: "Get started",
      items: [
        "trial",
        "create-first-DAG",
        'log-in-to-astro', 
        {
          type: "category",
          label: "Migrate to Astro",
          items: ["migrate-mwaa", "migrate-gcc"],
        },
      ],
    },
    {
      type: "category",
      label: "Develop",
      items: [
        "develop-project",
        "kubernetespodoperator",
        {
          type: "category",
          label: "Airflow connections and variables",
          items: [
            "manage-connections-variables",
            "import-export-connections-variables",
          ],
        },
        {
          type: "category",
          label: "Cloud IDE",
          items: [
            "cloud-ide/overview",
            "cloud-ide/quickstart",
            "cloud-ide/run-python",
            "cloud-ide/run-sql",
            "cloud-ide/use-airflow-operators",
            "cloud-ide/document-pipeline",
            "cloud-ide/run-cells",
            "cloud-ide/configure-project-environment",
            "cloud-ide/deploy-project",
            "cloud-ide/security",
            "cloud-ide/custom-cell-reference"
          ],
        },
        "upgrade-runtime",
        "airflow-api",
        "test-and-troubleshoot-locally",
      ],
    },
    {
      type: "category",
      label: "Deploy code",
      items: [
        "deploy-code",
        "deploy-project-image",
        "deploy-dags", 
        "set-up-ci-cd", 
        {
          type: "category",
          label: "CI/CD templates",
          items: [
            "ci-cd-templates/template-overview",
            "ci-cd-templates/github-actions",
            "ci-cd-templates/jenkins",
            "ci-cd-templates/gitlab",
            "ci-cd-templates/aws-s3",
            "ci-cd-templates/aws-codebuild",
            "ci-cd-templates/azure-devops",
            "ci-cd-templates/gcs",
            "ci-cd-templates/bitbucket",
            "ci-cd-templates/circleci",
            "ci-cd-templates/drone",
          ],
        },
      ],
    },
    {
      type: "category",
      label: "Manage Deployments",
      items: [
        "create-deployment",
        "configure-deployment-resources",
        "manage-dags",
        {
          type: "category",
          label: "Configure executors",
          items: ["executors-overview","celery-executor", "kubernetes-executor"],
        }, 
        "configure-worker-queues",
        "api-keys",
        "environment-variables",
        "secrets-backend",
        "manage-deployments-as-code",
        {
          type: "category",
          label: "Connect to external resources",
          link: {
            type: 'generated-index',
            title: 'Connect Astro',
            description: 'Connect Astro to your existing cloud resources.'
          },
          items: ["astro-ips","connect-aws", "connect-azure", "connect-gcp"],
        },       
      ],
    },
    {
      type: "category",
      label: "Observability",
      items: [
        "view-logs",
        {
          type: "category",
          label: "View metrics",
          items: ["dag-metrics", "deployment-metrics", "organization-metrics"],
        },
        {
          type: "category",
          label: "Data lineage",
          items: ["set-up-data-lineage", "data-lineage"],
        },
        "alerts",
        "airflow-email-notifications",
      ],
    },
    {
      type: "category",
      label: "Administration",
      items: [
        {
          type: "category",
          label: "Organizations",
          items: [
            {
              type: "category",
              label: "User access",
              items: [
                "configure-idp",
                "set-up-scim-provisioning",
                "manage-domains",
                "add-user", 
                "manage-teams", 
                "user-permissions",
              ],
            },
            "organization-api-tokens",
            "audit-logs",
          ],
        },
        {
          type: "category",
          label: "Workspaces",
          items: ["manage-workspaces", "workspace-api-tokens"],
        },
        {
          type: "category",
          label: "Clusters",
          items: [
            "create-dedicated-cluster",
            "resource-reference-hosted",
          ],
        },
        {
          type: "category",
          label: "Astro Hybrid",
          items: [
            "hybrid-overview",
            {
              type: "category",
              label: "Install Astro Hybrid",
              link: {
                type: 'generated-index',
                title: 'Install Astro Hybrid',
                description: 'Install Astro Hybrid on your cloud.'
              },
              items: ["install-aws-hybrid", "install-azure-hybrid", "install-gcp-hybrid"],
            },
            "manage-hybrid-clusters",
            {
              type: "category",
              label: "Hybrid cluster settings reference",
              link: {
                type: "generated-index",
                title: "Astro Hybrid cluster settings reference",
                description:
                  "Manage your existing AWS, Azure, or GCP cluster resource settings on Astro. Unless otherwise specified, new clusters on Astro are created with a set of default resources that should be suitable for standard use cases.",
              },
              items: [
                "resource-reference-aws-hybrid",
                "resource-reference-azure-hybrid",
                "resource-reference-gcp-hybrid",
              ],
            },
          ],
        },
        "manage-billing",
      ],
    },
    {
      type: "category",
      label: "Release notes",
      items: [
        "release-notes",
        "runtime-release-notes",
        {
          type: 'link',
          label: 'Astro CLI',
          href: 'https://docs.astronomer.io/astro/cli/release-notes',
        },
        "release-notes-subscribe",
      ],
    },
    {
      type: "category",
      label: "Reference",
      items: [
        "astro-support",
        {
          type: "category",
          label: "Astro Runtime",
          items: [
            "runtime-image-architecture",
            "runtime-version-lifecycle-policy",
          ],
        },
        'platform-variables',
        "audit-logs-reference",
        "feature-previews",
        {
          type: "category",
          label: "Security",
          link: { type: "doc", id: "security" },
          items: [
            "shared-responsibility-model",
            "resilience",
            "disaster-recovery",
            "data-protection",
            "gdpr-compliance",
            "hipaa-compliance",
            "secrets-management",
          ],
        },
        "astro-glossary"
      ],
    },
  ],
  cli: [
    {
      type: "doc",
      label: "CLI overview",
      id: "cli/overview",
    },
    {
      type: "doc",
      label: "Install the CLI",
      id: "cli/install-cli",
    },
    {
      type: "doc",
      label: "Get started with the CLI",
      id: "cli/get-started-cli",
    },
    {
      type: "doc",
      label: "Configure the CLI",
      id: "cli/configure-cli",
    },
    {
      type: "doc",
      label: "Test your Astro project locally",
      id: "cli/test-your-astro-project-locally",
    },
    {
      type: "doc",
      label: "Authenticate to cloud services",
      id: "cli/authenticate-to-clouds",
    },
    {
      type: "doc",
      label: "Release notes",
      id: "cli/release-notes",
    },
    {
      type: 'category',
      label: 'Command reference',
      link: { type: 'doc', id: 'cli/reference' },
      items: [
        'cli/astro-completion',
        {
          type: "category",
          label: "astro config",
          items: [
            'cli/astro-config-get',
            'cli/astro-config-set',
          ],
        },
        {
          type: "category",
          label: "astro context",
          items: [
            'cli/astro-context-delete',
            'cli/astro-context-list',
            'cli/astro-context-switch',
          ],
        },
        'cli/astro-deploy',
        {
          type: "category",
          label: "astro deployment",
          items: [
            'cli/astro-deployment-airflow-upgrade',
            {
              type: "category",
              label: "astro deployment airflow-variable",
              items: [
                'cli/astro-deployment-airflow-variable-copy',
                'cli/astro-deployment-airflow-variable-create',
                'cli/astro-deployment-airflow-variable-list',
                'cli/astro-deployment-airflow-variable-update',
              ],
            },
            {
              type: "category",
              label: "astro deployment connection",
              items: [
                'cli/astro-deployment-connection-copy',
                'cli/astro-deployment-connection-create',
                'cli/astro-deployment-connection-list',
                'cli/astro-deployment-connection-update',
              ],
            },
            'cli/astro-deployment-create',
            'cli/astro-deployment-delete',
            'cli/astro-deployment-inspect',
            'cli/astro-deployment-list',
            'cli/astro-deployment-logs',
            {
              type: "category",
              label: "astro deployment pool",
              items: [
                'cli/astro-deployment-pool-copy',
                'cli/astro-deployment-pool-create',
                'cli/astro-deployment-pool-list',
                'cli/astro-deployment-pool-update',
              ],
            },
            'cli/astro-deployment-runtime-upgrade',
            'cli/astro-deployment-service-account',
            'cli/astro-deployment-team',
            'cli/astro-deployment-update',
            'cli/astro-deployment-user',
            'cli/astro-deployment-variable-create',
            'cli/astro-deployment-variable-list',
            'cli/astro-deployment-variable-update',
          ],
        },
        {
          type: "category",
          label: "astro dev",
          items: [
            'cli/astro-dev-bash',
            'cli/astro-dev-init',
            'cli/astro-dev-kill',
            'cli/astro-dev-logs',
            'cli/astro-dev-object-export',
            'cli/astro-dev-object-import',
            'cli/astro-dev-parse',
            'cli/astro-dev-ps',
            'cli/astro-dev-pytest',
            'cli/astro-dev-run',
            'cli/astro-dev-start',
            'cli/astro-dev-stop',
            'cli/astro-dev-restart',
            'cli/astro-dev-upgrade-test',
          ],
        },
        'cli/astro-login',
        'cli/astro-logout',
        {
          type: "category",
          label: "astro organization",
          items: [
            "cli/astro-organization-list",
            "cli/astro-organization-switch",
            "cli/astro-organization-team-create",
            "cli/astro-organization-team-delete",
            "cli/astro-organization-team-list",
            "cli/astro-organization-team-update",
            "cli/astro-organization-team-user",
            "cli/astro-organization-token-create",
            "cli/astro-organization-token-delete",
            "cli/astro-organization-token-list",
            "cli/astro-organization-token-roles",
            "cli/astro-organization-token-rotate",
            "cli/astro-organization-token-update",
            "cli/astro-organization-user-invite",
            "cli/astro-organization-user-list",
            "cli/astro-organization-user-update",
            
          ],
        },
        {
          type: "category",
          label: "astro registry",
          items: [
            "cli/astro-registry-dag-add",
            "cli/astro-registry-provider-add"
          ],
        },
        'cli/astro-run',
        'cli/astro-team',
        'cli/astro-user-create',
        'cli/astro-version',
        {
          type: "category",
          label: "astro workspace",
          items: [
            "cli/astro-workspace-create",
            "cli/astro-workspace-delete",
            "cli/astro-workspace-list",
            "cli/astro-workspace-service-account",
            "cli/astro-workspace-switch",
            "cli/astro-workspace-team",
            "cli/astro-workspace-update",
            "cli/astro-workspace-user-add",
            "cli/astro-workspace-user-list",
            "cli/astro-workspace-user-remove",
            "cli/astro-workspace-user-update",
            "cli/astro-workspace-team-add",
            "cli/astro-workspace-team-list",
            "cli/astro-workspace-team-remove",
            "cli/astro-workspace-token-add",
            "cli/astro-workspace-token-create",
            "cli/astro-workspace-token-list",
            "cli/astro-workspace-token-rotate",
            "cli/astro-workspace-token-update",
          ],
        },
      ],
    },
  ],
};
