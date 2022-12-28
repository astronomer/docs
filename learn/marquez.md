---
title: "Integrate OpenLineage and Airflow locally with Marquez"
sidebar_label: "Run OpenLineage locally with Marquez"
description: "Use OpenLineage and Marquez to get lineage data locally from your Airflow DAGs."
id: marquez
tags: [Lineage]
---

and implement an example local integration of Airflow and OpenLineage for tracking data movement in Postgres

In this tutorial, you'll run OpenLineage with Airflow locally using Marquez as a lineage front end. You'll then generate and interpret lineage data using a simple DAG that processes data in Postgres.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of OpenLineage. See [Integrate OpenLineage and Airflow](airflow-openlineage.md).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A database

## Step 1: Run Marquez locally

Marquez is an open source lineage front end that you will use to view OpenLineage data generated from Airflow.

1. Run Marquez locally using the quickstart in the [Marquez README](https://github.com/MarquezProject/marquez#quickstart).

## Step 2: Configure your Astro project

Use the Astro CLI to create and run an Airflow project locally that will integrate with Marquez.

1. Create a new Astro project:

    ```sh
    $ mkdir astro-marquez-tutorial && cd astro-marquez-tutorial
    $ astro dev init
    ```

2. Add the following line to the `requirements.txt` file of your Astro project:

    ```text
    openlineage-airflow
    ```

    This installs the [openLineage-airflow package](https://openlineage.io/integration/apache-airflow/) that allows OpenLineage to integrate with Airflow.

3. Add the following environment variables below to your `.env` file:
    
    ```bash
    OPENLINEAGE_URL=http://host.docker.internal:5000
    OPENLINEAGE_NAMESPACE=example
    AIRFLOW__LINEAGE__BACKEND=openlineage.lineage_backend.OpenLineageBackend
    ```

    These will allow Airflow to connect with the OpenLineage API and send your lineage data to Marquez.
    
    By default, Marquez uses port 5000 when you run it using Docker. If you are using a different OpenLineage front end instead of Marquez, or you are running Marquez remotely, you can modify the `OPENLINEAGE_URL` as needed.
    
4. Modify your `config.yaml` in the `.astro/` directory to choose a different port for Postgres:
    
    ```yaml
    project:
      name: openlineage
    postgres:
      port: 5435
    ```

    Marquez also uses Postgres, so you will need to have Airflow use a different port than the default 5432, which is already allocated.
    
5. Run the following command to start your local project:

    ```sh
    astro dev start
    ```

6. Confirm Airflow is running by going to `http://localhost:8080`, and Marquez is running by going to `http://localhost:3000`.

## Step 3: Configure your database

To show the lineage data that can result from Airflow DAG runs, you'll use two sample DAGs that process data in Postgres. To run this example in your own environment, complete the following steps:

1. (Optional) Create a local Postgres database in the same container as the Airflow metastore using `psql`:

    ```bash
    psql -h localhost -p 5435 -U postgres
    <enter password `postgres` when prompted>
    create database lineagedemo;
    ```

    If you already have a Postgres database or are using a different type of database you can skip this step. Note that this database should be separate from the Airflow and Marquez metastores.

2. Run the following SQL statements to create and populate two source tables:

    ```sql
    CREATE TABLE IF NOT EXISTS adoption_center_1
    (date DATE, type VARCHAR, name VARCHAR, age INTEGER);

    CREATE TABLE IF NOT EXISTS adoption_center_2
    (date DATE, type VARCHAR, name VARCHAR, age INTEGER);

    INSERT INTO
        adoption_center_1 (date, type, name, age)
    VALUES
        ('2022-01-01', 'Dog', 'Bingo', 4),
        ('2022-02-02', 'Cat', 'Bob', 7),
        ('2022-03-04', 'Fish', 'Bubbles', 2);

    INSERT INTO
        adoption_center_2 (date, type, name, age)
    VALUES
        ('2022-06-10', 'Horse', 'Seabiscuit', 4),
        ('2022-07-15', 'Snake', 'Stripes', 8),
        ('2022-08-07', 'Rabbit', 'Hops', 3);
    ```

## Step 4: Configure your Airflow connection

The connection you configure will connect to the Postgres database you created in [Step 3](#step-3-configure-your-database).

1. In the Airflow UI, go to **Admin** -> **Connections**.

2. Create a new connection named `postgres_default` and choose the `postgres` connection type. Enter the following information: 


    If you are working with a database other than local Postgres, you may need to provide different information to the connection.

## Step 5: Create your DAGs

For this tutorial you will create two DAGs to generate and interpret lineage data. 

1. In your Astro project `dags` folder, create a new file called `lineage-combine.py`. Paste the following code into the file:

    ```python
    from airflow import DAG
    from airflow.providers.postgres.operators.postgres import PostgresOperator

    from datetime import datetime, timedelta

    create_table_query= '''
    CREATE TABLE IF NOT EXISTS animal_adoptions_combined (date DATE, type VARCHAR, name VARCHAR, age INTEGER);
    '''

    combine_data_query= '''
    INSERT INTO animal_adoptions_combined (date, type, name, age) 
    SELECT * 
    FROM adoption_center_1
    UNION 
    SELECT *
    FROM adoption_center_2;
    '''

    with DAG('lineage-combine-postgres',
            start_date=datetime(2020, 6, 1),
            max_active_runs=1,
            schedule='@daily',
            default_args = {
                'retries': 1,
                'retry_delay': timedelta(minutes=1)
            },
            catchup=False
            ):

        create_table = PostgresOperator(
            task_id='create_table',
            postgres_conn_id='postgres_default',
            sql=create_table_query
        ) 

        insert_data = PostgresOperator(
            task_id='combine',
            postgres_conn_id='postgres_default',
            sql=combine_data_query
        ) 

        create_table >> insert_data
    ```

2. Create another file in your `dags` folder and call it `lineage-reporting.py`. Paste the following code into the file:

    ```python
    from airflow import DAG
    from airflow.providers.postgres.operators.postgres import PostgresOperator

    from datetime import datetime, timedelta

    aggregate_reporting_query = '''
    INSERT INTO adoption_reporting_long (date, type, number)
    SELECT c.date, c.type, COUNT(c.type)
    FROM animal_adoptions_combined c
    GROUP BY date, type;
    '''

    with DAG('lineage-reporting-postgres',
            start_date=datetime(2020, 6, 1),
            max_active_runs=1,
            schedule='@daily',
            default_args={
                'retries': 1,
                'retry_delay': timedelta(minutes=1)
            },
            catchup=False
            ):

        create_table = PostgresOperator(
            task_id='create_reporting_table',
            postgres_conn_id='postgres_default',
            sql='CREATE TABLE IF NOT EXISTS adoption_reporting_long (date DATE, type VARCHAR, number INTEGER);',
        ) 

        insert_data = PostgresOperator(
            task_id='reporting',
            postgres_conn_id='postgres_default',
            sql=aggregate_reporting_query
        ) 

        create_table >> insert_data
    ```

The first DAG creates and populates a table (`animal_adoptions_combined`) with data aggregated from the two source tables (`adoption_center_1` and `adoption_center_2`) you created in [Step 3](#step-3-configure-your-database). The second DAG creates and populates a reporting table (`adoption_reporting_long`) using data from the aggregated table (`animal_adoptions_combined`) created in your first DAG.

You might want to make adjustments to these DAGs if you are working with different source tables, or if your Postgres connection id is not `postgres_default`.

## Step 6: Run your DAGs and view lineage data

If you run these DAGs in Airflow, and then go to Marquez, you will see a list of your jobs, including the four tasks from the previous DAGs.

![Marquez Jobs](/img/guides/marquez_jobs.png)

Then, if you click one of the jobs from your DAGs, you see the full lineage graph.

![Marquez Graph](/img/guides/marquez_lineage_graph.png)

The lineage graph shows:

- Two origin datasets that are used to populate the combined data table;
- The two jobs (tasks) from your DAGs that result in new datasets: `combine` and `reporting`;
- Two new datasets that are created by those jobs.

The lineage graph shows you how these two DAGs are connected and how data flows through the entire pipeline, giving you insight you wouldn't have if you were to view these DAGs in the Airflow UI alone.

## Step 7: Track a task failure using lineage


