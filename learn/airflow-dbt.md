---
title: "Orchestrate dbt Core jobs with Airflow and Cosmos"
sidebar_label: "dbt Core"
id: airflow-dbt
sidebar_custom_props: { icon: 'img/integrations/dbt.png' }
---

<head>
  <meta name="description" content="Learn how to use Cosmos to orchestrate dbt Core jobs with Airflow." />
  <meta name="og:description" content="Learn how to use Cosmos to orchestrate dbt Core jobs with Airflow." />
</head>

import CodeBlock from '@theme/CodeBlock';
import cosmos_dag from '!!raw-loader!../code-samples/dags/airflow-dbt/cosmos_dag.py';
import airflow_dbt_bashoperator from '!!raw-loader!../code-samples/dags/airflow-dbt/airflow_dbt_bashoperator.py';

[dbt Core](https://docs.getdbt.com/) is an open-source library for analytics engineering that helps users build interdependent SQL models for in-warehouse data transformation, using ephemeral compute of data warehouses. 

The open-source provider package [Cosmos](https://astronomer.github.io/astronomer-cosmos/) allows you to integrate dbt jobs into Airflow by automatically creating Airflow tasks from dbt models. You can turn your dbt Core projects into an Airflow task group with just a few lines of code:

```python
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="my_db_conn",
        profile_args={"schema": "my_schema"},
    ),
)

DbtTaskGroup(
    project_config=ProjectConfig("path/to/my_project"),
    profile_config=profile_config,
    default_args={"retries": 2},
)
```

:::tip Related content

There are multiple resources for learning about this topic. See also:

- Webinar: [Introducing Cosmos: The Easy Way to Run dbt Models in Airflow](https://www.astronomer.io/events/webinars/introducing-cosmos-the-east-way-to-run-dbt-models-in-airflow/).
- Use case: [ELT with Airflow and dbt Core](use-case-airflow-dbt.md) including a a ready-to-use [example Cosmos project repository](https://github.com/astronomer/cosmos-use-case).

For a tutorial on how to use dbt Cloud with Airflow, see [Orchestrate dbt Cloud with Airflow](airflow-dbt-cloud.md).

:::

## Why use Airflow with dbt Core?

dbt Core offers the possibility to build modular, reuseable SQL components with built-in dependency management and [incremental builds](https://docs.getdbt.com/docs/build/incremental-models). With [Cosmos](https://astronomer.github.io/astronomer-cosmos/) you can integrate dbt jobs into your Airflow orchestration environment as a standalone DAG or as a task group within a DAG. 

The benefits of using Airflow with dbt Core include:

- Use Airflow's [data-aware scheduling](airflow-datasets.md) and [Airflow sensors](what-is-a-sensor.md) to run models depending on other events in your data ecosystem.
- Turn each dbt model into a task, complete with Airflow features like [retries](rerunning-dags.md#automatically-retry-tasks) and [error notifications](error-notifications-in-airflow.md), as well as full observability into past runs directly in the Airflow UI.
- Run `dbt test` on tables created by individual models immediately after a model has completed. Catch issues before moving downstream and integrate additional [data quality checks](data-quality.md) with your preferred tool to run alongside dbt tests.
- Run dbt projects using [Airflow connections](connections.md) instead of dbt profiles. You can store all your connections in one place, directly within Airflow or by using a [secrets backend](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html).
- Leverage native support for installing and running dbt in a virtual environment to avoid dependency conflicts with Airflow.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of dbt Core. See [What is dbt?](https://docs.getdbt.com/docs/introduction).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- How Airflow and dbt concepts relate to each other. See [Similar dbt & Airflow concepts](https://astronomer.github.io/astronomer-cosmos/getting_started/dbt-airflow-concepts.html).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow task groups. See [Airflow task groups](task-groups.md).
- Airflow connections. See [Manage connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- Access to a data warehouse supported by dbt Core. See [dbt documentation](https://docs.getdbt.com/docs/supported-data-platforms) for all supported warehouses. This tutorial uses a Postgres database.

You do not need to have dbt Core installed locally in order to complete this tutorial.

## Step 1: Configure your Astro project

To use dbt with Airflow install dbt Core in a virtual environment and Cosmos in a new Astro project.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-dbt-core-tutorial && cd astro-dbt-core-tutorial
    $ astro dev init
    ```

2. Open the `Dockerfile` and add the following lines to the end of the file:

    ```text
    # replace dbt-postgres with another supported adapter if you're using a different warehouse type
    RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
        pip install --no-cache-dir dbt-postgres && deactivate
    ```

    This code runs a bash command when the Docker image is built that creates a virtual environment called `dbt_venv` inside of the Astro CLI scheduler container. The `dbt-postgres` package, which also contains `dbt-core`, is installed in the virtual environment. If you are using a different data warehouse, replace `dbt-postgres` with the adapter package for your data warehouse.

3. Add [Cosmos](https://github.com/astronomer/astronomer-cosmos) and the [Postgres provider](https://registry.astronomer.io/providers/apache-airflow-providers-postgres/versions/latest) to your Astro project `requirements.txt` file. If you are using a different data warehouse, replace `apache-airflow-providers-postgres` with the provider package for your data warehouse. You can find information on all provider packages on the [Astronomer registry](https://registry.astronomer.io/).

    ```text
    astronomer-cosmos==1.0.4
    apache-airflow-providers-postgres==5.6.0
    ```

## Step 2: Prepare your dbt project

To integrate your dbt project with Airflow, you need to add the project folder to your Airflow environment. For this step you can either add your own project in a new `dbt` folder in your `dags` directory, or follow the steps below to create a simple project using two models.

1. Create a folder called `dbt` in your `dags` folder. 

2. In the `dbt` folder, create a folder called `my_simple_dbt_project`.

3. In the `my_simple_dbt_project` folder add your `dbt_project.yml`. This configuration file needs to contain at least the name of the project. This tutorial additionally shows how to inject a variable called `my_name` from Airflow into your dbt project.

    ```yaml
    name: 'my_simple_dbt_project'
    vars:
        my_name: "No entry"
    ```

4. Add your dbt models in a subfolder called `models` in the `my_simple_dbt_project` folder. You can add as many models as you want to run. This tutorial uses the following two models:

    `model1.sql`:

    ```sql
    SELECT '{{ var("my_name") }}' as name
    ```

    `model2.sql`:

    ```sql
    SELECT * FROM {{ ref('model1') }}
    ```

    `model1.sql` selects the variable `my_name`. `model2.sql` depends on `model1.sql` and selects everything from the upstream model.

You should now have the following structure within your Astro project:

```text
.
└── dags
    └── dbt
        └── my_simple_dbt_project
           ├── dbt_project.yml
           └── models
               ├── model1.sql
               └── model2.sql
```

## Step 3: Create an Airflow connection to your data warehouse

Cosmos allows you to apply Airflow connections to your dbt project. 

1. Start Airflow by running `astro dev start`.

2. In the Airflow UI, go to **Admin** -> **Connections** and click **+**. 

3. Create a new connection named `db_conn`. Select the connection type and supplied parameters based on the data warehouse you are using. For a Postgres connection, enter the following information:

    - **Connection ID**: `db_conn`.
    - **Connection Type**: `Postgres`.
    - **Host**: Your Postgres host address.
    - **Schema**: Your Postgres database. 
    - **Login**: Your Postgres login username.
    - **Password**: Your Postgres password.
    - **Port**: Your Postgres port.

:::info

If a connection type for your database isn't available, you might need to make it available by adding the [relevant provider package](https://registry.astronomer.io/) to `requirements.txt` and running `astro dev restart`.

:::

## Step 4: Write your Airflow DAG

The DAG you'll write uses Cosmos to create tasks from existing dbt models and the [PostgresOperator](https://registry.astronomer.io/providers/apache-airflow-providers-postgres/versions/latest/modules/PostgresOperator) to query a table that was created. You can add more upstream and downstream tasks to embed the dbt project within other actions in your data ecosystem.

1. In your `dags` folder, create a file called `my_simple_dbt_dag.py`.

2. Copy and paste the following DAG code into the file:

    <CodeBlock language="python">{cosmos_dag}</CodeBlock>

    This DAG uses the `DbtTaskGroup` class from the Cosmos package to create a task group from the models in your dbt project. Dependencies between your dbt models are automatically turned into dependencies between Airflow tasks. Make sure to add your own values for `YOUR_NAME`, `DB_NAME`, and `SCHEMA_NAME`.
    
    Using the `vars` keyword in the dictionary provided to the `operator_args` parameter, you can inject variables into the dbt project. This DAG injects `YOUR_NAME` for the `my_name` variable. If your dbt project contains dbt tests, they will be run directly after a model has completed. Note that it is a best practice to set `retries` to at least 2 for all tasks that run dbt models.

:::tip

In some cases, especially in larger dbt projects, you might run into a `DagBag import timeout` error. 
This error can be resolved by increasing the value of the Airflow configuration [core.dagbag_import_timeout](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dagbag-import-timeout).

:::

3. Run the DAG manually by clicking the play button and view the DAG in the graph view. Double click the task groups in order to expand them and see all tasks. 

    ![Cosmos DAG graph view](/img/integrations/airflow-dbt-cosmos_dag_graph_view.png)

4. Check the [XCom](airflow-passing-data-between-tasks.md) returned by the `query_table` task to see your name in the `model2` table.

:::info

The DbtTaskGroup class populates an Airflow task group with Airflow tasks created from dbt models inside of a normal DAG. To directly define a full DAG containing only dbt models use the `DbtDag` class, as shown in the [Cosmos documentation](https://astronomer.github.io/astronomer-cosmos/getting_started/astro.html).

:::

Congratulations! You've run a DAG using Cosmos to automatically create tasks from dbt models. You can learn more about how to configure Cosmos in the [Cosmos documentation](https://astronomer.github.io/astronomer-cosmos/index.html).

## Alternative ways to run dbt Core with Airflow

While using Cosmos is recommended, there are several other ways to run dbt Core with Airflow.

### Using the BashOperator

You can use the [BashOperator](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator) to execute specific dbt commands. It's recommended to run `dbt-core` and the dbt adapter for your database in a virtual environment because there often are dependency conflicts between dbt and other packages.

The DAG below uses the BashOperator to activate the virtual environment and execute `dbt_run` for a dbt project.

<CodeBlock language="python">{airflow_dbt_bashoperator}</CodeBlock>

Using the `BashOperator` to run `dbt run` and other dbt commands can be useful during development. However, running dbt at the project level has a couple of issues:

- There is low observability into what execution state the project is in.
- Failures are absolute and require all models in a project to be run again, which can be costly.

### Using a manifest file

Using a dbt-generated `manifest.json` file gives you more visibility into the steps dbt is running in each task. This file is generated in the target directory of your `dbt` project and contains its full representation. For more information on this file, see the [dbt documentation](https://docs.getdbt.com/reference/dbt-artifacts/).

You can learn more about a manifest-based dbt and Airflow project structure, view example code, and read about the `DbtDagParser` in a 3-part blog post series on [Building a Scalable Analytics Architecture With Airflow and dbt](https://www.astronomer.io/blog/airflow-dbt-1/). 
