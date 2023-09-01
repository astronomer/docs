---
sidebar_label: Pass data to cells
title: Pass data to Astro Cloud IDE cells
id: pass-data-between-cells
description: Learn how to run Python code by creating and configuring Python cells in the Astro Cloud IDE.
---

You can use the output of an Astro Cloud IDE cell as the input for another cell in your pipeline. When you pass data from one cell to another, you create a _data dependency_ which defines the order in which the cells must be executed. A cell that is downstream of a data dependency will not run until the upstream cell finishes and produces data. The Astro Cloud IDE automatically renders these dependencies in your project code and orders them in the **Pipeline** view of your project.

Use this document to understand how to pass data to different types of Astro Cloud IDE cells.

## Pass data to a Python cell

To use the output of a Python or SQL cell in a [Python cell](run-python.md), reference the upstream cell's name in the body of the downstream Python cell. Doing this automatically creates a dependency between the cells.

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

This works similarly with SQL cells. When you reference the name of a SQL cell in a Python cell, the table created by your SQL cell's `SELECT` statement is automatically converted to a pandas DataFrame and passed to the Python cell. Note that the SQL cell you reference must contain a `SELECT` statement. 

The following Python cell is dependent on a SQL cell named `my_sql_cell`.

```python
df = my_sql_cell # my_sql_cell is a SQL cell which gets converted to a pandas DataFrame by default
df['col_a'] = df['col_a'] + 1
return df
```

## Pass data to a SQL cell

To use the output of a Python or SQL cell in a SQL cell, reference the name of the upstream cell in curly braces in the body of the downstream SQL cell. Note that: 

- You can pass data from a Python cell to a SQL cell only if the Python cell returns a pandas DataFrame.
- You can only pass data from a SQL cell to another SQL cell only if the upstream SQL cell has a `SELECT` statement. 

For example, a SQL cell containing the following query is dependent on a SQL cell named `my_table`.

```sql
select * from {{my_table}} -- my_table is another SQL cell
```

Similarly, the following SQL cell is dependent on a Python cell named `my_dataframe`.

```sql
select * from {{my_dataframe}} -- my_dataframe is a Python cell
where col_a > 10
```

## Pass external data to cells

There are currently two ways to use external data sources in your cells:

- Access the data through an API or Airflow connection.
- Include the data in your IDE project, deploy the project to GitHub, and [connect the repository to the Astro Cloud IDE](deploy-project.md#connect-your-repository). You can then load the data into your cell as you would from an Astro project. 

This applies to all cell types.