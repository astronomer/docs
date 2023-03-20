---
title: "Airflow operators"
sidebar_label: "Operators"
id: what-is-an-operator
---

<head>
  <meta name="description" content="Learn the basics of operators, which are the building blocks of Airflow DAGs. See an example of how to implement several common operators available in Apache Airflow." />
  <meta name="og:description" content="Learn the basics of operators, which are the building blocks of Airflow DAGs. See an example of how to implement several common operators available in Apache Airflow." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import operator_example_taskflow from '!!raw-loader!../code-samples/dags/what-is-an-operator/operator_example_taskflow.py';
import operator_example_traditional from '!!raw-loader!../code-samples/dags/what-is-an-operator/operator_example_traditional.py';

Operators are the building blocks of Airflow DAGs. They contain the logic of how data is processed in a pipeline. Each task in a DAG is defined by instantiating an operator.

There are many different types of operators available in Airflow. Some operators such as Python functions execute general code provided by the user, while other operators perform very specific actions such as transferring data from one system to another.

In this guide, you'll learn the basics of using operators in Airflow and then implement them in a DAG.

To view all of the available Airflow operators, go to the [Astronomer Registry](https://registry.astronomer.io/modules?types=operators).

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).

## Operator basics

Operators are Python classes that encapsulate logic to do a unit of work. They can be viewed as a wrapper around each unit of work that defines the actions that will be completed and abstract the majority of code you would typically need to write. When you create an instance of an operator in a DAG and provide it with its required parameters, it becomes a task.

All operators inherit from the abstract [BaseOperator class](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html), which contains the logic to execute the work of the operator within the context of a DAG.

The following are some of the most frequently used Airflow operators:

- [PythonOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonoperator): Executes a Python function.
- [BashOperator](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator): Executes a bash script.
- [KubernetesPodOperator](https://registry.astronomer.io/providers/kubernetes/modules/kubernetespodoperator): Executes a task defined as a Docker image in a Kubernetes Pod.
- [SnowflakeOperator](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator): Executes a query against a Snowflake database.

Operators typically only require a few parameters. Keep the following considerations in mind when using Airflow operators:

- The [Astronomer Registry](https://registry.astronomer.io/modules?types=operators) is the best resource for learning what operators are available and how they are used.
- The core Airflow package includes basic operators such as the `PythonOperator` and `BashOperator`. These operators are automatically available in your Airflow environment. All other operators are part of provider packages, which you must install separately. For example, the `SnowflakeOperator` is part of the [Snowflake provider package](https://registry.astronomer.io/providers/snowflake).
- If an operator exists for your specific use case, you should use it instead of your own Python functions or [hooks](what-is-a-hook.md). This makes your DAGs easier to read and maintain.
- If an operator doesn't exist for your use case, you can extend an operator to meet your needs. For more information about customizing operators, see the video [Anatomy of an Operator](https://www.astronomer.io/events/webinars/anatomy-of-an-operator).
- [Sensors](what-is-a-sensor.md) are a type of operator that waits for something to happen. They can be used to make your DAGs more event-driven.
- [Deferrable Operators](deferrable-operators.md) are a type of operator that releases their worker slot while waiting for their work to be completed. This can result in cost savings and greater scalability. Astronomer recommends using deferrable operators whenever one exists for your use case and your task takes longer than a minute. You must be using Airflow 2.2 or later and have a triggerer running to use deferrable operators.
- Any operator that interacts with a service external to Airflow typically requires a connection so that Airflow can authenticate to that external system. For more information about setting up connections, see [Managing your connections in Apache Airflow](connections.md) or in the examples to follow.

## Example implementation

The following example shows how to use multiple operators in a DAG to transfer data from Amazon S3 to Redshift and perform data quality checks.

The code for this example is available in the [Astronomer Registry](https://registry.astronomer.io/dags/simple-redshift-3).

The following operators are used in this example:

- [EmptyOperator](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/empty/index.html): Organizes the flow of tasks in the DAG. Included with Airflow.
- [PythonDecoratedOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonoperator): Executes a Python function. It is functionally the same as the PythonOperator, but it is instantiated using the `@task` [decorator](airflow-decorators.md). Included with Airflow.
- [LocalFilesystemToS3Operator](https://registry.astronomer.io/providers/amazon/modules/localfilesystemtos3operator): Uploads a file from a local file system to Amazon S3. Included with the [AWS provider package](https://registry.astronomer.io/providers/amazon).
- [S3ToRedshiftOperator](https://registry.astronomer.io/providers/amazon/modules/s3toredshiftoperator): Transfers data from Amazon S3 to Redshift. Included with the [AWS provider package](https://registry.astronomer.io/providers/amazon).
- [PostgresOperator](https://registry.astronomer.io/providers/postgres/modules/postgresoperator): Executes a query against a Postgres database. Included with the [Postgres provider package](https://registry.astronomer.io/providers/postgres).
- [SQLCheckOperator](https://registry.astronomer.io/providers/common-sql/modules/sqlcheckoperator): Checks against a database using a SQL query. Included with Airflow.

There are a few things to note about the operators in this example DAG:

- Every operator is given a `task_id`. This is a required parameter, and the value provided is displayed as the name of the task in the Airflow UI.
- Each operator requires different parameters based on the work it does. For example, the PostgresOperator has a `sql` parameter for the SQL script to be executed, and the `S3ToRedshiftOperator` has parameters to define the location and keys of the files being copied from Amazon S3 and the Redshift table receiving the data.
- Connections to external systems are passed in most of these operators. The parameters `conn_id`, `postgres_conn_id`, and `aws_conn_id` all point to the names of the relevant connections stored in Airflow.

The following code shows how each of the operators is instantiated in a DAG file to define the pipeline:

<Tabs
    defaultValue="taskflow"
    groupId= "example-implementation"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{operator_example_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{operator_example_traditional}</CodeBlock>

</TabItem>
</Tabs>

The resulting DAG appears similar to this image:

![DAG Graph](/img/guides/example_dag_graph.png)
