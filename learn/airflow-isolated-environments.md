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

- A newly created virtual environment with the [`@task.virtualenv` decorator / PythonVirtualEnvOperator (PVEO)](#taskvirtualenv-decorator--pythonvirtualenvoperator).
- An existing virtual environment with the [`@task.external_python` decorator / ExternalPythonOperator (EPO)](#taskexternal_python-decorator--externalpythonoperator). 
- A dedicated Kubernetes pod with the [`@task.kubernetes` decorator / KubernetesPodOperator (KPO)](#taskkubernetes-decorator--kubernetespodoperator).

Additionally, you can run most traditional operators inside a dedicated Kubernetes pod with the [IsolatedOperator](https://github.com/astronomer/apache-airflow-providers-isolation/) and use [virtual branching operators](#virtual-branching-decorators--operators) to execute conditional task logic inside a virtual environment.

In this guide you'll learn:

- How to use the `@task.virtualenv` decorator / PythonVirtualEnvOperator.
- How to use the `@task.external_python` decorator / ExternalPythonOperator.
- Basic use of the `@task.kubernetes` decorator / KubernetesPodOperator. To learn more about the `@task.kubernetes` decorator and the KubernetesPodOperator, see [Use the KubernetesPodOperator](kubepod-operator.md) and [Run the KubernetesPodOperator on Astro](https://docs.astronomer.io/astro/kubernetespodoperator).
- Execute conditional task logic in a virtual environment with virtual branching operators.
- How to use some Airflow context variables in isolated environments.
- How to use Airflow variables in isolated environments.

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

When creating isolated environments in Airflow, you may not be able to use common Airflow features or connect to your Airflow environment in the same way you would in a regular Airflow task.  

Common limitations include:

- You [cannot pass all Airflow context variables](https://airflow.apache.org/docs/apache-airflow/latest/howto/operator/python.html#id1) to a virtual decorator, since Airflow does not support serializing `var`, `ti` and `task_instance` objects. See, [Use Airflow context variables in isolated environments](#use-airflow-context-variables-in-isolated-environments) 
- You do not have access to your [secrets backend](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html) from within the isolated environment. To access your secrets consider passing them in through [Jinja templating](templating.md). See, [Use Airflow variables in isolated environments](#use-airflow-variables-in-isolated-environments).
- Installing Airflow itself and Airflow provider packages in the environment provided to the `@task.external_python` decorator or the ExternalPythonOperator can lead to unexpected behavior. If you need to use Airflow and Airflow providers module inside your virtual environment, Astronomer recommends to choose the `@task.virtualenv` decorator or the PythonVirtualEnvOperator instead. See, [Use Airflow packages in isolated environments](#use-airflow-packages-in-isolated-environments).

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

To run any Python function in your virtual environment, provide it to the `python_callable` parameter of the ExternalPythonOperator and set the `python` parameter to the location of your Python binary.

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

## @task.kubernetes decorator / KubernetesPodOperator

To use the `@task.kubernetes` decorator or the KubernetesPodOperator, you need provide Docker image as well as have access to a Kubernetes cluster. The example below shows how to use the modules to run in a task in a separate Kubernetes pod inside the same namespace and Kubernetes cluster as your Airflow environment. For more information on how to use the KubernetesPodOperator, see [Use the KubernetesPodOperator](kubepod-operator.md) and [Run the KubernetesPodOperator on Astro](https://docs.astronomer.io/astro/kubernetespodoperator).

<Tabs
    defaultValue="taskflow"
    groupId="task.kubernetes-decorator-kubepodoperator"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">
    
```python
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

## Use Airflow context variables in isolated environments

Some variables from the [Airflow context](airflow-context.md) can be passed to isolated environments, for example the `logical_date` of the DAG run.
Due to compatibility issues, other objects from the context such as `ti` cannot be passed to isolated environments, see the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/latest/howto/operator/python.html#id1).

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

Using Airflow packages inside of isolated environments can lead to unexpected behavior and is not recommended. 

:::

If you need to use Airflow and Airflow providers module inside your virtual environment, use the `@task.virtualenv` decorator or the PythonVirtualEnvOperator instead of the `@task.external_python` decorator or the ExternalPythonOperator.
As of Airflow 2.8 you can cache the virtual environment for reuse by providing a `venv_cache_path` to the `@task.virtualenv` decorator / PythonVirtualEnvOperator.

<Tabs
    defaultValue="taskflow"
    groupId="use-airflow-packages-in-isolated-environments"
    values={[
        {label: '@task.external_python', value: 'taskflow'},
        {label: 'ExternalPythonOperator', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
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

## Use Airflow variables in isolated environments

You can inject Airflow variables into isolated environments by using [Jinja templating](templating.md) in the `op_kwargs` argument of the PythonVirtualenvOperator or ExternalPythonOperator. This is a good way to pass secrets into your isolated environment, which will be masked in the logs according to the rules described in [Hide sensitive information in Airflow variables](airflow-variables.md#hide-sensitive-information-in-airflow-variables).

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