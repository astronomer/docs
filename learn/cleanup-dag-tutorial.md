---
title: 'Clean up the Airflow metadata database using DAGs'
sidebar_label: 'Clean up the metadata database'
id: cleanup-dag-tutorial
description: 'Learn how to remove unnecessary data from the Airflow metadata database using the `airflow db clean` command from a DAG.'
---

import CodeBlock from '@theme/CodeBlock';
import db_cleanup from '!!raw-loader!../code-samples/dags/cleanup-dag-tutorial/db_cleanup.py';

In addition to storing configuration about your Airflow environment, the Airflow [metadata database](https://docs.astronomer.io/learn/airflow-database) stores data about past and present task runs. Airflow never automatically removes metadata, so the longer you use it, the more task run data is stored in your metadata DB. Over a long enough time, this can result in a bloated metadata DB, which can affect performance across your Airflow environment.

When a table in the metadata DB is larger than 50GB, you might start to experience degraded scheduler performance. This can result in:

- Slow task scheduling
- Slow DAG parsing
- [List more specifics]

The following tables in the database are at risk of becoming too large over time:

- `job` 
- `dag_run` 
- `task_instance`
- `log` 
- `dags` 
- `task_reschedule`
- `task_fail`

To keep your Airflow environment running at optimal performance, you can clean the metadata DB using the Airflow CLI `airflow db clean` command. This command was created as a way to safely clean up your metadata DB without modifying it directly, as this can cause dependency issues and corrupt your Airflow instance. This tutorial walks you through how to implement a cleanup DAG in Airflow so that you can clean your database using the command directly from the Airflow UI.

:::danger

Even when using `airflow db clean`, deleting data from the metadata database can be destructive . Read the [Warnings](#warnings) section carefully before implementing this tutorial DAG in any production Airflow environments.

:::

## Warnings


Deleting data from the metadata database can be an extremely destructive action. If you delete data that future task runs depend on, it's difficult to recover the database to its previous state without interrupting your data pipelines. Before implementing the DAG in this tutorial, consider the following:

- Only trigger a database cleanup if you need to. If your Airflow scheduler is running normally, there's no need to clean the DB. On Astro, you will receive alerts when specific tables contain enough data to cause performance issues.
- Delete older data before newer data. The older the deleted data, the less likely it is to affect your currently running DAGs.
- On Astro, the DAG will fail if it runs for longer than five minutes, which can happen if you have an exceptionally large amount of data to delete. If this happens, use the DAG's params to reduce the amount of data being deleted at once, either by reducing the time window for deletion or reducing the number of tables to clean.

## Prerequisites

- An Astro project
- The Astro CLI

## Step 1: Create your DAG


1. In your dags folder, create a file called `db_cleanup.py`.

2. Copy the following code into the file.

    <CodeBlock language="python">{db_cleanup}</CodeBlock>

    Rather than running on a schedule, this DAG is triggered manually by default and includes params so that you're in full control over how you clean the metadata DB.

    It includes one task, `clean_db`, that runs `airflow db clean` with the params you specify at runtime. The params let you specify:

    - What age of data to delete. Any data that was created before the specified time will be deleted. The default is to delete all data older than 90 days.
    - Whether to run the cleanup as a dry run, meaning that no data is deleted. The DAG will instead return the SQL that would be executed based on other parameters you have specified. The default is to run the deletion without a dry run.
    - Which tables to delete data from. The default is all tables.

## Step 2: Run the DAG

In this step, you'll run the DAG in a local Airflow environment to practice the workflow for cleaning metadata DB data. In reality, you would first deploy this DAG to a production environment, such as an Astro Deployment, then run the DAG only when your metadata DB was getting full.

1. Run `astro dev start` in your Astro project to start Airflow, then open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `db_cleanup` DAG by clicking the play button, then click **Trigger DAG w/ Config**. Configure the following params:

    - `dry_run`: `true`
    - `tables`: `all_tables`
    - `clean_before_timestamp`: `datetime.now(tz=UTC) - timedelta(days=90)`

3. Click **Trigger**. 
4. After the task completes, click **Graph**.
5. Click a task run.
6. Click **Instance Details**.
7. Click **Log**.
8. Check that the `airflow db cleanup` command completed successfully. Note that you created a new Astro project, the run will not show much data to be deleted. 

You can now use this DAG to periodically clean data from the Airflow metadata DB as needed. 