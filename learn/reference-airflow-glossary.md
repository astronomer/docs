---
sidebar_label: 'Airflow Glossary'
title: 'Airflow Glossary'
id: airflow-glossary
description: Common Airflow terms that will help you understand Airflow concepts.
---


| Term | Definition |
|------|-------------|
| Airflow Connection| Airflow connections are used for storing credentials and other information necessary for connecting to external services. Airflow connections can be created using Airflow UI, Airflow CLI or environment variables. |
| Airflow UI| Airflow UI is a useful tool for understanding, monitoring, and troubleshooting the Airflow DAGs. It provides insights into DAGs and DAG runs.  |
| Airflow Variable| Airflow variables are a generic way to store and retrieve arbitrary content or settings as a simple key value store within Airflow. Airflow variables can be created using Airflow UI, Airflow CLI or environment variables. |
| Apache Airflow | A flexible, mature and modern data orchestration platform for workflows written in Python allowing users to schedule, monitor and integrate  data across their data ecosystem. |
| Dataset| Dataset refers to a logical grouping of data consumed or produced by tasks in an Airflow DAG. It can be a table, a file, a blob or a dataframe. it helps to define dependencies between tasks. |
| Decorator| In Python, decorators are functions that take another function as an argument and extend the behavior of that function. In Airflow, decorators provide a simpler, cleaner way to define Airflow tasks and DAG reducing the boilerplate code required by traditional operators. |
| Dependency| Dependencies in Airflow allow users to create and link atomic tasks allowing users to make flexible DAGs that can follow a certain path based on the state and the order of the tasks. |
| Docker Image| Docker image is a template used to build a Docker container and execute code in it. Airflow relies on Docker and uses the Astro Runtime image as the base to build an Airflow environment. |
| Dynamic DAGs| A Dynamic DAG is generated automatically during the parsing of the DAG file. Parsing could dynamically create different type and number of tasks based on the DAG params for the same DAG or users can use one DAG file to generate multiple DAGs. |
| Environment Variable| Environment variables in Airflow allow users to customize their Airflow environment applying settings like secrets backend, setting worker concurrency etc. Users can customize these settings via Dockerfile or Airflow configuration file. |
| Executor| Executors are the mechanism by which task instances get run. They have a common API and are “pluggable”, meaning users can swap executors based on their installation needs. Only one executor can be configured in Airflow at any given time. |
| Hook| A hook is an abstraction of a specific API that allows Airflow to interact with an external system. Hooks are built into many operators, but they can also be used directly in DAG code. See [Hook basics](https://docs.astronomer.io/learn/what-is-a-hook) to learn more about hooks. |
| Jinja Template| Jinja templating allows users to pass dynamic information into task instances at runtime. The code needs to be evaluated can be enclosed between double curly braces, and the expression is evaluated at runtime. See [Jinja templating](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html#jinja-templating) for more details. |
| Notifier| Pre-built custom classes that can be used to standardize and modualrize functions used to send notifications. This allows user to define and share functionality used in callback functions as Airflow modules. Available in Astro Runtime 8.1.0+. |
| Operator| Operators are the building blocks of Airflow DAGs. They contain the logic of how data is processed in a pipeline. Each task in a DAG is defined by instantiating an operator. See [Operator basics](https://docs.astronomer.io/learn/what-is-an-operator) to learn more about operators. |
| Scheduler| A Daemon responsible for scheduling jobs. This is a multi-threaded Python process that determines what tasks need to be run, when they need to be run, and where they are run. |
| Sensor| Airflow Sensors are a special kind of operator that are designed to wait for something to happen. When sensors run, they check to see if a certain condition is met before they are marked successful and let their downstream tasks execute. See [Sensor basics](https://docs.astronomer.io/learn/what-is-a-sensor) to learn more about sensors. |
| Task| A Task is the basic unit of execution in Airflow. Tasks are arranged into DAGs, and then have upstream and downstream dependencies set between them into order to express the order they should run in. |
| Task Group| A TaskGroup can be used to organize tasks into hierarchical groups in Graph view. It is useful for creating repeating patterns and cutting down visual clutter. TaskGroup is purely a UI grouping concept. Tasks in TaskGroups live on the same original DAG, and honor all the DAG settings and pool configurations. |
| TaskFlow API| TaskFlow API uses Python decorators to render them as Airflow tasks. It also handles passing data between tasks using XCom and inferring task dependencies automatically. |
| Triggerer| A process which supports deferrable operators. This component is optional and must be run separately. It is needed only if there is a plan to use deferrable (or "asynchronous") operators. |
| Webserver| A Flask server running with Gunicorn that serves the Airflow UI. |
| XCom| XCom is a built-in Airflow feature. XComs allow tasks to exchange task metadata or small amounts of data. They are defined by a key, value, and timestamp. See [Passing data between tasks](https://docs.astronomer.io/learn/airflow-passing-data-between-tasks#xcom) for details. |