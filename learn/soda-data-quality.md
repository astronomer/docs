---
title: "Run Soda Core checks with Airflow"
description: "Learn how to orchestrate Soda Core data quality checks with your Airflow DAGs."
id: soda-data-quality
sidebar_label: "Soda Core"
sidebar_custom_props: { icon: 'img/integrations/soda.png' }
---

[Soda Core](https://www.soda.io/core) is an open source framework for checking data quality. It uses the Soda Checks Language (SodaCL) to run checks defined in a YAML file.

Soda Core lets you:

- Define checks as YAML configuration, including many preset checks.
- Provide a SQL query within the YAML file and check against a returned value if no preset checks fit your use case.
- Integrate data quality checks with commonly used data engineering tools such as Airflow, Apache Spark, PostgreSQL, Snowflake [and more](https://www.soda.io/integrations).

In this tutorial, you'll learn about the key features of Soda Core and how to use Airflow to run data quality checks on a database.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- How to design a data quality process. See [Data quality and Airflow](data-quality.md).
- The basics of Soda Core. See [How Soda Core works](https://docs.soda.io/soda-core/how-core-works.html).
- How to use the BashOperator. See [Using the BashOperator](bashoperator.md).
- Relational Databases. See [IBM's "Relational Databases Explained"](https://www.ibm.com/cloud/learn/relational-databases).
- Familiarity with writing YAML configurations. See [yaml.org](https://yaml.org/).

## Prerequisites

To complete this tutorial, you need:

- The Soda Core package for your database backend. The [Soda documentation](https://docs.soda.io/soda-core/configuration.html) provides a list of supported databases and how to configure them. This tutorial uses Snowflake.
- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

## Step 1: Configure your Astro project

Configure a new Astro project to run Airflow locally.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-soda-tutorial && cd astro-soda-tutorial
    $ astro dev init
    ```

2. Add the following line to the `requirements.txt` file of your Astro project:

    ```text
    soda-core-snowflake
    ```

    This installs the relevant Soda Core Python package. If you are using a different database backend, replace `snowflake` with your backend. See the [Prerequisites](#prerequisites) section for more details.

3. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 2: Create the configuration file

Create a configuration file to connect to your database backend. The following example uses the template from the Soda documentation to create the configuration file for Snowflake.

```yaml
# the first line names the datasource "MY_DATASOURCE"
data_source MY_DATASOURCE:
  type: snowflake
  connection:
    # provide your snowflake username and password in double quotes
    username: "MY_USERNAME"
    password: "MY_PASSWORD"
    # provide the account in the format xy12345.eu-central-1
    account: my_account
    database: MY_DATABASE
    warehouse: MY_WAREHOUSE
    # if your connection times out you may need to adjust the timeout value
    connection_timeout: 300
    role: MY_ROLE
    client_session_keep_alive:
    session_parameters:
      QUERY_TAG: soda-queries
      QUOTED_IDENTIFIERS_IGNORE_CASE: false
  schema: MY_SCHEMA
```

Save the YAML instructions in a file named `configuration.yml` and place the file into the `/include` directory of your Astro project.

## Step 3: Create the checks file

Define your data quality checks using the [many preset checks available for SodaCL](https://docs.soda.io/soda-cl/soda-cl-overview.html). For more details on creating checks, see [How it works](#how-it-works). If you cannot find a preset check that works for your use case, you can create a custom one using SQL as shown in the following example.

```yaml
checks for example_table:
  # check that MY_EMAIL_COL contains only email addresses according to the
  # format name@domain.extension
  - invalid_count(MY_EMAIL_COL) = 0:
      valid format: email
  # check that all entries in MY_DATE_COL are unique
  - duplicate_count(MY_DATE_COL) = 0
  # check that MY_TEXT_COL has no missing values
  - missing_count(MY_TEXT_COL) = 0
  # check that MY_TEXT_COL has at least 10 distinct values using SQL
  - distinct_vals >= 10:
      distinct_vals query: |
        SELECT DISTINCT(MY_TEXT_COL) FROM example_table
  # check that MY_NUM_COL has a minimum between 90 and 110
  - min(MY_NUM_COL) between 90 and 110
  # check that example table has at least 1000 rows
  - row_count >= 1000
  # check that the sum of MY_COL_2 is bigger than the sum of MY_COL_1
  - sum_difference > 0:
      sum_difference query: |
        SELECT SUM(MY_COL_2) - SUM(MY_COL_1) FROM example_table
  # checks that all entries in MY_COL_3 are part of a set of possible values
  - invalid_count(MY_COL_3) = 0:
      valid values: [val1, val2, val3, val4]
```

Save the YAML instructions in a file named `checks.yml` and place the file in the `/include` directory of your Astro project.

## Step 4: Create your DAG

In your Astro project `dags/` folder, create a new file called `soda-pipeline.py`. Paste the following code into the file:

```python
from airflow import DAG
from datetime import datetime

from airflow.operators.bash import BashOperator

SODA_PATH="<filepath>" # can be specified as an env variable

with DAG(
    dag_id="soda_example_dag",
    schedule='@daily',
    start_date=datetime(2022,8,1),
    catchup=False
) as dag:

    soda_test = BashOperator(
        task_id="soda_test",
        bash_command=f"soda scan -d MY_DATASOURCE -c \
            {SODA_PATH}/configuration.yml {SODA_PATH}/checks.yml"
    )
```

In this DAG, Soda Core checks are executed by using the BashOperator to run the `soda scan` command referencing the configuration and check YAML files.

## Step 5: Run your DAG and review check results

Go to the Airflow UI, unpause your `soda_example_dag` DAG, and trigger it to run the Soda Core data quality checks. Go to the task log to see a list of all checks that ran and their results.

This is an example of what your logs might look like when 3 out of 3 checks pass:

```text
[2022-08-04, 13:07:22 UTC] {subprocess.py:92} INFO - Scan summary:
[2022-08-04, 13:07:22 UTC] {subprocess.py:92} INFO - 3/3 checks PASSED:
[2022-08-04, 13:07:22 UTC] {subprocess.py:92} INFO -     MY_TABLE in MY_DATASOURCE
[2022-08-04, 13:07:22 UTC] {subprocess.py:92} INFO -       duplicate_count(MY_ID_COLUMN) = 0 [PASSED]
[2022-08-04, 13:07:22 UTC] {subprocess.py:92} INFO -       missing_count(MY_ID_COLUMN) = 0 [PASSED]
[2022-08-04, 13:07:22 UTC] {subprocess.py:92} INFO -       min(MY_NUM_COL) between 0 and 10 [PASSED]
[2022-08-04, 13:07:22 UTC] {subprocess.py:92} INFO - All is good. No failures. No warnings. No errors.
```

In the case of a check failure, the logs show which check failed and the `check_value` that caused the failure:

```text
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO - Scan summary:
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO - 2/3 checks PASSED:
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO -     MY_TABLE in MY_DATASOURCE
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO -       duplicate_count(MY_ID_COLUMN) = 0 [PASSED]
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO -       missing_count(MY_ID_COLUMN) = 0 [PASSED]
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO - 1/3 checks FAILED:
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO -     MY_TABLE in MY_DATASOURCE
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO -       max(MY_NUM_COL) between 10 and 20 [FAILED]
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO -         check_value: 3
[2022-08-04, 13:23:59 UTC] {subprocess.py:92} INFO - Oops! 1 failures. 0 warnings. 0 errors. 2 pass.
[2022-08-04, 13:24:00 UTC] {subprocess.py:96} INFO - Command exited with return code 2
[2022-08-04, 13:24:00 UTC] {taskinstance.py:1909} ERROR - Task failed with exception
Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/airflow/operators/bash.py", line 194, in execute
    raise AirflowException(
airflow.exceptions.AirflowException: Bash command failed. The command returned a non-zero exit code 2.
```

## How it works

Soda Core uses the Soda Checks Language (SodaCL) to run data quality checks defined in a YAML file.  Integrating Soda Core into your Airflow data pipelines lets you use the results of data quality checks to influence downstream tasks. For an overview of SodaCL, see the [SodaCL documentation](https://docs.soda.io/soda-cl/soda-cl-overview.html).

As shown in the following example, you can use Soda Core to run checks on different properties of your dataset against a numerically defined threshold:

```yaml
checks for MY_TABLE_1:
  # MY_NUM_COL_1 has a minimum of above or equal 0
  - min(MY_NUM_COL_1) >= 0
  # MY_TEXT_COL has less than 10% missing values
  - missing_percent(MY_TEXT_COL) < 10
checks for MY_TABLE_2:
  # MY_NUM_COL_2 has an average between 100 and 1000
  - avg(MY_NUM_COL_2) is between 100 and 1000
  # MY_ID_COL has no duplicates
  - duplicate_count(MY_ID_COL) = 0
```

You can add optional configurations, such as custom names for checks and error levels:

```yaml
checks for MY_TABLE_1:
  # fail the check when MY_TABLE_1 has less than 10 or more than a million rows
  # warn if there are less than 100 (but 10 or more) rows
  - row_count:
      warn: when < 100
      fail:
        when < 10
        when > 1000000
      name: Wrong number of rows!
```

You can use the following methods to check the validity of data:

- List of valid values
- Predefined valid format
- Regex
- SQL query

```yaml
checks for MY_TABLE_1:
  # MY_CATEGORICAL_COL has no other values than val1, val2 and val3
  - invalid_count(MY_CATEGORICAL_COL) = 0:
      valid values: [val1, val2, val3]
  # MY_NUMERIC_COL has no other values than 0, 1 and 2.
  # Single quotes are necessary for valid values checks involving numeric
  # characters.
  - invalid_count(MY_NUMERIC_COL) = 0:
      valid values: ['0', '1', '2']
  # less than 10 missing valid IP addresses
  - missing_count(IP_ADDRESS_COL) < 10:
      valid format: ip address
  # WEBSITE_COL has less than 5% entries that don't contain "astronomer.io"
  - invalid_percent(WEBSITE_COL) < 5:
      valid regex: astronomer\.io
  # The average of 3 columns for values of category_1 is between 10 and 100
  - my_average_total_for_category_1 between 10 and 100:
      my_average_total_for_category_1 query: |
        SELECT AVG(MY_COL_1 + MY_COL_2 + MY_COL_3)
        FROM MY_TABLE_1
        WHERE MY_CATEGORY = 'category_1'
```

Three more unique features of Soda Core are:

- [Freshness checks](https://docs.soda.io/soda-cl/freshness.html): Set limits to the age of the youngest row in the table.
- [Schema checks](https://docs.soda.io/soda-cl/schema.html): Run checks on the existence of columns and validate data types.
- [Reference checks](https://docs.soda.io/soda-cl/reference.html): Ensure parity in between columns in different datasets in the same data source.

```yaml
checks for MY_TABLE_1:
  # MY_DATE's youngest row is younger 10 days
  - freshness(MY_DATE) < 10d
  # The schema has to have the MY_KEY column
  - schema:
      fail:
        when required column missing: [MY_KEY]
  # all names listed in MY_TABLE_1's MY_NAMES column have to also exist
  # in the MY_CUSTOMER_NAMES column in MY_TABLE_2
  - values in (MY_NAMES) must exist in MY_TABLE_2 (MY_CUSTOMER_NAMES)
```
