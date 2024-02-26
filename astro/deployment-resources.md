---
sidebar_label: 'Deployment resources'
title: 'Configure Deployment resources'
id: deployment-resources
description: "Configure your Deployment resource settings to optimze Deployment performance."
---

Your Deployment resources are the computational resources Astro uses to run Airflow in the cloud. Update Deployment resource settings to optimize performance and reduce the cost of running Airflow in the cloud.

## Update Airflow configurations

To update a Deployment's [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html), you set the configurations as environment variables on Astro. See [Set Airflow configurations using environment variables](manage-env-vars.md).

## Update environment objects

You can add, update, and delete Airflow connections that were added through the Cloud UI from your Deployment page. To edit a Deployment's [linked connections](manage-connections-variables.md#astro-cloud-ui-environment-manager), click the **Environment** tab, and then select the connection you want to **Edit**. See [Create connections with the Cloud UI](create-and-link-connections.md) for more options.

## Deployment executor

Astro supports two executors, both of which are available in the Apache Airflow open source project:

- [Celery executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/celery.html)
- [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) (_Requires Astro Runtime version 8.1.0 or later_)

All Deployments use the Celery executor by default. See [Choose an executor](executors-overview.md#choose-an-executor) to understand the benefits and limitations of each executor. When you've determined the right executor type for your Deployment, complete the steps in the following topic to update your Deployment's executor type.

### Update the Deployment executor

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Execution** section, select **Celery** or **Kubernetes** in the **Executor** list.

    If you're moving from the Celery to the Kubernetes executor, all existing worker queues are deleted. Running tasks stop gracefully and all new tasks start with the selected executor.

4. Click **Update Deployment**.

See [Configure an executor](executors-overview.md) for more information about each available executor type, including how to optimize executor usage.

## Configure Kubernetes Pod resources

The [Kubernetes executor](kubernetes-executor.md) and [KubernetesPodOperator](kubernetespodoperator.md) both use Kubernetes Pods to execute tasks. While you still need to configure Pods in your DAG code to define individual task environments, you can set some safeguards on Astro so that tasks in your Deployment don't request more CPU or memory than expected.

Set safeguards by configuring default Pod limits and requests from the Cloud UI. If a task requests more CPU or memory than is currently allowed in your configuration, the task fails.

:::info

To manage Kubernetes resources programmatically, you can set default Pod limits and resources with the [`astro deployment create`](cli/astro-deployment-create.md) and [`astro deployment update`](cli/astro-deployment-update.md) Astro CLI commands, or by adding the configurations to a [Deployment file](deployment-file-reference.md).

:::

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Execution** section, configure the following values:
    - **CPU Quota**: The maximum combined CPU usage across all running Pods on your Deployment.
    - **Memory Quota**: The maximum combined memory usage across all running Pods on your Deployment.
    - **Default Pod Size**:
        - **CPU**: The amount of CPUs that your tasks run with if no CPU usage is specified in their Pod configuration.
        - **Memory**: The amount of memory that your tasks run with if no memory usage is specified in their Pod configuration.

     For a Deployment running in a Hosted dedicated or shared cluster, the maximum possible **CPU** quota is 1600 vCPU and maximum **Memory** quota is 3200 GiB.

     :::warning Astro Hosted

     For Astro Hosted environments, if you set resource requests to be less than the maximum limit, Astro automatically requests the maximum limit that you set. This means that you might consume more resources than you expected if you set the limit much higher than the resource request you need. Check your [Billing and usage](manage-billing.md) to view your resource use and associated charges.

     :::

4. Click **Update Deployment**.

## Scheduler size

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met.

Scheduler resources must be set for each Deployment and are managed separately from cluster-level infrastructure. To ensure that your tasks have the CPU and memory required to complete successfully on Astro, you can provision the scheduler with varying amounts of CPU and memory.

Unlike workers, schedulers do not autoscale. The resources you set for them are the resources you have regardless of usage. For more information about how scheduler configuration affects resources usage, see [Pricing](https://astronomer.io/pricing).

Astronomer Deployments run a single scheduler. You can configure your scheduler to have different amounts of resources based on how many tasks you need to schedule. The following table lists all possible scheduler sizes for Astro Hosted:

| Scheduler size | vCPU | Memory | Ephemeral storage |
| -------------- | ---- | ------ | ----------------- |
| Small          | 1    | 2G     | 5Gi               |
| Medium         | 2    | 4G     | 5Gi               |
| Large          | 4    | 8G     | 5Gi              |

### Update scheduler size

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** section, choose a scheduler size. See [Scheduler size](#scheduler-size).
4. Click **Update Deployment**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code and triggers a rebuild of your Deployment image. If you're using the Celery executor, currently running tasks have 24 hours to complete before their running workers are terminated. See [What happens during a code deploy](deploy-project-image.md#what-happens-during-a-project-deploy).

<details>
  <summary><strong>Alternative Astro Hybrid setup</strong></summary>

To configure the scheduler on an [Astro Hybrid](hybrid-overview.md) Deployment:

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** section, configure the following values:

    - **Scheduler Resources**: Determine the total CPU and memory allocated to each scheduler in your Deployment, defined as Astronomer Units (AU). One AU is equivalent to 0.1 CPU and 0.375 GiB of memory. The default scheduler size is 5 AU, or .5 CPU and 1.88 GiB memory. The number of schedulers running in your Deployment is determined by **Scheduler Count**, but all schedulers are created with the same CPU and memory allocations.
    - **Scheduler Count**: Move the slider to select the number of schedulers for the Deployment. Each scheduler is provisioned with the AU you specified in the **Scheduler Resources** field. For example, if you set scheduler resources to 10 AU and **Scheduler Count** to 2, your Deployment will run with 2 Airflow schedulers using 10 AU each. For high availability, Astronomer recommends selecting a minimum of two schedulers.

4. Click **Update Deployment**.

</details>

## Enable high availability

By default, the Pods running your Deployment's Airflow components are distributed across multiple nodes. When you enable high availability, your Deployment runs two instances of [PgBouncer](https://www.pgbouncer.org/) and two instances of the Airflow Scheduler across different nodes. However, Astro makes a best effort to use different availability zones for your PGBouncer and Scheduler, which means it is possible but unlikely that they are both located in the same availability zone. This ensures that your DAGs can continue to run if there's an issue with one of your Airflow components in a specific node or availability zone.

Because this setting results in more resource usage, it can increase the cost of your Deployment. See [Pricing](https://astronomer.io/pricing).

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** section, click the toggle to **On** for **High Availability**.

4. Select **Update Deployment** to save your changes.

<details>
  <summary><strong>Alternative Astro Hybrid setup</strong></summary>

On Astro Hybrid, PgBouncer is highly available by default for all Deployments. Schedulers are highly available if a Deployment uses two or more schedulers.

Every Deployment has two PgBouncer Pods assigned to two different nodes to prevent zombie tasks. If you configure your Deployment with two schedulers, each scheduler Pod is assigned to a separate node to ensure availability. To limit cost, a Deployment that uses three or four schedulers can assign all scheduler Pods across two nodes.

</details>

## Hibernate a development Deployment

:::caution

This feature is in [Private Preview](feature-previews.md). To access this feature or learn more, [contact Astronomer](https://www.astronomer.io/contact/). All customers are eligible to use this feature upon request.

:::

When you create a Deployment on Astro, you pay for the infrastructure resources that are required to run the Deployment for the duration that it's active. In development environments when you aren't always running tasks, you can _hibernate_, or scale down, all Deployment resources on a specified schedule. When you hibernate a Deployment, all Deployment configurations are preserved, but computing resources are scaled to zero.

For example, if you only need to test a DAG during working hours, you can set a hibernation schedule for 5:00 PM until 9:00 AM on Monday through Friday. During this time, your Deployment settings are preserved and your cost on Astro for the Deployment is $0. When the hibernation schedule ends, you can resume using the Deployment. Waking up a Deployment from hibernation is faster than creating a new Deployment and preserves all of your configurations.

![Example of setting a hibernation schedule in the Cloud UI. A schedule is being set so that the Deployment hibernates outside of work hours.](/img/docs/hibernating-schedule.png)

Use Deployment hibernation to ensure that:

- You only pay for the resources that you need, when you need them.
- You don't have to delete a Deployment in order to avoid the cost of the Deployment.
- You don't have to recreate development environments and re-enter Deployment configurations.

### Prerequisites

You can hibernate a Deployment only if you enabled **Development Mode** when you [created the Deployment](create-deployment.md). Deployments without this setting enabled can't be hibernated.

### Create a hibernation schedule

Before you create a hibernation schedule for a Deployment, consider the following constraints:

- The Deployment must have the **Development Mode** setting turned on. This setting can only be configured when you create a Deployment.
- The **High Availability** feature is not supported. A Deployment with a hibernation schedule cannot be highly available.
- The **Small Scheduler** (1 vCPU, 2 GiB RAM) is the only scheduler size supported.
- Deployments with hibernation schedules are not required to meet the uptime SLAs of standard production Deployments.

To create a hibernation schedule:

1. In the Cloud UI, select a Workspace, click **Deployments**, then select a Deployment.
2. Click **Details**. In the **Advanced** section of your Deployment configuration, click **Edit**.
3. Configure the following values in **Hibernation schedules**:
     - **Start Schedule**: Specify a cron schedule for your Deployment resources to scale to zero.
     - **End Schedule**: Specify a cron schedule for Astro to restart your configured resources.
     - **Description**: (Optional) Give your hibernation schedule a description.
     - **Enabled**: Tick this checkbox if you want to activate the schedule after configuring it.

4. (Optional) Specify additional hibernation schedules for your Deployment.
5. Select **Update Deployment** to save your changes.

:::tip

You can use the following example cron expressions to implement common Deployment hibernation schedules:

| Schedule                                               | Start schedule | End schedule |
| ------------------------------------------------------ | -------------- | ------------ |
| Hibernate from 5:00 PM to 9:00 AM                      | 0 17 * * *     | 0 9 * * *    |
| Hibernate on weekends (Friday 5:00PM to Monday 9:00AM) | 0 17 * * 5     | 0 9 * * 1    |

:::

:::warning

Astro sets all cron schedules for hibernation in UTC. If you're running a Deployment in another time zone, you must convert the cron expression for your time zone to UTC. For example, if you want your Deployment to hibernate at 17:00 EST, you use `0 22 * * *` (22:00 UTC) as the cron expression.

:::

When your hibernation schedule starts:

- Your Deployment shows a **Hibernating** status in the Cloud UI:

    ![A Deployment with a Hibernating status on the Deployments page of the Cloud UI](/img/docs/hibernating-status.png)

- Any task that was previously running will be killed and marked as failed.
- Tasks and DAGs do not run. Task instances that were already running or scheduled at the time of hibernation will fail and trigger any related notifications.
- No Deployment resources are available. This includes the scheduler, webserver, and all workers.
- You can't access the Airflow UI for the Deployment.
- You can't deploy project images or DAGs to the Deployment.

When your hibernation schedule ends, the Deployment will start any DAG runs for data intervals that were missed during hibernation for DAGs with `catchup=true`. To avoid incurring additional resource costs, Astronomer recommends disabling catchup on DAGs in hibernating Deployments.

### Manually hibernate a Deployment

Instead of creating a regular hibernation schedule, you can manually hibernate a development Deployment from the Cloud UI. This is recommended if you're not sure when you'll need to use the Deployment again after hibernating it.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **More Actions** menu of the Deployment you want to update, then select **Hibernate Deployment**.
3. Configure the manual hibernation period, then click **Confirm**.

If you need to run a task or DAG on a Deployment that is currently in hibernation, you can manually wake up a Deployment from hibernation before the end of its schedule.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **More Actions** menu of the Deployment you want to update, then select **Wake up from Hibernation**.
3. Select one of the following options for how you want your Deployment to wake up:

    - **Wake until further notice**: Your Deployment wakes up immediately for an indefinite period and ignores any configured hibernation schedules.
    - **Wake until set time and date**: Specify a time that the Deployment should go back into hibernation after waking up.
    - **Remove override and return to normal schedule**: The Deployment returns to following your configured hibernation schedules.

4. Click **Confirm**.