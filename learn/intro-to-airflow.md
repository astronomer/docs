---
title: "An introduction to Apache Airflow"
sidebar_label: "Introduction to Airflow"
id: intro-to-airflow
description: "Learn what Apache Airflow is and what problems it solves. Get free access to valuable learning resources."
---

import CodeBlock from '@theme/CodeBlock';
import example_astronauts from '!!raw-loader!../code-samples/dags/intro-to-airflow/example_astronauts.py';

[Apache Airflow](https://airflow.apache.org/) is an open source tool for programmatically authoring, scheduling, and monitoring data pipelines. It is downloaded millions of times per month and has a large and active open source community. The core principle of Airflow is to define data pipelines as code, allowing for dynamic and scalable workflows.

This guide offers an introduction to Apache Airflow and its core concepts. You'll learn:

- Milestones in the history of Apache Airflow.
- Why you should use Airflow.
- Common use cases of Airflow.
- Core Airflow concepts.

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Hands-on tutorial: [Get started with Apache Airflow](get-started-with-airflow.md).
- Astronomer Academy: [Airflow 101 Learning Path](https://academy.astronomer.io/path/airflow-101).
- Webinar: [Airflow 101: How to get started writing data pipelines with Apache Airflow](https://www.astronomer.io/events/webinars/intro-to-airflow-get-started-writing-pipelines-for-any-use-case-video/).

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).

## Quickstart

If you already have some Airflow experience 

- Ease of use: With the [Astro CLI](https://docs.astronomer.io/astro/cli/get-started), you can run a local Airflow environment with only three bash commands.


## Milestones

- 2015: Airflow started as an open source project at Airbnb. In 2015, Airbnb was growing rapidly and struggling to manage the vast quantities of internal data it generated every day. To satisfy the need for a robust scheduling tool, [Maxime Beauchemin](https://maximebeauchemin.medium.com/) created Airflow to allow Airbnb to quickly author, iterate, and monitor batch data pipelines.
- 2016: Airflow officially joined the Apache Foundation Incubator.
- 2019: Airflow graduated as a top-level Apache project.
- 2020: Airflow 2.0 was released, bringing with it major upgrades and powerful new features.
- 2020-present: Adoption of Airflow continues to accelerate as the community grows stronger. Consistent releases add new features and improvements.

Airflow has come a long way since Maxime's first commit. As of March 2024, Airflow has over 2,800 contributors, 23,300 commits and 33,700 stars on [GitHub](https://github.com/apache/airflow).

## Why use Airflow

[Apache Airflow](https://airflow.apache.org/index.html) is a platform for programmatically authoring, scheduling, and monitoring workflows. It is especially useful for creating and orchestrating complex data pipelines.

Data orchestration sits at the heart of any modern data stack and provides elaborate automation of data pipelines. With orchestration, actions in your data pipeline become aware of each other and your data team has a central location to monitor, edit, and troubleshoot their workflows.

Airflow provides many benefits, including:

- **Tool agnosticism**: Airflow can connect to any application in your data ecosystem that allows connections through an API and prebuilt modules exist for many common data tools.
- **High extensibility**: Since Airflow pipelines are written in Python, you can build on top of the existing codebase and extend the functionality of Airflow to meet your needs. Anything you can do in Python, you can do in Airflow.
- **CI/CD for data pipelines**: With all the logic of your workflows defined in Python, it is possible to implement best practice CI/CD processes for your data pipelines.
- **Infinite scalability**: Given enough computing power, you can orchestrate as many processes as you need, no matter the complexity of your pipelines.
- **Dynamic data pipelines**: Airflow offers the ability to create [dynamically mapped tasks](dynamic-tasks.md) to adjust your workflows based on the data you are processing at runtime.
- **Active OSS community**: With millions of users and thousands of contributors, Airflow is here to stay and grow. Join the [Airflow Slack](https://apache-airflow-slack.herokuapp.com/) to become part of the community.
- **Observability**: The Airflow UI provides an immediate overview of all your data pipelines and can provide the source of truth for workflows in your whole data ecosystem.

![Screenshot of the main view of the Airflow UI with seven enabled workflows.](/img/guides/intro-to-airflow_data_engineering_prod_overview.png)

## Airflow use cases

Airflow is used by many data professionals with a wide range of backgrounds and use cases in [companies of all sizes and types](https://github.com/apache/airflow/blob/main/INTHEWILD.md). Data engineers, data scientists, ML engineers, and data analysts all need to perform actions on data in a complex web of dependencies. With Airflow you can orchestrate these actions and dependencies in a single platform, no matter which tools you are using and how complex your pipelines are.

![Symbolic graph with Airflow shown as the center of the data ecosystem, with arrows pointing out from Airflow to logos of a variety of common data tools.](/img/guides/intro-to-airflow_airflow_in_ecosystem.png)

Some common use cases of Airflow include:

- **ETL/ELT for analytics**: [90% of Airflow users](https://airflow.apache.org/survey/), use it for Extract-Transform-Load (ETL) and Extract-Load-Transfrom (ELT) patterns related to data analytics, which makes it the most common use case. Often, these pipelines support critical operational processes like regulatory reports. For an example use case, see [ELT with Airflow and dbt Core](use-case-airflow-dbt.md).
- **ETL/ELT for business operations**: 68% of Airflow users have used Airflow to orchestrate data supporting their business directly, creating data-powered applications and products, often in combination with MLOps pipelines. For an example use case, see [The Laurel Algorithm: MLOps, AI, and Airflow for Perfect Timekeeping](https://www.astronomer.io/events/webinars/the-laurel-algorithm-mlops-ai-and-airflow-for-perfect-timekeeping-video/).
- **MLOps**: 28% of Airflow users are already orchestrating Machine Learning Operations (MLOps) with Apache Airflow. For an example use case, see [Use Cohere and OpenSearch to analyze customer feedback in an MLOps pipeline](use-case-llm-customer-feedback.md).
- **Spinning up and down infrastructure**: Airflow can be used to spin up and down infrastructure, for example, to run create and delete temporary tables in a database or spin up and down a Spark cluster. For an example use case, see [Use Airflow setup/ teardown to run data quality checks in an MLOps pipeline](use-case-setup-teardown-data-quality.md).

Of course, these are just a few examples, you can orchestrate almost any kind of batch workflows with Airflow.

## Airflow concepts

To navigate Airflow resources, it is helpful to have a general understanding of the following Airflow concepts.

### Core concepts

- **DAG**: Directed Acyclic Graph. An Airflow DAG is a workflow defined as a graph, where all dependencies between nodes are directed and nodes do not self-reference, meaning there are no circular dependencies. For more information on Airflow DAGs, see [Introduction to Airflow DAGs](dags.md).
- **DAG run**: The execution of a DAG at a specific point in time. A DAG run can be one of four different types: [`scheduled`](scheduling-in-airflow.md), `manual`, [`dataset_triggered`](airflow-datasets.md) or [`backfill`](rerunning-dags.md).
- **Task**: A step in a DAG describing a single unit of work.
- **Task instance**: The execution of a task at a specific point in time.
- **Dynamic task**: An Airflow tasks that serves as a blueprint for a variable number of dynamically mapped tasks created at runtime. For more information, see [Dynamic tasks](dynamic-tasks.md).

The Screenshot below shows one simple DAG called `example_astronauts` with two tasks, `get_astronauts` and `print_astronaut_craft`. The `get_astronauts` task is a regular task, while the `print_astronaut_craft` task is a dynamic task. The grid view of the Airflow UI shows individual DAG runs and task instances, while the graph displays the structure of the DAG. You can learn more about the Airflow UI in [An introduction to the Airflow UI](airflow-ui.md).

![Screenshot of the Airflow UI Grid view with the Graph tab selected showing a DAG graph with a regular and a dynamic task as well as a DAG run and Task instance.](/img/guides/intro-to-airflow_core_concepts_ui.png)

<details>
<summary>Click to view the full DAG code used for the Screenshot</summary>
<div>
    <div><CodeBlock language="python">{example_astronauts}</CodeBlock></div>
</div>
</details>

It is a core best practice to keep tasks as atomic as possible, meaning that each task should perform a single action. Additionally, tasks should be idempotent, which means they produce the same output every time they are run with the same input. See [DAG writing best practices in Apache Airflow](dag-best-practices.md).

### Building blocks

Airflow tasks are defined in Python code. You can define tasks using:

- **Decorators (`@task`)**: The [TaskFlow API](airflow-decorators.md) allows you to define tasks by using a set of decorators that wrap Python functions. This is the easiest way to create tasks from existing Python scripts. Each call to a decorated function becomes one task in your DAG.
- **Operators (`XYZOperator`)**: [Operators](what-is-an-operator.md) are classes abstracting over Python code designed to perform a specific action. You can instantiate an operator by providing the necessary parameters to the class. Each instantiated operator becomes one task in your DAG.

There are a couple of special types of operators that are worth mentioning:

- **Sensors**: [Sensors](what-is-a-sensor.md) are Operators that keep running until a certain condition is fulfilled. For example, the [HttpSensor](https://registry.astronomer.io/providers/apache-airflow-providers-http/versions/latest/modules/HttpSensor) waits for an Http request object to fulfill a user defined set of criteria.
- **Deferrable Operators**: [Deferrable Operators](deferrable-operators.md) use the Python [asyncio](https://docs.python.org/3/library/asyncio.html) library to run tasks asynchronously. For example, the [DateTimeSensorAsync](https://registry.astronomer.io/providers/astronomer-providers/modules/HttpOperatorAsync) waits asynchronously for a specific date and time to occur. Note that your Airflow environment needs to run a triggerer component to use deferrable operators.

Some commonly used building blocks like the BashOperator, the `@task` decorator or the PythonOperator are part of core Airflow and automatically installed in all Airflow instances. Additionally, many operators are maintained separately to Airflow in **Airflow provider packages**, which group modules interacting with a specific service.

You can browse all available operators and find detailed information about their parameters in the [Astronomer Registry](https://registry.astronomer.io/). For many common data tools, there are [integration tutorials](https://docs.astronomer.io/learn/category/integrations) available, showing a simple implementation of the provider package.

### Additional concepts

Of course there is much more to Airflow than just DAGs and tasks. Here are a few additional concepts and features that you are likely to encounter:

- **Airflow scheduling**: Airflow offers a variety of ways to schedule your DAGs. For more information, see [DAG scheduling and timetables in Airflow](scheduling-in-airflow.md).
- **Airflow connections**: Airflow connections offer a way to store credentials and other connection information for external systems and reference them in your DAGs. For more information, see [Manage connections in Apache Airflow](connections.md).
- **Airflow variables**: Airflow variables are key-value pairs that can be used to store information in your Airflow environment. For more information, see [Use Airflow variables](airflow-variables.md).
- **XComs**: XCom is short for "cross-communication", you can use XCom to pass information between your Airflow tasks. For more information, see [Passing data between tasks](airflow-passing-data-between-tasks.md).
- **Airflow REST API**: The [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) allows Airflow to interact with RESTful web services.
- **Airflow plugins**: Airflow plugins are a way to further extend the functionality of Airflow. For more information, see [Airflow plugins](airflow-plugins.md). Note that custom hooks and operators do not need to be installed as plugins, but can be used directly imported into your DAGs as Python modules.

## Airflow components

When working with Airflow, it can be helpful to understand the components of its infrastructure.

The following Airflow components are mandatory for any Airflow installation:

- **Webserver**: A Flask server running with Gunicorn that serves the [Airflow UI](airflow-ui.md).
- **[Scheduler](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html)**: A Daemon responsible for scheduling jobs. This is a multi-threaded Python process that determines what tasks need to be run, when they need to be run, and where they are run.
- **[Database](airflow-database.md)**: A database where all DAG and task metadata are stored. This is typically a Postgres database, but MySQL and SQLite are also supported.
- **[Executor](airflow-executors-explained.md)**: The mechanism that defines how the available computing resources are used to execute tasks. An executor is running within the scheduler whenever Airflow is up.

Additionally, you may also have the following situational components:

- **Triggerer**: A separate process which supports [deferrable operators](deferrable-operators.md). This component is optional and must be run separately.
- **Worker**: The process that executes tasks, as defined by the executor. Depending on which executor you choose, you may or may not have workers as part of your Airflow infrastructure.

To learn more about the Airflow infrastructure, see [Airflow Components](airflow-components.md).

## Resources

- [Astro CLI](https://docs.astronomer.io/astro/cli/get-started): The easiest way to run a local Airflow environment.
- [Astronomer Webinars](https://www.astronomer.io/events/webinars/): Live deep dives into Airflow and Astronomer topics, all previous webinars are available to watch on-demand.
- [Astronomer Learn](https:/docs.astronomer.io/learn/): (you are here!) A collection of guides and tutorials on Airflow. 
- [Astronomer Academy](https://academy.astronomer.io/): In depth video courses on Airflow and Astronomer topics.
- [Astronomer Registry](https://registry.astronomer.io/): A collection of Airflow providers, with detailed information about each provider and its operators, as well as example DAGs showing how to use them.
- [Official Airflow Documentation](https://airflow.apache.org/docs/): The official documentation for Apache Airflow.
- [Airflow GitHub](https://github.com/apache/airflow): The official GitHub repository for Apache Airflow.
- [Airflow Slack](https://apache-airflow-slack.herokuapp.com/): The official Airflow Slack workspace, the best place to ask your Airflow questions!