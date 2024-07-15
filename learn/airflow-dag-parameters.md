---
title: "DAG-level parameters in Apache Airflow®" 
sidebar_label: "DAG parameters"
id: airflow-dag-parameters
description: "Learn about all important DAG-level parameters in Apache Airflow®."
---

In Apache Airflow®, you can configure when and how your DAG runs by setting parameters in the DAG object. DAG-level parameters affect how the entire DAG behaves, as opposed to task-level parameters which only affect a single task or [Apache Airflow® configs](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html) which affect the entire Airflow instance. 

This guide covers all user-relevant DAG-level parameters in Airflow.

## Basic DAG-level parameters

There are four basic DAG-level parameters. It is best practice to always set these parameters in any DAG:

| Parameter                           | Description |
|-------------------------------------|-------------|
| `dag_id`                           | The name of the DAG. This must be unique for each DAG in the Airflow environment. When using the `@dag` decorator and not providing the `dag_id` parameter name, the function name is used as the `dag_id`. When using the `DAG` class, this parameter is required. |
| `start_date` | The date and time after which the DAG starts being scheduled. Note that the first actual run of the DAG may be later than this date depending on how you define the schedule. See [DAG scheduling and timetables in Apache Airflow®](scheduling-in-airflow.md) for more information. This parameter may be required depending on your Airflow version and `schedule`. |
| `schedule`   | The schedule for the DAG. There are many different ways to define a schedule, see [Scheduling in Apache Airflow®](scheduling-in-airflow.md) for more information. Defaults to `timedelta(days=1)`. This parameter replaces the deprecated `schedule_interval` and `timetable` parameters. |
| `catchup`    | Whether the scheduler should backfill all missed DAG runs between the current date and the start date when the DAG is unpaused. This parameter defaults to `True`. It is a best practice to always set it to `False` unless you specifically want to backfill missed DAG runs, see [Catchup](rerunning-dags.md#catchup) for more information. |

## UI parameters

Some parameters [add documentation](custom-airflow-ui-docs-tutorial.md) to a DAG or change its appearance in the Airflow UI:

| Parameter                           | Description |
|-------------------------------------|-------------|
| `description`                       | A short string that is displayed in the Airflow UI next to the DAG name. |
| `doc_md`        | A string that is rendered as [DAG documentation](custom-airflow-ui-docs-tutorial.md) in the Airflow UI. Tip: use `__doc__` to use the docstring of the Python file. It is a best practice to give all your DAGs a descriptive DAG documentation. |
| `owner_links`   | A dictionary with the key being the DAG owner and the value being a URL to link to when clicking on the owner in the Airflow UI. Commonly used as a mailto link to the owner's email address. Note that the `owner` parameter is set at the task level, usually by defining it in the `default_args` dictionary. |
| `tags`          | A list of tags shown in the Airflow UI to help with filtering DAGs. |
| `default_view`  | The default view of the DAG in the Airflow UI. Defaults to `grid`. |
| `orientation`   | The orientation of the DAG graph in the Airflow UI. Defaults to `LR` (left to right). |

## Jinja templating parameters

There are parameters that relate to [Jinja templating](templating.md), such as:

| Parameter                           | Description |
|-------------------------------------|-------------|
| `template_searchpath`               | A list of folders where Jinja looks for templates. The path of the DAG file is included by default. |
| `template_undefined`             | The behavior of Jinja when a variable is undefined. Defaults to [StrictUndefined](https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.StrictUndefined). |
| `render_template_as_native_obj`     | Whether to render Jinja templates as native Python objects instead of strings. Defaults to `False`. |
| `user_defined_macros`            | A dictionary of macros that are available in the DAG's Jinja templates. Use `user_defined_filters` to add filters and `jinja_environment_kwargs` for additional Jinja configuration. See [Macros: using custom functions and variables in templates](templating.md#macros-using-custom-functions-and-variables-in-templates). |

## Scaling

Some parameters can be used to scale your DAG's resource usage in Airflow. See [Scaling Apache Airflow® to optimize performance](airflow-scaling-workers.md) for more information.

| Parameter                           | Description |
|-------------------------------------|-------------|
| `max_active_tasks`                  | The number of task instances allowed to run concurrently for all DAG runs of this DAG. This parameter replaces the deprecated `concurrency`. |
| `max_active_runs`                   | The number of active DAG runs allowed to run concurrently for this DAG. |
| `max_consecutive_failed_dag_runs`   | (experimental, added in Airflow 2.9) The maximum number of consecutive failed DAG runs, after which the scheduler will disable this DAG. |

## Callback parameters

These parameters help you configure the behavior of [Apache Airflow® callbacks](error-notifications-in-airflow.md#airflow-callbacks).

| Parameter                           | Description |
|-------------------------------------|-------------|
| `on_success_callback`                  | A function to be executed after completion of a successful DAG run. |
| `on_failure_callback`                   | A function to be executed after a failed DAG run. |
| `sla_miss_callback`   | A function to be executed when a DAG misses its defined [Service Level Agreement (SLA)](error-notifications-in-airflow.md#airflow-service-level-agreements) |


:::tip

On Astro, you can use Astro alerts instead of or in addition to Airflow callbacks. See [When to use Apache Airflow® or Astro alerts for your pipelines on Astro](https://www.astronomer.io/docs/astro/best-practices/airflow-vs-astro-alerts) for more information.

:::

## Other parameters

Other DAG parameters include:

| Parameter                           | Description |
|-------------------------------------|-------------|
| `end_date`                          | The date beyond which no further DAG runs will be scheduled. Defaults to `None`. |
| `default_args`            | A dictionary of parameters that are applied to all tasks in the DAG. These parameters are passed directly to each operator, so they must be parameters that are part of the [`BaseOperator`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html). You can override default arguments at the task level. |
| `params`                  | A dictionary of DAG-level Airflow params. See [Apache Airflow® params](airflow-params.md) for more information. |
| `dagrun_timeout`          | The time it takes for a DAG run of this DAG to time out and be marked as `failed`. |
| `access_control`          | Specify optional permissions for roles specific to an individual DAG. See [DAG-level permissions](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#dag-level-permissions). This cannot be implemented on Astro. Astronomer recommends customers to use [Astro's RBAC features](https://www.astronomer.io/docs/astro/user-permissions) instead. |
| `is_paused_upon_creation` | Whether the DAG is paused when it is created. When not set, the Airflow config `core.dags_are_paused_at_creation` is used, which defaults to `True`. |
| `auto_register`           | Defaults to `True` and can be set to `False` to prevent DAGs using a `with` context from being automatically registered which can be relevant in some advanced dynamic DAG generation use cases. See [Registering dynamic DAGs](https://airflow.apache.org/docs/apache-airflow/stable/howto/dynamic-dag-generation.html#registering-dynamic-dags). |
| `fail_stop`               |  In Airflow 2.7+, you can set this parameter to `True` to stop DAG execution as soon as one task in this DAG fails. Any tasks that are still running are marked as `failed`, and any tasks that have not run yet are marked as `skipped`. Note that you cannot have any [trigger rule](airflow-trigger-rules.md) other than `all_success` in a DAG with `fail_stop` set to `True`. |
| `dag_display_name`        | Airflow 2.9+ allows you to override the `dag_id` to display a different DAG name in the Airflow UI. This parameter allows special characters. |