---
title: "Branching in Airflow"
sidebar_label: "Branches"
id: airflow-branch-operator
---

<head>
  <meta name="description" content="Learn about Airflow’s multiple options for building conditional logic and branching within DAGs, including the BranchPythonOperator and ShortCircuitOperator." />
  <meta name="og:description" content="Learn about the options available in Airflow for building conditional logic and branching within DAGs, including the BranchPythonOperator and ShortCircuitOperator." />
</head>

When designing your data pipelines, you may encounter use cases that require more complex task flows than "Task A > Task B > Task C". For example, you may have a use case where you need to decide between multiple tasks to execute based on the results of an upstream task. Or you may have a case where part of your pipeline should only run under certain external conditions. Fortunately, Airflow has multiple options for building conditional logic and/or branching into your DAGs.

In this guide, you'll learn how you can use `@task.branch` (`BranchPythonOperator`) and `@task.short_circuit` (`ShortCircuitOperator`), other available branching operators, and additional resources to implement conditional logic in your Airflow DAGs.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Dependencies in Airflow. See [Managing Dependencies in Apache Airflow](managing-dependencies.md).
- Using Airflow decorators. See [Introduction to Airflow decorators](airflow-decorators.md).

## @task.branch and BranchPythonOperator

One of the simplest ways to implement branching in Airflow is to use the `@task.branch` decorator or the [BranchPythonOperator](https://registry.astronomer.io/providers/apache-airflow/modules/branchpythonoperator). Like the `@task` decorator and the [`PythonOperator`](https://registry.astronomer.io/providers/apache-airflow/modules/pythonoperator), `@task.branch` and the `BranchPythonOperator` take a Python function as their input. However, the input function to `@task.branch` and to the `BranchPythonOperator` must return a list of valid task IDs that the DAG should proceed with based on some logic. 

For example, we can pass the following function that returns one set of task IDs if the result is greater than 0.5 and a different set if the result is less than or equal to 0.5:

```python
def choose_branch(result):
    if result > 0.5:
        return ['task_a', 'task_b']
    return ['task_c']
```

In general, the `@task.branch` or `BranchPythonOperator` is a good choice if your branching logic can be easily implemented in a simple Python function. Whether you want to use the decorated version or the traditional operator is a question of personal preference.

The code below shows a full example of how to use the `@task.branch` decorator or the `BranchPythonOperator` in a DAG:

<Tabs
    defaultValue="taskflow"
    groupId= "example-branch"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional Operators', value: 'traditional'},
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

The DAG above shows how `random.choice()` is used to return one random option out of a list of four branches. In the following DAG run screenshot, where `branch_b` was randomly chosen, we see that the two tasks in `branch_b` were successfully run while the others were skipped.

![Branching Graph View](/img/guides/branching_decorator_graph.png)

If you have downstream tasks that need to run regardless of which branch is taken, like the `join` task in our example above, you need to update the trigger rule appropriately. The default trigger rule in Airflow is `all_success`, which means that if upstream tasks are skipped, then the downstream task will not run. In this case, we chose `none_failed_min_one_success` to indicate that the task should run as long as one upstream task succeeded and no tasks failed.

Finally, note that with the `@task.branch` decorator and the `BranchPythonOperator`, your Python callable *must* return at least one task ID for whichever branch is chosen (i.e. it can't return nothing). If one of the paths in your branching should do nothing, you can use an `EmptyOperator` in that branch.

:::info

More examples using the `@task.branch` decorator, can be found on the [Astronomer Registry](https://registry.astronomer.io/dags/example-branch-python-dop-operator-3).

:::

## @task.short_circuit and ShortCircuitOperator

Another option for implementing conditional logic in your DAGs is the `@task.short_circuit` decorator and [ShortCircuitOperator](https://registry.astronomer.io/providers/apache-airflow/modules/shortcircuitoperator). This operator takes a Python callable that returns `True` or `False` based on logic implemented for your use case. If `True` is returned, the DAG will continue, and if `False` is returned, all downstream tasks will be skipped.

The `@task.short_circuit` and `ShortCircuitOperator` is best used in cases where you know that part of your DAG runs only occasionally. For example, maybe your DAG runs daily, but some tasks should only run on Sundays. Or maybe your DAG orchestrates a machine learning model, and tasks that publish the model should only be run if a certain accuracy is reached after training. This type of logic can also be implemented with `@task.branch`, but that operator requires a task ID to be returned. Using the `@task.short_circuit` decorator or `ShortCircuitOperator` can be cleaner in cases where the conditional logic equates to "run or not" as opposed to "run this or that".

The following DAG shows an example of how to implement the `@task.short_circuit` and `ShortCircuitOperator`:

<Tabs
    defaultValue="taskflow"
    groupId= "example-short-circuit"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional Operators', value: 'traditional'},
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

In this DAG there are two short circuits, one which will always return `True` and one which will return `False`. When you run the DAG, you can see that tasks downstream of the `True` condition operator ran, while tasks downstream of the `False` condition operator were skipped.

![Short Circuit](/img/guides/short_circuit_decorator_graph.png)

:::info

Another example using the `ShortCircuitOperator`, can be found on the [Astronomer Registry](https://registry.astronomer.io/dags/example-short-circuit-operator).

:::

## Other branch operators

Airflow offers a few other branching operators that work similarly to the `BranchPythonOperator` but for more specific contexts: 

- [`BranchSQLOperator`](https://registry.astronomer.io/providers/apache-airflow/modules/branchsqloperator): Branches based on whether a given SQL query returns `true` or `false`.
- [`BranchDayOfWeekOperator`](https://registry.astronomer.io/providers/apache-airflow/modules/branchdayofweekoperator): Branches based on whether the current day of week is equal to a given `week_day` parameter.
- [`BranchDateTimeOperator`](https://registry.astronomer.io/providers/apache-airflow/modules/branchdatetimeoperator): Branches based on whether the current time is between `target_lower` and `target_upper` times.

All of these operators take `follow_task_ids_if_true` and `follow_task_ids_if_false` parameters which provide the list of task(s) to include in the branch based on the logic returned by the operator.

## Additional branching resources

There is much more to the BranchPythonOperator than simply choosing one task over another.

- What if you want to trigger your tasks only on specific days? And not on holidays?  
- What if you want to trigger a DAG Run only if the previous one succeeded?

For more guidance and best practices on common use cases like the ones above, try out Astronomer's
[Academy Course on Branching](https://academy.astronomer.io/branching-course) for free today.
