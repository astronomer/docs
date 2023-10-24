---
title: "Orchestrate Great Expectations with Airflow"
sidebar_label: "Great Expectations"
description: "Orchestrate Great Expectations data quality checks with your Airflow DAGs."
id: airflow-great-expectations
sidebar_custom_props: { icon: 'img/integrations/great-expectations.png' }
---

import CodeBlock from '@theme/CodeBlock';
import gx_dag from '!!raw-loader!../code-samples/dags/airflow-great-expectations/gx_dag.py';

[Great Expectations](https://greatexpectations.io) (GX) is an open source Python-based data validation framework. You can test your data by expressing what you “expect” from it as simple declarative statements in JSON or YAML, then run validations using those [Expectation Suites](https://docs.greatexpectations.io/docs/terms/expectation_suite/) against data in a [Source Data System](https://docs.greatexpectations.io/docs/guides/setup/optional_dependencies/cloud/connect_gx_source_data_system) or a [pandas DataFrame](https://docs.greatexpectations.io/docs/0.15.50/guides/connecting_to_your_data/in_memory/pandas/). Astronomer, with help from Superconductive, maintains the [Great Expectations Airflow Provider](https://registry.astronomer.io/providers/airflow-provider-great-expectations/versions/latest) that gives users a convenient method for running validations directly from their DAGs.

This tutorial shows how to use the [`GreatExpectationsOperator`](https://registry.astronomer.io/providers/airflow-provider-great-expectations/versions/latest/modules/GreatExpectationsOperator) in an Airflow DAG, leveraging automatic creation of a default [Checkpoint](https://docs.greatexpectations.io/docs/terms/checkpoint) and connecting via an [Airflow connection](connections.md).

:::tip Related content

There are multiple resources for learning about this topic. See also:

- Webinar: [How to Improve Data Quality with Airflow's Great Expectations Operator](https://www.astronomer.io/events/webinars/how-to-improve-data-quality-with-airflows-great-expectations-operator/).

:::

## Time to complete

This tutorial takes approximately 20 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Great Expectations. See [GX Quickstart](https://docs.greatexpectations.io/docs/tutorials/getting_started/tutorial_overview).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- Access to a SQL database. This tutorial uses a local Postgres instance.
- (Optional) Local installation of the [`great_expectations` package](https://pypi.org/project/great-expectations/).

## Step 1: Configure your Astro project

To use GX with Airflow, install the [Great Expectations Airflow Provider](https://registry.astronomer.io/providers/airflow-provider-great-expectations/versions/latest) in your Astro project.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-gx-tutorial && cd astro-gx-tutorial
    $ astro dev init
    ```

2. Add the GX Airflow provider to your Astro project `requirements.txt` file.

    ```text
    airflow-provider-great-expectations==0.2.7
    ```

3. Add the following GX dependency to your Astro project `packages.txt` file.

    ```text
    libgeos-c1v5
    ```

## Step 2: Configure a GX project

The Great Expectations Airflow Provider requires a GX project to be present in your Airflow environment. The easiest way to create a GX project is by using the [`great_expectations` package](https://pypi.org/project/great-expectations/) and following the steps below. If you cannot install the GX package locally, you can copy the [`great_expectations` folder from this GitHub repository](https://github.com/astronomer/gx-tutorial/tree/main/include/great_expectations) into your Astro project `include` folder instead and continue this tutorial at [Step 3](#step-3-create-a-database-connection).

1. In your `include` folder, create a new file called `gx_init_script.py`. Then, copy and paste the following code into the file:

    ```python
    import great_expectations as gx
    context = gx.get_context()
    context = context.convert_to_file_context()
    ```

2. Go to your `include` folder and run the `gx_init_script.py` file to instantiate a [Data Context](https://docs.greatexpectations.io/docs/guides/setup/configuring_data_contexts/instantiating_data_contexts/instantiate_data_context) at `include/great_expectations`.

    ```sh
    $ cd include
    $ python gx_init_script.py
    ```

3. Create a new file in your `include/great_expectations/expectations` folder called `strawberry_suite.json`. Then, copy and paste the following code into the file:

    ```json
    {
        "data_asset_type": null,
        "expectation_suite_name": "strawberry_suite",
        "expectations": [
            {
                "expectation_context": {
                    "description": null
                },
                "expectation_type": "expect_table_row_count_to_be_between",
                "ge_cloud_id": null,
                "kwargs": {
                    "min_value": 2,
                    "max_value": 1000
                },
                "meta": {}
            }
        ],
        "ge_cloud_id": null,
        "meta": {
            "great_expectations_version": "0.15.34"
        }
    }
    ```

    This JSON file defines an [Expectation Suite](https://docs.greatexpectations.io/docs/terms/expectation_suite) containing one expectation of the type [`expect_table_row_count_to_be_between`](https://greatexpectations.io/expectations/expect_table_row_count_to_be_between). This expectation will check that the number of rows in a table is between 2 and 1000.

    You should now have the following file structure in your `include` folder:

    ```text
    └── include
        └── great_expectations
        │   ├── checkpoints
        │   ├── expectations
        │   │   └── strawberry_suite.json
        │   ├── plugins
        │   ├── profilers
        │   ├── uncommitted
        │   ├── .gitignore
        │   └── great_expectations.yml
        └── gx_init_script.py
    ```

4. Run `astro dev start` to start your Astro project.

## Step 3: Create a database connection

The easiest way to use GX with Airflow is to let the GreatExpectationsOperator create a default [Checkpoint](https://docs.greatexpectations.io/docs/terms/checkpoint) and [Datasource](https://docs.greatexpectations.io/docs/terms/datasource) based on an Airflow connection. To set up a connection to a Postgres database complete the following steps:

1. In the Airflow UI at `localhost:8080`, go to **Admin** -> **Connections** and click **+**. 

2. Create a new connection named `postgres_default` using the following information:

    - **Connection Id**: `postgres_default`.
    - **Connection Type**: `Postgres`.
    - **Host**: `<your postgres host>`.
    - **Login**: `<your postgres username>`.
    - **Password**: `<your postgres password>`.
    - **Schema**: `postgres`. Note that this is the name of the PostgreSQL database, not of the schema in the database. See the [PostgreSQL provider documentation](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/connections/postgres.html).
    - **Port**: `<your postgres port>`.

3. Click **Save**.

## Step 4: Create a DAG

1. Create a new file in your `dags` folder called `gx_tutorial.py`.

2. Copy and paste the following DAG code into the file:

    <CodeBlock language="python">{gx_dag}</CodeBlock>

    This DAG will create a table in your Postgres database, run a GX validation on the table, and then drop the table.

    The data in the table is validated using the GreatExpectationsOperator (GXO). The operator automatically creates a default Checkpoint and Datasource based on the `postgres_default` connection and runs the Expectations defined in the `strawberry_suite.json` file on the `strawberries` table. Note that instead of using the `schema` parameter of the GXO, you can also provide the schema name to the `data_asset_name` parameter in the form of `my_schema_name.my_table_name`. 

3. Open Airflow at `http://localhost:8080/`. Run the DAG manually by clicking the play button.

:::info

By default, the `GreatExpectationsOperator` pushes a [CheckpointResult object](https://docs.greatexpectations.io/docs/terms/checkpoint/#checkpointresult) to XCom. You can instead  return a json-serializable dictionary by setting the `return_json_dict` parameter to `True`.

If you do not want to use this built-in serialization, you can either enable XCom pickling by setting the environment variable `AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True`, or use a custom serialization method in a [custom XCom backend](https://docs.astronomer.io/learn/xcom-backend-tutorial).

:::

## How it works

The GreatExpectationsOperator is a versatile operator allowing you to integrate GX into your Airflow environment. This tutorial shows the simplest way of using the operator by letting it create a default Checkpoint and Datasource based on an Airflow connection.
The GreatExpectationsOperator also allows you to pass in a CheckpointConfig object using the `checkpoint_config` parameter or a `checkpoint_kwargs` dictionary. You can also customize the [Execution Engines](https://docs.greatexpectations.io/docs/terms/execution_engine) and pass [DataContextConfig objects](https://docs.greatexpectations.io/docs/terms/data_context) by configuring [Operator parameters](#operator-parameters).

For more examples, check out the [Get Improved Data Quality Checks in Airflow with the Updated Great Expectations Operator](https://www.astronomer.io/blog/improved-data-quality-checks-in-airflow-with-great-expectations-operator/) blog post and the [Airflow data quality demo repository](https://github.com/astronomer/airflow-data-quality-demo/).

### Operator parameters

The GreatExpectationsOperator is highly customizable to allow expert GX users to use their custom objects. This section explains some of the most commonly used parameters. Please refer to the [GX documentation](https://docs.greatexpectations.io/docs/) for in depth explanations of GX concepts.

When using the GreatExpectationsOperator, you must pass in either one of the following parameters:

- `data_context_root_dir` (str): The path to your GX project directory. This is the directory containing your `great_expectations.yml` file.
- `data_context_config` (DataContextConfig): To use an in-memory [Data Context](https://docs.greatexpectations.io/docs/terms/data_context), a `DataContextConfig` must be defined and passed to the operator, see also [this example DataContextConfig](https://github.com/great-expectations/airflow-provider-great-expectations/blob/main/include/great_expectations/object_configs/example_data_context_config.py).

Next, the operator will determine the Checkpoint and Datasource used to run your GX validations:

- If your Data Context does not specify a Datasource, and you do not pass in a Checkpoint, then the operator will build a Datasource and Checkpoint for you based on the `conn_id` you pass in and run the given Expectation Suite. This is the simplest way to use the operator and what is shown in this tutorial.
- If your project's Data Context specifies Datasources already, all you need to pass is the Data Context and the Expectation Suite. The operator will use the Datasources in the Data Context to create a default Checkpoint.
- If your project's [CheckpointStore](https://docs.greatexpectations.io/docs/terms/checkpoint_store) already contains a Checkpoint, you can specify its use by passing the name to the `checkpoint_name` parameter. The CheckpointStore is often in the `great_expectations/checkpoints/` path, so that `checkpoint_name = "strawberries.pass.chk"` would reference the file `great_expectations/checkpoints/strawberries/pass/chk.yml`.
- If you want to run a custom Checkpoint, you can either pass a CheckpointConfig object to `checkpoint_config` or a dictionary of your checkpoint config to `checkpoint_kwargs`. `checkpoint_kwargs` can also be used to specify additional overwriting configurations. See the [example CheckpointConfig](https://github.com/great-expectations/airflow-provider-great-expectations/blob/main/include/great_expectations/object_configs/example_checkpoint_config.py).

The Datasource can also be a pandas DataFrame, as shown in [Running GX validations on pandas DataFrames](#running-gx-validations-on-pandas-dataframes). Depending on how you define your Datasource the `data_asset_name` parameter has to be adjusted:

- If a pandas DataFrame is passed, the `data_asset_name` parameter can be any name that will help you identify the DataFrame.
- If a `conn_id` is supplied, the `data_asset_name` must be the name of the table the Expectations Suite runs on.

By default, a Great Expectations task runs validations and raises an `AirflowException` if any of the tests fail. To override this behavior and continue running the pipeline even if tests fail, set the `fail_task_on_validation_failure` flag to `False`.

In Astronomer or any environment with OpenLineage configured, the `GreatExpectationsOperator` will automatically add the OpenLineage action to its default action list when a Checkpoint is not specified to the operator. To turn off this feature, set the `use_open_lineage` parameter to `False`.

For a full list of parameters, see the [the Astronomer registry](https://registry.astronomer.io/providers/airflow-provider-great-expectations/versions/latest/modules/GreatExpectationsOperator). For more information about the parameters and examples, see the [README in the provider repository](https://github.com/great-expectations/airflow-provider-great-expectations).

### Running GX validations on pandas DataFrames

The GreatExpectationsOperator can also be used to run validations on CSV files by passing them in as a pandas DataFrame. This pattern is useful to test pipelines locally with small amounts of data. Note that the `execution_engine` parameter needs to be adjusted. 

```python
gx_validate_pg = GreatExpectationsOperator(
    task_id="gx_validate_pg",
    data_context_root_dir="include/great_expectations",
    dataframe_to_validate=pd.read_csv("include/strawberries.csv"),
    execution_engine="PandasExecutionEngine",
    expectation_suite_name="strawberry_suite",
    return_json_dict=True,
)
```

### Connections and backends

The GreatExpectationsOperator can run a Checkpoint on a dataset stored in any backend compatible with GX. This includes BigQuery, MSSQL, MySQL, PostgreSQL, Redshift, Snowflake, SQLite, and Athena, among others. All that’s needed to get the GreatExpectationsOperator to point at an external dataset is to set up an [Airflow Connection](connections.md) to the Datasource and setting the `conn_id` parameter. Connections will still work if you have your connection configured in both Airflow and Great Expectations, as long as the correct Datasource is specified in the Checkpoint passed to the operator.
