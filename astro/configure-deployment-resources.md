---
sidebar_label: 'Configure Deployment resources'
title: 'Configure Deployment resources'
id: configure-deployment-resources
description: Learn how to create and configure Astro Deployment resources.
---

After you create an Astro Deployment, you can modify its resource settings to make sure that your tasks have the CPU and memory required to complete successfully.

## Scheduler resources

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met. By adjusting the **Scheduler Count** slider in the **Configuration** tab of the Cloud UI, you can configure up to 4 schedulers, each of which will be provisioned with the AU specified in **Resources**.

For example, if you set scheduler resources to 10 AU and **Scheduler Count** to 2, your Deployment will run with 2 Airflow schedulers using 10 AU each.

If you experience delays in task execution, which you can track with the Gantt Chart view of the Airflow UI, Astronomer recommends increasing the AU allocated towards the scheduler. The default resource allocation is 10 AU.

### Edit scheduler settings 

1. In the Cloud UI, select a Workspace and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**. 
4. Edit the scheduler resource settings. See [Scheduler resources](#scheduler-resources).
5. Click **Update**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code to your Deployment and does not impact running tasks that have 24 hours to complete before running workers are terminated. See [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Update a Deployment name and description

1. In the Cloud UI, select a Workspace and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**.
4. Update the Deployment name or description. 
5. Click **Update**.

## Add or delete a Deployment alert email

The alert email assigned to a Deployment is used to notify recipients of Deployment issues.

1. In the Cloud UI, select a Workspace and then select a Deployment.
2. Click the **Details** tab.
3. To add an alert email:
    - Click **Edit Emails** in the **Alert Emails** area.
    - Enter an email address and then click **Add**.
4. To delete an alert email address:
    - Click **Edit Emails** in the **Alert Emails** area.
    - Click **Delete** next to the email you want to delete.
    - Click **Yes, Continue**.

## Delete a Deployment

When you delete a Deployment, all infrastructure resources assigned to the Deployment are immediately deleted from your data plane. However, the Kubernetes namespace and metadata database for the Deployment are retained for 30 days. Deleted Deployments can't be restored. If you accidentally delete a Deployment, contact [Astronomer support](https://cloud.astronomer.io/support).

1. In the Cloud UI, select a Workspace.
2. Click the **Options** menu of the Deployment you want to delete, and select **Delete Deployment**.

    ![Options menu](/img/docs/delete-deployment.png)

3. Enter `Delete` and click **Yes, Continue**.

## Next steps

- [Set environment variables on Astro](environment-variables.md).
- [Manage Deployment API keys](api-keys.md).
