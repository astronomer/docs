---
sidebar_label: 'Integrate lineage'
title: "Integrate data lineage from external systems to Astro"
id: set-up-data-lineage
description: Configure your external systems to emit OpenLineage data to Astro with Apache Airflow.
toc_min_heading_level: 2
toc_max_heading_level: 2
---

[Data lineage](https://en.wikipedia.org/wiki/Data_lineage) is the concept of tracking data from its origin to wherever it is consumed downstream as it flows through a data pipeline. This includes connections between datasets and tables in a database as well as rich metadata about the tasks that create and transform data. You can observe data lineage to:

- Trace the history of a dataset.
- Troubleshoot run failures.
- Manage personally identifiable information (PII).
- Ensure compliance with data regulations.

This guide provides information about how lineage data is automatically extracted from Apache Airflow tasks on Astro and how to integrate external systems, including Databricks and dbt, that require additional configuration. To learn about how to view data lineage on Astro, see [View data lineage](data-lineage.md).

## Data lineage on Astro

To view lineage data, it first needs to be extracted from an external application and then stored in a lineage backend. Astro uses the [OpenLineage Airflow library](https://openlineage.io/integration/apache-airflow/) (`openlineage-airflow`) to extract lineage from Airflow tasks and stores that data in the Astro control plane. The latest version of the OpenLineage Airflow library is installed on [Astro Runtime](runtime-image-architecture.md) by default.

There are two ways to emit lineage data to Astro:

- Run a task on Astro with a supported Airflow operator, such as the SnowflakeOperator. These operators include extractors that automatically emit lineage data and don’t require additional configuration. See [Supported Airflow operators](data-lineage-support-and-compatibility.md#supported-airflow-operators).
- Integrate OpenLineage with an external service, such as dbt or Apache Spark, to emit data lineage outside of an Airflow DAG or task using an OpenLineage API key.

The data lineage graph in the Cloud UI shows lineage data that is emitted with both methods, including jobs that are not run on the Astro data plane. This graph can provide context to your data before, during, and after it reaches your Deployment.

## Extract lineage data from external systems to Astro

To emit lineage data from an Airflow task that runs outside of Astro or from an external system that does not interact with Airflow:

- Retrieve your Organization OpenLineage API key from the Cloud UI. See [Retrieve an OpenLineage API key](#retrieve-an-openlineage-api-key).
- Specify your OpenLineage API key in the external system. See the following integration guides for specific instructions.

### Retrieve an OpenLineage API key

1. In the Cloud UI, click **Settings**.
2. Copy the value in the **Lineage API Key** field.
3. Specify your Organization's OpenLineage API key in the external system's configuration.

## Snowflake and OpenLineage with Airflow

Lineage data emitted from [Snowflake](https://www.snowflake.com/en/) is similar to what is collected from other SQL databases, including Amazon Redshift and Google BigQuery. However, Snowflake is unique in that it emits [query tags](https://docs.snowflake.com/en/user-guide/object-tagging.html#what-is-a-tag) that provide additional task execution details.

When you run a task in Airflow that interacts with Snowflake, the query tag allows each task to be directly matched with the Snowflake query or queries that are run by that task. If the task fails, for example, you can look up the Snowflake query that was executed by that task and reduce the time required to troubleshoot the task failure.

To emit lineage data from Snowflake:

1. Add a Snowflake connection to Airflow. See [Snowflake connection](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/connections/snowflake.html).
2. Run an Airflow DAG or task with the [`SnowflakeOperator`](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator) or `SnowflakeOperatorAsync`. This operator is officially supported by OpenLineage and does not require additional configuration. If you don't run Airflow on Astro, see [Extract lineage data from external systems to Astro](#extract-lineage-data-from-external-systems-to-Astro).

### Data collected

When you run an Airflow task with the `SnowflakeOperator`, the following data is collected:

- Task duration
- SQL queries. Only CREATE statements are currently supported
- Query duration. This is different from the Airflow task duration
- Input datasets
- Output datasets
- Quality metrics based on dataset and column-level checks, including successes and failures per run

To view this data in the Cloud UI, click **Lineage**, select a SnowflakeOperator task, and then click the dataset. See [View data lineage](data-lineage.md#view-metrics-for-a-specific-run-or-dataset).

:::tip

Airflow tasks run with the `SnowflakeOperator` emit SQL source code that you can view in the Cloud UI. See [View SQL source code](#view-SQL-source-code).

:::

## OpenLineage and Databricks with Airflow

Use the information provided here to set up lineage collection for Spark running on a Databricks cluster.

#### Prerequisites

- A [Databricks cluster](https://docs.databricks.com/clusters/create-cluster.html).

### Setup

1. In your Databricks File System [(DBFS)](https://docs.databricks.com/data/databricks-file-system.html), create a new directory at `dbfs:/databricks/openlineage/`.
2. Download the latest OpenLineage `jar` file to the new directory. See [Maven Central Repository](https://search.maven.org/artifact/io.openlineage/openlineage-spark).
3. Download the `open-lineage-init-script.sh` file to the new directory. See [OpenLineage GitHub](https://github.com/OpenLineage/OpenLineage/blob/main/integration/spark/databricks/open-lineage-init-script.sh).
4. In Databricks, run this command to create a [cluster-scoped init script](https://docs.databricks.com/clusters/init-scripts.html#example-cluster-scoped-init-script) and install the `openlineage-spark` library at cluster initialization:

    ```sh
    dbfs:/databricks/openlineage/open-lineage-init-script.sh
    ```

5. In the cluster configuration page for your Databricks cluster, specify the following [Spark configuration](https://docs.databricks.com/clusters/configure.html#spark-configuration):

   ```sh
      bash
   spark.driver.extraJavaOptions -Djava.security.properties=
   spark.executor.extraJavaOptions -Djava.security.properties=
   spark.openlineage.url https://<your-astro-base-domain>
   spark.openlineage.apiKey <your-lineage-api-key>
   spark.openlineage.namespace <NAMESPACE_NAME> // Astronomer recommends using a meaningful namespace like `spark-dev`or `spark-prod`.
   ```

> **Note:** You override the JVM security properties for the spark _driver_ and _executor_ with an _empty_ string as some TLS algorithms are disabled by default. For a more information, see [this](https://docs.microsoft.com/en-us/answers/questions/170730/handshake-fails-trying-to-connect-from-azure-datab.html) discussion.

After you save this configuration, lineage is enabled for all Spark jobs running on your cluster.

### Verify Setup

To test that lineage was configured correctly on your Databricks cluster, run a test Spark job on Databricks. After your job runs, click **Lineage** in the Cloud UI and then click **Runs** in the left menu. If your configuration is successful, your Spark job appears in the table of most recent runs. Click a job run to see it within a lineage graph.

## OpenLineage and dbt Core with Airflow

Use the information provided here to set up lineage collection for dbt Core tasks. To learn how to create and productionize dbt tasks in Airflow, and how to automatically create dbt Core tasks based on a manifest, see [Orchestrate dbt with Airflow](https://docs.astronomer.io/learn/airflow-dbt).

If your organization wants to orchestrate dbt Cloud jobs with Airflow, contact [Astronomer support](https://cloud.astronomer.io/support). 

### Prerequisites

- A [dbt project](https://docs.getdbt.com/docs/building-a-dbt-project/projects).
- The [dbt CLI](https://docs.getdbt.com/dbt-cli/cli-overview) v0.20+.

### Setup

1. Add the following line to the `requirements.txt` file of your Astro project:

   ```text
    openlineage-dbt
    ```

2. Run the following command to generate the [`catalog.json`](https://docs.getdbt.com/reference/artifacts/catalog-json) file for your dbt project:

   ```bash
   $ dbt docs generate
   ```

3. In your dbt project, run the [OpenLineage](https://openlineage.io/integration/dbt/) wrapper script using the `dbt run` [command](https://docs.getdbt.com/reference/commands/run):

   ```bash
   $ dbt-ol run
   ```

4. Optional. Run the following command to test your set up:

   ```bash
   $ dbt-ol test
   ```

### Verify setup

To confirm that your setup is successful, run a dbt model in your project. After you run this model, click **Lineage** in the Cloud UI and then click **Runs** in the left menu. If the setup is successful, the run that you triggered appears in the table of most recent runs.

## OpenLineage and Great Expectations with Airflow

Use the information provided here to set up lineage collection for a running Great Expectations suite.

This guide outlines how to set up lineage collection for a Great Expectations project.

#### Prerequisites

- A [Great Expectations project](https://legacy.docs.greatexpectations.io/en/latest/guides/tutorials/getting_started.html#tutorials-getting-started).
- Your Astro base domain.
- Your Organization's OpenLineage API key.

#### Setup

If you use the `GreatExpectationsOperator` version 0.2.0 or later and don't use a custom Checkpoint or Checkpoint Config, the operator detects your Astro OpenLineage configuration and sends lineage information automatically. If you use custom Checkpoints, complete the following steps:

1. Update your `great_expectations.yml` file to add `OpenLineageValidationAction` to your `action_list_operator` configuration:

    ```yml
    validation_operators:
      action_list_operator:
        class_name: ActionListValidationOperator
        action_list:
          - name: openlineage
            action:
              class_name: OpenLineageValidationAction
              module_name: openlineage.common.provider.great_expectations
              openlineage_host: https://<your-astro-base-domain>
              openlineage_apiKey: <your-lineage-api-key>
              openlineage_namespace: <NAMESPACE_NAME> # Replace with your job namespace; Astronomer recommends using a meaningful namespace such as `dev` or `prod`.
              job_name: validate_my_dataset
    ```

2. Lineage support for GreatExpectations requires the use of the `ActionListValidationOperator`. In each of your checkpoint's xml files in `checkpoints/`, set the `validation_operator_name` configuration to `action_list_operator`:

    ```xml
    name: check_users
    config_version:
    module_name: great_expectations.checkpoint
    class_name: LegacyCheckpoint
    validation_operator_name: action_list_operator
    batches:
      - batch_kwargs:
    ```

### Verify

To confirm that your setup is successful, click **Lineage** in the Cloud UI and then click **Issues** in the left menu. Recent data quality assertion issues appear in the **All Issues** table.

If your code hasn't produced any data quality assertion issues, use the search bar to search for a dataset and view its node on the lineage graph for a recent job run. Click **Quality** to view metrics and assertion pass or fail counts.

## OpenLineage and Spark

Use the information provided here to set up lineage collection for Spark.

### Prerequisites

- A Spark application.
- A Spark job.
- Your Astro base domain.
- Your Organization's OpenLineage API key.

### Setup

In your Spark application, set the following properties to configure your lineage endpoint, install the [`openlineage-spark`](https://search.maven.org/artifact/io.openlineage/openlineage-spark) library, and configure an _OpenLineageSparkListener_:

   ```python
   SparkSession.builder \
     .config('spark.jars.packages', 'io.openlineage:openlineage-spark:0.2.+')
     .config('spark.extraListeners', 'io.openlineage.spark.agent.OpenLineageSparkListener')
     .config('spark.openlineage.host', 'https://astro-<your-astro-base-domain>.datakin.com')
     .config('spark.openlineage.apiKey', '<your-openlineage-api-key>')
     .config('spark.openlineage.namespace', '<namespace-name>') # Replace with the name of your Spark cluster.
     .getOrCreate()                                             # Astronomer recommends using a meaningful namespace such as `spark-dev` or `spark-prod`.
   ```

### Verify

To confirm that your setup is successful, run a Spark job after you save your configuration. After you run this model, click **Lineage** in the Cloud UI and then click **Runs** in the left menu. Your recent Spark job run appears in the table of most recent runs.

## View SQL source code

The SQL source code view for [supported Airflow operators](data-lineage-support-and-compatibility.md#supported-airflow-operators) in the Cloud UI  **Lineage** page is off by default for all Workspace users. To enable the source code view, set the following [environment variable](environment-variables.md) for each Astro Deployment:

- Key: `OPENLINEAGE_AIRFLOW_DISABLE_SOURCE_CODE`
- Value: `False`

Astronomer recommends enabling this feature only for Deployments with non-sensitive code. For more information about Workspace permissions, see [Workspace roles](user-permissions.md#workspace-roles).
