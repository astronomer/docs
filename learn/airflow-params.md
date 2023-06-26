---
title: "Use DAG- and task-level params in Airflow"
sidebar_label: "Params"
description: "Create and access DAG- and task-level params in Airflow."
id: airflow-params
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import tdro_example_upstream from '!!raw-loader!../code-samples/dags/airflow-params/tdro_example_upstream.py';
import tdro_example_downstream from '!!raw-loader!../code-samples/dags/airflow-params/tdro_example_downstream.py';
import simple_param_dag from '!!raw-loader!../code-samples/dags/airflow-params/simple_param_dag.py';

Params are arguments which you can pass to an Airflow DAG or task at runtime and stored in the [Airflow context dictionary](airflow-context.md) for each DAG run. You can pass DAG and task-level params to a DAG run by calling their keywords in `params`.

This guide covers:

- How to pass params to a DAG at runtime.
- How to define DAG-level param defaults which are rendered in the Trigger DAG w/config UI.
- How to access params in an Airflow task.
- The hierarchy of params in Airflow.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow DAGs. See [Introduction to Airflow DAGs](dags.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow context. See [Access the Apache Airflow context](airflow-context.md).

## Pass params to a DAG run at runtime

Params can be passed to a DAG at runtime in three different ways:

- In the Airflow UI by using the **Trigger DAG w/ config** button.
- Running a DAG with the `--conf` flag using the Airflow CLI.
- Using the TriggerDagRunOperator with the `conf` parameter.

Param values passed to a DAG by any of these methods will override existing default values for the same key as long as the [Airflow core config `dag_run_conf_overrides_params`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-run-conf-overrides-params) is set to `True`. 

:::info 

While it's possible to pass non-JSON serializable params, this behavior is deprecated and will be removed in a future release. It is best practice to make sure your params are JSON serializable.

:::

### Trigger DAG w/ config

You can pass params to a DAG from the Airflow UI by clicking on the Play button and selecting **Trigger DAG w/ config**.

![Trigger DAG w/ config](/img/guides/airflow-params_trigger_dag_w_config.png)

![Trigger DAG UI](/img/guides/airflow-params_trigger_dag_ui.png)

The **Trigger DAG w/ config** button opens a UI you can specify details for the DAG run: 

- The **Logical date** of the DAG run can be set to any date that is in between the `start_date` and the `end_date` of the DAG to create DAG runs in the past or future.
- The **Run id** can be set to any string. If no run id is specified, it will be generated based on the type of run (`scheduled`, `dataset_triggered`, `manual` or `backfill`) and the logical date, for example: `manual__2023-06-16T08:03:45+00:00`. 
- You can select configurations from recent DAG runs in the **Select Recent Configurations** dropdown menu.
- For DAG-level params that have a defined default value, a UI element is rendered to set the param value. See also [Define DAG-level params defaults](#define-dag-level-params-defaults).
- From information in the UI elements a Configuration JSON is generated. You can directly edit the **Generated Configuration JSON** in the UI and add any additional params, whether a default has been defined for them or not.

After setting the configuration, you can start the DAG run with the **Trigger** button.

### CLI

When you run an [Airflow DAG from the CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#dags), you can pass params to the DAG run by providing a JSON string to the `--conf` flag. For example, to trigger the `params_default_example` DAG with the value of `Hello from the CLI` for `param1`, run: 

<Tabs
    defaultValue="astro"
    groupId= "cli"
    values={[
        {label: 'Astro CLI', value: 'astro'},
        {label: 'Airflow CLI', value: 'airflow'},
    ]}>
<TabItem value="astro">

```sh
astro dev run dags trigger params_defaults_example --conf '{"param1" : "Hello from the CLI"}'
```

</TabItem>

<TabItem value="airflow">


```sh
airflow dags trigger params_defaults_example --conf '{"param1" : "Hello from the CLI"}'
```

</TabItem>

</Tabs>

The CLI prints configuration for the triggered run to the command line:

![CLI output](/img/guides/airflow-params_cli_param_output.png)

You can use a `--conf` flag with the following Airflow CLI sub-commands:

- `airflow dags backfill`
- `airflow dags test`
- `airflow dags trigger`

### TriggerDagRunOperator

The [TriggerDagRunOperator](cross-dag-dependencies.md#triggerdagrunoperator) is a core Airflow operator that allows you to start a DAG run from within another DAG. You can use the TriggerDAGRunOperator `conf` param to trigger the dependent DAG with a specific configuration.

The DAG below uses the TriggerDagRunOperator to trigger the `tdro_example_downstream` DAG while passing a dynamic value for the `upstream_color` param via the `conf` parameter. The value for `upstream_color` is passed via a [Jinja template](templating.md) pulling the return value of an upstream task via [XCom](airflow-passing-data-between-tasks.md#xcom).

<CodeBlock language="python">{tdro_example_upstream}</CodeBlock>

Runs of the `tdro_example_downstream` DAG that are triggered by this upstream DAG will override the default value of the `upstream_color` param with the value passed via the `conf` parameter, which leads to the `print_color` task to print out one of the values `red`, `green`, `blue` or `yellow`. 

<CodeBlock language="python">{tdro_example_downstream}</CodeBlock>


## Define DAG-level param defaults

To specify params for all runs of a given DAG, pass new default values to the `param` parameter of the `@dag` decorator or the `DAG` class in your DAG file. You can directly specify a default value or use the `Param` class to define a default value with additional attributes.

The DAG below has two DAG-level params with defaults: `param1` and `param2`, the latter only accepting integers.

<CodeBlock language="python">{simple_param_dag}</CodeBlock>

If you trigger an individual DAG run from the Airflow UI, the **Trigger DAG** now renders a form for each param. From here, you can then override your new defaults for individual DAG runs. A param with a red asterisk is a required param.

![Trigger DAG with simple defaults](/img/guides/airflow-params_simple_param_dag_trigger_ui.png)

:::info

When you specify a required `type` for a param, the field will be a required input by default because of [JSON validation](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-dates-times-and-duration). To make a field optional but still require a specific input type, allow NULL values by setting the type to `["null", "<my_type>"]`.

:::

:::info

By default, Airflow assumes that the values provided to a keyword in the `params` dictionary are strings. You can change this behavior by setting the DAG parameter `render_template_as_native_obj=True`. See [Render native Python code](templating.md#render-native-python-code).

:::

### Param types

The following param types are supported:

- `string`: A string. This is the default type.
- `null`: Allows the param to be None by being left empty.
- `integer` or `number`: An integer (floats are not supported).
- `boolean`: `True` or `False`.
- `array`: An HTML multi line text field, every line edited will be made into a string array as the value.
- `object`: A JSON entry field.

### Param attributes

Aside from the `type` attribute, the `Param` class has several other attributes that you can use to define how users interact with the param:

- `title`: The title of the param that appears in the **Trigger DAG** UI.
- `description`: A description of the param.
- `description_html`: A description defined in HTML that can contain links and other HTML elements. Note that adding invalid HTML might lead to the UI not rendering correctly.
- `section`: Creates a section under which the param will appear in the Trigger DAG UI. All params with no specified section will appear under the default section **DAG conf Parameters**.
- `format`: A [JSON format](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-dates-times-and-duration) that Airflow will validate a user's input against.
- `enum`: A list of valid values for a param. Setting this attribute creates a dropdown menu in the UI.
- `const`: Defines a permanent default value and hides the param from the **Trigger DAG** UI. Note that you still need to provide a `default` value for the param.
- `custom_html_form`: Allows you to create custom HTML on top of the provided features.

All `Param` attributes are optional to set. For string type params, you can additionally set `min_length` and `max_length` to define the minimum and maximum length of the input. Similarly, integer and number type params can have a `minimum` and `maximum` value.

### Param examples in the Airflow UI

This section presents a few examples of params and how they are rendered in the **Trigger DAG** UI.

The code snippet below defines a mandatory string param with a few UI elements to help users input a value.

```python
"my_string_param": Param(
    "Airflow is awesome!",
    type="string",
    title="Favorite orchestrator:",
    description="Enter your favorite data orchestration tool.",
    section="Important params",
    min_length=1,
    max_length=200,
)
```

![String param example](/img/guides/airflow-params_string_param_example.png)

When you define [date, datetime, or time param](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6), a calendar picker appears in the **Trigger DAG** UI.

```python
"my_datetime_param": Param(
    "2016-10-18T14:00:00+00:00",
    type="string",
    format="date-time",
),
```

![Datetime param example](/img/guides/airflow-params_datetime_picker.png)

Providing a list of values to the `enum` attribute will create a dropdown menu in the **Trigger DAG** UI. Note that the default value must also be in the list of valid values provided to `enum`. Due to JSON validation rules, a value has to be selected.

```python
"my_enum_param": Param(
    "Hi :)", type="string", enum=["Hola :)", "Hei :)", "Bonjour :)", "Hi :)"]
),
```

![Enum param example](/img/guides/airflow-params_enum_example.png)

A boolean type param will create a toggle in the **Trigger DAG** UI.

```python
 "my_bool_param": Param(True, type="boolean"),
```

![Bool param example](/img/guides/airflow-params_bool.png)

If you provide custom HTML to the `description_html` attribute, you can create more complex UI elements like a color picker. For sample code, see the [the example DAG in the Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/example_dags/example_params_ui_tutorial.html).

![Bool param example](/img/guides/airflow-params_color_picker.png)

## Define task-level param defaults

You can set task-level param defaults in the same way as for DAG-level params. If a param of the same key is specified at both the DAG and task level, the task-level param will take precedence.

<Tabs
    defaultValue="taskflow"
    groupId= "define-task-level-param-defaults"
    values={[
        {label: 'TaskFlow', value: 'taskflow'},
        {label: 'Traditional Operator', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@task(params={"param1": "Hello World!"})
def t1(**context):
    print(context["params"]["param1"])
```

</TabItem>

<TabItem value="traditional">

```python
t1 = BashOperator(
    task_id="t1",
    bash_command="echo {{ params.param1 }}",
    params={"param1": "Hello World!"},
)
```

</TabItem>

</Tabs>


## Access params in a task

You can access params in an Airflow task like you can with other elements in the [Airflow context](airflow-context.md).

<Tabs
    defaultValue="taskflow"
    groupId= "access-params-in-a-task"
    values={[
        {label: 'TaskFlow', value: 'taskflow'},
        {label: 'Traditional Operator', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@task
def t1(**context):
    print(context["params"]["my_param"])
```

</TabItem>

<TabItem value="traditional">

```python
def t1_func(**context):
    print(context["params"]["my_param"])

t1 = PythonOperator(
    task_id="t1",
    python_callable=t1_func,
)
```

</TabItem>

</Tabs>

Params are also accessible as a [Jinja template](templating.md) using the `{{ params.my_param }}` syntax.

If you try to access a param that has not been specified for a specific DAG run, the task will fail with an exception. 

## Param precedence

The order of precedence for params, with the first item taking most precedence, is as follows:

- Params that have been provided for a specific DAG run by a method detailed in [pass params to a DAG run at runtime](#pass-params-to-a-dag-run-at-runtime) as long as the [Airflow config core.dag_run_conf_overrides_params](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-run-conf-overrides-params) is set to `True`.
- Param defaults that have been defined at the task level.
- Param defaults that have been defined at the DAG level.