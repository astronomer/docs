---
title: 'View Logs'
sidebar_label: 'View Logs'
id: view-logs
description: View Deployment Airflow logs in the Cloud UI.
---

## Overview

You can access the the recorded Scheduler logs for a 24 hour period for a Deployment on the Cloud UI **Scheduler Logs** page. When a Deployment generates more than 500 logs in 24 hours, only the most recent 500 logs are available. Logs are color-coded to simplify log type identification. The scheduler logs can help you understand why specific tasks failed.

Airflow task logs are available in the Airflow UI. Task logs can help you troubleshoot a specific task instance that failed or retried.

## View Scheduler Logs

1. In the Cloud UI, select a Workspace.
2. Click **Logs**.

    ![Logs icon and button](/img/docs/log-location.png)

3. Select a Deployment in the **Select a deployment list**.
4. Optional. Select the log level and click **Apply**. These are the available options:

    - **Error**: Emitted when a process fails or does not complete. For example, these logs might indicate a missing DAG file, an issue with your Scheduler's connection to the Airflow database, or an irregularity with your Scheduler's heartbeat.
    - **Warn**: Emitted when Airflow detects an issue that may or may not be of concern but does not require immediate action. This often includes deprecation notices marked as `DeprecationWarning`. For example, Airflow might recommend that you upgrade your Deployment if there was a change to the Airflow database or task execution logic.
    - **Info**: Emitted frequently by Airflow to show that a standard Scheduler process, such as DAG parsing, has started. These logs are frequent but can contain useful information. If you run dynamically generated DAGs, for example, these logs will show how many DAGs were created per DAG file and how long it took the Scheduler to parse each of them.

5. Optional. To view the Scheduler logs for a different Deployment, select a Deployment in the **Select a deployment list**.

## View Airflow Task Logs

Submit a support request if you're using Amazon S3 and need your Airflow task logs forwarded to Datadog. You'll need to provide your Datadog API key and identify on which cluster(s) you want integration enabled. See [Submit a Support Request](astro-support.md).

1.Open a browser and go to `http://localhost:8080`.
2. Open the DAG you want to troubleshoot:

    <div class="text--center">
    <img src="/img/docs/open-dag.png" alt="Access DAG from Airflow UI" />
    </div>

3. In the **Tree View**, click on the task run you want to see logs for:

    <div class="text--center">
    <img src="/img/docs/tree-view.png" alt="Task runs in the tree view" />
    </div>

4. Click **Instance Details**:

    <div class="text--center">
    <img src="/img/docs/instance-details.png" alt="Instance details button in the task log menu" />
    </div>

5. Click **Log**:

    <div class="text--center">
    <img src="/img/docs/task-log.png" alt="Log button from a task instance" />
    </div>

## Access Airflow Component Logs

Airflow Webserver, Worker, and Triggerer logs are not available for Astro Deployments.

To show logs for your Airflow Scheduler, Webserver, or metadata database locally, run the following command:

```sh
astro dev logs
```

Once you run this command, the most recent logs for these components appear in your terminal window.

By default, running `astro dev logs` shows logs for all Airflow components. If you want to see logs for a specific component, add any of the following flags to your command:

- `--scheduler`
- `--webserver`
- `--triggerer`

To continue monitoring logs, run `astro dev logs --follow`. The `--follow` flag ensures that the latest logs continue to appear in your terminal window. For more information about this command, see [CLI Command Reference](cli/astro-dev-logs.md)
