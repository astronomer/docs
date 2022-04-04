---
sidebar_label: 'Set Up Lineage'
title: "Enable Data Lineage for External Systems"
id: lineage-integrations
---

## Overview

This guide explains how to configure your data pipelines to emit lineage data to Astro.

To generate lineage graphs for your data pipelines, you first need to configure your data pipelines to emit lineage data. Because lineage data can be generated in all stages of your pipeline, you can configure pipeline components outside of Astro, such as dbt or Databricks, to emit lineage data whenever they're running a job. Coupled with lineage data emitted from your DAGs, Astro generates a lineage graph that can provide context to your data before, during, and after it reaches your Deployment.

Lineage data is generated via OpenLineage, which is an open source standard for lineage data creation and collection. Astro receives metadata about running jobs and datasets via the OpenLineage API. Each Astro Organization has an OpenLineage API key that you can specify in your external systems. Your external systems can use this API key to send lineage data back to your Control Plane.

![Diagram showing how lineage data flows to Astro](/img/docs/lineage-diagram.png)

Generally, configuring a system to send lineage data requires:

- Installing an OpenLineage backend to emit lineage data from the system
- Specifying your organization's OpenLineage API endpoint to send lineage data back to the Astro Control Plane.

:::tip

You can access a version of this documentation directly from the **Lineage** tab in the Cloud UI. The embedded documentation additionally loads your Organization's configuration values, such as your OpenLineage API key and your Astro base domain, directly into configuration steps.

:::

### Retrieve Your OpenLineage API Key

Each Organization has a unique OpenLineage API key that is required to send lineage data from external systems to Astro. To find your Organization's key:

1. In the Cloud UI, open the **Lineage** tab.
2. In the left-hand lineage menu, click **Integrations**:

    ![Location of the "Integrations" button in the Lineage tab of the Cloud UI](/img/docs/lineage-integrations.png)

3. In **Getting Started**, copy the value in **Lineage API Key**.

This key is required in each of the following integration guides.

## Integration Guides

<Tabs
    defaultValue="astronomer"
    values={[
        {label: 'Astronomer', value: 'astronomer'},
        {label: 'Databricks', value: 'databricks'},
        {label: 'Great Expectations', value: 'greatexpectations'},
        {label: 'Apache Spark', value: 'spark'},
        {label: 'dbt', value: 'dbt'},
    ]}>
<TabItem value="astronomer">

Lineage is configured automatically for all Deployment on Astro Runtime 4.2.0+. Therefore, the easiest way to add lineage to an existing Deployment on Runtime <4.2.0 is to [upgrade Runtime to at least 4.2.0](https://docs.astronomer.io/cloud/upgrade-runtime).

>**Note:** If you don't see lineage features enabled for a Deployment on Astro Runtime 4.2.0+, then you might need to [push code](deploy-code.md) to the Deployment to trigger the configuration process.

To configure lineage on an existing Deployment on Runtime <4.2.0 without upgrading Runtime:

1. In your locally hosted Astro project, update your `requirements.txt` file to include the following line:

   ```
   openlineage-airflow
   ```

2. [Push your changes](deploy-code.md) to your Deployment.

3. In the Cloud UI, [set the following environment variables](environment-variables.md) in your Deployment:

    ```
    AIRFLOW__LINEAGE__BACKEND=openlineage.lineage_backend.OpenLineageBackend
    OPENLINEAGE_URL=https://api.<your-astro-base-domain>
    OPENLINEAGE_API_KEY=<your-lineage-api-key>
    ```

#### Verify

To view lineage metadata, go to your organization's [landing page](http://cloud.astronomer.io) and open the **Lineage** tab at the top of the page. If lineage was configured correctly, you should see your DAGs represented in the lineage graph.

>**Note:** Lineage information will appear only for DAGs that use operators which have extractors defined in the `openlineage-airflow` library, such as the `PostgresOperator` and `SnowflakeOperator`. For a full list of supported operators, see Astronomer documentation.

> **Note:** To see lineage for existing DAGs, your DAGs need to run at least once after configuring lineage in order to emit data to the lineage backend and generate a graph.

</TabItem>

<TabItem value="databricks">

This guide outlines how to set up lineage collection for Spark running on a Databricks cluster.

#### Prerequisites

To complete this setup, you need:

- A Databricks cluster.
- Your Astro base domain.
- Your Organization's OpenLineage API key.

#### Setup

1. In Databricks, create a [cluster-scoped init script](https://docs.databricks.com/libraries/cluster-libraries.html#init-script-1) with the following command to install the `openlineage-spark` library at cluster initialization:

    ```sh
    #!/bin/bash

    /databricks/python/bin/pip install openlineage-spark
    ```

2. In the cluster configuration page for your Databricks cluster, specify the following [Spark configuration](https://docs.databricks.com/clusters/configure.html#spark-configuration):

   ```bash
   spark.driver.extraJavaOptions -Djava.security.properties=
   spark.executor.extraJavaOptions -Djava.security.properties=
   spark.openlineage.url https://api.<your-astro-base-domain>
   spark.openlineage.apiKey <your-lineage-api-key>
   spark.openlineage.namespace <NAMESPACE_NAME> // We recommend a meaningful namespace like `spark-dev`, `spark-prod`, etc.
   ```

After you save this configuration, lineage will be enabled for all Spark jobs running on your cluster.

#### Verify Setup

To test that lineage was configured correctly on your Databricks cluster, run a test Spark job on Databricks. After your job runs, open the **Lineage** tab in the Cloud UI. If your configuration was successful, you should see your Spark job appear in the **Explore** tab. From here, you can click a job run to see it within a lineage graph.

</TabItem>

<TabItem value="dbt">

This guide outlines how to set up lineage collection for a dbt project.

#### Prerequisites

To complete this setup, you need:

- A [dbt project](https://docs.getdbt.com/docs/building-a-dbt-project/projects).
- The [dbt CLI](https://docs.getdbt.com/dbt-cli/cli-overview).
- Your Astro base domain.
- Your Organization's OpenLineage API key.

#### Setup

1. On your local machine, run the following command to install the [`openlineage-dbt`](https://pypi.org/project/openlineage-dbt) library:

   ```sh
   $ pip install openlineage-dbt
   ```

2. Configure the following environment variables in your shell:

   ```bash
   OPENLINEAGE_URL=https://api.<your-astro-base-domain>
   OPENLINEAGE_API_KEY=<your-lineage-api-key>
   OPENLINEAGE_NAMESPACE=<NAMESPACE_NAME> # Replace with the name of your dbt project.
                                          # We recommend a meaningful namespace like `dbt-dev`, `dbt-prod`, etc.
   ```

3. Run the following command to generate the [`catalog.json`](https://docs.getdbt.com/reference/artifacts/catalog-json) for your dbt project:

   ```bash
   $ dbt docs generate
   ```

4. In your dbt project, run the [OpenLineage](https://openlineage.io/integration/dbt/) wrapper script using the `dbt run` [command](https://docs.getdbt.com/reference/commands/run):

   ```bash
   $ dbt-ol run
   ```

#### Verify Setup

To confirm that your setup was successful, run a `dbt` model in your project. After you run this model, go to the Cloud UI and open the **Lineage** tab. In the **Explore** menu, you should see the run that you triggered.

</TabItem>

<TabItem value="greatexpectations">

This guide outlines how to set up lineage collection for a running Great Expectations suite.

#### Prerequisites

To complete this setup, you need:

- A [Great Expectations suite](https://legacy.docs.greatexpectations.io/en/latest/guides/tutorials/getting_started.html#tutorials-getting-started).
- Your Astro base domain.
- Your Organization's OpenLineage API key.

#### Setup

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
              openlineage_host: https://api.<your-astro-base-domain>
              openlineage_apiKey: <your-lineage-api-key>
              openlineage_namespace: <NAMESPACE_NAME> # Replace with your job namespace; we recommend a meaningful namespace like `dev` or `prod`, etc.
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

#### Verify

To confirm that your setup was successful,  open the **Lineage** tab and open the **Home** menu. Any recent data quality assertion issues should appear in the **All Issues** table.

If your code hasn't produced any data quality assertion issues, use the search bar to search for the relevant dataset and view its node on the lineage graph. When you click on the **Quality** tab, you should see metrics and assertion pass/fail counts:

</TabItem>

<TabItem value="spark">

This guide outlines how to set up lineage collection for Spark.

#### Prerequisites

To complete this setup you need:

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
     .config('spark.openlineage.host', 'https://api.<your-astro-base-domain>')
     .config('spark.openlineage.apiKey', '<your-lineage-api-key>')
     .config('spark.openlineage.namespace', '<NAMESPACE_NAME>') # Replace with the name of your Spark cluster.
     .getOrCreate()                                             # We recommend a meaningful namespace like `spark-dev`, `spark-prod`, etc.
   ```

#### Verify

To confirm that your setup was successful, run a Spark job after you save your configuration. In the Cloud UI, open the **Lineage** tab and open the **Explore** menu. Your recent Spark job run should appear under **Most Recent Runs**.

</TabItem>
