---
sidebar_label: Configure your project environment
title: Configure your Astro Cloud IDE project environment
id: configure-project-environment
description: Learn how to configure environment variables, connections, and dependencies for use in your Astro cloud IDE pipelines.
---

Configure your Astro Cloud IDE project environment, including Airflow dependencies, variables, and connections, in the Cloud UI. You can use your environment configurations in any pipeline within your project.

Environment configuration in the Astro Cloud IDE is similar to Astro project and Airflow configuration, but more options are provided to minimize the time you spend configuring text files. 

## Limitations

- You can't set OS-level dependencies with the Astro Cloud IDE.
- Only a subset of Airflow connections can be configured through Astro Cloud IDE templates. All other connections must be configured through a generic connection template.
- Environment configurations are not saved when you export a data pipeline as a DAG. To run your data pipeline outside of the Astro Cloud IDE, you must reconfigure these values in the Airflow environment where you exported your data pipeline.

## Add Python package requirements

Setting Python package requirements in the Astro Cloud IDE is equivalent to setting them in the Astro project `requirements.txt` file or running `pip install <package>`.

1. In the Cloud UI, select a Workspace and then select **Cloud IDE**.

2. Select a project.

3. Click **Requirements**, then click **+ Requirement** to add a new requirement.
   
4. Enter a Python package name, and then select a package version. 

5. Click **Add**.

The package requirement appears in the **Requirements** list. To edit the Python package dependency, click **Edit** in the **Requirements** list.

## Configure environment variables

The process for configuring environment variables in the Astro Cloud IDE and in Deployments is similar, and Astro Cloud IDE environment variables are stored and retrieved in the same way as Deployment environment variables. See [How environment variables are stored on Astro](environment-variables.md#how-environment-variables-are-stored-in-the-cloud-ui).

In the Astro Cloud IDE, you can additionally specify whether an environment variable should be used as an Airflow variable or a system level environment variable.

1. In the Cloud UI, select a Workspace and then select **Cloud IDE**.

2. Select a project.

3. Click the **Variables** tab, and then click **Variable**.

4. Complete the following fields:

    - **Type**: Select the purpose of the environment variable. 

        - Select **Environment** if you want to configure a system-level environment variable for your runtime environment, such as `AIRFLOW__CORE__DEFAULT_TASK_EXECUTION_TIMEOUT`. 
        - Select **Airflow** if you want to call the variable value in a Python, SQL, or Warehouse SQL cell. Unlike in open source Airflow, do not specify your environment variable key with `AIRFLOW_VAR_`. 
  
    - **Key**: They key for your environment variable.
    - **Value**: The value for your environment variable.

5. Optional. Check **Mask Value** to make the variable value secret.

6. Click **Create Variable**.

The environment variable appears in the **Variables** list. To edit the environment variable, click **Edit** in the **Variables** list.

### Call Airflow variables in cells 

Call Airflow variable values in Python cells using `Variable.get('<variable-key>')`. For example:

```python
value = Variable.get('MY_KEY')
print(value)
```

Call Airflow variables in SQL or Warehouse SQL cells using jinja templating. For example, if your environment variable value is the name of a column in `mytable`, you could run:

```sql
SELECT {{ var.value.MY_KEY }} FROM mytable;
```

## Configure Airflow connections

You can configure Airflow connections in the Astro Cloud IDE in the same way that you can in the [Airflow UI](https://docs.astronomer.io/learn/connections). You can then reference the connection in your Python cells as code or in SQL cells as a configuration.

1. In the Cloud UI, select a Workspace and then select **Cloud IDE**.

2. Select a project.

3. Click the **Connections** tab, and then click **Connection**.

4. Select a connection type.

5. Configure the connection. 
   
6. Optional. Click **Test connection** to check that you configured the connection correctly. Note that you cannot test generic connections.

7. Click **Create Connection**.

The connection appears in the **Connections** list. To edit the connection, click **Edit** in the **Connections** list.

### Use connections in cells

To use a connection in a Python cell, pass the connection ID to any function that accepts an Airflow connection as an argument, such as a [hook](https://docs.astronomer.io/learn/what-is-a-hook).

To use a connection in a SQL or Warehouse SQL cell:

1. In the Cloud UI, select a Workspace and then select **Cloud IDE**.

2. Select a project.

3. Click the **Pipelines** tab, and then click a pipeline name to open the pipeline editor.

4. In a SQL or Warehouse SQL cell, click **Select connection** and select the connection you want to use to store the results of the cell. If you are configuring a Warehouse SQL cell, additionally configure the **Output Table** where you want to permanently store the results of the cell query. 

5. Optional. Call a table from your database in your SQL query. For example:

```sql
SELECT * FROM table_name;
```

## View environment configurations from the pipeline editor

Environment configurations apply to all pipelines in a project. To view your configurations in the pipeline editor, click **Environment**. The **Use in your pipeline** pane shows all configurations that apply to your current pipeline. You can add, delete, or modify environment configurations in the pane.

:::info

Environment configurations exist at the project level. Modifying them in your pipeline editor updates the configurations for all pipelines in your project. To run a data pipeline with different environment configurations from its existing IDE project, you must recreate it in a new IDE project. 

:::
