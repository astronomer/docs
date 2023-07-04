---
title: "Airflow data quality checks with SQL Operators"
sidebar_label: "SQL check operators"
description: "Executing queries in Apache Airflow DAGs to ensure data quality."
id: "airflow-sql-data-quality"
---

import CodeBlock from '@theme/CodeBlock';
import sql_data_quality from '!!raw-loader!../code-samples/dags/airflow-sql-data-quality/sql_data_quality.py';

Data quality is key to the success of an organization's data systems. With in-DAG quality checks, you can halt pipelines and alert stakeholders before bad data makes its way to a production lake or warehouse.

The SQL check operators are a simple and effective way to implement data quality checks in your Airflow DAGs. Using this set of operators, you can quickly put together a pipeline specifically for checking data quality, or you can add data quality checks to existing pipelines with just a few more lines of code.

This tutorial shows how to use three SQL check operators (SQLColumnCheckOperator, SQLTableCheckOperator and SQLCheckOperator) to build a robust data quality suite for your DAGs.

:::info

You can find more examples of data quality checks in pipelines in the [data quality demo repository](https://github.com/astronomer/airflow-data-quality-demo/).

:::

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, you should have an understanding of:

- How to design a data quality process. See [Data quality and Airflow](data-quality.md).
- Running SQL from Airflow. See [Using Airflow to execute SQL](airflow-sql.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A love for birds.

## Step 1: Configure your Astro project

To use SQL check operators, install the [Common SQL provider](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/versions/latestb) in your Astro project. This tutorial also requires access to a relational database. You can use an in-memory SQLite database for which you'll need to install the [SQLite provider](https://registry.astronomer.io/providers/apache-airflow-providers-sqlite/versions/latest).

1. Create a new Astro project:

    ```sh
    $ mkdir astro-sql-check-tutorial && cd astro-sql-check-tutorial
    $ astro dev init
    ```

2. Add the Common SQL provider and the SQLite provider to your Astro project `requirements.txt` file.

    ```text
    apache-airflow-providers-common-sql==1.5.2
    apache-airflow-providers-sqlite==3.4.2
    ```

## Step 2: Create a connection to SQLite

1. In the Airflow UI, go to **Admin** > **Connections** and click **+**.

2. Create a new connection named `sqlite_conn` and choose the `SQLite` connection type. Enter the following information:

    - **Connection Id**: `sqlite_conn`.
    - **Connection Type**: `SQLite`.
    - **Host**: `/tmp/sqlite.db`.

## Step 3: Add a SQL file with a custom check

1. In the `include` folder, create a file called `custom_check.sql`.

2. Copy and past the following SQL statement into the file:

  ```sql
  WITH all_combinations_unique AS (
  SELECT DISTINCT bird_name, observation_year AS combos_unique
    FROM '{{ params.table_name }}'
    )
  SELECT CASE
    WHEN COUNT(*) = COUNT(combos_unique) THEN 1
    ELSE 0
  END AS is_unique
  FROM '{{ params.table_name }}' JOIN all_combinations_unique;
  ```

  This SQL statement returns 1 if all combinations of `bird_name` and `observation_year` in a templated table are unique, and 0 if not.

## Step 4: Create a DAG using SQL check operators

1. Start Airflow by running `astro dev start`.

2. Create a new file in your `dags` folder called `sql_data_quality.py`.

3. Copy and paste the following DAG code into the file:

    <CodeBlock language="python">{sql_data_quality}</CodeBlock>

    This DAG creates and populates a small SQlite table `birds` with information about birds. Then, three tasks containing data quality checks are run on the table:

    - The `column_checks` task uses the `SQLColumnCheckOperator`. The operator uses a operator-level [`partition_clause`](#partition_clause) which is `bird_name IS NOT NULL`. This means all checks contained in the `column_mapping` dictionary only run on rows where the `bird_name` column is not null. The `column_mapping` dictionary contains checks on all three columns:
      - `bird_name`: This column is checked to not have any null values and at least 2 distinct values.
      - `observation_year`: This column is checked to only have values below 2023.
      - `bird_happiness`: This columns is checked to only have values between 0 and 10.
    
    - The `table_checks` task uses the `SQLTableCheckOperator`. The operator does not have an operator-level [`partition_clause`](#partition_clause). The `checks` dictionary for this task contains two checks:
      - `row_count_check`: This check makes sure the table has a least three rows.
      - `average_happiness_check`: This check makes sure the average happiness of the birds is at least 9. This check has a check-level `partition_clause` which is `observation_year >= 2021`. This means the check only runs on rows with observations from 2021 onwards.
    
    - The `custom_check` task uses the `SQLCheckOperator`. This operator can run any SQL statement that returns a single row and will deem the data quality check failed if the that row contains any value [Python bool casting](https://docs.python.org/3/library/stdtypes.html) evaluates as `False`, for example `0`. Otherwise, the data quality check and the task will be marked as successful. This task will run the SQL statement in the file `include/custom_check.sql` on the `table_name` passed as a parameter. Note that in order to run SQL stored in a file, the path to the SQL file has to be added to the `template_searchpath` parameter of the DAG.

4. Open Airflow at `http://localhost:8080/`. Run the DAG manually by clicking the play button, then click the DAG name to view the DAG in the **Grid** view. All checks are set up to pass.

  ![Data quality check DAG grid view](/img/tutorials/airflow-sql-data-quality_dag_grid.png)

5. View the logs of the SQL check operators to get detailed information about the checks that were run and their results:

    Logs for the `column_checks` task show the five individual checks that were run on three columns:

    ```text
    [2023-07-04, 11:18:01 UTC] {sql.py:374} INFO - Running statement: SELECT col_name, check_type, check_result FROM (
          SELECT 'bird_name' AS col_name, 'null_check' AS check_type, bird_name_null_check AS check_result
          FROM (SELECT SUM(CASE WHEN bird_name IS NULL THEN 1 ELSE 0 END) AS bird_name_null_check FROM birds WHERE bird_name IS NOT NULL) AS sq
      UNION ALL
          SELECT 'bird_name' AS col_name, 'distinct_check' AS check_type, bird_name_distinct_check AS check_result
          FROM (SELECT COUNT(DISTINCT(bird_name)) AS bird_name_distinct_check FROM birds WHERE bird_name IS NOT NULL) AS sq
      UNION ALL
          SELECT 'observation_year' AS col_name, 'max' AS check_type, observation_year_max AS check_result
          FROM (SELECT MAX(observation_year) AS observation_year_max FROM birds WHERE bird_name IS NOT NULL) AS sq
      UNION ALL
          SELECT 'bird_happiness' AS col_name, 'min' AS check_type, bird_happiness_min AS check_result
          FROM (SELECT MIN(bird_happiness) AS bird_happiness_min FROM birds WHERE bird_name IS NOT NULL) AS sq
      UNION ALL
          SELECT 'bird_happiness' AS col_name, 'max' AS check_type, bird_happiness_max AS check_result
          FROM (SELECT MAX(bird_happiness) AS bird_happiness_max FROM birds WHERE bird_name IS NOT NULL) AS sq
      ) AS check_columns, parameters: None
    [2023-07-04, 11:18:01 UTC] {sql.py:397} INFO - Record: [('bird_name', 'null_check', 0), ('bird_name', 'distinct_check', 4), ('observation_year', 'max', 2022), ('bird_happiness', 'min', 8), ('bird_happiness', 'max', 10)]
    [2023-07-04, 11:18:01 UTC] {sql.py:420} INFO - All tests have passed
    ```

    Logs for the `table_checks` task show the two table-wide checks that ran:

    ```text
    [2023-07-04, 11:18:01 UTC] {sql.py:374} INFO - Running statement: SELECT check_name, check_result FROM (
        SELECT 'row_count_check' AS check_name, MIN(row_count_check) AS check_result
        FROM (SELECT CASE WHEN COUNT(*) >= 3 THEN 1 ELSE 0 END AS row_count_check
              FROM birds ) AS sq
        UNION ALL
        SELECT 'average_happiness_check' AS check_name, MIN(average_happiness_check) AS check_result
        FROM (SELECT CASE WHEN AVG(bird_happiness) >= 9 THEN 1 ELSE 0 END AS average_happiness_check
              FROM birds WHERE observation_year >= 2021) AS sq
        ) AS check_table, parameters: None
    [2023-07-04, 11:18:01 UTC] {sql.py:607} INFO - Record:
    [('row_count_check', 1), ('average_happiness_check', 1)]
    [2023-07-04, 11:18:01 UTC] {sql.py:625} INFO - All tests have passed
    ```

    Logs for the `custom_check` task shows the custom SQL statement that was run:

    ```text
    [2023-07-04, 11:18:01 UTC] {sql.py:374} INFO - Running statement: WITH all_combinations_unique AS (
      SELECT DISTINCT bird_name, observation_year AS combos_unique
      FROM 'birds'
      )
    SELECT CASE
      WHEN COUNT(*) = COUNT(combos_unique) THEN 1
      ELSE 0
    END AS is_unique
    FROM 'birds' JOIN all_combinations_unique;, parameters: None
    [2023-07-04, 11:18:01 UTC] {sql.py:710} INFO - Record: (1,)
    [2023-07-04, 11:18:01 UTC] {sql.py:716} INFO - Success.
    ```

## Conclusion

With the SQL check operators you have the foundation for a robust data quality suite right in your pipelines. If you are looking for more examples, or want to see how to use backend-specific operators like Redshift, BigQuery, or Snowflake, see the [data quality demo repository](https://github.com/astronomer/airflow-data-quality-demo/).

## How it works

The SQL Check operators are versions of the `SQLOperator` that abstract SQL queries to streamline data quality checks. One difference between the SQL Check operators and the standard [`BaseSQLOperator`](https://airflow.apache.org/docs/apache-airflow/2.2.0/_api/airflow/operators/sql/index.html#airflow.operators.sql.BaseSQLOperator) is that the SQL Check operators respond with a boolean, meaning the task fails when any of the resulting queries fail. This is particularly helpful in stopping a data pipeline before bad data makes it to a given destination. The lines of code and values that fail the check are observable in the Airflow logs.

The following SQL Check operators are recommended for implementing data quality checks:

- **[`SQLColumnCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlcolumncheckoperator)**: Runs multiple predefined data quality checks on multiple columns within the same task.
- **[`SQLTableCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqltablecheckoperator)**: Runs multiple user-defined checks on one or more columns of a table.
- **[`SQLCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlcheckoperator)**: Takes any SQL query and returns a single row that is evaluated to booleans. This operator is useful for more complicated checks that could span several tables of your database.
- **[`SQLIntervalCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlintervalcheckoperator)**: Checks current data against historical data.

Additionally, two older SQL Check operators exist that can run one check at a time against a defined value or threshold:

- [`SQLValueCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlvaluecheckoperator): A simpler operator that can be used when a specific, known value is being checked either as an exact value or within a percentage threshold.
- [`SQLThresholdCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlthresholdcheckoperator): An operator with flexible upper and lower thresholds, where the threshold bounds may also be described as SQL queries that return a numeric value.

Astronomer recommends using the `SQLColumnCheckOperator` and `SQLTableCheckOperator` over the `SQLValueCheckOperator` and `SQLThresholdCheckOperator` whenever possible to improve code readability. Note that currently the operators cannot support BigQuery `job_id`s.

### SQLColumnCheckOperator

The `SQLColumnCheckOperator` has a `column_mapping` parameter which stores a dictionary of checks. Using this dictionary, it can run many checks within one task and still provide observability in the Airflow logs over which checks passed and which failed.

This operator is useful for:

- Ensuring all numeric values in a column are above a minimum, below a maximum or within a certain range (with or without a tolerance threshold).
- Null checks.
- Checking primary key columns for uniqueness.
- Checking the number of distinct values of a column.

The `SQLColumnCheckOperator` offers 5 options for column checks which are abstractions over SQL statements:

- "min": `"MIN(column) AS column_min"`
- "max": `"MAX(column) AS column_max"`
- "unique_check": `"COUNT(column) - COUNT(DISTINCT(column)) AS column_unique_check"`
- "distinct_check": `"COUNT(DISTINCT(column)) AS column_distinct_check"`
- "null_check": `"SUM(CASE WHEN column IS NULL THEN 1 ELSE 0 END) AS column_null_check"`

The resulting values can be compared to an expected value using any of the following qualifiers:

- `greater_than`
- `geq_to` (greater or equal than)
- `equal_to`
- `leq_to` (lesser or equal than)
- `less_than`

Additionally, the SQLColumnCheckOperator:

- allows you to specify a tolerance to the comparisons in the form of a fraction (0.1 = 10% tolerance).
- converts a returned `result` of `None` to 0 by default and still runs the check. For example, if a column check for the `MY_COL` column is set to accept a minimum value of -10 or more but runs on an empty table, the check would still pass because the `None` result is treated as 0. You can toggle this behavior by setting `accept_none=False`, which will cause all checks returning `None` to fail. In previous versions of the provider, running a column check on an empty table always resulted in a failed check.
- accepts an operator-level `partition_clause` parameter that allows you to run checks on a subset of your table. See the [partition_clause](#partition_clause) section for more information.

### SQLTableCheckOperator

The `SQLTableCheckOperator` provides a way to check the validity of user defined SQL statements which can involve one or more columns of a table. There is no limit to the amount of columns these statements can involve or to their complexity. The statements are provided to the operator as a dictionary with the `checks` parameter.

The `SQLTableCheckOperator` is useful for:

- Checks that include aggregate values using the whole table (e.g. comparing the average of one column to the average of another using the SQL `AVG()` function).
- Row count checks.
- Checking if a date is between certain bounds (for example, using `MY_DATE_COL BETWEEN '2019-01-01' AND '2019-12-31'` to make sure only dates in the year 2019 exist).
- Comparisons between multiple columns, both aggregated and not aggregated.

Similarly to the SQLColumnCheckOperator, you can pass a SQL `WHERE`-clause (without the `WHERE` keyword) to the operator-level [`partition_clause`](#partition_clause) parameter or as a check-level `partition_clause`.

### SQLCheckOperator

The `SQLCheckOperator` returns a single row from a provided SQL query and checks to see if any of the returned values in that row are a value [Python bool casting](https://docs.python.org/3/library/stdtypes.html) evaluates as `False`, for example `0`. If any values are `False`, the task fails. This operator allows a great deal of flexibility in checking:

- A specific, single column value.
- Part of or an entire row compared to a known set of values.
- Options for categorical variables and data types.
- The results of any other function that can be written as a SQL query.

The target table for the `SQLCheckOperator` has to be specified within the SQL statement. The `sql` parameter of this operator can be either a complete SQL query as a string or, as in this turtorial example, a reference to a query stored in a local file. 

### `partition_clause`

When using the SQLColumnCheckOperator and SQLTableCheckOperator, you can run checks on a subset of your table using either a check-level or task-level `partition_clause` parameter. This parameter takes a SQL `WHERE`-clause (without the `WHERE` keyword) and uses it to filter your table before running a given check or group of checks in a task.

The code snippet below shows a SQLColumnCheckOperator defined with a `partition_clause` at the operator level, as well as a `partition_clause` in one of the two column checks defined in the `column_mapping`. 

In the following example, the operator checks whether:

- `MY_NUM_COL_1` has a minimum value greater than 10.
- `MY_NUM_COL_2` has a maximum value less than 300. Only rows that fulfill the check-level `partition_clause` are checked (rows where `CUSTOMER_STATUS = 'active'`).

Both of the above checks only run on rows that fulfill the operator-level partition clause `CUSTOMER_NAME IS NOT NULL`. If both an operator-level `partition_clause` and a check-level `partition_clause` are defined for a check, the check will only run on rows fulfilling both clauses.

```python
column_checks = SQLColumnCheckOperator(
    task_id="column_checks",
    conn_id="MY_DB_CONNECTION",
    table="MY_TABLE",
    partition_clause="CUSTOMER_NAME IS NOT NULL",
    column_mapping={
        "MY_NUM_COL_1": {"min": {"greater_than": 10}},
        "MY_NUM_COL_2": {
            "max": {"less_than": 300, "partition_clause": "CUSTOMER_STATUS = 'active'"}
        },
    },
)
```
