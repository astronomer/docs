---
title: "DAG writing best practices in Apache Airflow"
sidebar_label: "DAG writing best practices"
id: dag-best-practices
---

<head>
  <meta name="description" content="Keep up to date with the best practices for developing efficient, secure, and scalable DAGs using Airflow. Learn about DAG design and data orchestration." />
  <meta name="og:description" content="Keep up to date with the best practices for developing efficient, secure, and scalable DAGs using Airflow. Learn about DAG design and data orchestration." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import bad_practices_dag_1 from '!!raw-loader!../code-samples/dags/dag-best-practices/bad_practices_dag_1.py';
import bad_practices_dag_2 from '!!raw-loader!../code-samples/dags/dag-best-practices/bad_practices_dag_2.py';
import good_practices_dag_1 from '!!raw-loader!../code-samples/dags/dag-best-practices/good_practices_dag_1.py';
import good_practices_dag_2 from '!!raw-loader!../code-samples/dags/dag-best-practices/good_practices_dag_2.py';

Because Airflow is 100% code, knowing the basics of Python is all it takes to get started writing DAGs. However, writing DAGs that are efficient, secure, and scalable requires some Airflow-specific finesse. In this guide, you'll learn how you can develop DAGs that make the most of what Airflow has to offer.

In general, best practices fall into one of two categories: 

- DAG design
- Using Airflow as an orchestrator

For an in-depth walk through and examples of some of the concepts covered in this guide, it's recommended that you review the [DAG Writing Best Practices in Apache Airflow](https://www.astronomer.io/blog/dag-writing-best-practices-in-apache-airflow) webinar and the [Github repo](https://github.com/astronomer/webinar-dag-writing-best-practices) for DAG examples.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## Review idempotency

[Idempotency](https://en.wikipedia.org/wiki/Idempotence) is the foundation for many computing practices, including the Airflow best practices in this guide. A program is considered idempotent if, for a set input, running the program once has the same effect as running the program multiple times.

In the context of Airflow, a DAG is considered idempotent if rerunning the same DAG Run with the same inputs multiple times has the same effect as running it only once. This can be achieved by designing each individual task in your DAG to be idempotent. Designing idempotent DAGs and tasks decreases recovery time from failures and prevents data loss.

## DAG design

The following DAG design principles will help to make your DAGs idempotent, efficient, and readable.

### Keep tasks atomic

When organizing your pipeline into individual tasks, each task should be responsible for one operation that can be re-run independently of the others. In an atomized task, a success in part of the task means a success of the entire task. 

For example, in an ETL pipeline you would ideally want your Extract, Transform, and Load operations covered by three separate tasks. Atomizing these tasks allows you to rerun each operation in the pipeline independently, which supports idempotence.

### Use template fields, variables, and macros

By using templated fields in Airflow, you can pull values into DAGs using environment variables and jinja templating. Compared to using Python functions, using templated fields helps keep your DAGs idempotent and ensures you aren't executing functions on every Scheduler heartbeat. See [Avoid top level code in your DAG file](#avoid-top-level-code-in-your-dag-file).

Contrary to our best practices, the following example defines variables based on `datetime` Python functions:

```python
# Variables used by tasks
# Bad example - Define today's and yesterday's date using datetime module
today = datetime.today()
yesterday = datetime.today() - timedelta(1)
```

If this code is in a DAG file, these functions are executed on every Scheduler heartbeat, which may not be performant. Even more importantly, this doesn't produce an idempotent DAG. You can't rerun a previously failed DAG run for a past date because `datetime.today()` is relative to the current date, not the DAG execution date. 

A better way of implementing this is by using an Airflow variable:

```python
# Variables used by tasks
# Good example - Define yesterday's date with an Airflow variable
yesterday = {{ yesterday_ds_nodash }}
```

You can use one of the Airflow built-in [variables and macros](https://airflow.apache.org/docs/apache-airflow/stable/macros-ref.html), or you can create your own templated field to pass information at runtime. For more information on this topic, see [templating and macros in Airflow](templating.md).

### Incremental record filtering

You should break out your pipelines into incremental extracts and loads wherever possible. For example, if you have a DAG that runs hourly, each DAG run should process only records from that hour, rather than the whole dataset. When the results in each DAG run represent only a small subset of your total dataset, a failure in one subset of the data won't prevent the rest of your DAG Runs from completing successfully. If your DAGs are idempotent, you can rerun a DAG for only the data that failed rather than reprocessing the entire dataset. 

There are multiple ways you can achieve incremental pipelines.

#### Last modified date

Using a last modified date is recommended for incremental loads. Ideally, each record in your source system has a column containing the last time the record was modified. With this design, a DAG run looks for records that were updated within specific dates from this column.

For example, with a DAG that runs hourly, each DAG run is responsible for loading any records that fall between the start and end of its hour. If any of those runs fail, it doesn't affect other Runs.

#### Sequence IDs

When a last modified date is unavailable, a sequence or incrementing ID can be used for incremental loads. This logic works best when the source records are only being appended to and not updated. Although implementing a last modified date system in your records is considered best practice, basing your incremental logic off of a sequence ID can be a sound way to filter pipeline records without a last modified date.

### Avoid top-level code in your DAG file

In the context of Airflow, top-level code refers to any code that is run at the time the DAG is parsed, as opposed to the time the task is run.

Code that is part of an operator or a decorated task is run by Airflow only when the tasks runs, not  when the DAG is parsed. For example, in the following code, `call_external_systems()` is considered top-level code because it runs when the DAG is parsed. `x + y` is not top-level code, because it is part of the task definition and only runs when the task runs.

```python
@dag(...)
def the_dag():
    
    @task
    def do_thing():
        x + y

    num_of_things = call_external_system()    # this is "top level code"
    
    
    chain(do_thing() for _ in range(num_of_things))

my_dag = the_dag()

```

Generally, any code that isn't part of your DAG or operator instantiations and that makes requests to external systems is of concern. Airflow executes all code in the `dags_folder` on every [`min_file_process_interval`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#min-file-process-interval), which defaults to 30 seconds. Therefore, any code that is run when the DAG is parsed and makes requests to external systems, like an API or a database, or makes function calls outside of your tasks can cause performance issues since these requests and connections are being made every 30 seconds rather than only when the DAG is scheduled to run. 

To see another example, the following DAG example dynamically generates tasks using the PostgresOperator based on records pulled from a different database. 

In the **Bad practice** example the connection to the other database is made outside of an operator instantiation as top-level code. When the scheduler parses this DAG, it will use the `hook` and `result` variables to query the `grocery_list` table. This query is run every time the DAG is parsed, which can cause performance issues. 

The version shown under the **Good practice** DAG wraps the connection to the database into its own task, the `get_list_of_results` task. Now the connection is only made at when the DAG actually runs, preventing performance issues.

<Tabs
    defaultValue="good-practice"
    groupId="avoid-top-level-code-in-your-dag-file"
    values={[
        {label: 'Bad practice', value: 'bad-practice'},
        {label: 'Good practice', value: 'good-practice'},
    ]}>

<TabItem value="bad-practice">

<CodeBlock language="python">{bad_practices_dag_1}</CodeBlock>

</TabItem>

<TabItem value="good-practice">

<CodeBlock language="python">{good_practices_dag_1}</CodeBlock>

</TabItem>
</Tabs>


### Treat your DAG file like a config file

Including code that isn't part of your DAG or operator instantiations in your DAG file makes the DAG harder to read, maintain, and update. When possible, leave all of the heavy lifting to the hooks and operators that you instantiate within the file. If your DAGs need to access additional code such as a SQL script or a Python function, consider keeping that code in a separate file that can be read into a DAG run.

The following example DAGs demonstrate the difference between the bad and good practices of including code in your DAGs. In the **Bad practice** DAG, a SQL query is provided directly to the PostgresOperator, which unnecessarily exposes code in your DAG. In the **Good practice** DAG, the DAG-level configuration includes `template_searchpath` and the PostgresOperator specifies a `covid_state_query.sql` file that contains the query to execute.

<Tabs
    defaultValue="good-practice"
    groupId="treat-your-dag-file-like-a-config-file"
    values={[
        {label: 'Bad practice', value: 'bad-practice'},
        {label: 'Good practice', value: 'good-practice'},
    ]}>

<TabItem value="bad-practice">

<CodeBlock language="python">{bad_practices_dag_2}</CodeBlock>

</TabItem>

<TabItem value="good-practice">

<CodeBlock language="python">{good_practices_dag_2}</CodeBlock>

</TabItem>
</Tabs>

### Use a consistent method for task dependencies

In Airflow, task dependencies can be set multiple ways. You can use `set_upstream()` and `set_downstream()` functions, or you can use `<<` and `>>` operators. Which method you use is a matter of personal preference, but for readability it's best practice to choose one method and use it consistently.

For example, instead of mixing methods like this:

```python
task_1.set_downstream(task_2)
task_3.set_upstream(task_2)
task_3 >> task_4
```

Try to be consistent with something like this:

```python
task_1 >> task_2 >> [task_3, task_4]
```

## Leverage Airflow features

To get the most out of Airflow, leverage built-in features and the broader Airflow ecosystem, namely provider packages for third-party integrations, to fulfill specific use cases. Using Airflow in this way makes it easier to scale and pull in the right tools based on your needs.

### Make use of provider packages

One of the best aspects of Airflow is its robust and active community, which has resulted in integrations between Airflow and other tools known as [provider packages](https://airflow.apache.org/docs/apache-airflow-providers/). 

Provider packages let you orchestrate third party data processing jobs directly from Airflow. Wherever possible, it's recommended that you make use of these integrations rather than writing Python functions yourself. This makes it easier for organizations using existing tools to adopt Airflow, and you don't have to write new code.

For more information about the available provider packages, see the [Astronomer Registry](https://registry.astronomer.io/).

### Decide where to run data processing jobs

There are many options available for implementing data processing. For small to medium scale workloads, it is typically safe to do your data processing within Airflow as long as you allocate enough resources to your Airflow infrastructure. Large data processing jobs are typically best offloaded to a framework specifically optimized for those use cases, such as [Apache Spark](https://spark.apache.org/). You can then use Airflow to orchestrate those jobs.

Astronomer recommends that you consider the size of your data now and in the future when deciding whether to process data within Airflow or offload to an external tool. Follow these recommendations if your use case is well suited to processing data within Airflow:

- Ensure your Airflow infrastructure has the necessary resources.
- Use the Kubernetes Executor to isolate task processing and have more control over resources at the task level.
- Use a [custom XCom backend](custom-xcom-backends-tutorial.md) if you need to pass any data between the tasks so you don't overload your metadata database.

### Use intermediary data storage

Because it requires less code and fewer pieces, it can be tempting to write your DAGs to move data directly from your source to destination. However, this means you can't individually rerun the extract or load portions of the pipeline. By putting an intermediary storage layer such as Amazon S3 or SQL Staging tables in between your source and destination, you can separate the testing and rerunning of the extract and load.

Depending on your data retention policy, you could modify the load logic and rerun the entire historical pipeline without having to rerun the extracts. This is also useful in situations where you no longer have access to the source system such as hitting an API limit.

### Use the right tool for the job

Airflow excels at course-grain parallellism. If you need to do large scale transformations or fine-grain parallelism, consider using Airflow to trigger other data processing frameworks.

## Other best practices

Here are a few other noteworthy best practices that you should follow.

### Use a consistent file structure

Having a consistent file structure for Airflow projects keeps things organized and easy to adopt. This is the structure that Astronomer uses:

```bash
├── dags/ # Where your DAGs go
│   └── example-dag.py # An example dag that comes with the initialized project
├── Dockerfile # For Astronomer's Docker image and runtime overrides
├── include/ # For any other files you'd like to include
├── plugins/ # For any custom or community Airflow plugins
├── packages.txt # For OS-level packages
└── requirements.txt # For any Python packages

```

### Use DAG name and start date properly

You should always use a static `start_date` with your DAGs. A dynamic `start_date` is misleading, and can cause failures when clearing out failed task instances and missing DAG runs.

Additionally, if you change the `start_date` of your DAG you should also change the DAG name. Changing the `start_date` of a DAG creates a new entry in the Airflow database. This can confuse the Scheduler because there are two DAGs with the same name but different schedules.

Changing the name of a DAG also creates a new entry in the database that powers the dashboard. Follow a consistent naming convention since changing a DAG's name doesn't delete the entry in the database for the old name.

### Set retries

In a distributed environment where task containers are executed on shared hosts, it's possible for tasks to be killed off unexpectedly. When this happens, you might see  a [zombie process](https://en.wikipedia.org/wiki/Zombie_process) in the Airflow logs.

You can resolve issues like zombies by using task retries. Retries can be set at different levels with the following precedence:
1. **Tasks:**  Pass the `retries` parameter to the task's Operator.
2. **DAGs:** Include `retries` in a DAG's `default_args` object.
3. **Deployments:** Set the environment variable `AIRFLOW__CORE__DEFAULT_TASK_RETRIES`.

Setting retries to `2` will protect a task from most problems common to distributed environments. For more on using retries, see [Rerun DAGs and Tasks](rerunning-dags.md).
