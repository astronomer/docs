---
sidebar_label: Pass data to cells
title: Pass data to Astro Cloud IDE cells
id: pass-data-to-cells
description: Learn how to run Python code by creating and configuring Python cells in the Astro Cloud IDE.
---

You can use the output of an Astro Cloud IDE cell as the input for another cell in your pipeline. When you pass data from one cell to another, you create a data dependency between those tasks. A cell that is downstream of a data dependency will not run until the upstream cell finishes and produces data. The Astro Cloud IDE automatically renders these dependencies in your project code and in the **Pipeline** view of your project.

Use this document to understand how to pass data to different types of Astro Cloud IDE cells.

## Pass data to Python cells

You can use the output of other cells in your project in a [Python cell](run-python.md) by passing the data to the cell. 

### Pass data from a Python cell to another Python cell 

Use the value of a Python cell's `return` statement in another Python cell by calling the name of the Python cell containing the `return` statement. Doing this automatically creates a dependency between the cells.

For example, consider two Python cells. One cell is named `hello_world` and includes the following code:

```sh
return "Hello, world!"
```

Another cell is named `data_dependency` and includes the following code:

```sh
my_string = hello_world
return my_string
```

The **Pipeline** view in the Cloud IDE shows the newly created dependency between these two cells. 

![New dependency graph](/img/cloud-ide/data-dependency.png)

### Pass data from a SQL cell to a Python cell 

Use the results of a SQL cell in your Python cell by calling the name of the SQL cell. The SQL cell must contain a `SELECT` statement. 

The table created by the `SELECT` statement is automatically converted to pandas DataFrame and passed to the Python cell.

The following Python cell is dependent on a SQL cell named `my_sql_cell`.

```python
df = my_sql_cell # my_sql_cell is a SQL cell which gets converted to a pandas DataFrame by default
df['col_a'] = df['col_a'] + 1
return df
```

## Pass data to SQL cells

You can use the output of other cells in your project within a [SQL cell](run-sql.md). You define these dependencies in SQL using jinja templating.

For example, if you have a SQL cell that uses **In-memory SQL** to query a dataframe output of a Python cell, the Python cell is automatically marked as an upstream dependency for your SQL cell.

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

## Pass external data to cells

There are currently two ways to use external data sources in your cells:

- Access the data through an API or Airflow connection.
- Include the data in your IDE project, deploy the project to GitHub, and [connect the repository to the Astro Cloud IDE](deploy-project.md#connect-your-repository). You can then load the data into your cell as you would from an Astro project. 

This applies to all cell types.