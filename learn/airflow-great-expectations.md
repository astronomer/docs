---
title: "Orchestrate Great Expectations with Airflow"
sidebar_label: "Great Expectations"
description: "Orchestrate Great Expectations data quality checks with your Airflow DAGs."
id: airflow-great-expectations
sidebar_custom_props: { icon: 'img/integrations/great-expectations.png' }
---

:::info

You can now find the [Great Expectations Provider](https://registry.astronomer.io/providers/great-expectations) on the [Astronomer Registry](https://registry.astronomer.io), the discovery and distribution hub for Apache Airflow integrations created to aggregate and curate the best bits of the ecosystem.

:::

[Great Expectations](https://greatexpectations.io) is an open source Python-based data validation framework. You can test your data by expressing what you “expect” from it as simple declarative statements in Python, then run validations using those “expectations” against datasets with [Checkpoints](https://docs.greatexpectations.io/docs/reference/checkpoints_and_actions). Astronomer, with help from Superconductive, maintains an [Airflow provider](https://registry.astronomer.io/providers/great-expectations) that gives users a convenient method for running validations directly from their DAGs.

This guide will walk you through how to use the [`GreatExpectationsOperator`](https://registry.astronomer.io/providers/great-expectations/modules/greatexpectationsoperator) in an Airflow DAG and the Astronomer environment.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Great Expectations. See [Getting started with Great Expectations](https://docs.greatexpectations.io/docs/tutorials/getting_started/tutorial_overview).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Great Expectations concepts

Typically, using Great Expectations is a two-step process:

- Expectation Suite creation
- Validation

First, a user creates test suites, or “Expectation Suites”, using [Great Expectations methods](https://docs.greatexpectations.io/docs/terms/expectation/). These suites are usually stored in JSON and can be checked into version control, just like regular tests. The suites are then loaded by the Great Expectations framework at test runtime, for example, when processing a new batch of data in a pipeline.

:::tip

For a step-by-step guide on how to configure a simple Great Expectations project, see the [“Getting started” tutorial](https://docs.greatexpectations.io/en/latest/guides/tutorials.html).

:::

## Setup

This guide assumes that you have downloaded the code from the [demo repository](https://github.com/astronomer/airflow-data-quality-demo/), which contains a sample Great Expectations project.

If you want to use your own Great Expectations project along with this guide, ensure you have completed the following steps:

- Initialized a Great Expectations project
- Created at least one Expectation Suite, `my_suite`

If you set up a project manually, you will see a `great_expectations` directory which contains several sub-directories, as well as the `great_expectations.yml` Data Context file. If you cloned the demo repository, the `great_expectations` directory can be found under `include/`.

:::info

The `GreatExpectationsOperator` requires custom handling of XComs. You can either enable XCom pickling by setting the environment variable AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True`, or use a custom serialization method in a [custom XCom backend](https://docs.astronomer.io/learn/xcom-backend-tutorial).

:::

## Use Case: Great Expectations operator

Now that your system is set up to work with Great Expectations, you can start exploring how to use it in your DAGs. The current Great Expectations provider version uses the [Great Expectations V3 API](https://docs.greatexpectations.io/docs/).

### Configuration

To validate your data, the `GreatExpectationsOperator` runs a Checkpoint against your dataset. Before you start writing your DAG, make sure you have at least a Data Context configured. To do this, either verify the path to your `great_expectations.yml` file or define Python dictionaries containing the necessary [Data Context](https://github.com/astronomer/airflow-data-quality-demo/blob/main/include/great_expectations/configs/snowflake_configs.py#L14) fields and import those dictionaries into your DAG.

A [Data Context](https://docs.greatexpectations.io/docs/reference/data_context) represents a Great Expectations project. It organizes storage and access for Expectation Suites, data sources, notification settings, and data fixtures.

Our [demo repository](https://github.com/astronomer/airflow-data-quality-demo/) uses the following configuration:

- The `great_expectations` directory is accessible by your DAG, as it is loaded into the Docker container as part of the `include` directory.
- The Great Expectations provider is installed when you run `astro dev start`, as it is part of `requirements.txt`. For Astronomer projects, a provider version >=`0.1.1` is required. If you are not using an Astronomer environment, install the Great Expectations provider in your environment manually:

    ```bash
    pip install great_expectations airflow-provider-great-expectations==0.2.0
    ```

    It’s recommended that you specify a version when installing the package.

### Using the Great Expectations operator

1. Import the operator into your DAG file. You might also need to import the `DataContextConfig` or `CheckpointConfig` classes depending on how you're using the operator. To import the Great Expectations provider, and configurations in a given DAG, add the following line to the top of the DAG file in your `dags` directory:

    ```python
    from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
    from great_expectations.data_context.types.base import (
        DataContextConfig,
        CheckpointConfig
    )
    ```

2. Create a task using the [`GreatExpectationsOperator`](https://registry.astronomer.io/providers/great-expectations/modules/greatexpectationsoperator). To use the operator in the DAG, define an instance of the `GreatExpectationsOperator` class and assign it to a variable. In the following example, we define two different instances of the operator to showcase two different ways to pass the data context in to the operator:

    ```python
    ge_data_context_root_dir_pass = GreatExpectationsOperator(
        task_id="ge_data_context_root_dir_pass",
        data_context_root_dir=ge_root_dir,
        expectation_suite_name="taxi.demo",
        execution_engine="PandasExecutionEngine",
        data_asset_name="taxi_df_pass",
        dataframe_to_validate=pd.read_csv(
            filepath_or_buffer=data_file,
            header=0,
        ),
    )

    ge_data_context_config_pass = GreatExpectationsOperator(
        task_id="ge_data_context_config_with_checkpoint_config_pass",
        data_context_config=example_data_context_config,
        expectation_suite_name="taxi.demo",
        execution_engine="PandasExecutionEngine",
        data_asset_name="taxi_df_pass",
        dataframe_to_validate=pd.read_csv(
            filepath_or_buffer=data_file,
            header=0,
        ),
    )

    ge_data_context_root_dir_pass >> ge_data_context_config_pass
    ```

### Operator parameters

The operator has several optional parameters, but it always requires either a `data_context_root_dir` or a `data_context_config`. Depending on how you have your project configured, other parameters may also be necessary. The less configured your project, the more parameters you'll pass.

For example:

- If your project's data context specifies data sources, all you need to pass in is the data context and the expectation suite.
- If your data context does not specify a data source, and you do not pass in a checkpoint, then the operator will build a checkpoint for you based on the data source you pass in and run the given expectation suite.

The datasource can be a dataframe, as shown in the example code, or an Airflow connection using the `conn_id` parameter. Depending on how you define your data source the `data_asset_name` parameter has to be adjusted:

- If a dataframe is passed, the `data_asset_name` parameter can be any name that will help you identify the dataframe.
- If a `conn_id` is supplied, the `data_asset_name` must be the name of the table the expectations suite runs on.

The `data_context_root_dir` should point to the `great_expectations` project directory generated when you created the project with the CLI. If using an in-memory `data_context_config`, a `DataContextConfig` must be defined, as in [this example](https://github.com/great-expectations/airflow-provider-great-expectations/blob/main/include/great_expectations/object_configs/example_data_context_config.py).

While not a required parameter, if your project already contains Checkpoints, they too can be passed to the operator in two ways:

- A `checkpoint_name` may be passed with the `checkpoint_name` paramter and references a checkpoint in the project `CheckpointStore` defined in the `DataContext` (which is often in the `great_expectations/checkpoints/` path), so that `checkpoint_name = "taxi.pass.chk"` would reference the file `great_expectations/checkpoints/taxi/pass/chk.yml`.
- A `checkpoint_config` may be passed to the operator in place of a name, and can be defined like [this example](https://github.com/great-expectations/airflow-provider-great-expectations/blob/main/include/great_expectations/object_configs/example_checkpoint_config.py).

Additionally, `checkpoint_kwargs` may be passed to the operator to specify additional, overwriting configurations.

By default, a Great Expectations task runs validations and raises an `AirflowException` if any of the tests fail. To override this behavior and continue running the pipeline even if tests fail, set the `fail_task_on_validation_failure` flag to `False`.

By default in Astronomer or any environment with OpenLineage configured, the `GreatExpectationsOperator` will automatically add the OpenLineage action to its default action list when a checkpoint is not specified to the operator. To turn off this feature, set the `use_open_lineage` parameter to `False`.

For a full list of parameters, see the `GreatExpectationsOperator` [documentation](https://registry.astronomer.io/providers/great-expectations/modules/greatexpectationsoperator).

For more information about possible parameters and examples, see the [README in the provider repository](https://github.com/great-expectations/airflow-provider-great-expectations) and the [example DAG in the provider package](https://registry.astronomer.io/dags/example-great-expectations-dag).

### Connections and backends

The `GreatExpectationsOperator` can run a checkpoint on a dataset stored in any backend compatible with Great Expectations. This includes BigQuery, MSSQL, MySQL, PostgreSQL, Redshift, Snowflake, SQLite, and Athena, among others. All that’s needed to get the `GreatExpectationsOperator` to point at an external dataset is to set up an [Airflow Connection](connections.md) to the data source and set the `conn_id` parameter. Connections will still work if you have your connection configured in both Airflow and Great Expectations, as long as the correct datasource is specified in the Checkpoint passed to the operator.

## Next steps

In this guide, you learned about the purpose of Great Expectations and how to use the provider operator to create Great Expectations Airflow tasks. For more examples on how to use the `GreatExpectationsOperator` as part of an ELT pipeline, see the [Great Expectations Snowflake Example](https://legacy.registry.astronomer.io/dags/great-expectations-snowflake), [Great Expectations BigQuery Example](https://legacy.registry.astronomer.io/dags/great-expectations-bigquery), and [Great Expectations Redshift Example](https://legacy.registry.astronomer.io/dags/great-expectations-redshift) examples on the [Astronomer Registry](https://registry.astronomer.io/).
