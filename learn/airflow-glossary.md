---
sidebar_label: 'Airflow glossary'
title: 'Apache Airflow glossary'
id: airflow-glossary
description: A list of key Apache Airflow terms and definitions that can help you learn important concepts.
---

Whether you're new to Airflow or not, use this glossary to quickly reference key Airflow terms, components, and concepts.

| Term | Definition |
|------|-------------|
| Airflow Connection| An [Airflow connection](connections.md) is a set of configurations and credentials that allows Airflow to connect with other tools in the data ecosystem. For example, you need to create a Snowflake connection to access data in Snowflake. |
| Airflow UI| The [Airflow UI](airflow-ui.md) is the primary interface for managing DAG and task runs. You can open and use the Airflow UI in your web browser. It contains pages for modifying, monitoring, and troubleshooting an Airflow environment. |
| Airflow Variable| An [Airflow variable](airflow-variables.md) is a generic key value pair, such as an API key or file path, that's stored in the Airflow metadata database and that you can reference in a DAG. |
| Apache Airflow | Apache Airflow is an open source tool for programmatically authoring, scheduling, and monitoring data pipelines written in Python. Airflow is scalable, configurable, and the industry standard for managing workflows across your ecosystem. |
| Dataset| A [dataset](airflow-datasets.md) is a logical grouping of data consumed or produced by tasks in an Airflow DAG. It can be a table, a file, a blob, or a dataframe. Datasets can be used to schedule DAGs with dataset-driven scheduling. |
| Decorator| In Python, decorators are functions that take another function as an argument and extend the behavior of that function. In Airflow, [decorators](airflow-decorators.md) provide a simpler way to define Airflow tasks and DAGs compared to traditional operators. |
| Deferrable operator | A [deferrable operator](deferrable-operators.md), also known as an async operator, is an operator that suspends itself while waiting for its condition to be met and resumes on receiving the job status. Tasks that use deferrable operators consume worker resources more efficiently because they do not occupy a worker slot when they are in a deferred state. Instead, deferred tasks use the triggerer to poll for job statuses. |
| Task dependency| A task dependency is an instruction that defines whether a task must be completed either before or after another task in the same DAG. Dependencies are defined in DAG code either explicitly with bitshift operators and utility functions or implicitly with the TaskFlow API. The term 'dependency' is often also used to describe a Python or OS-level package. |
| Docker image| An Airflow [Docker image](https://www.techtarget.com/searchitoperations/definition/Docker-image) is a template used to build the Docker containers which run Airflow components and execute DAG code. Both Apache Airflow and Astronomer distribute Docker images for Airflow with different build instructions and pre-installed packages. |
| Dynamic DAG | A [Dynamic DAG](dynamically-generating-dags.md) is a DAG that is generated automatically when the scheduler parses the `dags` folder. You can dynamically create DAGs based on code in one or more Python files or by using tools like `gusty` or `dag-factory`.  |
| Dynamic task | A [Dynamic task](dynamic-tasks.md#dynamic-task-concepts) is a task instance that's generated at runtime based on a set of parameters in DAG code. Dynamic task mapping, the Airflow feature that creates dynamic tasks, allows users to create an arbitrary number of parallel tasks at runtime based on an input parameter. |
| Environment variable| An environment variable is a key-value pair that can be used to define an Airflow environment configuration. This includes Airflow values defined in the airflow.cfg file or any custom value. |
| Executor| An [Executor](airflow-executors-explained.md) is a core process within the Airflow scheduler that is responsible for assigning scheduled tasks to a worker process that will complete the function of a task. Airflow supports multiple executors that you can choose from depending on your use case. |
| Hook| A [hook](what-is-a-hook.md) is an abstraction of a specific API that allows Airflow to interact with an external system. Hooks are built into many operators, but they can also be used directly in DAG code. |
| Jinja Template| [Jinja templating](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html#jinja-templating) is a format that is used to pass dynamic information into task instances at runtime. A jinja templated value is enclosed in double curly braces. |
| Notifier| A [notifier](error-notifications-in-airflow#notifiers) is a custom class that is pre-built into some provider packages and can be used to send notifications to tools like Slack or PagerDuty when a task reaches a particular state. |
| Operator| [Operators](what-is-an-operator) are the building blocks of Airflow DAGs. An operator contains the logic of how data is processed in a pipeline. Each task in a DAG is defined by instantiating an operator. |
| Scheduler| The scheduler is the Airflow component responsible for scheduling job and task instances. It is a multi-threaded Python process that determines what tasks need to be run, when they need to be run, and where they are run. |
| Sensor| An [Airflow Sensor](what-is-a-sensor.md) is a special kind of operator that is designed to wait for something to happen. When sensors run, they check to see if a certain condition is met before they are marked successful and let their downstream tasks execute. |
| Task| A task is the basic unit of execution in Airflow. Tasks are arranged into DAGs, and then have upstream and downstream dependencies set between them to express the order in which they should run. |
| Task group| A [task group](task-groups.md) is a way to visually organize a group of tasks in the Airflow UI. Task groups are defined in DAG code and render as groupings in the **Graph** view of the Airflow UI.  |
| TaskFlow API| The [TaskFlow API](dags.md#writing-dags-with-the-taskflow-api) is a framework for using decorators to define DAGs and tasks. Compared to using traditional operators, using the TaskFlow API simplifies the process for passing data between tasks and defining dependencies. |
| Triggerer| The triggerer is an optional Airflow component responsible for running [deferrable operators](deferrable-operators.md#terms-and-concepts) when they're in a deferred state. |
| Webserver| The webserver is the core Airflow component that serves the Airflow UI. It is a Flask server running with Gunicorn. |
| XCom| [XCom](airflow-passing-data-between-tasks.md#xcom) is a core Airflow feature that allows you to exchange task metadata or small amounts of data between tasks. XComs are defined by a key, value, and timestamp. |
