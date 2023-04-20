---
sidebar_label: Write SQL
title: Write SQL in the Astro Cloud IDE
id: run-sql
description: Learn how to run SQL queries by creating and configuring SQL cells in the Astro Cloud IDE.
---

A SQL cell contains a SQL query that you can run in isolation or as a dependency in your pipeline. Create SQL cells and Warehouse SQL cells to execute SQL as part of your data pipeline. 

## Prerequisites 

- An IDE project and pipeline. See [Step 2: Create a pipeline](/astro/cloud-ide/quickstart.md#step-2-create-a-pipeline).
- For Warehouse SQL cells, you need: 
    - A database connection. See [Configure Airflow connections](/astro/cloud-ide/configure-project-environment.md#configure-airflow-connections).
    - Write permissions to the data warehouse in your database connection. 

## Choose a SQL cell type

A SQL cell runs a SQL query against a database and, by default, stores the results of the query in an XCom value for use in other cells. A Warehouse SQL cell runs a SQL query against a database connection and stores the results in your data warehouse. For more information about how these cells work, see [How SQL cells work](#how-sql-cells-work).

The Astro Cloud IDE includes a local [DuckDB](https://duckdb.org/) instance that stores the XCom outputs for all Python and SQL cells without an external database storage connections. Through this instance, SQL cells can run queries against the dataframe or table outputs of other cells. 

Both cell types execute SQL queries, but there are some scenarios where the use of one cell type is preferable. The following table lists the scenarios where Astronomer recommends using a specific type of SQL cell.
  
| Scenario                                                                                            |     Cell type      |
| --------------------------------------------------------------------------------------------------- | :----------------: |
| I don't have write access to an external database.                                                  |      SQL cell      |
| I'm going to use the output of the query outside of my external database, such as in a Python cell. |      SQL cell      |
| I want to query a small amount of data from the output of another IDE cell.                         |      SQL cell      |
| I'm going to use the output of the query only in my external database.                              | Warehouse SQL cell |
| I'm querying a large amount of data.                                                                | Warehouse SQL cell |
  
Regardless of the cell type you choose, you can use your query results in downstream cells. However, using the output of a Warehouse cell in a downstream cell requires fetching the output from your external database, which can take longer than fetching the output of a SQL cell with XComs.

## Create a SQL cell

1. In the Cloud UI, select a Workspace and then select **Cloud IDE**.

2. Select a project.

3. On the **Pipelines** page click a pipeline name to open the pipeline editor.

4. Click **Add Cell** and select one of the following options:

    - **SQL**: Runs a SQL query against a provided database connection and stores the results of the query in an XCom for use in other cells.
    - **Warehouse SQL**: Runs a SQL query against a provided database connection and stores the results in your data warehouse.

5. Click the cell name and enter a name for the cell.

6. Add your SQL query to the cell body.

7. In the **Select Connection** list, select the connection for the database you want to query against. For SQL cells, select **In-memory SQL** if you want to query the output of another cell that was stored locally in XComs.

8. (Optional) If you're using Warehouse SQL cells, configure the following additional fields to define an output table. If you don't define these values, your data pipeline will store the outputs of your cell in a temporary table.

    - **Database**: The database for your output table
    - **Schema**:  The schema for your output table
    - **Table name**: The name of your output table

    By default, your input is formatted as a literal string and is defined in your DAG with quotation marks. To format your input as a Python expression, click **Python expression** next to the value name. If you already entered a literal string before changing this setting, remove the quotation marks that the IDE adds to your Python expression.
    
    After you switch to **Python expression**, your input for the value is defined in the DAG as a Python expression without quotation marks. You can use your input to call any Python value in your pipeline, such as a global import, an Airflow variable, or an environment variable. 

## Run a SQL cell

See [Run cells in the Astro Cloud IDE](run-cells.md).

## Create explicit dependencies for a SQL cell

In your SQL cell, click **Dependencies** and select a cell to be upstream of your SQL cell. When you run your entire pipeline, the SQL cell cannot begin running until the selected upstream cell finishes running.

![Button for specifying an explicit dependency](/img/cloud-ide/create-dependency.png)

To make your SQL cell an upstream dependency for another cell, click **Dependencies** for the other cell and select the name of your SQL cell. 

## Create data dependencies for a SQL cell

You can use the output of other cells in your project within a SQL function. You define these dependencies in SQL, and the Cloud IDE automatically renders the dependencies in your project code and in the **Pipeline** view of your project.

### Pass a value from a Python cell to a SQL cell 

If a Python cell returns a pandas DataFrame, you can pass the DataFrame to a SQL cell as a table by calling the name of the Python cell. Call the name of the Python cell using double curly braces, also known as jinja templating. Pandas DataFrames are automatically converted to SQL tables when they are passed to SQL cells.

For example, a SQL cell containing the following query is dependent on a Python cell named `my_dataframe`.

```sql
select * from {{my_dataframe}} -- my_dataframe is a Python cell
where col_a > 10
```

### Pass a value from a SQL cell to a SQL cell 

You can pass the results of a `SELECT` statement to a SQL cell by calling the name of the SQL cell containing the `SELECT` statement. Call the name of the SQL cell using double curly braces, also known as jinja templating.

For example, a SQL cell containing the following query is dependent on a SQL cell named `my_table`.

```sql
select * from {{my_table}} -- my_table is another SQL cell
```

## View complete code for SQL cells

To view your SQL cell within the context of an Airflow DAG, click **Code**. The Airflow DAG includes your SQL query as well as all of the code required to run it on Airflow.

## How SQL cells work

SQL cells use the Astro SDK to execute your queries. A standard SQL cell executes your query using `aql.run_raw_sql` and stores the results in XComs. A Warehouse SQL cell runs your SQL query using `aql.transform` and loads the results in your data warehouse. See [Astro SDK documentation](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/raw_sql.html) for more information about these operators.
