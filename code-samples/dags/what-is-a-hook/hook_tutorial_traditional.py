# importing necessary packages
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.slack.hooks.slack import SlackHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

# set bucket name and file names
S3BUCKET_NAME = "myhooktutorial"
S3_EXAMPLE_FILE_NAME_1 = "file1.txt"
S3_EXAMPLE_FILE_NAME_2 = "file2.txt"
S3_EXAMPLE_FILE_NAME_3 = "file3.txt"


# function to read 3 keys from your S3 bucket
def read_keys_from_s3_function():
    s3_hook = S3Hook(aws_conn_id="aws_conn")
    response_file_1 = s3_hook.read_key(
        key=S3_EXAMPLE_FILE_NAME_1, bucket_name=S3BUCKET_NAME
    )
    response_file_2 = s3_hook.read_key(
        key=S3_EXAMPLE_FILE_NAME_2, bucket_name=S3BUCKET_NAME
    )
    response_file_3 = s3_hook.read_key(
        key=S3_EXAMPLE_FILE_NAME_3, bucket_name=S3BUCKET_NAME
    )

    response = {
        "num1": int(response_file_1),
        "num2": int(response_file_2),
        "num3": int(response_file_3),
    }

    return response


# function running a check on the data retrieved from your S3 bucket
def run_sum_check_function(response):
    if response["num1"] + response["num2"] == response["num3"]:
        return (True, response["num3"])
    return (False, response["num3"])


# function posting to slack depending on the outcome of the above check
# and returning the server response
def post_to_slack_function(sum_check_result):
    slack_hook = SlackHook(slack_conn_id="hook_tutorial_slack_conn")

    if sum_check_result[0] is True:
        server_response = slack_hook.call(
            api_method="chat.postMessage",
            json={
                "channel": "#test-airflow",
                "text": f"""All is well in your bucket!
                        Correct sum: {sum_check_result[1]}!""",
            },
        )
    else:
        server_response = slack_hook.call(
            api_method="chat.postMessage",
            json={
                "channel": "#test-airflow",
                "text": f"""A test on your bucket contents failed!
                        Target sum not reached: {sum_check_result[1]}""",
            },
        )

    # return the response of the API call (for logging or use downstream)
    return server_response


# implementing the DAG
with DAG(
    dag_id="hook_tutorial",
    start_date=datetime(2022, 5, 20),
    schedule="@daily",
    catchup=False,
    # Render templates using Jinja NativeEnvironment
    render_template_as_native_obj=True,
):
    read_keys_form_s3 = PythonOperator(
        task_id="read_keys_form_s3", python_callable=read_keys_from_s3_function
    )

    run_sum_check = PythonOperator(
        task_id="run_sum_check",
        python_callable=run_sum_check_function,
        op_kwargs={
            "response": "{{ ti.xcom_pull(task_ids='read_keys_form_s3', \
                key='return_value') }}"
        },
    )

    post_to_slack = PythonOperator(
        task_id="post_to_slack",
        python_callable=post_to_slack_function,
        op_kwargs={
            "sum_check_result": "{{ ti.xcom_pull(task_ids='run_sum_check', \
                key='return_value') }}"
        },
    )

    # the dependencies are automatically set by XCom
    read_keys_form_s3 >> run_sum_check >> post_to_slack
