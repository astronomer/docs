---
sidebar_label: 'Deployment settings'
title: 'Deployment settings'
id: deployment-settings
description: "Manage Deployment settings to customize your Deployment for your use case."
---

After you create an Astro Deployment, you can modify its settings using the Cloud UI and Astro CLI to tailor its performance. There's two categories of options for configuring your Astro Deployment to best meet your needs: Deployment details and resource configuration.

Use Deployment details to manage the administration of your Deployment. This includes includes actions like updating information about your Deployment or transferring it to another Workspace. The following actions allow you to organize and label your Deployments within your Workspace in a way that best fits how your team works with Astro: 

- Update a Deployment name and description.
- Add or delete a Deployment alert email.
- Transfer a Deployment to another Workspace in your Organization.
- Delete a Deployment.

You also have configuration options that allow you to customize the resource use, infrastructure, and performance of your Deployment. This means you can optimize how your deployment uses resources, so you can improve the efficeincy of your Deployment processing, optimize compute resources, or enable advanced use cases for workload and cost optimization. The following configuration options enable you to specialize your Deployment configuration to get the maximum performance out of your Astro resources:

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
2. Click the **Options** menu and select **Edit Deployment**. 

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Basic** section, update the Deployment **Name** or **Description**.

4. Click **Update Deployment**.

### Configure Deployment email alerts

Email alerts are used by Astronomer support to notify recipients in the case of an issue with a Deployment. This can include a problem with your scheduler or workers. 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. To add an alert email:
    - Click **Edit Emails** in the **Alert Emails** area.
    - Enter an email address and then click **Add**.
4. To delete an alert email address:
    - Click **Edit Emails** in the **Alert Emails** area.
    - Click **Delete** next to the email you want to delete.
    - Click **Yes, Continue**.

In addition to alert emails for your Deployments, Astronomer recommends configuring [Astro alerts](alerts.md) and subscribing to the [Astro status page](https://status.astronomer.io). When you subscribe to the status page, you'll receive email notifications about system-wide incidents as they happen.

### Transfer a Deployment to another Workspace 

Transferring a Deployment can be helpful when your team needs to change user access to a Deployment. Transferring a Deployment moves all DAGs, task history, connections, API keys, and other Astro configurations. Running tasks are not interrupted and tasks will continue to be scheduled.

To transfer a Deployment from one Workspace to another, the Workspaces must be in the same Organization. Transferred Deployments cannot be transferred to a different cluster from the one in which they were created.

Only the users who are members of the target Workspace can access the Deployment after it is transferred. To transfer a Deployment, you must be a Workspace Admin or Editor in both the original Workspace and the target Workspace.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu and select **Transfer Deployment**. 

    ![Transfer Deployment in options menu](/img/docs/transfer-deployment.png)

3. Select the target Workspace where you want to transfer the Deployment. 
4. Click **Transfer Deployment**.

### Enforce CI/CD deploys

By default, Deployments accept code deploys from any authenticated source. When you enforce CI/CD deploys for a Deployment:

- The Deployment accepts code deploys only if the deploys are triggered with a Deployment API token/key, Workspace API token, or Organization API token.
- You can't enable [DAG-only deploys](deploy-dags.md) for the Deployment.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu and select **Edit Deployment**. 

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** section, click the **CI/CD Enforcement** toggle to **On**.

4. Click **Update Deployment**.

You can also update your Workspace so that any new Deployments in the Workspace enforce CI/CD deploys by default. See [Update general Workspace settings](manage-workspaces.md#update-general-workspace-settings).

### Delete a Deployment

When you delete a Deployment, all infrastructure resources assigned to the Deployment are immediately deleted. However, the Kubernetes namespace and metadata database for the Deployment are retained for 30 days. Deleted Deployments can't be restored. If you accidentally delete a Deployment, contact [Astronomer support](https://cloud.astronomer.io/support).

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to delete, and select **Delete Deployment**.

    ![Delete Deployment in options menu](/img/docs/delete-deployment.png)

3. Enter `Delete` and click **Yes, Continue**.

## Configure Deployment resources

Update Deployment resource settings to optimize performance and reduce the cost of running Airflow in the cloud.

### Update Airflow configurations

To update a Deployment's [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html), you set the configurations as environment variables on Astro. See [Set Airflow configurations using environment variables](env-vars-astro.md).

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

## Update a Deployment name and description

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Basic** section, update the Deployment **Name** or **Description**. 

4. Click **Update Deployment**.

## Configure Deployment email alerts

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

## Update Airflow configurations

To update a Deployment's [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html), you set the configurations as environment variables on Astro. See [Set Airflow configurations using environment variables](environment-variables.md#set-airflow-configurations-using-environment-variables).

## Enforce CI/CD deploys

By default, Deployments accept code deploys from any authenticated source. When you enforce CI/CD deploys for a Deployment:

- The Deployment accepts code deploys only if the deploys are triggered with a Deployment API key, Workspace API token, or Organization API token.
- You can't enable [DAG-only deploys](deploy-dags.md) for the Deployment.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Advanced** sectionn, find **CI/CD Enforcement** and click the toggle to **On**.

You can also update your Workspace so that any new Deployments in the Workspace enforce CI/CD deploys by default. See [Update general Workspace settings](manage-workspaces.md#update-general-workspace-settings).

## Enable high availability

By default, the Pods running your Deployment's Airflow components are distributed across multiple nodes. When you enable high availability, your Deployment runs two instances of [PgBouncer](https://www.pgbouncer.org/) and two instances of its scheduler across different nodes. This ensures that your DAGs can continue to run if there's an issue with one of your Airflow components in a specific node. Note that PGBouncer Pods are guaranteed to run across multiple availability zones, but scheduler Pods are not. 

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

## See also

- [Set environment variables on Astro](environment-variables.md).
- [Manage Deployment API keys](api-keys.md).
- [Manage Deployments as Code](manage-deployments-as-code.md)
