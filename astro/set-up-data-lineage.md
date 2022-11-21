---
sidebar_label: 'Integrate OpenLineage'
title: "Integrate OpenLineage with external systems"
id: set-up-data-lineage
description: Configure your external systems to emit OpenLineage data to Astro.
toc_min_heading_level: 2
toc_max_heading_level: 2
---

To generate lineage graphs for your data pipelines, you first need to configure your data pipelines to emit lineage data. Because lineage data can be generated in all stages of your pipeline, you can configure pipeline components outside of Astro, such as dbt or Databricks, to emit lineage data whenever they're running a job. Coupled with lineage data emitted from your DAGs, Astro generates a lineage graph that can provide context to your data before, during, and after it reaches your Deployment.

Configuring a system to send lineage data requires:

- Installing an OpenLineage backend to emit lineage data from the system.
- Specifying your Organization's OpenLineage API endpoint to send lineage data to the Astro control plane.

## Retrieve an OpenLineage API key

To send lineage data from an external system to Astro, you must specify your Organization's OpenLineage API key in the external system's configuration.

1. In the Cloud UI, open the **Settings** tab.
2. Copy the value in **Lineage API Key**.
3. Configure the API key in an external system. see one of the following integration guides for your system.

## OpenLineage and Databricks

Use the information provided here to set up lineage collection for Spark running on a Databricks cluster.

### Prerequisites

- A Databricks cluster.

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

To test that lineage was configured correctly on your Databricks cluster, run a test Spark job on Databricks. After your job runs, open the **Lineage** tab in the Cloud UI and go to the **Rims** page. If your configuration is successful, you'll see your Spark job appear in the table of most recent runs. Click a job run to see it within a lineage graph.

## OpenLineage and dbt

Use the information provided here to set up lineage collection for a dbt project.

### Prerequisites

- A [dbt project](https://docs.getdbt.com/docs/building-a-dbt-project/projects).
- The [dbt CLI](https://docs.getdbt.com/dbt-cli/cli-overview) v0.20+.
- Your Astro base domain.
- Your Organization's OpenLineage API key.

### Setup

1. On your local machine, run the following command to install the [`openlineage-dbt`](https://pypi.org/project/openlineage-dbt) library:

   ```sh
   $ pip install openlineage-dbt
   ```

2. Configure the following environment variables in your shell:

   ```bash
   OPENLINEAGE_URL=https://<your-astro-base-domain>
   OPENLINEAGE_API_KEY=<your-lineage-api-key>
   OPENLINEAGE_NAMESPACE=<NAMESPACE_NAME> # Replace with the name of your dbt project.
                                          # Astronomer recommends using a meaningful namespace such as `dbt-dev` or `dbt-prod`.
   ```

3. Run the following command to generate the [`catalog.json`](https://docs.getdbt.com/reference/artifacts/catalog-json) file for your dbt project:

   ```bash
   $ dbt docs generate
   ```

4. In your dbt project, run the [OpenLineage](https://openlineage.io/integration/dbt/) wrapper script using the `dbt run` [command](https://docs.getdbt.com/reference/commands/run):

   ```bash
   $ dbt-ol run
   ```

### Verify Setup

To confirm that your setup is successful, run a dbt model in your project. After you run this model, open the **Lineage** tab in the Cloud UI and go to the **Runs** page. If the setup is successful, the run that you triggered appears in the table of most recent runs.

## OpenLineage and Great Expectations

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

To confirm that your setup is successful, open the **Lineage** tab in the Cloud UI and go to the **Issues** page. Recent data quality assertion issues appear in the **All Issues** table.

If your code hasn't produced any data quality assertion issues, use the search bar to search for a dataset and view its node on the lineage graph for a recent job run. Click the **Quality** tab to view metrics and assertion pass or fail counts.

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
     .config('spark.openlineage.host', 'https://<your-astro-base-domain>')
     .config('spark.openlineage.apiKey', '<your-lineage-api-key>')
     .config('spark.openlineage.namespace', '<NAMESPACE_NAME>') # Replace with the name of your Spark cluster.
     .getOrCreate()                                             # Astronomer recommends using a meaningful namespace such as `spark-dev` or `spark-prod`.
   ```

### Verify

To confirm that your setup is successful, run a Spark job after you save your configuration. After you run this model, open the **Lineage** tab in the Cloud UI and go to the **Runs** page. Your recent Spark job run appears in the table of most recent runs.

## OpenLineage and Snowflake 

Use the information provided here to set up lineage collection for Snowflake.

### Setup

Like other [supported Airflow operators](data-lineage-support-and-compatibility.md#supported-airflow-operators), the [SnowflakeOperator](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator) has full data lineage support and capabilities by default. As long as you connect to Snowflake through an Airflow connection, any task using the SnowflakeOperator emits lineage data about the Snowflake tables it queries.

### Verify 

After you run a DAG with the SnowflakeOperator, open the **Lineage** tab in the Cloud UI and go to the **Graph** page. The task using the SnowflakeOperator should appear as a run connected to a dataset. Click the dataset to view:

- The time that Snowflake was accessed.
- Tables that were accessed by upstream or downstream tasks.
- The name and description for each column in the dataset.
- Data quality checks for the accessed tables. Data quality checks require integrating Great Expectations with OpenLineage and Airflow. See [Integrate with Great Expectations](#integrate-with-great-expectations) and [Orchestrate Great Expectations with Airflow](https://docs.astronomer.io/learn/airflow-great-expectations#docusaurus_skipToContent_fallback).

## Make source code visible for Airflow operators

Because Workspace permissions are not yet applied to the **Lineage** tab, viewing source code for [supported Airflow operators](data-lineage-support-and-compatibility.md#supported-airflow-operators) is off by default. If you want users across Workspaces to be able to view source code for Airflow tasks in a given Deployment, create an [environment variable](environment-variables.md) in the Deployment with a key of `OPENLINEAGE_AIRFLOW_DISABLE_SOURCE_CODE` and a value of `False`. Astronomer recommends enabling this feature only for Deployments with non-sensitive code and workflows.
