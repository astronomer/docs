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
import python_virtualenv_operator_dag from '!!raw-loader!../code-samples/dags/airflow-isolated-environments/python_virtualenv_operator_dag.py';
import external_python_decorator_dag from '!!raw-loader!../code-samples/dags/airflow-isolated-environments/external_python_decorator_dag.py';
import external_python_operator_dag from '!!raw-loader!../code-samples/dags/airflow-isolated-environments/external_python_operator_dag.py';

It is common to require isolated environments for specific Airflow tasks, for example when needing to run tasks using conflicting versions of Python or Python packages. 

![Graph of options for isolated environments in Airflow.](/img/guides/airflow-isolated-environments_isolated_env_options_graph.png)

In Airflow you have several options to isolate tasks, you can your custom Python code in:

- A newly created virtual environment with the [`@task.virtualenv` decorator / PythonVirtualEnvOperator (PVEO)].
- An existing virtual environment with the [`@task.external_python` decorator / ExternalPythonOperator (EPO)]. 
- A dedicated Kubernetes pod with the [`@task.kubernetes` decorator / KubernetesPodOperator (KPO)].

Additionally, you can run most traditional operators inside a dedicated Kubernetes pod with the [IsolatedOperator](https://github.com/astronomer/apache-airflow-providers-isolation/) and use [virtual branching operators](#virtual-branching-decorators--operators) to execute conditional task logic inside a virtual environment.

In this guide you'll learn how to:

- Use the `@task.virtualenv` decorator / PythonVirtualEnvOperator.
- Use the `@task.external_python` decorator / ExternalPythonOperator.
- Execute conditional task logic in a virtual environment with virtual branching operators.

To learn how to use the `@task.kubernetes` decorator and the KubernetesPodOperator, see [Use the KubernetesPodOperator](kubepod-operator.md).

To learn more about the IsolatedOperator, see the [Isolation provider README](https://github.com/astronomer/apache-airflow-providers-isolation).

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Astronomer Academy: [Airflow: The ExternalPythonOperator](https://academy.astronomer.io/astro-runtime-the-externalpythonoperator).
- Astronomer Academy: [Airflow: The KubernetesPodOperator](https://academy.astronomer.io/astro-runtime-the-kubernetespodoperator-1).
- Webinar: [Running Airflow Tasks in Isolated Environments](https://www.astronomer.io/events/webinars/running-airflow-tasks-in-isolated-environments-video/).
- Learn from code: [Isolated environments example DAGs repository](https://github.com/astronomer/learn-demos/tree/airflow-isolated-environments).

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

### Limitations

secrets backends, airflow context. 

## Choosing an isolated environment option

When choosing an isolated environment option, first you need to decide if you want to run your code in a dedicated Kubernetes pod or a Python virtual environment.

A dedicated Kubernetes pod allows you to have full control over the environment and resources used, but requires access to a Kubernetes cluster. If you want to isolate a traditional operator, a Kubernetes pod is the only option.

There are 3 options to run your code in a dedicated Kubernetes pod with Airflow:

- To run a **traditional operator** in an isolated environment, use the [IsolatedOperator] to run your operator code inside a dedicated Kubernetes pod. To use the IsolatedOperator, you need to have access to a Kubernetes cluster. 
- To run **any custom Python code** in a dedicated Kubernetes pod, use the `@task.kubernetes` decorator or the KubernetesPodOperator (KPO). You need to have a Docker image with Python and the necessary packages for your code, as well as access to a Kubernetes cluster. Astronomer recommends to use the `@task.kubernetes` decorator over the KPO if you need to pass data into or out of the pod, as it makes handling [XCom](airflow-passing-data-between-tasks.md) easier.
- To run an **existing Docker image** without any additional Python code, use the [KubernetesPodOperator](kubepod-operator.md) (KPO). You need to provide Docker image to run, as well as access to a Kubernetes cluster.

A Python virtual environment is easier to set up since it does not require a Docker image or Kubernetes cluster, but does not provide the same level of control over the environment and resources used. 

If you want to run your code in a Python virtual environment, you have 2 options:

- To run your code in an **existing virtual environment**, use the `@task.external_python` decorator or the ExternalPythonOperator (EPO). This is a good option if you want to reuse a virtual environment in multiple tasks, the environment is created at build time, which speeds up the task execution. Astronomer 
- To run your code in a **newly created virtual environment**, use the `@task.virtualenv` decorator or the PythonVirtualEnvOperator (PVEO). This is a good option if you want the virtual environment to be created at Runtime instead of build time. The environment can be cached by providing a `venv_cache_path`.

Astronomer recommends to use the decorator versions over the operators, as they simplify handling of [XCom](airflow-passing-data-between-tasks.md).

If your isolated task contains branching logic, use the branching versions of the virtual environment decorators and operators:

- To run branching code in an existing virtual environment, use the `@task.branch_external_python` decorator or the ExternalBranchPythonOperator.
- To run branching code in a newly created virtual environment, use the `@task.branch_virtualenv` decorator or the BranchPythonVirtualenvOperator.

## `@task.external_python` decorator / ExternalPythonOperator

To use the `@task.external_python` decorator or the ExternalPythonOperator you need to create a separate Python environment to reference. You can use any Python binary created by any means. 

The easiest way to create a Python environment when using the Astro CLI is with the [Astronomer PYENV BuildKit](https://github.com/astronomer/astro-provider-venv). The BuildKit can be used by adding a comment on the first line of the Dockerfile as shown below. Adding this comment enables you to create virtual environments with the `PYENV` keyword.

```dockerfile
# syntax=quay.io/astronomer/airflow-extensions:v1

FROM quay.io/astronomer/astro-runtime:10.3.0-python-3.11

# create a virtual environment for the ExternalPythonOperator and @task.external_python decorator
# using Python 3.9 and install the packages from epo_requirements.txt
PYENV 3.9 epo_pyenv epo_requirements.txt
```

:::note

To use the BuildKit the [Docker BuildKit Backend](https://docs.docker.com/build/buildkit/) needs to be enabled. This is the default as of Docker Desktop version 23.0 but might need to be enabled manually in older versions of Docker.

:::

You can add any Python packages to the virtual environment by putting it into a separate requirements file, in our example using the name `epo_requirements.txt`. Make sure to pin all package versions.

```text
pandas==1.4.4
```

After restarting your Airflow environment you can use this Python binary by referencing the environment variable `ASTRO_PYENV_<my-pyenv-name>`. If you are using an alternative method to create you Python binary, you need to set the `python` parameter of the decorator/operator to the location of your Python binary.

<Tabs
    defaultValue="taskflow"
    groupId="task.external_python-decorator-externalpythonoperator"
    values={[
        {label: 'TaskFlow API simple', value: 'taskflow'},
        {label: 'Traditional syntax simple', value: 'traditional'},
        {label: 'TaskFlow API with XCom', value: 'taskflow-xcom'},
        {label: 'Traditional syntax with XCom', value: 'traditional-xcom'},
    ]}>
<TabItem value="taskflow">

To run any Python function in your virtual environment, use the `@task.external_python` decorator on it and set the `python` parameter to the location of your Python binary.

```python
@task.external_python(python=os.environ["ASTRO_PYENV_epo_pyenv"])
def my_isolated_task():
    import pandas as pd
    import sys
    print(f"The python version in the virtual env is: {sys.version}")
    print(f"The pandas version in the virtual env is: {pd.__version__}")
    # your code to run in the isolated environment
```

</TabItem>
<TabItem value="traditional">

To run any Python function in your virtual environment, provide it to the `python_callable` parameter of the ExternalPythonOperator and set the `python` parameter to the location of your Python binary.

```python
# from airflow.operators.python import ExternalPythonOperator

def my_isolated_function():
    import pandas as pd
    import sys
    print(f"The python version in the virtual env is: {sys.version}")
    print(f"The pandas version in the virtual env is: {pd.__version__}")

my_isolated_task = ExternalPythonOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    python=os.environ["ASTRO_PYENV_epo_pyenv"]
)
```

</TabItem>
<TabItem value="taskflow-xcom">

You can pass information into and out of the `@task.external_python` decorated task the same way as you would when interacting with a `@task` decorated task, see also [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).

<CodeBlock language="python">{external_python_decorator_dag}</CodeBlock>

</TabItem>

<TabItem value="traditional-xcom">

You can pass information into the ExternalPythonOperator by using a [Jinja template](templating.md) retrieving [XCom](airflow-passing-data-between-tasks.md) values from the [Airflow context](airflow-context.md). To pass information out of the ExternalPythonOperator, return it from the `python_callable`.
Note that Jinja templates will be rendered as strings unless you set `render_template_as_native_obj=True` in the DAG definition.

<CodeBlock language="python">{external_python_operator_dag}</CodeBlock>

</TabItem>

</Tabs>

To get a list of all parameters of the `@task.external_python` decorator /  ExternalPythonOperator, see the [Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/ExternalPythonOperator).

## `@task.virtualenv` decorator / PythonVirtualEnvOperator

To use the `@task.virtualenv` decorator or the PythonVirtualenvOperator to create a virtual environment with the same Python version as your Airflow environment but potentially conflicting packages, you do not need to create a Python binary up front. The decorator/operator will create a virtual environment for you at runtime.

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

Add the pinned versions of the packages you need to the `requirements` parameter of the `@task.virtualenv` decorator. The decorator will create a new virtual environment at runtime.

```python
@task.virtualenv(requirements=["pandas==1.5.1"])  # add your requirements to the list
def my_isolated_task(): 
    import pandas as pd
    print(f"The pandas version in the virtual env is: {pd.__version__}")"
    # your code to run in the isolated environment
```

</TabItem>
<TabItem value="traditional">

Add the pinned versions of the packages you need to the `requirements` parameter of the PythonVirtualenvOperator. The operator will create a new virtual environment at runtime.

```python
# from airflow.operators.python import PythonVirtualenvOperator

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

You can pass information into and out of the `@task.virtualenv` decorated task the same way as you would when interacting with a `@task` decorated task, see also [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).

<CodeBlock language="python">{virtualenv_decorator_dag}</CodeBlock>

</TabItem>

<TabItem value="traditional-xcom">

You can pass information into the PythonVirtualenvOperator by using a [Jinja template](templating.md) retrieving [XCom](airflow-passing-data-between-tasks.md) values from the [Airflow context](airflow-context.md). To pass information out of the PythonVirtualenvOperator, return it from the `python_callable`.
Note that Jinja templates will be rendered as strings unless you set `render_template_as_native_obj=True` in the DAG definition.

<CodeBlock language="python">{python_virtualenv_operator_dag}</CodeBlock>

</TabItem>

</Tabs>

If you want to build a virtual environment at runtime with a different Python version than your Airflow environment, you can use the [Astronomer PYENV BuildKit](https://github.com/astronomer/astro-provider-venv) to install a different Python version for your operator/decorator to use.


```dockerfile
# syntax=quay.io/astronomer/airflow-extensions:v1

FROM quay.io/astronomer/astro-runtime:10.3.0-python-3.11

PYENV 3.10 pyenv_3_10
```

:::note

To use the BuildKit the [Docker BuildKit Backend](https://docs.docker.com/build/buildkit/) needs to be enabled. This is the default as of Docker Desktop version 23.0 but might need to be enabled manually in older versions of Docker.

:::

The Python version can be referenced directly using the `python` parameter of the decorator/operator.

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
    requirements=["pandas==1.5.1"], 
    python_version="3.10",  # specify the Python version
)
def my_isolated_task():
    import pandas as pd
    import sys
    print(f"The python version in the virtual env is: {sys.version}")
    print(f"The pandas version in the virtual env is: {pd.__version__}")
    # your code to run in the isolated environment
```

</TabItem>
<TabItem value="traditional">

```python
#from airflow.operators.python import PythonVirtualenvOperator

def my_isolated_function():
    import pandas as pd
    import sys
    print(f"The python version in the virtual env is: {sys.version}")
    print(f"The pandas version in the virtual env is: {pd.__version__}")
    # your code to run in the isolated environment

my_isolated_task = PythonVirtualenvOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    requirements=["pandas==1.5.1"],
    python_version="3.10",  # specify the Python version
)
```

</TabItem>

</Tabs>

:::tip

To get a list of all parameters of the `@task.virtualenv` decorator / PythonVirtualenvOperator, see the [Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/pythonvirtualenvoperator).

:::

## Virtual branching decorators / operators

To run conditional task logic in an isolated environment, use the branching versions of the virtual environment decorators and operators.

<Tabs
    defaultValue="taskflow-epo"
    groupId="virtual-branching-decorators-operators"
    values={[
        {label: '@task.external_python', value: 'taskflow-epo'},
        {label: 'ExternalBranchPythonOperator', value: 'traditional-epo'},
        {label: '@task.virtualenv', value: 'taskflow-venv'},
        {label: 'BranchPythonVirtualenvOperator', value: 'traditional-venv'},
    ]}>
<TabItem value="taskflow-epo">

```python
@task.branch_external_python(python=os.environ["ASTRO_PYENV_epo_pyenv"])
def my_isolated_task():
    import pandas as pd
    import random
    print(f"The pandas version in the virtual env is: {pd.__version__}")

    num = random.randint(0, 100)

    if num > 50:
        return "downstream_task_a"  # return the task_id of the downstream task that should be executed
    else:
        return "downstream_task_b"
```

</TabItem>
<TabItem value="traditional-epo">

```python
# from airflow.operators.python import BranchExternalPythonOperator

def my_isolated_function():
    import pandas as pd
    import random
    print(f"The pandas version in the virtual env is: {pd.__version__}")

    num = random.randint(0, 100)

    if num > 50:
        return "downstream_task_a"  # return the task_id of the downstream task that should be executed
    else:
        return "downstream_task_b"

my_isolated_task = BranchExternalPythonOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    python=os.environ["ASTRO_PYENV_epo_pyenv"]
)
```

</TabItem>
<TabItem value="taskflow-venv">

```python
@task.branch_virtualenv(requirements=["pandas==1.5.3"])
def my_isolated_task():
    import pandas as pd
    import random
    print(f"The pandas version in the virtual env is: {pd.__version__}")

    num = random.randint(0, 100)

    if num > 50:
        return "downstream_task_a"  # return the task_id of the downstream task that should be executed
    else:
        return "downstream_task_b"
```

</TabItem>

<TabItem value="traditional-venv">

```python
# from airflow.operators.python import BranchPythonVirtualenvOperator

def my_isolated_function():
    import pandas as pd
    import random
    print(f"The pandas version in the virtual env is: {pd.__version__}")

    num = random.randint(0, 100)

    if num > 50:
        return "downstream_task_a"  # return the task_id of the downstream task that should be executed
    else:
        return "downstream_task_b"

my_isolated_task = BranchPythonVirtualenvOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    requirements=["pandas==1.5.1"],
)
```
</TabItem>
</Tabs>

## Use context variables in isolated environments

Some variables from the [Airflow context](airflow-context.md) can be passed to isolated environments, for example the `logical_date` of the DAG run.
Due to compatibility issues, objects from the context such as `ti` cannot be passed to isolated environments, see the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/latest/howto/operator/python.html#id1).

<Tabs
    defaultValue="taskflow-epo"
    groupId="context-variables-in-isolated-environments"
    values={[
        {label: '@task.external_python', value: 'taskflow-epo'},
        {label: 'ExternalPythonOperator', value: 'traditional-epo'},
        {label: '@task.virtualenv', value: 'taskflow-venv'},
        {label: 'PythonVirtualenvOperator', value: 'traditional-venv'},
    ]}>
<TabItem value="taskflow-epo">
    
```python
@task.external_python(python=os.environ["ASTRO_PYENV_epo_pyenv"])
def my_isolated_task(logical_date):  # note that to be able to use the logical date, pendulum needs to be installed in the epo_pyenv
    print(f"The logical date is: {logical_date}")
    # your code to run in the isolated environment 

my_isolated_task()
```
</TabItem>
<TabItem value="traditional-epo">

```python
def my_isolated_function(logical_date_from_op_kwargs):
    print(f"The logical date is: {logical_date_from_op_kwargs}")
    # your code to run in the isolated environment 

my_isolated_task = ExternalPythonOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    python=os.environ["ASTRO_PYENV_epo_pyenv"],
    op_kwargs={
        "logical_date_from_op_kwargs": "{{ logical_date }}",
    },
)
```
</TabItem>
<TabItem value="taskflow-venv">

```python
@task.virtualenv(
    requirements=[
        "pandas==1.5.1",
        "pendulum==3.0.0",
    ],  # pendulum is needed to use the logical date
)
def my_isolated_task(logical_date):
    print(f"The logical date is: {logical_date}")
    # your code to run in the isolated environment
```

</TabItem>
<TabItem value="traditional-venv">
    
```python
def my_isolated_function(logical_date_from_op_kwargs):
    print(f"The logical date is: {logical_date_from_op_kwargs}")
    # your code to run in the isolated environment 

my_isolated_task = PythonVirtualenvOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    requirements=[
        "pandas==1.5.1",
        "pendulum==3.0.0",
    ],  # pendulum is needed to use the logical date
    op_kwargs={
        "logical_date_from_op_kwargs": "{{ logical_date }}"
    },
)
```
</TabItem>
</Tabs>

## Use Airflow packages in isolated environments

:::warning

Using Airflow packages inside of isolated environments can lear to unexpected behavior and is not recommended. 

:::