---
title: "Airflow data quality checks with SQL Operators"
sidebar_label: "SQL check operators"
description: "Executing queries in Apache Airflow DAGs to ensure data quality."
id: "airflow-sql-data-quality"
---

Data quality is key to the success of an organization's data systems. With in-DAG quality checks, you can halt pipelines and alert stakeholders before bad data makes its way to a production lake or warehouse.

Executing SQL queries is one of the most common use cases for data pipelines, and it's a simple and effective way to implement data quality checks. Using Airflow, you can quickly put together a pipeline specifically for checking data quality, or you can add quality checks to existing ETL/ELT pipelines with just a few lines of boilerplate code.

In this guide, you'll learn about three SQL Check operators and how to use them to build a robust data quality suite for your DAGs.

All code used in this guide is located in the [Astronomer Registry](https://github.com/astronomer/airflow-data-quality-demo/).

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- How to design a data quality process. See [Data quality and Airflow](data-quality.md).
- Running SQL from Airflow. See [Using Airflow to execute SQL](airflow-sql.md).

## SQL Check operators

The SQL Check operators are versions of the `SQLOperator` that abstract SQL queries to streamline data quality checks. One difference between the SQL Check operators and the standard [`BaseSQLOperator`](https://airflow.apache.org/docs/apache-airflow/2.2.0/_api/airflow/operators/sql/index.html#airflow.operators.sql.BaseSQLOperator) is that the SQL Check operators respond with a boolean, meaning the task fails when any of the resulting queries fail. This is particularly helpful in stopping a data pipeline before bad data makes it to a given destination. The lines of code and values that fail the check are observable in the Airflow logs.

The following SQL Check operators are recommended for implementing data quality checks:

- **[`SQLColumnCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlcolumncheckoperator)**: Runs multiple predefined data quality checks on multiple columns within the same task.
- **[`SQLTableCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqltablecheckoperator)**: Runs multiple user-defined checks on one or more columns of a table.
- **[`SQLCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlcheckoperator)**: Takes any SQL query and returns a single row that is evaluated to booleans. This operator is useful for more complicated checks that could span several tables of your database.
- **[`SQLIntervalCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlintervalcheckoperator)**: Checks current data against historical data.

Additionally, two older SQL Check operators exist that can run one check at a time against a defined value or threshold:

- [`SQLValueCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlvaluecheckoperator): A simpler operator that can be used when a specific, known value is being checked either as an exact value or within a percentage threshold.
- [`SQLThresholdCheckOperator`](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/sqlthresholdcheckoperator): An operator with flexible upper and lower thresholds, where the threshold bounds may also be described as SQL queries that return a numeric value.

Astronomer recommends using the `SQLColumnCheckOperator` and `SQLTableCheckOperator` over the `SQLValueCheckOperator` and `SQLThresholdCheckOperator` whenever possible to improve code readability.

### Requirements

The `SQLColumnCheckOperator` and the `SQLTableCheckOperator` are available in the [common SQL provider package](https://pypi.org/project/apache-airflow-providers-common-sql/) which can be installed with:

```bash
pip install apache-airflow-providers-common-sql==<version>
```

The `SQLCheckOperator`, `SQLIntervalCheckOperator`, `SQLValueCheckOperator` and `SQLThresholdCheckOperator` are built into core Airflow and do not require a separate package installation.

### Database connection

The SQL Check operators work with any database that can be queried using SQL. You have to define your [connection](connections.md) in the Airflow UI and then pass the connection id to the operator's `conn_id` parameter.

Currently the operators cannot support BigQuery `job_id`s.

The target table can be specified as a string using the `table` parameter for the `SQLColumnCheckOperator` and `SQLTableCheckOperator`. When using the `SQLCheckOperator`, you can override the database defined in your Airflow connection by passing a different value to the `database` argument. The target table for the `SQLCheckOperator` has to be specified in the SQL statement.

## Example: SQLColumnCheckOperator

The `SQLColumnCheckOperator` has a `column_mapping` parameter which stores a dictionary of checks. Using this dictionary, it can run many checks within one task and still provide observability in the Airflow logs over which checks passed and which failed.

This check is useful for:

- Ensuring all numeric values in a column are above a minimum, below a maximum or within a certain range (with or without a tolerance threshold).
- Null checks.
- Checking primary key columns for uniqueness.
- Checking the number of distinct values of a column.

In the example below, 5 checks are performed on 3 different columns using the `SQLColumnCheckOperator`:

- "MY_DATE_COL" is checked to ensure that it contains only unique dates.
- "MY_TEXT_COL" is checked to ensure it has at least 10 distinct values and no `NULL` values.
- "MY_NUM_COL" is checked to ensure it contains a minimum value of less than 10 and a maximum value of 100 with a 10% tolerance (maximum values between 90 and 110 are accepted).

```python
check_columns = SQLColumnCheckOperator(
    task_id="check_columns",
    conn_id="MY_DB_CONNECTION",
    table="MY_TABLE",
    column_mapping={
        "MY_DATE_COL": {"unique_check": {"equal_to": 0}},
        "MY_TEXT_COL": {
            "distinct_check": {"geq_to": 10},
            "null_check": {"equal_to": 0},
        },
        "MY_NUM_COL": {
            "min": {"less_than": 10},
            "max": {"equal_to": 100, "tolerance": 0.1},
        },
    },
)
```

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

You can add a tolerance to the comparisons in the form of a fraction (0.1 = 10% tolerance).

If the boolean value resulting from the check is `True` the check will pass, otherwise it will fail. [Airflow generates logs](logging.md) that show the set of returned records for every check that passes and the full record for checks that failed.

The following example shows the output of 2 successful checks that ran on the `MY_NUM_COL` column of a table in Snowflake using the `SQLColumnCheckOperator`. The checks concerned the minimum value and the maximum value in the column.

The logged line `INFO - Record: (5, 101)` lists the results of the query: the minimum value was 5 and the maximum value was 101, which satisfied the conditions of the check.

```text
[2022-10-25, 06:12:55 UTC] {cursor.py:714} INFO - query: [SELECT MIN(MY_NUM_COL) AS MY_NUM_COL_min,MAX(MY_NUM_COL) AS MY_NUM_COL_max,SUM(C...]
[2022-10-25, 06:12:56 UTC] {cursor.py:738} INFO - query execution done
[2022-10-25, 06:12:56 UTC] {cursor.py:854} INFO - Number of results in first chunk: 1
[2022-10-25, 06:12:56 UTC] {connection.py:564} INFO - closed
[2022-10-25, 06:12:56 UTC] {connection.py:567} INFO - No async queries seem to be running, deleting session
[2022-10-25, 06:12:56 UTC] {sql.py:253} INFO - Record: (5, 101)
[2022-10-25, 06:12:56 UTC] {sql.py:271} INFO - All tests have passed
```

All checks that fail are listed at the end of the task log with their full record of check values. In the following sample entry, the `TASK_DURATION` column failed the check. Instead of a minimum that is greater than or equal to 0, it had a minimum of -12.

```text
Results:
(-12, 1000, 0)
The following tests have failed:
    Column: TASK_DURATION
    Check: min,
    Check Values: {'geq_to': 0, 'result': -12, 'success': False}
```

The SQLColumnCheckOperator converts a returned `result` of `None` to 0 by default and still runs the check.

For example, if a column check for the `MY_COL` column is set to accept a minimum value of -10 or more but runs on an empty table, the check would still pass because the `None` result is treated as 0. You can toggle this behavior by setting `accept_none=False`, which will cause all checks returning `None` to fail.

In previous versions of the provider, running a column check on an empty table always resulted in a failed check.

## Example: Run checks on a subset of a table using `partition_clause`

You can run checks on a subset of your table using either a check-level or task-level `partition_clause` parameter. This parameter takes a SQL `WHERE`-clause (without the `WHERE` keyword) and uses it to filter your table before running a given check or group of checks in a task.

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

## Example: SQLTableCheckOperator

The `SQLTableCheckOperator` provides a way to check the validity of user defined SQL statements which can involve one or more columns of a table. There is no limit to the amount of columns these statements can involve or to their complexity. The statements are provided to the operator as a dictionary with the `checks` parameter.

The `SQLTableCheckOperator` is useful for:

- Checks that include aggregate values using the whole table (e.g. comparing the average of one column to the average of another using the SQL `AVG()` function).
- Row count checks.
- Checking if a date is between certain bounds (for example, using `MY_DATE_COL BETWEEN '2019-01-01' AND '2019-12-31'` to make sure only dates in the year 2019 exist).
- Comparisons between multiple columns, both aggregated and not aggregated.

In the example below, three checks are defined: `my_row_count_check`, `my_column_sum_comparison_check` and  `my_column_addition_check`. The first check runs a SQL statement asserting that the table contains at least 1000 rows, the second check compares the sum of two columns, and the third check confirms that for each row `MY_COL_1 + MY_COL_2 = MY_COL_3` is true.

Similarly to the SQLColumnCheckOperator, you can pass a SQL `WHERE`-clause (without the `WHERE` keyword) to the operator-level `partition_clause` parameter or as a check-level `partition_clause`. All checks of the `table_checks` task below run only on rows in `MY_TABLE` where the date in the `START_DATE` column is 2022-01-01 or later. The `my_column_sum_comparison_check` additionally only runs on rows where the value in `MY_COL_4` is greater than 100.

```python
table_checks = SQLTableCheckOperator(
    task_id="table_checks",
    conn_id="MY_DB_CONNECTION",
    table="MY_TABLE",
    partition_clause="START_DATE >= '2022-01-01'",
    checks={
        "my_row_count_check": {"check_statement": "COUNT(*) >= 1000"},
        "my_column_sum_comparison_check": {
            "check_statement": "SUM(MY_COL_1) < SUM(MY_COL_2)",
            "partition_clause": "MY_COL_4 > 100",
        },
        "my_column_addition_check": {
            "check_statement": "MY_COL_1 + MY_COL_2 = MY_COL_3"
        },
    },
)
```

The operator performs a `CASE WHEN` statement on each of the checks, assigning `1` to the checks that pass and `0` to the checks that fail. Afterwards, the operator looks for the minimum of these results and marks the task as failed if the minimum is `0`. The `SQLTableCheckOperator` produces observable logs similar to those produced for `SQLColumnCheckOperator`.

## Example: SQLCheckOperator

The `SQLCheckOperator` returns a single row from a provided SQL query and checks to see if any of the returned values in that row are `False`. If any values are `False`, the task fails. This operator allows a great deal of flexibility in checking:

- A specific, single column value.
- Part of or an entire row compared to a known set of values.
- Options for categorical variables and data types.
- The results of any other function that can be written as a SQL query.

The following code snippet shows you how to use the operator in a DAG:

```python
yellow_tripdata_row_quality_check = SQLCheckOperator(
    conn_id="example_conn",
    task_id="yellow_tripdata_row_quality_check",
    sql="row_quality_yellow_tripdata_check.sql",
    params={"pickup_datetime": "2021-01-01"},
)
```

The `sql` argument can be either a complete SQL query as a string or, as in this example, a reference to a query in a local file. In Astronomer projects, this is in the `include/` directory. The `params` argument allows you to pass a dictionary of values to the SQL query, which can be accessed through the `params` keyword in the query. The `conn_id` argument points towards a previously defined Airflow connection to a database. The full code can be found in the [data quality demo repository](https://github.com/astronomer/airflow-data-quality-demo/).

Because the `SQLCheckOperator` can process a wide variety of queries, it's important to use the right SQL query for the job. The following sample query (which is passed into the `sql` argument) was crafted for the specific use case of analyzing daily taxicab data. So, the values checked in each equation come from domain knowledge. Even the `WHERE` clause needs a data steward to know that both the `vendor_id` and `pickup_datetime` are needed to return a unique row.

The query used in the `sql` argument is:

```sql
SELECT vendor_id, pickup_datetime,
  CASE
    WHEN dropoff_datetime > pickup_datetime THEN 1
    ELSE 0
  END AS date_check,
  CASE
    WHEN passenger_count >= 0
    THEN 1 ELSE 0
  END AS passenger_count_check,
  CASE
    WHEN trip_distance >= 0 AND trip_distance <= 100
    THEN 1 ELSE 0
  END AS trip_distance_check,
  CASE
    WHEN ROUND((fare_amount + extra + mta_tax + tip_amount + \
      improvement_surcharge + COALESCE(congestion_surcharge, 0)), 1) = \
      ROUND(total_amount, 1) THEN 1
    WHEN ROUND(fare_amount + extra + mta_tax + tip_amount + \
      improvement_surcharge, 1) = ROUND(total_amount, 1) THEN 1
    ELSE 0
  END AS fare_check
FROM yellow_tripdata
WHERE pickup_datetime IN (SELECT pickup_datetime
                          FROM yellow_tripdata
                          ORDER BY RANDOM()
                          LIMIT 1)
```

If you want to use a specific date to quality check a row instead of using a random `pickup_datetime`, you can use the `params` passed into the operator. For example:

```sql
WHERE pickup_datetime = '{{ params.pickup_datetime }}'
```

By using `CASE` statements in the SQL query, you can check very specific cases of data quality that should always be true for this use case:

- Drop-offs always occur after pickups.
- A trip is only valid if there is at least one passenger.
- A trip needs to be in a range allowed by the taxi company (in this case, it is assumed there is a maximum allowed trip distance of 100 miles).
- Each of the components of the total fare should add up to the total fare.

Using a for loop, tasks are generated to run this check on every row or other subset of the data. In the SQL above, a `pickup_datetime` is chosen randomly, and the corresponding code uses a loop to spot-check ten rows. In the example DAG below, you can see how the loop results in `TaskGroups` that can be collapsed or expanded in the Airflow UI:

![An example DAG showing data quality checks as part of a pipeline.](/img/guides/example_dq_dag.png)

In the previous example DAG, you learned how your data quality checks fit into a pipeline. By loading the data into Redshift then performing checks as queries, you are offloading compute resources from Airflow to Redshift, which frees up Airflow to act only as an orchestrator.

For a production pipeline, data could first be loaded from S3 to a temporary staging table, then have its quality checks completed. If the quality checks succeed, another `SQLOperator` can load the data from staging to a production table. If the data quality checks fail, the pipeline can be stopped, and the staging table can be either used to help diagnose the data issue or scrapped to save resources. To see the complete example DAG and run it for yourself, see the [data quality demo repository](https://github.com/astronomer/airflow-data-quality-demo/).

## Conclusion

After reading this guide, you should feel comfortable using the SQL Check operators, understand how each one works, and get a sense of when each one would be useful. With these operators you have the foundation for a robust data quality suite right in your pipelines. If you are looking for more examples, or want to see how to use backend-specific operators like Redshift, BigQuery, or Snowflake, see the [data quality demo repository](https://github.com/astronomer/airflow-data-quality-demo/).
