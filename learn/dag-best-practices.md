---
title: "DAG writing best practices in Apache Airflow"
sidebar_label: "DAG writing best practices"
id: dag-best-practices
---

<head>
  <meta name="description" content="Keep up to date with the best practices for developing efficient, secure, and scalable DAGs using Airflow. Learn about DAG design and data orchestration." />
  <meta name="og:description" content="Keep up to date with the best practices for developing efficient, secure, and scalable DAGs using Airflow. Learn about DAG design and data orchestration." />
</head>

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

In the context of Airflow, top-level code refers to any code that isn't part of your DAG or operator instantiations, particularly code making requests to external systems.

Airflow executes all code in the `dags_folder` on every `min_file_process_interval`, which defaults to 30 seconds. You can read more about this parameter in the [Airflow docs](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#min-file-process-interval)). Because of this, top-level code that makes requests to external systems, like an API or a database, or makes function calls outside of your tasks can cause performance issues since these requests and connections are being made every 30 seconds rather than only when the DAG is scheduled to run. 

The following DAG example dynamically generates `PostgresOperator` tasks based on records pulled from a database. For example, the `hook` and `result` variables which are written outside of an operator instantiation:

```python
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

hook = PostgresHook('database_conn')
result = hook.get_records("SELECT * FROM grocery_list;")

with DAG('bad_practices_dag_1',
         start_date=datetime(2021, 1, 1),
         max_active_runs=3,
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False
         ) as dag:

    for grocery_item in result:
        query = PostgresOperator(
            task_id='query_{0}'.format(result),
            postgres_conn_id='postgres_default',
            sql="INSERT INTO purchase_order VALUES (value1, value2, value3);"
        )
```

When the scheduler parses this DAG, it will use the `hook` and `result` variables to query the `grocery_list` table to construct the operators in the DAG. This query is run on every Scheduler heartbeat, which can cause performance issues. A better implementation leverages [dynamic task mapping](dynamic-tasks.md) to have a task that gets the required information from the `grocery_list` table and dynamically maps downstream tasks based on the result. Dynamic task mapping is available in Airflow 2.3 and later.

### Treat your DAG file like a config file

Including code that isn't part of your DAG or operator instantiations in your DAG file makes the DAG harder to read, maintain, and update. When possible, leave all of the heavy lifting to the hooks and operators that you instantiate within the file. If your DAGs need to access additional code such as a SQL script or a Python function, consider keeping that code in a separate file that can be read into a DAG run.

The following example DAG demonstrates what you shouldn't do. A SQL query is provided directly in the `PostgresOperator` `sql` param:

```python
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

#Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

#Instantiate DAG
with DAG('bad_practices_dag_2',
         start_date=datetime(2021, 1, 1),
         max_active_runs=3,
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False
         ) as dag:

    t0 = EmptyOperator(task_id='start')  

    #Bad example with SQL query directly in the DAG file
    query_1 = PostgresOperator(
        task_id='covid_query_wa',
        postgres_conn_id='postgres_default',
        sql='''WITH yesterday_covid_data AS (
                SELECT *
                FROM covid_state_data
                WHERE date = {{ params.today }}
                AND state = 'WA'
            ),
            today_covid_data AS (
                SELECT *
                FROM covid_state_data
                WHERE date = {{ params.yesterday }}
                AND state = 'WA'
            ),
            two_day_rolling_avg AS (
                SELECT AVG(a.state, b.state) AS two_day_avg
                FROM yesterday_covid_data AS a
                JOIN yesterday_covid_data AS b 
                ON a.state = b.state
            )
            SELECT a.state, b.state, c.two_day_avg
            FROM yesterday_covid_data AS a
            JOIN today_covid_data AS b
            ON a.state=b.state
            JOIN two_day_rolling_avg AS c
            ON a.state=b.two_day_avg;''',
            params={'today': today, 'yesterday':yesterday}
    )
```

Keeping the query in the DAG file like this makes the DAG harder to read and maintain. In the following DAG, the DAG-level configuration includes `template_searchpath` and the `PostgresOperator` specifies a `covid_state_query.sql` file that contains the same query as in the previous example:

```python
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

#Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

#Instantiate DAG
with DAG('good_practices_dag_1',
         start_date=datetime(2021, 1, 1),
         max_active_runs=3,
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False,
         template_searchpath='/usr/local/airflow/include' #include path to look for external files
         ) as dag:

        query = PostgresOperator(
            task_id='covid_query_{0}'.format(state),
            postgres_conn_id='postgres_default',
            sql='covid_state_query.sql', #reference query kept in separate file
            params={'state': "'" + state + "'"}
        )
```

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
- Use a [custom XCom backend](custom-xcom-backends.md) if you need to pass any data between the tasks so you don't overload your metadata database.

### Use intermediary data storage

Because it requires less code and fewer pieces, it can be tempting to write your DAGs to move data directly from your source to destination. However, this means you can't individually rerun the extract or load portions of the pipeline. By putting an intermediary storage layer such as Amazon S3 or SQL Staging tables in between your source and destination, you can separate the testing and rerunning of the extract and load.

Depending on your data retention policy, you could modify the load logic and rerun the entire historical pipeline without having to rerun the extracts. This is also useful in situations where you no longer have access to the source system such as hitting an API limit.

### Use an ELT framework

Whenever possible, look to implement an ELT (extract, load, transform) data pipeline pattern with your DAGs. This means that you should look to offload as much of the transformation logic to the source systems or the destination systems as possible, to leverage the strength of all tools in your data ecosystem. Many modern data warehouse tools, such as [Snowflake](https://www.snowflake.com/), give you easy access to the ELT framework, and are easily used in conjunction with Airflow.

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

### Set retries at the DAG level

In a distributed environment where task containers are executed on shared hosts, it's possible for tasks to be killed off unexpectedly. When this happens, you might see  a [zombie process](https://en.wikipedia.org/wiki/Zombie_process) in the Airflow logs.

Issues like this can be resolved by using task retries. The best practice is to set retries as a `default_arg` so they are applied at the DAG level and get more granular for specific tasks only where necessary. A good range is ~2–4 retries.
