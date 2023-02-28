---
title: "Datasets and data-aware scheduling in Airflow"
sidebar_label: "Datasets and data-aware scheduling"
description: "Using datasets to implement DAG dependencies and scheduling in Airflow."
id: airflow-datasets
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import dataset_upstream1 from '!!raw-loader!../code-samples/dags/airflow-datasets/dataset_upstream1.py';
import dataset_downstream_1_2 from '!!raw-loader!../code-samples/dags/airflow-datasets/dataset_downstream_1_2.py';
import datasets_ml_example_consume from '!!raw-loader!../code-samples/dags/airflow-datasets/datasets_ml_example_consume.py';
import datasets_ml_example_publish_taskflow from '!!raw-loader!../code-samples/dags/airflow-datasets/datasets_ml_example_publish_taskflow.py';
import datasets_ml_example_publish_traditional from '!!raw-loader!../code-samples/dags/airflow-datasets/datasets_ml_example_publish_traditional.py';
import example_sdk_datasets from '!!raw-loader!../code-samples/dags/airflow-datasets/example_sdk_datasets.py';

Datasets and data-aware scheduling were made available in [Airflow 2.4](https://airflow.apache.org/docs/apache-airflow/2.4.0/release_notes.html#airflow-2-4-0-2022-09-19). DAGs that access the same data now have explicit, visible relationships, and DAGs can be scheduled based on updates to these datasets. This feature helps make Airflow data-aware and expands Airflow scheduling capabilities beyond time-based methods such as cron.

Datasets can help resolve common issues. For example, consider a data engineering team with a DAG that creates a dataset and an analytics team with a DAG that analyses the dataset. Using datasets, the data analytics DAG runs only when the data engineering team's DAG publishes the dataset.

In this guide, you'll learn about datasets in Airflow and how to use them to implement triggering of DAGs based on dataset updates. You'll also learn how datasets work with the Astro Python SDK.

## Assumed knowledge

To get the most out of this guide, you should have an existing knowledge of:

- Airflow scheduling concepts. See [Scheduling and Timetables in Airflow](scheduling-in-airflow.md).
- Creating dependencies between DAGs. See [Cross-DAG Dependencies](cross-dag-dependencies.md).
- The Astro Python SDK. See [Using the Astro Python SDK](https://docs.astronomer.io/tutorials/astro-python-sdk).

## Dataset concepts

You can define datasets in your Airflow environment and use them to create dependencies between DAGs. To define a dataset, instantiate the `Dataset` class and provide a string to identify the location of the dataset. This string must be in the form of a valid Uniform Resource Identifier (URI). 

In Airflow 2.4, the URI is not used to connect to an external system and there is no awareness of the content or location of the dataset. However, using this naming convention helps you to easily identify the datasets that your DAG accesses and ensures compatibility with future Airflow features.

The dataset URI is saved as plain text, so it is recommended that you hide sensitive values using environment variables or a secrets backend.

You can reference the dataset in a task by passing it to the task's `outlets` parameter. `outlets` is part of the `BaseOperator`, so it's available to every Airflow operator. 

When you define a task's `outlets` parameter, Airflow labels the task as a producer task that updates the datasets. It is up to you to determine which tasks should be considered producer tasks for a dataset. As long as a task has an outlet dataset, Airflow considers it a producer task even if that task doesn't operate on the referenced dataset. In the following example, Airflow treats both `upstream_task_1` and `upstream_task_2` as producer tasks even though they only run `sleep` in a bash shell.

<CodeBlock language="python">{dataset_upstream1}</CodeBlock>

After a dataset is defined in one or more producer tasks, consumer DAGs in your Airflow environment listen to the producer tasks and run whenever the task completes, rather than running on a time-based schedule. For example, if you have a DAG that should run when `dag1_dataset` and `dag2_dataset` are updated, you define the DAG's schedule using the names of the datasets.

Any task that is scheduled with a dataset is considered a consumer task even if that task doesn't consume the referenced dataset. In other words, it is up to you as the DAG author to correctly reference and use the dataset that the consumer DAG is scheduled on.

<CodeBlock language="python">{dataset_downstream_1_2}</CodeBlock>

Any number of datasets can be provided to the `schedule` parameter as a list. The DAG is triggered after all of the datasets have received at least one update due to a producing task completing successfully. 

When you work with datasets, keep the following considerations in mind:

- Datasets can only be used by DAGs in the same Airflow environment.
- Airflow monitors datasets only within the context of DAGs and tasks. It does not monitor updates to datasets that occur outside of Airflow.
- Consumer DAGs that are scheduled on a dataset are triggered every time a task that updates that dataset completes successfully. For example, if `task1` and `task2` both produce `dataset_a`, a consumer DAG of `dataset_a` runs twice - first when `task1` completes, and again when `task2` completes.
- Consumer DAGs scheduled on a dataset are triggered as soon as the first task with that dataset as an outlet finishes, even if there are downstream producer tasks that also operate on the dataset.
- Scheduling a DAG on a dataset update cannot currently be combined with any other type of schedule. For example, you can't schedule a DAG on an update to a dataset and a timetable.

For more information about datasets, see [Data-aware scheduling](https://airflow.apache.org/docs/apache-airflow/2.4.0/concepts/datasets.html). 

The **Datasets** tab, and the **DAG Dependencies** view in the Airflow UI give you observability for datasets and data dependencies in the DAG's schedule.

On the **DAGs** view, you can see that your `dataset_downstream_1_2` DAG is scheduled on two producer datasets (one in `dataset_upstream1` and `dataset_upstream2`), and its next run is pending one dataset update. At this point the `dataset_upstream` DAG has run and updated its dataset, but the `dataset_upstream2` DAG has not.

![DAGs View](/img/guides/dags_view_dataset_schedule.png)

The **Datasets** tab shows a list of all datasets in your Airflow environment and a graph showing how your DAGs and datasets are connected. You can filter the lists of Datasets by recent updates.

![Datasets View](/img/guides/datasets_view_overview.png)

Click one of the datasets to display a list of task instances that updated the dataset and a highlighted view of that dataset and its connections on the graph.

![Datasets Highlight](/img/guides/datasets_view_highlight.png)

The **DAG Dependencies** view (found under the **Browse** tab) shows a graph of all dependencies between DAGs (in green) and datasets (in orange) in your Airflow environment.

![DAG Dependencies View](/img/guides/dag_dependencies.png)

## Example implementation

In this section you'll learn how datasets and data-aware scheduling can help with a classic ML Ops use case. In this example, it's assumed that two teams are responsible for DAGs that provide data, train a model, and publish the results. 

In this example, a data engineering team has a DAG that sends data to an Amazon S3 bucket and a data science team has another DAG that uses the data to train a Sagemaker model and publish the results to Redshift. 

Using datasets, the data science team can schedule their DAG to run only when the data engineering team's DAG has completed sending the data to the Amazon S3 bucket, ensuring that only the most recent data is used in the model.

The following is an example of the data engineering team's DAG:

<Tabs
    defaultValue="taskflow"
    groupId="example-implementation"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{datasets_ml_example_publish_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{datasets_ml_example_publish_traditional}</CodeBlock>

</TabItem>
</Tabs>



This DAG has a single task, `upload_data_to_s3`, that publishes the data. An outlet dataset is defined in the `@task` decorator using `outlets=Dataset(dataset_uri)` where the dataset URI is defined at the top of the DAG script.

The data science team can then provide that same dataset URI to the `schedule` parameter in their DAG:

<CodeBlock language="python">{datasets_ml_example_consume}</CodeBlock>
 
The dependency between the two DAGs is straightforward to implement and can be viewed alongside the dataset in the Airflow UI.

![ML Example Dependencies](/img/guides/ml_example_dependencies.png)

## Datasets with the Astro Python SDK

If you are using the [Astro Python SDK](https://docs.astronomer.io/tutorials/astro-python-sdk) version 1.1 or later, you do not need to make any code updates to use datasets. Datasets are automatically registered for any functions with output tables and you do not need to define any `outlet` parameters. 

The following example DAG results in three registered datasets: one for each `load_file` function and one for the resulting data from the `transform` function.

<CodeBlock language="python">{example_sdk_datasets}</CodeBlock>

![SDK datasets](/img/guides/sdk_datasets.png)
