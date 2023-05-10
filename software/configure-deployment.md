---
sidebar_label: 'Configure a Deployment'
title: 'Configure a Deployment on Astronomer Software'
id: configure-deployment
description: Configure your Airflow Deployment's resources on Astronomer Software.
---

An Airflow Deployment on Astronomer is an instance of Apache Airflow that was created using the Software UI or the Astro CLI. Each Airflow Deployment on Astronomer is hosted on a single Kubernetes namespace, has a dedicated set of resources, and operates with an isolated Postgres metadata database.

This guide walks you through the process of creating and configuring an Airflow Deployment on Astronomer.

## Prerequisites

To create an Airflow Deployment, you'll need:
* [The Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) installed.
* An Astronomer platform at `app.BASEDOMAIN`.
* An Astronomer [Workspace](manage-workspaces.md).

## Create a Deployment

To create an Airflow Deployment on Astronomer:

1. Log in to your Astronomer platform at `app.BASEDOMAIN`, select a Workspace, and then click **New Deployment**.
2. Complete the following fields:

    - **Name**: Enter a descriptive name for the Deployment.
    - **Description**: (Optional)
    - **Airflow Version**: Astronomer recommends using the latest version.
    - **Executor**: Astronomer recommends starting with Local.

3. Click **Create Deployment** and give the Deployment a few moments to be created. After the Deployment is created, you'll be able to access the **Settings** page of your new Deployment:

   ![New Deployment Celery Dashboard](/img/software/v0.23-new_deployment-dashboard.png)

    On this tab you can modify resources for your Deployment. Specifically, you can:

    - Select an Airflow executor
    - Allocate resources to your Airflow scheduler and webserver
    - Set scheduler count (*Airflow 2.0+ only*)
    - Add extra capacity (*Kubernetes only*)
    - Set worker count (*Celery only*)
    - Adjust your worker termination grace period (*Celery only*)

## Select an executor

The Airflow [executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html) works closely with the Airflow scheduler to decide what resources will complete tasks as they're queued. The difference between executors comes down to their available resources and how they utilize those resources to distribute work.

Astronomer supports 3 executors:

- [Local executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/local.html)
- [Celery executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html)
- [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/kubernetes.html)

Though it largely depends on your use case, we recommend the Local executor for development environments and the Celery or Kubernetes executors for production environments operating at scale.

For a detailed breakdown of each executor, see [Airflow executors explained](https://docs.astronomer.io/learn/airflow-executors-explained).

## Scale core resources

Apache Airflow requires two primary components:

- The Airflow Webserver
- The Airflow Scheduler

To scale either resource, simply adjust the corresponding slider in the Software UI to increase its available computing power.

Read the following sections to help you determine which core resources to scale and when.

### Airflow webserver

The Airflow webserver is responsible for rendering the [Airflow UI](https://airflow.apache.org/docs/apache-airflow/stable/ui.html), where users can monitor DAGs, view task logs, and set various non-code configurations.

If a function within the Airflow UI is slow or unavailable, we recommend increasing the AU allocated towards the webserver. The default resource allocation is 5 AU.

> **Note:** Introduced in Airflow 1.10.7, [DAG Serialization](https://airflow.apache.org/docs/apache-airflow/stable/dag-serialization.html?highlight=dag%20serialization) removes the need for the webserver to regularly parse all DAG files, making the component significantly more light-weight and performant. DAG Serialization is enabled by default in Airflow 1.10.12+ and is required in Airflow 2.0.

### Airflow scheduler

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks once dependencies have been met.

If you experience delays in task execution, which you can track via the [Gantt Chart](https://airflow.apache.org/docs/apache-airflow/stable/ui.html#gantt-chart) view of the Airflow UI, we recommend increasing the AU allocated towards the scheduler. The default resource allocation is 10 AU.

> **Tip:** To set alerts that notify you via email when your Airflow scheduler is underprovisioned, refer to [Airflow alerts](airflow-alerts.md).

#### Scheduler count

Airflow 2.0 comes with the ability for users to run multiple schedulers concurrently to ensure high-availability, zero recovery time, and faster performance. By adjusting the **Scheduler Count** slider in the Software UI, you can provision up to 4 schedulers on any Deployment running Airflow 2.0+ on Astronomer.

Each individual scheduler will be provisioned with the AU specified in **Scheduler Resources**. For example, if you set **Scheduler Resources** to 10 AU and **Scheduler Count** to 2, your Airflow Deployment will run with 2 Airflow schedulers using 10 AU each for a total of 20 AU.

To increase the speed at which tasks are scheduled and ensure high-availability, we recommend provisioning 2 or more Airflow schedulers for production environments. For more information on the Airflow 2.0 scheduler, refer to Astronomer's ["The Airflow 2.0 Scheduler" blog post](https://www.astronomer.io/blog/airflow-2-scheduler).

### Triggerer

Airflow 2.2 introduces the triggerer, which is a component for running tasks with [deferrable operators](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html). Like the scheduler, the triggerer is highly-available: If a triggerer shuts down unexpectedly, the tasks it was deferring can be recovered and moved to another triggerer.

By adjusting the **Triggerer** slider in the Software UI, you can provision up to 2 triggerers on any Deployment running Airflow 2.2+. To take advantage of the Triggerer's high availability, we recommend provisioning 2 triggerers for production Deployments.

## Kubernetes executor: Set extra capacity

On Astronomer, resources required for the [KubernetesPodOperator](kubepodoperator.md) or the [Kubernetes Executor](kubernetes-executor.md) are set as **Extra Capacity**.

The Kubernetes executor and KubernetesPodOperator each spin up an individual Kubernetes pod for each task that needs to be executed, then spin down the pod once that task is completed.

The amount of AU (CPU and Memory) allocated to **Extra Capacity** maps to [resource quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) on the [Kubernetes Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) in which your Airflow Deployment lives on Astronomer. More specifically, **Extra Capacity** represents the maximum possible resources that could be provisioned to a pod at any given time.

AU allocated to **Extra Capacity** does not affect scheduler or webserver performance and does not represent actual usage. It will not be charged as a fixed resource.

## Celery executor: Configure workers

To optimize for flexibility and availability, the Celery executor works with a set of independent Celery workers across which it can delegate tasks. On Astronomer, you're free to configure your Celery workers to fit your use case.

### Worker count

By adjusting the **Worker Count** slider, users can provision up to 20 Celery workers on any Airflow Deployment.

Each individual worker will be provisioned with the AU specified in **Worker Resources**. If you set **Worker Resources** to 10 AU and **Worker Count** to 3, for example, your Airflow Deployment will run with 3 Celery workers using 10 AU each for a total of 30 AU. **Worker Resources** has a maximum of 100 AU (10 CPU, 37.5 GB Memory).

### Worker termination grace period

On Astronomer, Celery workers restart following every code deploy to your Airflow Deployment. This is to make sure that workers are executing with the most up-to-date code. To minimize disruption during task execution, however, Astronomer supports the ability to set a **Worker Termination Grace Period**.

If a deploy is triggered while a Celery worker is executing a task and **Worker Termination Grace Period** is set, the worker will continue to process that task up to a certain number of minutes before restarting itself. By default, the grace period is ten minutes.

> **Tip:** The **Worker Termination Grace Period** is an advantage to the Celery executor. If your Airflow Deployment runs on the Local executor, the scheduler will restart immediately upon every code deploy or configuration change and potentially interrupt task execution.

## Set environment variables

Environment variables can be used to set [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) and custom values, both of which can be applied to your Airflow Deployment either locally or on Astronomer.

These can include setting Airflow Parallelism, an SMTP service for alerts, or a [secrets backend](secrets-backend.md) to manage Airflow connections and variables.

Environment variables can be set for your Airflow Deployment either in the **Variables** tab of the Software UI or in your `Dockerfile`. If you're developing locally, they can also be added to a local `.env` file. For more information on configuring environment variables, read [Environment variables on Astronomer](environment-variables.md).

> **Note**: Environment variables are distinct from [Airflow variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html?highlight=variables) and [XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html), which you can configure directly via the Airflow UI and are used for inter-task communication.

## Customize release names

An Airflow Deployment's release name on Astronomer is a unique, immutable identifier for that Deployment that corresponds to its Kubernetes namespace and that renders in Grafana, Kibana, and other platform-level monitoring tools. By default, release names are randomly generated in the following format: `noun-noun-<4-digit-number>`. For example: `elementary-zenith-7243`.

To customize the release name for a Deployment as you're creating it, you first need to enable the feature on your Astronomer platform. To do so, set the following value in your `config.yaml` file:

```yaml
astronomer:
  houston:
    config:
      deployments:
        manualReleaseNames: true # Allows you to set your release names
```

Then, push the updated `config.yaml` file to your installation as described in [Apply a config change](apply-platform-config.md).

After applying this change, the **Release Name** field in the Software UI becomes configurable:

![Custom Release Name Field](/img/software/custom-release-name.png)

## DAG deploy mechanisms

You can use two different DAG deploy mechanisms on Astronomer:

- Image-based deploys
- NFS volume-based deploys

### Image-based deploys

By default, you can deploy DAGs to an Airflow Deployment by building them into a Docker image and pushing that image to the Astronomer Registry via the CLI or API. This workflow is described in [Deploy DAGs via the CLI](deploy-cli.md).

This mechanism builds your DAGs into a Docker image alongside all other files in your Astro project directory, including your Python and OS-level packages, your Dockerfile, and your plugins.

The resulting image is then used to generate a set of Docker containers for each of Airflow's core components. Every time you run `astro deploy` in the Astro CLI, your DAGs are rebuilt into a new Docker image and all Docker containers are restarted.

Since the image-based deploy does not require additional setup, we recommend it for those getting started with Airflow.

### Volume-based deploys

For advanced teams who deploy DAG changes more frequently, Astronomer also supports an [NFS volume-based](https://kubernetes.io/docs/concepts/storage/volumes/#nfs) deploy mechanism.

Using this mechanism, you can deploy DAGs to an Airflow Deployment on Astronomer by adding the corresponding Python files to a shared file system on your network. Compared to image-based deploys, NFS volume-based deploys limit downtime and enable continuous deployment.

To deploy DAGs to a Deployment via an NFS volume, you must first enable the feature at the platform level. For more information, read [Deploy DAGs via NFS volume](deploy-nfs.md).

### Git-sync deploys

For teams using a Git-based workflow for DAG development, Astronomer supports a [git-sync](https://github.com/kubernetes/git-sync) deploy mechanism.

To deploy DAGs via git-sync, you add DAGs to a repository that has been configured to sync with your Astronomer Deployment. Once the Deployment detects a change in the repository, your DAG code will automatically sync to your Deployment with no downtime. For more information on configuring this feature, read [Deploy DAGs via git sync](deploy-git-sync.md).

## Delete a Deployment

You can delete an Airflow Deployment using the **Delete Deployment** button at the bottom of the Deployment's **Settings** tab. 

When you delete a Deployment, you delete your Airflow webserver, scheduler, metadata database, and deploy history, and you lose any configurations set in the Airflow UI. 

By default, Astro performs a _soft delete_ when you delete a Deployment. After you delete a Deployment, your Astronomer database, the corresponding `Deployment` record receives a `deletedAt` value and continues to persist until permanently deleted through a _hard delete_. A hard delete includes both the Deployment's metadata database and the Deployment entry in your Astronomer database. 14 days after your Deployment's soft delete, Astronomer automatically runs a hard delete cronjob that deletes any persisting values from your soft delete.

:::tip

Astronomer recommends regularly doing a database audit to confirm that you hard delete databases.

:::

### Automate Deployment deletion clean up 

Astronomer runs a cronjob to hard delete the deleted Deployment's metadata database and Deployment entry in your Astronomer database at midnight on a specified day. You can enable whether this cronjob runs or not, how many days after your soft delete to run the cronjob, and what time of day to run the cronjob by editing `astronomer.houston.cleanupDeployments` in your Astronomer Helm chart.

The following example shows the default settings you can find in your Helm chart.

```
# Cleanup deployments that have been soft-deleted
  # This clean up runs as a CronJob
  cleanupDeployments:
    # Enable the clean up CronJob
    enabled: true

    # Default time for the CronJob to run https://crontab.guru/#0_0_*_*_*
    schedule: "0 0 * * *"

    # Number of days after the Deployment deletion to run the CronJob
    olderThan: 14
```

### Hard delete a Deployment

To reuse a custom release name given to an existing Deployment after a soft delete but before Astronomer automatically cleans up any persisting Deployment records, you need to hard delete both the Deployment's metadata database and the Deployment's entry in your Astronomer database. 

1. Enable hard delete as an option at the platform level. To enable this feature, set `astronomer.houston.config.deployments.hardDeleteDeployment: true` in your `config.yaml` file and push the changes to your platform as described in [Apply a config change](apply-platform-config.md).

2. You can delete a Deployment with the UI or CLI.
  - **In the UI:** Go to the Deployment's **Settings** tab and select **Delete Deployment**. Then, select the **Hard Delete?** checkbox before confirming **Delete Deployment**. 
  - **Astro CLI:** Alternatively, you can run `astro deployment delete --hard`.

This action permanently deletes all data associated with a Deployment, including the database and underlying Kubernetes resources.

![Hard delete checkbox](/img/software/hard-delete.png)

## Programmatically create or update Deployments

You can programmatically create or update Deployments with all possible configurations using the Houston API `upsertDeployment` mutation. See [Create or update a Deployment with configurations](houston-api.md#create-or-update-a-deployment-with-configurations).