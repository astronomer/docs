---
title: "Cross-DAG dependencies"
sidebar_label: "Cross-DAG dependencies"
description: "How to implement dependencies between your Airflow DAGs."
id: cross-dag-dependencies
---

import CodeBlock from '@theme/CodeBlock';
import triggerdagrun_example_traditional from '!!raw-loader!../code-samples/dags/cross-dag-dependencies/triggerdagrun_example_traditional.py';
import triggerdagrun_example_taskflow from '!!raw-loader!../code-samples/dags/cross-dag-dependencies/triggerdagrun_example_taskflow.py';
import external_task_sensor_example_taskflow from '!!raw-loader!../code-samples/dags/cross-dag-dependencies/external_task_sensor_example_taskflow.py';
import external_task_sensor_example_traditional from '!!raw-loader!../code-samples/dags/cross-dag-dependencies/external_task_sensor_example_traditional.py';
import rest_api_example_traditional from '!!raw-loader!../code-samples/dags/cross-dag-dependencies/rest_api_example_traditional.py';
import rest_api_example_taskflow from '!!raw-loader!../code-samples/dags/cross-dag-dependencies/rest_api_example_taskflow.py';

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

When designing Airflow DAGs, it is often best practice to put all related tasks in the same DAG. However, it's sometimes necessary to create dependencies between your DAGs. In this scenario, one node of a DAG is its own complete DAG, rather than just a single task. Throughout this guide, the following terms are used to describe DAG dependencies:

- **Upstream DAG**: A DAG that must reach a specified state before a downstream DAG can run
- **Downstream DAG**: A DAG that cannot run until an upstream DAG reaches a specified state

The Airflow topic [Cross-DAG Dependencies](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html#cross-dag-dependencies), indicates cross-DAG dependencies can be helpful in the following situations:

- A DAG should only run after one or more datasets have been updated by tasks in other DAGs.
- Two DAGs are dependent, but they have different schedules.
- Two DAGs are dependent, but they are owned by different teams.
- A task depends on another task but for a different execution date.

In this guide, you'll review the methods for implementing cross-DAG dependencies, including how to implement dependencies if your dependent DAGs are located in different Airflow deployments.


All code used in this  is available in the [cross-dag-dependencies-tutorial registry](https://github.com/astronomer/cross-dag-dependencies-tutorial).

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Dependencies in Airflow. See [Managing Dependencies in Apache Airflow](managing-dependencies.md).
- Airflow DAGs. See [Introduction to Airflow DAGs](dags.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow sensors. See [Sensors 101](what-is-a-sensor.md).

## Implement cross-DAG dependencies

There are multiple ways to implement cross-DAG dependencies in Airflow, including:

- [Dataset driven scheduling](airflow-datasets.md).
- The [TriggerDagRunOperator](https://registry.astronomer.io/providers/apache-airflow/modules/triggerdagrunoperator).
- The [ExternalTaskSensor](https://registry.astronomer.io/providers/apache-airflow/modules/externaltasksensor).
- The [Airflow API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html).

In this section, you'll learn how and when you should use each method and how to view dependencies in the Airflow UI.

Using SubDAGs to handle DAG dependencies can cause performance issues. Instead, use one of the methods described in this guide.

### Dataset dependencies

In Airflow 2.4 and later, you can use datasets to create data-driven dependencies between DAGs. DAGs that access the same data can have explicit, visible relationships, and DAGs can be scheduled based on updates to this data.

You should use this method if you have a downstream DAG that should only run after a dataset has been updated by an upstream DAG, especially if those updates are irregular. This type of dependency also provides you with increased observability into the dependencies between your DAGs and datasets in the Airflow UI.

Using datasets requires knowledge of the following scheduling concepts:

- **Producing task**: A task that updates a specific dataset, defined by its `outlets` parameter.
- **Consuming DAG**: A DAG that runs as soon as a specific dataset is updated.

Any task can be made into a producing task by providing one or more datasets to the `outlets` parameter. For example:

```python
dataset1 = Dataset('s3://folder1/dataset_1.txt')

# producing task in the upstream DAG
EmptyOperator(
    task_id="producing_task",
    outlets=[dataset1]  # flagging to Airflow that dataset1 was updated
)
```

The following downstream DAG is scheduled to run after `dataset1` has been updated by providing it to the `schedule` parameter.

```python
dataset1 = Dataset('s3://folder1/dataset_1.txt')

# consuming DAG
with DAG(
    dag_id='consuming_dag_1',
    catchup=False,
    start_date=datetime.datetime(2022, 1, 1),
    schedule=[dataset1]
) as dag:
```

In the Airflow UI, the **Next Run** column for the downstream DAG shows dataset dependencies for the DAG and how many dependencies have been updated since the last DAG run. The following image shows that the DAG `dataset_dependent_example_dag` runs only after two different datasets have been updated. One of those datasets has already been updated by an upstream DAG.

![DAG Dependencies View](/img/guides/2_4_DatasetDependentDAG.png)

See [Datasets and Data-Aware Scheduling in Airflow](airflow-datasets.md) to learn more.

### TriggerDagRunOperator

The TriggerDagRunOperator is a straightforward method of implementing cross-DAG dependencies from an upstream DAG. This operator allows you to have a task in one DAG that triggers another DAG in the same Airflow environment. For more information about this operator, see [TriggerDagRunOperator](https://registry.astronomer.io/providers/apache-airflow/modules/triggerdagrunoperator).

You can trigger a downstream DAG with the TriggerDagRunOperator from any point in the upstream DAG. If you set the operator's  `wait_for_completion` parameter to `True`, the upstream DAG will pause and resume only once the downstream DAG has finished running. As of Airflow 2.6 this waiting process can be deferred to the triggerer by setting the parameter `deferrable` to True, turning the operator into a [deferrable operator](deferrable-operators.md) which increases Airflow's scalability and can reduce cost.

A common use case for this implementation is when an upstream DAG fetches new testing data for a machine learning pipeline, runs and tests a model, and publishes the model's prediction. In case of the model underperforming, the TriggerDagRunOperator is used to start a separate DAG that retrains the model while the upstream DAG waits. Once the model is retrained and tested by the downstream DAG, the upstream DAG resumes and publishes the new model's results.

The [schedule](scheduling-in-airflow.md) of the downstream DAG is independent of the runs triggered by the TriggerDagRunOperator. For a DAG to only run based on the TriggerDagRunOperator, set the `schedule` parameter to `None`. Note that the dependent DAG must be unpaused for it to be triggered by the TriggerDagRunOperator.

The following example DAG implements the TriggerDagRunOperator to trigger a DAG with the `dag_id` `dependent_dag` between two other tasks. Since both the `wait_for_completion` and the `deferrable` parameters of the `trigger_dependent_dag` task in the `trigger_dagrun_dag` are set to `True`, the task is deferred until the `dependent_dag` has finished its run. Once the `trigger_dagrun_dag` task completes, the `end_task` will run.

<Tabs
    defaultValue="taskflow"
    groupId="triggerdagrunoperator"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{triggerdagrun_example_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{triggerdagrun_example_traditional}</CodeBlock>

</TabItem>
</Tabs>

In the following image, you can see that the `trigger_dependent_dag` task in the middle is the TriggerDagRunOperator, which runs the `dependent-dag`.

![Trigger DAG Graph](/img/guides/trigger_dag_run_graph.png)

If your dependent DAG requires a config input or a specific execution date, you can specify them in the operator using the `conf` and `execution_date` params respectively.

### ExternalTaskSensor

To create cross-DAG dependencies from a downstream DAG, consider using one or more [ExternalTaskSensors](https://registry.astronomer.io/providers/apache-airflow/modules/externaltasksensor). The downstream DAG will pause until a task is completed in the upstream DAG before resuming.

This method of creating cross-DAG dependencies is especially useful when you have a downstream DAG with different branches that depend on different tasks in one or more upstream DAGs. Instead of defining an entire DAG as being downstream of another DAG as you do with datasets, you can set a specific task in a downstream DAG to wait for a task to finish in an upstream DAG.

For example, you could have upstream tasks modifying different tables in a data warehouse and one downstream DAG running one branch of data quality checks for each of those tables. You can use one ExternalTaskSensor at the start of each branch to make sure that the checks running on each table only start after the update to the specific table is finished.

In Airflow 2.2 and later, a deferrable version of the ExternalTaskSensor is available, the [ExternalTaskSensorAsync](https://registry.astronomer.io/providers/astronomer-providers/modules/externaltasksensorasync). For more info on deferrable operators and their benefits, see [Deferrable Operators](deferrable-operators.md)

The following example DAG uses three ExternalTaskSensors at the start of three parallel branches in the same DAG.

<Tabs
    defaultValue="taskflow"
    groupId="externaltasksensor"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{external_task_sensor_example_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{external_task_sensor_example_traditional}</CodeBlock>

</TabItem>
</Tabs>

In this DAG:

- `ets_branch_1` waits for the `my_task` task of `upstream_dag_1` to complete before moving on to execute `task_branch_1`.
- `ets_branch_2` waits for the `my_task` task of `upstream_dag_2` to complete before moving on to execute `task_branch_2`.
- `ets_branch_3` waits for the `my_task` task of `upstream_dag_3` to complete before moving on to execute `task_branch_3`.

These processes happen in parallel and are independent of each other. The graph view shows the state of the DAG after `my_task` in `upstream_dag_1` has finished which caused `ets_branch_1` and `task_branch_1` to run. `ets_branch_2` and `ets_branch_3` are still waiting for their upstream tasks to finish.

![ExternalTaskSensor 3 Branches](/img/guides/2_4_external_task_sensor_graph_3_branches.png)

If you want the downstream DAG to wait for the entire upstream DAG to finish instead of a specific task, you can set the `external_task_id` to `None`. In the example above, you specified that the external task must have a state of `success` for the downstream task to succeed, as defined by the `allowed_states` and `failed_states`.

In the previous example, the upstream DAG (`example_dag`) and downstream DAG (`external-task-sensor-dag`) must have the same start date and schedule interval. This is because the ExternalTaskSensor will look for completion of the specified task or DAG at the same `logical_date` (previously called `execution_date`). To look for completion of the external task at a different date, you can make use of either of the `execution_delta` or `execution_date_fn` parameters (these are described in more detail in the documentation linked above).

### Airflow API

The [Airflow API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) is another way of creating cross-DAG dependencies. This is especially useful in [Airflow 2.0](https://www.astronomer.io/blog/introducing-airflow-2-0), which has a fully stable REST API. To use the API to trigger a DAG run, you can make a POST request to the `DAGRuns` endpoint as described in the [Airflow API documentation](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run).

This method is useful if your dependent DAGs live in different Airflow environments (more on this in the Cross-Deployment Dependencies section below). The task triggering the downstream DAG will complete once the API call is complete.

Using the API to trigger a downstream DAG can be implemented within a DAG by using the [SimpleHttpOperator](https://registry.astronomer.io/providers/http/modules/simplehttpoperator) as shown in the example DAG below:

<Tabs
    defaultValue="taskflow"
    groupId="airflow-api"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{rest_api_example_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{rest_api_example_traditional}</CodeBlock>

</TabItem>
</Tabs>

This DAG has a similar structure to the TriggerDagRunOperator DAG, but instead uses the SimpleHttpOperator to trigger the `dependent-dag` using the Airflow API. The graph view appears similar to the following image:

![API Graph View](/img/guides/api_graph.png)

To use the SimpleHttpOperator to trigger another DAG, you need to define the following:

- `endpoint`: This should be of the form `'/api/v1/dags/<dag-id>/dagRuns'` where `<dag-id>` is the ID of the DAG you want to trigger.
- `data`: To trigger a DAG run using this endpoint, you must provide an execution date. In the example above, we use the `execution_date` of the upstream DAG, but this can be any date of your choosing. You can also specify other information about the DAG run as described in the API documentation linked above.
- `http_conn_id`: This should be an [Airflow connection](connections.md) of [type HTTP](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/connections/http.html), with your Airflow domain as the Host. Any authentication should be provided either as a Login/Password (if using Basic auth) or as a JSON-formatted Extra. In the example below, we use an authorization token.

![Http Connection](/img/guides/http_connection.png)

## DAG dependencies view

In [Airflow 2.1](https://airflow.apache.org/docs/apache-airflow/stable/changelog.html#airflow-2-1-0-2021-05-21), a new cross-DAG dependencies view was added to the Airflow UI. This view shows all DAG dependencies in your Airflow environment as long as they are implemented using one of the following methods:

- Using dataset driven scheduling
- Using a TriggerDagRunOperator
- Using an ExternalTaskSensor

To view dependencies in the UI, go to **Browse** > **DAG Dependencies** or by click **Graph** within the **Datasets** tab. The following image shows the dependencies created by the TriggerDagRunOperator and ExternalTaskSensor example DAGs.

![DAG Dependencies View](/img/guides/dag_dependencies_view.png)

When DAGs are scheduled depending on datasets, both the DAG containing the producing task and the dataset are shown upstream of the consuming DAG.

![DAG Dependencies View Datasets](/img/guides/2_4_CrossGuide_Dependencies.png)

In Airflow 2.4 an additional **Datasets** tab was added, which shows all dependencies between datasets and DAGs.

![DAG Dependencies View Datasets](/img/guides/2_5_Datasets.png)

## Cross-deployment dependencies

It is sometimes necessary to implement cross-DAG dependencies where the DAGs do not exist in the same Airflow deployment. The TriggerDagRunOperator, ExternalTaskSensor, and dataset methods are designed to work with DAGs in the same Airflow environment, so they are not ideal for cross-Airflow deployments. The Airflow API is ideal for this use case. In this section, you'll learn how to implement this method on Astro, but the general concepts are also applicable to your Airflow environments.

### Cross-deployment dependencies on Astro

To implement cross-DAG dependencies on two different Airflow environments on Astro, follow the steps for triggering a DAG using the Airflow API. Before you get started, you should review [Make requests to the Airflow REST API](https://docs.astronomer.io/astro/airflow-api). When you're ready to implement a cross-deployment dependency, follow these steps:

1. In the upstream DAG, create a SimpleHttpOperator task that will trigger the downstream DAG. Refer to the section above for details on configuring the operator.
2. In the Deployment running the downstream DAG, [create an API key](https://docs.astronomer.io/astro/api-keys) and copy it.
3. In the upstream DAG Airflow environment, create an Airflow connection as shown in the Airflow API section above. The Host should be `https://<your-base-domain>/<deployment-release-name>/airflow` where the base domain and deployment release name are from your downstream DAG's Airflow deployment. In the **Extras** field, enter `{"Authorization": "api-token"}` where `api-token` is the API key you copied in step 2.
4. Ensure the downstream DAG is turned on, then run the upstream DAG.

You can follow similar steps to implement cross-deployment dependencies on Astronomer Software. See [Make requests to the Airflow REST API](https://docs.astronomer.io/software/airflow-api) for Software-specific instructions on accessing the Airflow API.
