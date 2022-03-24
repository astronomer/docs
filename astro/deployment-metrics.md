---
sidebar_label: 'Deployment Metrics'
title: 'Deployment Metrics'
id: deployment-metrics
description: Monitor Deployment performance, health, and total task volume in the Cloud UI.
---

## Overview

The Cloud UI exposes a suite of observability metrics that show real-time data related to the performance and health of your Deployments. These metrics are a useful reference as you troubleshoot issues and can inform how you allocate resources. They can also help you estimate the cost of your Deployments. This document explains each available metric and where to find them.

## Deployment Health

Deployment health appears as a real-time status at the top of your Deployment's information page. Deployment health is meant to show whether or not the most important components within your Deployment are running as expected.

![Deployment Health status](/img/docs/deployment-health.png)

Deployment health can have one of two statuses:

- **Healthy** (Green): The Airflow Webserver and Scheduler are both healthy and running as expected.
- **Unhealthy** (Red): This status can mean one of two things:

    - Your Deployment was recently created and the Airflow Webserver and Scheduler are still spinning up.
    - Your Deployment's Webserver and/or Scheduler are restarting or otherwise not in a healthy, running state.

If your Deployment is unhealthy, we recommend checking the status of your tasks and waiting for a few minutes. If your Deployment is unhealthy for more than 5 minutes, we recommend [reviewing Scheduler logs](scheduler-logs.md) in the Cloud UI or reaching out to [Astronomer Support](https://support.astronomer.io).

## Deployment Analytics

Located in the Workspace view of the Astro UI, the **Analytics** page provides detailed metrics for all Deployments in a Workspace. This page includes metrics that give you insight into the performance of both your data pipelines and infrastructure. Because metrics are pulled from Splunk and Thanos in real time, you can use this page to detect irregularities in your pipelines or infrastructure at the moment they happen.

To view metrics for a given Deployment, click the **Analytics** button in the lefthand menu and select a Deployment and time range from the dropdown menus:

You can also access analytics for a specific Deployment from the Deployment's page:

Use the following topics to learn more about each available metric.

### DAG Runs

These metrics contain information about your Deployment's DAG runs over a given period of time.

- **DAG Runs**: This metric shows the total number of DAG runs.
- **Runs per Status**: This metric shows the number of failed and successful DAG runs, plotted based on the DAG run start time.
- **P90 Run Duration per Status**: This metric shows the 90th percentile of execution times for DAG runs, plotted based on the DAG run start time. In the example above, the P90 Run Duration per Status for successful DAG runs at 5:00 was 34 seconds, which means that 90% of those DAG runs finished in 34 seconds or less.

### Task Runs

These metrics contain information about your Deployment's task runs over a given period of time.

- **Task Runs**: This metric charts the total number of task runs.
- **Runs per Status**: This metric charts the number of failed and successful task runs, plotted based on the DAG run start time.
- **P90 Run Duration per Status**: This metric charts the 90th percentile of execution times for task runs, plotted based on the task run start time. In the example above, the P90 Run Duration per Status for successful task runs at 5:00 was 4 seconds, which means that 90% of those task runs finished in 4 seconds or less.

### Workers / Schedulers

These metrics contain information about your worker and Scheduler Pods' resource usage over time. Different worker and Scheduler Pods will appear on these charts as differently colored lines.

- **CPU Usage Per Pod (%)**: This metric charts each worker/ Scheduler pod's CPU usage as a percentage of the maximum allowed CPU usage per Pod. Different worker/ Scheduler Pods will appear on this chart as differently colored lines.
- **Memory Usage Per Pod (MB)**: This metric charts each worker/ Scheduler Pod's memory usage over time. The maximum allowed memory per Pod is charted as a dotted red line. Different worker/ Scheduler Pods will appear on this chart as differently colored lines.
- **Network Usage Per Pod (MB)**: This metric charts each worker/ Scheduler Pod's network usage over time.
- **Pod Count per Status**: This metric charts the number of worker/ Scheduler Pods in a given Kubernetes container state. Because Astro operates on a one-container-per-pod model, the state of container state is also the Pod state. For more information about container states, read the [Kubernetes Documentation](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-states).
- **Scheduler Heartbeat (_Scheduler Only_)**: A Scheduler emits a heartbeat at a regular rate to signal that it's healthy to other Airflow components. This metric charts the number of Scheduler heartbeats over a given time.

    A Scheduler is considered "Unhealthy" if it has not emitted a heartbeat for over 1 minute. The lack of a Scheduler heartbeat is expected during a code push, but erratic restarts or an "Unhealthy" state that persists for a significant amount of time is worth investigating further.

### Pools

These metrics contain information about your Deployment's configured Airflow pools. They can give you insight into how your DAGs are handling concurrency.

- **Status Count for ``<pool-name>``**: This metric charts both the number of open slots in your pool and the number of tasks in each pool state:

    - **Open**: The number of available slots in the pool
    - **Queued**: The number of task instances which are occupying a pool slot and waiting to be picked up by a worker
    - **Running**: The number of tasks instances which are occupying a pool slot and running
    - **Starving**: The number of tasks that can't be scheduled when there are 0 available pool slots

## Deployment Overview

Each Deployment includes four high-level performance charts which you can view from both the **Deployments** menu and individual Deployment pages. They include:

- DAG Runs
- Task Instances
- Worker CPU
- Worker Memory

<div class="text--center">
  <img src="/img/docs/deployment-metrics.png" alt="Metrics dashboard in the Cloud UI" />
</div>

The data in these four charts is recorded hourly and is displayed in both UTC and your local browser timezone. Each bar across all graphs covers a complete hour while the entire time window for a single graph is 24 hours. For example, a single bar might represent `16:00` to `17:00` while the entire time window of the graph might represent `Nov 1 16:00` to `Nov 2 16:00`.

The data for the most recent hour is for the hour to date. For example, if you are looking at this page at 16:30, then the bar for the `16:00-17:00` hour interval would show data for `16:00-16:30`.

These charts serve as high-level reports that are intended to be viewed at a glance. For example, you might notice failed task instances in the Cloud UI and then open the Airflow UI to troubleshoot.

The following sections describe each of the 4 available charts.

### Total DAG Runs

The **DAG Runs** metric records successful and failed DAG runs over hour-long intervals. A [DAG run](https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html) is defined as an instantiation of a DAG at a specific point in time.

You can hover over each bar to see the corresponding hour interval displayed in both UTC and your local timezone. Below that, you can see the number of successful DAG runs and the number of failed DAG runs. If a bar is partially or fully red, it means that one or more DAG runs failed within that hour interval.

The bolded value above the graph denotes the total number of DAG runs that have been executed in the last 24 hours.

:::caution

The DAG runs metric does not record DAG run timeouts as failed runs. To see timed out DAG runs, you must go into the Airflow UI to check on the statuses of each DAG run there.

:::

### Task Instances

The **Tasks** chart records successful and failed task instances over hour-long intervals. A [task instance](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html#task-instances) is defined as an instantiation of a task at a specific point in time.

You can hover over each bar to see the corresponding hour interval displayed in both UTC and your local timezone. Below that, you can see the number of successful and failed task instances. If a bar is partially or fully red, it means that one or more task instances failed within that hour interval.

The bolded value above the graph denotes the total number of tasks that have run in the last 24 hours.

### Resource Usage

The **Worker CPU** and **Worker Memory** charts in the Cloud UI provide visibility into the resources being consumed by the Workers in your Deployment as measured by CPU and memory consumption.

:::info

The number of Celery workers per Deployment autoscales based on a combination of worker concurrency and the number of `running` and `queued` tasks, which means that the total available CPU and memory for a single Deployment may change at any given time.

:::

#### Worker CPU

**Worker CPU** records the peak CPU usage by worker nodes over hour-long intervals.

Each bar in the graph shows how much CPU was being used by a single worker at the height of its usage for a given hour. This value is measured as a percentage of the total available CPU usage per worker as defined in **Worker Resources**. Hovering over a single bar in the graph can help you answer, "Did any of my workers approach 100% usage of total available CPU during this specific hour interval?"

The bolded value above the graph shows maximum CPU usage by a single worker at any point in time over the last 24 hours. This can help you answer, "Did any of my workers approach 100% usage of total available CPU in the past 24 hours?"

#### Worker Memory

**Worker Memory** records the peak memory usage by worker nodes over hour-long intervals.

Each bar in the graph shows how much memory was being used by a single worker at the height of its usage for a given hour. This value is measured as a percentage of the total available memory usage per worker as defined in **Worker Resources**. Hovering over a single bar in the graph can help you answer, "Did any of my workers approach 100% usage of total available memory during this specific hour interval?"

The bolded value above the graph shows the maximum memory usage by a single worker at any point in time over the last 24 hours. This can help you answer, "Did any of my workers approach 100% usage of total available memory in the past 24 hours?"

## DAG Runs

You can view key metrics about recent DAG runs using the **DAGs** page in the Cloud UI. This page shows DAG runs from the last 14 days across either all Deployments or a specific Deployment in a Workspace. For a given DAG, the **DAGs** page shows:

- Total DAG runs over the last 14 days, expressed as a bar chart.

    Each bar in the chart represents an individual DAG run. A bar's color represents whether the DAG run was a success or a failure, while its length represents the total duration of the DAG run. If there are more than 14 DAG runs in the last 14 days, then the chart shows only the 14 most recent DAG runs.

- **Last Run End**: The ending time of the DAG's most recent DAG run, expressed relative to the current time.
- **Last Run Duration**: The duration of the DAG's most recent DAG run.
- **Average Duration**: The average Duration of all DAG runs from the last 14 days.

:::info DAG Visibility

If a DAG run for any given DAG has not run in the last 14 days, then it will not appear in the **DAGs** view.

Additionally, the `astronomer_monitoring_dag` will never appear in this view even if it ran in the last 14 days.

:::

To access the **DAGs** page, you can either click the DAGs icon in the UI or click **View DAGs** on a Deployment's information page.

![DAGs page](/img/docs/dags-page.png)

## Astro Usage

Use the **Usage** tab in the Cloud UI to review the number of successful task runs across Deployments in your Organization. Astro is priced based on successful task runs, so this view can help you monitor both Astro cost as well as Airflow usage in aggregate.

![Usage tab in the Cloud UI](/img/docs/usage.png)

The bar chart on the left shows your Organization's total task runs per day for the past 31 days, with each day's volume sorted by Deployment. Each color in the bar chart represents a different Deployment. To see each Deployment's number of successful task runs for a given day, you can hover over the bar chart for that day with your mouse.

The legend on the right side of the menu shows the colors used for each Deployment. This legend shows each Deployment's total sum of successful task runs over the last 31 days. The daily numbers on the left bar chart add up to the monthly total per Deployment on the right.

To export this data as a `.csv` file, click the **Export** button above the legend.
