---
title: "Production-ready ML with Airflow, Snowpark, and Weaviate"
description: "Use Airflow, Snowpark and Weaviate to use Customer sentiment to predict LTV"
id: use-case-airflow-mlflow
sidebar_label: "ML with Snowpark and Airflow"
sidebar_custom_props: { icon: 'img/integrations/mlflow.png' }
---

[Snowpark ML](https://docs.snowflake.com/en/developer-guide/snowpark-ml/index) (in public preview) is a python framework for Machine Learning workloads with [Snowpark](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html).  Currently Snowpark ML provides a model registry (storing ML tracking data and models in Snowflake tables and stages), feature engineering primitives similar to scikit-learn (ie. LabelEncoder, OneHotEncoder, etc.) and support for training and deploying [certain model types](https://docs.snowflake.com/en/developer-guide/snowpark-ml/snowpark-ml-modeling#snowpark-ml-modeling-classes) as well as deployments as user-defined functions (UDFs).

This guide demonstrates how to use Apache Airflow to orchestrate a machine learning pipeline leveraging the Snowpark provider and Snowpark ML for feature engineering and model tracking. While Snowpark ML has its own support for models similar to scikit-learn this code demonstrates a "bring-your-own" model approach showing the use of open-source scikit-learn along with Snowpark ML model registry and model serving in an Airflow task rather than Snowpark user-defined function (UDF).  

This demonstration shows how to build a customer analytics dashboard.  Sissy-G Toys is a fictitious online retailer for toys and games.  The GroundTruth customer analytics application provides marketing, sales and product managers with a one-stop-shop for analytics.  The application uses machine learning models for audio transcription, natural language embeddings and sentiment analysis on structured, semi-structured and unstructured data. All of the processing and prediction work is managed by Airflow, leveraging Snowparks compute and proximity to Snowflake data

This demo also shows the use of the Snowflake XCOM backend which supports security and governance by serializing all task in/output to Snowflake tables and stages while storing in the Airflow XCOM table a URI pointer to the data.

This workflow includes:
- sourcing structured, unstructured and semistructured data from different systems
- extract, transform and load with [Snowpark Python provider for Airflow](https://github.com/astronomer/astro-provider-snowflake)
- ingest with Astronomer's [python SDK for Airflow](https://github.com/astronomer/astro-sdk)
- audio file transcription with [OpenAI Whisper](https://github.com/openai/whisper)
- natural language embeddings with [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) and the [Weaviate provider for Airflow](https://github.com/astronomer/airflow-provider-weaviate)
- vector search with [Weaviate](https://weaviate.io/)
- sentiment classification with [LightGBM](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html)  
- ML model management with [Snowflake ML](https://docs.snowflake.com/LIMITEDACCESS/snowflake-ml-modeling)
  
All of the above are presented in a [Streamlit](http://www.streamlit.io) application.  

## Before you start

Before trying this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- [Docker Desktop](https://www.docker.com/products/docker-desktop).
- A [Snowflake](https://www.snowflake.com/en/) Account with AccountAdmin permissions
- (Optional) OpenAI account or [Trial Account](https://platform.openai.com/signup)


## Set-up the project

Clone the example project from the [Astronomer GitHub](https://github.com/astronomer/airflow-snowparkml-demo/tree/main).

```bash
git clone https://github.com/astronomer/airflow-snowparkml-demo
cd airflow-snowparkml-demo 
```

Open the `.env` file in an editor and update the following variables with you account information. You only need to update the Snowflake Connection details to be able to run the Customer Analytics DAG. However, if you'd like to enable chat capabilities in the final streamlit application, please add an OpenAI API key where designated in the .env file as well. 

This demo assumes the use of a new Snowflake trial account with admin privileges.  A database named 'DEMO' and schema named 'DEMO' will be created in the DAG.  Running this demo without admin privileges or with existing database/schema will require further updates to the `.env` file.
  
- AIRFLOW_CONN_SNOWFLAKE_DEFAULT  
  -- login  
  -- password  
  -- account **  
- OPENAI_APIKEY  
  
** The Snowflake `account` field of the connection should use the new `ORG_NAME-ACCOUNT_NAME` format as per [Snowflake Account Identifier policies](https://docs.snowflake.com/en/user-guide/admin-account-identifier).  The ORG and ACCOUNT names can be found in the confirmation email or in the Snowflake login link (ie. `https://xxxxxxx-yyy11111.snowflakecomputing.com/console/login`)
Do not specify a `region` when using this format for accounts.
  
NOTE: Database and Schema names should be CAPITALIZED due to a bug in Snowpark ML.

## Run the project

To run the example project, first make sure Docker Desktop is running. Then, open your project directory and run:

```sh
astro dev start
```

This command builds your project and spins up 5 Docker containers on your machine to run it. In addition to the 4 standard Airflow containers, a Weaviate container is spun up as well. This allows us to run a fully local Weaviate environment for local development, giving every developer their own dedicated testing environment.

After the command finishes, open the the [Airflow UI](http://localhost:8080/) and press trigger the `customer_analytics` DAG using the play button. Then, monitor its status as it completes via the graph view!

## View Results in Streamlit

Once the DAG has completed, you can look at the results in a Streamlit customer analytics dashboard. 
Streamlit has been installed alongside the Airflow UI in the webserver container, and there's a script in the include directory called `streamlit_app.py` that you'll use to create the dashboard.

To do so, first go to your projects root directory and connect to the webserver container with the Astro CLI
```bash
astro dev bash -w
``` 

Then, run the following command to start Streamlit
```bash
cd include/streamlit/src
python -m streamlit run ./streamlit_app.py
```

You can then open the [streamlit application](http://localhost:8501) in a browser.

## Project Code

This project consists of one DAG, [customer_analytics](https://github.com/astronomer/airflow-snowparkml-demo/blob/main/dags/customer_analytics.py) which demonstrates an end-to-end ML application workflow using OpenAI embeddings with a Weaviate vector database as well as Snowpark decorators, the Snowflake XCOM backend and the Snowpark ML model registry. The Astro CLI can easily be adapted to include additionalDocker-based services, in this use case we used  Weaviate and streamlit.

```python
    @task.snowpark_python()
    def create_snowflake_objects(snowflake_objects:dict, calls_directory_stage:str):
       

        snowpark_session.sql(f"""CREATE DATABASE IF NOT EXISTS \
                                {snowflake_objects['demo_database']};""").collect()

        snowpark_session.sql(f"""CREATE SCHEMA IF NOT EXISTS \
                                {snowflake_objects['demo_database']}.\
                                {snowflake_objects['demo_schema']};""").collect()

        snowpark_session.sql(f"""CREATE STAGE IF NOT EXISTS \
                                {snowflake_objects['demo_database']}.\
                                {snowflake_objects['demo_schema']}.\
                                {snowflake_objects['demo_xcom_stage']} 
                                    DIRECTORY = (ENABLE = TRUE)
                                    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
                             """).collect()
        
        snowpark_session.sql(f"""CREATE TABLE IF NOT EXISTS \
                             {snowflake_objects['demo_database']}.\
                            {snowflake_objects['demo_schema']}.\
                            {snowflake_objects['demo_xcom_table']}
                                    ( 
                                        dag_id varchar NOT NULL, 
                                        task_id varchar NOT NULL, 
                                        run_id varchar NOT NULL,
                                        multi_index integer NOT NULL,
                                        key varchar NOT NULL,
                                        value_type varchar NOT NULL,
                                        value varchar NOT NULL
                                 ); 
                              """).collect()
        
        snowpark_session.sql(f"""CREATE OR REPLACE STAGE \
                                {snowflake_objects['demo_database']}.\
                                {snowflake_objects['demo_schema']}.\
                                {calls_directory_stage} 
                                        DIRECTORY = (ENABLE = TRUE) 
                                        ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
                                """).collect()
```

Task ‘create_snowflake_objects’:
Our first task creates Snowflake objects (databases, schemas, stages, etc.) prior to 
running any tasks, since we are assuming you are starting with a fresh trial account. This is implemented using the new setup/teardown task feature, and has a corresponding clean up task at the end of the DAG. This means that no matter what, temp tables used for this project will be deleted after usage to prevent unnecessary consumption, mimicking how you might use them in a production setting! 

```
@task_group()
    def enter():
        """
        Using an `enter()` task group allows us to group together tasks that should be run to setup 
        state for the rest of the DAG.  Functionally this is very similar to setup tasks but allows 
        some additional flexibility in dependency mapping.
        """

        @task()
        def download_weaviate_backup() -> str:
            """
            [Weaviate](http://www.weaviate.io) is a vector database which allows us to store a 
            vectorized representation of unstructured data like twitter tweets or audio calls.
            In this demo we use the [OpenAI  embeddings](https://platform.openai.com/docs/guides/embeddings/embeddings) 
            model to build the vectors.  With the vectors we can do sentiment classification 
            based on cosine similarity with a labeled dataset.  

            This demo uses a version of Weaviate running locally in a Docker container.  See the 
            `docker-compose.override.yml` file for details. The Astro CLI will start this container 
            alongside the Airflow webserver, trigger, scheduler and database.

            In order to speed up the demo process the data has already been ingested into weaviate 
            and vectorized.  The data was then backed up and stored in the cloud for easy restore.            
            
            This task will download the backup.zip and make it available in a docker mounted 
            filesystem for the weaviate restore task.  Normally this would be in an cloud storage.
            """
            import urllib
            import zipfile

            weaviate_restore_uri = f'{restore_data_uri}/weaviate-backup/backup.zip'

            zip_path, _ = urllib.request.urlretrieve(weaviate_restore_uri)
            with zipfile.ZipFile(zip_path, "r") as f:
                f.extractall('/usr/local/airflow/include/weaviate/data/backups')

        @task.snowpark_python()
        def check_model_registry(snowflake_objects:dict) -> dict:
            """
            Snowpark ML provides a model registry leveraging tables, views and stages to 
            track model state as well as model artefacts. 

            If the model registry objects have not yet been created in Snowflake this task 
            will create them and return a dictionary with the database and schema where they 
            exist.
            """
            from snowflake.ml.registry import model_registry

            assert model_registry.create_model_registry(session=snowpark_session, 
                                                        database_name=snowflake_objects['demo_database'], 
                                                        schema_name=snowflake_objects['demo_schema'])
            
            snowpark_model_registry = {'database': snowflake_objects['demo_database'], 
                                    'schema': snowflake_objects['demo_schema']}

            return snowpark_model_registry
        
        _snowpark_model_registry = check_model_registry(snowflake_objects)
        
        _restore_weaviate = WeaviateRestoreOperator(task_id='restore_weaviate',
                                                    backend='filesystem', 
                                                    id='backup',
                                                    include=list(weaviate_class_objects.keys()),
                                                    replace_existing=True)
        
        _restore_weaviate.doc_md = dedent(
            """
            ### Restoring Demo Data  
            In order to speed up the demo process the data has already been ingested into weaviate 
            and vectorized.  The data was then backed up and stored in the cloud for easy restore.

            This task restores the pre-vectorized demo data using the backup.zip file downloaded 
            in the `download_weaviate_backup` task.  

            Upstream tasks will try to import to weaviate will but will be `skipped` since they 
            already exist.  For any new data Weaviate will use OpenAI embeddings to vectorize 
            and import data.
            """
        )

        download_weaviate_backup() >> _restore_weaviate

        return _snowpark_model_registry, _restore_weaviate
```

The DAG then runs the “enter” task group, which includes 3 tasks to set up a Weaviate database, and create a Snowpark model registry if none exists already:

Task download_weaviate_backup: 
In order to speed up the demo process the data has already been ingested into Weaviate and vectorized.  The data was then backed up and stored in the cloud for easy restore. This task will download the backup.zip and make it available in a docker mounted filesystem for the restore_weaviate task.

Task restore_weaviate: 
This task exists only to speedup the demo in subsequent runs. By restoring prefetched embeddings to Weaviate the later tasks will skip embeddings and only make calls to OpenAI for data it hasn't yet embedded.

Task check_model_registry:
This task checks if a Snowpark model registry exists in the specified database and schema. If not, it creates one and returns a dictionary containing the database and schema information.

```python
    @task_group()
    def structured_data():
        """
        This demo shows the ability to build with structured, semi-strcutured and unstructured data 
        in Snowflake.  

        This section extracts, transforms and load structured data from an S3 bucket.
        """

        @task_group()
        def load_structured_data():
            """
            The [Astro Python SDK](https://docs.astronomer.io/learn/astro-python-sdk-etl)
            is a good way to easily load data to a database with very few lines of code.

            Here we use dynamically generated tasks in a task group.  A task will be created 
            to load each file in the `data_sources` list.
            """
            for source in data_sources:
                aql.load_file(task_id=f'load_{source}',
                    input_file = File(f"{restore_data_uri}/{source}.csv"), 
                    output_table = Table(name=f'STG_{source.upper()}', 
                                         conn_id=_SNOWFLAKE_CONN_ID)
                )

        @task_group()
        def transform_structured():

            @task.snowpark_python()
            def jaffle_shop(customers_df:SnowparkTable, orders_df:SnowparkTable, payments_df:SnowparkTable):
                """
                Historically users must write SQL code for data transformations in Snowflake.  
                For example, the SQL code in the `include/sql/jaffle_shop.sql` file can be 
                [orchestrated as a task](https://docs.astronomer.io/learn/airflow-snowflake) 
                in Airflow with something like the following:  
  
                _customers = SnowflakeOperator(task_id="jaffle_shop",
                                               sql=Path('include/sql/jaffle_shop.sql).read_text(),
                                               params={"table_name": CUSTOMERS})
                
                Alternatively, users can use the Snowpark Dataframe API for simplicity, 
                readability and extensibility.

                Best practices for pipeline orchestration dictate the need to build 'atomic' 
                and 'idempotent' tasks.  However, Snowpark sessions and session-residenct objects, 
                such as Snowpark DataFrames, are not serializable and cannot easily be passed between 
                tasks. 
                
                The Astronomer provider for Snowpark includes a `SnowparkTable` dataclass which 
                can be serialized and deserialized.

                Any SnowparkTable objects passed as arguments are automatically instantiated as 
                Snowpark dataframes.

                Any Snowpark dataframe objects returned from the task are automatically serialized as tables 
                based on the decorator parameters `temp_data_output`, `temp_data_schema`, `temp_data_overwrite`, 
                and `temp_data_table_prefix`.  For this demo these parameters are set as `default_args` at the 
                top of this file.  Alternatively, these can be set for each task or overriden per-task.

                The Snowpark `Functions` and `Types` have been automatically imported as `F` and 
                `T` respectively.
                """
                
                customer_orders_df = orders_df.group_by('customer_id').agg(F.min('order_date').alias('first_order'),
                                                                           F.max('order_date').alias('most_recent_order'),
                                                                           F.count('order_id').alias('number_of_orders'))
                
                customer_payments_df = payments_df.join(orders_df, how='left', on='order_id')\
                                                  .group_by('customer_id')\
                                                  .agg((F.sum('amount') / 100).alias('total_amount'))
                
                customers = customers_df.join(customer_orders_df, how='left', on='customer_id')\
                                        .join(customer_payments_df, how='left', on='customer_id')\
                                        .rename('total_amount', 'customer_lifetime_value')
                
                payment_types = ['credit_card', 'coupon', 'bank_transfer', 'gift_card']
                
                orders = payments_df.drop('payment_id')\
                                    .pivot('payment_method', payment_types )\
                                    .agg(F.sum('amount'))\
                                    .group_by('order_id')\
                                    .agg({f"'{x}'": "sum" for x in payment_types})\
                                    .rename({f"SUM('{x.upper()}')": x+'_amount' for x in payment_types})\
                                    .join(payments_df.group_by('order_id')\
                                                     .agg(F.sum('amount').alias('total_amount')), on='order_id')\
                                    .join(orders_df, on='order_id')

                return customers

            @task.snowpark_virtualenv(python_version='3.8', requirements=['snowflake-snowpark-python>=1.8'])
            def mrr_playbook(subscription_df:SnowparkTable):
                """
                Snowpark Python currently supports Python 3.8, 3.9, and 3.10.  If the version of 
                Python used to run Airflow is different it may be necessary to use a Python virtual 
                environment for Snowpark tasks.  
                  
                The `snowpark_virtualenv` decorator and `SnowparkVirtualenvOperator` allow users 
                to specify a different python version similar to the 
                [PythonVirtualenvOperator](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/pythonvirtualenvoperator).  
                Python executables for the specified version must be installed on the executor.  
                Additional packages can be installed in the virtual environment by specifying a
                `requirements` parameter as a list of strings.
                  
                Astronomer has created a [Docker Buildkit](https://github.com/astronomer/astro-provider-venv) 
                to simplify building virtual environments with Astro CLI.  See the `Dockerfile` for 
                details.
                """
                from snowflake.snowpark import Window
                from datetime import date

                day_count = date.today() - date(2018,1,1)
                months = snowpark_session.generator(F.seq4(), rowcount=day_count.days)\
                                         .with_column('date_month', F.date_trunc('month', 
                                                                            F.date_add(F.to_date(F.lit('2018-01-01')), 
                                                                                       F.row_number().over(Window.order_by('SEQ4(0)')))))\
                                         .select('date_month').distinct().sort('date_month', ascending=True)

                subscription_periods = subscription_df.with_column('start_date', F.to_date('start_date'))\
                                                      .with_column('end_date', F.to_date('end_date'))
                
                customers = subscription_periods.group_by('customer_id').agg(F.date_trunc('month', F.min('start_date')).alias('date_month_start'),
                                                                             F.date_trunc('month', F.max('end_date')).alias('date_month_end'))
                
                customer_months = customers.join(months, how='inner', on=(months['date_month'] >= customers['date_month_start']) & 
                                                                         ( months['date_month'] < customers['date_month_end']))\
                                           .select(['customer_id', 'date_month'])
                
                customer_revenue_by_month = customer_months.join(subscription_periods, 
                                                                how='left',
                                                                rsuffix='_',
                                                                on=(customer_months.customer_id == subscription_periods.customer_id) & 
                                                                    (customer_months.date_month >= subscription_periods.start_date) & 
                                                                    ((customer_months.date_month < subscription_periods.end_date) |
                                                                        (subscription_periods.end_date.is_null())))\
                                                            .fillna(subset=['monthly_amount'], value=0)\
                                                            .select(F.col('date_month'), F.col('customer_id'), F.col('monthly_amount').alias('mrr'))\
                                                            .with_column('is_active', F.col('mrr')>0)\
                                                            .with_column('first_active_month', 
                                                                         F.when(F.col('is_active'), 
                                                                            F.min(F.col('date_month')).over(Window.partition_by('customer_id'))))\
                                                            .with_column('last_active_month', 
                                                                         F.when(F.col('is_active'), 
                                                                            F.max(F.col('date_month')).over(Window.partition_by('customer_id'))))\
                                                            .with_column('is_first_month', F.col('first_active_month') == F.col('date_month'))\
                                                            .with_column('is_last_month', F.col('last_active_month') == F.col('date_month'))
                                                            
                customer_churn_month = customer_revenue_by_month.where('is_last_month')\
                                                                .select(F.add_months(F.col('date_month'), 1),
                                                                        'customer_id',
                                                                        F.to_decimal('mrr', 38, 2),
                                                                        F.lit(False).alias('is_active'),
                                                                        'first_active_month',
                                                                        'last_active_month',
                                                                        F.lit(False).alias('is_first_month'),
                                                                        F.lit(False).alias('is_last_month'))
                
                customer_date_window = Window.partition_by('customer_id').order_by('date_month')

                mrr = customer_revenue_by_month.union_all(customer_churn_month)\
                                               .with_column('id', F.md5(F.col('customer_id')))\
                                               .with_column('previous_month_is_active', 
                                                            F.lag('is_active', default_value=False).over(customer_date_window))\
                                               .with_column('previous_month_mrr', 
                                                            F.lag('mrr', default_value=0).over(customer_date_window))\
                                               .with_column('mrr_change', F.col('mrr') - F.col('previous_month_mrr'))\
                                               .with_column('change_category', 
                                                            F.when(F.col('is_first_month'), 'new')\
                                                             .when(F.not_(F.col('is_active') & F.col('previous_month_is_active')), 'churn')\
                                                             .when(F.col('is_active') & F.not_(F.col('previous_month_is_active')), 'reactivation')\
                                                             .when(F.col('mrr_change') > 0, 'upgrade')\
                                                             .when(F.col('mrr_change') < 0, 'downgrade')
                                                            )\
                                               .with_column('renewal_amount', F.least(F.col('mrr'), F.col('previous_month_mrr')))

                return mrr
            
            @task.snowpark_ext_python(python='/home/astro/.venv/snowpark/bin/python')
            def attribution_playbook(customer_conversions_df:SnowparkTable, sessions_df:SnowparkTable):
                """
                Snowpark Python currently supports Python 3.8, 3.9, and 3.10.  If the version of 
                Python used to run Airflow is different it may be necessary to use a Python virtual 
                environment for Snowpark tasks.  
                  
                The `snowpark_ext_python` decorator and `SnowparkExternalPythonOperator` allow users 
                to specify a different python executable similar to the 
                [ExternalPythonOperator](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/externalpythonoperator).  
                  
                Astronomer has created a [Docker Buildkit](https://github.com/astronomer/astro-provider-venv) 
                to simplify building virtual environments with Astro CLI.  See the `Dockerfile` for 
                details.
                """
                from snowflake.snowpark import Window

                customer_window = Window.partition_by('customer_id')

                attribution_touches = sessions_df.join(customer_conversions_df, on='customer_id')\
                                                .filter((F.col('started_at') <= F.col('converted_at')) & 
                                                        (F.col('started_at') >= F.date_add(F.col('converted_at'), -30)))\
                                                .with_column('total_sessions', F.count('customer_id')\
                                                                                .over(customer_window))\
                                                .with_column('session_index', F.row_number()\
                                                                                .over(customer_window\
                                                                                .order_by('started_at')))\
                                                .with_column('first_touch_points', 
                                                            F.when(F.col('session_index') == 1, 1)\
                                                            .otherwise(0))\
                                                .with_column('last_touch_points', 
                                                            F.when(F.col('session_index') == F.col('total_sessions'), 1)\
                                                            .otherwise(0))\
                                                .with_column('forty_twenty_forty_points', 
                                                            F.when(F.col('total_sessions') == 1, 1)\
                                                            .when(F.col('total_sessions') == 2, .5)\
                                                            .when(F.col('session_index') == 1, .4)\
                                                            .when(F.col('session_index') == F.col('total_sessions'), .4)\
                                                            .otherwise(F.lit(0.2) / (F.col('total_sessions') - 2)))\
                                                .with_column('linear_points', F.lit(1) / F.col('total_sessions'))\
                                                .with_column('first_touch_revenue', 
                                                             F.col('revenue') * F.col('first_touch_points'))\
                                                .with_column('last_touch_revenue', 
                                                             F.col('revenue') * F.col('last_touch_points'))\
                                                .with_column('forty_twenty_forty_revenue', 
                                                             F.col('revenue') * F.col('forty_twenty_forty_points'))\
                                                .with_column('linear_revenue', 
                                                             F.col('revenue') * (1 / F.col('total_sessions')))
                return attribution_touches

            _customers = jaffle_shop(customers_df=SnowparkTable('stg_customers'),
                                     orders_df=SnowparkTable('stg_orders'),
                                     payments_df=SnowparkTable('stg_payments'))
            
            _mrr = mrr_playbook(subscription_df=SnowparkTable('stg_subscription_periods'))

            _attribution_touches = attribution_playbook(customer_conversions_df=SnowparkTable('stg_customer_conversions'), 
                                                        sessions_df=SnowparkTable('stg_sessions'))
            
            return _attribution_touches, _mrr, _customers

        _structured_data = load_structured_data()
        _attribution_touches, _mrr, _customers = transform_structured()
        _structured_data >> [_attribution_touches, _mrr, _customers]

        return _attribution_touches, _mrr, _customers
```

