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
- Change the Deployment executor.
- Transfer a Deployment to another Workspace in your Organization.
- Delete a Deployment.

For advanced Deployment resource configurations, see [Manage Deployment executors](manage-astro-executors.md) and [Configure worker queues](configure-worker-queues.md).

## Choose an executor

The executor type you select determines which worker resources run your scheduled tasks. A single executor is assigned to each Deployment and you can update the executor assignment at any time. 

### Celery executor

The Celery executor works with a pool of workers and communicates with them to delegate tasks and it's a good option for most uses cases. Astronomer uses worker autoscaling logic to determine how many workers run on each worker queue on your Deployment at a given time. See [Worker autoscaling logic](manage-astro-executors.md#worker-autoscaling-logic). 

#### Benefits

- Worker queues let you assign tasks to different worker types. See [Configure worker queues](configure-worker-queues.md)
- Allows additional workers to be added to cope with higher demand (horizontal scaling).
- Provides a grace period for worker termination.
- Running tasks are not terminated.

#### Limitations

- Execution speed is prioritized over task reliability.
- Complicated set up.
- More maintenance.

### Kubernetes executor

The Kubernetes executor is recommended when you need to control resource optimization, isolate your workloads, maintain long periods without running tasks, or run tasks for extended periods during deployments.

#### Benefits

- Fault tolerance. A task that fails doesn't cause other tasks to fail.
- Specify CPU and memory limits or minimums to optimize performance and reduce costs.
- Task isolation. A task uses only the resources allocated to it and it can't consume resources allocated to other tasks. 
- Running tasks are not interrupted when a deploy is pushed.

On Astro, the Kubernetes infrastructure required to run the Kubernetes executor is built into every cluster in the data plane and is managed by Astronomer.

#### Limitations

- Tasks take longer to start and this causes task latency.
- PersistentVolumes (PVs) are not supported on Pods launched in an Astro cluster.
- The `pod_template_file` argument is not supported on Pods launched in an Astro cluster. If you use the `pod_template_file` argument, the DAG is rejected and a broken DAG error message appears in teh Airflow UI. Astronomer recommends using `python-kubernetes-sdk`. See [Astro Python SDK ReadTheDocs](https://astro-sdk-python.readthedocs.io/en/stable/).

### Update the Deployment executor

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**. 
4. Select **Celery** or **Kubernetes** in the **Executor** list. If you're moving from the Celery to the Kubernetes executor, all existing worker queues are deleted. Running tasks stop gracefully and all new tasks start with the selected executor.
5. Click **Update**.

## Set scheduler resources

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met. To ensure that your tasks have the CPU and memory required to complete successfully, you can set resources for:

- **Scheduler Resources**: Select the number of Astronomer Units (AU) assigned to the schedulers. Alternatively, move the CPU and memory slider to use specific CPU and memory values to automatically define the scheduler AU assignment. An AU is a unit of CPU and memory allocated to each scheduler in a Deployment. One AU is equivalent to 0.1 CPU and 0.375 GiB of memory. Assigning five AUs to a scheduler is equivalent to 0.5 CPUs and 1.88 GiB of memory. 

    If you experience delays in task execution, which you can track with the Gantt Chart view of the Airflow UI, Astronomer recommends increasing the allocated AU value. The default resource allocation is ten AU. 

- **Scheduler Count**: Move the slider to select the number of schedulers for the Deployment. Each scheduler is provisioned with the AU you specified in the **Scheduler Resources** field. For example, if you set scheduler resources to ten AU and **Scheduler Count** to two, your Deployment will run with two Airflow schedulers using ten AU each. For high availability, Astronomer recommends selecting a minimum of two schedulers. 
- The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html), which is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met.

Scheduler resources must be set for each Deployment and are managed separately from cluster-level infrastructure. Any additional components that Astro requires, including PgBouncer, KEDA, and the triggerer, are managed by Astronomer.

:::cli

If you prefer, you can set Deployment resources using the Astro CLI and a local Deployment configuration file. See [Deployments as Code](manage-deployments-as-code.md).

:::

### Edit scheduler settings 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**. 
4. Edit the scheduler resource settings. See [Scheduler resources](#scheduler-resources).
5. Click **Update**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code and triggers a rebuild of your Deployment image. If you're using the Celery executor, currently running tasks have 24 hours to complete before their running workers are terminated. See [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

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

## Next steps

- [Set environment variables on Astro](environment-variables.md).
- [Manage Deployment API keys](api-keys.md).
- [Manage Deployments as Code](manage-deployments-as-code.md)
