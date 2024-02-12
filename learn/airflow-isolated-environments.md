---
title: "Run tasks in an isolated environment in Apache Airflow"
sidebar_label: "Isolated Environments"
description: "Learn how to run an Airflow task in an isolated environment."
id: airflow-isolated-environments
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import virtualenv_decorator_dag from '!!raw-loader!../code-samples/dags/airflow-isolated-environments/virtualenv_decorator_dag.py';
import python_virtualenv_operator_dag from '!!raw-loader!../code-samples/dags/airflow-isolated-environments/python_virtualenv_operator_dag';
import external_python_decorator_dag from '!!raw-loader!../code-samples/dags/airflow-isolated-environments/external_python_decorator_dag';
import external_python_operator_dag from '!!raw-loader!../code-samples/dags/airflow-isolated-environments/external_python_operator_dag';

It is common to require isolated environments for specific Airflow tasks, for example when needing to run tasks using conflicting versions of Python or Python packages. 

In Airflow you have several options to isolate tasks, you can your custom Python code in:

- A newly created virtual environment with the [`@task.virtualenv` decorator / PythonVirtualEnvOperator (PVEO)].
- An existing virtual environment with the [`@task.external_python` decorator / ExternalPythonOperator (EPO)]. 
- A dedicated Kubernetes pod with the [`@task.kubernetes` decorator / KubernetesPodOperator (KPO)].

Additionally, you can run most traditional operators inside a dedicated Kubernetes pod with the [IsolatedOperator] and use [virtual branching operators]() to execute conditional task logic inside a virtual environment.

In this guide you'll learn how to:

- Use the `@task.virtualenv` decorator / PythonVirtualEnvOperator.
- Use the `@task.external_python` decorator / ExternalPythonOperator.
- Use the `@task.kubernetes` decorator / KubernetesPodOperator for basic use cases. For a more in-depth explanation of the KubernetesPodOperator, see [Use the KubernetesPodOperator](kubepod-operator.md).
- Execute conditional task logic in a virtual environment with [virtual branching operators]().

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Airflow: The ExternalPythonOperator](https://academy.astronomer.io/astro-runtime-the-externalpythonoperator).
- Astronomer Academy: [Airflow: The KubernetesPodOperator](https://academy.astronomer.io/astro-runtime-the-kubernetespodoperator-1).
- Webinar: [Running Airflow Tasks in Isolated Environments](https://www.astronomer.io/events/webinars/running-airflow-tasks-in-isolated-environments-video/).
- Learn from code: []().

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow decorators. See [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- Airflow operators. See [Airflow operators](what-is-an-operator.md).
- Python Virtual Environments. See [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/).
- Kubernetes basics. See the [Kubernetes Documentation](https://kubernetes.io/docs/home/).

## When to use isolated environments

Isolated environments enable you to pin specific versions of Python and Python packages for individual tasks, which conflict with the versions used by the Airflow environment or other Airflow tasks.

Apache Airflow is compatible Python 3.8, 3.9, 3.10, 3.11, see [Prerequisites](https://airflow.apache.org/docs/apache-airflow/stable/installation/prerequisites.html). If you need to run a task using a different version of Python than your Airflow environment, you need to use an isolated environment.

To know which Python packages are pinned to which versions within Airflow, you can retrieve the full list of constraints for each Airflow version by going to:

```text
https://raw.githubusercontent.com/apache/airflow/constraints-<AIRFLOW VERSION>/constraints-<PYTHON VERSION>.txt
```

If one of your tasks requires a different version of one of the Python packages listed, you need to use an isolated environment as well.

:::info

Astronomer's distribution of Airflow, the Astro Runtime has images available for Python 3.11, 3.10, 3.9 and 3.8 (see: [Quay.io astronomer/astro-runtime](https://quay.io/repository/astronomer/astro-runtime?tab=tags)). We recommend to use the Astro Runtime with the Astro CLI to run Airflow locally in Docker to ensure a reproducible environment separated from your local machine.

:::

## Choosing an isolated environment option

![Graph of options for isolated environments in Airflow.](/img/guides/airflow-isolated-environments_isolated_env_options_graph.png)

When choosing an isolated environment option, first you need to decide if you want to run your code in a dedicated Kubernetes pod or a Python virtual environment.

A dedicated Kubernetes pod allows you to have full control over the environment and resources used, but requires access to a Kubernetes cluster. If you want to isolate a traditional operator, a Kubernetes pod is the only option.

There are 3 options to run your code in a dedicated Kubernetes pod with Airflow:

- To run a traditional operator in an isolated environment, use the [IsolatedOperator]() to run your operator code inside a dedicated Kubernetes pod. To use the IsolatedOperator, you need to have access to a Kubernetes cluster. 
- To run any custom Python code in a dedicated Kubernetes pod, use the `@task.kubernetes` decorator or the KubernetesPodOperator (KPO). You need to have a Docker image with Python and the necessary packages for your code, as well as access to a Kubernetes cluster. Astronomer recommends to use the `@task.kubernetes` decorator over the KPO if you need to pass data into or out of the pod, as it makes handling [XCom](airflow-passing-data-between-tasks.md) easier.
- To run an existing Docker image without any additional Python code, use the [KubernetesPodOperator](kubepod-operator.md) (KPO). You need to provide Docker image to run, as well as access to a Kubernetes cluster.

A Python virtual environment is easier to set up since it does not require a Docker image or Kubernetes cluster, but does not provide the same level of control over the environment and resources used. 

If you want to run your code in a Python virtual environment, you have 2 options:

- To run your code in an existing virtual environment, use the `@task.external_python` decorator or the ExternalPythonOperator (EPO). This is a good option if you want to reuse a virtual environment in multiple tasks, the environment is created at build time, which speeds up the task execution. Astronomer 
- To run your code in a newly created virtual environment, use the `@task.virtualenv` decorator or the PythonVirtualEnvOperator (PVEO). This is a good option if you want the virtual environment to be created at Runtime instead of build time. The environment can be cached by providing a `venv_cache_path`.

Astronomer recommends to use the decorator versions over the operators, as they simplify handling of [XCom](airflow-passing-data-between-tasks.md).

If your isolated task contains branching logic, use the branching versions of the virtual environment decorators and operators:

- To run branching code in an existing virtual environment, use the `@task.branch_external_python` decorator or the ExternalBranchPythonOperator.
- To run branching code in a newly created virtual environment, use the `@task.branch_virtualenv` decorator or the BranchPythonVirtualenvOperator.

## `@task.external_python` decorator / ExternalPythonOperator

```dockerfile
# syntax=quay.io/astronomer/airflow-extensions:v1

FROM quay.io/astronomer/astro-runtime:10.3.0-python-3.11

# create a virtual environment for the ExternalPythonOperator and @task.external_python decorator
# using Python 3.9 and install the packages from epo_requirements.txt
PYENV 3.9 epo_pyenv epo_requirements.txt
```

```text
pandas==1.4.4
```

<Tabs
    defaultValue="taskflow"
    groupId="task.virtualenv-decorator-pythonvirtualenvoperator"
    values={[
        {label: 'TaskFlow API simple', value: 'taskflow'},
        {label: 'Traditional syntax simple', value: 'traditional'},
        {label: 'TaskFlow API with XCom', value: 'taskflow-xcom'},
        {label: 'Traditional syntax with XCom', value: 'traditional-xcom'},
    ]}>
<TabItem value="taskflow">

```python
    @task.external_python(python=os.environ["ASTRO_PYENV_epo_pyenv"])
    def my_isolated_task():
        import pandas as pd
        print(f"The pandas version in the virtual env is: {pd.__version__}")
        # your code to run in the isolated environment
```

</TabItem>
<TabItem value="traditional">

```python
def my_isolated_function():
    import pandas as pd
    print(f"The pandas version in the virtual env is: {pd.__version__}")

my_isolated_task = ExternalPythonOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    python=os.environ["ASTRO_PYENV_epo_pyenv"]
)
```

</TabItem>
<TabItem value="taskflow-xcom">

<CodeBlock language="python">{virtualenv_decorator_dag}</CodeBlock>

</TabItem>

<TabItem value="traditional-xcom">

<CodeBlock language="python">{python_virtualenv_operator_dag}</CodeBlock>

</TabItem>

</Tabs>

## `@task.virtualenv` decorator / PythonVirtualEnvOperator

<Tabs
    defaultValue="taskflow"
    groupId="task.virtualenv-decorator-pythonvirtualenvoperator"
    values={[
        {label: 'TaskFlow API simple', value: 'taskflow'},
        {label: 'Traditional syntax simple', value: 'traditional'},
        {label: 'TaskFlow API with XCom', value: 'taskflow-xcom'},
        {label: 'Traditional syntax with XCom', value: 'traditional-xcom'},
    ]}>
<TabItem value="taskflow">

```python
@task.virtualenv(requirements=["pandas==1.5.1"])  # add your requirements to the list
def my_isolated_task(): 
    import pandas as pd
    print(f"The pandas version in the virtual env is: {pd.__version__}")"
    # your code to run in the isolated environment
```

</TabItem>
<TabItem value="traditional">

```python
def my_isolated_function():
    import pandas as pd
    print(f"The pandas version in the virtual env is: {pd.__version__}")
    # your code to run in the isolated environment

my_isolated_task = PythonVirtualenvOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    requirements=[
        "pandas==1.5.1",
    ]  # add your requirements to the list
)
```

</TabItem>
<TabItem value="taskflow-xcom">

<CodeBlock language="python">{virtualenv_decorator_dag}</CodeBlock>

</TabItem>

<TabItem value="traditional-xcom">

<CodeBlock language="python">{python_virtualenv_operator_dag}</CodeBlock>

</TabItem>

</Tabs>




```dockerfile
# syntax=quay.io/astronomer/airflow-extensions:v1

FROM quay.io/astronomer/astro-runtime:10.3.0-python-3.11

PYENV 3.10 pyenv_3_10
```


<Tabs
    defaultValue="taskflow"
    groupId="as_setup-and-as_teardown-methods"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@task.virtualenv(
    requirements=[
        "pandas==1.5.1",
        "pendulum==3.0.0",
    ],  # pendulum is needed to use the logical date
    python_version="3.10",
)
def my_isolated_task(
    upstream_task_output: dict, logical_date
):  # note that not all objects from the context can be used!
    import pandas as pd
    import sys

    print(f"The python version in the virtual env is: {sys.version}")
    print(f"The pandas version in the virtual env is: {pd.__version__}")
    print(f"The logical_date is {logical_date}")

    return upstream_task_output
```

</TabItem>
<TabItem value="traditional">



</TabItem>

</Tabs>



## `@task.kubernetes` decorator / KubernetesPodOperator

## IsolatedOperator

## Virtual branching operators

## Use context variables in isolated environments

## Use Airflow packages in isolated environments