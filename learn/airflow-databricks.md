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

Astronomer has many customers who use Databricks to run jobs as part of complex pipelines. This can easily be accomplished by leveraging the [Databricks provider](https://registry.astronomer.io/providers/databricks), which includes Airflow hooks and operators that are actively maintained by the Databricks and Airflow communities. In this guide, you'll learn about the hooks and operators available for interacting with Databricks clusters and run jobs, and how to use both available operators in an Airflow DAG.

:::info

All code in this guide can be found on [the Astronomer Registry](https://legacy.registry.astronomer.io/dags/databricks-tutorial).

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
- Access to a Databricks workspace. See [Databricks' documentation](https://docs.databricks.com/getting-started/index.html) for instructions. You can use any workspace that has access to the [Databricks workflows](https://docs.databricks.com/workflows/index.html) feature with a user having permissions to create notebooks and Databricks jobs. You can use any underlying cloud service and a [14-day free trial](https://www.databricks.com/try-databricks) is available.
- Access to an [object storage supported by the Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/supported_file.html). This tutorial uses an [AWS S3](https://aws.amazon.com/s3/) bucket, if you are using a different object storage you will need to make changes to the Databricks notebook code and the DAG code that is shown.
- Access to a [relational database supported by the Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/supported_databases.html). This tutorial uses [PostgreSQL](https://www.postgresql.org/).

## Step 1: Configure your Astro project

An Astro project contains all of the files you need to run Airflow locally.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-databricks-tutorial && cd astro-databricks-tutorial
    $ astro dev init
    ```

2. Add the [Astro Databricks provider package](https://github.com/astronomer/astro-provider-databricks) and the [Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/index.html), as well as the plotting libraries [seaborn](https://seaborn.pydata.org/) and [matplotlib](https://matplotlib.org/) to your Astro project `requirements.txt` file. This tutorial uses the Astro Python SDK to load and analyze data transformed using a Databricks workflow and seaborn together with matplotlib to produce a graph.

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

## Step 3: Prepare your Object storage

In you object storage solution create a new bucket. This tutorial uses AWS S3 and a bucket named `databricks-tutorial-bucket`. 

## Step 4: Create Databricks Notebooks

In this tutorial you will orchestrate a Databricks job that sequentially runs two notebooks. 

1. [Create an empty notebook](https://docs.databricks.com/notebooks/notebooks-manage.html) in your Databricks workspace called `join_data`. 

2. Copy and paste the following code into the `join_data` notebook. You can divide the code into cells as you see fit. Make sure to replace the `ACCESS_KEY` and `SECRET_KEY` variables with your respective credentials, see the Databricks documentation for recommended ways to securely [manage Secrets](https://docs.databricks.com/security/secrets/index.html) in Databricks. If you are using a different object storage than AWS S3 you will need to replace the code wrapped in `# --------- AWS S3 specific -------- #` comments with code connecting to your object storage.

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

If a connection type isn't available, you might need to make it available by adding the [relevant provider package](https://registry.astronomer.io/) to `requirements.txt` and running `astro dev restart`.

:::

## Step 6: Write your Airflow DAG

The DAG you'll write uses the Astro Databricks provider to create a Databricks workflow from Airflow tasks referencing the Databricks notebooks you prepared in [Step 4](#step-4-create-databricks-notebooks).

1. In your `dags` folder, create a file called `renewable_analysis_dag`.

2. Copy and paste the following DAG code into the file:

    <CodeBlock language="python">{databricks_tutorial_dag}</CodeBlock>

    This DAG consists of seven tasks and one task group:

    - The `in_tables` task uses the [`LoadFileOperator`](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/load_file.html) of the Astro Python SDK in order to load CSV files from the local `include` directory to the relational database. This task is [dynamically mapped](dynamic-tasks.md), creating one mapped task instance for each file.
    - The `select_countries` task uses the [`aql.transform`](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/transform.html) decorator from the Astro Python SDK to run a SQL query, selecting the relevant rows for `COUNTRY` from each of the temporary tables created by the previous task. The result is stored in another temporary table.
    - The `save_files_to_S3` task dynamically maps over the country subsets created by the previous task and creates one CSV file per table in your S3 bucket via the [ExportToFileOperator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/export.html). This task uses the `.map` function, a utility function that can transform XComArg objects, learn more [here](dynamic-tasks.md#transform-outputs-with-map).

    - The `databricks_workflow` task group, created using the `DatabricksWorkflowTaskGroup` class, contains two tasks using the `DatabricksNotebookOperator`. 
        - The task group provisions a Databricks `job_cluster` with the spec defined as `job_cluster_spec` and creates the Databricks job from the tasks within the task group. Creation of this cluster and job runs as the automatically generated `launch` task.
        - The `join_data` task runs the `join_data` notebook in this cluster as the first part of the Databricks job. In this notebook the information from the three input CSVs is joined in one file, using Spark.
        - The `transform_data` task runs the `transform_data` notebook as the second part of the Databricks job. This notebook creates a new column in the data called `"SHW%"` which contains the sum of the percentage of solar, wind and hydro in your country's electricity supply.

    - The `delete_intake_files_S3` task deletes all files from the `country_subset` folder in S3.
    - The `load_file` task retrieves the CSV file that the `transform_data` Databricks notebook wrote to S3 and saves the contents in a temporary table in your relational database.
    - Finally, the `create_graph` task uses the `@aql.dataframe` decorator of the Astro Python SDK to create a graph of the `"SHW%"` column. The graph is saved as a `.png` file in the `include` directory.

3. Run the DAG manually by clicking the play button and view the DAG in the graph view. Double click the task group in order to expand it and see all tasks.  

    ![Astro Databricks DAG graph view](/img/guides/astro_databricks_provider_dag_graph.png)
    
4. Open the `shw.png` file in your `include` folder to see your graph.

    ![SWH graph Switzerland](/img/guides/databricks_tutorial_shw_graph.png)

:::info

If you are using a different object storage you will need to make changes to the DAG code above, namely the `OBJECT_STORAGE_CONN_ID` as well as the operator used in the `delete_intake_files_S3` task. To find relevant operators for your object storage see the [Astronomer registry](https://registry.astronomer.io/).

:::



## Alternative ways to run Databricks with Airflow

### Databricks hooks and operators

The Databricks provider package includes many hooks and operators that allow users to accomplish most common Databricks-related use cases without writing a ton of code.

:::info

In Airflow 2.0, provider packages are separate from the core of Airflow. If you are running 2.0, you may need to install the `apache-airflow-providers-databricks` provider package to use the hooks, operators, and connections described here. In an Astronomer project this can be accomplished by adding the packages to your `requirements.txt` file. To learn more, see [Provider Packages](https://airflow.apache.org/docs/apache-airflow-providers/index.html).

:::

### Hooks

Using the [Databricks hook](https://registry.astronomer.io/providers/databricks/modules/databrickshook) is the best way to interact with a Databricks cluster or job from Airflow. The hook has methods to submit and run jobs to the Databricks REST API, which are used by the operators described below. There are also additional methods users can leverage to:

- Get information about runs or jobs
- Cancel, start, or terminate a cluster
- Install and uninstall libraries on a cluster

### Operators

There are currently two operators in the Databricks provider package:

- The `DatabricksSubmitRunOperator` makes use of the Databricks [Runs Submit API Endpoint](https://docs.databricks.com/dev-tools/api/latest/jobs.html#runs-submit) and submits a new Spark job run to Databricks.
- The `DatabricksRunNowOperator` makes use of the Databricks [Run Now API Endpoint](https://docs.databricks.com/dev-tools/api/latest/jobs.html#run-now) and runs an existing Spark job.

The `DatabricksRunNowOperator` should be used when you have an existing job defined in your Databricks workspace that you want to trigger using Airflow. The `DatabricksSubmitRunOperator` should be used if you want to manage the definition of your Databricks job and its cluster configuration within Airflow. Both operators allow you to run the job on a Databricks General Purpose cluster you've already created or on a separate Job Cluster that is created for the job and terminated upon the job’s completion.

Documentation for both operators can be found on the [Astronomer Registry](https://registry.astronomer.io/providers/databricks?type=operators).

### Example - Using Airflow with Databricks

You'll now learn how to write a DAG that makes use of both the `DatabricksSubmitRunOperator` and the `DatabricksRunNowOperator`. Before diving into the DAG itself, you need to set up your environment to run Databricks jobs.

#### Create a Databricks connection

In order to use any Databricks hooks or operators, you first need to create an Airflow connection that allows Airflow to talk to your Databricks account. In general, Databricks recommends using a personal access token (PAT) to authenticate to the Databricks REST API. For more information on how to generate a PAT for your account, read the [Managing dependencies in data pipelines](https://docs.databricks.com/dev-tools/data-pipelines.html).

For this example, you'll use the PAT authentication method and set up a connection using the Airflow UI. It should look something like this:

![Databricks Connection](/img/guides/databricks_connection.png)

The **Host** should be your Databricks workspace URL, and your PAT should be added as a JSON block in **Extra**.

Note that it is also possible to use your login credentials to authenticate, although this isn't Databricks' recommended method of authentication. To use this method, you would enter the username and password you use to sign in to your Databricks account in the Login and Password fields of the connection.

#### Create a Databricks job

In order to use the `DatabricksRunNowOperator` you must have a job already defined in your Databricks workspace. If you are new to creating jobs on Databricks, [this guide](https://docs.databricks.com/jobs.html) walks through all the basics.

To follow the example DAG below, you will want to create a job that has a cluster attached and a parameterized notebook as a task. For more information on parameterizing a notebook, see [this page](https://docs.databricks.com/notebooks/widgets.html).

Once you create a job, you should be able to see it in the Databricks UI Jobs tab:

![Databricks Job](/img/guides/databricks_job.png)

#### Define the DAG

Now that you have a Databricks job and Airflow connection set up, you can define your DAG to orchestrate a couple of Spark jobs. This example makes use of both operators, each of which are running a notebook in Databricks.

```python
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator, DatabricksRunNowOperator
from datetime import datetime, timedelta

#Define params for Submit Run Operator
new_cluster = {
    'spark_version': '7.3.x-scala2.12',
    'num_workers': 2,
    'node_type_id': 'i3.xlarge',
}

notebook_task = {
    'notebook_path': '/Users/kenten+001@astronomer.io/Quickstart_Notebook',
}

#Define params for Run Now Operator
notebook_params = {
    "Variable":5
}

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

with DAG('databricks_dag',
    start_date=datetime(2021, 1, 1),
    schedule='@daily',
    catchup=False,
    default_args=default_args
    ) as dag:

    opr_submit_run = DatabricksSubmitRunOperator(
        task_id='submit_run',
        databricks_conn_id='databricks',
        new_cluster=new_cluster,
        notebook_task=notebook_task
    )
    opr_run_now = DatabricksRunNowOperator(
        task_id='run_now',
        databricks_conn_id='databricks',
        job_id=5,
        notebook_params=notebook_params
    )

    opr_submit_run >> opr_run_now
```

For both operators you need to provide the `databricks_conn_id` and necessary parameters.

For the `DatabricksSubmitRunOperator`, you need to provide parameters for the cluster that will be spun up (`new_cluster`). This should include, at a minimum:

- Spark version
- Number of workers
- Node type ID

These can be defined more granularly as needed. For more information on what Spark version runtimes are available, see the [Databricks REST API documentation](https://docs.databricks.com/dev-tools/api/latest/index.html#runtime-version-strings).

You also need to provide the task that will be run. In this example you use the `notebook_task`, which is the path to the Databricks notebook you want to run. This could also be a Spark JAR task, Spark Python task, or Spark submit task, which would be defined using the `spark_jar_task`, `spark_python_test`, or `spark_submit_task` parameters respectively. The operator will look for one of these four options to be defined.

For the `DatabricksRunNowOperator`, you only need to provide the `job_id` for the job you want to submit, since the job parameters should already be configured in Databricks. You can find the `job_id` on the **Jobs** tab of your Databricks account. However, you can also provide `notebook_params`, `python_params`, or `spark_submit_params` as needed for your job. In this case, you parameterized your notebook to take in a `Variable` integer parameter and passed in '5' for this example.

#### Error handling

When using either of these operators, any failures in submitting the job, starting or accessing the cluster, or connecting with the Databricks API will propagate to a failure of the Airflow task and generate an error message in the logs.

If there is a failure in the job itself, like in one of the notebooks in this example, that failure will also propagate to a failure of the Airflow task. In that case, the error message may not be shown in the Airflow logs, but the logs should include a URL link to the Databricks job status which will include errors, print statements, etc. For example, if you set up the notebook in Job ID 5 in the example above to have a bug in it, you get a failure in the task causing the Airflow task log to look something like this:

![Error Log Example](/img/guides/databricks_failure_airflow_log.png)

In the case above, you can click on the URL link to get to the Databricks log in order to debug the issue.

### Next steps

This example DAG shows how little code is required to get started orchestrating Databricks jobs with Airflow. By using existing hooks and operators, you can easily manage your Databricks jobs from one place while also building your data pipelines. With just a few more tasks, you can turn the DAG above into a pipeline for orchestrating many different systems:

![Pipeline Example](/img/guides/pipeline_example_w_databricks.png)
