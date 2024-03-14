from airflow.decorators import dag, task_group, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.models.baseoperator import chain, chain_linear
from airflow.utils.edgemodifier import Label
from airflow.datasets import Dataset
from pendulum import datetime


@dag(
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)
def complex_dag_structure():

    start = EmptyOperator(task_id="start")

    sales_data_extract = BashOperator.partial(task_id="sales_data_extract").expand(
        bash_command=["echo 1", "echo 2", "echo 3", "echo 4"]
    )
    internal_api_extract = BashOperator.partial(task_id="internal_api_extract").expand(
        bash_command=["echo 1", "echo 2", "echo 3", "echo 4"]
    )

    @task.branch
    def determine_load_type():
        return "internal_api_load_incremental"

    sales_data_transform = EmptyOperator(task_id="sales_data_transform")

    determine_load_type_obj = determine_load_type()

    sales_data_load = EmptyOperator(task_id="sales_data_load")
    internal_api_load_full = EmptyOperator(task_id="internal_api_load_full")
    internal_api_load_incremental = EmptyOperator(
        task_id="internal_api_load_incremental"
    )

    @task_group()
    def sales_data_reporting(a):
        prepare_report = EmptyOperator(
            task_id="prepare_report", trigger_rule="all_done"
        )
        publish_report = EmptyOperator(task_id="publish_report")

        chain(prepare_report, publish_report)

    sales_data_reporting_obj = sales_data_reporting.expand(a=[1, 2, 3, 4, 5, 6])

    @task_group
    def cre_integration():
        cre_extract = EmptyOperator(task_id="cre_extract", trigger_rule="all_done")
        cre_transform = EmptyOperator(task_id="cre_transform")
        cre_load = EmptyOperator(task_id="cre_load")

        chain(cre_extract, cre_transform, cre_load)

    cre_integration_obj = cre_integration()

    @task_group()
    def mlops():
        set_up_cluster = EmptyOperator(
            task_id="set_up_cluster", trigger_rule="all_done"
        )
        train_model = EmptyOperator(
            task_id="train_model", outlets=[Dataset("model_trained")]
        )
        tear_down_cluster = EmptyOperator(task_id="tear_down_cluster")

        chain(set_up_cluster, train_model, tear_down_cluster)

        tear_down_cluster.as_teardown(setups=set_up_cluster)

    mlops_obj = mlops()

    end = EmptyOperator(task_id="end")

    chain(
        start,
        sales_data_extract,
        sales_data_transform,
        sales_data_load,
        [sales_data_reporting_obj, cre_integration_obj],
        end,
    )
    chain(
        start,
        internal_api_extract,
        determine_load_type_obj,
        [internal_api_load_full, internal_api_load_incremental],
        mlops_obj,
        end,
    )

    chain_linear(
        [sales_data_load, internal_api_load_full],
        [sales_data_reporting_obj, cre_integration_obj],
    )

    chain(
        determine_load_type_obj, Label("additional data"), internal_api_load_incremental
    )
    chain(
        determine_load_type_obj, Label("changed existing data"), internal_api_load_full
    )


complex_dag_structure()
