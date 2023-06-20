---
title: "ELT pipelines with Airflow, Databricks, the Astro Databricks provider, and the Astro Python SDK"
description: "Use Airflow, Databricks and the Astro Python SDK in an ELT pipeline to analyze energy data."
id: use-case-airflow-databricks
sidebar_label: "ELT with Airflow + Databricks + Astro SDK"
sidebar_custom_props: { icon: 'img/integrations/databricks.png' }
---

[Databricks](https://databricks.com/) is a popular unified data and analytics platform built around fully managed Apache Spark clusters. With the [Astro Databricks provider](https://github.com/astronomer/astro-provider-databricks) provider package you can create a Databricks Workflow from existing Databricks notebooks as a task group in your Airflow DAG, allowing you to use Airflow's orchestration capabilities in combination with Databricks' cheapest compute. See also [Why use Airflow with Databricks](airflow-databricks.md#why-use-airflow-with-databricks). The open-source [Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/index.html) greatly simplifies common ELT tasks like loading data and allows users to easily use Pandas on data stored in a data warehouse. 

This example shows a DAG that extracts data from three local CSV files containing the share of solar, hydro and wind electricity in different countries over several years, runs a transformation on each file and loads the results to S3, using [dynamic task mapping](dynamic-tasks.md) over operators from the [Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/index.html). Transformation steps in Databricks are fully integrated into the DAG as a task group via the Astro Databricks provider and filter and aggregate the data to get a combined measure of solar, hydro and wind electricity share for a user-selected country. Lastly, a task created with the `@aql.dataframe` decorator from the Astro Python SDK leverages [seaborn](https://seaborn.pydata.org/) and [matplotlib](https://matplotlib.org/) to create a line chart of the aggregated data.

![DAG graph screenshot](/img/examples/use-case-airflow-databricks_dag_graph_full.png)

After the DAG in this project runs, a graph appears in the `include` directory which shows the combined percentage of solar, hydro and wind energy in a country you selected.

![SHW graph](/img/examples/use-case-airflow-databricks_shw_graph.png)

:::info

For more detailed instructions on using Databricks with the Astro Databricks provider, see the [Databricks tutorial](airflow-databricks.md).
:::

## Before you start

Before trying this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- [Docker Desktop](https://www.docker.com/products/docker-desktop).
- Access to a Databricks workspace. See [Databricks' documentation](https://docs.databricks.com/getting-started/index.html) for instructions. You can use any workspace that has access to the [Databricks Workflows](https://docs.databricks.com/workflows/index.html) feature. You need a user account with permissions to create notebooks and Databricks jobs. You can use any underlying cloud service, and a [14-day free trial](https://www.databricks.com/try-databricks) is available.
- Access to an [object storage supported by the Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/supported_file.html). This tutorial uses an [AWS S3](https://aws.amazon.com/s3/) bucket.
- Access to a [relational database supported by the Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/supported_databases.html). This tutorial uses [PostgreSQL](https://www.postgresql.org/).

## Clone the project

Clone the example project from this [Astronomer GitHub](https://github.com/astronomer/learn-airflow-databricks-tutorial). Make sure to create a file called `.env` with the contents of the `.env_example` file in the project root directory and replace the connection details with your own. You will also need to replace the `DATABRICKS_LOGIN_EMAIL`, `S3_BUCKET` and `AWS_REGION` variables with your own values at the start of the DAG code. Change the `COUNTRY` to analyze a different country (for available countries, refer to the source data in the `include` folder).

## Run the project

To run the example project, first make sure Docker Desktop is running. Then, navigate to your project directory and run:

```sh
astro dev start
```

This command builds your project and spins up 4 Docker containers on your machine to run it. After the command finishes, open the Airflow UI at `https://localhost:8080/` and trigger the `renewable_analysis_dag` DAG using the play button.

## Project contents

### Data source

This example analyzes the share of solar, wind and hydro electricity for different countries. The full source data including other electricity modalities can be found in this [Kaggle dataset](https://www.kaggle.com/datasets/programmerrdai/renewable-energy) derived from [Our World in Data](https://ourworldindata.org/renewable-energy) (License [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).

The subset of data used in this example can be found in the include folder of the accompanying [GitHub repository](https://github.com/astronomer/learn-airflow-databricks-tutorial/tree/main/include).

### Project code

This project consists of one DAG, [renewable_analysis_dag](https://github.com/astronomer/learn-airflow-databricks-tutorial/blob/main/dags/renewable_analysis_dag.py), which performs an ELT process using the Astro Python SDK and a task group created through the Astro Databricks provider that orchestrates two Databricks notebooks in a Databricks Workflow.

First, all three separate CSV files, each containing the energy percentages for a list of countries for solar, hydro and wind power respectively are loaded into a new temporary table in the data warehouse using the [Astro Python SDK `load file` operator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/load_file.html). The operator uses [dynamic task mapping](dynamic-tasks.md) to create a mapped task instance for each file provided to the `input_file` parameter of the `.expand` method, which are then executed in parallel.

```python
in_tables = aql.LoadFileOperator.partial(
    task_id="in_tables",
    output_table=Table(
        conn_id=DB_CONN_ID,
    ),
).expand(
    input_file=[
        File(path=SOLAR_CSV_PATH),
        File(path=HYDRO_CSV_PATH),
        File(path=WIND_CSV_PATH),
    ]
)
```

Next, the `select_countries` task uses the [Astro Python SDK `@aql.transform` decorator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/transform.html) to execute a SQL query on each of the three temporary tables created in the `in_tables` task to select only rows for the specified `COUNTRY` and save the results in three new temporary tables. Again, dynamic task mapping is used to execute the SQL queries in parallel on each of the tables contained in the [XCom](airflow-passing-data-between-tasks.md#xcom) output of the previous task (`in_tables.output` provided to `in_table` in `.expand`) in their own dynamically mapped task instances.

```python
@aql.transform
def select_countries(in_table, country):
    return """SELECT * FROM {{ in_table }} WHERE "Entity" = {{ country }};"""

### [...]

country_tables = select_countries.partial(country=COUNTRY).expand(
    in_table=in_tables.output
)
```

The third task is defined with the [Astro Python SDK ExportToFileOperator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/export.html) to export the data from the three temporary tables created in the `select_countries` task to an object storage. Dynamic task mapping for this task is achieved using the [`.expand_kwargs` method](dynamic-tasks.md#sets-of-keyword-arguments) since the `input_data` and `output_file` parameter will vary together. The [`.map` method](dynamic-tasks.md#transform-outputs-with-map) is used to modify the output of the upstream task to a list of dictionaries containing the `input_data` and `output_file` parameters for each task instance.

```python
save_files_to_S3 = aql.ExportToFileOperator.partial(
    task_id="save_files_to_S3",
    if_exists="replace",
).expand_kwargs(
    country_tables.map(
        lambda x: {
            "input_data": x,
            "output_file": File(
                path=f"s3://{S3_BUCKET}/{S3_FOLDER_COUNTRY_SUBSET}/{x.name}.csv",
                conn_id=AWS_CONN_ID,
            ),
        }
    )
)
```

Using the Astro Python SDK in the first three steps allows you to easily switch between data warehouses and object storage solutions, simply by changing the connection ID.
After these preparatory steps follows a task group created by the [Astro Databricks provider DatabricksWorkflowTaskGroup](https://astronomer.github.io/astro-provider-databricks/#databricks-workflow-taskgroup):

```python
task_group = DatabricksWorkflowTaskGroup(
    group_id="databricks_workflow",
    databricks_conn_id=DATABRICKS_CONN_ID,
    job_clusters=job_cluster_spec,
)

with task_group:
    notebook_1 = DatabricksNotebookOperator(
        task_id="join_data",
        databricks_conn_id=DATABRICKS_CONN_ID,
        notebook_path=DATABRICKS_NOTEBOOK_PATH_JOIN_DATA,
        source=S3_BUCKET,
        job_cluster_key=DATABRICKS_JOB_CLUSTER_KEY,
    )
    notebook_2 = DatabricksNotebookOperator(
        task_id="transform_data",
        databricks_conn_id=DATABRICKS_CONN_ID,
        notebook_path=DATABRICKS_NOTEBOOK_PATH_TRANSFORM_DATA,
        source=S3_BUCKET,
        job_cluster_key=DATABRICKS_JOB_CLUSTER_KEY,
    )
    notebook_1 >> notebook_2
```

This task group contains three tasks: 

- `launch`: This task is automatically created byt the task group and launches a job cluster with the specifications provided in the `job_cluster_spec`.
- `join_data`: This task executes the first notebook in the Databricks Workflow, which joins the data from the three CSV files created in the object storage into a single CSV file. View the full notebook code [here](https://github.com/astronomer/learn-airflow-databricks-tutorial/blob/main/databricks_notebook_code/join_data_notebook_code.py), note that if you are using an object storage other than S3 you will need to make changes to the code enclosed in `# --------- AWS S3 specific --------- #` comments.
- `transform_data`: This task executes the second notebook in the Databricks Workflow, which fetches the CSV created by the `join_data` task, creates a new column `SHW%` by summing the % points for solar, hydro and wind energy for each year in the specified country and saves the result as a CSV in the object storage. View the full notebook code [here](https://github.com/astronomer/learn-airflow-databricks-tutorial/blob/main/databricks_notebook_code/transform_data_notebook_code.py) (adjust for other object storage solutions as described above).

After the task group is completed, two tasks run in parallel.

The `delete_intake_files_S3` task cleans up files no longer needed in the S3 bucket using the [S3DeleteObjectsOperator](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest/modules/S3DeleteObjectsOperator). If you use a different object storage solution, you will need to define this task using an operator from the corresponding provider. See the [Astronomer Registry](https://registry.astronomer.io/) to explore available providers and operators.

```python
delete_intake_files_S3 = S3DeleteObjectsOperator(
    task_id="delete_intake_files_S3",
    bucket=S3_BUCKET,
    prefix=f"{S3_FOLDER_COUNTRY_SUBSET}/",
    aws_conn_id=AWS_CONN_ID,
)
```

The the `create_graph` task uses the [Astro Python SDK dataframe operator](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html) to load the information from the combined and transformed CSV created by the Databricks notebook executed via the `transform_data` task into a Pandas dataframe. The task creates a line plot of the % of solar, hydro and wind energy in the specified country over time using [seaborn](https://seaborn.pydata.org/) and [matplotlib](https://matplotlib.org/) and saves it in the `include` folder of the repository.

```python
@aql.dataframe
def create_graph(df: pd.DataFrame):
    sns.set_style("whitegrid")
    sns.lineplot(x="Year", y="SHW%", data=df)
    plt.title(f"% of Solar, Hydro and Wind in the {COUNTRY}")
    plt.xlabel("Year")
    plt.ylabel("Combined SHW (in %)")
    plt.savefig("include/shw.png")

# [...]

load_file_to_db = aql.load_file(
    input_file=File(path=DATABRICKS_RESULT_FILE_PATH, conn_id=AWS_CONN_ID),
    output_table=Table(conn_id=DB_CONN_ID),
)
```

Finally, the [Astro Python SDK `aql.cleanup()`](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/cleanup.html) task removes all temporary tables in the data warehouse that were created by Astro Python SDK tasks.

## See also

- Tutorial: [Orchestrate dbt Core jobs with Airflow and Cosmos](airflow-databricks.md).
- Documentation: [Astro Databricks provider](https://astronomer.github.io/astro-provider-databricks/).
- Webinar: [The easiest way to orchestrate your dbt workflows from Airflow](https://www.astronomer.io/events/webinars/how-to-orchestrate-databricks-jobs-using-airflow/).