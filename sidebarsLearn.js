module.exports = {
  learn: [
    'overview',
    {
      type: 'category',
      label: 'Get started',
      link: {
        type: 'generated-index',
        title: 'Get started',
        description: 'Get started with Airflow.',
      },
      items: [
        'airflow-quickstart',
        {
          type: 'category',
          label: 'Tutorials',
          link: {
            type: 'doc',
            id: 'get-started-with-airflow',
          },
          items: [
            'get-started-with-airflow',
            'get-started-with-airflow-part-2',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Airflow concepts',
      link: {
        type: 'generated-index',
        title: 'Airflow concepts',
        description: 'Learn about the fundamentals of Apache Airflow.'
      },
      items: [
        {
          type: 'category',
          label: 'Basics',
          link: {
            type: 'generated-index',
            title: 'Basics',
            description: 'Learn about the fundamentals of running Apache Airflow.',
          },
          items: [
            'bashoperator',
            'connections',
            'dags',
            'what-is-a-hook',
            'intro-to-airflow',
            'managing-airflow-code',
            'airflow-openlineage',
            'what-is-an-operator',
            'airflow-sql',
            'scheduling-in-airflow',
            'what-is-a-sensor',
            'managing-dependencies',
            'airflow-ui',
            'airflow-variables',
          ],
        },
        {
          type: 'category',
          label: 'DAGs',
          link: {
            type: 'generated-index',
            title: 'DAGs',
            description: 'Learn about how to construct and manage data pipelines to be reliable and performant.',
          },
          items: [
            'astro-python-sdk-etl',
            'airflow-branch-operator',
            'airflow-context',
            'cross-dag-dependencies',
            'airflow-importing-custom-hooks-operators',
            'error-notifications-in-airflow',
            'dag-best-practices',
            'debugging-dags',
            'dynamic-tasks',
            'templating',
            'airflow-params',
            'airflow-passing-data-between-tasks',
            'rerunning-dags',
            'subdags',
            'airflow-decorators',
            'task-groups',
          ],
        },
        {
          type: 'category',
          label: 'Infrastructure',
          link: {
            type: 'generated-index',
            title: 'Infrastructure',
            description: 'Learn how to tune your infrastructure to make the most of Airflow.',
          },
          items: [
            'airflow-components',
            'airflow-executors-explained',
            'airflow-database',
            'airflow-scaling-workers',
          ],
        },
        {
          type: 'category',
          label: 'Advanced',
          link: {
            type: 'generated-index',
            title: 'Management',
            description: 'Learn how to reliably run Airflow at scale.',
          },
          items: [
            'logging',
            'data-quality',
            'airflow-datasets',
            'deferrable-operators',
            'dynamically-generating-dags',
            'kubepod-operator',
            'using-airflow-plugins',
            'airflow-pools',
            'airflow-sql-data-quality',
            'testing-airflow',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Airflow tutorials',
      link: {
        type: 'generated-index',
        title: 'Airflow tutorials',
        description: 'Step-by-step guides for writing DAGs and running Airflow.'
      },
      items: [
        'cloud-ide-tutorial',
        'operator-extra-link-tutorial',
        'xcom-backend-tutorial',
        'astro-python-sdk',
        'external-python-operator',
        'custom-airflow-ui-docs-tutorial',
      ],
    },
    {
      type: 'category',
      label: 'Integrations',
      link: {
        type: 'generated-index',
        title: 'Integrations',
        description: 'Integrate Airflow with commonly used data engineering tools.',
      },
      items: [
        'airflow-redshift',
        'airflow-sagemaker',
        'airflow-kafka',
        'airflow-azure-container-instances',
        'airflow-azure-data-explorer',
        'airflow-azure-data-factory-integration',
        'airflow-databricks',
        'airflow-dbt-cloud',
        'airflow-dbt',
        'airflow-fivetran',
        'airflow-great-expectations',
        'execute-notebooks',
        'marquez',
        'airflow-mongodb',
        'airflow-snowflake',
        'soda-data-quality',
        'airflow-talend-integration',
        'airflow-weights-and-biases',
      ],
    },
    {
      type: 'category',
      label: 'Examples',
      link: {
        type: 'generated-index',
        title: 'Examples',
        description: 'See examples of use cases and more with Apache Airflow.'
      },
      items: [
          'pycharm-local-dev',
          'vscode-local-dev',
          {
            type: 'category',
            label: 'Use cases',
            items: [
              'use-case-airflow-dbt',
            ],
          },
      ],
    },
  ],
};
