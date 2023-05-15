"""
Example showing how to use the SlackNotifier. Needs a Slack connection set
up with Slack API Token for a Slack bot (starts with 'xoxb-...')
"""

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.providers.slack.notifications.slack_notifier import SlackNotifier

SLACK_CONNECTION_ID = "slack_conn"
SLACK_CHANNEL = "alerts"
SLACK_MESSAGE = """
Hello! The {{ ti.task_id }} task is saying hi :wave: 
Today is the {{ ds }} and this task finished with the state: {{ ti.state }} :tada:.
"""


@dag(
    start_date=datetime(2023, 4, 18),
    schedule=None,
    catchup=False,
    tags=["Notifier", "Slack"],
)
def slack_notifier_example_dag():
    @task(
        on_success_callback=SlackNotifier(
            slack_conn_id=SLACK_CONNECTION_ID,
            text=SLACK_MESSAGE,
            channel=SLACK_CHANNEL,
        ),
    )
    def post_to_slack():
        return 10

    post_to_slack()


slack_notifier_example_dag()
