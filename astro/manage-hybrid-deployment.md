---
sidebar_label: 'Manage Hybrid Deployments'
title: 'Manage hybrid Deployments'
id: manage-hybrid-deployment
---

:::info

This document applies only to Astro Hybrid users. To see whether you're an Astro Hybrid user, open your Organization in the Cloud UI and go to **Settings** > **General**. You version of Astro is listed under **Product Type**.

To create a Deployment on Astro Hosted, see [Create a Deployment](create-deployment.md).

:::

## Create a Hybrid Deployment

1. In the Cloud UI, select a Workspace.

2. On the **Deployments** page, click **Deployment**.

3. Complete the following fields:

    - **Name**: Enter a name for your Deployment.
    - **Astro Runtime**: By default, the latest version of Astro Runtime is selected. The Astro Runtime versions provided in the Cloud UI are limited to patches for the most recent major and minor releases. Deprecated versions of Astro Runtime aren't available.

        To upgrade the Astro Runtime version for your Deployment, you’ll need to update your Docker image in your Astro project directory. For more information about upgrading Astro Runtime, see [Upgrade Astro Runtime](upgrade-runtime.md).

    - **Description**: Optional. Enter a description for your Deployment.
    - **Cluster**: Select the Astro cluster in which you want to create this Deployment.
    - **Executor**: Select an executor to run your scheduled tasks. The Celery executor runs multiple tasks in a single worker and is a good choice for most teams. The Kubernetes executor runs each task in an isolated Kubernetes Pod and is a good option for teams that want fine-grained control over the execution environment for each of their tasks. For more information about the benefits and limitations of each executor, see [Choose an executor](configure-deployment-resources.md#choose-an-executor).
    - **Worker Type**: Select the worker type for your default worker queue. See [Worker queues](configure-deployment-resources.md#worker-queues).

4. Optional. Edit additional Deployment resource settings. See [Configure Deployment resources](configure-deployment-resources.md). If you don't change any Deployment resource settings, your Deployment is created with the following resources:

    - The celery executor
    - A worker queue named `default` that runs a maximum of 10 workers. Each of these workers can run a maximum of 16 tasks can run at a time.
    - A single scheduler with 0.5 CPUs and 1.88 GiB of memory.

5. Click **Create Deployment**.

     A confirmation message appears indicating that the Deployment is in progress. Select the **Deployments** link to go to the **Deployments** page. The Deployment status is **Creating** until all underlying components in your Astro cluster are healthy, including the Airflow webserver and scheduler. During this time, the Airflow UI is unavailable and you can't deploy code or modify Deployment settings. When the Deployment is ready, the status changes to **Healthy**.
    
    For more information about possible Deployment health statuses, see [Deployment health](deployment-metrics.md#deployment-health).


## Configure Hybrid Deployment resources

After you create an Astro Deployment, you can modify its settings to meet the unique requirements of your organization. Using the Cloud UI and Astro CLI, you can:

- Allocate resources for the Airflow scheduler and workers.
- Update a Deployment name and description.
- Add or delete a Deployment alert email.
- Change the Deployment executor.
- Transfer a Deployment to another Workspace in your Organization.
- Delete a Deployment.

For advanced Deployment resource configurations, see [Manage Deployment executors](executors.md) and [Configure worker queues](configure-worker-queues.md).

:::cli

This document focuses on configuring Deployments through the Cloud UI. For steps and best practices for configuring Deployments as code using the Astro CLI, see [Manage Deployments as code](manage-deployments-as-code.md).

:::

### Deployment executor

Astro supports two executors, both of which are available in the Apache Airflow open source project:

- Celery executor
- Kubernetes executor

All Deployments use the Celery executor by default. See [Choose an executor](executors.md#choose-an-executor) to understand the benefits and limitations of each executor. When you've determined the right executor type for your Deployment, complete the steps in the following topic to update your Deployment's executor type.

#### Update the Deployment executor

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**. 
4. Select **Celery** or **Kubernetes** in the **Executor** list. If you're moving from the Celery to the Kubernetes executor, all existing worker queues are deleted. Running tasks stop gracefully and all new tasks start with the selected executor.
5. Click **Update**.
6. Optional. Configure worker queues and tasks to optimize resource usage on your Deployment. See [Configure an executor](executors.md).

### Scheduler resources

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met. 

Scheduler resources must be set for each Deployment and are managed separately from cluster-level infrastructure. To ensure that your tasks have the CPU and memory required to complete successfully on Astro, you can set:

- **Scheduler Resources**: Determine the total CPU and memory allocated to each scheduler in your Deployment, defined as Astronomer Units (AU). One AU is equivalent to 0.1 CPU and 0.375 GiB of memory. The default scheduler size is 5 AU, or .5 CPU and 1.88 GiB memory. The number of schedulers running in your Deployment is determined by **Scheduler Count**, but all schedulers are created with the same CPU and memory allocations.

- **Scheduler Count**: Move the slider to select the number of schedulers for the Deployment. Each scheduler is provisioned with the AU you specified in the **Scheduler Resources** field. For example, if you set scheduler resources to 10 AU and **Scheduler Count** to 2, your Deployment will run with 2 Airflow schedulers using 10 AU each. For high availability, Astronomer recommends selecting a minimum of two schedulers. 

#### Update scheduler settings 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**. 
4. Edit the scheduler resource settings. See [Scheduler resources](#scheduler-resources).
5. Click **Update**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code and triggers a rebuild of your Deployment image. If you're using the Celery executor, currently running tasks have 24 hours to complete before their running workers are terminated. See [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

### Update a Deployment name and description

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**.
4. Update the Deployment name or description. 
5. Click **Update**.

### Add or delete a Deployment alert email

Alert emails assigned to a Deployment are used by Astronomer support to notify recipients in the case of an issue with the Deployment. This can include a problem with your scheduler or workers. Automated email alerts are coming soon.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. To add an alert email:
    - Click **Edit Emails** in the **Alert Emails** area.
    - Enter an email address and then click **Add**.
4. To delete an alert email address:
    - Click **Edit Emails** in the **Alert Emails** area.
    - Click **Delete** next to the email you want to delete.
    - Click **Yes, Continue**.

In addition to alert emails for your Deployments, Astronomer recommends subscribing to the [Astro status page](https://status.astronomer.io). When you subscribe, you'll receive email notifications about system-wide incidents in real time.

### Update Airflow configurations

To update a Deployment's [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html), you set the configurations as environment variables on Astro. See [Set Airflow configurations using environment variables](environment-variables.md#set-airflow-configurations-using-environment-variables).

### Enforce CI/CD deploys

By default, Deployments accept code deploys from any authenticated source. When you enforce CI/CD deploys for a Deployment, the Deployment only accepts code deploys if they are triggered with a Deployment API key or Workspace token. 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**.
4. In **CI/CD Enforcement**, click the toggle to **On**.

You can also update your Workspace so that any new Deployments in the Workspace enforce CI/CD deploys by default. See [Update general Workspace settings](manage-workspaces.md#update-general-workspace-settings).

### Transfer a Deployment to another Workspace 

Transferring a Deployment can be helpful when your team needs to change user access to a Deployment. Transferring a Deployment moves all DAGs, task history, connections, API keys, and other Astro configurations. Running tasks are not interrupted and tasks will continue to be scheduled.

To transfer a Deployment from one Workspace to another, the Workspaces must be in the same Organization. Transferred Deployments cannot be transferred to a different cluster from the one in which they were created.

Only the users who are members of the target Workspace can access the Deployment after it is transferred. To transfer a Deployment, you must be a Workspace Admin or Editor in both the original Workspace and the target Workspace.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu and select **Transfer Deployment**. 

    ![Transfer Deployment in options menu](/img/docs/transfer-deployment.png)

3. Select the target Workspace where you want to transfer the Deployment. 
4. Click **Transfer Deployment**.

### Delete a Deployment

When you delete a Deployment, all infrastructure resources assigned to the Deployment are immediately deleted from your data plane. However, the Kubernetes namespace and metadata database for the Deployment are retained for 30 days. Deleted Deployments can't be restored. If you accidentally delete a Deployment, contact [Astronomer support](https://cloud.astronomer.io/support).

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to delete, and select **Delete Deployment**.

    ![Delete Deployment in options menu](/img/docs/delete-deployment.png)

3. Enter `Delete` and click **Yes, Continue**.

## See also

- [Set environment variables on Astro](environment-variables.md).
- [Manage Deployment API keys](api-keys.md).
- [Manage Deployments as Code](manage-deployments-as-code.md)