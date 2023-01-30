from pendulum import datetime

from airflow.models import DAG
from pandas import DataFrame

from astro import sql as aql
from astro.files import File
from astro.sql.table import Table

S3_FILE_PATH = "s3://<aws-bucket-name>"
S3_CONN_ID = "aws_default"
SNOWFLAKE_CONN_ID = "snowflake_default"
SNOWFLAKE_ORDERS = "orders_table"
SNOWFLAKE_FILTERED_ORDERS = "filtered_table"
SNOWFLAKE_JOINED = "joined_table"
SNOWFLAKE_CUSTOMERS = "customers_table"
SNOWFLAKE_REPORTING = "reporting_table"


@aql.transform
def filter_orders(input_table: Table):
    return "SELECT * FROM {{input_table}} WHERE amount > 150"


@aql.transform
def join_orders_customers(filtered_orders_table: Table, customers_table: Table):
    return """SELECT c.customer_id, customer_name, order_id, purchase_date, amount, type
    FROM {{filtered_orders_table}} f JOIN {{customers_table}} c
    ON f.customer_id = c.customer_id"""


@aql.dataframe
def transform_dataframe(df: DataFrame):
    purchase_dates = df.loc[:, "purchase_date"]
    print("purchase dates:", purchase_dates)
    return purchase_dates


with DAG(
    dag_id="astro_orders",
    start_date=datetime(2019, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    # Extract a file with a header from S3 into a Table object
    orders_data = aql.load_file(
        # data file needs to have a header row
        input_file=File(
            path=S3_FILE_PATH + "/orders_data_header.csv", conn_id=S3_CONN_ID
        ),
        output_table=Table(conn_id=SNOWFLAKE_CONN_ID),
    )

    # create a Table object for customer data in our Snowflake database
    customers_table = Table(
        name=SNOWFLAKE_CUSTOMERS,
        conn_id=SNOWFLAKE_CONN_ID,
    )

    # filter the orders data and then join with the customer table
    joined_data = join_orders_customers(filter_orders(orders_data), customers_table)

    # merge the joined data into our reporting table, based on the order_id .
    # If there's a conflict in the customer_id or customer_name then use the ones from
    # the joined data
    reporting_table = aql.merge(
        target_table=Table(
            name=SNOWFLAKE_REPORTING,
            conn_id=SNOWFLAKE_CONN_ID,
        ),
        source_table=joined_data,
        target_conflict_columns=["order_id"],
        columns=["customer_id", "customer_name"],
        if_conflicts="update",
    )

    purchase_dates = transform_dataframe(reporting_table)