---
title: "Orchestrate Snowflake Queries with Airflow"
description: "Get enhanced observability and compute savings while orchestrating Snowflake jobs from your Airflow DAGs."
id: airflow-snowflake
sidebar_label: Snowflake
---

[Snowflake](https://www.snowflake.com/) is one of the most commonly used data warehouses. Orchestrating Snowflake queries as part of a data pipeline is one of the most common Airflow use cases. Using Airflow with Snowflake is straightforward, and there are multiple open source packages, tools, and integrations that can help you realize the full potential of your existing Snowflake instance.

This tutorial covers an example of orchestrating complex Snowflake operations with Airflow, including:

- Creating tables.
- Loading data into Snowflake.
- Running transformations on data in Snowflake using Airflow operators. 
- Running data quality checks on data in Snowflake. 

Additionally, [More on the Airflow Snowflake integration](#more-on-the-airflow-snowflake-integration) offers further information on:

- Available operators and hooks for orchestrating actions in Snowflake.
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
- A Snowflake account. A [30-day free trial](https://signup.snowflake.com/) is available. You need to have at least one schema in one database available for which you have permissions to create and write to tables.

## Step 1: Configure your Astro project

Use the Astro CLI to create and run an Airflow project on your local machine.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-snowflake-tutorial && cd astro-snowflake-tutorial
    $ astro dev init
    ```


2. Run the following command to start your Airflow project:

    ```sh
    $ astro dev start
    ```

## Step 2: Configure a Snowflake connection

1. In the Airflow UI, go to **Admin** -> **Connections** and click **+**. 

2. Create a new connection named `snowflake_default` and choose the `Snowflake` connection type. Enter the following information:

    - [Schema](https://docs.snowflake.com/en/sql-reference/sql/create-schema.html): Your Snowflake schema. 
    - Login: Your Snowflake login username.
    - Password: Your Snowflake password.
    - Account: Your Snowflake account in the format `xy12345`.
    - [Database](https://docs.snowflake.com/en/sql-reference/sql/create-database.html): Your Snowflake database.
    - Region: Your Snowflake region, for example `us-east-1`.

    Your connection should look something like the screenshot below.

    ![Snowflake connection](/img/guides/snowflake_tutorial_connection.png)

## Step 3: Add your SQL statements

The DAG you will create in Step 4 runs multiple SQL statements against your Snowflake data warehouse. While it is possible to add SQL statements directly in your DAG file it is common practice to store them in separate files. When initializing your Astro project with the Astro CLI, an `include` folder was created. The contents of this folder will automatically be mounted into the Dockerfile, which makes it the standard location in which supporting files are stored.

1. Create a folder called `sql` in your `include` folder.

2. Create a new file in `include/sql` called `tutorial_sql_statements.py` and copy the following code:

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
        INSERT INTO forestfire_costs (
                id, land_damage_cost, property_damage_cost, lost_profits_cost,
                total_cost, y, month, day, area
            )
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

    This file contains 7 SQL statements, each of which you can run individually from your DAG.

3. The Snowflake operator also accepts a direct `.sql` file for execution. Create a file in your `include/sql` folder called `delete_table.sql` and add the following SQL code to it:

    ```sql
    DROP TABLE IF EXISTS {{ params.table_name }};
    ```

    This file highlights how you can parameterize your SQL queries to pass information in at runtime.

:::tip

When running SQL statements from Airflow operators, you can store the SQL code in individual SQL files, in a combined SQL file, or as strings in a Python module. Astronomer recommends storing lengthy SQL statements in a dedicated file to keep your DAG files clean and readable.

:::

## Step 4: Write a Snowflake DAG

1. Create a new file in your `dags` directory called `complex_snowflake_example.py`.

2. Copy and paste the code below into the file:

    ```python
    from airflow import DAG
    from airflow.models.baseoperator import chain
    from airflow.operators.empty import EmptyOperator
    from airflow.providers.common.sql.operators.sql import (
        SQLColumnCheckOperator, SQLTableCheckOperator
    )
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
        schedule=None,
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

    This complex DAG implements a write, audit, publish pattern showcasing loading data into Snowflake and running [data quality](data-quality.md) checks on the data that has been written. 

    ![Complex Snowflake DAG](/img/guides/snowflake_complex_dag.png)

    The DAG completes the following steps:

    - Creates three tables simultaneously using the [SnowflakeOperator](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator). 
    - Loads data into two of the tables that were created.
    - Runs data quality checks on the data to ensure that no erroneous data is moved to production. These checks are structured with [task groups](task-groups.md) that include column checks using the [SQLColumnCheckOperator](https://registry.astronomer.io/providers/common-sql/modules/sqlcolumncheckoperator) and table checks using the [SQLTableCheckOperator](https://registry.astronomer.io/providers/common-sql/modules/sqltablecheckoperator). The task group structure logically groups tasks which simplifies setting dependencies and collapses a set of tasks visually in the Airflow UI. 
    - Copies data into the production table.
    - Deletes the tables to clean up the example.

    The `chain()` method at the end of the DAG sets the dependencies. This method is commonly used over bitshift operators (`>>`) to make it easier to read dependencies between many tasks.

## Step 5: Run the DAG and review data quality results

1. In the Airflow UI, click the play button to manually run your DAG.

2. Navigate to the `Grid` view of the `complex_snowflake_example` DAG and click on the `quality_check_group_forestfire_costs` task group to expand it. You should see two tasks which ran data quality checks on the `forestfire_costs` table. Click on the `forestfire_costs_column_checks` task to view the successful checks in the task's logs.

    ![Forestfire quality checks logs](/img/guides/snowflake_forestfire_quality_checks_logs.png)

## Step 6: Use deferrable operators

The `complex_snowflake_example` DAG runs several queries against the same Snowflake database in parallel. While some queries, like the ones creating tables, run quickly, larger transformation or loading queries might take longer to complete. These queries are a great use case for the deferrable version of the SnowflakeOperator, the [SnowflakeOperatorAsync](https://registry.astronomer.io/providers/astronomer-providers/modules/snowflakeoperatorasync). Deferrable operators use the triggerer component in your Airflow environment, which is configured automatically with the Astro CLI, to release their worker slot while they wait for the task to be completed. This allows you to use your Airflow resources much more efficiently in production. Learn more about deferrable operators in our [Deferrable operators guide](deferrable-operators.md).

Using deferrable operators from the [Astronomer providers package](https://registry.astronomer.io/providers/astronomer-providers) is easy, you simply have to switch out the operator class. All parameters stay the same.

1. Add the following statement to your DAG to import the SnowflakeOperatorAsync:

    ```python
    from astronomer.providers.snowflake.operators.snowflake import (
        SnowflakeOperatorAsync
    )
    ```

2. Switch out the operators used in the `load_forestfire_data` and `load_cost_data` tasks by replacing `SnowflakeOperator` with `SnowflakeOperatorAsync`:

    ```python
    load_forestfire_data = SnowflakeOperatorAsync(  # changed operator name
        task_id="load_forestfire_data",
        sql=sql_stmts.load_forestfire_data,
        params={"table_name": SNOWFLAKE_FORESTFIRE_TABLE}
    )

    load_cost_data = SnowflakeOperatorAsync( # changed operator name
        task_id="load_cost_data",
        sql=sql_stmts.load_cost_data,
        params={"table_name": SNOWFLAKE_COST_TABLE}
    )
    ```

3. Run your DAG and observe how the two load tasks go into a deferred state (purple border) before being completed.

     ![Load tasks deferred state](/img/guides/snowflake_example_deferred_state.png)

## More on the Airflow Snowflake integration

This section provides additional information on orchestrating actions in Snowflake with Airflow.

### Snowflake Operators and Hooks

Several open source packages contain operators used to orchestrate Snowflake in Airflow. If you are using the Astro CLI these packages will all be pre-installed in your project.

The [Snowflake provider package](https://registry.astronomer.io/providers/snowflake) contains:

- [SnowflakeOperator](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator): Executes any SQL query in Snowflake.
- [S3ToSnowflakeOperator](https://registry.astronomer.io/providers/snowflake/modules/s3tosnowflakeoperator): Executes an COPY command to load files from s3 to Snowflake.
- [SnowflakeToSlackOperator](https://registry.astronomer.io/providers/snowflake/modules/snowflaketoslackoperator): An operator that executes a SQL statement in Snowflake and sends the result to Slack.
- [SnowflakeHook](https://registry.astronomer.io/providers/snowflake/modules/snowflakehook): A client to interact with Snowflake which is commonly used when building custom operators interacting with Snowflake.

The [Common SQL provider package](https://registry.astronomer.io/providers/common-sql) contains [SQL check operators](airflow-sql-data-quality.md) that you can use to perform data quality checks against Snowflake data, namely the:

- [SQLColumnCheckOperator](https://registry.astronomer.io/providers/common-sql/modules/sqlcolumncheckoperator): Performs a data quality check against columns of a given table.
- [SQLTableCheckOperator](https://registry.astronomer.io/providers/common-sql/modules/sqltablecheckoperator): Performs a data quality check against a given table.

The [Astronomer Providers](https://github.com/astronomer/astronomer-providers) package contains deferrable modules built and maintained by Astronomer, including the [SnowflakeOperatorAsync](https://registry.astronomer.io/providers/astronomer-providers/modules/snowflakeoperatorasync) and the [SnowflakeHookAsync](https://registry.astronomer.io/providers/astronomer-providers/modules/snowflakehookasync).

### Snowflake and enhanced observability with OpenLineage

The [OpenLineage project](https://openlineage.io/) integration with Airflow lets you obtain and view lineage data from your Airflow tasks. As long as an extractor exists for the operator being used, lineage data is generated automatically from each task instance. For an overview of how OpenLineage works with Airflow, see [OpenLineage and Airflow](airflow-openlineage.md).

The SnowflakeOperator, SnowflakeOperatorAsync, SQLColumnCheckOperator and SQLTableCheckOperator all have an extractor, which allows you to use lineage metadata to answer the following questions across DAGs:

- How does data stored in Snowflake flow through my DAGs? Are there any upstream dependencies?
- What downstream data does a task failure impact?
- Where did a change in data format originate?
- Where were data quality checks performed and what was their result?

This image shows an overview of the interaction between OpenLineage, Airflow, and Snowflake:

![Snowflake OpenLineage](/img/guides/snowflake_openlineage_architecture.png)

To view lineage data from your DAGs, you need to have OpenLineage installed in your Airflow environment and a lineage front end running. If you're using [Astro](https://docs.astronomer.io/astro/data-lineage), lineage is enabled automatically. If you're using open source tools, you can run Marquez locally and connect it to your Airflow environment. See [OpenLineage and Airflow](airflow-openlineage.md).

To show an example of lineage resulting from Snowflake orchestration, you'll look at the write, audit, publish DAG from the previous example. The following image shows the Lineage UI integrated with Astro.

![Lineage Graph](/img/guides/lineage_complex_snowflake_example.png)

Looking at the lineage graph, you can see the flow of data from the creation of the table, to the insertion of data, to the data quality checks. If a failure occurs during the data quality checks or elsewhere, the lineage graph identifies the affected datasets. If your work on this dataset expanded into other DAGs in Airflow, you would see those connections here as well.

### Snowflake and the Astro Python SDK

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

For more detailed instructions on running this example DAG, see the [Write a DAG with the Astro Python SDK](astro-python-sdk.md) tutorial.

### Best practices and considerations

The following are some best practices and considerations to keep in mind when orchestrating Snowflake queries from Airflow:

-  To reduce costs and improve the scalability of your Airflow environment, use the deferrable version of operators.
- Set your default Snowflake query specifications such as Warehouse, Role, Schema, and so on in the Airflow connection. Then overwrite those parameters for specific tasks as necessary in your operator definitions. This is cleaner and easier to read than adding `USE Warehouse XYZ;` statements within your queries.
- Pay attention to which Snowflake compute resources your tasks are using, as overtaxing your assigned resources can cause slowdowns in your Airflow tasks. It is generally recommended to have different warehouses devoted to your different Airflow environments to ensure DAG development and testing does not interfere with DAGs running in production.
- Make use of [Snowflake stages](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html) when loading data from an external system using Airflow. Transfer operators such as the `S3ToSnowflake` operator require a Snowflake stage be set up. Stages generally make it much easier to repeatedly load data in a specific format.

## Conclusion

Congratulations! You've run a complex DAG performing a common orchestration pattern on data in your Snowflake data warehouse.
