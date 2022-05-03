---
sidebar_label: 'Deployment Metrics'
title: 'Deployment Metrics'
id: deployment-metrics
description: Monitor Deployment performance, health, and total task volume in the Cloud UI.
---

## Overview

The Cloud UI exposes a suite of observability metrics that show real-time data related to the performance and health of your Deployments. These metrics are a useful reference as you troubleshoot issues and can inform how you allocate resources. They can also help you estimate the cost of your Deployments. This document explains each available metric and where to find them.

## Deployment Analytics

Located in the Workspace view of the Cloud UI, the **Analytics** page contains a suite of metrics for your Deployments. This page includes metrics that give you insight into the performance of both your data pipelines and infrastructure. Because metrics are collected in real time, you can use this page to detect irregularities in your pipelines or infrastructure as they happen.

To view metrics for a given Deployment, click the **Analytics** button in the left-hand menu. From here, you can select a Deployment and a time range for your metrics:

![Analytics menu location](/img/docs/access-analytics.png)

You can also access analytics for a specific Deployment from the Deployment's page:

![Analytics menu location](/img/docs/access-analytics-deployments.png)

The following topics contain information about each available metric.

### DAG Runs / Task Runs

These metrics contain information about your Deployment's DAG runs and task runs over a given period of time.

![DAG run analytics in the Cloud UI](/img/docs/analytics-dag-task-runs.png)

#### Available Metrics

- **DAG/ Task Runs**: This metric graphs the total number of DAG/ task runs.
- **Runs per Status**: This metric graphs the number of failed and successful DAG/ task runs, plotted based on the DAG/ task run start time. Use this metric to see exactly when recent DAG/ task runs succeeded or failed.

  :::caution

  The DAG runs metric does not record DAG run timeouts as failed runs. To see timed out DAG runs, you must go into the Airflow UI to check on the statuses of each DAG run there.

  :::

- **P90 Run Duration per Status**: This metric graphs the 90th percentile of execution times for DAG/ task runs, plotted based on the DAG/ task run start time. In the example above, the P90 Run Duration per Status for successful DAG/ task runs at 5:00 was 34 seconds, which means that 90% of those DAG/ task runs finished in 34 seconds or less.

    This metric can both help you understand how your pipelines are performing overall, as well as identify DAG/ task runs that didn't result in a failure but still took longer to run than expected.

### Workers / Schedulers

These metrics contain information about the Kubernetes Pods running your workers and Schedulers. Different worker and Scheduler Pods will appear on these charts as differently colored lines.

![Worker analytics in the Cloud UI](/img/docs/analytics-workers.png)

#### Available Metrics

- **CPU Usage Per Pod (%)**: This metric graphs a worker's peak CPU usage over a given time interval. The maximum allowed CPUs per Pod as defined in **Worker Resources** appears as a dotted red line. Different worker/ Scheduler Pods will appear on this chart as differently colored lines.

    This metric should be at or below 90% at any given time. If a Pod surpasses 90% usage, the line in the graph will turn red.  

- **Memory Usage Per Pod (MB)**: This metric graphs a worker's peak memory usage over a given time interval. The maximum allowed memory per Pod as defined in **Worker Resources** appears as a dotted red line. Different worker/ Scheduler Pods will appear on this chart as differently colored lines. This metric should be at or below 50% of your total allowed memory at any given time.

    This metric should be at or below 90% at any given time. If a Pod surpasses 90% usage, the line in the graph will turn red.  

  :::info

  The number of Celery workers per Deployment autoscales based on a combination of worker concurrency and the number of `running` and `queued` tasks, which means that the total available CPU and memory for a single Deployment may change at any given time.

  :::

- **Network Usage Per Pod (MB)**: This metric graphs each worker/ Scheduler Pod's peak network usage over time. Sudden, irregular spikes in this metric should be investigated as a possible error in your project code.
- **Pod Count per Status**: This metric graphs the number of worker/ Scheduler Pods in a given Kubernetes container state. Because Astro operates on a one-container-per-pod model, the state of the container state is also the Pod state. For more information about container states, read the [Kubernetes Documentation](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-states).

    If a pod is stuck in a `Waiting` state, it could indicate that your Deployment did not successfully pull and run your Runtime image.

- **Scheduler Heartbeat (_Scheduler Only_)**: A Scheduler emits a heartbeat at a regular rate to signal that it's healthy to other Airflow components. This metric graphs a Scheduler's average heartbeats per minute over a given time.

   On average, a Scheduler should emit ~11-12 heartbeats per minute. A Scheduler is considered "unhealthy" if it has not emitted a heartbeat for over 1 minute. The lack of a Scheduler heartbeat is expected during a code push, but erratic restarts or an "Unhealthy" state that persists for a significant amount of time is worth investigating further.

### Pools

These metrics contain information about your Deployment's configured [Airflow pools](https://airflow.apache.org/docs/apache-airflow/stable/concepts/pools.html). They can give you insight into how your DAGs are handling concurrency.

![Pool analytics in the Cloud UI](/img/docs/analytics-pools.png)

#### Available Metrics

- **Status Count for `<pool-name>`**: This metric graphs both the number of open slots in your pool and the number of tasks in each pool state:

    - **Open**: The number of available slots in the pool
    - **Queued**: The number of task instances which are occupying a pool slot and waiting to be picked up by a worker
    - **Running**: The number of tasks instances which are occupying a pool slot and running
    - **Starving**: The number of tasks that can't be scheduled when there are 0 available pool slots

    A large number of starving tasks could indicate that you should reconfigure your pools to run more tasks in parallel.

## Deployment Health

Deployment health appears as a real-time status at the top of your Deployment's information page. Deployment health is meant to show whether or not the most important components within your Deployment are running as expected.

![Deployment Health status](/img/docs/deployment-health.png)

Deployment health can have one of two statuses:

- **Healthy** (Green): The Airflow Webserver and Scheduler are both healthy and running as expected.
- **Unhealthy** (Red): This status can mean one of two things:

    - Your Deployment was recently created and the Airflow Webserver and Scheduler are still spinning up.
    - Your Deployment's Webserver and/or Scheduler are restarting or otherwise not in a healthy, running state.

If your Deployment is unhealthy, we recommend checking the status of your tasks and waiting for a few minutes. If your Deployment is unhealthy for more than 5 minutes, we recommend [reviewing Scheduler logs](scheduler-logs.md) in the Cloud UI or reaching out to [Astronomer Support](https://support.astronomer.io).

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

These charts show the same data that's available from the **Analytics** page. They serve as high-level reports that are intended to be viewed at a glance. For example, you might notice failed task instances in the Cloud UI and then open the **Analytics** page to investigate further.

The following sections describe each of the 4 available charts.

### Total DAG Runs

The **DAG Runs** metric records successful and failed DAG runs over hour-long intervals. A [DAG run](https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html) is defined as an instantiation of a DAG at a specific point in time.

You can hover over each bar to see the corresponding hour interval displayed in both UTC and your local timezone. Below that, you can see the number of successful DAG runs and the number of failed DAG runs. If a bar is partially or fully red, it means that one or more DAG runs failed within that hour interval.

The bolded value above the graph denotes the total number of DAG runs that have been executed in the last 24 hours.

### Task Instances

The **Tasks** chart records successful and failed task instances over hour-long intervals. A [task instance](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html#task-instances) is defined as an instantiation of a task at a specific point in time.

You can hover over each bar to see the corresponding hour interval displayed in both UTC and your local timezone. Below that, you can see the number of successful and failed task instances. If a bar is partially or fully red, it means that one or more task instances failed within that hour interval.

The bolded value above the graph denotes the total number of tasks that have run in the last 24 hours.

### Resource Usage

The **Worker CPU** and **Worker Memory** charts in the Cloud UI provide visibility into the resources being consumed by the Workers in your Deployment as measured by CPU and memory consumption.

**Worker CPU** records the peak CPU usage, while **Worker Memory** records the peak memory usage by worker nodes over hour-long intervals. The bolded values above each graph show the maximum CPU/ memory usage by a single worker at any point in time over the last 24 hours.

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
