---
sidebar_label: 'Glossary'
title: 'Airflow glossary'
id: airflow-glossary
description: A list of Airflow terms and definitions that can help you learn or brush up on key Airflow concepts.
---
Whether you're new to Airflow or a DAG-writing pro, use this glossary as a quick reference for key Airflow terms, components, and concepts.

| Term | Definition |
|------|-------------|
| Airflow Connection| An [Airflow connection](connections.md) is a set of configurations and credentials that allows Airflow to connect with other tools in the data ecosystem. |
| Airflow UI| The [Airflow UI](airflow-ui.md) is the primary interface for managing DAG and task runs. It contains pages for understanding, monitoring, and troubleshooting a running Airflow environment. |
| Airflow Variable| An Airflow variable is a generic key value pair that's stored in the Airflow metadata database. |
| Apache Airflow | Apache Airflow is a flexible, mature and modern data orchestration platform for data workflows written in Python. Airflow is used to schedule, monitor, and integrate data pipelines across the data ecosystem. |
| Dataset| A [dataset](airflow-datasets.md) is a logical grouping of data consumed or produced by tasks in an Airflow DAG. It can be a table, a file, a blob, or a dataframe. Datasets can be used to schedule DAGs with dataset-driven scheduling. |
| Decorator| In Python, decorators are functions that take another function as an argument and extend the behavior of that function. In Airflow, [decorators](airflow-decorators.md) provide a simpler way to define Airflow tasks and DAGs compared to traditional operators. |
| Deferrable operators | A [deferrable operator](deferrable-operators.md), also known as an async operator, is an operator thats suspends itself while waiting for a job status and resumes on receiving the job status. Tasks that use deferrable operators don't occupy a worker slot when they are in a deferred state. Instead, deferred tasks use the triggerer to poll for job statuses. |
| Dependency| A dependency is an instruction that defines whether a task must be completed either before or after another task in the same DAG. Dependencies are defined in DAG code either explicitly with bitshift operators or implicitly through the TaskFlow API. |
| Docker image| An Airflow [Docker image](https://www.techtarget.com/searchitoperations/definition/Docker-image) is a template used to build the Docker containers which run Airflow components and execute DAG code. Both Apache Airflow and Astronomer distribute Docker images for Airflow with different dependencies and build instructions. |
| Dynamic DAG | A [Dynamic DAG](dynamically-generating-dags.md) is a DAG instance that is generated automatically during the parsing of the DAG file. |
| Dynamic task | A [Dynamic task](dynamic-tasks#dynamic-task-concepts) is a task instance that's generated at runtime based on a set of parameters in DAG code. Dynamic task mapping, the Airflow feature that creates dynamic tasks, allows users to create an arbitrary number of parallel tasks at runtime based on an input parameter. |
| Environment variable| An environment variable is a key-value pair that can be used to define an Airflow environment configuration. |
| Executor| An [Executor](airflow-executors-explained.md) is the Airflow component that's responsible for running the work contained within tasks. |
| Hook| A [hook](what-is-a-hook) is an abstraction of a specific API that allows Airflow to interact with an external system. Hooks are built into many operators, but they can also be used directly in DAG code. |
| Jinja Template| [Jinja templating](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html#jinja-templating) is a format that is used to pass dynamic information into task instances at runtime. A jinja templated value is enclosed in double curly braces. |
| Notifier| A [notifier](error-notifications-in-airflow#notifiers) is a custom class that can be used to standardize and modularize functions for sending notifications from tasks. |
| Operator| [Operators](what-is-an-operator) are the building blocks of Airflow DAGs. They contain the logic of how data is processed in a pipeline. Each task in a DAG is defined by instantiating an operator. |
| Scheduler| The scheduler is the Airflow component responsible for scheduling job and task instances. It is a multi-threaded Python process that determines what tasks need to be run, when they need to be run, and where they are run. |
| Sensor| An [Airflow Sensor](what-is-a-sensor) is a special kind of operator that is designed to wait for something to happen. When sensors run, they check to see if a certain condition is met before they are marked successful and let their downstream tasks execute. |
| Task| A task is the basic unit of execution in Airflow. Tasks are arranged into DAGs, and then have upstream and downstream dependencies set between them to express the order in which they should run. |
| Task group| A [task group](task-groups.md) is a way to visually organize a group of tasks in the Airflow UI. Task groups are defined in DAG code and render as groupings in the **Graph** view of the Airflow UI.  |
| TaskFlow API| The [TaskFlow API](dags.md#writing-dags-with-the-taskflow-api) is a framework for using decorators to define DAGs and tasks. Compared to using traditional operators, using the TaskFlow API simplifies the process for passing data between tasks and defining dependencies. |
| Triggerer| The triggerer is an optional Airflow component responsible for running [deferrable operators](deferrable-operators#terms-and-concepts) when they're in a deferred state. |
| Webserver| The webserver is a Flask server running with Gunicorn that serves the Airflow UI. |
| XCom| [XCom](airflow-passing-data-between-tasks#xcom) is a built-in Airflow feature. XComs allow tasks to exchange task metadata or small amounts of data. They are defined by a key, value, and timestamp. |