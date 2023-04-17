---
sidebar_label: 'Configure a Deployment'
title: 'Configure a Deployment'
id: configure-deployment-resources
---

<head>
  <meta name="description" content="Modify the resource settings of a Deployment to make sure that your tasks have the CPU and memory required to complete successfully." />
  <meta name="og:description" content="Modify the resource settings of a Deployment to make sure that your tasks have the CPU and memory required to complete successfully." />
</head>

After you create an Astro Deployment, you can modify its settings to meet the unique requirements of your organization. On Astro, you can:

- Allocate resources for the Airflow scheduler and workers.
- Update a Deployment name and description.
- Add or delete a Deployment alert email.
- Transfer a Deployment to another Workspace in your Organization.
- Delete a Deployment.

## Set Deployment resources

To ensure that your tasks have the CPU and memory required to complete successfully, you can set resources for:

- The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html), which is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met.
- Workers, which are responsible for executing tasks that have been scheduled and queued by the scheduler.

Worker and scheduler resources must be set for each Deployment and are managed separately from cluster-level infrastructure. Any additional components that Astro requires, including PgBouncer, KEDA, and the triggerer, are managed by Astronomer.

:::cli

If you prefer, you can set Deployment resources using the Astro CLI and a local Deployment configuration file. See [Deployments as Code](manage-deployments-as-code.md).

:::

### Worker queues 

Worker queues are a set of configurations that apply to a group of workers in your Deployment. Each Deployment includes a `default` worker queue for running tasks, but you can configure additional worker queues to define CPU and memory limits for your tasks.

See [Configure worker queues](configure-worker-queues.md).

### Scheduler resources

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met. By adjusting the **Scheduler Count** slider in the **Configuration** tab of the Cloud UI, you can configure up to 4 schedulers, each of which will be provisioned with the Astronomer Units (AU) specified in **Resources**. An AU is a unit of CPU and memory allocated to each scheduler in a Deployment. 1 AU is equivalent to 0.1 CPU and 0.375 GiB of memory. Assigning 5 AUs to a scheduler is equivalent to 0.5 CPUs and 1.88 GiB of memory. You can view the CPU and memory allocations for schedulers on the Deployment **Details** page in the Cloud UI.

For example, if you set scheduler resources to 10 AU and **Scheduler Count** to 2, your Deployment will run with 2 Airflow schedulers using 10 AU each.

If you experience delays in task execution, which you can track with the Gantt Chart view of the Airflow UI, Astronomer recommends increasing the AU allocated towards the scheduler. The default resource allocation is 10 AU.

#### Edit scheduler settings 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**. 
4. Edit the scheduler resource settings. See [Scheduler resources](#scheduler-resources).
5. Click **Update**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code to your Deployment and does not impact running tasks that have 24 hours to complete before running workers are terminated. See [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Update a Deployment name and description

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**.
4. Update the Deployment name or description. 
5. Click **Update**.

## Add or delete a Deployment alert email

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

## Update Airflow configurations

To update a Deployment's [Airflow configurations](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html), you set the configurations as environment variables on Astro. See [Set Airflow configurations using environment variables](environment-variables.md#set-airflow-configurations-using-environment-variables).
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

When you delete a Deployment, all infrastructure resources assigned to the Deployment are immediately deleted from your data plane. However, the Kubernetes namespace and metadata database for the Deployment are retained for 30 days. Deleted Deployments can't be restored. If you accidentally delete a Deployment, contact [Astronomer support](https://cloud.astronomer.io/support).

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to delete, and select **Delete Deployment**.

    ![Delete Deployment in options menu](/img/docs/delete-deployment.png)

3. Enter `Delete` and click **Yes, Continue**.

## See also

- [Set environment variables on Astro](environment-variables.md).
- [Manage Deployment API keys](api-keys.md).
- [Manage Deployments as Code](manage-deployments-as-code.md)
