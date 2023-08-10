---
title: "Use Airflow variables"
sidebar_label: "Variables"
description: "Create and use Airflow variables."
id: airflow-variables
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

An Airflow variable is a key-value pair that can be used to store information in your Airflow environment. They are commonly used to store instance level information that rarely changes, including secrets like an API key or the path to a configuration file. 

There are two distinct types of Airflow variables: regular values and JSON serialized values. 

![Variables in the Airflow UI](/img/guides/airflow-variables_variables_in_UI.png)

This concept guide covers how to create Airflow variables and access them programmatically.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow DAGs. See [Introduction to Airflow DAGs](dags.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## Best practices for storing information in Airflow

[Airflow variables](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/variables.html#variables) store key-value pairs or short JSON objects that need to be accessible in your whole Airflow instance. They are Airflow’s runtime configuration concept and defined using the [`airflow.model.variable`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/variable/index.html#module-airflow.models.variable) object. 

There are some best practices to keep in mind when using Airflow variables:

- Airflow variables should be used for information that is runtime dependent but doesn't change too frequently.
- You should avoid using Airflow variables outside of tasks in top-level DAG code, as they will create a connection to the Airflow metastore every time the DAG is parsed, which can lead to performance issues. See [DAG writing best practices in Apache Airflow](dag-best-practices.md#avoid-top-level-code-in-your-dag-file).
- If you do use Airflow variables in top-level DAG code, use the [Jinja template](templating.md) syntax so that your Airflow variables are only rendered when a task executes.
- Airflow variables are encrypted with [Fernet](https://github.com/fernet/spec/) when they are written to the Airflow metastore. To mask Airflow variables in the UI and logs, include a substring indicating a sensitive value in your Airflow variable name. See [Hiding sensitive information](#hiding-sensitive-information).

See the Airflow documentation for examples of code showing [good and bad practices for accessing Airflow variables in a DAG](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#airflow-variables).

Aside from Airflow variables, there are other ways of storing information in Airflow. The ideal option depends on what type of information you are storing and where and how you want to access it:

- Environment variables store small pieces of information that are available to the whole Airflow environment. There is no direct way to see environment variables in the Airflow UI but they can be accessed using `os.getenv("MY_ENV_VAR")` inside of Airflow DAGs and tasks. Environment variables are very versatile, as they can be used to both store arbitrary information and [configure Airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html). One advantage of using environment variables is that you can include their creation in your CI/CD process. They are also often used to store credentials for local development.
- [Params](airflow-params.md) can be used to store information specific to a DAG or DAG run. You can define defaults for params at the DAG or task level and override them at runtime. Params are not encrypted and should not be used to store secrets.
- [XComs](airflow-passing-data-between-tasks.md) can be used to pass small pieces of information between Airflow tasks. Use XComs when the information is likely to change with each DAG run and mostly needs to be accessed by individual tasks in or outside of the DAG from within which the XCom is created. Default XComs are not encrypted and should not be used to store secrets.


## Create an Airflow variable

There are several ways to create Airflow variables:

- Using the Airflow UI
- Using the Airflow CLI.
- Using an environment variable.
- Programmatically from within an Airflow task.

To create an Airflow variable in the UI, click on the **Admin** tab and select **Variables**. Then click on the **+** button and enter a key, value and an optional description for your Airflow variable. You also have the option to **Import Variables** from a file.

![UI](/img/guides/airflow-variables_UI_600.png) 

The Airflow CLI contains options to set, get and delete [Airflow variables](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#variables). To create an Airflow variable via the CLI use the following command:

<Tabs
    defaultValue="astro"
    groupId= "create-an-airflow-variable"
    values={[
        {label: 'Astro CLI', value: 'astro'},
        {label: 'Airflow CLI', value: 'airflow'},
    ]}>
<TabItem value="astro">

```sh
astro dev run variables set my_var my_value
astro dev run variables set -j my_json_var '{"key": "value"}'
```

Note that [`astro dev run`](https://docs.astronomer.io/astro/cli/astro-dev-run) executes Airflow commands only in your local Airflow environment and can't be used on Astro Deployments. To set Airflow variables for an Astro Deployment, either create them using the Deployment's Airflow UI or using [Astro environment variables](https://docs.astronomer.io/astro/environment-variables).

</TabItem>

<TabItem value="airflow">


```sh
airflow variables set my_var my_value
airflow variables set -j my_json_var '{"key": "value"}'
```

</TabItem>

</Tabs>

To set Airflow variables via an environment variable create an environment variable with the prefix `AIRFLOW_VAR_` + the name of the Airflow variable you want to set

```text
AIRFLOW_VAR_MYREGULARVAR='my_value'
AIRFLOW_VAR_MYJSONVAR='{"hello":"world"}'
```

To learn more about how to set environment variables on Astro, see [Environment Variables](https://docs.astronomer.io/astro/environment-variables).

Lastly, you can programmatically set Airflow variables within your Airflow tasks via the [`Variable` model](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/variable/index.html#module-airflow.models.variable). If you want to serialize a JSON value, make sure to set `serialize_json=True`.

<Tabs
    defaultValue="taskflow"
    groupId="create-an-airflow-variable-2"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@task
def set_var():
    from airflow.models import Variable
    Variable.set(key="my_regular_var", value="Hello!")
    Variable.set(key="my_json_var", value={"num1": 23, "num2": 42}, serialize_json=True)
```

</TabItem>
<TabItem value="traditional">


```python
def set_var_func():
    from airflow.models import Variable
    Variable.set(key="my_regular_var", value="Hello!")
    Variable.set(key="my_json_var", value={"num1": 23, "num2": 42}, serialize_json=True)


PythonOperator(
    task_id="set_var",
    python_callable=set_var_func,
)
```

</TabItem>

</Tabs>


Updating an Airflow variable works the same way by using the `.update()` method.

## Retrieving an Airflow variable

To programmatically retrieve an Airflow variable, you can either use the `.get()` method of the Airflow variable model or you can pull the Airflow variable value directly from the [Airflow context](airflow-context).

When retrieving a JSON serialized Airflow variable, make sure to set `deserialize_json=True` in the `.get()` method or access the `json` key from the `var` dictionary in the Airflow context.

<Tabs
    defaultValue="taskflow"
    groupId="retrieving-an-airflow-variable"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@task
def get_var_regular():
    from airflow.models import Variable
    my_regular_var = Variable.get("my_regular_var", default_var=None)
    my_json_var = Variable.get(
        "my_json_var", deserialize_json=True, default_var=None
    )["num1"]
    print(my_regular_var)
    print(my_json_var)

@task
def get_var_from_context(**context):
    my_regular_var = context["var"]["value"].get("my_regular_var")
    my_json_var = context["var"]["json"].get("my_json_var")["num2"]
    print(my_regular_var)
    print(my_json_var)
```

</TabItem>
<TabItem value="traditional">


```python
def get_var_regular_func():
    from airflow.models import Variable
    my_regular_var = Variable.get("my_regular_var", default_var=None)
    my_json_var = Variable.get(
        "my_json_var", deserialize_json=True, default_var=None
    )["num1"]
    print(my_regular_var)
    print(my_json_var)


def get_var_from_context_func(**context):
    my_regular_var = context["var"]["value"].get("my_regular_var")
    my_json_var = context["var"]["json"].get("my_json_var")["num2"]
    print(my_regular_var)
    print(my_json_var)


PythonOperator(
    task_id="get_var_regular",
    python_callable=get_var_regular_func,
)

PythonOperator(
    task_id="get_var_from_context",
    python_callable=get_var_from_context_func,
)
```

</TabItem>

</Tabs>

When using traditional Airflow operators, it's often easier to use a [Jinja template](templating.md) to retrieve Airflow variables. See [Airflow variables in Templates](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#airflow-variables-in-templates).

```python
get_var_jinja = BashOperator(
    task_id="get_var_jinja",
    bash_command='echo "{{ var.value.my_regular_var }} {{ var.json.my_json_var.num2 }}"',
)
```

You can also retrieve an Airflow variable using the Airflow CLI's [`get`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#get_repeat3) and [`list`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#list_repeat8) commands. 

## Hide sensitive information in Airflow variables

Airflow variables are [Fernet](https://github.com/fernet/spec/) encrypted in the Airflow metastore.

As seen in the screenshot at the beginning of this guide, some Airflow variables are additionally masked in the Airflow UI and logs. By default, the [`hide_sensitive_var_conn_fields`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#hide-sensitive-var-conn-fields) configuration is set to `True`, which automatically masks all Airflow variables that contain the following strings:

- `access_token`
- `api_key`
- `apikey`
- `authorization`
- `passphrase`
- `passwd`
- `password`
- `private_key`
- `secret`
- `token`

This list can be extended by adding comma separated strings to the [`sensitive_var_conn_names`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#sensitive-var-conn-names) configuration. See [Masking sensitive data](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/secrets/mask-sensitive-values.html).

On Astro you can also manually mark Airflow variables as secrets when creating them as an environment variable. See [Set environment variables on Astro](https://docs.astronomer.io/astro/environment-variables).

:::info

If you need to access the same sensitive information in several Airflow instances, consider using a [Secrets Backend](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/secrets/secrets-backend/index.html).

:::