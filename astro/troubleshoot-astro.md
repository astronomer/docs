---
sidebar_label: 'Troubleshooting FAQ'
title: 'Astro Troubleshooting FAQ'
id: troubleshoot-astro
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Use this document to learn more about common issues on Astro and how to resolve them. 

## Why does my Deployment have zombie tasks? 

Zombie tasks are task runs that Airflow assumes are running but have somehow died. Zombie tasks often occur when a process running a task is killed or the node running a task worker is terminated.

There are a few reasons why your Deployment could have zombie tasks:

- You are receiving `FailedScheduling` errors due to insufficient scheduler CPU and memory.
- You have DAG parsing issues.
- You are encountering a known Airflow bug in versions 2.0.0 - 2.3.2.
- (AWS only) T2 and T3 instance types are throttled due to lack of credits.

### Context: Symptoms of zombie tasks

Use the following methods to find zombie tasks on a Deployment:

- Search for missing log errors in your task logs. For example, the following log might indicate a zombie task run because there was no evidence of it running to completion:

    ```text
    *** Falling back to local log 
    *** Log file does not exist: /usr/local/airflow/logs/dag_id=<dag>/run_id=<run>/task_id=<task>/attempt=1.log 
    *** Fetching from: http://<ip>/log/dag_id=<dag>/run_id=<run>/task_id=<task>/attempt=1.log 
    *** Failed to fetch log file from worker. Client error '404 NOT FOUND' for url 'http://<ip>/log/dag_id=<dag>/run_id=<run>/task_id=<task>/attempt=1.log' For more information check: https://httpstatuses.com/404
    ```

- Search for zombie logs in your task logs. For example:

    ```text
    ERROR - Detected zombie job
    ```

    Because Airflow occasionally creates these logs with irregular spacing, search only for `zombie` to find all available zombie logs. 
    
### Solution: Use safeguards for preventing zombie tasks

Implement the following practices to limit zombie tasks on your Deployment:

- Ensure that you run at least 2 retries for all tasks by setting `retries=2` in your task parameters. 
- Whenever possible, use deferrable operators and sensors. These operators can mitigate zombie tasks because their execution often occurs outside of Airflow, meaning that the Airflow task itself won't be killed by the loss of a worker node.

### Solution: Upgrade to the latest patch of Astro Runtime 5 or validate DAGs

In Runtime 5.0.7 and earlier, it's possible for Airflow to produce zombie tasks by attempting to run a DAG with syntax errors. When you push breaking changes to an existing DAG on Astro:

- Airflow attempts to run a task that it detected from an earlier version of the DAG.
- The task fails and triggers `on_failure_callback` logic.
- Airflow doesn't know how to handle the `on_failure_callback` logic because it can't parse the broken DAG, and after 5 minutes produces a zombie task. 

If your DAG failed to parse, you might have one of the following logs in your task logs:

- `Broken DAG`
- `Failed to parse`
- `airflow.exceptions.AirflowTaskTimeout: DagBag import timeout`

If your Deployment has a DAG with syntax errors, complete one of the following actions to stop zombie tasks:

- Upgrade to the latest patch version Astro Runtime 5 or later. See [Upgrade Runtime](upgrade-runtime.md).
- Upgrade to Astro CLI 1.0 or later. Later versions of the Astro CLI parse your DAGs by default and prevent your from deploying DAGs if they contain syntax errors. See [Install the CLI](cli/install-cli.md).

## How do I confirm that my deploy to Astro was successful?

1. Check the Astro CLI logs for your deploy. If you deployed an image to Astro, you should see the following confirmation message:
    
    ```text
    Deployed Image Tag:  <new-image-tag>
    Successfully pushed Docker image to Astronomer registry. Navigate to the Astronomer UI for confirmation that your deploy was successful.
    ```

    If you triggered a DAG-only deploy to Astro, you should see the following confirmation message:

    ```text
    Successfully uploaded DAGs with version <new-dag-bundle-version> to Astro. Navigate to the Airflow UI to confirm that your deploy was successful. The Airflow UI takes about 1 minute to update.
    ```

    If you didn't receive one of these messages and instead received an error, you might have encountered one of the following errors:

    - Docker doesn't have access to your DAGs directory. Check your **File sharing** settings on Docker Desktop to confirm that Docker can access your Astro project directory. 
    - You didn't successfully authenticate to Astro. Ensure you're in the right Organization and Workspace by running `astro organization list` and `astro workspace list`. If you're deploying from a CI/CD pipeline, ensure that your CI/CD environment has access to a valid [Deployment API key](api-keys.md#use-an-api-key-with-the-astro-cli) or [Workspace API token](workspace-api-tokens.md#use-a-workspace-api-token-with-the-astro-cli).
    - You had a parsing error in one of your DAGs. Fix the errors or run `astro deploy --force` to deploy without checking for errors. 

2. In the Cloud UI, open your Deployment and check the **Docker Image** and **DAG Bundle Version** info boxes. These fields should show the image tag or latest DAG bundle version from your most recent deploy. Both of the values include the date and time that the deploy was executed. 

    Confirm that these values are the same as `<new-image-tag>` and `<new-dag-bundle-version>` from Step 1. If they aren't, and nobody else has deployed changes since your last deploy, contact [Astronomer Support](https://cloud.astronomer.io/support).

3. In the Cloud UI, open your Deployment and click **Logs**. Change the **Log Level** to include **Info** level logs, then click **Apply**. After the info-level logs appear, check that Airflow is parsing the DAGs you deployed. You should see all of your deployed DAGs listed under the log titled `DAG File Processing Stats`.

    If you confirmed the deploy was successful in Steps 1 and 2 but Airflow isn't parsing your DAGs, contact [Astronomer Support](https://cloud.astronomer.io/support).


