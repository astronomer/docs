module.exports = {
  learn: [
    'overview',
    {
      type: 'category',
      label: 'Concepts',
      link: {
        type:'generated-index',
        title: 'Concepts',
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
            'what-is-a-sensor',
            'connections',
            'what-is-a-hook',
            'airflow-decorators',
            'bashoperator',
            'airflow-sql',
            'airflow-ui',
            'scheduling-in-airflow',
          ],
        },
        {
          type: 'category',
          label: 'Pipelines',
          link: {
            type: 'generated-index',
            title: 'Pipelines',
            description: 'Learn about how to construct and manage data pipelines to be reliable and performant.',
          },
          items: [
            'dag-best-practices',
            'airflow-passing-data-between-tasks',
            'airflow-branch-operator',
            'airflow-importing-custom-hooks-operators',
            'debugging-dags',
            'subdags',
            'task-groups',
            'execute-notebooks',
            'rerunning-dags',
            'managing-dependencies',
            'managing-airflow-code',
            'templating',
            'cross-dag-dependencies',
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
            'deferrable-operators',
            'airflow-database',
            'using-airflow-plugins',
            'airflow-scaling-workers',
            'airflow-executors-explained',
            'airflow-pools',
          ],
        },
        {
          type: 'category',
          label: 'Management',
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
          label: 'Get started with Apache Airflow',
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
            'airflow-openlineage',
            'airflow-dbt',
            'airflow-databricks',
            'airflow-sagemaker',
            'airflow-snowflake',
            'airflow-redshift',
            'airflow-great-expectations',
            'airflow-talend-integration',
            'soda-data-quality',
         ],
        },
      ],
    },
  ],
};
