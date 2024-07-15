---
sidebar_label: 'Configure a Deployment'
title: 'Configure a Deployment on Astronomer Software'
id: configure-deployment
---

## Overview

An Apache Airflow® Deployment on Astronomer is an instance of Apache Airflow that was created either via the Software UI or the Astronomer CLI. Each Airflow Deployment on Astronomer is hosted on a single Kubernetes namespace, has a dedicated set of resources, and operates with an isolated Postgres Metadata Database.

This guide walks you through the process of creating and configuring an Airflow Deployment on Astronomer.

## Prerequisites

To create an Airflow Deployment, you'll need:
* [The Astronomer CLI](cli-quickstart.md) installed.
* An Astronomer platform at `app.BASEDOMAIN`.
* An Astronomer [Workspace](manage-workspaces.md).

## Create a Deployment

To create an Airflow Deployment on Astronomer:

1. Log in to your Astronomer platform at `app.BASEDOMAIN`, open your Workspace, and click **New Deployment**.
2. Use the **New Deployment** menu to configure the following:

    - **Name**
    - **Description** (Optional)
    - **Airflow Version**: We recommend using the latest version.
    - **Executor**: We recommend starting with Local.

3. Click **Create Deployment** and give the Deployment a few moments to spin up. Within a few seconds, you'll have access to the **Settings** page of your new Deployment:

   ![New Deployment Celery Dashboard](/img/software/v0.23-new_deployment-dashboard.png)

This tab is the best place to modify resources for your Deployment. Specifically, you can:

- Select an Airflow Executor
- Allocate resources to your Airflow Scheduler and Webserver
- Set Scheduler Count (*Airflow 2.0+ only*)
- Add Extra Capacity (*Kubernetes only*)
- Set Worker Count (*Celery only*)
- Adjust your Worker Termination Grace Period (*Celery only*)

The rest of this guide provides additional guidance for configuring each of these settings.

## Select an Executor

The Airflow [Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html) works closely with the Airflow Scheduler to decide what resources will complete tasks as they're queued. The difference between Executors comes down to their available resources and how they utilize those resources to distribute work.

Astronomer supports 3 Executors:

- [Local Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/local.html)
- [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html)
- [Kubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/kubernetes.html)

Though it largely depends on your use case, we recommend the Local Executor for development environments and the Celery or Kubernetes Executors for production environments operating at scale.

For a detailed breakdown of each Executor, read Astronomer's [Airflow Executors Explained](https://www.astronomer.io/guides/airflow-executors-explained).

## Scale Core Resources

Apache Airflow requires two primary components:

- The Airflow Webserver
- The Airflow Scheduler

To scale either resource, simply adjust the corresponding slider in the Software UI to increase its available computing power.

Read the following sections to help you determine which core resources to scale and when.

### Apache Airflow® Webserver

The Airflow Webserver is responsible for rendering the [Airflow UI](https://airflow.apache.org/docs/apache-airflow/stable/ui.html), where users can monitor DAGs, view task logs, and set various non-code configurations.

If a function within the Airflow UI is slow or unavailable, we recommend increasing the AU allocated towards the Webserver. The default resource allocation is 5 AU.

> **Note:** Introduced in Apache Airflow® 1.10.7, [DAG Serialization](https://airflow.apache.org/docs/apache-airflow/stable/dag-serialization.html?highlight=dag%20serialization) removes the need for the Webserver to regularly parse all DAG files, making the component significantly more light-weight and performant. DAG Serialization is enabled by default in Airflow 1.10.12+ and is required in Airflow 2.0.

### Apache Airflow® Scheduler

The [Airflow Scheduler](https://airflow.apache.org/docs/apache-airflow/stable/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks once dependencies have been met.

If you experience delays in task execution, which you can track via the [Gantt Chart](https://airflow.apache.org/docs/apache-airflow/stable/ui.html#gantt-chart) view of the Airflow UI, we recommend increasing the AU allocated towards the Scheduler. The default resource allocation is 10 AU.

> **Tip:** To set alerts that notify you via email when your Airflow Scheduler is underprovisioned, refer to [Airflow Alerts](airflow-alerts.md).

#### Scheduler Count

Airflow 2.0 comes with the ability for users to run multiple Schedulers concurrently to ensure high-availability, zero recovery time, and faster performance. By adjusting the **Scheduler Count** slider in the Software UI, you can provision up to 4 Schedulers on any Deployment running Airflow 2.0+ on Astronomer.

Each individual Scheduler will be provisioned with the AU specified in **Scheduler Resources**. For example, if you set **Scheduler Resources** to 10 AU and **Scheduler Count** to 2, your Airflow Deployment will run with 2 Airflow Schedulers using 10 AU each for a total of 20 AU.

To increase the speed at which tasks are scheduled and ensure high-availability, we recommend provisioning 2 or more Airflow Schedulers for production environments. For more information on the Airflow 2.0 Scheduler, refer to Astronomer's ["The Airflow 2.0 Scheduler" blog post](https://www.astronomer.io/blog/airflow-2-scheduler).

## Kubernetes Executor: Set Extra Capacity

On Astronomer, resources required for the [KubernetesPodOperator](kubepodoperator.md) or the [Kubernetes Executor](kubernetes-executor.md) are set as **Extra Capacity**.

The Kubernetes Executor and KubernetesPodOperator each spin up an individual Kubernetes pod for each task that needs to be executed, then spin down the pod once that task is completed.

The amount of AU (CPU and Memory) allocated to **Extra Capacity** maps to [resource quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) on the [Kubernetes Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) in which your Airflow Deployment lives on Astronomer. More specifically, **Extra Capacity** represents the maximum possible resources that could be provisioned to a pod at any given time.

AU allocated to **Extra Capacity** does not affect Scheduler or Webserver performance and does not represent actual usage. It will not be charged as a fixed resource.

## Celery Executor: Configure Workers

To optimize for flexibility and availability, the Celery Executor works with a set of independent Celery Workers across which it can delegate tasks. On Astronomer, you're free to configure your Celery Workers to fit your use case.

### Worker Count

By adjusting the **Worker Count** slider, users can provision up to 20 Celery Workers on any Airflow Deployment.

Each individual Worker will be provisioned with the AU specified in **Worker Resources**. If you set **Worker Resources** to 10 AU and **Worker Count** to 3, for example, your Airflow Deployment will run with 3 Celery Workers using 10 AU each for a total of 30 AU. **Worker Resources** has a maximum of 100 AU (10 CPU, 37.5 GB Memory).

### Worker Termination Grace Period

On Astronomer, Celery Workers restart following every code deploy to your Airflow Deployment. This is to make sure that Workers are executing with the most up-to-date code. To minimize disruption during task execution, however, Astronomer supports the ability to set a **Worker Termination Grace Period**.

If a deploy is triggered while a Celery Worker is executing a task and **Worker Termination Grace Period** is set, the Worker will continue to process that task up to a certain number of minutes before restarting itself. By default, the grace period is ten minutes.

> **Tip:** The **Worker Termination Grace Period** is an advantage to the Celery Executor. If your Airflow Deployment runs on the Local Executor, the Scheduler will restart immediately upon every code deploy or configuration change and potentially interrupt task execution.

## Set Environment Variables

Environment Variables can be used to set [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) and custom values, both of which can be applied to your Airflow Deployment either locally or on Astronomer.

These can include setting Airflow Parallelism, an SMTP service for Alerts, or a [secrets backend](secrets-backend.md) to manage Airflow Connections and Variables.

Environment Variables can be set for your Airflow Deployment either in the **Variables** tab of the Software UI or in your `Dockerfile`. If you're developing locally, they can also be added to a local `.env` file. For more information on configuring Environment Variables, read [Environment Variables on Astronomer](environment-variables.md).

> **Note**: Environment Variables are distinct from [Airflow Variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html?highlight=variables) and [XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html), which you can configure directly via the Airflow UI and are used for inter-task communication.

## Customize Release Names

An Airflow Deployment's release name on Astronomer is a unique, immutable identifier for that Deployment that corresponds to its Kubernetes namespace and that renders in Grafana, Kibana, and other platform-level monitoring tools. By default, release names are randomly generated in the following format: `noun-noun-<4-digit-number>`. For example: `elementary-zenith-7243`.

To customize the release name for a Deployment as you're creating it, you first need to enable the feature on your Astronomer platform. To do so, set the following value in your `config.yaml` file:

```yaml
astronomer:
  houston:
    config:
      deployments:
        manualReleaseNames: true # Allows you to set your release names
```

Then, push the updated `config.yaml` file to your installation as described in [Apply a Config Change](apply-platform-config.md).

After applying this change, the **Release Name** field in the Software UI becomes configurable:

![Custom Release Name Field](/img/software/custom-release-name.png)

## DAG Deploy Mechanisms

You can use two different DAG deploy mechanisms on Astronomer:

- Image-based deploys
- NFS volume-based deploys

### Image-based deploys

By default, you can deploy DAGs to an Airflow Deployment by building them into a Docker image and pushing that image to the Astronomer Registry via the CLI or API. This workflow is described in [Deploy DAGs via the CLI](deploy-cli.md).

This mechanism builds your DAGs into a Docker image alongside all other files in your Airflow project directory, including your Python and OS-level packages, your Dockerfile, and your plugins.

The resulting image is then used to generate a set of Docker containers for each of Airflow's core components. Every time you run `astro deploy` via the Astronomer CLI, your DAGs are rebuilt into a new Docker image and all Docker containers are restarted.

Since the image-based deploy does not require additional setup, we recommend it for those getting started with Airflow.

### Volume-based deploys

For advanced teams who deploy DAG changes more frequently, Astronomer also supports an [NFS volume-based](https://kubernetes.io/docs/concepts/storage/volumes/#nfs) deploy mechanism.

Using this mechanism, you can deploy DAGs to an Airflow Deployment on Astronomer by adding the corresponding Python files to a shared file system on your network. Compared to image-based deploys, NFS volume-based deploys limit downtime and enable continuous deployment.

To deploy DAGs to a Deployment via an NFS volume, you must first enable the feature at the platform level. For more information, read [Deploy DAGs via NFS Volume](deploy-nfs.md).

## Delete a Deployment

You can delete an Airflow Deployment using the **Delete Deployment** button at the bottom of the Deployment's **Settings** tab.

When you delete a Deployment, your Airflow Webserver, Scheduler, metadata database, and deploy history will be deleted, and you will lose any configurations set in the Airflow UI.

In your Astronomer database, the corresponding `Deployment` record will be given a `deletedAt` value and continue to persist until permanently deleted.

### Hard delete a Deployment

> **Note:** This feature must first be enabled at the platform level before it can be used. To enable this feature, set `astronomer.houston.config.deployments.hardDeleteDeployment: true` in your `config.yaml` file and push the changes to your platform as described in [Apply a Config Change](apply-platform-config.md).

To reuse a custom release name given to an existing Deployment, you need to first hard delete both the Deployment's metadata database and the Deployment's entry in your Astronomer database. To do so, select the **Hard Delete?** checkbox before clicking **Delete Deployment**. Alternatively, you can run `astro deployment delete --hard` via the Astronomer CLI.

![Hard delete checkbox](/img/software/hard-delete.png)

This action permanently deletes all data associated with a Deployment, including the database and underlying Kubernetes resources.
