module.exports = {
  learn: [
    'overview',
    {
      type: 'category',
      label: 'Airflow concepts',
      link: {
        type:'generated-index',
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
            'intro-to-airflow',
            'dags',
            'what-is-an-operator',
            'airflow-ui',
            'scheduling-in-airflow',
            'what-is-a-sensor',
            'connections',
            'what-is-a-hook',
            'bashoperator',
            'airflow-sql',
            'managing-dependencies',
            'managing-airflow-code',
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
            'dag-best-practices',
            'airflow-passing-data-between-tasks',
            'airflow-branch-operator',
            'airflow-importing-custom-hooks-operators',
            'astro-python-sdk-etl',
            'debugging-dags',
            'task-groups',
            'rerunning-dags',
            'templating',
            'cross-dag-dependencies',
            'error-notifications-in-airflow',
            'subdags',
            'airflow-decorators',
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
            'airflow-database',
            'using-airflow-plugins',
            'airflow-scaling-workers',
            'airflow-executors-explained',
            'airflow-pools',
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
            'testing-airflow',
            'custom-xcom-backends',
            'logging',
            'kubepod-operator',
            'data-quality',
            'airflow-sql-data-quality',
            'dynamically-generating-dags',
            'dynamic-tasks',
            'airflow-datasets',
            'deferrable-operators',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Tutorials',
      link: {
        type:'generated-index',
        title: 'Tutorials',
        description: 'Step-by-step guides for writing DAGs and running Airflow.'
      },
      items: [
        {
          type: 'category',
          label: 'Get started with Airflow',
          link: {
                type: 'doc',
                id: 'get-started-with-airflow',
           },
          items: [
            'get-started-with-airflow',
            'get-started-with-airflow-part-2',
          ],
        },
        'astro-python-sdk',
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
        'airflow-azure-data-factory-integration',
        'airflow-azure-data-explorer',
        'airflow-azure-container-instances',
        'airflow-openlineage',
        'airflow-dbt',
        'airflow-databricks',
        'airflow-sagemaker',
        'airflow-snowflake',
        'airflow-redshift',
        'airflow-great-expectations',
        'airflow-talend-integration',
        'execute-notebooks',
        'soda-data-quality',
     ],
    },
  ],
};
