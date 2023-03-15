---
sidebar_label: 'Configure a Deployment'
title: 'Configure a Deployment'
id: configure-deployment-resources
---

<head>
  <meta name="description" content="Modify the resource settings of a Deployment to make sure that your tasks have the CPU and memory required to complete successfully." />
  <meta name="og:description" content="Modify the resource settings of a Deployment to make sure that your tasks have the CPU and memory required to complete successfully." />
</head>

After you create an Astro Deployment, you can modify its settings to meet the unique requirements of your organization. Through the Cloud UI and Astro CLI, you can:

- Allocate resources for the Airflow scheduler and workers.
- Update a Deployment name and description.
- Add or delete a Deployment alert email.
- Change the Deployment executor.
- Transfer a Deployment to another Workspace in your Organization.
- Delete a Deployment.

For advanced Deployment resource configurations, see [Manage Deployment executors](configure-executors.md) and [Configure worker queues](configure-worker-queues.md).

:::cli

This document focuses on configuring Deployments through the Cloud UI. For steps and best practices for configuring Deployments as code using the Astro CLI, see [Manage Deployments as code](manage-deployments-as-code.md).

:::

## Choose an executor

A Deployment's executor type determines which worker resources run your scheduled tasks. Every Deployment requires an executor and you can update the executor at any time. Astro supports two executors, both of which are available in the Apache Airflow open source project:

- Celery executor
- Kubernetes executor

Use the following topics to understand the benefits and limitations of each executor to determine which one is right for your Deployment. 

### Celery executor

The Celery executor is the default for all new Deployments. It utilizes a pool of workers and communicates with them to delegate tasks. Astronomer uses [Worker autoscaling logic](configure-executors.md#worker-autoscaling-logic) to determine how many workers run on each worker queue on your Deployment at a given time.

The Celery executor is a good option for most use cases. Specifically, the Celery executor is a good fit for your team if:

- You're just getting started with Airflow.
- You want to use multiple worker queues. This allows you to use multiple worker node types for different types of tasks and optimize for task performance. See [Configure worker queues](configure-worker-queues.md).
- You have a high number of short-running tasks and want to ensure low latency between tasks.
- You don't often experience conflicts between Python or OS-level packages and don't require dependency isolation.

If your team regularly experiences dependency conflicts or finds that resource intensive tasks consume the resources of other tasks and cause them to fail, Astronomer recommends implementing worker queues or moving to the Kubernetes executor.

See [Manage the Celery executor](configure-executors.md#manage-the-celery-executor) to learn more about how to configure the Celery executor.

### Kubernetes executor

The Kubernetes executor runs each task in an individual Kubernetes Pod instead of in shared Celery workers. For each task that needs to run, the executor calls the Kubernetes API to dynamically launch a Pod for the task. You can specify the configuration of the task and Pod, including CPU and memory, in a `pod_override` file. When the task completes, the Pod terminates. On Astro, the Kubernetes infrastructure required to run the Kubernetes executor is built into every Deployment and is managed by Astronomer.

The Kubernetes executor is a good fit for teams that need fine-grained configurations for each of their tasks. Specifically, the Kubernetes executor is a good fit for your team if:

- You have long-running tasks that require more than 24 hours to execute. The Kubernetes executor ensures that tasks longer than 24 hours are not interrupted when your team deploys code.
- You experience a high number of dependency conflicts between tasks and could benefit from task isolation. For example, one task in your Deployment requires a different version of pandas than another task.
- You have a strong understanding of the CPU and memory that your tasks require and would benefit from being able to allocate and optimize infrastructure resources at the task level.
- Your team has had issues running certain tasks reliably with the Celery executor.
  
The primary limitation with the Kubernetes executor is that each task takes up to 1 minute to start running once scheduled. If you're running short-running tasks and cannot tolerate high latency, Astronomer recommends the Celery executor. To learn more, see [Kubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html) in Airflow documentation or [Manage the Kubernetes executor on Astro](configure-executors.md#manage-the-kubernetes-executor).

If you want to run only specific tasks in a Kubernetes Pod, consider using the [KubernetesPodOperator](kubernetespodoperator.md).

### Update the Deployment executor

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Details** tab.
3. Click **Edit Details**. 
4. Select **Celery** or **Kubernetes** in the **Executor** list. If you're moving from the Celery to the Kubernetes executor, all existing worker queues are deleted. Running tasks stop gracefully and all new tasks start with the selected executor.
5. Click **Update**.

## Scheduler resources

The [Airflow scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is responsible for monitoring task execution and triggering downstream tasks when the dependencies are met. To ensure that your tasks have the CPU and memory required to complete successfully on Astro, you can set:

- **Scheduler Resources**: Determine the total CPU and memory allocated to each scheduler in your Deployment, defined as Astronomer Units (AU). One AU is equivalent to 0.1 CPU and 0.375 GiB of memory. The default scheduler size is 5 AU, or .5 CPU and 1.88 GiB memory. The number of schedulers running in your Deployment is determined by **Scheduler Count**, but all schedulers are created with the same CPU and memory allocations.

- **Scheduler Count**: Move the slider to select the number of schedulers for the Deployment. Each scheduler is provisioned with the AU you specified in the **Scheduler Resources** field. For example, if you set scheduler resources to 10 AU and **Scheduler Count** to 2, your Deployment will run with 2 Airflow schedulers using 10 AU each. For high availability, Astronomer recommends selecting a minimum of two schedulers. 

Scheduler resources must be set for each Deployment and are managed separately from cluster-level infrastructure. Any additional components that Astro requires, including PgBouncer, KEDA, and the triggerer, are managed by Astronomer.

### Update scheduler settings 

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
