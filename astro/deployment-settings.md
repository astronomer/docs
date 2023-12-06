---
sidebar_label: 'Deployment settings'
title: 'Deployment settings'
id: deployment-settings
description: "Manage Deployment settings to customize your Deployment for your use case."
---

After you create an Astro Deployment, you can modify its settings using the Cloud UI and Astro CLI to tailor its performance. There are two categories of options for configuring your Astro Deployment to best meet your needs: Deployment details and resource configuration.

Use Deployment details to manage the administration of your Deployment. This includes includes actions like updating information about your Deployment or transferring it to another Workspace. The following actions allow you to organize and label your Deployments within your Workspace in a way that best fits how your team works with Astro: 

- Update a Deployment name and description.
- Add or delete a Deployment alert email.
- Transfer a Deployment to another Workspace in your Organization.
- Delete a Deployment.

You also have configuration options that allow you to customize the resource use, infrastructure, and performance of your Deployment. This means you can optimize how your Deployment uses resources, so you can improve the efficiency of your Deployment processing, optimize compute resources and cost, or enable advanced use cases with intensive workloads. The following configuration options enable you to customize your Deployment to get the most out of your resources on Astro:

- Change the Deployment executor.
- Configure Kubernetes Pod resources.
- Change Scheduler resources.
- Enforce CI/CD Deploys.
- Enable High Availability.
- Update your Airflow configuration.

For advanced Deployment resource configurations, see [Manage Airflow executors on Astro](executors-overview.md) and [Configure worker queues](configure-worker-queues.md).

:::cli

This document focuses on configuring Deployments through the Cloud UI. To configure Deployments as code using the Astro CLI, see [Manage Deployments as code](manage-deployments-as-code.md).

:::

## Configure Deployment details

Deployment details define how users can view and interact with your Deployment. They include metadata settings, observability settings, and user access settings.

### Update a Deployment name and description

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Basic** section, update the Deployment **Name** or **Description**. 

4. Click **Update Deployment**.

### Configure Deployment email alerts

Email alerts are used by Astronomer support to notify recipients in the case of an issue with a Deployment. This can include a problem with your scheduler or workers. 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Details** tab.

3. To add an alert email:
    - Click **Edit Emails** in the **Other** area.
    - Enter an email address and then click **Add**.

4. To delete an alert email address:
    - Click **Edit Emails** in the **Other** area.
    - Click **Delete** next to the email you want to delete.
    - Click **Yes, Continue**.

In addition to alert emails for your Deployments, Astronomer recommends configuring [Astro alerts](alerts.md) and subscribing to the [Astro status page](https://status.astronomer.io). When you subscribe to the status page, you'll receive email notifications about system-wide incidents as they happen.

### Enforce CI/CD deploys

By default, Deployments accept code deploys from any authenticated source. When you enforce CI/CD deploys for a Deployment:

- The Deployment accepts code deploys only if the deploys are triggered with a Deployment API token, Workspace API token, or Organization API token.
- You can't enable [DAG-only deploys](deploy-dags.md) for the Deployment.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** section, find **CI/CD Enforcement** and click the toggle to **On**.

You can also update your Workspace so that any new Deployments in the Workspace enforce CI/CD deploys by default. See [Update general Workspace settings](manage-workspaces.md#update-general-workspace-settings).

### Delete a Deployment

When you delete a Deployment, all infrastructure resources assigned to the Deployment are immediately deleted. However, the Kubernetes namespace and metadata database for the Deployment are retained for 30 days. Deleted Deployments can't be restored. If you accidentally delete a Deployment, contact [Astronomer support](https://cloud.astronomer.io/open-support-request).

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to delete, and select **Delete Deployment**.

    ![Delete Deployment in options menu](/img/docs/delete-deployment.png)

3. Enter `Delete` and click **Yes, Continue**.

## Configure Deployment resources

Update Deployment resource settings to optimize performance and reduce the cost of running Airflow in the cloud.

### Update Airflow configurations

To update a Deployment's [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html), you set the configurations as environment variables on Astro. See [Set Airflow configurations using environment variables](manage-env-vars.md).

### Update environment objects

You can add, update, and delete Airflow connections that were added through the Cloud UI from your Deployment page. To edit a Deployment's [linked connections](manage-connections-variables.md#cloud-ui-connections), click the **Environment** tab, and then select the connection you want to **Edit**. See [Create connections with the Cloud UI](create-and-link-connections.md) for more options.

### Deployment executor

Astro supports two executors, both of which are available in the Apache Airflow open source project:

- [Celery executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/celery.html)
- [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html)

All Deployments use the Celery executor by default. See [Choose an executor](executors-overview.md#choose-an-executor) to understand the benefits and limitations of each executor. When you've determined the right executor type for your Deployment, complete the steps in the following topic to update your Deployment's executor type.

#### Update the Deployment executor

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Execution** section, select **Celery** or **Kubernetes** in the **Executor** list. 
    
    If you're moving from the Celery to the Kubernetes executor, all existing worker queues are deleted. Running tasks stop gracefully and all new tasks start with the selected executor.

4. Click **Update Deployment**.

See [Configure an executor](executors-overview.md) for more information about each available executor type, including how to optimize executor usage.

### Configure Kubernetes Pod resources

The [Kubernetes executor](kubernetes-executor.md) and [KubernetesPodOperator](kubernetespodoperator.md) both use Kubernetes Pods to execute tasks. While you still need to configure Pods in your DAG code to define individual task environments, you can set some safeguards on Astro so that tasks in your Deployment don't request more CPU or memory than expected.

Set safeguards by configuring default Pod limits and requests from the Cloud UI. If a task requests more CPU or memory than is currently allowed in your configuration, the task fails.

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
     
     :::caution Astro Hosted

     For Astro Hosted environments, if you set resource requests to be less than the maximum limit, Astro automatically requests the maximum limit that you set. This means that you might consume more resources than you expected if you set the limit much higher than the resource request you need. Check your [Billing and usage](manage-billing.md) to view your resource use and associated charges.

     :::
     
4. Click **Update Deployment**.

After you change the Pod size, wait for a couple of minutes before running your tasks to allow Astro to apply the changes to your Pod's ConfigMap. 

Your CPU and memory quotas determine how many tasks can run at once on your Deployment. For example, if your Deployment has a CPU quota of 3vCPU and a memory quota of 6GiB, and a task requests this amount, then your Deployment can run only that task until it completes.

The CPU and memory quotas also determine the **Max Pod Size**, which is the maximum amount of resources that a task can request.

:::caution

For Deployments running on dedicated clusters, the largest possible CPU and memory quotas can exceed the largest possible **Max Pod Size**. Because tasks run in a single Pod, your tasks can't request resources that exceed the **Max Pod Size**, even if your quota is larger.

For example, if your Deployment has a CPU quota of 150vCPU and a memory quota of 300GiB, your **Max Pod Size** might only be 12 vCPU and 24GiB RAM. If you try to run a task that requests 20vCPU, the task won't run even though it's within your quotas.

:::

:::info Alternative Astro Hybrid setup

On Astro Hybrid, Kubernetes executor Pods run on a worker node in your Astro cluster. If a worker node can't run any more Pods, Astro automatically provisions a new worker node to begin running any queued tasks in new Pods. By default, each task runs in a dedicated Kubernetes Pod with up to 1 CPU and 384 Mi of memory. 

To give your tasks more or less resources, change the worker type in the task's worker queue and then change your resource requests using a `pod_override` configuration. See [(Hybrid clusters only) Change the Kubernetes executor's worker node type](kubernetes-executor.md#hybrid-clusters-only-change-the-kubernetes-executors-worker-node-type).

:::

### Scheduler size

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met. 

Scheduler resources must be set for each Deployment and are managed separately from cluster-level infrastructure. To ensure that your tasks have the CPU and memory required to complete successfully on Astro, you can provision the scheduler with varying amounts of CPU and memory.

Unlike workers, schedulers do not autoscale. The resources you set for them are the resources you have regardless of usage. For more information about how scheduler configuration affects resources usage, see [Pricing](https://astronomer.io/pricing).

#### Update scheduler size 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** section, choose a scheduler size. See [Scheduler size](#scheduler-size).
4. Click **Update Deployment**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code and triggers a rebuild of your Deployment image. If you're using the Celery executor, currently running tasks have 24 hours to complete before their running workers are terminated. See [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

:::info Alternative Astro Hybrid setup

To configure the scheduler on an [Astro Hybrid](hybrid-overview.md) Deployment:

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** section, configure the following values:

    - **Scheduler Resources**: Determine the total CPU and memory allocated to each scheduler in your Deployment, defined as Astronomer Units (AU). One AU is equivalent to 0.1 CPU and 0.375 GiB of memory. The default scheduler size is 5 AU, or .5 CPU and 1.88 GiB memory. The number of schedulers running in your Deployment is determined by **Scheduler Count**, but all schedulers are created with the same CPU and memory allocations.
    - **Scheduler Count**: Move the slider to select the number of schedulers for the Deployment. Each scheduler is provisioned with the AU you specified in the **Scheduler Resources** field. For example, if you set scheduler resources to 10 AU and **Scheduler Count** to 2, your Deployment will run with 2 Airflow schedulers using 10 AU each. For high availability, Astronomer recommends selecting a minimum of two schedulers. 

4. Click **Update Deployment**.

:::

### Enable high availability

By default, the Pods running your Deployment's Airflow components are distributed across multiple nodes. When you enable high availability, your Deployment runs two instances of [PgBouncer](https://www.pgbouncer.org/) and two instances of the Airflow Scheduler across different nodes. However, Astro makes a best effort to use different availability zones for your PGBouncer and Scheduler, which means it is possible but unlikely that they are both located in the same availability zone. This ensures that your DAGs can continue to run if there's an issue with one of your Airflow components in a specific node or availability zone. 

Because this setting results in more resource usage, it can increase the cost of your Deployment. See [Pricing](https://astronomer.io/pricing).

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** section, click the toggle to **On** for **High Availability**.

4. Select **Update Deployment** to save your changes.

:::info Alternative Astro Hybrid Setup

On Astro Hybrid, PgBouncer is highly available by default for all Deployments. Schedulers are highly available if a Deployment uses two or more schedulers. 

Every Deployment has two PgBouncer Pods assigned to two different nodes to prevent zombie tasks. If you configure your Deployment with two schedulers, each scheduler Pod is assigned to a separate node to ensure availability. To limit cost, a Deployment that uses three or four schedulers can assign all scheduler Pods across two nodes.

:::

### Hibernate a development Deployment

:::caution

This feature is in [Private Preview](feature-previews.md). To access this feature or learn more, [contact Astronomer](https://www.astronomer.io/contact/). All customers are eligible to use this feature upon request.

:::

When you create a Deployment on Astro, you pay for the infrastructure resources that are required to run the Deployment for the duration that it's active. In development environments when you aren't always running tasks, you can _hibernate_, or scale down, all Deployment resources on a specified schedule. When you hibernate a Deployment, all Deployment configurations are preserved, but computing resources are scaled to zero.

For example, if you only need to test a DAG during working hours, you can set a hibernation schedule for 5:00 PM until 9:00 AM on Monday through Friday. During this time, your Deployment settings are preserved and your cost on Astro for the Deployment is $0. When the hibernation schedule ends, you can resume using the Deployment.

Use Deployment Hibernation to ensure that:

- You only pay for the resources that you need, when you need them.
- You don't have to delete a Deployment in order to avoid the cost of the Deployment.
- You don't have to recreate development environments and re-enter Deployment configurations.

#### Create a hibernation schedule

Before you create a hibernation schedule for a Deployment, consider the following constraints:

- The Deployment must have the **Is Development?** setting turned on.
- The **High Availability** feature is not supported. A Deployment with a hibernation schedule cannot be highly available.
- The **Small Scheduler** (1v CPU, 2 Gib RAM) is the only scheduler size supported. 
- Deployments with hibernation schedules are not required to meet the uptime SLAs of standard production Deployments.

To create a hibernation schedule:

1. In the Cloud UI, select a Workspace, click **Deployments**, then select a Deployment.
2. Click **Details**. In the **Advanced** section of your Deployment configuration, click **Edit**.
3. In **Scheduler** sub-section and, click the toggle to **On** for **Is Development?**. A **Hibernation schedules** section appears.
4. Configure the following values in **Hibernation schedules**:
     - **Start Schedule**: Specify the time that your Deployment resources scale to zero.
     - **End Schedule**: Specify the time that Astro restarts your configured resources.
     - **Description**: (Optional) Give your hibernation schedule a description.
     - **Enabled**: Tick this checkbox if you want to activate the schedule after configuring it.

5. (Optional) Specify additional hibernation schedules for your Deployment.
5. Select **Update Deployment** to save your changes.

When your hibernation schedule starts:

- Your Deployment shows a **Hibernating** status in the Cloud UI:

    ![A Deployment with a Hibernating status on the Deployments page of the Cloud UI](/img/docs/hibernating-status.png)

- Any task that was previously running will be killed and marked as failed.
- Tasks and DAGs do not run. Scheduled tasks will fail.
- No Deployment resources are available. This includes the scheduler, webserver, and all workers.
- You cannot access the Airflow UI for the Deployment.

#### Wake up from hibernation

If you need to run a task or DAG on a Deployment that is currently in hibernation, you cna manually wake up the Deployment from hibernation before the end of its schedule.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to update, and select **Wake up from hibernation**.
3. Wait for the Deployment status to turn `HEALTHY`. Then, you can access the Airflow UI and resume running tasks.

## See also

- [Set environment variables on Astro](environment-variables.md)
- [Authenticate an automation tool to Astro](automation-authentication.md)
- [Manage Deployments as Code](manage-deployments-as-code.md)
