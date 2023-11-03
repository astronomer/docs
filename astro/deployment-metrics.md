---
sidebar_label: 'Deployments'
title: 'View metrics for Astro Deployments'
id: deployment-metrics
---

<head>
  <meta name="description" content="Learn how to monitor Deployment performance, health, and total task volume in the Cloud UI. These metrics can help you with resource allocation and issue troubleshooting." />
  <meta name="og:description" content="Learn how to monitor Deployment performance, health, and total task volume in the Cloud UI. These metrics can help you with resource allocation and issue troubleshooting." />
</head>

The Cloud UI exposes a suite of observability metrics that show real-time data related to the performance and health of your Deployments. These metrics are a useful reference as you troubleshoot issues and can inform how you allocate resources. They can also help you estimate the cost of your Deployments. This document explains each available metric and where to find them.

To view metrics for individual DAGs, see [DAG metrics](dag-metrics.md).

## Deployment analytics

The **Overview** page contains a suite of metrics for a given Deployment. This page includes metrics that give you insight into the performance of both your data pipelines and infrastructure. Because metrics are collected in real time, you can use this page to detect irregularities in your pipelines or infrastructure as they happen.

To view metrics for a Deployment, open the Deployment in the Cloud UI, click **Overview**, then click **Get Analytics**. The following topics contain information about each available metric.

### DAG and task runs

These metrics contain information about your Deployment's DAG runs and task runs over a given period of time.

![DAG run analytics in the Cloud UI](/img/docs/analytics-dag-task-runs.png)

#### Available metrics

- **DAG/ Task Runs**: This metric graphs the total number of DAG/ task runs.
- **Runs per Status**: This metric graphs the number of failed and successful DAG/ task runs, plotted based on the DAG/ task run start time. Use this metric to see exactly when recent DAG/ task runs succeeded or failed.

  :::caution

  The DAG runs metric does not record DAG run timeouts as failed runs. To see timed out DAG runs, you must go into the Airflow UI to check on the statuses of each DAG run there.

  :::

- **P90 Run Duration per Status**: This metric graphs the 90th percentile of execution times for DAG/ task runs, plotted based on the DAG/ task run start time. In the example above, the P90 Run Duration per Status for successful DAG/ task runs at 5:00 was 34 seconds, which means that 90% of those DAG/ task runs finished in 34 seconds or less.

    This metric can both help you understand how your pipelines are performing overall, as well as identify DAG/ task runs that didn't result in a failure but still took longer to run than expected.

### Airflow workers and schedulers

These metrics contain information about the Kubernetes Pods running your workers and schedulers. Different worker and scheduler Pods will appear on these charts as differently colored lines. 

Hover over the graph to view a graph legend. If a given worker queue spins a worker down and back up again within a given interval, the newly spun up worker appears as a new color on the graph. 

![Worker analytics in the Cloud UI](/img/docs/analytics-workers.png)

#### Available metrics

- **CPU Usage Per Pod (%)**: This metric graphs the peak CPU usage for all workers and schedulers for a given interval. Different worker and scheduler Pods appear as differently colored lines on this chart. For scheduler metrics, the maximum allowable CPU for each scheduler Pod appears as a dotted red line.

    The percentage value is proportional to the usage of a single CPU core by a worker Pod. For this reason, the utilization percentage value for a worker Pod with multiple CPU cores can be greater than 100%. For example, because the maximum utilization percentage value for a single CPU core is 100%, the utilization percentage value for a worker Pod with four assigned CPU cores can be as much as 400%. 

- **Memory Usage Per Pod (MB)**: This metric graphs the peak memory usage for all workers and schedulers for a given interval. Different worker and scheduler Pods will appear as differently colored lines on this chart. This metric should be at or below 50% of your total allowed memory at any given time. For scheduler metrics, the maximum allowable memory for each scheduler Pod appears as a dotted red line.

:::info

  The number of workers per Deployment autoscales based on a combination of worker concurrency and the number of `running` and `queued` tasks. This means that the total available CPU and memory for a single Deployment may change at any time.

:::


- **Network Usage Per Pod (MB)**: This metric graphs each worker/ scheduler Pod's peak network usage over time. Sudden, irregular spikes in this metric should be investigated as a possible error in your project code.
- **Pod Count per Status**: This metric graphs the number of worker/ scheduler Pods in a given Kubernetes container state. Because Astro operates on a one-container-per-pod model, the state of the container state is also the Pod state. For more information about container states, read the [Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-states).

    If a pod is stuck in a `Waiting` state, it could indicate that your Deployment did not successfully pull and run your Runtime image.

- **Scheduler Heartbeat (_Scheduler Only_)**: A scheduler emits a heartbeat at a regular rate to signal that it's healthy to other Airflow components. This metric graphs a scheduler's average heartbeats per minute over a given time.

   On average, a scheduler should emit ~11-12 heartbeats per minute. A scheduler is considered "unhealthy" if it has not emitted a heartbeat for over 1 minute. The lack of a scheduler heartbeat is expected during a code push, but erratic restarts or an "Unhealthy" state that persists for a significant amount of time is worth investigating further.

### Pools

These metrics contain information about your Deployment's configured [Airflow pools](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html). They can give you insight into how your DAGs are handling concurrency.

![Pool analytics in the Cloud UI](/img/docs/analytics-pools.png)

#### Available metrics

- **Status Count for `<pool-name>`**: This metric graphs both the number of open slots in your pool and the number of tasks in each pool state:

    - **Open**: The number of available slots in the pool
    - **Queued**: The number of task instances which are occupying a pool slot and waiting to be picked up by a worker
    - **Running**: The number of tasks instances which are occupying a pool slot and running
    - **Starving**: The number of tasks that can't be scheduled when there are 0 available pool slots

    A large number of starving tasks could indicate that you should reconfigure your pools to run more tasks in parallel.

## Deployment health

After you create a Deployment, its real-time health status appears at the top of the Deployment information page. Deployment health indicates if the components within your Deployment are running as expected.

![Deployment Health status](/img/docs/deployment-health.png)

The following are the possible Deployment health statuses:

- **Creating** (Grey): Astro is still provisioning Deployment resources. It is not yet available to run DAGs. See [Create a Deployment](create-deployment.md).
- **Deploying** (Grey): A code deploy is in progress. Hover over the status indicator to view specific information about the deploy, including whether it was an image deploy or a DAG-only deploy.
- **Healthy** (Green): The Airflow webserver and scheduler are both healthy and running as expected.
- **Unhealthy** (Red): Your Deployment webserver or scheduler are restarting or otherwise not in a healthy, running state.
- **Unknown** (Grey): The Deployment status can't be determined.

If your Deployment is unhealthy or the status can't be determined, check the status of your tasks and wait for a few minutes. If your Deployment is unhealthy for more than five minutes, review the logs in the [Airflow component logs](view-logs.md#view-airflow-component-logs-in-the-cloud-ui) in the Cloud UI or contact [Astronomer support](https://cloud.astronomer.io/support).

## Deployment overview

Each Deployment includes four high-level performance charts about the `default` worker queue which you can view from both the **Deployments** menu and a Deployment's **Overview** page. They include:

- DAG runs
- Task Instances
- Worker CPU
- Worker Memory

![Metrics dashboard in the Cloud UI](/img/docs/deployment-metrics.png)

The data in these four charts is recorded hourly and is displayed in both UTC and your local browser timezone. Each bar across all graphs covers a complete hour while the entire time window for a single graph is 24 hours. For example, a single bar might represent `16:00` to `17:00` while the entire time window of the graph might represent `Nov 1 16:00` to `Nov 2 16:00`.

The data for the most recent hour is for the hour to date. For example, if you are looking at this page at 16:30, then the bar for the `16:00-17:00` hour interval would show data for `16:00-16:30`.

These charts serve as high-level reports for your `default` worker queue that you can investigate further.

The following sections describe each of the 4 available charts.

### Total DAG runs

The **DAG Runs** metric records successful and failed DAG runs over hour-long intervals. A [DAG run](https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html) is defined as an instantiation of a DAG at a specific point in time.

You can hover over each bar to see the corresponding hour interval displayed in both UTC and your local timezone. Below that, you can see the number of successful DAG runs and the number of failed DAG runs. If a bar is partially or fully red, it means that one or more DAG runs failed within that hour interval.

The bolded value above the graph denotes the total number of DAG runs that have been executed in the last 24 hours.

### Task instances

The **Tasks** chart records successful and failed task instances over hour-long intervals. A [task instance](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#task-instances) is defined as an instantiation of a task at a specific point in time.

You can hover over each bar to see the corresponding hour interval displayed in both UTC and your local timezone. Below that, you can see the number of successful and failed task instances. If a bar is partially or fully red, it means that one or more task instances failed within that hour interval.

The bolded value above the graph denotes the total number of tasks that have run in the last 24 hours.

### Resource usage

The **Worker CPU** and **Worker Memory** charts in the Cloud UI provide visibility into the resources being consumed by the workers in your Deployment as measured by CPU and memory consumption.

**Worker CPU** records the peak CPU usage, while **Worker Memory** records the peak memory usage by worker nodes over hour-long intervals. The bolded values above each graph show the maximum CPU/ memory usage by a single worker at any point in time over the last 24 hours.

:::info

 A known issue with Celery might cause worker memory allocation to increase without a corresponding increase in task count or DAG memory use. To correct this issue, redeploy your code without making any changes to restart the Celery worker and reset memory requests. See [Deploy code to Astro](deploy-code.md). This issue should not affect your tasks or cause OutOfMemory (OOM) errors. If you experience complications, contact Astronomer Support.

:::

## See also

- [Organization metrics](organization-metrics.md)
- [Export task logs and metrics to Datadog](export-datadog.md)
- [Export task logs to AWS Cloudwatch](export-cloudwatch.md)