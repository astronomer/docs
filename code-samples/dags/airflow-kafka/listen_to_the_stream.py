"""
### DAG continuously listening to a Kafka topic for a specific message

This DAG will always run and asynchronously monitor a Kafka topic for a message 
which causes the funtion supplied to the `apply_function` parameter to return a value.
If a value is returned by the `apply_function`, the `event_triggered_function` is 
executed. Afterwards the task will go into a deferred state again. 
"""

from airflow.decorators import dag
from pendulum import datetime
from airflow.providers.apache.kafka.sensors.kafka import (
    AwaitMessageTriggerFunctionSensor,
)
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import json
import uuid

PET_MOODS_NEEDING_A_WALK = ["zoomy", "bouncy"]
KAFKA_TOPIC = "my_topic"


def listen_function(message, pet_moods_needing_a_walk=[]):
    """Checks if the message received indicates a pet is in
    a mood listed in `pet_moods_needing_a_walk` when they received the last
    treat of a treat-series."""

    message_content = json.loads(message.value())
    print(f"Full message: {message_content}")
    pet_name = message_content["pet_name"]
    pet_moode_post_treat = message_content["pet_moode_post_treat"]
    final_treat = message_content["final_treat"]
    if final_treat:
        if pet_moode_post_treat in pet_moods_needing_a_walk:
            return pet_name, pet_moode_post_treat


def event_triggered_function(event, **context):
    "Kicks off a downstream DAG with conf and waits for its completion."

    pet_name = event[0]
    pet_mood_post_treat = event[1]
    print(
        f"Due to {pet_name} being in a {pet_mood_post_treat} mood, a walk is being initiated..."
    )
    # use the TriggerDagRunOperator (TDRO) to kick off a downstream DAG
    TriggerDagRunOperator(
        trigger_dag_id="walking_my_pet",
        task_id=f"triggered_downstream_dag_{uuid.uuid4()}",
        wait_for_completion=True,  # wait for downstream DAG completion
        conf={"pet_name": pet_name},
        poke_interval=5,
    ).execute(context)

    print(f"The walk has concluded and {pet_name} is now happily taking a nap!")


@dag(
    start_date=datetime(2023, 4, 1),
    schedule="@continuous",
    max_active_runs=1,
    catchup=False,
    render_template_as_native_obj=True,
)
def listen_to_the_stream():
    listen_for_mood = AwaitMessageTriggerFunctionSensor(
        task_id="listen_for_mood",
        kafka_config_id="kafka_listener",
        topics=[KAFKA_TOPIC],
        # the apply function will be used from within the triggerer, this is
        # why it needs to be a dot notation string
        apply_function="listen_to_the_stream.listen_function",
        poll_interval=5,
        poll_timeout=1,
        apply_function_kwargs={"pet_moods_needing_a_walk": PET_MOODS_NEEDING_A_WALK},
        event_triggered_function=event_triggered_function,
    )


listen_to_the_stream()
