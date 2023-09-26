---
title: "Orchestrate Redshift operations with Airflow"
sidebar_label: "Implementation"
description: "Orchestrate Redshift queries from your Airflow DAGs."
id: airflow-redshift
tags: [Database, SQL, DAGs, Integrations, AWS]
sidebar_custom_props: { icon: 'img/integrations/redshift.png' }
---

Amazon Redshift is a fully-managed cloud data warehouse. It has become the most popular cloud data warehouse in part because of its ability to analyze exabytes of data and run complex analytical queries.

Developing a dimensional data mart in Redshift requires automation and orchestration for repeated queries, data quality checks, and overall cluster operations. This makes Airflow the perfect orchestrator to pair with Redshift. With Airflow, you can orchestrate each step of your Redshift pipeline, integrate with services that clean your data, and store and publish your results using SQL and Python code.

In this tutorial, you'll learn about the Redshift modules that are available in the [AWS Airflow provider package](https://registry.astronomer.io/providers/amazon). You'll also complete sample implementations that execute SQL in a Redshift cluster, pause and resume a Redshift cluster, and transfer data between Amazon S3 and a Redshift cluster.

All code in this tutorial is located in the [GitHub repo](https://github.com/astronomer/cs-tutorial-redshift).

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of [Amazon Redshift](https://aws.amazon.com/redshift/getting-started/?nc=sn&loc=4&dn=1).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Setup

To use Redshift operators in Airflow, you first need to install the Redshift provider package and create a connection to your Redshift cluster.

1. If you are working with the [Astro CLI](https://docs.astronomer.io/astro/install-cli), add `apache-airflow-providers-amazon` to the `requirements.txt` file of your Astro project. Otherwise, run `pip install apache-airflow-providers-amazon`.

2. Connect your Airflow instance to Redshift. The most common way of doing this is by configuring an Airflow connection. In the Airflow UI, go to **Admin** > **Connections** and add the following connections:

    - `redshift_default`: The default connection that Airflow Redshift modules use. If you use a name other than `redshift_default` for this connection, you'll need to specify it in the modules that require a Redshift connection. Use the following parameters for your new connection (all other fields can be left blank):
  
     ```yaml
     Connection ID: redshift_default
     Connection Type: Amazon Redshift
     Host: <your-redshift-endpoint> (for example, redshift-cluster-1.123456789.us-west-1.redshift.amazonaws.com)
     Schema: <your-redshift-database> (for example, dev, test, prod, etc.)
     Login: <your-redshift-username> (for example, awsuser)
     Password: <your-redshift-password>
     Port: <your-redshift-port> (for example, 5439)
     ```
  
    - `aws_default`: The default connection that other Airflow AWS modules use. For the examples in this guide, you will need this connection for Airflow to communicate with Amazon S3. If you use a name other than `aws_default` for this connection, you'll need to specify it in the modules that require an AWS connection. Use the following parameters for your new connection (all other fields can be left blank):
  
     ```yaml
     Connection ID: aws_default
     Connection Type: Amazon Web Services
     Extra: {
       "aws_access_key_id": "<your-access-key-id>", 
       "aws_secret_access_key": "<your-secret-access-key>", 
       "region_name": "<your-region-name>"
     }
     ```

3. Configure the following in your Redshift cluster:

    - [Allow inbound traffic](https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-authorize-cluster-access.html) from the IP Address where Airflow is running
    - Give `aws_default` the following permissions on AWS:
        - Read/write permissions for a preconfigured S3 Bucket
        - Permission to interact with the Redshift cluster, specifically:
            - `redshift:DescribeClusters`
            - `redshift:PauseCluster`
            - `redshift:ResumeCluster`

    If your Airflow instance is running in the same AWS VPC as your Redshift cluster, you may have other authentication options available. To authenticate to Redshift using IAM Authentication or Okta, see the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/redshift.html).

### Sample data

The following examples use the sample database (TICKIT) provided by AWS. For more details on the underlying data, see [Sample database](https://docs.aws.amazon.com/redshift/latest/dg/c_sampledb.html).

## Using the RedshiftSQLOperator

After you've implemented a connection to Redshift, you can start using the [`RedshiftSQLOperator`](https://registry.astronomer.io/providers/amazon/modules/redshiftsqloperator). The `RedshiftSQLOperator` is used to run one or multiple SQL statements against a Redshift cluster. Use cases for this operator include:

- Creating data schema models in your data warehouse.
- Creating fact or dimension tables for various data models.
- Performing data transformations or data cleaning.

The following DAG shows how you can use the `RedshiftSQLOperator` to run a `.sql` query against a Redshift schema:

```python
from datetime import datetime
from airflow.models import DAG
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator

with DAG(
    dag_id=f"example_dag_redshift",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    template_searchpath='/usr/local/airflow/include/example_dag_redshift',
    catchup=False
) as dag:

    t = RedshiftSQLOperator(
        task_id='fct_listing',
        sql='/sql/fct_listing.sql',
        params={
            "schema": "fct",
            "table": "listing"
        }
    )
```

Notice the value for `template_searchpath` in the `DAG()` configuration. This value indicates that the DAG looks for the `.sql` file at `/usr/local/airflow/include/example_dag_redshift/sql/fct_listing.sql`. For this example, you'll use the following SQL file:

```sql
begin;
create table if not exists {{ params.schema }}.{{ params.table }} (
  date_key date,
  total_sellers int,
  total_events int,
  total_tickets int,
  total_revenue double precision
) sortkey(date_key)
;

delete from {{ params.schema }}.{{ params.table }} where date_key = '{{ ds }}';

insert into {{ params.schema }}.{{ params.table }}
  select
    listtime::date as date_key,
    count(distinct sellerid) as total_sellers,
    count(distinct eventid) as total_events,
    sum(numtickets) as total_tickets,
    sum(totalprice) as total_revenue
  from tickit.listing
  where listtime::date = '{{ ds }}'
  group by date_key
;
end;
```

In this SQL query, there are multiple templated parameters: `{{ params.schema }}`, `{{ params.table }}`, and `{{ ds }}`. Based on the task definition, `{{ params.schema }}` is set as `fct` and `{{ params.table }}` is set as `listing`. These values are injected into the SQL query at runtime. The `{{ ds }}` variable is a built-in [Airflow Jinja Template Variable](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html) that returns the DAG run's logical date in the format YYYY-MM-DD. Using templated variables makes your SQL code reusable and aligned DAG writing best practices (particularly in relation to [idempotency](dag-best-practices.md#reviewing-idempotency)).

## Using the S3ToRedshiftOperator

The [`S3ToRedshiftOperator`](https://registry.astronomer.io/providers/amazon/modules/s3toredshiftoperator) executes a
`COPY` command to load files from S3 to Redshift. The following example DAG demonstrates how to use this operator:

```python
from datetime import datetime
from airflow.models import DAG
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

with DAG(
    dag_id=f"example_dag_redshift",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    template_searchpath='/usr/local/airflow/include/example_dag_redshift',
    catchup=False
) as dag:

    s3_to_redshift = S3ToRedshiftOperator(
        task_id='s3_to_redshift',
        schema='fct',
        table='from_redshift',
        s3_bucket='airflow-redshift-demo',
        s3_key='fct/from_redshift',
        redshift_conn_id='redshift_default',
        aws_conn_id='aws_default',
        copy_options=[
            "DELIMITER AS ','"
        ],
        method='REPLACE'
    )
```

This DAG copies the S3 blob `s3://airflow-redshift-demo/fct/from_redshift` into the table `fct.from_redshift` on the Redshift cluster. With this operator, you can pass all the same copy options that exist in AWS with the `copy_options` parameter. For more information about the `COPY` command, see [Data format parameters](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html#r_COPY-syntax-overview-data-format). In this example, a copy option is used to change the delimiter for the blob from a pipe character to a comma.

## Use the RedshiftToS3Operator

The [`RedshiftToS3Operator`](https://registry.astronomer.io/providers/amazon/modules/redshifttos3operator) executes an `UNLOAD` command to Amazon S3 as a CSV file with headers. `UNLOAD` automatically creates encrypted files using Amazon S3 server-side encryption (SSE). There are numerous use cases for using the `UNLOAD` command. Some of the more common use cases include:

- Archiving old data that is no longer needed in your Redshift cluster.
- Sharing the results of query data without granting access to Redshift.
- Saving the result of query data into Amazon S3 for analysis with BI tools or use in an ML pipeline.

The following DAG shows an example implementation:

```python
from datetime import datetime
from airflow.models import DAG
from airflow.providers.amazon.aws.transfers.redshift_to_s3 import RedshiftToS3Operator

with DAG(
    dag_id=f"example_dag_redshift",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    template_searchpath='/usr/local/airflow/include/example_dag_redshift',
    catchup=False
) as dag:
  
    redshift_to_s3 = RedshiftToS3Operator(
        task_id='fct_listing_to_s3',
        s3_bucket='airflow-redshift-demo',
        s3_key='fct/listing/{{ ds }}_',
        schema='fct',
        table='listing',
        redshift_conn_id='redshift_default',
        aws_conn_id='aws_default',
        table_as_file_name=False,
        unload_options=[
            "DELIMITER AS ','",
            "FORMAT AS CSV",
            "ALLOWOVERWRITE",
            "PARALLEL OFF",
            "HEADER"
        ]
    )
```

This DAG copies the `fct.listing` table from a Redshift cluster to the Amazon S3 blob `s3:://airflow-redshift-demo/fct/listing/YYYY-MM-DD_` (where YYYY-MM-DD is the logical date for the DAG run). With this operator, you can pass all the same unload options that exist in AWS. For more information on the `UNLOAD` command, see the AWS [UNLOAD documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_UNLOAD.html).

In this example, based on the parameters set in the DAG, the delimiter for the blob has been specified as a comma and the format of the blob has been specified as a CSV. Any existing files are overwritten, data is not written in parallel across multiple files, and a header line containing column names is included at the top of the file.

## Pause and resume a Redshift cluster from Airflow

Amazon Redshift supports the ability to pause and resume a cluster, allowing customers to suspend on-demand billing when the cluster isn't being used. For more information, see [Amazon Redshift launches pause and resume](https://aws.amazon.com/about-aws/whats-new/2020/03/amazon-redshift-launches-pause-resume/#:~:text=Amazon%20Redshift%20now%20supports%20the,suspended%20when%20not%20in%20use.).

You may want your Airflow DAG to pause and unpause a Redshift cluster at times when it isn't being queried or used. Additionally, you may want to pause your Redshift cluster at the end of your Airflow pipeline, or resume your Redshift cluster at the beginning of your Airflow pipeline. There are currently three Airflow modules available to accomplish this:

- The [`RedshiftPauseClusterOperator`](https://registry.astronomer.io/providers/amazon/modules/redshiftpauseclusteroperator) can be used to pause an AWS Redshift Cluster.
- The [`RedshiftResumeClusterOperator`](https://registry.astronomer.io/providers/amazon/modules/redshiftresumeclusteroperator) can be used to resume a paused AWS Redshift Cluster.
- The [`RedshiftClusterSensor`](https://registry.astronomer.io/providers/amazon/modules/redshiftclustersensor) can be used to wait for a Redshift cluster to reach a specific status, For example, available after it has been unpaused.

If no operations queried your Redshift cluster after your last ETL job, you can use the `RedshiftPauseClusterOperator` to pause your Redshift cluster, which would lower your AWS bill. On the first ETL job of the day, you could add the `RedshiftResumeClusterOperator` at the beginning of your DAG to send the request to AWS to unpause it. Following that task, you could use a `RedshiftClusterSensor` to ensure the cluster is fully available before running the remainder of your DAG.

The following DAG shows how to pause and unpause a Redshift cluster using the available operators. As the sensor is implemented at the end, the DAG is identified as successful when the cluster state is `Available`.

```python
from datetime import datetime
from airflow.models import DAG
from airflow.providers.amazon.aws.operators.redshift_cluster import RedshiftPauseClusterOperator
from airflow.providers.amazon.aws.operators.redshift_cluster import RedshiftResumeClusterOperator
from airflow.providers.amazon.aws.sensors.redshift_cluster import RedshiftClusterSensor


with DAG(
    dag_id=f"example_dag_redshift",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    template_searchpath='/usr/local/airflow/include/example_dag_redshift',
    catchup=False
) as dag:
  
    pause_redshift = RedshiftPauseClusterOperator(
        task_id='pause_redshift',
        cluster_identifier='astronomer-success-redshift',
        aws_conn_id='aws_default'
    )
    
    resume_redshift = RedshiftResumeClusterOperator(
      task_id='resume_redshift',
      cluster_identifier='astronomer-success-redshift',
      aws_conn_id='aws_default'
    )

    cluster_sensor = RedshiftClusterSensor(
        task_id='wait_for_cluster',
        cluster_identifier='astronomer-success-redshift',
        target_status='available',
        aws_conn_id='aws_default'
    )

    pause_redshift >> resume_redshift >> cluster_sensor
```
