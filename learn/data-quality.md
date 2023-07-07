---
title: "Data quality and Airflow"
description: "Check the quality of your data using Airflow."
id: data-quality
sidebar_label: "Data quality"
---

import CodeBlock from '@theme/CodeBlock';
import example_dag_sql_check_operators from '!!raw-loader!../code-samples/dags/data-quality/example_dag_sql_check_operators.py';
import gx_example_dag from '!!raw-loader!../code-samples/dags/data-quality/gx_example_dag.py';

## Overview

Checking the quality of your data is essential to getting actionable insights from your data pipelines. Airflow offers many ways to orchestrate data quality checks directly from your DAGs.

This guide covers:

- Best practices and essential knowledge surrounding the planning of a data quality approach.
- When to implement data quality checks.
- How to choose a data quality check tool.
- How data lineage is connected to data quality.
- An in-depth look at two commonly used data quality check tools: SQL check operators and Great Expectations.
- An example comparing implementations of data quality checks using each of these tools.

## Assumed knowledge

To get the most out of this guide, you should have knowledge of:

- What Airflow is and when to use it. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).
- Relational databases. See [Relational database on Wikipedia](https://en.wikipedia.org/wiki/Relational_database).

## Data quality essentials

What is considered good quality data is determined by the needs of your organization. Defining quality criteria for a given collection of datasets is often a task requiring collaboration with all data professionals involved in each step of the pipeline.

The following is a typical data quality check process:

- Assess where and in what formats relevant data is stored, and where it moves along your pipeline. A data lineage tool can assist with this process.
- Gather the data quality criteria from data professionals using the data.
- Determine the quality checks to run different components of the dataset.
- Determine where those quality checks should occur in your pipeline.
- Determine what happens when a check fails.
- Choose a data quality tool.
- Write the checks.
- Test the checks.

### Types of data quality checks

Data quality checks can be run on different components of the dataset:

- **Column**: Common checks include confirming uniqueness of a key column, restricting the amount of `NULL` values that are allowed, defining logical bounds for numeric or date columns, and defining valid options for categorical variables.
- **Row**: Common checks include comparing the values in several columns for each row, and ensuring that there are no mutually exclusive values present in the same row.
- **Table**: Common checks include checking against a template schema to verify that it has not changed, and checking that a table has a minimum row count.
- **Over several tables**: Common checks include data parity checks across several tables. You can also create logical checks like making sure a customer marked as `inactive` has no purchases listed in any of the other tables.

It is also important to distinguish between the two types of control in data quality:

- **Static control**: Runs checks on Spark or pandas DataFrames, or on existing tables in a database. These checks can be performed anywhere in a typical ETL pipeline and might halt the pipeline in case of a failed check to prevent further processing of data with quality issues.
- **Flow control**: Monitors incoming data on a record-by-record basis, which sometimes prevents single records that fail certain data quality checks from entering the database. This guide does not cover flow controls.

### Where to run data quality checks

Data quality checks can be run at different times within a data pipeline or an Airflow environment. It often makes sense to test them in a dedicated DAG before you incorporate them into your pipelines to make downstream behavior dependent on the outcome of selected data quality checks.

For example, data quality checks can be placed in the following locations within an ETL pipeline:

- Before the transform step (`data_quality_check_1`)
- After the transform step (`data_quality_check_2`)
- Branching off from a step (`data_quality_check_3`)

The following DAG graph shows the typical locations for data quality checks:

![Different locations for data quality checks in an ETL pipeline](/img/guides/dq_checks_locations_example_graph.png)

It's common to use downstream tasks of data quality checks (`post_check_action_1` and `post_check_action_2`) or [Airflow callbacks](error-notifications-in-airflow.md#airflow-callbacks) to alert data professionals of data quality issues, for example as an email or a Slack message. It is also possible to create a downstream task that only runs when all data quality checks are successful. For example, the successful checking event for reporting purposes.

When implementing data quality checks, consider how a check success or failure should influence downstream dependencies. [Trigger Rules](managing-dependencies.md#trigger-rules) are especially useful for managing operator dependencies.

## When to implement data quality checks

When implementing data quality checks, it is important to consider the tradeoffs between the upfront work of implementing checks versus the cost of downstream issues caused by bad quality data.

You might need to implement data quality checks in the following circumstances:

- Downstream models serve customer-facing results that could be compromised in the case of a data quality issue.
- There are data quality concerns where an issue might not be immediately obvious to the data professional using the data.

## Data quality tools

There are multiple open source tools that can be used to check data quality from an Airflow DAG. While this guide lists the most commonly used tools here, it focuses on the two tools that also integrate with OpenLineage:

- **[SQL check operators](airflow-sql-data-quality.md)**: A group of operators in the [Common SQL provider](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/versions/latest) package that you can use to define data quality checks using Python dictionaries and SQL from within your DAGs.
- **[Great Expectations](airflow-great-expectations.md)**: An open source data validation framework where checks are defined in JSON. Airflow offers a provider package including the [GreatExpectationsOperator](https://registry.astronomer.io/providers/airflow-provider-great-expectations/versions/latest) for easy integration.

Other tools that can be used for data quality checks include:

- **[Soda](soda-data-quality.md)**: An open source data validation framework that uses YAML to define checks which can be run in Airflow using the [BashOperator](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/BashOperator). Soda also offers the ability to write any custom checks using SQL.
- **[dbt test](https://docs.getdbt.com/docs/building-a-dbt-project/tests)**: A testing framework for [dbt](https://docs.getdbt.com/) models. The easiest way to run dbt models including `dbt test` within Airflow is with the [Cosmos package](airflow-dbt.md).

### Choosing a tool

Which tool you choose is determined by the needs and preferences of your organization. Astronomer recommends using SQL check operators if you want to:

- Write checks without needing to set up software in addition to Airflow.
- Write checks as Python dictionaries and in SQL.
- Use any SQL statement that returns a single row of booleans as a data quality check.
- Implement many different downstream dependencies depending on the outcome of different checks.
- Have full observability of which checks failed from within Airflow task logs, including the full SQL statements of failed checks.

Astronomer recommends using a data validation framework such as Great Expectations or Soda in the following circumstances:

- You want to collect the results of your data quality checks in a central place.
- You prefer to write checks in JSON (Great Expectations) or YAML (Soda).
- Most or all of your checks can be implemented by the predefined checks in the solution of your choice.
- You want to abstract your data quality checks from the DAG code.

Currently only SQL check operators and the GreatExpectationsOperator offer data lineage extraction through [OpenLineage](airflow-openlineage.md).

### SQL check operators

:::info

You can find more details and examples using SQL check operators in the [Run data quality checks using SQL check operators](airflow-sql-data-quality.md) tutorial.

:::

SQL check operators execute a SQL statement that results in a set of booleans. A result of `True` leads to the check passing and the task being labeled as successful. A result of `False`, or any error when the statement is executed, leads to a failure of the task. Before using any of the operators, you need to define the [connection](connections.md) to your data storage from the Airflow UI or with an external secrets manager.

The SQL check operators work with any backend solution that accepts SQL queries and supports Airflow, and differ in what kind of data quality checks they can perform and how they are defined. All SQL check operators are part of the [Common SQL provider](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/versions/latest).

- [SQLColumnCheckOperator](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlcolumncheckoperator): Can quickly define checks on columns of a table using a Python dictionary.
- [SQLTableCheckOperator](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqltablecheckoperator): Can run aggregated and non-aggregated statements involving several columns of a table.
- [SQLCheckOperator](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlcheckoperator): Can be used with any SQL statement that returns a single row of booleans.
- [SQLIntervalCheckOperator](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlintervalcheckoperator): Runs checks against historical data.

As well as the older [SQLValueCheckOperator](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlvaluecheckoperator) and [SQLThresholdCheckOperator](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlthresholdcheckoperator).

The logs from SQL check operators can be found in the regular Airflow task logs.

### Great Expectations

Great Expectations is an open source data validation framework that allows the user to define data quality checks in JSON. The checks, also known as Expectation Suites, can be run in a DAG using the GreatExpectationsOperator from the [Great Expectations provider](https://registry.astronomer.io/providers/airflow-provider-great-expectations/versions/latest). All currently available Expectations can be viewed on the [Great Expectations website](https://greatexpectations.io/expectations) and creation of [Custom Expectations](https://docs.greatexpectations.io/docs/guides/expectations/custom_expectations_lp) is possible.

The easiest way to use Great Expectations with Airflow is to initialize a Great Expectations project in a directory accessible to your Airflow environment and using the automatic creation of a [Checkpoint](https://docs.greatexpectations.io/docs/terms/checkpoint) and [Datasource](https://docs.greatexpectations.io/docs/terms/datasource) from an [Airflow connection](connections.md) by the GreatExpectationsOperator. This basic usage of the GreatExpectationsOperator does not need in-depth Great Expectations knowledge and full customization is possible. 

When using Great Expectations, Airflow task logs show the results of the suite at the test-level in a JSON format. To get a [detailed report](https://docs.greatexpectations.io/docs/terms/data_docs/) on the checks that were run and their results, you can view the HTML files located in the `great_expectations/uncommitted/data_docs/local_site/validations` directory in any browser. These data docs can be generated to other backends as well as the local file.

You can find more information on how to use Great Expectations with Airflow in the [Orchestrate Great Expectations with Airflow](airflow-great-expectations.md) tutorial.

## Data lineage and data quality

In complex data ecosystems, lineage can be a powerful addition to data quality checks, especially for investigating what data from which origins caused a check to fail.

:::info

For more information on data lineage and setting up OpenLineage with Airflow, see [OpenLineage and Airflow](airflow-openlineage.md).

:::

Both the `SQLColumnCheckOperator` and the `SQLTableCheckOperator` have OpenLineage extractors that emit lineage metadata. While the other SQL check operators will show up on the lineage graph, they do not emit test data to the OpenLineage backend. The `GreatExpectationsOperator` will automatically trigger the OpenLineage action if an OpenLineage environment is recognized. If you are working with open source tools, you can view the resulting lineage from the extractors using Marquez.

The output from the `SQLColumnCheckOperator` contains each individual check and whether or not it succeeded:

![Marquez SQLColumnCheckOperator](/img/guides/marquez_sql_column_check.png)

For the `GreatExpectationsOperator`, OpenLineage receives whether or not the whole Expectation Suite succeeded or failed:

![Marquez GreatExpectationsOperator](/img/guides/marquez_ge.png)

## Example: Comparing SQL check operators and Great Expectations

This example shows the steps necessary to perform the same set of data quality checks with SQL check operators and with Great Expectations.

The checks performed for both tools are:

- `MY_DATE_COL` has only unique values.
- `MY_DATE_COL` has only values between 2017-01-01 and 2022-01-01.
- `MY_TEXT_COL` has no null values.
- `MY_TEXT_COL` has at least 10 distinct values.
- `MY_NUM_COL` has a minimum value between 90 and 110.
- `example_table` has at least 10 rows.
- The value in each row of `MY_COL_1` plus the value of the same row in `MY_COL_2` is equal to 100.
- The most common value in `MY_COL_3` is either `val1` or `val4`.

### Example: SQL check operators

The example DAG includes the following tasks:

- The`SQLColumnCheckOperator` performs checks on several columns in the target table.
- The `SQLTableCheckOperators` performs checks on the whole table, involving one or more columns.
- The `SQLCheckOperator` makes sure the most common value of a categorical variable is one of two options.

While this example shows all the checks being written within the Python file defining the DAG, it is possible to modularize commonly used checks and SQL statements in separate files. If you're using the Astro CLI, you can add the files to the `include` directory.

<CodeBlock language="python">{example_dag_sql_check_operators}</CodeBlock>

### Example: Great Expectations

The following example runs the same data quality checks as the SQL check operators example against the same database. After setting up the Great Expectations instance with at least the data context, the checks can be defined in a JSON file to form an Expectation Suite.

:::info

For each of the checks in this example, an Expectation already exists. This is not always the case, and for more complicated checks you may need to define a [custom Expectation](https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/overview).

:::


```json
{
    "data_asset_type": null,
    "expectation_suite_name": "my_suite",
    "expectations": [
        {
            "expectation_context": {
                "description": "MY_DATE_COL has values between 2017-01-01 - 2022-01-01"
            },
            "expectation_type": "expect_column_values_to_be_between",
            "ge_cloud_id": null,
            "kwargs": {
                "column": "MY_DATE_COL",
                "max_value": "2022-01-01",
                "min_value": "2017-01-01"
            },
            "meta": {}
        },
        {
            "expectation_context": {
                "description": "MY_DATE_COL's values are all unique"
            },
            "expectation_type": "expect_column_values_to_be_unique",
            "ge_cloud_id": null,
            "kwargs": {
                "column": "MY_DATE_COL"
            },
            "meta": {}
        },
        {
            "expectation_context": {
                "description": "MY_TEXT_COL has at least 10 distinct values"
            },
            "expectation_type": "expect_column_unique_value_count_to_be_between",
            "ge_cloud_id": null,
            "kwargs": {
                "column": "MY_TEXT_COL",
                "min_value": 10
            },
            "meta": {}
        },
        {
            "expectation_context": {
                "description": "MY_TEXT_COL has no NULL values"
            },
            "expectation_type": "expect_column_values_to_not_be_null",
            "ge_cloud_id": null,
            "kwargs": {
                "column": "MY_TEXT_COL"
            },
            "meta": {}
        },
        {
            "expectation_context": {
                "description": "MY_NUM_COL has a maximum val between 90 and 110"
            },
            "expectation_type": "expect_column_max_to_be_between",
            "ge_cloud_id": null,
            "kwargs": {
                "column": "MY_NUM_COL",
                "min_value": 90,
                "max_value": 110
            },
            "meta": {}
        },
        {
            "expectation_context": {
                "description": "the table has at least 10 rows"
            },
            "expectation_type": "expect_table_row_count_to_be_between",
            "ge_cloud_id": null,
            "kwargs": {
                "min_value": 10
            },
            "meta": {}
        },
        {
            "expectation_context": {
                "description": "for each row MY_COL_1 plus MY_COL_2 is = 100"
            },
            "expectation_type": "expect_multicolumn_sum_to_equal",
            "ge_cloud_id": null,
            "kwargs": {
                "column_list": [
                    "MY_COL_1",
                    "MY_COL_2"
                ],
                "sum_total": 100
            },
            "meta": {}
        },
        {
            "expectation_context": {
                "description": "the most common value in MY_COL_3 is in the set ['val1', 'val4']"
            },
            "expectation_type": "expect_column_most_common_value_to_be_in_set",
            "ge_cloud_id": null,
            "kwargs": {
                "column": "MY_COL_3",
                "value_set": [
                    "val1",
                    "val4"
                ]
            },
            "meta": {}
        }
    ],
    "ge_cloud_id": null,
    "meta": {
        "great_expectations_version": "0.15.14"
    }
}
```

The corresponding DAG code shows how all the Expectations are run within one task using the GreatExpectationsOperator. Only the root directory of the data context, the schema and the data asset name have to be provided. For a step-by-step example and more information on the parameters of this operator see the [Orchestrate Great Expectations with Airflow](airflow-great-expectations.md) tutorial.

<CodeBlock language="python">{gx_example_dag}</CodeBlock>

## Conclusion

The growth of tools designed to perform data quality checks reflect the importance of ensuring data quality in production workflows. Commitment to data quality requires in-depth planning and collaboration between data professionals. What kind of data quality solution your organization needs will depend on your unique use case, which you can explore using the steps outlined in this guide. Special consideration should be given to the type of data quality checks and their location in the data pipeline.

Integrating Airflow with a data lineage tool can further enhance your ability to trace the origin of data that did not pass the checks you established.

This guide highlights two types of data quality tools and their use cases:

- SQL check operators offer a way to define your checks directly from within the DAG, with no other tools necessary.
- If you run many checks on different databases, you may benefit from using a more complex testing solution like Great Expectations or Soda.

No matter which tool is used, data quality checks can be orchestrated from within an Airflow DAG, which makes it possible to trigger downstream actions depending on the outcome of your checks.
