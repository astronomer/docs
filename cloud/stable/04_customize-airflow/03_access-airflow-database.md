---
title: "Access the Airflow Database"
navTitle: "Access the Airflow Database"
description: "How to access Airflow's Postgres Metadata Database on Astronomer Cloud."
---

## Overview

On Astronomer, each Airflow deployment is equipped with a PostgreSQL database that serves as Airflow's underlying metadata database and your Airflow Scheduler's source of truth.

For Astronomer Cloud users, our team securely hosts that database.

This guide will cover guidelines for the following:

- Risks associated with and use cases for Database Access
- Access to Airflow's Database in Local Development
- Access to Airflow's Database on Astronomer
- Example DAG that incorporates a query to the database

> **Note:** Airflow's "Ad-Hoc Query" feature used to be a common way to test DB connections and query the Airflow Metadata Database via the Airflow UI but was deprecated in 1.10 for security reasons.

### Risk Associated with Database Access

As noted above, your Airflow Deployment's Metadata Database on Astronomer is hosted by our team. Given its importance to the Scheduler's performance, it's worth noting the risks associated with accessing Airflow's Database.

We strongly recommend users do not write to the database directly as it can compromise both the integrity of your Airflow Deployment and our team's ability to support you in the case of an issue.

### Use Cases

Keeping the above risk in mind, pulling from and reading the database safely can be a great way to gather metadata from your Airflow Deployment that isn't otherwise exposed on Astronomer and Airflow (yet). 

A few examples of what you can query for:
- Completed Task Count
- Tasks started per hour, per week
- Task duration

Read below for DB access guidelines both locally and on Astronomer.

## Local Access to the Airflow Database

To successfully query from your Airflow Deployment's Database, you'll need to set up your local Postgres connection.

**1. Find the `airflow_db` Connection Object**

On the Airflow UI, navigate over to `Admin` > `Connections`.

The `airflow_db` connection is generated by default.

![Connections Page](https://assets2.astronomer.io/main/docs/query-postgres/query-postgres-connection-page.png)

**2. Edit the Connection**

In the `airflow_db` connection object:

- Change the `Conn Type` to `Postgres`
- Add the following connection information:

    ```
    host: postgres
    schema: postgres
    login: postgres
    password: postgres
    port (optional): 5432
    ```
Your connection should look something like:

![Local Connections Details Page](https://assets2.astronomer.io/main/docs/query-postgres/query-postgres-connection-details.png)

The port will be set to 5342 by default but if you???ve set a custom port, you???ll need to update that here as well.

**3. Connect to `airflow_db` in your DAG**

Here's an example DAG, where `postgres_conn_id` is set to `airflow_db`:

```py
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


def get_dag_ids():
    postgres_hook = PostgresHook(postgres_conn_id="airflow_db")
    records = postgres_hook.get_records(sql="select dag_id from dag")
    print(records)


with DAG(
    "example_dag",
    start_date=datetime(2019, 1, 1),
    max_active_runs=1,
    schedule_interval=None,
    # catchup=False # enable if you don't want historical dag runs to run
) as dag:

    t1 = PythonOperator(
        task_id="get_dag_nums",
        python_callable=get_dag_ids,
        sql="select dag_id from dag",
        postgres_conn_id="airflow_db",
    )
```

Here, the task above grabs all `dag_ids` stored inside `dag` Table within Airflow's Metadata Database.

### Connect to the DB via a PostgreSQL Client

With the connection information above, you should also be able to connect to the Airflow Database from any PostgreSQL client. 

Using [`psql`](https://www.postgresql.org/docs/9.3/app-psql.html), a terminal-based front-end to PostgreSQL, run:

```
$ psql -h localhost -U postgres -p 5432 -W
```

When prompted, enter the password from the Connection Object above to access the database.

Alternatively, you can also connect to the DB via the Postgres container itself by exec-ing into it and executing the `psql` command.

To do so, run:

```
    $ docker exec -it <postgres_container_id> /bin/bash
    psql -U postgres
```
    
## Access to the Airflow Database on Astronomer

The easiest way to pull from Airflow's Metadata Database on Astronomer is to leverage the `AIRFLOW_CONN_AIRFLOW_DB` Environment Variable, which we set [here](https://github.com/astronomer/airflow-chart/blob/master/templates/_helpers.yaml#L16-L20).

This Environment Variable, which we set by default, silently enables users to leverage the `airflow_db` connection. It's worth noting that the connection itself in the Airflow UI will NOT reflect the correct credentials (Conn Type, Host, Schema, Login, Password, Port).

To pull from the Airflow Database, follow the steps below. Note that you do _not_ have to set this Environment Variable yourself and you do _not_ have to populate the `airflow_db` connection in the Airflow UI.

**1. Leave your `airflow_db` Connection as is**

Your `airflow_db` connection by default will look like the following:

```
Conn Id: airflow_db
Conn Type: MySQL
Host: mysql
Schema: airflow
Login: root
```

While this information is incorrect in the Airflow UI, the underlying connection will still succeed, as connections set by an Environment Variable take precedence over connection details in the Astronomer UI and in the Metadata Database itself.

For clarity, we intend to make sure this connection is properly populated in upcoming versions of Astronomer.

**2. Call `airflow_db` in your DAG**

You can use the same example DAG outlined above where `postgres_conn_id` is set to `airflow_db`.

**3. Verify the Connection in your Task Logs**

To verify a successful connection, you can inspect the corresponding task log -

```
Dependencies all met for <TaskInstance: example_dag.get_dag_nums 2020-05-07T19:02:38.022685+00:00 [queued]>

--------------------------------------------------------------------------------
Starting attempt 1 of 1

--------------------------------------------------------------------------------
Executing <Task(PythonOperator): get_dag_nums> on 2020-05-07T19:02:38.022685+00:00
Started process 429 to run task
Running %s on host %s <TaskInstance: example_dag.get_dag_nums 2020-05-07T19:02:38.022685+00:00 [running]> desolate-spectrum-3088-worker-866745d995-rn576
[2020-05-07 19:02:54,033] {base_hook.py:87} INFO - Using connection to: id: airflow_db. Host: desolate-spectrum-3088-pgbouncer.astronomer-desolate-spectrum-3088.svc.cluster.local, Port: 6543, Schema: desolate-spectrum-3088-metadata, Login: desolate_spectrum_3088_airflow, Password: XXXXXXXX, extra: XXXXXXXX
[('example_dag',)]
Done. Returned value was: None
```

In these logs, you can see that the connection info is properly passed:

```
Conn Id: airflow_db
Host: desolate-spectrum-3088-pgbouncer
Schema: desolate-spectrum-3088-metadata
Login: desolate_spectrum_3088_airflow
Password: XXXXXXXX
Port: 6543
```

## What's Next

For a list of handy queries to reference, check out [Useful SQL queries for Apache Airflow](/guides/airflow-queries/).
