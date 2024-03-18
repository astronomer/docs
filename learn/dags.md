---
title: "Introduction to Airflow DAGs"
sidebar_label: "DAGs"
id: dags
description: "Learn how to write DAGs and get tips on how to define an Airflow DAG in Python. Learn all about DAG parameters and their settings."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import example_astronauts_three_tasks from '!!raw-loader!../code-samples/dags/dags/example_astronauts_three_tasks.py';
import complex_dag_structure from '!!raw-loader!../code-samples/dags/dags/complex_dag_structure.py';

In Airflow, a **DAG** is a data pipeline or workflow. DAGs are the main organizational unit in Airflow, they contain a collection of tasks with defined dependencies between them that you want to execute on a schedule. An Airflow DAG is defined in Python code and visualized in the Airflow UI. DAGs can be as simple as a single task or as complex as hundreds or thousands of tasks with complicated dependencies.

The following screenshot shows a [complex DAG graph](#example-complex-dag-run) in the Airflow UI. After reading this guide, you'll be able to understand the elements of this graph, as well as know how to define DAGs and use DAG parameters.

![Screenshot from the Graph tab of the Airflow UI of a complex DAG with dynamically mapped tasks, task groups and setup/teardown tasks.](/img/guides/dags_complex_DAG.png)

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Airflow: DAGs 101](https://academy.astronomer.io/dag-101-1) module.

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## What is a DAG?

A **DAG** is a **directed acyclic graph**, a mathematical structure consisting of nodes and edges. In Airflow, a DAG represents the unit of one data pipeline or workflow.
Within an Airflow DAG, each node represents a task and each edge represents a dependency between tasks. Each DAG has a unique `dag_id`.

The mathematical properties of DAGs make them useful for building data pipelines:

- **Directed**: There is a clear direction of flow between tasks. A task can either be upstream, downstream, or parallel to another task.

    ![Visualization of two graphs with 3 nodes each. The first graph is directed, the arrow in between the nodes always points into one direction. The second graph is not directed, the arrow between the second and third node points in both directions. Only the first graph would be possible to define in Airflow.](/img/guides/dags_directed_vs_not_directed.png)

- **Acyclic**: There cannot be any circular dependencies in your DAG. This means that a task cannot depend on itself, nor can it depend on a task that ultimately depends on it.

    ![Visualization of two graphs with 4 nodes each. The first graph is acyclic, there are no circles defined between the nodes. In the second graph a dependency is added between task 4 and task 1, meaning task 1 depends on task 4. This creates a circle because task 4 is downstream of task 1. Only the first graph would be possible to define in Airflow.](/img/guides/dags_acyclic_vs_cyclic.png)

Aside from these requirements, DAGs in Airflow can be as complicated as you need! You can define tasks that run in parallel or sequentially, implement conditional branches, and visually group tasks together in [task groups](task-groups.md).

Each task in a DAG performs one unit of work. Tasks can be anything from a simple Python function to a complex data transformation or a call to an external service. They are defined using [Airflow operators](what-is-an-operator.md) or [Airflow decorators](airflow-decorators.md). The dependencies between tasks can be set in different ways, see [Managing Dependencies](managing-dependencies.md).

The following screenshot shows a simple DAG graph with 3 sequential tasks.  

![Screenshot of the Airflow UI showing the Grid view with the Graph tab selected. A simple DAG is shown with 3 sequential tasks, get_astronauts, print_astronaut_craft (which is a dynamically mapped task) and print_reaction.](/img/guides/dags_simple_dag_graph.png)

<details>
<summary>Click to view the full DAG code used to create the DAG in the screenshot</summary>
<div>
    <div><CodeBlock language="python">{example_astronauts_three_tasks}</CodeBlock></div>
</div>
</details>

## What is a DAG run?

An instance of a DAG running at a specific point in time is called a **DAG run**. An instance of a task running at a specific point in time is called a **task instance**. Each DAG run has a unique `dag_run_id` and contains one or more task instances. The history of previous DAG runs is stored in the [Airflow metadata database](airflow-database.md).

In the Airflow UI you can view previous runs of a DAG in the Grid view and select individual DAG runs by clicking on the respective duration bar. The DAG run graph looks similar to the DAG graph with additional information about the status of each task instance in the DAG run.

![Screenshot of the Airflow UI showing the Grid view with the Graph tab selected. A simple DAG run is shown with 3 successful sequential tasks, get_astronauts, print_astronaut_craft (which is a dynamically mapped task with 7 mapped task instances) and print_reaction.](/img/guides/dags_simple_dag_run_graph.png)

### DAG run properties

A DAG run graph in the Airflow UI contains information about the DAG run, as well as the status of each task instance in the DAG run. The following screenshot shows the same simple DAG as in the previous section but with annotations explaining the different elements of the graph.

![Screenshot of the Airflow UI showing the Grid view with the Graph tab selected. A DAG run with 3 tasks is shown. The annotations show the location of the dag_id and logical date (top of the screenshot), the task_id, task state and operator/decorator used in the nodes of the graph, as well as the number of dynamically mapped task instances in [] behind the task id and the DAG dependency layout to the right of the screen.](/img/guides/dags_simple_dag_run_graph_annotated.png)

- `dag_id`: The unique identifier of the DAG.
- `logical date`: The point in time for which the DAG run is scheduled. This date and time is not necessarily the same as the actual moment the DAG run is executed. See [Scheduling](scheduling-in-airflow.md) for more information.
- `task_id`: The unique identifier of the task.
- `task state`: The status of the task instance in the DAG run. Possible states are `running`, `success`, `failed`, `skipped`, `restarting`, `up_for_retry`, `upstream_failed`, `queued`, `scheduled`, `none`, `removed`, `deferred`, and `up_for_reschedule`, they each cause the border of the node to be colored differently. See the OSS documentation on [task instances](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#task-instances) for an explanation of each state.

The previous screenshot shows 4 successful DAG runs, one for each DAG run type:

- **backfill**: The first DAG run shown was created by a [backfill](rerunning-dags.md#backfill). You can see an arrow on the DAG run bar.
- **scheduled**: The second DAG run was created by the Airflow scheduler based on the DAG's defined schedule. This DAG run bar has no additional icon and is the DAG run selected in the screenshot.
- **manual**: The third DAG run was started manually by a user in the Airflow UI or using the Airflow CLI. You can see a play icon on the DAG run bar.
- **dataset_triggered**: The fourth DAG run was started by a [dataset](airflow-datasets.md). You can see a dataset icon on the DAG run bar.

A DAG run can have the following statuses:

- `queued`: The time after which the DAG run can be created has passed but the scheduler has not created task instances for it yet.
- `running`: The DAG run is eligible to have task instances scheduled.
- `success`: All task instances are in a terminal state (`success`, `skipped`, `failed` or `upstream_failed`) and all leaf tasks (tasks with no downstream tasks) are either in the state `success` or `skipped`. All 4 DAG runs in the screenshot are in the state `success`.
- `failed`: All task instances are in a terminal state and at least one leaf task is in the state `failed` or `upstream_failed`.

### Example complex DAG run

Once you start writing more complex DAGs, you will see additional elements of different Airflow features that are visualized in the DAG run graph. The following screenshot shows the same complex DAG as in the first section but with annotations explaining the different elements of the graph. Don't worry if you don't know about all these features yet, you will learn about them as you become more familiar with Airflow.

![Screenshot of the Airflow UI showing the Grid view with the Graph tab selected. A DAG run of a complex DAG is shown with annotations showing a dynamically mapped task, a branching task, an edge label, a dynamically mapped task group, regular task groups, setup/ teardown tasks as well as a Dataset.](/img/guides/dags_complex_DAG_annotated.png)

<details>
<summary>Click to view the full DAG code used for the Screenshot</summary>
<div>
    <div>
    The following code creates the same DAG structure as shown in the previous screenshot. Note that custom operators have been replaced with the BashOperator and EmptyOperator to make it possible to run the DAG without additional setup.
    <CodeBlock language="python">{complex_dag_structure}</CodeBlock>
    </div>
</div>
</details>

- **Dynamically mapped task**: A task that is [dynamically created](dynamic-tasks.md) at runtime based on changing user defined input. The number of task instances is shown in `[]` behind the task id. Task groups can also be [dynamically mapped](task-groups#generate-task-groups-dynamically-at-runtime).
- **Branching task**: A task that creates a conditional branch in the DAG. See [Branching in Airflow](airflow-branch-operator.md) for more information.
- **Edge label**: A label on the edge between two tasks. These labels are often helpful to annotate branch decisions in a DAG graph. 
- **Task group**: A task group is a tool to logically and visually group tasks in an Airflow DAG. See [Airflow task groups](task-groups.md) for more information.
- **Setup/teardown tasks**: When using Airflow to manage infrastructure it can be helpful to define tasks as setup and teardown tasks to take advantage of additional intelligent dependency behavior. You can recognize setup and teardown tasks by little arrows next to the task id in the task node and the dotted line connecting them. See [Use setup and teardown tasks in Airflow](airflow-setup-teardown.md) for more information.
- **Dataset**: Datasets are shown in the DAG graph. If a DAG is scheduled on a dataset, it is shown upstream of the first task of the DAG. If a task in the DAG updates a dataset, it is shown after the respective task as in the previous screenshot. See [Airflow datasets](airflow-datasets.md) for more information.

You can learn more about how to set complex dependencies between tasks and task groups in the [Managing Dependencies](managing-dependencies.md) guide.

## Write a DAG

DAGs in Airflow are defined in a Python script that is placed in an Airflow project's `DAG_FOLDER`, which is `dags/` when using the [Astro CLI](https://docs.astronomer.io/astro/cli/get-started-cli). Airflow automatically parses all files in this folder to load any new DAGs every 5 minutes and update any existing DAGs every 30 seconds. You can force a new parsing of the DAGs by running `astro dev run dags reserialize` ([`airflow dags reserialize`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#reserialize)).

There are two main ways to define a DAG:

- **TaskFlow API**: The TaskFlow API contains the `@dag` decorator. A function decorated with `@dag` defines a DAG. Note that you need to call the function at the end of the script for Airflow to register the DAG. All tasks are defined within the context of the DAG function.
- **Traditional syntax**: You can create a DAG by instantiating a DAG context using the `DAG` class and defining tasks within that context.

TaskFlow API and traditional syntax can be freely mixed, see [Mixing TaskFlow decorators with traditional operators](airflow-decorators.md#mixing-taskflow-decorators-with-traditional-operators) for more information.

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

Astronomer recommends creating one Python file for each DAG and naming it after the `dag_id` as a best practice for organizing your Airflow project. At scale it is common to dynamically generate DAGs using Python code, see [Dynamically generate DAGs in Airflow](dynamically-generating-dags.md) for more information.

:::

### DAG-level parameters

In Airflow, you can configure when and how your DAG runs by setting parameters in the DAG object. DAG-level parameters affect how the entire DAG behaves, as opposed to task-level parameters which only affect a single task. The DAGs in the previous section have the following parameters defined:

- `dag_id`: The name of the DAG. This must be unique for each DAG in the Airflow environment. When using the `@dag` decorator and not providing the `dag_id` parameter name, the function name is used as the `dag_id`. When using the `DAG` class, this parameter is required.
- `start_date`: The date and time after which the DAG starts being scheduled. Note that the first actual run of the DAG may be later than this date depending on how you define the schedule. See [DAG scheduling and timetables in Airflow](scheduling-in-airflow.md) for more information. This parameter may be required depending on your Airflow version and `schedule`.
- `schedule`: The schedule for the DAG. There are many different ways to define a schedule, see [Scheduling in Airflow](scheduling-in-airflow.md) for more information. Defaults to `timedelta(days=1)`.
- `catchup`: Whether the scheduler should backfill all missed DAG runs between the current date and the start date when the DAG is unpaused. This parameter defaults to `True`. It is a best practice to always set it to `False` unless you specifically want to backfill missed DAG runs, see [Catchup](rerunning-dags.md#catchup) for more information.

There are many additional parameters that can be set on the DAG object. 

Some parameters relate to adding information to the DAG or change its appearance in the **Airflow UI**:

- `description`: A short string that is displayed in the Airflow UI next to the DAG name.
- `doc_md`: A string that is rendered as [DAG documentation](custom-airflow-ui-docs-tutorial.md) in the Airflow UI. Tip: use `__doc__` to use the docstring of the Python file.
- `owner_links`: A dictionary with the key being the DAG owner and the value being a URL to link to when clicking on the owner in the Airflow UI. Commonly used as a mailto link to the owner's email address. Note that the `owner` parameter is set at the task level, usually by defining it in the `default_args` dictionary.
- `tags`: A list of tags shown in the Airflow UI to help with filtering DAGs.
- `default_view`: The default view of the DAG in the Airflow UI. Defaults to `grid`.
- `orientation`: The orientation of the DAG graph in the Airflow UI. Defaults to `LR` (left to right).

There are parameters that relate to **Jinja templating**, such as:

- `template_searchpath`: A list of folders where [Jinja](templating.md) looks for templates. The path of the DAG file is included by default.
- `render_template_as_native_obj`: Whether to render Jinja templates as native Python objects instead of strings. Defaults to `False`.
- `user_defined_macros`: A dictionary of macros that are available in the DAG's Jinja templates. Use `user_defined_filters` to add filters and `jinja_environment_kwargs` for additional Jinja configuration. See [Macros: using custom functions and variables in templates](templating.md#macros-using-custom-functions-and-variables-in-templates).

Two other helpful parameters relate to **scaling** in Airflow. For more information see [Scaling Airflow to optimize performance](airflow-scaling-workers.md):

- `max_active_tasks`: The number of task instances allowed to run concurrently for all DAG runs of this DAG.
- `max_active_runs`: The number of active DAG runs allowed to run concurrently for this DAG.

Other DAG parameters include:

- `end_date`: The date beyond which no further DAG runs will be scheduled. Defaults to `None`.
- `default_args`: A dictionary of parameters that are applied to all tasks in the DAG. These parameters are passed directly to each operator, so they must be parameters that are part of the [`BaseOperator`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html). You can override default arguments at the task level.
- `params`: A dictionary of DAG-level Airflow params. See [Airflow params](airflow-params.md) for more information.
- `dagrun_timeout`: The time it takes for a DAG run of this DAG to time out and be marked as `failed`.
- `access_control`: Specify optional permissions for roles specific to an individual DAG. See [DAG-level permissions](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html#dag-level-permissions). Astronomer recommends customers to use [Astro's RBAC features](https://docs.astronomer.io/astro/user-permissions) instead.
- `is_paused_upon_creation`: Whether the DAG is paused when it is created. When not set, the Airflow config `core.dags_are_paused_at_creation` is used, which defaults to `True`.
- `fail_stop`: In Airflow 2.7+ you can set this parameter to `True` to stop DAG execution as soon as one task in this DAG fails. Any tasks that are still running are marked as `failed` and any tasks that have not run yet are marked as `skipped`. Note that you cannot have any [trigger rule](managing-dependencies.md#trigger-rules) other than `all_success` in a DAG with `fail_stop` set to `True`.

Additionally you can set DAG-level callbacks in the DAG definition, see [DAG-level callbacks](error-notifications-in-airflow.md#airflow-callbacks) for more information.

## See also 

- [Get started with Apache Airflow](get-started-with-airflow.md) tutorial for a hands-on introduction to writing your first simple DAG.
- [Introduction to Apache Airflow](intro-to-airflow.md) for an overview of Airflow concepts.
- [Airflow operators](what-is-an-operator.md) and [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md) for more information on how to define tasks in a DAG.