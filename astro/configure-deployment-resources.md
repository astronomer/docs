---
sidebar_label: 'Configure a Deployment'
title: 'Configure a Deployment'
id: configure-deployment-resources
---

<head>
  <meta name="description" content="Modify the resource settings of a Deployment to make sure that your tasks have the CPU and memory required to complete successfully." />
  <meta name="og:description" content="Modify the resource settings of a Deployment to make sure that your tasks have the CPU and memory required to complete successfully." />
</head>

After you create an Astro Deployment, you can modify its settings using the Cloud UI and Astro CLI. Specifically you can:

- Allocate resources for your tasks.
- Update a Deployment name and description.
- Add or delete a Deployment alert email.
- Change the Deployment executor.
- Transfer a Deployment to another Workspace in your Organization.
- Delete a Deployment.

For advanced Deployment resource configurations, see [Manage Deployment executors](executors.md) and [Configure compute queues](configure-worker-queues.md).

:::cli

This document focuses on configuring Deployments through the Cloud UI. For steps and best practices for configuring Deployments as code using the Astro CLI, see [Manage Deployments as code](manage-deployments-as-code.md).

:::

## Deployment executor

Astro supports two executors, both of which are available in the Apache Airflow open source project:

- Celery executor
- Kubernetes executor

All Deployments use the Celery executor by default. See [Choose an executor](executors.md#choose-an-executor) to understand the benefits and limitations of each executor. When you've determined the right executor type for your Deployment, complete the steps in the following topic to update your Deployment's executor type.

### Update the Deployment executor

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**. 
4. Select **Celery** or **Kubernetes** in the **Executor** list. If you're moving from the Celery to the Kubernetes executor, all existing worker queues are deleted. Running tasks stop gracefully and all new tasks start with the selected executor.
5. Click **Update**.
6. Optional. Configure worker queues and tasks to optimize resource usage on your Deployment. See [Configure an executor](executors.md).

## Scheduler size

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met. 

Scheduler resources must be set for each Deployment and are managed separately from cluster-level infrastructure. To ensure that your tasks have the CPU and memory required to complete successfully on Astro, you can provision the scheduler with varying amounts of CPU and memory. See the following table for recommendations of 

| Deployment size | Scheduler size |
|-----------------|----------------|
|                 |                |
|                 |                |
|                 |                |

### Update scheduler size 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**. 
4. Choose a scheduler size. See [Scheduler resources](#scheduler-resources).
5. Click **Update**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code and triggers a rebuild of your Deployment image. If you're using the Celery executor, currently running tasks have 24 hours to complete before their running workers are terminated. See [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Update a Deployment name and description

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**.
4. Update the Deployment name or description. 
5. Click **Update**.

## Configure Deployment email alerts

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

## Enforce CI/CD deploys

By default, Deployments accept code deploys from any authenticated source. When you enforce CI/CD deploys for a Deployment, the Deployment only accepts code deploys if they are triggered with a Deployment API key or Workspace token. 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**.
4. In **CI/CD Enforcement**, click the toggle to **On**.

You can also update your Workspace so that any new Deployments in the Workspace enforce CI/CD deploys by default. See [Update general Workspace settings](manage-workspaces.md#update-general-workspace-settings).

## Transfer a Deployment to another Workspace 

Transferring a Deployment can be helpful when your team needs to change user access to a Deployment. Transferring a Deployment moves all DAGs, task history, connections, API keys, and other Astro configurations. Running tasks are not interrupted and tasks will continue to be scheduled.

To transfer a Deployment from one Workspace to another, the Workspaces must be in the same Organization. Transferred Deployments cannot be transferred to a different cluster from the one in which they were created.

Only the users who are members of the target Workspace can access the Deployment after it is transferred. To transfer a Deployment, you must be a Workspace Admin or Editor in both the original Workspace and the target Workspace.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu and select **Transfer Deployment**. 

    ![Transfer Deployment in options menu](/img/docs/transfer-deployment.png)

3. Select the target Workspace where you want to transfer the Deployment. 
4. Click **Transfer Deployment**.

## Delete a Deployment

When you delete a Deployment, all infrastructure resources assigned to the Deployment are immediately deleted. However, the Kubernetes namespace and metadata database for the Deployment are retained for 30 days. Deleted Deployments can't be restored. If you accidentally delete a Deployment, contact [Astronomer support](https://cloud.astronomer.io/support).

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to delete, and select **Delete Deployment**.

    ![Delete Deployment in options menu](/img/docs/delete-deployment.png)

3. Enter `Delete` and click **Yes, Continue**.

## Next steps

- [Set environment variables on Astro](environment-variables.md).
- [Manage Deployment API keys](api-keys.md).
- [Manage Deployments as Code](manage-deployments-as-code.md)
