---
title: "Airflow pools"
sidebar_label: "Pools"
description: "Use pools to control Airflow task parallelism."
id: airflow-pools
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import pool_example_1_traditional from '!!raw-loader!../code-samples/dags/airflow-pools/pool_example_1_traditional.py';
import pool_example_1_taskflow from '!!raw-loader!../code-samples/dags/airflow-pools/pool_example_1_taskflow.py';
import pool_example_2_traditional from '!!raw-loader!../code-samples/dags/airflow-pools/pool_example_2_traditional.py';
import pool_example_2_taskflow from '!!raw-loader!../code-samples/dags/airflow-pools/pool_example_2_taskflow.py';

One of the benefits of Apache Airflow is that it is built to scale. With the right supporting infrastructure, you can run many tasks in parallel seamlessly. Unfortunately, horizontal scalability also necessitates some guardrails. For example, you might have many tasks that interact with the same source system, such as an API or database, that you don't want to overwhelm with requests. Airflow [pools](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html) are designed for exactly this use case.

Pools allow you to limit parallelism for an arbitrary set of tasks, allowing you to control when your tasks are run. They are often used in cases where you want to limit the number of parallel tasks that do a certain thing. For example, tasks that make requests to the same API or database, or tasks that run on a GPU node of a Kubernetes cluster.

In this guide, you'll learn basic Airflow pool concepts, how to create and assign pools, and what you can and can't do with pools. You'll also implement some sample DAGs that use pools to fulfill simple requirements. 

:::tip Related Content

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Airflow: Pools](https://academy.astronomer.io/astro-runtime-pools) module.

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- The basics of scaling Airflow. See [Scaling out Airflow](airflow-scaling-workers.md).

## Create a pool

There are three ways you can create and manage pools in Airflow:

- The Airflow UI: Go to **Admin** > **Pools** and add a new record. You can define a name, the number of slots, and a description.

    ![Pools UI](/img/guides/pools_ui.png)

- The Airflow CLI: Run the `airflow pools` command with the `set` subcommand to create a new pool. See the [Airflow CLI documentation](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#pools) for the full list of pool commands. With the Airflow CLI, you can also import pools from a JSON file with the `import` subcommand. This can be useful if you have a large number of pools to define and doing so programmatically would be more efficient.
- The Airflow REST API: This option is available with Airflow version 2.0 and later. To create a pool, submit a POST request with the name and number of slots as the payload. For more information on working with pools from the API, see the [API documentation](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_pool).


## Assign tasks to a pool

By default, all tasks in Airflow get assigned to the `default_pool` which has 128 slots. You can modify the number of slots, but you can't remove the default pool. Tasks can be assigned to other pools by updating the `pool` parameter. This parameter is part of the `BaseOperator`, so it can be used with any operator.

<Tabs
    defaultValue="taskflow"
    groupId="assign-tasks-to-a-pool"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
@task(task_id="task_a", pool="single_task_pool")
def sleep_function():
```

</TabItem>

<TabItem value="traditional">

```python
task_a = PythonOperator(
    task_id="task_a", python_callable=sleep_function, pool="single_task_pool"
)
```

</TabItem>
</Tabs>

When tasks are assigned to a pool, they are scheduled as normal until all of the pool's slots are filled. As slots become available, the remaining queued tasks start running. 

If you assign a task to a pool that doesn't exist, then the task isn't scheduled when the DAG runs. There are currently no errors or checks for this in the Airflow UI, so be sure to double check the name of the pool that you're assigning a task to.

You can control which tasks within the pool are run first by assigning [priority weights](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/priority-weight.html). These are assigned at the pool level with the `priority_weights` parameter. The values can be any arbitrary integer (the default is 1), and higher values get higher priority in the executor queue.

For example, in the DAG snippet below `task_a` and `task_b` are both assigned to the `single_task_pool` which has one slot. `task_b` has a priority weight of 2, while `task_a` has the default priority weight of 1. Therefore, `task_b` is executed first.

<Tabs
    defaultValue="taskflow"
    groupId="assign-tasks-to-a-pool"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
@task
def sleep_function(x):
    time.sleep(x)


@dag(
    start_date=datetime(2023, 1, 1),
    schedule="*/30 * * * *",
    catchup=False,
    default_args=default_args,
)
def pool_dag():
    sleep_function.override(task_id="task_a", pool="single_task_pool")(5)
    sleep_function.override(
        task_id="task_b", pool="single_task_pool", priority_weight=2
    )(10)


pool_dag()
```

</TabItem>

<TabItem value="traditional">

```python
def sleep_function(x):
    time.sleep(x)


with DAG(
    "pool_dag",
    start_date=datetime(2023, 1, 1),
    schedule="*/30 * * * *",
    catchup=False,
    default_args=default_args,
) as dag:

    task_a = PythonOperator(
        task_id="task_a",
        python_callable=sleep_function,
        pool="single_task_pool",
        op_args=[5],
    )

    task_b = PythonOperator(
        task_id="task_b",
        python_callable=sleep_function,
        pool="single_task_pool",
        priority_weight=2,
        op_args=[10],
    )

```

</TabItem>
</Tabs>

Additionally, you can configure the number of slots occupied by a task by updating the `pool_slots` parameter (the default is 1). Modifying this value could be useful in cases where you are using pools to manage resource utilization. 

## Pool limitations

When working with pools, keep in mind the following limitations:

- Each task can only be assigned to a single pool.
- If you are using SubDAGs, pools must be applied directly on tasks inside the SubDAG. Pools set within the `SubDAGOperator` will not be honored.
- Pools are meant to control parallelism for task Instances. If you need to place limits on the number of concurrent DagRuns for a single DAG or all DAGs, use the `max_active_runs` or `core.max_active_runs_per_dag` parameters.

## Example: Limit tasks hitting an API endpoint

This example shows how to implement a pool to control the number of tasks hitting an API endpoint. 

In this scenario, five tasks across two different DAGs hit the API and may run concurrently based on the DAG schedules. However, to limit the tasks hitting the API at a time to three, you'll create a pool named `api_pool` with three slots. You'll also prioritize the tasks in the `pool_priority_dag` when the pool is full.

In the `pool_priority_dag` below, all three of the tasks hit the API endpoint and should all be assigned to the pool, so you define the `pool` argument in the DAG `default_args` to apply to all tasks. You also want all three of these tasks to have the same priority weight and for them to be prioritized over tasks in the second DAG, so you assign a `priority_weight` of three as a default argument. This value is arbitrary. To prioritize these tasks, you can assign any integer that is higher than the priority weights defined in the second DAG.

<Tabs
    defaultValue="taskflow"
    groupId="example-limit-tasks-hitting-an-api-endpoint"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{pool_example_1_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{pool_example_1_traditional}</CodeBlock>

</TabItem>
</Tabs>


In the `pool_unimportant_dag` DAG, there are two tasks that hit the API endpoint that should be assigned to the pool, but there are also two other tasks that do not hit the API. Therefore, you assign the pool and priority weights in the `PythonOperator` instantiations. 

To prioritize `task_x` over `task_y` while keeping both at a lower priority than the tasks in the first DAG, you assign `task_x` a priority weight of 2 and leave `task_y` with the default priority weight of 1. 

<Tabs
    defaultValue="taskflow"
    groupId="example-limit-tasks-hitting-an-api-endpoint"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{pool_example_2_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{pool_example_2_traditional}</CodeBlock>

</TabItem>
</Tabs>
