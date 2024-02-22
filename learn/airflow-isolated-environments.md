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

It is very common to run a task with different dependencies than your Airflow environment. Your task might need a different Python version than core Airflow, or it has packages that conflict with your other tasks. In these cases, running tasks in an isolated environment can help manage dependency conflicts and enable compatibility with your execution environments.

In Airflow, you have several options for running custom Python code in isolated environments. This guide teaches you how to choose the right isolated environment option for your use case, implement different virtual environment operators and decorators, and access Airflow context and variables in isolated environments.

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

There are two situations when you might want to run a task in an isolated environment:

- Your task requires a **different version of Python** than your Airflow environment. Apache Airflow is compatible with and available in Python 3.8, 3.9, 3.10, 3.11. The Astro Runtime has [images](https://quay.io/repository/astronomer/astro-runtime?tab=tags) available for all supported Python versions, so you can run Airflow inside Docker in a reproducible environment. See [Prerequisites](https://airflow.apache.org/docs/apache-airflow/stable/installation/prerequisites.html) for more information.
- Your task requires **different versions of Python packages** which conflict with the package versions installed in your Airflow environment. To know which Python packages are pinned to which versions within Airflow, you can retrieve the full list of constraints for each Airflow version by going to:

    ```text
    https://raw.githubusercontent.com/apache/airflow/constraints-<AIRFLOW VERSION>/constraints-<PYTHON VERSION>.txt
    ```

:::tip Airflow Best Practice

Make sure to pin all package versions, both in your core Airflow environment (`requirements.txt`) and in your isolated environments. This helps you avoid unexpected behavior due to package updates that might create version conflicts.

:::

### Limitations

When creating isolated environments in Airflow, you might not be able to use common Airflow features or connect to your Airflow environment in the same way you would in a regular Airflow task.  

Common limitations include:

- You [cannot pass all Airflow context variables](https://airflow.apache.org/docs/apache-airflow/latest/howto/operator/python.html#id1) to a virtual decorator, since Airflow does not support serializing `var`, `ti`, and `task_instance` objects. See [Use Airflow context variables in isolated environments](#use-airflow-context-variables-in-isolated-environments).
- You do not have access to your [secrets backend](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html) from within the isolated environment. To access your secrets, consider passing them in through [Jinja templating](templating.md). See [Use Airflow variables in isolated environments](#use-airflow-variables-in-isolated-environments).
- Installing Airflow itself, or Airflow provider packages in the environment provided to the `@task.external_python` decorator or the ExternalPythonOperator, can lead to unexpected behavior. If you need to use Airflow or an Airflow providers module inside your virtual environment, Astronomer recommends using the `@task.virtualenv` decorator or the PythonVirtualenvOperator instead. See [Use Airflow packages in isolated environments](#use-airflow-packages-in-isolated-environments).

## Choosing an isolated environment option

Airflow provides several options for running tasks in isolated environments.

To run tasks in a dedicated Kubernetes Pod you can use:

- [`@task.kubernetes`](#kubernetes-pod-operator) decorator 
- [KubernetesPodOperator](#kubernetes-pod-operator) (KPO)

To run tasks in a Python virtual environment you can use:

- [`@task.external_python`](#external-python-operator) decorator / ExternalPythonOperator (EPO)
- [`@task.virtualenv`](#virtualenv-operator) decorator / PythonVirtualenvOperator (PVO)
- [`@task.branch_external_python`](#virtual-branching-operators) decorator / BranchExternalPythonOperator (BEPO)
- [`@task.branch_virtualenv`](#virtual-branching-operators) decorator / BranchPythonVirtualenvOperator (BPVO)

The virtual environment decorators have operator equivalents with the same functionality. Astronomer recommends using decorators where possible because they simplify the handling of [XCom](airflow-passing-data-between-tasks.md).

![Graph of options for isolated environments in Airflow.](/img/guides/airflow-isolated-environments_isolated_env_options_graph.png)

Which option you choose depends on your use case and the requirements of your task. The table below shows which operators are best for particular use cases.

| Use Case | Implementation Options |
|----------|----------|
| Run a Python task in a K8s Pod | [`@task.kubernetes`](#kubernetes-pod-operator),<br> [KubernetesPodOperator](#kubernetes-pod-operator) |
| Run a Docker image without additional Python code in a K8s Pod | [KubernetesPodOperator](#kubernetes-pod-operator) |
| Run a Python task in an existing (reusable) virtual environment | [`@task.external_python`](#external-python-operator),<br> [ExternalPythonOperator](#external-python-operator) |
| Run a Python task in a new virtual environment | [`@task.virtualenv`](#virtualenv-operator),<br> [PythonVirtualenvOperator](#virtualenv-operator)|
| Run branching code in an existing (reusable) virtual environment | [`@task.branch_external_python`](#virtual-branching-operators), [BranchExternalPythonOperator](#virtual-branching-operators) |
| Run branching code in a new virtual environment | [`@task.branch_virtualenv`](#virtual-branching-operators), [BranchPythonVirtualenvOperator](#virtual-branching-operators) |
| Install different packages for each run of a task | [PythonVirtualenvOperator](#virtualenv-operator),<br> [BranchPythonVirtualenvOperator](#virtual-branching-operators) |

Another consideration when choosing an operator is the infrastructure you have available. Operators that run tasks in Kubernetes pods allow you to have full control over the environment and resources used, but they require a Kubernetes cluster. Operators that run tasks in Python virtual environments are easier to set up, but do not provide the same level of control over the environment and resources used.

| Requirements | Decorators | Operators |
|----------|----------|---------|
| A Kubernetes cluster | [`@task.kubernetes`](#kubernetes-pod-operator) | [KubernetesPodOperator](#kubernetes-pod-operator) |
| A Docker image | [`@task.kubernetes`](#kubernetes-pod-operator) (with Python installed) | [KubernetesPodOperator](#kubernetes-pod-operator) (with or without Python installed) |
| A Python binary | [`@task.external_python`](#external-python-operator),<br> [`@task.branch_external_python`](#virtual-branching-operators),<br> [`@task.virtualenv`](#virtualenv-operator) (\*),<br> [`@task.branch_virtualenv`](#virtual-branching-operators) (\*) | [ExternalPythonOperator](#external-python-operator),<br> [BranchExternalPythonOperator](#virtual-branching-operators),<br> [PythonVirtualenvOperator](#virtualenv-operator) (\*),<br> [BranchPythonVirtualenvOperator](#virtual-branching-operators) (\*) |

*Only required if you need to use a different Python version than your Airflow environment.

## External Python operator

The ExternalPython operator, `@task.external_python` decorator or ExternalPythonOperator, runs a Python function in an existing virtual Python environment, isolated from your Airflow environment. To use the `@task.external_python` decorator or the ExternalPythonOperator, you need to create a separate Python environment to reference. You can use any Python binary created by any means. 

The easiest way to create a Python environment when using the Astro CLI is with the [Astronomer PYENV BuildKit](https://github.com/astronomer/astro-provider-venv). The BuildKit can be used by adding a comment on the first line of the Dockerfile as shown in the following example. Adding this comment enables you to create virtual environments with the `PYENV` keyword.

```dockerfile
# syntax=quay.io/astronomer/airflow-extensions:v1

FROM quay.io/astronomer/astro-runtime:10.3.0-python-3.11

# create a virtual environment for the ExternalPythonOperator and @task.external_python decorator
# using Python 3.9 and install the packages from epo_requirements.txt
PYENV 3.9 epo_pyenv epo_requirements.txt
```

:::note

To use the BuildKit, the [Docker BuildKit Backend](https://docs.docker.com/build/buildkit/) needs to be enabled. This is the default as of Docker Desktop version 23.0, but might need to be enabled manually in older versions of Docker.

:::

You can add any Python packages to the virtual environment by putting them into a separate requirements file. In this example, by using the name `epo_requirements.txt`. Make sure to pin all package versions.

```text
pandas==1.4.4
```

:::warning

Installing Airflow itself and Airflow provider packages in isolated environments can lead to unexpected behavior and is not recommended. If you need to use Airflow and Airflow providers module inside your virtual environment, Astronomer recommends to choose the `@task.virtualenv` decorator or the PythonVirtualenvOperator. See [Use Airflow packages in isolated environments](#use-airflow-packages-in-isolated-environments).

:::

After restarting your Airflow environment, you can use this Python binary by referencing the environment variable `ASTRO_PYENV_<my-pyenv-name>`. If you choose an alternative method to create you Python binary, you need to set the `python` parameter of the decorator or operator to the location of your Python binary.

<Tabs
    defaultValue="taskflow"
    groupId="task.external_python-decorator-externalpythonoperator"
    values={[
        {label: '@task.external_python simple', value: 'taskflow'},
        {label: 'ExternalPythonOperator simple', value: 'traditional'},
        {label: '@task.external_python with XCom', value: 'taskflow-xcom'},
        {label: 'ExternalPythonOperator with XCom', value: 'traditional-xcom'},
    ]}>
<TabItem value="taskflow">

To run any Python function in your virtual environment, use the `@task.external_python` decorator on it and set the `python` parameter to the location of your Python binary.

```python
# from airflow.decorators import task
# import os

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

To run any Python function in your virtual environment, define the `python_callable` parameter of the ExternalPythonOperator with your Python function, and set the `python` parameter to the location of your Python binary.

```python
# from airflow.operators.python import ExternalPythonOperator
# import os

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
Note that Jinja templates are rendered as strings unless you set `render_template_as_native_obj=True` in the DAG definition.

<CodeBlock language="python">{external_python_operator_dag}</CodeBlock>

</TabItem>

</Tabs>

To get a list of all parameters of the `@task.external_python` decorator /  ExternalPythonOperator, see the [Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/ExternalPythonOperator).

## Virtualenv operator

The Virtualenv operator (`@task.virtualenv` or PythonVirtualenvOperator) creates a new virtual environment each time the task runs. If you only specify different package versions, you do not need to create or specify a Python binary.

:::warning

Installing Airflow itself and Airflow provider packages in isolated environments can lead to unexpected behavior and is generally not recommended. See [Use Airflow packages in isolated environments](#use-airflow-packages-in-isolated-environments).

:::

<Tabs
    defaultValue="taskflow"
    groupId="task.virtualenv-decorator-pythonvirtualenvoperator"
    values={[
        {label: '@task.virtualenv simple', value: 'taskflow'},
        {label: 'PythonVirtualenvOperator simple', value: 'traditional'},
        {label: '@task.virtualenv with XCom', value: 'taskflow-xcom'},
        {label: 'PythonVirtualenvOperator with XCom', value: 'traditional-xcom'},
    ]}>
<TabItem value="taskflow">

Add the pinned versions of the packages to the `requirements` parameter of the `@task.virtualenv` decorator. The decorator creates a new virtual environment at runtime.

```python
# from airflow.decorators import task

@task.virtualenv(requirements=["pandas==1.5.1"])  # add your requirements to the list
def my_isolated_task(): 
    import pandas as pd
    print(f"The pandas version in the virtual env is: {pd.__version__}")"
    # your code to run in the isolated environment
```

</TabItem>
<TabItem value="traditional">

Add the pinned versions of the packages you need to the `requirements` parameter of the PythonVirtualenvOperator. The operator creates a new virtual environment at runtime.

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

You can pass information into and out of the `@task.virtualenv` decorated task using the same process as you would when interacting with a `@task` decorated task. See [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md) for more detailed information.

<CodeBlock language="python">{virtualenv_decorator_dag}</CodeBlock>

</TabItem>

<TabItem value="traditional-xcom">

You can pass information into the PythonVirtualenvOperator by using a [Jinja template](templating.md) to retrieve [XCom](airflow-passing-data-between-tasks.md) values from the [Airflow context](airflow-context.md). To pass information out of the PythonVirtualenvOperator, return it from the `python_callable`.
Note that Jinja templates are rendered as strings unless you set `render_template_as_native_obj=True` in the DAG definition.

<CodeBlock language="python">{python_virtualenv_operator_dag}</CodeBlock>

</TabItem>

</Tabs>

Since the `requirements` parameter of the PythonVirtualenvOperator is [templatable](templating.md), you can use [Jinja templating](templating.md) to pass information at runtime. For example, you can use a Jinja template to install a different version of pandas for each run of the task.

```python
# from airflow.decorators import task
# from airflow.models.baseoperator import chain
# from airflow.operators.python import PythonVirtualenvOperator

@task
def get_pandas_version():
    pandas_version = "1.5.1"  # retrieve the pandas version according to your logic
    return pandas_version

my_isolated_task = PythonVirtualenvOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    requirements=[
        "pandas=={{ ti.xcom_pull(task_ids='get_pandas_version') }}",
    ],
)

chain(get_pandas_version(), my_isolated_task)
```

If your task requires a different Python version than your Airflow environment, you need to install the Python version your task requires in your Airflow environment so the Virtualenv task can use it. Use the [Astronomer PYENV BuildKit](https://github.com/astronomer/astro-provider-venv) to install a different Python version in your Dockerfile.


```dockerfile
# syntax=quay.io/astronomer/airflow-extensions:v1

FROM quay.io/astronomer/astro-runtime:10.3.0-python-3.11

PYENV 3.10 pyenv_3_10
```

:::note

To use the BuildKit, the [Docker BuildKit Backend](https://docs.docker.com/build/buildkit/) needs to be enabled. This is the default starting in Docker Desktop version 23.0, but might need to be enabled manually in older versions of Docker.

:::

The Python version can be referenced directly using the `python` parameter of the decorator/operator.

<Tabs
    defaultValue="taskflow"
    groupId="task.virtualenv-decorator-pythonvirtualenvoperator"
    values={[
        {label: '@task.virtualenv', value: 'taskflow'},
        {label: 'PythonVirtualenvOperator', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
# from airflow.decorators import task

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

To get a list of all parameters of the `@task.virtualenv` decorator or PythonVirtualenvOperator, see the [Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/pythonvirtualenvoperator).

:::

## Kubernetes pod operator

The Kubernetes operator, `@task.kubernetes` decorator or KubernetesPodOperator, runs an Airflow task in a dedicated Kubernetes pod. You can use the `@task.kubernetes` to run any custom Python code in a separate Kubernetes pod on a Docker image with Python installed, while the KubernetesPodOperator runs any existing Docker image.

To use the `@task.kubernetes` decorator or the KubernetesPodOperator, you need to provide a Docker image and have access to a Kubernetes cluster. The following example shows how to use the modules to run in a task in a separate Kubernetes pod in the same namespace and Kubernetes cluster as your Airflow environment. For more information on how to use the KubernetesPodOperator, see [Use the KubernetesPodOperator](kubepod-operator.md) and [Run the KubernetesPodOperator on Astro](https://docs.astronomer.io/astro/kubernetespodoperator).

<Tabs
    defaultValue="taskflow"
    groupId="task.kubernetes-decorator-kubepodoperator"
    values={[
        {label: '@task.kubernetes', value: 'taskflow'},
        {label: 'KubernetesPodOperator', value: 'traditional'},
    ]}>

<TabItem value="taskflow">
    
```python
# from airflow.decorators import task
# from airflow.configuration import conf

# if you are running Airflow on Kubernetes, you can get 
# the current namespace from the Airflow conf
namespace = conf.get("kubernetes", "NAMESPACE")

@task.kubernetes(
    image="<YOUR IMAGE>",
    in_cluster=True,
    namespace=namespace,
    name="<YOUR POD NAME>",
    get_logs=True,
    log_events_on_failure=True,
    do_xcom_push=True,
)
def my_isolated_task(num: int):
    return num + 1
```

</TabItem>
<TabItem value="traditional">

```python
# from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
# from airflow.configuration import conf

# if you are running Airflow on Kubernetes, you can get 
# the current namespace from the Airflow conf
namespace = conf.get("kubernetes", "NAMESPACE")

my_isolated_task = KubernetesPodOperator(
    task_id="my_isolated_task",
    namespace=namespace,
    # your Docker image contains the scripts to run in the isolated environment  
    image="<YOUR IMAGE>",
    name="<YOUR POD NAME>",
    in_cluster=True,
    is_delete_operator_pod=True,
    get_logs=True,
)
```
</TabItem>
</Tabs>

## Virtual branching operators

Virtual branching operators allow you to run conditional task logic in an isolated Python environment.

- `@task.branch_external_python` decorator or BranchExternalPythonOperator: Run conditional task logic in an existing virtual Python environment.
- `@task.branch_virtualenv` decorator or BranchPythonVirtualenvOperator: Run conditional task logic in a newly created virtual Python environment.

To run conditional task logic in an isolated environment, use the branching versions of the virtual environment decorators and operators. You can learn more about branching in Airflow in the [Branching in Airflow](airflow-branch-operator.md) guide.

<Tabs
    defaultValue="taskflow-epo"
    groupId="virtual-branching-decorators-operators"
    values={[
        {label: '@task.external_python', value: 'taskflow-epo'},
        {label: 'BranchExternalPythonOperator', value: 'traditional-epo'},
        {label: '@task.virtualenv', value: 'taskflow-venv'},
        {label: 'BranchPythonVirtualenvOperator', value: 'traditional-venv'},
    ]}>
<TabItem value="taskflow-epo">

```python
# from airflow.decorators import task
# import os

@task.branch_external_python(python=os.environ["ASTRO_PYENV_epo_pyenv"])
def my_isolated_task():
    import pandas as pd
    import random
    print(f"The pandas version in the virtual env is: {pd.__version__}")

    num = random.randint(0, 100)

    if num > 50:
        # return the task_id of the downstream task that should be executed
        return "downstream_task_a"  
    else:
        return "downstream_task_b"
```

</TabItem>
<TabItem value="traditional-epo">

```python
# from airflow.operators.python import BranchExternalPythonOperator
# import os

def my_isolated_function():
    import pandas as pd
    import random
    print(f"The pandas version in the virtual env is: {pd.__version__}")

    num = random.randint(0, 100)

    if num > 50:
        # return the task_id of the downstream task that should be executed
        return "downstream_task_a"  
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
# from airflow.decorators import task

@task.branch_virtualenv(requirements=["pandas==1.5.3"])
def my_isolated_task():
    import pandas as pd
    import random
    print(f"The pandas version in the virtual env is: {pd.__version__}")

    num = random.randint(0, 100)

    if num > 50:
        # return the task_id of the downstream task that should be executed
        return "downstream_task_a"
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
        # return the task_id of the downstream task that should be executed
        return "downstream_task_a"  
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

## Use Airflow context variables in isolated environments

Some variables from the [Airflow context](airflow-context.md) can be passed to isolated environments, for example the `logical_date` of the DAG run. Due to compatibility issues, other objects from the context such as `ti` cannot be passed to isolated environments. For more information, see the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/latest/howto/operator/python.html#id1).

<Tabs
    defaultValue="taskflow-epo"
    groupId="use-airflow-context-variables-in-isolated-environments"
    values={[
        {label: '@task.external_python', value: 'taskflow-epo'},
        {label: 'ExternalPythonOperator', value: 'traditional-epo'},
        {label: '@task.virtualenv', value: 'taskflow-venv'},
        {label: 'PythonVirtualenvOperator', value: 'traditional-venv'},
    ]}>
<TabItem value="taskflow-epo">
    
```python
# from airflow.decorators import task
# import os

# note that to be able to use the logical date, pendulum needs to be installed in the epo_pyenv
@task.external_python(python=os.environ["ASTRO_PYENV_epo_pyenv"])
def my_isolated_task(logical_date): 
    print(f"The logical date is: {logical_date}")
    # your code to run in the isolated environment 

my_isolated_task()
```
</TabItem>
<TabItem value="traditional-epo">

```python
# from airflow.operators.python import ExternalPythonOperator
# import os

def my_isolated_function(logical_date_from_op_kwargs):
    print(f"The logical date is: {logical_date_from_op_kwargs}")
    # your code to run in the isolated environment 

my_isolated_task = ExternalPythonOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    # note that to be able to use the logical date, pendulum needs to be installed in the epo_pyenv
    python=os.environ["ASTRO_PYENV_epo_pyenv"],
    op_kwargs={
        "logical_date_from_op_kwargs": "{{ logical_date }}",
    },
)
```
</TabItem>
<TabItem value="taskflow-venv">

```python
# from airflow.decorators import task

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
# from airflow.operators.python import PythonVirtualenvOperator

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

## Use Airflow variables in isolated environments

You can inject Airflow variables into isolated environments by using [Jinja templating](templating.md) in the `op_kwargs` argument of the PythonVirtualenvOperator or ExternalPythonOperator. This strategy lets you pass secrets into your isolated environment, which are masked in the logs according to rules described in [Hide sensitive information in Airflow variables](airflow-variables.md#hide-sensitive-information-in-airflow-variables).

<Tabs
    defaultValue="traditional-venv"
    groupId="use-airflow-variables-in-isolated-environments"
    values={[
        {label: 'PythonVirtualenvOperator', value: 'traditional-venv'},
        {label: 'ExternalPythonOperator', value: 'traditional-epo'},
    ]}>

<TabItem value="traditional-venv">

```python
# from airflow.operators.python import PythonVirtualenvOperator

def my_isolated_function(password_from_op_kwargs):
    print(f"The password is: {password_from_op_kwargs}")

my_isolated_task = PythonVirtualenvOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    requirements=["pandas==1.5.1"],
    python_version="3.10",
    op_kwargs={
        "password_from_op_kwargs": "{{ var.value.my_secret }}",
    },
)
```

</TabItem>
<TabItem value="traditional-epo">

```python
# from airflow.operators.python import ExternalPythonOperator
# import os

def my_isolated_function(password_from_op_kwargs):
    print(f"The password is: {password_from_op_kwargs}")

my_isolated_task = ExternalPythonOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    python=os.environ["ASTRO_PYENV_epo_pyenv"],
    op_kwargs={
        "password_from_op_kwargs": "{{ var.value.my_secret }}",
    },
)
```
</TabItem>
</Tabs>

## Use Airflow packages in isolated environments

:::warning

Using Airflow packages inside of isolated environments can lead to unexpected behavior and is not recommended. 

:::

If you need to use Airflow or an Airflow providers module inside your virtual environment, use the `@task.virtualenv` decorator or the PythonVirtualenvOperator instead of the `@task.external_python` decorator or the ExternalPythonOperator.
As of Airflow 2.8, you can cache the virtual environment for reuse by providing a `venv_cache_path` to the `@task.virtualenv` decorator, PythonVirtualenvOperator, to speed up subsequent runs of your task.

<Tabs
    defaultValue="taskflow"
    groupId="use-airflow-packages-in-isolated-environments"
    values={[
        {label: '@task.virtualenv', value: 'taskflow'},
        {label: 'PythonVirtualenvOperator', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
# from airflow.decorators import task

@task.virtualenv(
    requirements=[
        "apache-airflow-providers-snowflake==5.3.0",
        "apache-airflow==2.8.1",
        "pandas==1.5.3",
    ],
    venv_cache_path="/tmp/venv_cache",  # optional caching of the virtual environment
)
def my_isolated_task():
    from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
    import pandas as pd

    hook = SnowflakeHook(snowflake_conn_id="MY_SNOWFLAKE_CONN_ID")
    result = hook.get_first("SELECT * FROM MY_TABLE LIMIT 1")
    print(f"The pandas version in the virtual env is: {pd.__version__}")

    return result

my_isolated_task()
```

</TabItem>
<TabItem value="traditional">

```python
# from airflow.operators.python import PythonVirtualenvOperator

def my_isolated_function():
    from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
    import pandas as pd

    hook = SnowflakeHook(snowflake_conn_id="MY_SNOWFLAKE_CONN_ID")
    result = hook.get_first("SELECT * FROM MY_TABLE LIMIT 1")
    print(f"The pandas version in the virtual env is: {pd.__version__}")

    return result

my_isolated_task = PythonVirtualenvOperator(
    task_id="my_isolated_task",
    python_callable=my_isolated_function,
    requirements=[
        "pandas==1.5.3",
        "apache-airflow==2.8.1",
        "apache-airflow-providers-snowflake==5.3.0",
    ],
    venv_cache_path="/tmp/venv_cache",  # optional caching of the virtual environment
)
```
</TabItem>
</Tabs>

