---
sidebar_label: 'Integrate lineage'
title: "Send lineage metadata to Astro"
id: set-up-data-lineage
description: Configure Airflow and external systems to emit OpenLineage data to Astro with Apache Airflow.
toc_min_heading_level: 2
toc_max_heading_level: 2
---

[Data lineage](https://en.wikipedia.org/wiki/Data_lineage) is the concept of tracking data from its origin to wherever it is consumed downstream as it flows through a data pipeline. This includes connections between datasets and tables in a database as well as rich metadata about the tasks that create and transform data. You can observe data lineage to:

- Trace the history of a dataset.
- Troubleshoot run failures.
- Manage personally identifiable information (PII).
- Ensure compliance with data regulations.

This guide provides information about how lineage metadata is automatically extracted from Apache Airflow tasks on Astro and how to integrate external systems, including Databricks and dbt, that require additional configuration. To learn about how to view data lineage on Astro, see [View data lineage](data-lineage.md).

## Extract lineage metadata from Airflow operators using supported extractors

Astro uses the [OpenLineage Airflow library](https://openlineage.io/docs/integrations/airflow/) (`openlineage-airflow`) to extract lineage from Airflow tasks and stores that data in the Astro control plane. This package includes [default extractors](https://openlineage.io/docs/integrations/airflow/default-extractors) for popular Airflow operators.

The latest version of the OpenLineage Airflow library is installed on [Astro Runtime](runtime-image-architecture.md) by default, meaning that you can use all default extractors without additional configuration. If you use an Airflow operator that includes a default extractor in your DAG, the operator automatically generates lineage metadata to the **Lineage** page on Astro. 

Each operator generates different lineage metadata based on its default extractor. For more information about operators with default extractors and what lineage metadata they generate, see [OpenLineage documentation](https://openlineage.io/docs/integrations/about#capability-matrix).

## Extract lineage metadata from Airflow operators using custom extractors

If you want to extract lineage metadata from an Airflow operator that doesn't have a default extractor, you can write a custom extractor and add it to your Astro project.

To write a custom extractor, see [OpenLineage documentation](https://openlineage.io/docs/integrations/airflow/extractors/custom-extractors). To add a custom extractor to an Astro Deployment:

1. Add your custom extractor files to the `include` folder of your local Astro project.
2. Deploy your project. See [Deploy code](deploy-code.md).
3. Set the following [environment variable](environment-variables.md) in your Astro Deployment:

    ```text
    OPENLINEAGE_EXTRACTORS='<path-to-extractor-class-1>;<path-to-extractor-class-2>;<path-to-extractor-class-x>'
    ```

    Specify the path to your extractor class as relative to the base of your Astro project directory (for example, `include/myExtractorClass`). If you are importing only one custom extractor, do not include a semicolon after the file path. 

## Extract lineage metadata from Airflow operators using custom inlets and outlets

An alternative to writing a custom extractor is to specify dataset inlets and outlets directly in your task parameters. These inlets and outlets appear as dependency lines on the lineage graph for your DAG. This option is suitable if your priority is rendering an accurate lineage graph of your DAG, and you don't need to generate specific facets from your operators.

To specify inlets and outlets, see the [OpenLineage documentation](https://openlineage.io/docs/integrations/airflow/manual) and [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/lineage.html). Note that OpenLineage only supports specifying inlets and outlets using `Table` objects.

## Extract lineage metadata from external systems to Astro

To send lineage metadata from an external system to Astro, you need to configure the external system's OpenLineage integration with a Deployment namespace, your Organization's OpenLineage URL, and your organization's OpenLineage API key. This information is used to send OpenLineage data to your Astro lineage backend.

To locate your Deployment namespace in the Cloud UI, open the Deployment and copy the value in **Namespace**. To locate your Organization's OpenLineage URL and OpenLineage API key, go to `https://cloud.<your-astro-base-domain>.io/settings` and copy the values in the **Lineage API Key** and **OpenLineage URL** fields.

Use the following topics to configure these values in supported external systems and send lineage metadata from those systems to Astro.

### Snowflake and OpenLineage with Airflow

Lineage data emitted from [Snowflake](https://www.snowflake.com/en/) is similar to what is collected from other SQL databases, including Amazon Redshift and Google BigQuery. However, Snowflake is unique in that it emits [query tags](https://docs.snowflake.com/en/user-guide/object-tagging.html#what-is-a-tag) that provide additional task execution details.

When you run a task in Airflow that interacts with Snowflake, the query tag allows each task to be directly matched with the Snowflake query or queries that are run by that task. If the task fails, for example, you can look up the Snowflake query that was executed by that task and reduce the time required to troubleshoot the task failure.

To emit lineage metadata from Snowflake:

1. Add a Snowflake connection to Airflow. See [Snowflake connection](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/connections/snowflake.html).
2. Run an Airflow DAG or task with the [`SnowflakeOperator`](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator) or `SnowflakeOperatorAsync`. This operator is officially supported by OpenLineage and does not require additional configuration. If you don't run Airflow on Astro, see [Extract lineage metadata from external systems to Astro](#extract-lineage-data-from-external-systems-to-Astro).

#### Data collected

When you run an Airflow task with the `SnowflakeOperator`, the following data is collected:

- Task duration
- SQL queries. For a list of supported queries, see the [OpenLineage `tests` repository](https://github.com/OpenLineage/OpenLineage/tree/main/integration/sql/impl/tests).
- Query duration. This is different from the Airflow task duration
- Input datasets
- Output datasets
- Quality metrics based on dataset and column-level checks, including successes and failures per run

To view this data in the Cloud UI, click **Lineage**, select a SnowflakeOperator task, and then click the dataset. See [View data lineage](data-lineage.md#view-metrics-for-a-specific-run-or-dataset).

:::tip

Airflow tasks run with the `SnowflakeOperator` emit SQL source code that you can view in the Cloud UI. See [View SQL source code](#view-SQL-source-code).

:::

### OpenLineage and Databricks with Airflow

Use the information provided here to set up lineage collection for Spark running on a Databricks cluster.

#### Prerequisites

- A [Databricks cluster](https://docs.databricks.com/clusters/create-cluster.html).

#### Setup

1. In your Databricks File System [(DBFS)](https://docs.databricks.com/data/databricks-file-system.html), create a new directory at `dbfs:/databricks/openlineage/`.
2. Download the latest OpenLineage `jar` file to the new directory. See [Maven Central Repository](https://search.maven.org/artifact/io.openlineage/openlineage-spark).
3. Download the `open-lineage-init-script.sh` file to the new directory. See [OpenLineage GitHub](https://github.com/OpenLineage/OpenLineage/blob/main/integration/spark/databricks/open-lineage-init-script.sh).
4. In Databricks, run this command to create a [cluster-scoped init script](https://docs.databricks.com/clusters/init-scripts.html#example-cluster-scoped-init-script) and install the `openlineage-spark` library at cluster initialization:

    ```sh
    dbfs:/databricks/openlineage/open-lineage-init-script.sh
    ```

5. In the cluster configuration page for your Databricks cluster, specify the following [Spark configuration](https://docs.databricks.com/clusters/configure.html#spark-configuration):

   ```sh
   spark.driver.extraJavaOptions -Djava.security.properties=
   spark.executor.extraJavaOptions -Djava.security.properties=
   spark.openlineage.url https://<your-astro-base-domain>
   spark.openlineage.apiKey <your-lineage-api-key>
   spark.openlineage.namespace <NAMESPACE_NAME> // Astronomer recommends using a meaningful namespace like `spark-dev`or `spark-prod`.
   ```

> **Note:** You override the JVM security properties for the spark _driver_ and _executor_ with an _empty_ string as some TLS algorithms are disabled by default. For more information, see [this](https://docs.microsoft.com/en-us/answers/questions/170730/handshake-fails-trying-to-connect-from-azure-datab.html) discussion.

After you save this configuration, lineage is enabled for all Spark jobs running on your cluster.

#### Verify Setup

To test that lineage was configured correctly on your Databricks cluster, run a test Spark job on Databricks. After your job runs, click **Lineage** in the Cloud UI and then click **Runs** in the left menu. If your configuration is successful, your Spark job appears in the table of most recent runs. Click a job run to see it within a lineage graph.

### OpenLineage and dbt Core with Airflow

Use the information provided here to set up lineage collection for dbt Core tasks. To learn how to create and productionize dbt tasks in Airflow, and how to automatically create dbt Core tasks based on a manifest, see [Orchestrate dbt with Airflow](https://docs.astronomer.io/learn/airflow-dbt).

If your organization wants to orchestrate dbt Cloud jobs with Airflow, contact [Astronomer support](https://cloud.astronomer.io/support). 

#### Prerequisites

- A [dbt project](https://docs.getdbt.com/docs/building-a-dbt-project/projects).
- The [dbt CLI](https://docs.getdbt.com/dbt-cli/cli-overview) v0.20+.

#### Setup

1. Add the following line to the `requirements.txt` file of your Astro project:

   ```text
    openlineage-dbt
    ```

2. Run the following command to generate the [`catalog.json`](https://docs.getdbt.com/reference/artifacts/catalog-json) file for your dbt project:

   ```bash
   $ dbt docs generate
   ```

3. In your dbt project, run the [OpenLineage](https://openlineage.io/docs/integrations/dbt) wrapper script using the `dbt run` [command](https://docs.getdbt.com/reference/commands/run):

   ```bash
   $ dbt-ol run
   ```

4. Optional. Run the following command to test your set up:

   ```bash
   $ dbt-ol test
   ```

#### Verify setup

To confirm that your setup is successful, run a dbt model in your project. After you run this model, click **Lineage** in the Cloud UI and then click **Runs** in the left menu. If the setup is successful, the run that you triggered appears in the table of most recent runs.

### OpenLineage and Great Expectations with Airflow

Use the information provided here to set up lineage collection for a running Great Expectations suite.

This guide outlines how to set up lineage collection for a Great Expectations project.

#### Prerequisites

- A [Great Expectations Data Context](https://legacy.docs.greatexpectations.io/en/latest/guides/tutorials/getting_started.html#tutorials-getting-started)
- If using a Checkpoint or Checkpoint config, your Astro base domain and OpenLineage API key.

#### Setup

1. Make your Data Context accessible to your DAGs. For most use cases, Astronomer recommends adding the Data Context to your Astro project `include` folder. The GreatExpectationsOperator will access `include/great_expectations/great_expectations.yml` and use the configuration to run your Expectations. Then, add the following lines to your DAGs: 

    ```python
    # Required imports for Great Expectations
    import os
    from pathlib import Path
    from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
    # Set base path for Data Context 
    base_path = Path(__file__).parents[2]

    ...

    # Example task using GreatExpectationsOperator 
    ge_task = GreatExpectationsOperator(
      task_id="ge_task",
      # Set directory for the Data Context
      ge_root_dir=os.path.join(base_path, "include", "great_expectations"),
      ...
    )
    ```

   If you use the `GreatExpectationsOperator` version 0.2.0 or later and don't provide a Checkpoint file or Checkpoint Config, you can skip steps 2 and 3.
   
2. In each of your Checkpoint files, add `OpenLineageValidationAction` to your `action_list` like in the following example:
    
    ```yaml{10-17}
    name: my.simple.chk
    config_version: 1.0
    template_name:
    module_name: great_expectations.checkpoint
    class_name: Checkpoint
    run_name_template:
    expectation_suite_name:
    batch_request: {}
    action_list:
      - name: open_lineage
        action:
          class_name: OpenLineageValidationAction,
          module_name: openlineage.common.provider.great_expectations,
          openlineage_host: https://astro-<your-astro-base-domain>.datakin.com,
          openlineage_apiKey: <your-openlineage-api-key>,
          openlineage_namespace: <namespace-name> # Replace with your job namespace; Astronomer recommends using a meaningful namespace such as `dev` or `prod`,
          job_name: validate_task_name,
   ```

3. Deploy your changes to Astro. See [Deploy code](deploy-code.md).

#### Verify

To confirm that your setup is successful, click **Lineage** in the Cloud UI and then click **Issues** in the left menu. Recent data quality assertion issues appear in the **All Issues** table.

If your code hasn't produced any data quality assertion issues, use the search bar to search for a dataset and view its node on the lineage graph for a recent job run. Click **Quality** to view metrics and assertion pass or fail counts.

### OpenLineage and Spark

Use the information provided here to set up lineage collection for Spark.

#### Prerequisites

- A Spark application.
- A Spark job.
- Your Astro base domain.
- Your Organization's OpenLineage API key.

#### Setup

In your Spark application, set the following properties to configure your lineage endpoint, install the [`openlineage-spark`](https://search.maven.org/artifact/io.openlineage/openlineage-spark) library, and configure an _OpenLineageSparkListener_:

   ```python
   SparkSession.builder \
     .config('spark.jars.packages', 'io.openlineage:openlineage-spark:0.2.+')
     .config('spark.extraListeners', 'io.openlineage.spark.agent.OpenLineageSparkListener')
     .config('spark.openlineage.transport.url', 'https://astro-<your-astro-base-domain>.datakin.com')
     .config('spark.openlineage.apiKey', '<your-openlineage-api-key>')
     .config('spark.openlineage.namespace', '<namespace-name>') # Replace with the name of your Spark cluster.
     .getOrCreate()                                             # Astronomer recommends using a meaningful namespace such as `spark-dev` or `spark-prod`.
   ```

#### Verify

To confirm that your setup is successful, run a Spark job after you save your configuration. After you run this model, click **Lineage** in the Cloud UI and then click **Runs** in the left menu. Your recent Spark job run appears in the table of most recent runs.


## Enable/Disable OpenLineage

Astro uses OpenLineage to extract lineage metadata for your Airflow operators and to send Astro alerts. By default, OpenLineage is enabled for all Astro Deployments. 

To disable it, add the following line to your `Dockerfile`:

`ENV OPENLINEAGE_DISABLED = True`

Deploy your Astro project for the changes to take effect in your Deployment.

To re-enable OpenLineage, you can either set `ENV OPENLINEAGE_DISABLED = False` or remove this line from your `Dockerfile`.

## View SQL source code

The SQL source code view for [supported Airflow operators](https://openlineage.io/docs/integrations/about/#capability-matrix) in the Cloud UI  **Lineage** page is off by default for all Workspace users. To enable the source code view, set the following [environment variable](environment-variables.md) for each Astro Deployment:

- Key: `OPENLINEAGE_AIRFLOW_DISABLE_SOURCE_CODE`
- Value: `False`

Astronomer recommends enabling this feature only for Deployments with non-sensitive code. For more information about Workspace permissions, see [Workspace roles](user-permissions.md#workspace-roles).

## Generate custom facets for OpenLineage events

[OpenLineage facets](https://openlineage.io/docs/spec/facets/) are JSON objects that provide additional context about a given job run. By default, a job run for an Airflow task includes facets that show the source code for the task, whether the task run was successful, and who owns the task. All default facets for a job run appear as **Standard Facets** in the **Info** tab of your data pipeline's lineage graph. 

You can configure both Airflow and external systems to generate custom facets that contain more specific information about job runs. Custom facets appear as **Custom Facets** in the **Info** tab of your data pipeline's lineage graph. To create a custom facet, see [OpenLineage Documentation](https://openlineage.io/docs/spec/facets/custom-facets).


