---
sidebar_label: 'Scale Airflow components and resources'
title: 'Configure resources for Airflow components on Astronomer Software Deployments'
id: deployment-resources
description: Configure Deployment components to use the right amount of computational resources for your use case.
---

Use this document to configure resource usage for a Deployment's executor , webserver, scheduler and triggerer components.

## Select an executor

The Airflow [executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html) works closely with the Airflow scheduler to determine what resources complete tasks as they queue. The main difference between executors is their available resources and how they utilize those resources to distribute work.

Astronomer supports three executors:

- [Local executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/local.html)
- [Celery executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html)
- [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/kubernetes.html)

Though it largely depends on your use case, Astronomer recommends the Local executor for development environments and the Celery or Kubernetes executors for production environments operating at scale.

For a detailed description of each executor, see [Airflow executors explained](https://docs.astronomer.io/learn/airflow-executors-explained).

## Select a resource strategy

A Deployment's **Resource Strategy** defines how you can allocate CPU and memory to the Deployment's Airflow components. Astronomer Software offers two different resource strategies: **Custom Resources** and **Astronomer Units (AUs)**.

An AU is equivalent to 0.1 CPU and 0.375 GiB of memory. If you set your resource strategy to **Astronomer Units**, you can only scale components based on this resource ratio. Components must use the same AU value for both CPU and memory.

If you set your resource strategy to **Custom Resources**, you can freely set CPU and memory for each component without a predetermined ratio. See [Customize resource usage](customize-resource-usage.md).

:::info

If you still want a constant ratio of CPU to memory, but also want to change the specific ratio, you can change the amount of resources an AU represents. See [Overprovision Deployments](cluster-resource-provisioning).

:::

## Scale core resources

Apache Airflow requires four primary components:

- The Webserver
- The Scheduler
- The executor (and the workers it runs)
- The triggerer

To scale these resources, adjust the corresponding slider in the Software UI to increase its available resources. The units associated with these sliders will vary based on your [resource strategy](#select-a-resource-strategy).

Read the following sections to help you determine which core resources to scale and when.

### Airflow webserver

The Airflow webserver is responsible for rendering the [Airflow UI](https://airflow.apache.org/docs/apache-airflow/stable/ui.html), where users can monitor DAGs, view task logs, and set various non-code configurations.

If a function within the Airflow UI is slow or unavailable, Astronomer recommends increasing the resources allocated towards the webserver.

### Scheduler

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks once dependencies have been met.

If you experience delays in task execution, which you can track via the [Gantt Chart](https://airflow.apache.org/docs/apache-airflow/stable/ui.html#gantt-chart) view of the Airflow UI, Astronomer recommends increasing the resources allocated towards the scheduler.

:::tip

To set alerts that notify you via email when your Airflow scheduler is underprovisioned, configure an [Airflow alert](airflow-alerts.md).

:::

#### Scheduler count

Airflow 2.0 comes with the ability for users to run multiple schedulers concurrently to ensure high-availability, zero recovery time, and faster performance. You can provision up to 4 schedulers on any Deployment.

Each individual scheduler will be provisioned with the resources specified in **Scheduler Resources**. For example, if you set the CPU figure in **Scheduler Resources** to 5 CPUs and set **Scheduler Count** to 2, your Airflow Deployment will run with 2 Airflow schedulers using 5 CPUs each for a total of 10 CPUs.

To increase the speed at which tasks are scheduled and ensure high-availability, Astronomer recommends provisioning 2 or more Airflow schedulers for production environments.

### Triggerer

Airflow 2.2 introduces the triggerer, which is a component for running tasks with [deferrable operators](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html). Like the scheduler, the triggerer is highly-available: If a triggerer shuts down unexpectedly, the tasks it was deferring can be recovered and moved to another triggerer.

By adjusting the **Triggerer** slider in the Software UI, you can provision up to 2 triggerers on any Deployment running Airflow 2.2+. To take advantage of the Triggerer's high availability, we recommend provisioning 2 triggerers for production Deployments.

### (Kubernetes executor only) Set extra capacity

On Astronomer, resources required for the [KubernetesPodOperator](kubepodoperator.md) or the [Kubernetes Executor](kubernetes-executor.md) are set as **Extra Capacity**.

The Kubernetes executor and KubernetesPodOperator each spin up an individual Kubernetes pod for each task that needs to be executed, then spin down the pod after that task is completed.

The amount of CPU and Memory allocated to **Extra Capacity** maps to [resource quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) on the [Kubernetes Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) in which your Airflow Deployment lives on Astronomer. More specifically, **Extra Capacity** represents the maximum possible resources that could be provisioned to a pod at any given time.

Resources allocated to **Extra Capacity** do not affect scheduler or webserver performance and do not represent actual usage.

### (Celery executor only) Configure workers

To optimize for flexibility and availability, the Celery executor works with a set of independent Celery workers across that it can delegate tasks. On Astronomer, you can configure your Celery workers to fit your use case.

#### Worker count

By adjusting the **Worker Count** slider, users can provision up to 20 Celery workers on any Airflow Deployment.

Each individual worker will be provisioned with the resources specified in **Worker Resources**. If you set the CPU figure in **Worker Resources** to 5 CPUs and set **Worker Count** to 3, for example, your Airflow Deployment will run with 3 Celery workers using 5 CPUs each for a total of 15 CPUs.

#### Worker termination grace period

On Astronomer, Celery workers restart after every code deploy to your Airflow Deployment. This makes sure that workers execute with the most up-to-date code. To minimize disruption during task execution, however, Astronomer supports the ability to set a **Worker Termination Grace Period**.

If a deploy is triggered while a Celery worker is executing a task and **Worker Termination Grace Period** is set, the worker will continue to process that task up to a certain number of minutes before restarting itself. By default, the grace period is ten minutes.