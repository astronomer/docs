---
title: "Orchestrate Snowflake Queries with Airflow"
description: "Get enhanced observability and compute savings while orchestrating Snowflake jobs from your Airflow DAGs."
id: airflow-snowflake
sidebar_label: Snowflake
---

[Snowflake](https://www.snowflake.com/) is one of the most commonly used data warehouses. Orchestrating Snowflake queries as part of a data pipeline is one of the most common Airflow use cases. Using Airflow with Snowflake is straightforward, and there are multiple open source packages, tools, and integrations that can help you realize the full potential of your existing Snowflake instance.

This guide covers the following topics:

- Using Snowflake providers and the available modules, and how to implement deferrable versions of common operators.
- Leveraging the OpenLineage Airflow integration to get data lineage and enhanced observability from your Snowflake jobs.
- Using the Astro SDK for the next generation of DAG authoring for Snowflake query tasks.
- General best practices and considerations when interacting with Snowflake from Airflow.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- Snowflake basics. See [Introduction to Snowflake](https://docs.snowflake.com/en/user-guide-intro.html).
- Airflow operators. See [Airflow operators](what-is-an-operator.md).
- SQL basics. See the [W3 SQL tutorial](https://www.w3schools.com/sql/).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- A Snowflake account. A [30-day free trial](https://signup.snowflake.com/) is available.

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-snowflake-tutorial && cd astro-snowflake-tutorial
    $ astro dev init
    ```

2. Ensure that you are using version 7.0.0 or newer of the Astro Runtime (Airflow 2.5+) and that version 4.0.2+ of the [Snowflake provider package](https://registry.astronomer.io/providers/snowflake) and version 1.3.1+ of the [Common SQL provider package](https://registry.astronomer.io/providers/common-sql) are installed. If you are creating a new Astro project with the Astro CLI, these packages come pre-installed in their latest version and no further action is necessary.

3. Start your Airflow project by running:

    ```sh
    $ astro dev start
    ```

## Step 2: Configure your Snowflake connection

1. Navigate to **Admin** -> **Connections** in the Airflow UI and click on the **+** sign. 

2. Give your new connection the connection ID `snowflake_default` and fill out the fields for [`Schema`](https://docs.snowflake.com/en/sql-reference/sql/create-schema.html), `Login`, `Password`, `Account`, [`Database`](https://docs.snowflake.com/en/sql-reference/sql/create-database.html) and `Region` with your credentials as shown in the screenshot below. The user you provide needs to have sufficient permissions to create and write to new tables in the Snowflake schema you are providing.

    ![Snowflake connection](/img/guides/snowflake_tutorial_connection.png)

## Step 3: Add your SQL statements

The DAG you will create in Step 4 contains references to multiple SQL statements. While it is possible to add SQL statements directly within the DAG code a modular approach with SQL statements being saved in a dedicated folder in the `include` directory is best practice.

1. Create a new folder in your include directory called `sql` with an empty `__init__.py` file. 

    ```sh
    $ mkdir include/sql && touch include/sql/__init__.py

2. Create a new file in `include/sql` called `tutorial_sql_statements.py` and add copy the following code which contains 7 SQL statements:

    ```python
    create_forestfire_table = """
        CREATE OR REPLACE TRANSIENT TABLE {{ params.table_name }}
            (
                id INT,
                y INT,
                month VARCHAR(25),
                day VARCHAR(25),
                ffmc FLOAT,
                dmc FLOAT,
                dc FLOAT,
                isi FLOAT,
                temp FLOAT,
                rh FLOAT,
                wind FLOAT,
                rain FLOAT,
                area FLOAT
            );
    """

    create_cost_table = """
        CREATE OR REPLACE TRANSIENT TABLE {{ params.table_name }}
            (
                id INT,
                land_damage_cost INT,
                property_damage_cost INT,
                lost_profits_cost INT
            );
    """

    create_forestfire_cost_table = """
        CREATE OR REPLACE TRANSIENT TABLE {{ params.table_name }}
            (
                id INT,
                land_damage_cost INT,
                property_damage_cost INT,
                lost_profits_cost INT,
                total_cost INT,
                y INT,
                month VARCHAR(25),
                day VARCHAR(25),
                area FLOAT
            );
    """

    load_forestfire_data = """
        INSERT INTO {{ params.table_name }} VALUES
            (1,2,'aug','fri',91,166.9,752.6,7.1,25.9,41,3.6,0,100),
            (2,2,'feb','mon',84,9.3,34,2.1,13.9,40,5.4,0,57.8),
            (3,4,'mar','sat',69,2.4,15.5,0.7,17.4,24,5.4,0,92.9),
            (4,4,'mar','mon',87.2,23.9,64.7,4.1,11.8,35,1.8,0,1300),
            (5,5,'mar','sat',91.7,35.8,80.8,7.8,15.1,27,5.4,0,4857),
            (6,5,'sep','wed',92.9,133.3,699.6,9.2,26.4,21,4.5,0,9800),
            (7,5,'mar','fri',86.2,26.2,94.3,5.1,8.2,51,6.7,0,14),
            (8,6,'mar','fri',91.7,33.3,77.5,9,8.3,97,4,0.2,74.5),
            (9,9,'feb','thu',84.2,6.8,26.6,7.7,6.7,79,3.1,0,8880.7);
    """

    load_cost_data = """
        INSERT INTO {{ params.table_name }} VALUES
            (1,150000,32000,10000),
            (2,200000,50000,50000),
            (3,90000,120000,300000),
            (4,230000,14000,7000),
            (5,98000,27000,48000),
            (6,72000,800000,0),
            (7,50000,2500000,0),
            (8,8000000,33000000,0),
            (9,6325000,450000,76000);
    """

    load_forestfire_cost_data = """
        INSERT INTO forestfire_costs (id, land_damage_cost, property_damage_cost, lost_profits_cost, total_cost, y, month, day, area)
            SELECT
                c.id,
                c.land_damage_cost,
                c.property_damage_cost,
                c.lost_profits_cost,
                c.land_damage_cost + c.property_damage_cost + c.lost_profits_cost,
                ff.y,
                ff.month,
                ff.day,
                ff.area
            FROM costs c
            LEFT JOIN forestfires ff
                ON c.id = ff.id
    """

    transform_forestfire_cost_table = """
        SELECT
            id,
            month,
            day,
            total_cost,
            area,
            total_cost / area as cost_per_area
        FROM {{ params.table_name }}
    """
    ```

3. The Snowflake operator also allows you to pass in a `.sql` file directly. Create a file called `delete_table.sql` in the `include/sql` directory. Copy and paste the following SQL code:

    ```sql
    DROP TABLE IF EXISTS {{ params.table_name }};
    ```

:::tip

Whether you want to store your SQL code in individual SQL files or as strings in a Python module is a matter of personal preference. 

:::

## Step 4: Add a complex Snowflake DAG

1. Create a new file in your `dags` directory called `complex_snowflake_example.py`.

2. Copy and paste the code below into the new DAG file:

    ```python
    from airflow import DAG
    from airflow.models.baseoperator import chain
    from airflow.operators.empty import EmptyOperator
    from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator, SQLTableCheckOperator
    from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
    from pendulum import datetime
    from airflow.utils.task_group import TaskGroup
    import include.sql.tutorial_sql_statements as sql_stmts 

    SNOWFLAKE_FORESTFIRE_TABLE = "forestfires"
    SNOWFLAKE_COST_TABLE = "costs"
    SNOWFLAKE_FORESTFIRE_COST_TABLE = "forestfire_costs"

    SNOWFLAKE_CONN_ID = "snowflake_default"

    ROW_COUNT_CHECK = "COUNT(*) = 9"

    with DAG(
        "complex_snowflake_example",
        description="""
            Example DAG showcasing loading, transforming, 
            and data quality checking with multiple datasets in Snowflake.
        """,
        doc_md=__doc__,
        start_date=datetime(2022, 12, 1),
        schedule_interval=None,
        # defining the directory where SQL templates are stored
        template_searchpath="/usr/local/airflow/include/sql/",
        catchup=False
    ) as dag:
        """
        #### Snowflake table creation
        Create the tables to store sample data.
        """
        create_forestfire_table = SnowflakeOperator(
            task_id="create_forestfire_table",
            sql=sql_stmts.create_forestfire_table,
            params={"table_name": SNOWFLAKE_FORESTFIRE_TABLE}
        )

        create_cost_table = SnowflakeOperator(
            task_id="create_cost_table",
            sql=sql_stmts.create_cost_table,
            params={"table_name": SNOWFLAKE_COST_TABLE}
        )

        create_forestfire_cost_table = SnowflakeOperator(
            task_id="create_forestfire_cost_table",
            sql=sql_stmts.create_forestfire_cost_table,
            params={"table_name": SNOWFLAKE_FORESTFIRE_COST_TABLE}
        )

        """
        #### Insert data
        Insert data into the Snowflake tables using existing SQL queries
        stored in the include/sql/snowflake_examples/ directory.
        """
        load_forestfire_data = SnowflakeOperator(
            task_id="load_forestfire_data",
            sql=sql_stmts.load_forestfire_data,
            params={"table_name": SNOWFLAKE_FORESTFIRE_TABLE}
        )

        load_cost_data = SnowflakeOperator(
            task_id="load_cost_data",
            sql=sql_stmts.load_cost_data,
            params={"table_name": SNOWFLAKE_COST_TABLE}
        )

        load_forestfire_cost_data  = SnowflakeOperator(
            task_id="load_forestfire_cost_data",
            sql=sql_stmts.load_forestfire_cost_data,
            params={"table_name": SNOWFLAKE_FORESTFIRE_COST_TABLE}
        )

        """
        #### Transform
        Transform the forestfire_costs table to perform
        sample logic.
        """
        transform_forestfire_cost_table = SnowflakeOperator(
            task_id="transform_forestfire_cost_table",
            sql=sql_stmts.transform_forestfire_cost_table,
            params={"table_name": SNOWFLAKE_FORESTFIRE_COST_TABLE}
        )

        """
        #### Quality checks
        Perform data quality checks on the various tables.
        """
        with TaskGroup(
            group_id="quality_check_group_forestfire",
            default_args={
                "conn_id": SNOWFLAKE_CONN_ID,
            }
        ) as quality_check_group_forestfire:
            """
            #### Column-level data quality check
            Run data quality checks on columns of the forestfire table
            """
            forestfire_column_checks = SQLColumnCheckOperator(
                task_id="forestfire_column_checks",
                table=SNOWFLAKE_FORESTFIRE_TABLE,
                column_mapping={
                    "ID": {"null_check": {"equal_to": 0}},
                    "RH": {"max": {"leq_to": 100}}
                }
            )

            """
            #### Table-level data quality check
            Run data quality checks on the forestfire table
            """
            forestfire_table_checks = SQLTableCheckOperator(
                task_id="forestfire_table_checks",
                table=SNOWFLAKE_FORESTFIRE_TABLE,
                checks={"row_count_check": {"check_statement": ROW_COUNT_CHECK}}
            )

        with TaskGroup(
            group_id="quality_check_group_cost",
            default_args={
                "conn_id": SNOWFLAKE_CONN_ID,
            }
        ) as quality_check_group_cost:
            """
            #### Column-level data quality check
            Run data quality checks on columns of the forestfire table
            """
            cost_column_checks = SQLColumnCheckOperator(
                task_id="cost_column_checks",
                table=SNOWFLAKE_COST_TABLE,
                column_mapping={
                    "ID": {"null_check": {"equal_to": 0}},
                    "LAND_DAMAGE_COST": {"min": {"geq_to": 0}},
                    "PROPERTY_DAMAGE_COST": {"min": {"geq_to": 0}},
                    "LOST_PROFITS_COST": {"min": {"geq_to": 0}},
                }
            )

            """
            #### Table-level data quality check
            Run data quality checks on the forestfire table
            """
            cost_table_checks = SQLTableCheckOperator(
                task_id="cost_table_checks",
                table=SNOWFLAKE_COST_TABLE,
                checks={"row_count_check": {"check_statement": ROW_COUNT_CHECK}}
            )

        with TaskGroup(
            group_id="quality_check_group_forestfire_costs",
            default_args={
                "conn_id": SNOWFLAKE_CONN_ID,
            }
        ) as quality_check_group_forestfire_costs:
            """
            #### Column-level data quality check
            Run data quality checks on columns of the forestfire table
            """
            forestfire_costs_column_checks = SQLColumnCheckOperator(
                task_id="forestfire_costs_column_checks",
                table=SNOWFLAKE_FORESTFIRE_COST_TABLE,
                column_mapping={"AREA": {"min": {"geq_to": 0}}}
            )

            """
            #### Table-level data quality check
            Run data quality checks on the forestfire table
            """
            forestfire_costs_table_checks = SQLTableCheckOperator(
                task_id="forestfire_costs_table_checks",
                table=SNOWFLAKE_FORESTFIRE_COST_TABLE,
                checks={
                    "row_count_check": {"check_statement": ROW_COUNT_CHECK},
                    "total_cost_check": {"check_statement": "land_damage_cost + \
                        property_damage_cost + lost_profits_cost = total_cost"}
                }
            )

        """
        #### Delete tables
        Clean up the tables created for the example.
        """
        delete_forestfire_table = SnowflakeOperator(
            task_id="delete_forestfire_table",
            sql="delete_table.sql",
            params={"table_name": SNOWFLAKE_FORESTFIRE_TABLE}
        )

        delete_cost_table = SnowflakeOperator(
            task_id="delete_costs_table",
            sql="delete_table.sql",
            params={"table_name": SNOWFLAKE_COST_TABLE}
        )

        delete_forestfire_cost_table = SnowflakeOperator(
            task_id="delete_forestfire_cost_table",
            sql="delete_table.sql",
            params={"table_name": SNOWFLAKE_FORESTFIRE_COST_TABLE}
        )

        begin = EmptyOperator(task_id="begin")
        create_done = EmptyOperator(task_id="create_done")
        load_done = EmptyOperator(task_id="load_done")
        end = EmptyOperator(task_id="end")

        chain(
            begin,
            [create_forestfire_table, create_cost_table, create_forestfire_cost_table],
            create_done,
            [load_forestfire_data, load_cost_data],
            load_done,
            [quality_check_group_forestfire, quality_check_group_cost],
            load_forestfire_cost_data,
            quality_check_group_forestfire_costs,
            transform_forestfire_cost_table,
            [delete_forestfire_table, delete_cost_table, delete_forestfire_cost_table],
            end
        )
    ```

    This complex DAG has a write, audit publish pattern showcasing loading data into Snowflake and running [data quality](data-quality.md) checks on the data that has been written. 

    ![Complex Snowflake DAG](/img/guides/snowflake_complex_dag.png)

    The DAG accomplishes the following steps:

    - Creating three tables simultaneously using the [SnowflakeOperator](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator). 
    - Loading data into two of the tables that were created using the [SnowflakeOperatorAsync](https://registry.astronomer.io/providers/astronomer-providers/modules/snowflakeoperatorasync) a deferrable version of the SnowflakeOperator. In order to be able to use deferrable operators you need to have a triggerer component running in your Airflow environment, which is configured automatically if you are using the Astro CLI. Learn more about deferrable operators in our [Deferrable operators guide](deferrable-operators.md).
    - Running data quality checks on the data to ensure that no erroneous data is moved to production. These checks are structured with [task groups](task-groups.md) that include column checks using the `SQLColumnCheckOperator` and table checks using the `SQLTableCheckOperator`.
    - Copy data into the production table using the SnowflakeOperatorAsync.
    - Deleting the tables to clean up the example.

3. Run the DAG.

## Snowflake operators and providers

The following are some of the open source packages that you can use to orchestrate Snowflake in Airflow:

- The [Snowflake provider package](https://registry.astronomer.io/providers/snowflake) is maintained by the Airflow community and contains hooks, operators, and transfer operators for Snowflake.
- The [Astronomer Providers](https://github.com/astronomer/astronomer-providers) package contains deferrable operators built and maintained by Astronomer, including a deferrable version of the `SnowflakeOperator`.
- The [Common SQL provider package](https://registry.astronomer.io/providers/common-sql) contains SQL check operators that you can use to perform data quality checks against Snowflake data.

To leverage all of the available Snowflake modules, install all three packages in your Airflow environment. If you use the Astro CLI, add the following three lines to your Astro project `requirements.txt` file:

```bash
apache-airflow-providers-snowflake
apache-airflow-providers-common-sql
astronomer-providers[snowflake]
```

The following are the available modules for orchestrating basic queries and functions in Snowflake:

- [`SnowflakeOperator`](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator): Executes a SQL query in Snowflake. This operator is part of `apache-airflow-providers-snowflake`.
- [`S3ToSnowflakeOperator`](https://registry.astronomer.io/providers/snowflake/modules/s3tosnowflakeoperator): Executes a COPY command to transfer data from S3 into Snowflake.
- [`SnowflakeToSlackOperator`](https://registry.astronomer.io/providers/snowflake/modules/snowflaketoslackoperator): Executes a SQL query in Snowflake and sends the results to Slack.
- `SnowflakeOperatorAsync`: The [deferrable](deferrable-operators.md) version of the `SnowflakeOperator`, executes a SQL query in Snowflake.
- [`SnowflakeHook`](https://registry.astronomer.io/providers/snowflake/modules/snowflakehook): A hook abstracting the Snowflake API. Generally, you only need to use this hook when creating a custom operator or function. This hook is part of `apache-airflow-providers-snowflake`.
- `SnowflakeHookAsync`: The [deferrable](deferrable-operators.md) version of the `SnowflakeHook`, abstracts the Snowflake API.

The following are the available modules for orchestrating data quality checks in Snowflake:

- [`SQLColumnCheckOperator`](https://registry.astronomer.io/providers/common-sql/modules/sqlcolumncheckoperator): Performs a data quality check against columns of a given table. Using this operator with Snowflake requires a Snowflake connection ID, the name of the table to run checks on, and a `column_mapping` describing the relationship between columns and tests to run.
- [`SQLTableCheckOperator`](https://registry.astronomer.io/providers/common-sql/modules/sqltablecheckoperator): Performs a data quality check against a given table. Using this operator with Snowflake requires a Snowflake connection ID, the name of the table to run checks on, and a checks dictionary describing the relationship between the table and the tests to run.

Although the `apache-airflow-providers-snowflake` package contains operators that you can use to run data quality checks in Snowflake, Astronomer recommends that you use `apache-airflow-providers-common-sql` instead for its additional flexibility and community support. For more information about using the SQL check operators, see [Airflow Data Quality Checks with SQL Operators](airflow-sql-data-quality.md).


## Enhanced Observability with OpenLineage

The [OpenLineage project](https://openlineage.io/) integration with Airflow lets you obtain and view lineage data from your  Airflow tasks. As long as an extractor exists for the operator being used, lineage data is generated automatically from each task instance. For an overview of how OpenLineage works with Airflow, see [OpenLineage and Airflow](airflow-openlineage.md).

Because `SnowflakeOperator` and `SnowflakeOperatorAsync` have an extractor, you can use lineage metadata to answer the following questions across DAGs:

- How does data stored in Snowflake flow through my DAGs? Are there any upstream dependencies?
- What downstream data does a task failure impact?
- Where did a change in data format originate?

This image shows an overview of the interaction between OpenLineage, Airflow, and Snowflake:

![Snowflake Openlineage](/img/guides/snowflake_openlineage_architecture.png)

To view lineage data from your DAGs, you need to have OpenLineage installed in your Airflow environment and a lineage front end running. If you're using [Astro users](https://docs.astronomer.io/astro/data-lineage), lineage is enabled automatically. If you're using open source tools, you can run Marquez locally and connect it to your Airflow environment. See [OpenLineage and Airflow](airflow-openlineage.md).

To show an example of lineage resulting from Snowflake orchestration, you'll look at the write, audit, publish DAG from the previous example. The following image shows the Datakin UI integrated with Astro, but Marquez will show similar information.

![Lineage Graph](/img/guides/lineage_graph.png)

Looking at the lineage graph, you can see the flow of data from the creation of the table, to the insertion of data, to the data quality checks. If a failure occurs during the data quality checks or elsewhere, the lineage graph identifies the affected datasets. If your work on this dataset expanded into other DAGs in Airflow, you would see those connections here as well.

## DAG Authoring with the Astro Python SDK

The Astro Python SDK is an open source DAG authoring tool maintained by Astronomer that simplifies the data transformation process between different environments, so you can focus solely on writing execution logic without worrying about Airflow orchestration logic. Details such as creating dataframes, storing intermediate results, passing context and data between tasks, and creating Airflow task dependencies are all managed automatically.

The Astro Python SDK supports Snowflake as a data warehouse and can be used to simplify ETL workflows with Snowflake. For example, the following DAG moves data from Amazon S3 into Snowflake, performs some data transformations, and loads the resulting data into a reporting table.

```python
from pendulum import datetime

from airflow.models import DAG
from pandas import DataFrame

from astro import sql as aql
from astro.files import File
from astro.sql.table import Table

S3_FILE_PATH = "s3://<aws-bucket-name>"
S3_CONN_ID = "aws_default"
SNOWFLAKE_CONN_ID = "snowflake_default"
SNOWFLAKE_ORDERS = "orders_table"
SNOWFLAKE_FILTERED_ORDERS = "filtered_table"
SNOWFLAKE_JOINED = "joined_table"
SNOWFLAKE_CUSTOMERS = "customers_table"
SNOWFLAKE_REPORTING = "reporting_table"


@aql.transform
def filter_orders(input_table: Table):
    return "SELECT * FROM {{input_table}} WHERE amount > 150"


@aql.transform
def join_orders_customers(filtered_orders_table: Table, customers_table: Table):
    return """SELECT c.customer_id, customer_name, order_id, purchase_date, amount, type
    FROM {{filtered_orders_table}} f JOIN {{customers_table}} c
    ON f.customer_id = c.customer_id"""


@aql.dataframe
def transform_dataframe(df: DataFrame):
    purchase_dates = df.loc[:, "purchase_date"]
    print("purchase dates:", purchase_dates)
    return purchase_dates


with DAG(
    dag_id="astro_orders",
    start_date=datetime(2019, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Extract a file with a header from S3 into a Table object
    orders_data = aql.load_file(
        # data file needs to have a header row
        input_file=File(
            path=S3_FILE_PATH + "/orders_data_header.csv", conn_id=S3_CONN_ID
        ),
        output_table=Table(conn_id=SNOWFLAKE_CONN_ID),
    )

    # create a Table object for customer data in our Snowflake database
    customers_table = Table(
        name=SNOWFLAKE_CUSTOMERS,
        conn_id=SNOWFLAKE_CONN_ID,
    )

    # filter the orders data and then join with the customer table
    joined_data = join_orders_customers(filter_orders(orders_data), customers_table)

    # merge the joined data into our reporting table, based on the order_id .
    # If there's a conflict in the customer_id or customer_name then use the ones from
    # the joined data
    reporting_table = aql.merge(
        target_table=Table(
            name=SNOWFLAKE_REPORTING,
            conn_id=SNOWFLAKE_CONN_ID,
        ),
        source_table=joined_data,
        target_conflict_columns=["order_id"],
        columns=["customer_id", "customer_name"],
        if_conflicts="update",
    )

    purchase_dates = transform_dataframe(reporting_table)
```

Using Astro SDK `aql` functions, you are able to seamlessly transition between SQL transformations (`filter_orders` and `join_orders_customers`) to Python dataframe transformations (`transform_dataframe`). All intermediary data created by each task is automatically stored in Snowflake and made available to downstream tasks.

For more detailed instructions on running this example DAG, see [Astro SDK Getting Started](https://github.com/astronomer/astro-sdk/blob/main/docs/getting-started/GETTING_STARTED.md).

## Best practices and considerations

The following are some best practices and considerations to keep in mind when orchestrating Snowflake queries from Airflow:

-  To reduce costs and improve the scalability of your Airflow environment, use the deferrable version of operators.
- Set your default Snowflake query specifications such as Warehouse, Role, Schema, and so on in the Airflow connection. Then overwrite those parameters for specific tasks as necessary in your operator definitions. This is cleaner and easier to read than adding `USE Warehouse XYZ;` statements within your queries.
- Pay attention to which Snowflake compute resources your tasks are using, as overtaxing your assigned resources can cause slowdowns in your Airflow tasks. It is generally recommended to have different warehouses devoted to your different Airflow environments to ensure DAG development and testing does not interfere with DAGs running in production.
- Make use of [Snowflake stages](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html) when loading data from an external system using Airflow. Transfer operators such as the `S3ToSnowflake` operator require a Snowflake stage be set up. Stages generally make it much easier to repeatedly load data in a specific format.
