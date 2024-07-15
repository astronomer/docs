---
title: "Introduction to Apache Airflow® DAGs"
sidebar_label: "DAGs"
id: dags
description: "Learn how to write DAGs and get tips on how to define an Apache Airflow® DAG in Python. Learn all about DAG parameters and their settings."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import example_astronauts_three_tasks from '!!raw-loader!../code-samples/dags/dags/example_astronauts_three_tasks.py';
import complex_dag_structure from '!!raw-loader!../code-samples/dags/dags/complex_dag_structure.py';

In Apache Airflow®, a **DAG** is a data pipeline or workflow. DAGs are the main organizational unit in Airflow; they contain a collection of tasks and dependencies that you want to execute on a schedule. 

A DAG is defined in Python code and visualized in the Airflow UI. DAGs can be as simple as a single task or as complex as hundreds or thousands of tasks with complicated dependencies.

The following screenshot shows a [complex DAG graph](#example-complex-dag-run) in the Apache Airflow® UI. After reading this guide, you'll be able to understand the elements in this graph, as well as know how to define DAGs and use DAG parameters.

![Screenshot from the Graph tab of the Apache Airflow® UI of a complex DAG with dynamically mapped tasks, task groups and setup/teardown tasks.](/img/guides/dags_complex_DAG.png)

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Apache Airflow®: DAGs 101](https://academy.astronomer.io/path/airflow-101/dag-101-1) module.

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- What Airflow is. See [Introduction to Apache Airflow®](intro-to-airflow.md).

## What is a DAG?

A _DAG_ (directed acyclic graph) is a mathematical structure consisting of nodes and edges. In Airflow, a DAG represents a data pipeline or workflow with a start and an end.

The mathematical properties of DAGs make them useful for building data pipelines:

- **Directed**: There is a clear direction of flow between tasks. A task can be either upstream, downstream, or parallel to another task.

    ![Visualization of two graphs with 3 nodes each. The first graph is directed, the arrow in between the nodes always points into one direction. The second graph is not directed, the arrow between the second and third node points in both directions. Only the first graph would be possible to define in Apache Airflow®.](/img/guides/dags_directed_vs_not_directed.png)

- **Acyclic**: There are no circular dependencies in a DAG. This means that a task cannot depend on itself, nor can it depend on a task that ultimately depends on it.

    ![Visualization of two graphs with 4 nodes each. The first graph is acyclic, there are no circles defined between the nodes. In the second graph a dependency is added between task 4 and task 1, meaning task 1 depends on task 4. This creates a circle because task 4 is downstream of task 1. Only the first graph would be possible to define in Apache Airflow®.](/img/guides/dags_acyclic_vs_cyclic.png)

- **Graph**: A DAG is a graph, which is a structure consisting of nodes and edges. In Airflow, nodes are tasks and edges are dependencies between tasks. Defining workflows as graphs helps you visualize the entire workflow in a way that's easy to navigate and conceptualize.

Beyond these requirements, a DAG can be as simple or as complicated as you need! You can define tasks that run in parallel or sequentially, implement conditional branches, and visually group tasks together in [task groups](task-groups.md).

Each task in a DAG performs one unit of work. Tasks can be anything from a simple Python function to a complex data transformation or a call to an external service. They are defined using [Apache Airflow® operators](what-is-an-operator.md) or [Apache Airflow® decorators](airflow-decorators.md). The dependencies between tasks can be set in different ways (see [Managing Dependencies](managing-dependencies.md)).

The following screenshot shows a simple DAG graph with 3 sequential tasks.  

![Screenshot of the Apache Airflow® UI showing the Grid view with the Graph tab selected. A simple DAG is shown with 3 sequential tasks, get_astronauts, print_astronaut_craft (which is a dynamically mapped task) and print_reaction.](/img/guides/dags_simple_dag_graph.png)

<details>
<summary>Click to view the full DAG code used to create the DAG in the screenshot</summary>
<div>
    <div><CodeBlock language="python">{example_astronauts_three_tasks}</CodeBlock></div>
</div>
</details>

## What is a DAG run?

A _DAG run_ is an instance of a DAG running at a specific point in time. A _task instance_, also known as a task run, is an instance of a task running at a specific point in time. Each DAG run has a unique `dag_run_id` and contains one or more task instances. The history of previous DAG runs is stored in the [Apache Airflow® metadata database](airflow-database.md).

In the Airflow UI, you can view previous runs of a DAG in the **Grid** view and select individual DAG runs by clicking on their respective duration bar. A DAG run graph looks similar to the DAG graph, but includes additional information about the status of each task instance in the DAG run.

![Screenshot of the Apache Airflow® UI showing the Grid view with the Graph tab selected. A simple DAG run is shown with 3 successful sequential tasks, get_astronauts, print_astronaut_craft (which is a dynamically mapped task with 7 mapped task instances) and print_reaction.](/img/guides/dags_simple_dag_run_graph.png)

### DAG run properties

A DAG run graph in the Airflow UI contains information about the DAG run, as well as the status of each task instance in the DAG run. The following screenshot shows the same DAG as in the previous section, but with annotations explaining the different elements of the graph.

![Screenshot of the Apache Airflow® UI showing the Grid view with the Graph tab selected. A DAG run with 3 tasks is shown. The annotations show the location of the dag_id and logical date (top of the screenshot), the task_id, task state and operator/decorator used in the nodes of the graph, as well as the number of dynamically mapped task instances in [] behind the task id and the DAG dependency layout to the right of the screen.](/img/guides/dags_simple_dag_run_graph_annotated.png)

- `dag_id`: The unique identifier of the DAG.
- `logical date`: The point in time for which the DAG run is scheduled. This date and time is not necessarily the same as the actual moment the DAG run is executed. See [Scheduling](scheduling-in-airflow.md) for more information.
- `task_id`: The unique identifier of the task.
- `task state`: The status of the task instance in the DAG run. Possible states are `running`, `success`, `failed`, `skipped`, `restarting`, `up_for_retry`, `upstream_failed`, `queued`, `scheduled`, `none`, `removed`, `deferred`, and `up_for_reschedule`, they each cause the border of the node to be colored differently. See the OSS documentation on [task instances](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#task-instances) for an explanation of each state.

The previous screenshot also shows the four common ways you can trigger a DAG run:

- **Backfill**: The first DAG run was created using a [backfill](rerunning-dags.md#backfill). Backfilled DAG runs include a curved arrow on their DAG run duration bar.
- **Scheduled**: The second DAG run, which is currently selected in the screenshot, was created by the Airflow scheduler based on the DAG's defined schedule. This is the default method for running DAGs.
- **Manual**: The third DAG run was triggered manually by a user using the Airflow UI or the Airflow CLI. Manually triggered DAG runs include a play icon on the DAG run duration bar.
- **Dataset triggered**: The fourth DAG run was started by a [dataset](airflow-datasets.md). DAG runs triggered by a dataset include a dataset icon on their DAG run duration bar.

A DAG run can have the following statuses:

- **Queued**: The time after which the DAG run can be created has passed but the scheduler has not created task instances for it yet.
- **Running**: The DAG run is eligible to have task instances scheduled.
- **Success**: All task instances are in a terminal state (`success`, `skipped`, `failed` or `upstream_failed`) and all leaf tasks (tasks with no downstream tasks) are either in the state `success` or `skipped`. In the previous screenshot, all four DAG runs were successful.
- **Failed**: All task instances are in a terminal state and at least one leaf task is in the state `failed` or `upstream_failed`.

### Complex DAG runs

When you start writing more complex DAGs, you will see additional Airflow features that are visualized in the DAG run graph. The following screenshot shows the same complex DAG as in the overview but with annotations explaining the different elements of the graph. Don't worry if you don't know about all these features yet - you will learn about them as you become more familiar with Airflow.

![Screenshot of the Apache Airflow® UI showing the Grid view with the Graph tab selected. A DAG run of a complex DAG is shown with annotations showing a dynamically mapped task, a branching task, an edge label, a dynamically mapped task group, regular task groups, setup/ teardown tasks as well as a Dataset.](/img/guides/dags_complex_DAG_annotated.png)

<details>
<summary>Click to view the full DAG code used for the screenshot</summary>
<div>
    <div>
    The following code creates the same DAG structure as shown in the previous screenshot. Note that custom operators have been replaced with the BashOperator and EmptyOperator to make it possible to run the DAG without additional setup.
    <CodeBlock language="python">{complex_dag_structure}</CodeBlock>
    </div>
</div>
</details>

Some more complex features visible in this DAG graph are:

- **Dynamically mapped tasks**: A dynamically mapped task is [created dynamically](dynamic-tasks.md) at runtime based on user-defined input. The number of dynamically mapped task instances is shown in brackets (`[]`) behind the task ID.
- **Branching tasks**: A branching task creates a conditional branch in the DAG. See [Branching in Apache Airflow®](airflow-branch-operator.md) for more information.
- **Edge labels**: Edge labels appear on the edge between two tasks. These labels are often helpful to annotate branch decisions in a DAG graph. 
- **Task groups**: A task group is a tool to logically and visually group tasks in an Airflow DAG. See [Apache Airflow® task groups](task-groups.md) for more information.
- **Setup/teardown tasks**: When using Airflow to manage infrastructure, it can be helpful to define tasks as setup and teardown tasks to take advantage of additional intelligent dependency behavior. Setup and teardown tasks appear with diagonal arrows next to their task IDs and are connected with a dotted line. See [Use setup and teardown tasks in Apache Airflow®](airflow-setup-teardown.md) for more information.
- **Datasets**: Datasets are shown in the DAG graph. If a DAG is scheduled on a dataset, it is shown upstream of the first task of the DAG. If a task in the DAG updates a dataset, it is shown after the respective task as in the previous screenshot. See [Apache Airflow® datasets](airflow-datasets.md) for more information.

You can learn more about how to set complex dependencies between tasks and task groups in the [Managing Dependencies](managing-dependencies.md) guide.

## Write a DAG

A DAG can be defined with a Python file placed in an Airflow project's `DAG_FOLDER`, which is `dags` when using the [Astro CLI](https://www.astronomer.io/docs/astro/cli/get-started-cli). Airflow automatically parses all files in this folder every 5 minutes to check for new DAGs, and it parses existing DAGs for code changes every 30 seconds. You can force a new DAG parse using [`airflow dags reserialize`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#reserialize), or `astro dev run dags reserialize` using the Astro CLI.

There are two types of syntax you can use to structure your DAG:

- **TaskFlow API**: The TaskFlow API contains the `@dag` decorator. A function decorated with `@dag` defines a DAG. Note that you need to call the function at the end of the script for Airflow to register the DAG. All tasks are defined within the context of the DAG function.
- **Traditional syntax**: You can create a DAG by instantiating a DAG context using the `DAG` class and defining tasks within that context.

TaskFlow API and traditional syntax can be freely mixed. See [Mixing TaskFlow decorators with traditional operators](airflow-decorators.md#mixing-taskflow-decorators-with-traditional-operators) for more information. 

The following is an example of the same DAG written using each type of syntax.

<Tabs
    defaultValue="taskflow"
    groupId= "writing-dags-with-the-taskflow-api"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
# Import all packages needed at the top level of the DAG
from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from pendulum import datetime


# Define the DAG function a set of parameters
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
)
def taskflow_dag():
    # Define tasks within the DAG context
    @task
    def my_task_1():
        import time  # import packages only needed in the task function
        time.sleep(5)
        print(1)

    @task
    def my_task_2():
        print(2)

    # Define dependencies and call task functions
    chain(my_task_1(), my_task_2())

# Call the DAG function
taskflow_dag()

```

</TabItem>

<TabItem value="traditional">

```python
# Import all packages needed at the top level of the DAG
from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime


def my_task_1_func():
    import time  # import packages only needed in the task function

    time.sleep(5)
    print(1)


# Instantiate the DAG
with DAG(
    dag_id="traditional_syntax_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
):
    # Instantiate tasks within the DAG context
    my_task_1 = PythonOperator(
        task_id="my_task_1",
        python_callable=my_task_1_func,
    )

    my_task_2 = PythonOperator(
        task_id="my_task_2",
        python_callable=lambda: print(2),
    )

    # Define dependencies
    my_task_1 >> my_task_2
```

</TabItem>
</Tabs>

:::tip

Astronomer recommends creating one Python file for each DAG and naming it after the `dag_id` as a best practice for organizing your Airflow project. For certain advanced use cases it may be appropriate to dynamically generate DAGs using Python code, see [Dynamically generate DAGs in Apache Airflow®](dynamically-generating-dags.md) for more information.

:::

### DAG-level parameters

In Airflow, you can configure when and how your DAG runs by setting parameters in the DAG object. DAG-level parameters affect how the entire DAG behaves, as opposed to task-level parameters which only affect a single task.

The DAGs in the previous section have the following basic parameters defined. It's best practice to always define these parameters for any DAGs you create:

- `dag_id`: The name of the DAG. This must be unique for each DAG in the Airflow environment. When using the `@dag` decorator and not providing the `dag_id` parameter name, the function name is used as the `dag_id`.
- `start_date`: The date and time after which the DAG starts being scheduled.
- `schedule`: The schedule for the DAG. There are many different ways to define a schedule, see [Scheduling in Apache Airflow®](scheduling-in-airflow.md) for more information.
- `catchup`: Whether the scheduler should [backfill all missed DAG runs](rerunning-dags.md#catchup) between the current date and the start date when the DAG is unpaused. It is a best practice to always set it to `False` unless you specifically want to backfill missed DAG runs.

There are many more DAG-level parameters that let you configure anything from resource usage to the DAG's appearance in the Airflow UI. See [DAG-level parameters](airflow-dag-parameters.md) for a complete list.

## See also 

- [Get started with Apache Airflow®](get-started-with-airflow.md) tutorial for a hands-on introduction to writing your first simple DAG.
- [Apache Airflow® operators](what-is-an-operator.md) and [Introduction to the TaskFlow API and Apache Airflow® decorators](airflow-decorators.md) for more information on how to define tasks in a DAG.
- [Intro to Apache Airflow®: Get Started Writing Pipelines for Any Use Case](https://www.astronomer.io/events/webinars/intro-to-airflow-get-started-writing-pipelines-for-any-use-case-video/) webinar for a one-hour webinar introducing Airflow and how to write DAGs.