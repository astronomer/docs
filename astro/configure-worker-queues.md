---
sidebar_label: 'Worker queues'
title: 'Configure worker queues'
id: configure-worker-queues
description: Learn how to create and configure worker queues to create best-fit execution environments for your tasks.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

By default, all tasks using the Celery executor run in a `default` worker queue. You can create additional worker queues to enable multiple worker types or configurations for different groups of tasks, and assign tasks to these queues in your DAG code. For more information about Airflow executors on Astro, see [Manage Airflow executors on Astro](executors-overview.md).

Use worker queues to create optimized execution environments for different types of tasks in the same Deployment. You can use worker queues to:

- Separate resource-intensive tasks, such as those that execute machine learning models, from tasks that require minimal resources, such as those that execute SQL queries.
- Separate short-running tasks from long-running tasks.
- Isolate a single task from other tasks in your Deployment.
- Allow some workers to scale to zero but keep a minimum of 1 for other types of workers.

## Benefits

Worker queues can enhance performance, decrease cost, and increase the reliability of task execution in your Deployment. Specifically:

- Executing a task with dedicated hardware that best fits the needs of that task can result in faster performance. In some cases, this can decrease the duration of a DAG by up to 50%.
- Paying for larger workers only for select tasks means that you can lower your infrastructure cost by not paying for that worker when your tasks don't need it.
- Separating tasks that have different characteristics often means they're less likely to result in a failed or zombie state.

## Example

By configuring multiple worker queues and assigning tasks to these queues based on the requirements of the tasks, you can enhance the performance, reliability, and throughput of your Deployment. For example, consider the following scenario:

- You are running Task A and Task B in a Deployment.
- Task A and Task B are dependent on each other, so they need to run in the same Deployment.
- Task A is a long-running task that uses a lot of CPU and memory, while Task B is a short-running task that uses minimal amounts of CPU and memory.

You can assign Task A to a worker queue that is configured to use the A20 worker type, which is optimized for running compute-heavy tasks. Then, you can assign Task B to a worker queue that is configured to use the A5 worker type, which is smaller and optimized for general usage.

## Worker queue settings

You can configure each worker queue on Astro with the following settings:

- **Name:** The name of your worker queue. Use this name to assign tasks to the worker queue in your DAG code. Worker queue names must consist only of lowercase letters and hyphens. For example, `machine-learning-tasks` or `short-running-tasks` or `high-cpu`.
- **Worker Type:** The size of workers in the worker queue, for example A5 or A20. A worker’s total available CPU, memory, and storage is defined by its worker size. For more information about worker types, see [Astro Hosted resource reference](resource-reference-hosted.md).
- **Concurrency:** The maximum number of tasks that a single worker can run at a time. If the number of queued and running tasks exceeds this number, a new worker is added to run the remaining tasks. This value is equivalent to [worker concurrency](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#worker-concurrency) in Apache Airflow. The default for your worker type is suitable for most use cases.
- **Min # Workers / Max # Workers**: The minimum and maximum number of workers that can run at a time. The number of workers autoscales based on **Concurrency** and the current number of tasks in a `queued` or `running` state. 

:::info Alternative Astro Hybrid setup 

On Astro Hybrid clusters, worker type is defined as a node instance type that is supported by the cloud provider of your cluster. For example, a worker type might be `m5.2xlarge` or `c6i.4xlarge` for a Deployment running on a Hybrid AWS cluster hosted on your cloud. Actual worker size is equivalent to the total capacity of the worker type minus Astro’s system overhead.

Your Organization can enable up to 10 additional different worker types for each Hybrid cluster. After a worker type is enabled on an Astro Hybrid cluster, the worker type becomes available to any Deployment in that cluster and appears in the **Worker Type** menu of the Cloud UI.

1. Review the list of supported worker types for your cloud provider. See [AWS](resource-reference-aws-hybrid.md#worker-node-types), [Azure](resource-reference-azure-hybrid.md#worker-node-size-resource-reference), or [GCP resource references](resource-reference-gcp-hybrid.md#worker-node-size-resource-reference).
2. Contact [Astronomer support](https://cloud.astronomer.io/support) and provide the following information: 
  
    - The name of your cluster. 
    - The name of the worker type(s) you want to enable for your cluster. For example, `m6i.2xlarge`.

For more information on requesting cluster changes, see [Manage Hybrid clusters](manage-hybrid-clusters.md).

:::

## Default worker queue

Each Deployment requires a worker queue named `default` to run tasks. Tasks that are not assigned to a worker queue in your DAG code are executed by workers in the `default` worker queue.

You can change all settings of the default worker queue except for its name.

## Create or edit a worker queue

:::cli

If you prefer, you can also run the `astro deployment worker-queue create` command in the Astro CLI to create a worker queue. See the [CLI Command Reference](cli/astro-deployment-worker-queue-create.md).

:::

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. In the **Execution** section, configure the worker queue’s settings:

    * Edit the **Worker Type**, **Concurrency**, or **Min # Workers / Max # Workers** of an existing queue. You can't change the name of a worker queue after you create it.
    
    * Click **Add Queue** to create a new worker queue, and then configure its related attributes.

6. When you're done editing worker queues, click **Update Deployment** to save your changes.

:::tip

You can create, update, and delete multiple worker queues at once using a Deployment file. See [Deployments as Code](manage-deployments-as-code.md).

:::

## Assign tasks to a worker queue

By default, all tasks run in the default worker queue. To run tasks on a different worker queue, assign the task to the worker queue in your DAG code.

### Step 1: Copy the name of the worker queue

1. In the Cloud UI, select a Workspace and select a Deployment.
2. Click the **Worker Queues** tab.
3. Copy the name of the worker queue name you want to assign a task to.

### Step 2: Assign the task in your DAG code

In your DAG code, add a `queue='<worker-queue-name>'` argument to the definition of the task. If a task is assigned to a queue that does not exist or is not referenced properly, the task might remain in a `queued` state and fail to execute. Make sure that the name of the queue in your DAG code matches the name of the queue in the Cloud UI.

Astronomer recommends using Apache Airflow's [Taskflow API](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html) to define your task argument. The Taskflow API is feature in Airflow 2 that includes a task [decorator](learn/airflow-decorators) and makes DAGs easier to write. In the following examples, all instances of the task will run in the `machine-learning-tasks` queue. Choose an example based on whether or not you use the Taskflow API.

<Tabs
    defaultValue="classicoperator"
    groupId= "assign-worker-queue"
    values={[
        {label: 'Classic Operator Example', value: 'classicoperator'},
        {label: 'TaskFlow API Example', value: 'taskflow'},
    ]}>

<TabItem value="classicoperator">

 ```python
  train_model = PythonOperator(
   task_id='train_model',
   python_callable=train_model_flights
   queue='machine-learning-tasks'
  )
 ```

</TabItem>

<TabItem value="taskflow">

 ```python
  @task(task_id='train_model', queue='machine-learning-tasks')
  def train_model_flights(x_train, y_train):
   import xgboost
   from sklearn.preprocessing import StandardScaler
   from sklearn.pipeline import Pipeline

   xgbclf = xgboost.XGBClassifier() 
   
   pipe = Pipeline([('scaler', StandardScaler(with_mean=False)),
     ('xgbclf', xgbclf)])
   
   pipe.fit(x_train, y_train)

   return pipe
 ```

</TabItem>

</Tabs>

## Update a worker queue

:::cli

If you prefer, you can run the `astro deployment worker-queue update` command in the Astro CLI to update a worker queue. See the [CLI Command Reference](cli/astro-deployment-worker-queue-update.md).

:::

You can update worker queue configurations at any time. The worker queue name can't be changed.

If you need to change the worker type of an existing worker queue, Astronomer recommends making the change at a time when it will not affect production pipelines. After you've changed a worker type, Astronomer recommends waiting a minimum of five minutes before pushing new code to your Deployment.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. Expand the **Execution** section if it is not already expanded.
4. Update the worker queue settings, and then click **Update Deployment**.

    The Airflow components of your Deployment automatically restart to apply the updated resource allocations. This action is equivalent to deploying code to your Deployment and does not impact running tasks that have 24 hours to complete before running workers are terminated. See [What happens during a code deploy](deploy-code.md#what-happens-during-a-code-deploy).

## Delete a worker queue

:::cli
If you prefer, you can also run the `astro deployment worker-queue delete` command in the Astro CLI to delete a worker queue. See the [CLI Command Reference](cli/astro-deployment-worker-queue-delete.md).
:::

All scheduled tasks that are assigned to a worker queue after the worker queue is deleted remain in a `queued` state indefinitely and won't execute. To avoid stalled task runs, ensure that you reassign all tasks from a worker queue before deleting it. You can either remove the worker queue argument or assign the task to a different queue.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu of the Deployment you want to update, and select **Edit Deployment**.

    ![Edit Deployment in options menu](/img/docs/edit-deployment.png)

3. Expand the **Execution** section if it is not already expanded.
4. Click the trash can icon for the worker queue that you want to delete, and then click **Update Deployment**.
