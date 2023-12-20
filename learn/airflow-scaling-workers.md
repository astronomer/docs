---
title: "Scaling Airflow to optimize performance"
sidebar_label: "Scaling Airflow"
id: airflow-scaling-workers
---

<head>
  <meta name="description" content="See which parameters to modify when scaling up data pipelines to make the most of Airflow. Learn about the environment, DAG, and task-level settings." />
  <meta name="og:description" content="See which parameters to modify when scaling up data pipelines to make the most of Airflow. Learn about the environment, DAG, and task-level settings." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

One of the biggest strengths of Apache Airflow is its ability to scale to meet the changing demands of your organization. To make the most of Airflow, there are a few key settings that you should consider modifying as you scale up your data pipelines.

Airflow exposes a number of parameters that are closely related to DAG and task-level performance. These include:

- Environment-level settings.
- DAG-level settings.
- Task-level settings.

In this guide, you'll learn about the key parameters that you can use to modify Airflow performance. you'll also learn how your choice of executor can impact scaling and how best to respond to common scaling issues.

This guide references the parameters available in Airflow version 2.0 and later. If you're using an earlier version of Airflow, some of the parameter names might be different.

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Webinar: [Scaling Out Airflow](https://www.astronomer.io/events/webinars/scaling-out-airflow/).

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow core components. See [Airflow's components](airflow-components.md).
- Airflow executors. See [Airflow executors explained](airflow-executors-explained.md).

## Parameter tuning

Airflow has many parameters that impact its performance. Tuning these settings can impact DAG parsing and task scheduling performance, parallelism in your Airflow environment, and more. 

The reason Airflow allows so many adjustments is that, as an agnostic orchestrator, Airflow is used for a wide variety of use cases. Airflow admins or DevOps engineers might tune scaling parameters at the environment level to ensure that their supporting infrastructure isn't overstressed, while DAG authors might tune scaling parameters at the DAG or task level to ensure that their pipelines don't overwhelm external systems. Knowing the requirements of your use case before scaling Airflow will help you choose which parameters to modify.

### Environment-level settings

Environment-level settings are those that impact your entire Airflow environment (all DAGs). They all have default values that can be overridden by setting the appropriate environment variable or modifying your `airflow.cfg` file. Generally, all default values can be found in the [Airflow Configuration Reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html). To check current values for an existing Airflow environment, go to **Admin** > **Configurations** in the Airflow UI. For more information, see [Setting Configuration Options](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html) in the Apache Airflow documentation.

If you're running Airflow on Astronomer, you should modify these parameters with Astronomer environment variables. For more information, see [Environment Variables on Astronomer](https://docs.astronomer.io/astro/environment-variables).

You should modify environment-level settings if you want to tune performance across all of the DAGs in your Airflow environment. This is particularly relevant if you want your DAGs to run well on your support infrastructure. 

#### Core Settings

Core settings control the number of processes running concurrently and how long processes run across an entire Airflow environment. The associated environment variables for all parameters in this section are formatted as `AIRFLOW__CORE__PARAMETER_NAME`.

- `parallelism`: The maximum number of tasks that can run concurrently on each scheduler within a single Airflow environment. For example, if this setting is set to 32, and there are two schedulers, then no more than 64 tasks can be in a running or queued state at once across all DAGs. If your tasks remain in a scheduled state for an extended period, you might want to increase this value. The default value is 32. 

    On Astro, this value is [set automatically](https://docs.astronomer.io/astro/configure-worker-queues#worker-autoscaling-logic) based on your maximum worker count, meaning that you don't have to configure it.

- `max_active_tasks_per_dag` (formerly `dag_concurrency`): The maximum number of tasks that can be scheduled at once, per DAG. Use this setting to prevent any one DAG from taking up too many of the available slots from parallelism or your pools. The default value is 16.

  If you increase the amount of resources available to Airflow (such as Celery workers or Kubernetes resources) and notice that tasks are still not running as expected, you might have to increase the values of both `parallelism` and `max_active_tasks_per_dag`.

- `max_active_runs_per_dag`: Determines the maximum number of active DAG runs (per DAG) that the Airflow scheduler can create at a time. In Airflow, a [DAG run](https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html) represents an instantiation of a DAG in time, much like a task instance represents an instantiation of a task. This parameter is most relevant if Airflow needs to backfill missed DAG runs. Consider how you want to handle these scenarios when setting this parameter.  The default value is 16. 

- `dag_file_processor_timeout`: How long a `DagFileProcessor`, which processes a DAG file, can run before timing out. The default value is 50 seconds.

- `dagbag_import_timeout`: How long the `dagbag` can import DAG objects before timing out in seconds, which must be lower than the value set for `dag_file_processor_timeout`. If your DAG processing logs show timeouts, or if your DAG is not showing in the DAGs list or the import errors, try increasing this value. You can also try increasing this value if your tasks aren't executing, since workers need to fill up the `dagbag` when tasks execute. The default value is 30 seconds.

#### Scheduler settings

[Scheduler config settings](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#scheduler) control how the scheduler parses DAG files and creates DAG runs. The associated environment variables for all parameters in this section are formatted as `AIRFLOW__SCHEDULER__PARAMETER_NAME`.

- `min_file_process_interval`: The frequency that each DAG file is parsed, in seconds. Updates to DAGs are reflected after this interval. A low number increases scheduler CPU usage. If you have dynamic DAGs created by complex code, you can increase this value to improve scheduler performance. The default value is 30 seconds. 

- `dag_dir_list_interval`: The frequency that the DAGs directory is scanned for new files, in seconds. The lower the value, the faster new DAGs are processed and the higher the CPU usage. The default value is 300 seconds (5 minutes). 

    It's helpful to know how long it takes to parse your DAGs (`dag_processing.total_parse_time`) to know what values to choose for `min_file_process_interval` and `dag_dir_list_interval`. If your `dag_dir_list_interval` is less than the amount of time it takes to parse each DAG, performance issues can occur. 
  
  :::tip

  If you have less than 200 DAGs in a Deployment on Astro, it's safe to set `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL=30` (30 seconds) as a Deployment-level [environment variable](https://docs.astronomer.io/astro/environment-variables).

  ::: 

- `parsing_processes` (formerly `max_threads`): How many processes the scheduler can run in parallel to parse DAGs. Astronomer recommends setting a value that is twice your available vCPUs. Increasing this value can help serialize a large number of DAGs more efficiently. If you are running multiple schedulers, this value applies to each of them. The default value is 2. 

- `file_parsing_sort_mode`: Determines how the scheduler lists and sorts DAG files to determine the parsing order. Set to one of: `modified_time`, `random_seeded_by_host` and `alphabetical`. The default value is `modified_time`. 

- `scheduler_heartbeat_sec`: Defines how often the scheduler should run (in seconds) to trigger new tasks. The default value is 5 seconds. 

- `max_dagruns_to_create_per_loop`: The maximum number of DAGs to create DAG runs for per scheduler loop. Decrease the value to free resources for scheduling tasks. The default value is 10. 

- `max_tis_per_query`: Changes the batch size of queries to the metastore in the main scheduling loop. A higher value allows more `tis` to be processed per query, but your query may become too complex and cause performance issues. The default value is 16 queries. Note that the `scheduler.max_tis_per_query` value needs to be lower than the `core.parallelism` value.

### DAG-level Airflow settings

DAG-level settings apply only to specific DAGs and are defined in your DAG code. You should modify DAG-level settings if you want to performance tune a particular DAG, especially in cases where that DAG is hitting an external system such as an API or a database that might cause performance issues if hit too frequently. When a setting exists at both the DAG-level and environment-level, the DAG-level setting takes precedence.

There are three primary DAG-level Airflow settings that you can define in code:

- `max_active_runs`: The maximum number of active DAG runs allowed for the DAG. When this limit is exceeded, the scheduler won't create new active DAG runs. If this setting is not defined, the value of the environment-level setting `max_active_runs_per_dag` is assumed.

  If you're utilizing `catchup` or `backfill` for your DAG, consider defining this parameter to ensure that you don't accidentally trigger a high number of DAG runs.
- `max_active_tasks`:** The total number of tasks that can run at the same time for a given DAG run. It essentially controls the parallelism within your DAG. If this setting is not defined, the value of the environment-level setting `max_active_tasks_per_dag` is assumed.
- `concurrency`:** The maximum number of task instances allowed to run concurrently across all active DAG runs for a given DAG. This allows you to allow one DAG to run 32 tasks at once, and another DAG can be set to run 16 tasks at once. If this setting is not defined, the value of the environment-level setting `max_active_tasks_per_dag` is assumed.

You can define any DAG-level settings within your DAG definition. For example:

<Tabs
    defaultValue="taskflow"
    groupId="dag-level-airflow-settings"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
# Allow a maximum of concurrent 10 tasks across a max of 3 active DAG runs
@dag("my_dag_id", concurrency=10, max_active_runs=3)
def my_dag():
```

</TabItem>

<TabItem value="traditional">

```python
# Allow a maximum of concurrent 10 tasks across a max of 3 active DAG runs
with DAG("my_dag_id", concurrency=10, max_active_runs=3):
```

</TabItem>
</Tabs>

### Task-level Airflow settings

Task-level settings are defined by task operators that you can use to implement additional performance adjustments. Modify task-level settings when specific types of tasks are causing performance issues. 

There are two primary task-level Airflow settings users can define in code:

- `max_active_tis_per_dag` (formerly `task_concurrency`): The maximum number of times that the same task can run concurrently across all DAG runs. For instance, if a task pulls from an external resource, such as a data table, that should not be modified by multiple tasks at once, then you can set this value to 1.
- `pool`: Defines the amount of pools available for a task. Pools are a way to limit the number of concurrent instances of an arbitrary group of tasks. This setting is useful if you have a lot of workers or DAG runs in parallel, but you want to avoid an API rate limit or otherwise don't want to overwhelm a data source or destination. For more information, see the [Airflow Pools Guide](airflow-pools.md).

The parameters above are inherited from the `BaseOperator`, so you can set them in any operator definition. For example:


<Tabs
    defaultValue="taskflow"
    groupId="task-level-airflow-settings"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@task(
    pool="my_custom_pool",
    max_active_tis_per_dag=14
) 
def t1():
    pass
```

</TabItem>

<TabItem value="traditional">

```python
def t1_func():
    pass

t1 = PythonOperator(
    task_id="t1",
    python_callable=t1_func,
    pool="my_custom_pool",
    max_active_tis_per_dag=14
)
```

</TabItem>
</Tabs>

## Executors and scaling

Depending on which executor you choose for your Airflow environment, there are additional settings to keep in mind when scaling.

### Celery executor

The [Celery executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html) utilizes standing workers to run tasks. Scaling with the Celery executor involves choosing both the number and size of the workers available to Airflow. The more workers you have available in your environment, or the larger your workers are, the more capacity you have to run tasks concurrently.

You can also tune your `worker_concurrency` (environment variable: `AIRFLOW__CELERY__WORKER_CONCURRENCY`), which determines how many tasks each Celery worker can run at any given time. By default, the Celery executor runs a maximum of sixteen tasks concurrently. If you increase `worker_concurrency`, you might also need to provision additional CPU and/or memory for your workers.   

### Kubernetes executor

The [Kubernetes executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/kubernetes.html) launches a pod in a Kubernetes cluster for each task. Since each task runs in its own pod, resources can be specified on an individual task level.

When tuning performance with the Kubernetes executor, it is important to consider the supporting infrastructure of your Kubernetes cluster. Many users will enable auto-scaling on their cluster to ensure they get the benefit of Kubernetes' elasticity.

You can also tune your `worker_pods_creation_batch_size` (environment variable: `AIRFLOW__KUBERNETES__WORKER_PODS_CREATION_BATCH_SIZE`), which determines how many pods can be created per scheduler loop. The default is 1, but you'll want to increase this number for better performance, especially if you have concurrent tasks. The maximum value is determined by the tolerance of your Kubernetes cluster.

## Potential scaling issues

Scaling your Airflow environment is an art and not a science, and it's highly dependent on your supporting infrastructure and your DAGs. The following are some of the most common issues: 

- Task scheduling latency is high.
    - The scheduler may not have enough resources to parse DAGs in order to then schedule tasks.
    - Change `worker_concurrency` (if using Celery), or `parallelism`.
- DAGs remain in queued state, but are not running.
    - The number of tasks being scheduled may be beyond the capacity of your Airflow infrastructure.
    - If you're using the Kubernetes executor, check that there are available resources in the namespace and check if `worker_pods_creation_batch_size` can be increased. If using the Celery executor, check if `worker_concurrency` can be increased.
- An individual DAG is having trouble running tasks in parallel, while other DAGs are unaffected.
    - Possible DAG-level bottleneck.
    - Change `max_active_task_per_dag`, pools (if using them), or overall `parallelism`.

For help with scaling issues, consider joining the [Apache Airflow Slack](https://airflow.apache.org/community/) or contact [Astronomer support](https://www.astronomer.io/get-astronomer/).
