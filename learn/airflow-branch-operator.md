---
title: "Branching in Airflow"
sidebar_label: "Branches"
id: airflow-branch-operator
---

<head>
  <meta name="description" content="Learn about Airflow’s multiple options for building conditional logic and branching within DAGs, including the BranchPythonOperator and ShortCircuitOperator." />
  <meta name="og:description" content="Learn about the options available in Airflow for building conditional logic and branching within DAGs, including the BranchPythonOperator and ShortCircuitOperator." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

When designing your data pipelines, you may encounter use cases that require more complex task flows than "Task A > Task B > Task C". For example, you may have a use case where you need to decide between multiple tasks to execute based on the results of an upstream task. Or you may have a case where part of your pipeline should only run under certain external conditions. Fortunately, Airflow has multiple options for building conditional logic and/or branching into your DAGs.

In this guide, you'll learn how you can use `@task.branch` (BranchPythonOperator) and `@task.short_circuit` (ShortCircuitOperator), other available branching operators, and additional resources to implement conditional logic in your Airflow DAGs.

:::tip Related content

Other ways to learn:

- Astronomer Academy: [Airflow: Branching](https://academy.astronomer.io/astro-runtime-branching) module.

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Dependencies in Airflow. See [Managing Dependencies in Apache Airflow](managing-dependencies.md).
- Using Airflow decorators. See [Introduction to Airflow decorators](airflow-decorators.md).

## `@task.branch` (BranchPythonOperator)

One of the simplest ways to implement branching in Airflow is to use the `@task.branch` decorator, which is a decorated version of the [BranchPythonOperator](https://registry.astronomer.io/providers/apache-airflow/modules/branchpythonoperator). `@task.branch` accepts any Python function as an input as long as the function returns a list of valid IDs for Airflow tasks that the DAG should run after the function completes. 

In the following example we use a `choose_branch` function that returns one set of task IDs if the result is greater than 0.5 and a different set if the result is less than or equal to 0.5:

<Tabs
    defaultValue="taskflow"
    groupId="taskbranch-branchpythonoperator"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
result = 1

@task.branch
def choose_branch(result):
    if result > 0.5:
        return ['task_a', 'task_b']
    return ['task_c']

choose_branch(result)
```

</TabItem>

<TabItem value="traditional">

```python
result = 1

def choose_branch(result):
    if result > 0.5:
        return ['task_a', 'task_b']
    return ['task_c']

branching = BranchPythonOperator(
    task_id='branching',
    python_callable=choose_branch,
    op_args=[result]
)
```

</TabItem>
</Tabs>

In general, the `@task.branch` decorator is a good choice if your branching logic can be easily implemented in a simple Python function. Whether you want to use the decorated version or the traditional operator is a question of personal preference.

The code below shows a full example of how to use `@task.branch` in a DAG:

<Tabs
    defaultValue="taskflow"
    groupId= "taskbranch-branchpythonoperator"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
"""Example DAG demonstrating the usage of the `@task.branch`
TaskFlow API decorator."""

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.utils.edgemodifier import Label

import random
from pendulum import datetime


@dag(
    start_date=datetime(2023, 1, 1),
    catchup=False,
    schedule="@daily"
)
def branch_python_operator_decorator_example():

    run_this_first = EmptyOperator(task_id="run_this_first")

    options = ["branch_a", "branch_b", "branch_c", "branch_d"]

    @task.branch(task_id="branching")
    def random_choice(choices):
        return random.choice(choices)

    random_choice_instance = random_choice(choices=options)

    run_this_first >> random_choice_instance

    join = EmptyOperator(
        task_id="join",
        trigger_rule="none_failed_min_one_success"
    )

    for option in options:

        t = EmptyOperator(
            task_id=option
        )

        empty_follow = EmptyOperator(
            task_id="follow_" + option
        )

        # Label is optional here, but it can help identify more complex branches
        random_choice_instance >> Label(option) >> t >> empty_follow >> join


branch_python_operator_decorator_example()
```

</TabItem>

<TabItem value="traditional">

```python
"""Example DAG demonstrating the usage of the BranchPythonOperator."""

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.edgemodifier import Label

import random
from pendulum import datetime

with DAG(
    dag_id='branch_python_operator_example',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    schedule="@daily"
) as dag:

    run_this_first = EmptyOperator(
        task_id='run_this_first',
    )

    options = ['branch_a', 'branch_b', 'branch_c', 'branch_d']

    branching = BranchPythonOperator(
        task_id='branching',
        python_callable=lambda: random.choice(options),
    )

    run_this_first >> branching

    join = EmptyOperator(
        task_id='join',
        trigger_rule="none_failed_min_one_success",
    )

    for option in options:

        t = EmptyOperator(
            task_id=option,
        )

        empty_follow = EmptyOperator(
            task_id='follow_' + option,
        )

        # Label is optional here, but it can help identify more complex branches
        branching >> Label(option) >> t >> empty_follow >> join
```

</TabItem>
</Tabs>

In this DAG, `random.choice()` returns one random option out of a list of four branches. In the following screenshot, where `branch_b` was randomly chosen, the two tasks in `branch_b` were successfully run while the others were skipped.

![Branching Graph View](/img/guides/branching_decorator_graph.png)

If you have downstream tasks that need to run regardless of which branch is taken, like the `join` task in the previous example, you need to update the trigger rule. The default trigger rule in Airflow is `all_success`, which means that if upstream tasks are skipped, then the downstream task will not run. In the previous example, `none_failed_min_one_success` is specified to indicate that the task should run as long as one upstream task succeeded and no tasks failed.

Finally, note that with the `@task.branch` decorator your Python function *must* return at least one task ID for whichever branch is chosen (i.e. it can't return nothing). If one of the paths in your branching should do nothing, you can use an EmptyOperator in that branch.

:::info

More examples using the `@task.branch` decorator, can be found on the [Astronomer Registry](https://legacy.registry.astronomer.io/dags/example-branch-python-dop-operator-3).

:::

## `@task.short_circuit` (ShortCircuitOperator)

Another option for implementing conditional logic in your DAGs is the `@task.short_circuit` decorator, which is a decorated version of the [ShortCircuitOperator](https://registry.astronomer.io/providers/apache-airflow/modules/shortcircuitoperator). This operator takes a Python function that returns `True` or `False` based on logic implemented for your use case. If `True` is returned, the DAG continues, and if `False` is returned, all downstream tasks are skipped.

`@task.short_circuit` is useful when you know that some tasks in your DAG should run only occasionally. For example, maybe your DAG runs daily, but some tasks should only run on Sundays. Or maybe your DAG orchestrates a machine learning model, and tasks that publish the model should only be run if a certain accuracy is reached after training. This type of logic can also be implemented with `@task.branch`, but that operator requires a task ID to be returned. Using the `@task.short_circuit` decorator can be cleaner in cases where the conditional logic equates to "run or not" as opposed to "run this or that".

The following DAG shows an example of how to implement `@task.short_circuit`:

<Tabs
    defaultValue="taskflow"
    groupId= "taskshort_circuit-shortcircuitoperator"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

```python
"""Example DAG demonstrating the usage of the @task.short_circuit decorator."""

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator

from pendulum import datetime


@dag(
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
)
def short_circuit_operator_decorator_example():

    @task.short_circuit
    def condition_is_True():
        return True

    @task.short_circuit
    def condition_is_False():
        return False

    ds_true = [EmptyOperator(task_id='true_' + str(i)) for i in [1, 2]]
    ds_false = [EmptyOperator(task_id='false_' + str(i)) for i in [1, 2]]

    chain(condition_is_True(), *ds_true)
    chain(condition_is_False(), *ds_false)


short_circuit_operator_decorator_example()
```

</TabItem>

<TabItem value="traditional">

```python
"""Example DAG demonstrating the usage of the ShortCircuitOperator."""

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import ShortCircuitOperator

from pendulum import datetime

with DAG(
    dag_id='short_circuit_operator_example',
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    cond_true = ShortCircuitOperator(
        task_id='condition_is_True',
        python_callable=lambda: True,
    )

    cond_false = ShortCircuitOperator(
        task_id='condition_is_False',
        python_callable=lambda: False,
    )

    ds_true = [EmptyOperator(task_id='true_' + str(i)) for i in [1, 2]]
    ds_false = [EmptyOperator(task_id='false_' + str(i)) for i in [1, 2]]

    chain(cond_true, *ds_true)
    chain(cond_false, *ds_false)
```

</TabItem>
</Tabs>

In this DAG there are two short circuits, one which always returns `True` and one which always returns `False`. When you run the DAG, you can see that tasks downstream of the `True` condition operator ran, while tasks downstream of the `False` condition operator were skipped.

![Short Circuit](/img/guides/short_circuit_decorator_graph.png)

:::info

Another example using the ShortCircuitOperator, can be found on the [Astronomer Registry](https://legacy.registry.astronomer.io/dags/example-short-circuit-operator).

:::

## Other branch operators

Airflow offers a few other branching operators that work similarly to the BranchPythonOperator but for more specific contexts: 

- [BranchSQLOperator](https://registry.astronomer.io/providers/apache-airflow-providers-common-sql/modules/branchsqloperator): Branches based on whether a given SQL query returns `true` or `false`.
- [BranchDayOfWeekOperator](https://registry.astronomer.io/providers/apache-airflow/modules/branchdayofweekoperator): Branches based on whether the current day of week is equal to a given `week_day` parameter.
- [BranchDateTimeOperator](https://registry.astronomer.io/providers/apache-airflow/modules/branchdatetimeoperator): Branches based on whether the current time is between `target_lower` and `target_upper` times.
- [ExternalBranchPythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html#airflow.operators.python.ExternalBranchPythonOperator): Branches based on a Python function like the [BranchPythonOperator](#taskbranch-branchpythonoperator) but runs in a virtual environment like the [ExternalPythonOperator](external-python-operator.md) (available in Airflow 2.7+).

All of these operators take `follow_task_ids_if_true` and `follow_task_ids_if_false` parameters which provide the list of task(s) to include in the branch based on the logic returned by the operator.

## Additional branching resources

There is much more to the BranchPythonOperator than simply choosing one task over another.

- What if you want to trigger your tasks only on specific days? And not on holidays?  
- What if you want to trigger a DAG Run only if the previous one succeeded?

For more guidance and best practices on common use cases like the ones above, try out Astronomer's
[Academy Course on Branching](https://academy.astronomer.io/astro-runtime-branching) for free today.
