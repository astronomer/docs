---
title: 'View logs'
sidebar_label: 'View logs'
id: view-logs
description: View logs for your data pipelines both on Astro and locally.
---

View task and component logs for your DAGs to troubleshoot your data pipelines and better understand the behavior of your tasks and their execution environment.

## Log and message types

- _Scheduler logs_ can help you understand scheduler performance and indicate if a task failed due to an issue with the scheduler. For more information on configuring the scheduler on Astro, see [Scheduler resources](configure-deployment-resources.md#scheduler-resources).

- _Triggerer logs_ provide information about the performance of the triggerer, the Airflow component responsible for running triggers and signaling tasks to resume when their conditions have been met. The triggerer is used exclusively for tasks that are run with [deferrable operators](https://docs.astronomer.io/learn/deferrable-operators.md).

- _Worker logs_ describe the performance of the _woriker_, the process that executes tasks, as defined by the [executor](https://docs.astronomer.io/learn/airflow-executors-explained.md#what-is-an-executor)

- _Webserver logs_ relate to the health and performance of [the Airflow UI](https://docs.astronomer.io/learn/intro-to-airflow.md#airflow-components)

### Log Levels 

Each log and message type is also associated with one of the following _log levels_: 

    - **Error**: Emitted when a process fails or does not complete. For example, these logs might indicate a missing DAG file, an issue with your scheduler's connection to the Airflow database, or an irregularity with your scheduler's heartbeat.
    - **Warn**: Emitted when Airflow detects an issue that may or may not be of concern but does not require immediate action. This often includes deprecation notices marked as `DeprecationWarning`. For example, Airflow might recommend that you upgrade your Deployment if there was a change to the Airflow database or task execution logic.
    - **Info**: Emitted frequently by Airflow to show that a standard scheduler process, such as DAG parsing, has started. These logs are frequent but can contain useful information. If you run dynamically generated DAGs, for example, these logs will show how many DAGs were created per DAG file and how long it took the scheduler to parse each of them.

## View Airflow task logs

Airflow task logs for both local Airflow environments and Deployments on Astro are available in the Airflow UI. Task logs can help you troubleshoot a specific task instance that failed or retried.

On Astro, Airflow task logs are stored in the data plane on your cloud. On Amazon Web Services (AWS), they are stored in S3. On Google Cloud Platform (GCP), they are stored in Cloud Storage. On Azure, they are stored in Azure Blob Storage. 

On clusters hosted in your own cloud, task logs are stored indefinitely. On clusters hosted in Astronomer's cloud, task logs are hosted for 90 days. The task log retention policy is not currently configurable.

1.  Access the Airflow UI. To access the Airflow UI for a Deployment, open the Deployment in the Cloud UI and click **Open Airflow**. To access the Airflow UI in a local environment, open a browser and go to `http://localhost:8080`.
2. Click a DAG.
3. Click **Graph**.
4. Click a task run.
5. Click **Instance Details**.
6. Click **Log**.

## View logs in the Cloud UI

You can access scheduler, triggerer, and worker logs in the Cloud UI to find the past 24 hours of logs for any Deployment on its **Logs** page. Logs are color-coded according to their type. 

1. In the Cloud UI, select a Workspace and then a Deployment.

2. Click the **Logs** tab.

    When a Deployment generates more than 500 lines of logs in 24 hours, only the most recent 500 lines are shown. If there are no logs available for a given Deployment, the following message appears:

    ```  
    No matching events have been recorded in the past 24 hours.
    ```

    Typically, this indicates that the Deployment you selected does not currently have any DAGs running.

### Filter options

You can use the following options to specify the types of logs or messages that you want to view. 

- **String search**: Enter a string, keyword, or phrase to find in your logs.

- **Time range**: Filter the logs displayed based on time. 

- **Log type**: Filter based on whether the log message is from scheduler, worker, webserver, or trigger. 

## Access Airflow component logs locally

To show logs for your Airflow scheduler, webserver, or triggerer locally, run the following Astro CLI command:

```sh
astro dev logs
```

Once you run this command, the most recent logs for these components appear in your terminal window.

By default, running `astro dev logs` shows logs for all Airflow components. To see logs only for a specific component, add any of the following flags to your command:

- `--scheduler`
- `--webserver`
- `--triggerer`

To continue monitoring logs, run `astro dev logs --follow`. The `--follow` flag ensures that the latest logs continue to appear in your terminal window. For more information about this command, see [CLI Command Reference](cli/astro-dev-logs.md).

Logs for the Airflow webserver, worker, and triggerer are not available for Deployments on Astro.

## Export task logs to Datadog (_AWS only_)

Astro supports forwarding Airflow task logs to [Datadog](https://www.datadoghq.com/). You only need to enable Datadog once for each Astro cluster. After you enable Datadog, task logs from all Deployments in the cluster are exported.

1. Create a new Datadog API key or copy an existing API key. See [API and Application Keys](https://docs.datadoghq.com/account_management/api-app-keys/).
2. Identify the Astro cluster from which you want to forward task logs.
3. Submit a request to [Astronomer support](https://cloud.astronomer.io/support) with your Datadog API key, the name of your Astro cluster, and the [Datadog Site](https://docs.datadoghq.com/getting_started/site/) where you want the logs forwarded.

Astro also supports exporting Airflow metrics to Datadog. See [Export Airflow metrics to Datadog](deployment-metrics.md#export-airflow-metrics-to-datadog).