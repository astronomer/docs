---
sidebar_label: 'Worker queues'
title: 'Configure worker queues'
id: configure-worker-queues
description: Learn how to create and configure worker queues to create best-fit execution environments for your tasks.
---

A worker queue is a set of configurations that apply to a group of workers in your Deployment. In Apache Airflow, a worker is responsible for executing tasks that have been scheduled and queued by the scheduler. On Astro, each worker is a Kubernetes Pod that is hosted within a Kubernetes node in your Astro cluster.

Use worker queues to create optimized execution environments for different types of tasks in the same Deployment. You can use worker queues to:

- Separate resource-intensive tasks, such as those that execute machine learning models, from tasks that require minimal resources, such as those that execute SQL queries.
- Separate short-running tasks from long-running tasks.
- Isolate a single task from other tasks in your Deployment.
- Allow some workers to scale to zero but keep a minimum of 1 for other types of workers.

By default, all tasks run in a default worker queue that does not require configuration or code. To enable worker types or configurations for different groups of tasks, you can create additional worker queues in the Cloud UI and assign tasks to queues in your DAG code.

## Benefits

Worker queues can enhance performance, decrease cost, and increase the reliability of task execution in your Deployment. Specifically:

- Executing a task with dedicated hardware that best fits the needs of that task can result in faster performance. In some cases, this can decrease the duration of a DAG by up to 50%.
- Paying for larger workers only for select tasks means that you can lower your infrastructure cost by not paying for that worker when your tasks don't need it.
- Separating tasks that have different characteristics often means they're less likely to result in a failed or zombie state.

## Example

By configuring multiple worker queues and assigning tasks to these queues based on the requirements of the tasks, you can enhance the performance, reliability, and throughput of your Deployment. For example, consider the following scenario:

- You are running Task A and Task B in a Deployment on an AWS cluster.
- Task A and Task B are dependent on each other, so they need to run in the same Deployment.
- Task A is a long-running task that uses a lot of CPU and little memory, while Task B is a short-running task that uses minimal amounts of CPU and memory.

You can assign Task A to a worker queue that is configured to use the [`c6i.4xlarge`](https://aws.amazon.com/ec2/instance-types/c6i/) worker type that's optimized for compute. Then, you can assign Task B to a worker queue that is configured to use the [`m5.xlarge`](https://aws.amazon.com/ec2/instance-types/m5) worker type that is smaller and optimized for general usage.

## Worker queue settings

You can configure each worker queue on Astro with the following settings:

- **Name:** The name of your worker queue. Use this name to assign tasks to the worker queue in your DAG code. Worker queue names must consist only of lowercase letters and hyphens. For example, `machine-learning-tasks` or `short-running-tasks`.
- **Worker Type:** The size and type of workers in the worker queue, defined as a node instance type that is supported by the cloud provider of your cluster. For example, a worker type might be `m5.2xlarge` or `c6i.4xlarge` for a Deployment running on an AWS cluster. A worker’s total available CPU, memory, storage, and GPU is defined by its worker type. Actual worker size is equivalent to the total capacity of the worker type minus Astro’s system overhead.
- **Max Tasks per Worker:** The maximum number of tasks that a single worker can run at a time. If the number of queued and running tasks exceeds this number, a new worker is added to run the remaining tasks. This value is equivalent to [worker concurrency](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-concurrency) in Apache Airflow. It is 16 by default.
- **Worker Count**: The minimum and maximum number of workers that can run at a time.  The number of running workers changes regularly based on Maximum Tasks per Worker and the current number of tasks in a `queued` or `running` state. By default, the minimum number of workers is 1 and the maximum is 10.

### Default worker queue

Each Deployment requires a worker queue named `default` to run tasks. Tasks that are not assigned to a worker queue in your DAG code are executed by workers in the default worker queue. 

If you don’t change any settings in the default worker queue:

- A maximum of 16 tasks can run at one time per worker. If more than 16 tasks are queued or running, a new worker is added to run the remaining tasks.
- A maximum of 10 workers can run at once, meaning that a maximum of 160 tasks can be in a `running` state at a time. Remaining tasks will stay in a `queued` or `scheduled` state until running tasks complete.

You can change all settings of the default worker queue except for its name.

## Worker autoscaling logic

The number of workers running per worker queue on your Deployment at a given time is based on two values:

- The total number of tasks in a `queued` or `running` state
- The worker queue's setting for **Maximum Tasks per Worker**

The calculation is made based on the following expression:

`[Number of workers]= ([Queued tasks]+[Running tasks])/(Maximum tasks per worker)`

The number of workers subsequently determines the Deployment's [parallelism](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#parallelism), which is the maximum number of tasks which can run concurrently within a single Deployment and across worker queues. To ensure that you can always run as many tasks as your workers allow, parallelism is calculated with the following expression:

`[Parallelism]= ([Total number of running workers for all worker queues] * [The sum of all **Maximum tasks per worker*** values for all worker queues])`.

These calculations are computed by KEDA every 10 seconds. For more information on how workers are affected by changes to a Deployment, read [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

### Request a worker type

Your organization can enable up to 10 different worker types for each cluster. After a worker type is enabled on an Astro cluster, the worker type becomes available to any Deployment in that cluster and appears in the **Worker Type** menu of the Cloud UI.

1. Review the list of supported worker types for your cloud provider. See [AWS](resource-reference-aws.md#worker-node-types), [Azure](resource-reference-azure.md#worker-node-size-resource-reference), or [GCP](resource-reference-gcp.md#worker-node-size-resource-reference).
2. Contact [Astronomer support](https://cloud.astronomer.io/support) with the name of the worker type(s) you want to enable for your cluster. For example, `m6i.2xlarge`.

For more information on requesting cluster changes, see [Modify a cluster](modify-cluster.md).

## Create a worker queue

:::cli

If you prefer, you can also run the `astro deployment worker-queue create` command in the Astro CLI to create a worker queue. See the [CLI Command Reference](cli/astro-deployment-worker-queue-create.md).

:::

1. In the Cloud UI, select a Workspace and then select a Deployment.

2. Click the **Worker Queues** tab and then click **Worker Queue**.

3. Configure the worker queue’s settings. You can't change the name of a worker queue after you create it.

4. Click **Create Queue**.

## Assign tasks to a worker queue

By default, all tasks run in the default worker queue. To run tasks on a different worker queue, assign the task to the worker queue in your DAG code.

To assign an Airflow task to a worker queue:

1. In the Cloud UI, select a Workspace and select a Deployment.

2. Click the **Worker Queues** tab.

3. Copy the name of the worker queue name you want to assign a task to.

4. In your DAG code, add a `queue='<worker-queue-name>'` argument to the definition of the task. If a task is assigned to a queue that does not exist or is not referenced properly, the task might remain in a `queued` state and fail to execute. Make sure that the name of the queue in your DAG code matches the name of the queue in the Cloud UI.

	For example, all instances of this task will run in the `short-running-tasks` queue:

	```python
	feature_engineering = DatabricksSubmitRunOperator(
		task_id='feature_engineering_notebook_task'
		notebook_task={
			'notebook_path': "/Users/{{ var.value.databricks_user }}/feature-eng_census-pred"
		},
		queue='short-running-tasks',
		)
	```

## Update a worker queue

:::cli

If you prefer, you can run the `astro deployment worker-queue update` command in the Astro CLI to update a worker queue. See the [CLI Command Reference](cli/astro-deployment-worker-queue-update.md).

:::

You can update worker queue configurations at any time. The worker queue name can't be changed.

If you need to change the worker type of an existing worker queue, Astronomer recommends making the change at a time when it will not affect production pipelines. After you've changed a worker type, Astronomer recommends waiting a minimum of five minutes before pushing new code to your Deployment.

1. In the Cloud UI, select a Workspace and then select a Deployment.

2. Click the **Worker Queues** tab.

3. Click **Edit** for the worker queue that you want to update. 

4. Update the worker queue settings, and then click **Update Queue**. 

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code to your Deployment and does not impact running tasks that have 24 hours to complete before running workers are terminated. See [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Delete a worker queue

:::cli
If you prefer, you can also run the `astro deployment worker-queue delete` command in the Astro CLI to delete a worker queue. See the [CLI Command Reference](cli/astro-deployment-worker-queue-delete.md).
:::

All scheduled tasks that are assigned to a worker queue after the worker queue is deleted remain in a `queued` state indefinitely and won't execute. To avoid stalled task runs, ensure that you reassign all tasks from a worker queue before deleting it. You can either remove the worker queue argument or assign the task to a different queue.

1. In the Cloud UI, select a Workspace and then select a Deployment.

2. Click the **Worker Queues** tab.

3. Click **Delete** for the worker queue that you want to delete.

4. Enter `Delete <worker-queue-name>` and then click **Yes, Continue**.
