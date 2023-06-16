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

Params are arguments which are passed to an Airflow DAG or task at runtime and stored in the [Airflow context dictionary](airflow-context.md) of a specific DAG run. Both DAG- and task-level params can be passed to a DAG run using the respective `params` keyword.

This concept guide covers:

- Different of passing params to a DAG at runtime.
- How to define DAG-level params defaults which are rendered in the Trigger DAG w/config UI.
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
- Through Airflow CLI commands that run a DAG by using the `--conf` flag.
- Through a TriggerDagRunOperator by using the `conf` parameter.

Params values passed to a DAG by any of these methods will override existing default values for the same key as long as the [Airflow core config `dag_run_conf_overrides_params`](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-run-conf-overrides-params) is set to `True`. 

:::info 

While passing non-JSON serializable params is possible, this behavior is deprecated and will be removed in a future release. It is best practice to make sure your params are JSON serializable.

:::

### Trigger DAG w/ config

Params can be passed to a DAG from the Airflow UI by clicking on the Play button and selecting **Trigger DAG w/ config**.

![Trigger DAG w/ config](/img/guides/airflow-params_trigger_dag_w_config.png)

![Trigger DAG UI](/img/guides/airflow-params_trigger_dag_ui.png)

The **Trigger DAG w/ config** button opens a UI where details for a DAG run can be specified: 

- The **Logical date** of the DAG run can be set to any date that is in between the `start_date` and the `end_date` of the DAG to create DAG runs in the past or future.
- The **Run id** can be set to any string. If no run id is specified the run id will be generated based on the type of run (`scheduled`, `dataset_triggered`, `manual` or `backfill`) and the logical date of the run, for example: `manual__2023-06-16T08:03:45+00:00`. 
- You can select configurations from recent DAG runs in the **Select Recent Configurations** dropdown menu.
- For DAG-level params that have a defined default a UI element is rendered to set the param value. See also [Define DAG-level params defaults](#define-dag-level-params-defaults).
- From information in the UI elements a Configuration JSON is generated. You can directly edit the **Generated Configuration JSON** in the UI and add any additional params, whether a default has been defined for them or not.

After setting the configuration you can start the DAG run with the **Trigger** button.

### CLI

When running an [Airflow DAG from the CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#dags) you can pass params to the DAG run by providing a JSON string to the `--conf` flag. For example to trigger the `params_default_example` DAG with the value of `Hello from the CLI` for the `param1` run: 

<Tabs
    defaultValue="astro"
    groupId= "airflow-cli"
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

The configuration for the triggered run will be printed into the command line:

![CLI output](/img/guides/airflow-params_cli_param_output.png)

The Airflow CLI sub-commands with a `--conf` flag are:

- `airflow dags backfill`
- `airflow dags test`
- `airflow dags trigger`

### TriggerDagRunOperator

The TriggerDagRunOperators is a core Airflow operator that allows you to kick of a DAG run from within another DAG. Two key use cases of the TriggerDagRunOperator are to trigger another DAG and wait for its completion and to be able to trigger another DAG with a specific configuration. You can learn more about the TriggerDagRunOperator in the [Cross-DAG dependencies](cross-dag-dependencies.md#triggerdagrunoperator) guide. 

The code below shows a simple DAG `tdro_example_upstream` that uses the TriggerDagRunOperator to trigger the `tdro_example_downstream` DAG while passing a dynamic value for the `upstream_color` param to the downstream DAG via the `conf` parameter. The value for `upstream_color` is passed via a [Jinja template](templating.md) pulling the return value of an upstream task via [XCom](airflow-passing-data-between-tasks.md#xcom).

<CodeBlock language="python">{tdro_example_upstream}</CodeBlock>

Runs of the `tdro_example_downstream` DAG which are triggered by this upstream DAG will override the default value of the `upstream_color` param with the value passed via the `conf` parameter, which leads to the `print_color` task to print out one of the values `red`, `green`, `blue` or `yellow`. 

<CodeBlock language="python">{tdro_example_downstream}</CodeBlock>

This functionality is one of several ways to pass information between your DAGs. Note that you can also use XCom across different DAGs.

## Define DAG-level params defaults

Default values for DAG-level params can be created by passing them to the `param` parameter of the `@dag` decorator or the `DAG` class in your DAG file. You can directly specify a default value or use the `Param` class to define a default value with additional attributes.

The DAG below has two DAG-level params with a defined default: `param1` and `param2`, the latter having been defined to only accept integers.

<CodeBlock language="python">{simple_param_dag}</CodeBlock>

The Trigger DAG UI will render an element for each param with the respective default. A param with a red asterisk is a required param.

![Trigger DAG with simple defaults](/img/guides/airflow-params_simple_param_dag_trigger_ui.png)

:::info

By default values provided to a keyword in the `params` dictionary are assumed to be strings. You can change this behavior by setting the DAG parameter `render_template_as_native_obj=True`. See also [Render native Python code](templating.md#render-native-python-code).

:::

### Param types

Params can support one or more of seven types:

- `string`: A string. This is the default type.
- `null`: Allows the param to be None by being left empty.
- `integer` or `number`: An integer (floats are not supported).
- `boolean`: `True` or `False`.
- `array`: A HTML multi line text field, every line edited will be made into a string array as value
- `object`: A JSON entry field.

:::info

When a `type` is specified for a Param the field will turn into a required input by default because of [JSON validation](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-dates-times-and-duration). To make a field optional allow NULL values by setting the type to `["null", "<my_type>"]`.

:::

### Param attributes

Aside from the `type` attribute the `Param` class has several other attributes that can be used to define a default value:

- `title`: The title of the param that will be displayed in the Trigger DAG UI instead of the param key when specified.
- `description`: A description of the param where further instructions can be added.
- `description_html`: A description that will be rendered in html format that can contain links and other html elements. Note that adding invalid HTML might lead to the UI not rendering correctly.
- `section`: Creates a section under which the param will be displayed in the Trigger DAG UI. All params with no specified section will be displayed under the default section **DAG conf Parameters**.
- `format`: a [JSON format](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-dates-times-and-duration) the input will be validated against.
- `enum`: A defined list of valid values for a param. Setting this attribute will create a dropdown menu in the Trigger DAG UI.
- `const`: Setting this attribute to a valid value will make that value a constant default and hide the param from the Trigger DAG UI. Note that you still need to provide a `default` value for the param.
- `custom_html_form`: Allows you to create custom HTML on top of the provided features.

All Param attributes are optional to set. For Params of the type string you can additionally set `min_length` and `max_length` to define the minimum and maximum length of the input. Similarly Params of the types `integer` and `number` can have a `minimum` and `maximum` value.

### Param default examples

This section presents a few examples of Param defaults and how they are rendered in the Trigger DAG UI.

The code snippet below defines a mandatory param of the type `string` with UI elements like the section and title specified.

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

By defining a [valid date, datetime or time format](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6) you can create a calendar picker in the Trigger DAG UI.

```python
"my_datetime_param": Param(
    "2016-10-18T14:00:00+00:00",
    type="string",
    format="date-time",
),
```

![Datetime param example](/img/guides/airflow-params_datetime_picker.png)

Providing a list of values to the `enum` attribute will create a dropdown menu in the Trigger DAG UI. Note that the default value must also be in the list of valid values provided to `enum`. Due to JSON validation rules, a value has to be selected.

```python
"my_enum_param": Param(
    "Hi :)", type="string", enum=["Hola :)", "Hei :)", "Bonjour :)", "Hi :)"]
),
```

![Enum param example](/img/guides/airflow-params_enum_example.png)

A boolean type param will create a toggle in the Trigger DAG UI.

```python
 "my_bool_param": Param(True, type="boolean"),
```

![Bool param example](/img/guides/airflow-params_bool.png)

Lastly, by providing custom HTML to the `description_html` attribute you can create more complex UI elements like a color picker. You can find the code which created the UI element below in [this example DAG in the Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/example_dags/example_params_ui_tutorial.html).

![Bool param example](/img/guides/airflow-params_color_picker.png)

## Define task-level param defaults

Defaults for a param at the task level can be set in the same manner as for DAG-level params. If a param of the same key is specified at the DAG- and task-level, the task-level param will take precedence.

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

You can access params in an Airflow task like other elements in the [Airflow context](airflow-context.md).

<Tabs
    defaultValue="taskflow"
    groupId= "define-task-level-param-defaults"
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

If you try to access a param that has not been specified for a specific DAG run the task will fail with an exception. 

The order of precedence for params is as follows:

- Params that have been provided for a specific DAG run by a method detailed in [pass params to a DAG run at runtime](#pass-params-to-a-dag-run-at-runtime) as long as the [Airflow config core.dag_run_conf_overrides_params](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dag-run-conf-overrides-params) is set to `True`.
- Param defaults that have been defined at the task level.
- Param defaults that have been defined at the DAG level.