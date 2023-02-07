---
sidebar_label: Write SQL
title: Write SQL in the Astro Cloud IDE
id: run-sql
description: Learn how to run SQL queries by creating and configuring SQL cells in the Astro Cloud IDE.
---

A SQL cell contains a SQL query that you can run in isolation or as a dependency in your pipeline. Create SQL cells to execute SQL as part of your data pipeline. 

## Prerequisites 

- An IDE project and pipeline. See [Step 2: Create a pipeline](/astro/cloud-ide/quickstart.md#step-2-create-a-pipeline).
- A database connection. See [Step 5: Create a database connection](/astro/cloud-ide/quickstart.md#step-5-create-a-database-connection).
- For Warehouse SQL cells, you need write permissions to the data warehouse in your database connection. 

## Create a SQL cell

1. In the Cloud UI, select a Workspace and then select **Cloud IDE**.

2. Select a project.

3. On the **Pipelines** page click a pipeline name to open the pipeline editor.

4. Click **Add Cell** and select one of the following options:

    - **SQL**: Runs a SQL query against a provided database connection and persists the results of the query in an XCom for use by other cells.

    - **Warehouse SQL**: Runs a SQL query against a provided database connection and stores the results in your data warehouse.

    Regardless of which cell type you choose, you can use the results of your queries in downstream SQL and Python cells.

5. Click the cell name and enter a name for the cell.

6. Add your SQL query to the cell body.

7. In the **Select Connection** list, select the connection for the database you want to query against.

8. If you're using Warehouse SQL cells, configure the **Output Table** for storing the results of your query. This table must be accessible from your configured connection.

## Run a SQL cell

See [Run cells in the Astro Cloud IDE](run-cells.md).

## Create explicit dependencies for a SQL cell

In your SQL cell, click **Dependencies** and select a cell to be upstream of your SQL cell. When you run your entire pipeline, the SQL cell cannot begin running until the selected upstream cell finishes running.

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

SQL cells use the Astro SDK to execute your queries. A standard SQL cell executes your query using `aql.run_raw_sql` and stores the results in XComs. A Warehouse SQL cell runs your SQL query using `aql.transform` and loads the results in your data warehouse. See [Astro SDK documentation](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/raw_sql.html).