---
title: "Orchestrate dbt Cloud with Airflow"
sidebar_label: "dbt Cloud"
id: airflow-dbt
---

<head>
  <meta name="description" content="Learn how to use the dbt Cloud Provider to orchestrate dbt Cloud with Airflow." />
  <meta name="og:description" content="Learn how to use the dbt Cloud Provider to orchestrate dbt Cloud with Airflow." />
</head>

import CodeBlock from '@theme/CodeBlock';
import airflow_dbt_simple from '!!raw-loader!../code-samples/dags/airflow-dbt/airflow_dbt_simple.py';

[dbt Cloud](https://getdbt.com/) is a managed service providing a hosted architecture to run dbt, a tool that helps users build interdependent SQL models for in-warehouse data transformation, using ephemeral compute of data warehouses. For a tutorial on how to use the open-source dbt Core package with Airflow see [Orchestrate dbt Core with the Astronomer dbt provider](airflow-dbt-cosmos.md).

The [dbt Cloud provider](https://registry.astronomer.io/providers/dbt-cloud) allows user to orchestrate actions in dbt Cloud embedded in the Airflow environment. Running dbt with Airflow ensures a reliable, scalable environment for models, as well as the ability to trigger models based on upstream dependencies in the whole data ecosystem. Airflow also gives you fine-grained control over dbt tasks such that teams have observability over every step in their dbt models.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of dbt. See [Getting started with dbt Cloud](https://docs.getdbt.com/guides/getting-started).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## Time to complete

This tutorial takes approximately 30min to complete.

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli).
- A dbt Cloud account. A [14-day free trial](https://www.getdbt.com/signup/) is available.
- Access to an instance of a data warehouse supported by dbt Cloud. View the [dbt documentation](https://docs.getdbt.com/docs/supported-data-platforms) for an up-to-date list of adapters.

## Step 1: Configure your Astro project

An Astro project contains all of the files you need to run Airflow locally.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-dbt-cloud-tutorial && cd astro-dbt-cloud-tutorial
    $ astro dev init
    ```

2. Add the [dbt Cloud provider](https://registry.astronomer.io/providers/dbt-cloud) to your `requirements.txt` file.

    ```text
    apache-airflow-providers-dbt-cloud
    ```

3. Run the following command to start your Astro project:

    ```sh
    $ astro dev start
    ```

## Step 2: Configure a dbt connection

1. In the Airflow UI, go to **Admin** -> **Connections** and click **+**. 

2. Create a new connection named `dbt_conn` and choose the `dbt Cloud` connection type. Enter the following information:

    - Tenant: the URL under which your API cloud is hosted at, defaults to `cloud.getdbt.com` if left empty.
    - Account ID: (optional) default dbt account to use with this connection.
    - API Token: A dbt [User Token](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens).

## Step 3: Configure a dbt Cloud job

In the dbt Cloud UI create one dbt Cloud job. The contents of this job do not matter, you can for example use the jaffle shop example from dbt's [Quickstart documentation](https://docs.getdbt.com/docs/quickstarts/overview). Write down the dbt Cloud `job_id` for use in the next step.

## Step 4: Write a dbt Cloud DAG

1. In your `dags` folder create a file called `check_before_running_dbt_cloud_job.py`.

2. Copy the following code into the file and provide the `JOB_ID` of your dbt Cloud job:

    <CodeBlock language="python">{airflow_dbt_simple}</CodeBlock>

    This DAG shows a simple implementation of using the [DbtCloudRunJobOperator](https://registry.astronomer.io/providers/dbt-cloud/modules/dbtcloudrunjoboperator) operator from the dbt Cloud provider to trigger the run of a dbt Cloud job and how to utilize the [DbtCloudHook](https://registry.astronomer.io/providers/dbt-cloud/modules/dbtcloudhook). The DAG consists of two tasks:

    - `check_job_is_not_running`: uses the [ShortCircuitOperator](https://registry.astronomer.io/providers/apache-airflow/modules/shortcircuitoperator) to ensure that the dbt Cloud job with the specified `JOB_ID` is not currently running. The list of currently running dbt Cloud jobs is retrieved using the `list_job_runs()` method of the `DbtCloudHook`. If the job is currently not in a state of 10 (Success), 20 (Error), or 30 (Canceled), the pipeline will not try to trigger another run.
    - `trigger_dbt_cloud_job` uses the `DbtCloudRunJobOperator` to trigger a run of the dbt Cloud job with the correct `JOB_ID`.

3. Run the DAG and verify that the dbt Cloud job ran in the dbt Cloud UI.

:::info

The full code for this example, along with other DAGs that implement the dbt Cloud provider, can be found on the [Astronomer Registry](https://registry.astronomer.io/dags?providers=dbt+Cloud&page=1). 

:::

:::info

You can find more examples of how to use dbt Cloud with Airflow in [dbt's documentation](https://docs.getdbt.com/guides/orchestration/airflow-and-dbt-cloud/1-airflow-and-dbt-cloud).

:::

## Async dbt Cloud operators

With the addition of [deferrable operators](deferrable-operators.md) to Airflow such operators were developed for dbt Cloud as well. 
The Astronomer provider contains asynchronous version of several dbt modules:

- [DbtCloudHookAsync](https://registry.astronomer.io/providers/astronomer-providers/modules/dbtcloudhookasync): asynchronous version of the DbtCloudHook.
- [DbtCloudRunJobTrigger](https://registry.astronomer.io/providers/astronomer-providers/modules/dbtcloudrunjobtrigger): Trigger class used in deferrable dbt Cloud operators.
- [DbtCloudJobRunSensorAsync](https://registry.astronomer.io/providers/astronomer-providers/modules/dbtcloudjobrunsensorasync): Asynchronously checks the status of dbt Cloud job runs.
- [DbtCloudRunJobOperatorAsync](https://registry.astronomer.io/providers/astronomer-providers/modules/dbtcloudrunjoboperatorasync): Executes a dbt Cloud job asynchronously and waits for the job to reach a terminal status before completing successfully.

## Conclusion

Congratulations! You've run a DAG which uses the dbt Cloud provider to orchestrate a job run in dbt Cloud.