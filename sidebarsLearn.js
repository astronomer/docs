module.exports = {
  learn: [
    'overview',
    {
      type: 'category',
      label: 'Get started',
      link: {
        type: 'generated-index',
        title: 'Get started',
        description: 'Get started with Apache Airflow.',
      },
      items: [
        'intro-to-airflow',
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
            'airflow-datasets',
            'what-is-a-hook',
            'managing-airflow-code',
            'airflow-openlineage',
            'what-is-an-operator',
            'airflow-sql',
            'scheduling-in-airflow',
            'what-is-a-sensor',
            'managing-dependencies',
            'airflow-ui',
            'airflow-trigger-rules',
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
            'airflow-dag-parameters',
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
            'custom-xcom-backend-strategies',
            'data-quality',
            'deferrable-operators',
            'dynamically-generating-dags',
            'airflow-isolated-environments',
            'kubepod-operator',
            'airflow-mlops',
            'using-airflow-plugins',
            'airflow-pools',
            'airflow-setup-teardown',
            'sharing-code-multiple-projects',
            'testing-airflow'
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
        'airflow-listeners',
        'operator-extra-link-tutorial',
        'cleanup-dag-tutorial',
        'xcom-backend-tutorial',
        'pycharm-local-dev',
        'vscode-local-dev',
        "dag-factory",
        'example-ms-teams-callback',
        'cloud-ide-tutorial',
        'airflow-object-storage-tutorial',
        'airflow-sql-data-quality',
        'astro-python-sdk',
        'custom-airflow-ui-docs-tutorial',
      ],
    },
    {
      type: 'category',
      label: 'Integrations & connections',
      link: {
        type: 'generated-index',
        title: 'Integrations & connections',
        description: 'Integrate Airflow with commonly used data engineering tools.',
      },
      items: [
        'airflow-sagemaker',
        'airflow-kafka',
        'connections/azure-blob-storage',
        'airflow-azure-container-instances',
        {
          type: 'category',
          label: 'Azure Data Factory',
          link: {
              type: 'generated-index',
              title: 'Azure Data Factory',
              description: 'Integrate Airflow with Azure Data Factory',
              image: '/img/integrations/azure-data-factory.png'
          },
          items: [
            'connections/azure-data-factory',
            'airflow-azure-data-factory-integration',
          ],
        },
        'connections/entra-workload-identity',
        'connections/bigquery',
        'airflow-cohere',
        {
          type: 'category',
          label: 'Databricks',
          link: {
              type: 'generated-index',
              title: 'Databricks',
              description: 'Integrate Airflow with Databricks',
              image: '/img/integrations/databricks.png'
          },
          items: [
            'connections/databricks',
            'airflow-databricks',
          ],
        },
        {
          type: 'category',
          label: 'dbt Cloud',
          link: {
              type: 'generated-index',
              title: 'dbt Cloud',
              description: 'Integrate Airflow with dbt Cloud',
              image: '/img/integrations/dbt.png'
          },
          items: [
            'connections/dbt-cloud',
            'airflow-dbt-cloud',
          ],
        },
        'airflow-dbt',
        'airflow-duckdb',
        'airflow-fivetran',
        'airflow-great-expectations',
        'execute-notebooks',
        'marquez',
        'airflow-mlflow',
        'airflow-mongodb',
        'connections/ms-sqlserver',
        'airflow-openai',
        'airflow-opensearch',
        'airflow-pgvector',
        'airflow-pinecone',
        'connections/postgres',
        'airflow-qdrant',
        {
          type: 'category',
          label: 'Redshift',
          link: {
              type: 'generated-index',
              title: 'Redshift',
              description: 'Orchestrate Redshift queries from your Airflow DAGs.',
              image: '/img/integrations/redshift.png'
          },
          items: [
            'connections/redshift',
            'airflow-redshift',
          ],
        },
        {
          type: 'category',
          label: 'Snowflake',
          link: {
              type: 'generated-index',
              title: 'Snowflake',
              description: 'Orchestrate Snowflake queries from your Airflow DAGs.',
              image: '/img/integrations/snowflake.png'
          },
          items: [
            'connections/snowflake',
            'airflow-snowflake',
            'airflow-snowpark',
          ],
        },
        'soda-data-quality',
        'airflow-weaviate',
        'airflow-weights-and-biases',
      ],
    },
    {
      type: 'category',
      label: 'Use cases',
      link: {
        type: 'generated-index',
        title: 'Use cases',
        description: 'Example use cases and implementations with Apache Airflow.'
      },
      items: [
          'use-case-setup-teardown-data-quality',
          'use-case-airflow-databricks',
          'use-case-airflow-dbt',
          'use-case-elt-ml-finance',
          'use-case-airflow-llm-rag-finance',
          'use-case-llm-customer-feedback',
          'use-case-airflow-ml-datasets',
          'use-case-airflow-mlflow',
      ],
    },
    'airflow-glossary'
  ],
};
