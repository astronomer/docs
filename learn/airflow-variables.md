---
title: "Use Airflow Variables"
sidebar_label: "Variables"
description: "Create and use Airflow Variables."
id: airflow-variables
---

An Airflow variable is a key-value pair that can be used to store information in your Airflow environment. They are commonly used to store instance level information that rarely changes, including secrets like for example an API key or the path to a configuration file. Airflow variables are [Fernet](https://github.com/fernet/spec/) encrypted and can also be retrieved from a [secrets backend](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/secrets/secrets-backend/index.html).

There are two distinct types of Airflow variables, regular values and JSON serialized values. 

This concept guide covers how to create Airflow variables and access them programmatically.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow DAGs. See [Introduction to Airflow DAGs](dags.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## Best practices for storing information in Airflow

Airflow offers several ways to store your information, including variables. The ideal option often depends on what type of information you are storing and where and how you want to access it:

- Environment variables store small pieces of information that you want to be available in your whole Airflow environment. The advantage of using environment variables is that you can include their creation in your CI/CD process. Environment variables are the only type of variable storage that can be accessed in top-level DAG code. Note that unless you create an Airflow variable via the environment variable by starting it with `AIRFLOW_VAR_` you will not be able to view or update it in the Airflow UI. 
- Airflow variables store key-value pairs or short JSON objects that need to be accessible in your whole Airflow environment. It is best practice to use Airflow variables for information that is runtime dependent but does not change too frequently. Airflow variables are also encrypted, making them suitable for storing secrets.
- [Params](airflow-params.md) can be used to store variables that are specific to a DAG or DAG run. You can define defaults for params at the DAG or task level and override them at runtime. Params are not encrypted and should not be used to store secrets.
- [XComs](airflow-passing-data-between-tasks.md) can be used to pass small pieces of information between Airflow tasks. Use XComs when the information is likely to change with each DAG run and mostly needs to be accessed by individual tasks in or outside of the DAG from within which the XCom is created.

## Create an Airflow variable

There are several ways to create Airflow variables:

- Using the Airflow UI
- Using the Airflow CLI.
- Using an environment variable.
- Using the `airflow_settings.yaml` file (Astro CLI users).
- Programmatically from within an Airflow task.

To create an Airflow Variable in the UI, click on the **Admin** tab and select **Variables**. Then click on the **+** button and enter a key, value and an optional description for your variable. You also have the option to **Import Variables** from a file.

![UI](/img/guides/airflow-variables_UI.png)

The Airflow CLI contains options to set, get and delete [Airflow variables](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#variables). To create a variable via the CLI use the following command:

<Tabs
    defaultValue="astro"
    groupId= "create-airflow-variable"
    values={[
        {label: 'Astro CLI', value: 'astro'},
        {label: 'Airflow CLI', value: 'airflow'},
    ]}>
<TabItem value="astro">

```sh
astro dev run variables set my_var my_value
astro dev run variables set -j my_json_var '{"key": "value"}'
```

</TabItem>

<TabItem value="airflow">


```sh
airflow variables set my_var my_value
airflow variables set -j my_json_var '{"key": "value"}'
```

</TabItem>

</Tabs>

To set Airflow variables via an environment variable create an environment variable with the prefix `AIRFLOW_VAR_` + the name of the variable you want to set

```text
AIRFLOW_VAR_MYREGULARVAR='my_value'
AIRFLOW_VAR_MYJSONVAR='{"hello":"world"}'
```

Astro CLI users can create Airflow variables from the `airflow_settings.yaml` file. 

```yaml
  variables:
    - variable_name: my_regular_variable_key
      variable_value: my_value
    - variable_name: my_json_variable_key
      variable_value: '{"hello":"world"}'
```

Lastly, you can programmatically set Variables within your Airflow tasks via the [Variable model](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/variable/index.html#module-airflow.models.variable). If you want to serialize a JSON value, make sure to set `serialize_json=True`.

```python
@task
def set_var():
    from airflow.models import Variable
    Variable.set(key="my_regular_var", value="Hello!")
    Variable.set(key="my_json_var", value={"num1": 23, "num2": 42}, serialize_json=True)
```

Updating an Airflow variable works the same way by using the `.update()` method.

## Retrieving an Airflow variable

To programmatically retrieve an Airflow variable, you can either use the `.get()` method of the Airflow Variable model or you can pull the Variable value directly from the [Airflow context](airflow-context).

When retrieving a JSON serialized variable, make sure to set `deserialize_json=True` in the `.get()` method or access the `json` key from the `var` dictionary in the Airflow context.

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

For using Airflow variables in traditional Airflow operators it is often easier to use a [Jinja template](templating.md). See also [Airflow Variables in Templates](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#airflow-variables-in-templates).

```python
get_var_jinja = BashOperator(
    task_id="get_var_jinja",
    bash_command='echo "{{ var.value.my_regular_var }} {{ var.json.my_json_var.num2 }}"',
)
```

You can also retrieve an Airflow variable via the Airflow CLI's [`get`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#get_repeat3) and [`list`](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#list_repeat8) commands. 