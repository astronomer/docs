---
sidebar_label: Configure your project environment
title: Configure your Astro Cloud IDE project environment
id: configure-project-environment
description: Learn how to configure environment variables, connections, and dependencies for use in your Astro cloud IDE pipelines.
---

Configure your Astro Cloud IDE project environment, including Airflow dependencies, variables, and connections, directly in the cloud UI. You can use your environment configurations in any pipeline within your project.

Environment configuration in the Astro Cloud IDE is similar Astro project and Airflow configuration, but includes more options for specifying values that minimize the time you spend configuring through text files. 

## Limitations

- You can't currently set OS-level dependencies through the Astro Cloud IDE.
- Only a subset of Airflow connections can be configured from the Astro Cloud IDE.
- Airflow connections configured through the Astro Cloud IDE can be used only to configure external databases for SQL and Warehouse SQL cells.
- Environment configurations are not saved when you export a data pipeline as a DAG. To run your data pipeline outside of the Astro Cloud IDE, you must reconfigure these values in the Airflow environment where you exported your data pipeline.

## Add Python package requirements

Setting Python package requirements in the Astro Cloud IDE is equivalent to setting them in the Astro project `requirements.txt` file or running `pip install <package>`.

1. In the Cloud UI, select a Workspace and then select Cloud IDE.

2. Select a project.

3. Click **Requirements**, then click **+ Requirement** to add a new requirement.
   
4. Enter the name and version for the Python package. 

5. Click **Add**.

The package requirement appears in the **Requirements** table. To edit the Python package dependency, click **Edit** in the **Requirements** table.

## Configure environment variables

You can configure environment variables in the Astro Cloud IDE in the same way that you can for Astro Deployments. Similarly, Astro Cloud IDE environment variables are stored and retrieved in the same way as Deployment environment variables. See [How environment variables are stored on Astro](environment-variables.md#how-environment-variables-are-stored-on-astro).

Additionally, the Astro Cloud IDE lets you specify whether an environment variable should be used as either an Airflow variable or a system level environment variable.

1. In the Cloud UI, select a Workspace and then select Cloud IDE.

2. Select a project.

3. Click **Variables**, then click **+ Variable** to add a new environment variable.

4. Configure the following values:

    - **Type**: Select the purpose of the environment variable. Select **Environment** if you want to configure a system-level environment variable for your runtime environment, such as `AIRFLOW__CORE__DEFAULT_TASK_EXECUTION_TIMEOUT`. Select **Airflow** if you want to call the variable key from a Python cell using `Variable.get('<variable-name>')`. If you select **Airflow**, do not specify your environment variable key with `AIRFLOW_VAR_`. 
    - **Key**: They key for your environment variable.
    - **Value**: The value for your environment variable.

5. Optional. Check **Mask Value** to make the variable value secret.

6. Click **Create Variable**.

The environment variable appears in the **Variables** table. To edit the environment variable, click **Edit** in the **Variables** table.

## Configure Airflow connections

You can configure Airflow connections in the Astro Cloud IDE in the same way that you can in the [Airflow UI](https://docs.astronomer.io/learn/connections). You can then reference the connection in your Python cells as code or in SQL cells as a configuration

1. In the Cloud UI, select a Workspace and then select Cloud IDE.

2. Select a project.

3. Click **Connections**, then click **+ Connection** to add a new environment variable.

4. Choose a connection type.

5. Configure the connection. 
   
6. Optional. Click **Test connection** to check that the you correctly configured the connection. 

7. Click **Create Connection**.

The connection appears in the **Connections** table. To edit the connection, click **Edit** in the **Connections** table.

### Use connections in SQL cells

Currently, Airflow connections configured through the Astro Cloud IDE can be used only to configure external databases for SQL and Warehouse SQL cells. To specify a connection in one of these cell types:

1. In the Cloud UI, select a Workspace and then select **Cloud IDE**.

2. Select a project.

3. On the **Pipelines** page click a pipeline name to open the pipeline editor.

4. In a SQL or Warehouse SQL cell, click **Select connection** and select the connection you want to use to store the results of the cell. If you are configuring a Warehouse SQL cell, additionally configure the **Output Table** where you want to permanently store the results of the cell query. 

You can then use jinja templating to call your configured database connection from your SQL cell queries. For example:

```sql
SELECT * FROM {{<connection-id>}};
```

## View environment configurations from the pipeline editor

Environment configurations apply to all pipelines in a given project. To view your configurations from the pipeline editor, click **Environment**. The **Use in your pipeline…** menu shows all configurations which apply to your current pipeline. You can also use this menu to add, delete, or modify environment configurations.

:::info

Because environment configurations exist at the project level, modifying them from your pipeline editor will update the configurations for all pipelines in your project. To run a data pipeline with different environment configurations from its existing IDE project, you must recreate it in a new IDE project. 

:::