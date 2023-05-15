---
title: "Orchestrate Databricks jobs with Airflow"
sidebar_label: "Databricks"
description: "Orchestrate Databricks jobs with your Airflow DAGs."
id: airflow-databricks
tags: [Integrations, DAGs]
sidebar_custom_props: { icon: 'img/integrations/databricks.png' }
---

import CodeBlock from '@theme/CodeBlock';
import databricks_tutorial_dag from '!!raw-loader!../code-samples/dags/airflow-databricks/databricks_tutorial_dag.py';

[Databricks](https://databricks.com/) is a popular unified data and analytics platform built around [Apache Spark](https://spark.apache.org/) that provides users with fully managed Apache Spark clusters and interactive workspaces. Astronomer recommends using Airflow primarily as an orchestrator, and to use an execution framework like Apache Spark to do the heavy lifting of data processing. It follows that using Airflow to orchestrate Databricks jobs is a natural solution for many common use cases.

The easiest way to orchestrate your Databricks notebooks from Airflow and execute them as Databricks Workflows is to use the open source [Astro Databricks provider](https://github.com/astronomer/astro-provider-databricks) which provides full observability and control from Airflow so you can manage your Workflows from one place.

For orchestration of actions in Databricks outside of Databricks Workflows, the [Databricks provider](https://registry.astronomer.io/providers/databricks) created and maintained by the Airflow community is available. You can find information on the community-managed Databricks provider in the [Alternative ways to run Databricks with Airflow](#alternative-ways-to-run-databricks-with-airflow) section.

In this tutorial you will learn how to use the Astro Databricks provider with an example use case analyzing renewable energy data.

:::info

All code in this tutorial can be found on [the Astronomer Registry] (INSERT REGISTRY LINK LATER).

:::

## Time to complete

This tutorial takes approximately 1 hour to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Databricks. See [Getting started with Databricks](https://www.databricks.com/learn).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- Access to a Databricks workspace. See [Databricks' documentation](https://docs.databricks.com/getting-started/index.html) for instructions. You can use any workspace that has access to the [Databricks Workflows](https://docs.databricks.com/workflows/index.html) feature. You will need a user with permissions to create notebooks and Databricks jobs. You can use any underlying cloud service, and a [14-day free trial](https://www.databricks.com/try-databricks) is available.
- Access to an [object storage supported by the Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/supported_file.html). This tutorial uses an [AWS S3](https://aws.amazon.com/s3/) bucket.
- Access to a [relational database supported by the Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/supported_databases.html). This tutorial uses [PostgreSQL](https://www.postgresql.org/).

## Step 1: Configure your Astro project

An Astro project contains all of the files you need to run Airflow locally.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-databricks-tutorial && cd astro-databricks-tutorial
    $ astro dev init
    ```

2. Add the following packages to your `requirements.txt` file. The [Astro Databricks provider package](https://github.com/astronomer/astro-provider-databricks) and the [Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/index.html) are used to load, transform, and analyze, the data. [seaborn](https://seaborn.pydata.org/) and [matplotlib](https://matplotlib.org/) are used to plot the results.

    ```text
    astro-provider-databricks==0.1.3
    astro-sdk-python==1.6.0
    seaborn==0.12.2
    matplotlib==3.7.1
    ```

3. Define the following environment variables in the `.env` file in order to be able to serialize Astro Python SDK and Astro Databricks provider objects:

    ```text
    AIRFLOW__CORE__ALLOWED_DESERIALIZATION_CLASSES = airflow\.* astro\.* astro_databricks\.*
    ```

## Step 2: Prepare the data

This tutorial uses an Airflow DAG to orchestrate a Databricks job that joins datasets about shares of renewable electricity sources in different years for a selected country and calculates the percentage of electricity coming from solar, wind and hydro power.

1. [Download the CSV files](https://github.com/astronomer/learn-tutorials-data/tree/main/databricks-tutorial) from GitHub.
2. Save the downloaded CSV files in the `include` directory of your Astro project.

This tutorial uses parts of a dataset from a [Kaggle](https://www.kaggle.com/datasets/programmerrdai/renewable-energy) about renewable energy derived from [Our World in Data](https://ourworldindata.org/renewable-energy) (License [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).

## Step 3: Prepare your object storage

Create a new bucket named `databricks-tutorial-bucket` in your object storage solution. In this tutorial we use AWS S3, but you can use any solution that is supported by the Astro SDK.

## Step 4: Create Databricks Notebooks

In this tutorial you will orchestrate a Databricks job that sequentially runs two notebooks. 

1. [Create an empty notebook](https://docs.databricks.com/notebooks/notebooks-manage.html) in your Databricks workspace called `join_data`. 

2. Copy and paste the following code into the `join_data` notebook. You can divide the code into cells as you see fit. Make sure to replace the `ACCESS_KEY` and `SECRET_KEY` variables with your respective credentials. If you are using a different object storage than AWS S3 you will need to replace the code wrapped in `# --------- AWS S3 specific -------- #` comments with code connecting to your object storage.

    ```python
    # package imports
    import csv

    # --------- AWS S3 specific --------- #
    import boto3
    # --------- /AWS S3 specific -------- #

    import pandas as pd
    from io import StringIO
    from pyspark.sql.types import (
        StructType,
        StructField,
        StringType,
        IntegerType,
    )

    # set variables
    ACCESS_KEY = "<your AWS Access Key ID>"  # dbutils.secrets.get(scope="my-scope", key="my-aws-key-key")
    SECRET_KEY = "<your AWS Secret Access Key>"  # dbutils.secrets.get(scope="my-scope", key="my-aws-secret-key")
    BUCKET_NAME = "databricks-tutorial-bucket"
    S3_FOLDER_COUNTRY_SUBSET = "country_subset"
    S3_FOLDER_JOINED_DATA = "joined_data"

    # --------- AWS S3 specific -------- #
    # list files in the `country_subset` directory of your S3 bucket
    s3 = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{S3_FOLDER_COUNTRY_SUBSET}/")
    csv_files = [obj["Key"] for obj in objects["Contents"] if obj["Key"].endswith(".csv")]
    # --------- /AWS S3 specific ------- #

    # load data from CSVs in the `country_subset` folder into separate Spark dataframes
    dfs = []
    for file in csv_files:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=file)
        body = obj["Body"].read().decode("utf-8")
        csv_reader = csv.reader(StringIO(body), delimiter=",", quotechar='"')
        header = next(csv_reader)
        schema = StructType([StructField(col, StringType(), True) for col in header])
        df = spark.createDataFrame(csv_reader, schema)
        dfs.append(df)

    # collect name of the country assessed
    entity_name = dfs[0].select("Entity").distinct().collect()[0]["Entity"]

    # define results table
    schema = StructType(
        [
            StructField("Year", IntegerType(), True),
        ]
    )
    result_df = spark.createDataFrame([], schema)

    # join data tables to result table
    for df in dfs:
        col_name = df.columns[3]

        df = df.select("Year", col_name)
        result_df = result_df.join(df, "Year", "outer")

    # convert spark dataframe to pandas and remove potentially duplicated columns
    pandas_df = result_df.toPandas()
    df_t = pandas_df.T
    df_t = df_t.loc[~df_t.index.duplicated(keep="first")]
    df_clean = df_t.T
    csv_buffer = StringIO()
    df_clean.to_csv(csv_buffer, index=False)

    # --------- AWS S3 specific --------- #
    # upload data as a CSV file to S3
    s3 = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    s3.put_object(
        Body=csv_buffer.getvalue(),
        Bucket=BUCKET_NAME,
        Key=f"{S3_FOLDER_JOINED_DATA}/{entity_name}.csv",
    )
    # --------- /AWS S3 specific -------- #
    ```

3. Create a second empty notebook in your Databricks workspace called `transform_data`.

4. Copy and paste the following code into the `transform_data` notebook. You can divide the code into cells as you see fit. Make sure to replace the `ACCESS_KEY` and `SECRET_KEY` variables with your respective credentials, see the Databricks documentation for recommended ways to securely [manage Secrets](https://docs.databricks.com/security/secrets/index.html) in Databricks. If you are using a different object storage than AWS S3 you will need to replace the code wrapped in `# --------- AWS S3 specific -------- #` comments with code connecting to your object storage.

    ```python
    import csv

    # --------- AWS S3 specific --------- #
    import boto3
    # --------- /AWS S3 specific -------- #

    from io import StringIO
    from pyspark.sql.functions import col
    from pyspark.sql.types import StructType, StructField, StringType

    # set variables
    ACCESS_KEY = "<your AWS Access Key ID>"  # dbutils.secrets.get(scope="my-scope", key="my-aws-key-key")
    SECRET_KEY = "<your AWS Secret Access Key>"  # dbutils.secrets.get(scope="my-scope", key="my-aws-secret-key")
    BUCKET_NAME = "databricks-tutorial-bucket"
    S3_FOLDER_JOINED_DATA = "joined_data"
    S3_FOLDER_TRANSFORMED_DATA = "transformed_data"

    # --------- AWS S3 specific -------- #
    # list files in the `joined_data` directory of your S3 bucket
    s3 = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{S3_FOLDER_JOINED_DATA}/")
    csv_files = [obj["Key"] for obj in objects["Contents"] if obj["Key"].endswith(".csv")]
    # --------- /AWS S3 specific -------- #

    # load data from CSVs in the `joined_data` folder into separate Spark dataframes
    dfs = []
    for file in csv_files:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=file)
        body = obj["Body"].read().decode("utf-8")
        csv_reader = csv.reader(StringIO(body), delimiter=",", quotechar='"')
        header = next(csv_reader)
        schema = StructType([StructField(col, StringType(), True) for col in header])
        df = spark.createDataFrame(csv_reader, schema)
        dfs.append(df)

    # calculate summation column for each Spark dataframe
    dfs_transformed = []
    for df in dfs:
        df = df.withColumn(
            "SHW%",
            col("Solar (% electricity)")
            + col("Hydro (% electricity)")
            + col("Wind (% electricity)"),
        )
        dfs_transformed.append(df)

    # convert each spark dataframe into pandas and load to S3
    for file_name, df in zip(csv_files, dfs_transformed):
        # Convert Spark DataFrame to Pandas DataFrame and write to in memory CSV file
        pandas_df = df.toPandas()
        csv_buffer = StringIO()
        pandas_df.to_csv(csv_buffer, index=False)

        # --------- AWS S3 specific --------- #
        # upload data to S3
        s3 = boto3.client(
            "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
        )
        s3.put_object(
            Body=csv_buffer.getvalue(),
            Bucket=BUCKET_NAME,
            Key=f"{S3_FOLDER_TRANSFORMED_DATA}/{file_name.split('/')[1]}",
        )
        # --------- /AWS S3 specific -------- #

    ```

:::info

Please note that while you can provide your credentials to AWS in plain text to the notebook code above, this is highly discouraged, especially in a production environment. Databricks offers the possiblility to [configure S3 access with instance profiles](https://docs.databricks.com/aws/iam/instance-profile-tutorial.html) and [secure handling of secrets](https://docs.databricks.com/security/secrets/index.html).

:::

## Step 5: Configure connections

This tutorial uses three data tools external to Airflow: Databricks, Amazon S3 (or another object storage) and a PostgreSQL database (or another relational database). You will create an Airflow connection to each of these tools.

1. Start Airflow by running `astro dev start`.

2. In the Airflow UI, go to **Admin** -> **Connections** and click **+**. 

3. Create a new connection named `databricks_conn`. Select the connection type `Databricks` and enter the following information:

    - **Connection ID**: `databricks_conn`.
    - **Connection Type**: `Databricks`.
    - **Host**: Your Databricks host address (format: `https://dbc-1234cb56-d7c8.cloud.databricks.com/`).
    - **Login**: Your Databricks login username (email).
    - **Password**: Your [Databricks personal access token](https://docs.databricks.com/dev-tools/auth.html#databricks-personal-access-tokens).

4. Create a new connection named `aws_conn`. Make sure the credentials you add have permission to read and write from your S3 bucket. If you are using a different object storage you will need to adjust this step to connect to your tooling.

    - **Connection ID**: `aws_conn`.
    - **Connection Type**: `Amazon Web Services`.
    - **AWS Access Key ID**: Your [AWS Access Key ID](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html). 
    - **AWS Secret Access Key**: Your AWS Secret Access Key.

5. Create a new connection named `db_conn`. Select the connection type and supplied parameters based on the data warehouse you are using. For a Postgres connection, enter the following information:

    - **Connection ID**: `db_conn`.
    - **Connection Type**: `Postgres`.
    - **Host**: Your Postgres host address.
    - **Schema**: Your Postgres database. 
    - **Login**: Your Postgres login username.
    - **Password**: Your Postgres password.
    - **Port**: Your Postgres port.

:::info

If the right connection type isn't available, you might need to add the [relevant provider package](https://registry.astronomer.io/) to `requirements.txt` and run `astro dev restart`.

:::

## Step 6: Write your Airflow DAG

The DAG you'll write uses the Astro Databricks provider to create a Databricks Workflow from Airflow tasks referencing the Databricks notebooks you prepared in [Step 4](#step-4-create-databricks-notebooks).

1. In your `dags` folder, create a file called `renewable_analysis_dag.py`.

2. Copy and paste the following DAG code into the file:

    <CodeBlock language="python">{databricks_tutorial_dag}</CodeBlock>

    This DAG consists of seven tasks and one task group:

    - The `in_tables` task uses the [`LoadFileOperator`](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/load_file.html) of the Astro Python SDK in order to load CSV files from the local `include` directory to the relational database. This task is [dynamically mapped](dynamic-tasks.md), creating one mapped task instance for each file.
    - The `select_countries` task uses the [`aql.transform`](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/transform.html) decorator from the Astro Python SDK to run a SQL query, selecting the relevant rows for `COUNTRY` from each of the temporary tables created by the previous task. The result is stored in another temporary table.
    - The `save_files_to_S3` task dynamically maps over the country subsets created by the previous task and creates one CSV file per table in your S3 bucket via the [ExportToFileOperator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/export.html). This task uses the `.map` function, a utility function that can transform XComArg objects, learn more [here](dynamic-tasks.md#transform-outputs-with-map).

    - The `databricks_workflow` task group, created using the `DatabricksWorkflowTaskGroup` class, contains two tasks using the `DatabricksNotebookOperator`. This task group automatically creates a Databricks Workflow executing the Databricks notebooks specified in the individual DatabricksNotebookOperators. One of the biggest benefits of this setup is the use of a Databricks job cluster instead of other cluster types, allowing you to [significantly reduce your Databricks cost](https://www.databricks.com/product/pricing). In this tutorial example the tasks within the task group will be the following:
        - The task group provisions a Databricks `job_cluster` with the spec defined as `job_cluster_spec` and creates the Databricks job from the tasks within the task group. Creation of this cluster and job runs as the automatically generated `launch` task.
        - The `join_data` task runs the `join_data` notebook in this cluster as the first part of the Databricks job. In this notebook the information from the three input CSVs is joined in one file, using Spark.
        - The `transform_data` task runs the `transform_data` notebook as the second part of the Databricks job. This notebook creates a new column in the data called `"SHW%"` which contains the sum of the percentage of solar, wind and hydro in your country's electricity supply.

    - The `delete_intake_files_S3` task deletes all files from the `country_subset` folder in S3.
    - The `load_file` task retrieves the CSV file that the `transform_data` Databricks notebook wrote to S3 and saves the contents in a temporary table in your relational database.
    - Tthe `create_graph` task uses the `@aql.dataframe` decorator of the Astro Python SDK to create a graph of the `"SHW%"` column. The graph is saved as a `.png` file in the `include` directory.
    - Finally, the `cleanup` task using the [`aql.cleanup`](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/cleanup.html) operator of the Astro Python SDK runs in parallel with the whole DAG, cleaning up any temporary tables created by the Astro Python SDK when they are not needed anymore.

3. Run the DAG manually by clicking the play button and view the DAG in the graph view. Double click the task group in order to expand it and see all tasks.  

    ![Astro Databricks DAG graph view](/img/guides/astro_databricks_provider_dag_graph.png)
    
4. Open the `shw.png` file in your `include` folder to see your graph.

    ![SWH graph Switzerland](/img/guides/databricks_tutorial_shw_graph.png)

:::info

If you are using a different object storage you will need to make changes to the DAG code above, namely the `OBJECT_STORAGE_CONN_ID` as well as the operator used in the `delete_intake_files_S3` task. To find relevant operators for your object storage see the [Astronomer registry](https://registry.astronomer.io/).

:::

## How it works

This section will explain Astro Databricks provider functionality in more depth. You can learn more about the Astro Databricks provider in the [provider documentation](https://astronomer.github.io/astro-provider-databricks/).

### Defining params

The DatabricksWorkflowTaskGroup provides configuration options via several parameters:

- `job_clusters`: the job clusters to be used in this Workflow. You can provide the full `job_cluster_spec` as shown in the tutorial DAG.
- `notebook_params`: a dictionary of parameters to make available to all notebook tasks in a Workflow.
- `notebook_packages`: a list of dictionaries defining Python packages to be installed in all notebook tasks in a Workflow.
- `extra_job_params`: a dictionary with properties to override the default Databricks Workflow job definitions.

You also have the ability to specifiy parameters at the task level in the DatabricksNotebookOperator:

- `notebook_params`: a dictionary of parameters to make available to the notebook.
- `notebook_packages`: a list of dictionaries defining Python packages to be installed in the notebook.

Note that you cannot specifiy the same packages in the `notebook_packages` parameter of a DatabricksWorkflowTaskGroup and in the `notebook_packages` parameter of a task using the DatabricksNotebookOperator in that same task group. Duplicate entries in this parameter will cause an error within Databricks.

### Repairing a Databricks Workflow

The Astro Databricks provider includes the possibility to repair a failed Databricks Workflow by making a repair request to the [Databricks Jobs API](https://docs.databricks.com/api-explorer/workspace/jobs/repairrun). Databricks expects a single repair request for all tasks that need to be rerun in one cluster, this can be achieved via the Airflow UI by using the operator extra link **Repair All Failed Tasks**.

![Repair All Failed Tasks OEL](/img/guides/repair_all_failed_databricks_tasks_oel.png)

If you only want to rerun specific tasks within your Workflow you can use the **Repair a single failed task** operator extra link on an individual task in the Databricks Workflow.

![Repair a single failed task OEL](/img/guides/repair_single_failed_databricks_task_oel.png)

## Alternative ways to run Databricks with Airflow

The Astro Databricks provider is under active development and support for more Databricks task types is still being added. If you want to perform an action in your Databricks environment that is not yet supported by the Astro Databricks provider such as [updating a Databricks repository](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest/modules/DatabricksReposUpdateOperator) you will often find relevant operators in the [community-managed Databricks provider](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest). 

Additionally, the community-managed Databricks provider contains hooks (for example the [DatabricksHook](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest/modules/DatabricksHook)) that simplify interaction with Databricks, including writing your own [custom Databricks operators](airflow-importing-custom-hooks-operators.md#create-a-custom-operator).

You can find several example DAGs using the community-managed Databricks provider on the [Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest).
