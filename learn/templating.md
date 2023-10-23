---
title: "Use Airflow templates"
sidebar_label: "Jinja templates"
id: templating
---

<head>
  <meta name="description" content="Learn about Jinja templating in Apache Airflow and see examples of how to pass dynamic information into task instances at runtime. " />
  <meta name="og:description" content="Learn about Jinja templating in Apache Airflow and see examples of how to pass dynamic information into task instances at runtime. " />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Templating allows you to pass dynamic information into task instances at runtime. For example, you can run the following command to print the day of the week every time you run a task:

```python
BashOperator(
    task_id="print_day_of_week",
    bash_command="echo Today is {{ execution_date.format('dddd') }}",
)
```

In this example, the value in the double curly braces `{{ }}` is the templated code that is evaluated at runtime. If you execute this code on a Wednesday, the BashOperator  prints `Today is Wednesday`. Templates have numerous applications. For example, you can use templating to create a new directory named after a task's execution date for storing daily data (`/data/path/20210824`). Alternatively, you can select a specific partition (`/data/path/yyyy=2021/mm=08/dd=24`) so that only the relevant data for a given execution date is scanned.

Airflow leverages [Jinja](https://jinja.palletsprojects.com), a Python templating framework, as its templating engine. In this guide, you'll learn the following:

- How to apply Jinja templates in your code.
- Which variables and functions are available when templating.
- Which operator fields can be templated and which cannot.
- How to validate templates.
- How to apply custom variables and functions when templating.
- How to render templates to strings and native Python code.

:::tip Related Content

- Astronomer Academy: [Airflow: Templating](https://academy.astronomer.io/astro-runtime-templating) module.

:::

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Jinja templating. See [Jinja basics](https://jinja.palletsprojects.com/en/3.1.x/api/#basics). 

## Templating variables in Airflow

Templating in Airflow works the same as Jinja templating in Python. You enclose the code you want evaluated between double curly braces, and the expression is evaluated at runtime. 

Some of the most commonly used Airflow variables that you can use in templates are:

- `{{ ds }}`: The DAG Run’s logical date as `YYYY-MM-DD`.
- `{{ ds_nodash }}`: The DAG run’s logical date as `YYYYMMDD`.
- `{{ data_interval_start }}`: The start of the data interval.
- `{{ data_interval_end }}`: The end of the data interval.

For a complete list of the available variables, see the Airflow [Templates reference](https://airflow.apache.org/docs/apache-airflow/stable/macros-ref.html#default-variables).

## Templateable fields and scripts

Templates cannot be applied to all arguments of an operator. Two attributes in the BaseOperator define where you can use templated values:

- `template_fields`: Defines which operator arguments can use templated values.
- `template_ext`: Defines which file extensions can use templated values.

The following example shows a simplified version of the BashOperator:

```python
class BashOperator(BaseOperator):
    template_fields = ('bash_command', 'env')  # defines which fields are templateable
    template_ext = ('.sh', '.bash')  # defines which file extensions are templateable

    def __init__(
        self,
        *,
        bash_command,
        env: None,
        output_encoding: 'utf-8',
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.bash_command = bash_command  # templateable (can also give path to .sh or .bash script)
        self.env = env  # templateable
        self.output_encoding = output_encoding  # not templateable
```

The `template_fields` attribute holds a list of attributes that can use templated values. You can also find this list in [the Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/bash/index.html#airflow.operators.bash.BashOperator.template_fields) or in the Airflow UI as shown in the following image:

![Rendered Template view](/img/guides/taskinstancedetails.png)

`template_ext` contains a list of file extensions that can be read and templated at runtime. For example, instead of providing a Bash command to `bash_command`, you could provide a `.sh` script that contains a templated value:

```python
run_this = BashOperator(
    task_id="run_this",
    bash_command="script.sh",  # .sh extension can be read and templated
)
```

The BashOperator takes the contents of the following script, templates it, and executes it:

```bash
# script.sh
echo "Today is {{ execution_date.format('dddd') }}"
```

Templating from files speeds development because an integrated development environment (IDE) can apply language-specific syntax highlighting on the script. This wouldn't be possible if your script is defined as a big string of Airflow code.

By default, Airflow searches for the location of your scripts relative to the directory the DAG file is defined in. So, if your DAG is stored in `/path/to/dag.py` and your script is stored in `/path/to/scripts/script.sh`, you would update the value of `bash_command` in the previous example to `scripts/script.sh`.

Alternatively, you can set a base path for templates at the DAG-level with the `template_searchpath` argument. For example, the following DAG would look for `script.sh` at `/tmp/script.sh`:

<Tabs
    defaultValue="taskflow"
    groupId="templateable-fields-and-scripts"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>
<TabItem value="taskflow">

```python
@dag(..., template_searchpath="/tmp")
def my_dag():
    run_this = BashOperator(task_id="run_this", bash_command="script.sh")
```

</TabItem>
<TabItem value="traditional">

```python
with DAG(..., template_searchpath="/tmp") as dag:
    run_this = BashOperator(task_id="run_this", bash_command="script.sh")
```

</TabItem>
</Tabs>

## Validate templates

The output of templates can be checked in both the Airflow UI and Airflow CLI. One advantage of the Airflow CLI is that you don't need to run any tasks before seeing the result.

The Airflow CLI command `airflow tasks render` renders all templateable attributes of a given task. Given a `dag_id`, `task_id`, and random `execution_date`, the command output is similar to the following example:

```bash
$ airflow tasks render example_dag run_this 2021-01-01

# ----------------------------------------------------------
# property: bash_command
# ----------------------------------------------------------
echo "Today is Friday"

# ----------------------------------------------------------
# property: env
# ----------------------------------------------------------
None
```

For this command to work, Airflow needs access to a metadata database. To set up a local SQLite database, run the following commands:

```bash
cd <your-project-directory>
export AIRFLOW_HOME=$(pwd)
airflow db migrate  # generates airflow.db, airflow.cfg, and webserver_config.py in your project dir
                    # note that in Airflow versions pre-2.7 you'll need to use `airflow db init` instead

# airflow tasks render [dag_id] [task_id] [execution_date]
```

If you use the Astro CLI, a postgres metadata database is automatically configured for you after running `astro dev start` in your project directory. From here, you can run `astro dev run tasks render <parameters>` to test your templated values. 

For most templates, this is sufficient. However, if an external system such as a variable in your production Airflow metadata database is reached by the templating logic, you must have connectivity to it.

To view the result of templated attributes after running a task in the Airflow UI, click a task and then click **Rendered** as shown in the following image:

![Rendered button in the task instance popup](/img/guides/renderedbutton.png)

The Rendered Template view and the output of the templated attributes are shown in the following image:

![Rendered Template view](/img/guides/renderedtemplate.png)

## Macros: using custom functions and variables in templates

As discussed previously, there are several variables available during templating. A Jinja environment and Airflow runtime are different. You can view a Jinja environment as a very stripped-down Python environment. That, among other things, means modules cannot be imported. For example, this command won't work in a Jinja template:

```python
from datetime import datetime

BashOperator(
    task_id="print_now",
    # raises jinja2.exceptions.UndefinedError: 'datetime' is undefined
    bash_command="echo It is currently {{ datetime.now() }}",
)
```

However, it is possible to inject functions into your Jinja environment. In Airflow, several standard Python modules are injected by default for templating, under the name macros. For example, the previous code example can be updated to use `macros.datetime`:

```python
BashOperator(
    task_id="print_now",
    # It is currently 2021-08-30 13:51:55.820299
    bash_command="echo It is currently {{ macros.datetime.now() }}",  
)
```

Airflow includes some pre-injected functions out of the box for you to use in your templates. See [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#macros) for a list of available functions. You can also load information in JSON format using `"{{ macros.json.loads(...) }}"` and information in YAML format using `"{{ macros.yaml.safe_load(...) }}"`.
Besides pre-injected functions, you can also use self-defined variables and functions in your templates. Airflow provides a convenient way to inject these into the Jinja environment. In the following example, a function is added to the DAG to print the number of days since May 1st, 2015:

```python
def days_to_now(starting_date):
    return (datetime.now() - starting_date).days
```

To use this inside a Jinja template, you can pass a dict to `user_defined_macros` in the DAG. For example:

```python
def days_to_now(starting_date):
    return (datetime.now() - starting_date).days


@dag(
    start_date=datetime(2021, 1, 1),
    schedule=None,
    user_defined_macros={
        "starting_date": datetime(2015, 5, 1),  # Macro can be a variable
        "days_to_now": days_to_now,  # Macro can also be a function
    },
)
def demo_template():
    print_days = BashOperator(
        task_id="print_days",
        # Call user defined macros
        bash_command="echo Days since {{ starting_date }} is {{ days_to_now(starting_date) }}",  
    )
    # Days since 2015-05-01 00:00:00 is 2313


demo_template():

```

It's also possible to inject functions as Jinja [filters](https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Environment.filters) using `user_defined_filters`. You can use filters as pipe-operations. The following example completes the same work as the previous example, only this time filters are used:

```python
@dag(
    start_date=datetime(2021, 1, 1),
    schedule=None,
    # Set user_defined_filters to use function as pipe-operation
    user_defined_filters={"days_to_now": days_to_now},  
    user_defined_macros={"starting_date": datetime(2015, 5, 1)},
)
def bash_script_template():
    print_days = BashOperator(
        task_id="print_days",
        # Pipe value to function
        bash_command="echo Days since {{ starting_date }} is {{ starting_date | days_to_now }}", 
    )
    # Days since 2015-05-01 00:00:00 is 2313


bash_script_template()

```

Functions injected with `user_defined_filters` and `user_defined_macros` are both usable in the Jinja environment. While they achieve the same result, Astronomer recommends using filters when you need to import multiple custom functions because the filter formatting improves the readability of your code. You can see this when comparing the two techniques side-to-side:

```python
"{{ name | striptags | title }}"  # chained filters are read naturally from left to right
"{{ title(striptags(name)) }}"  # multiple functions are more difficult to interpret because reading right to left
```

## Render native Python code

By default, Jinja templates always render to Python strings. Sometimes it's desirable to render templates to native Python code. When the code you're calling doesn't work with strings, it can cause issues. For example:

```python
def sum_numbers(*args):
    total = 0
    for val in args:
        total += val
    return total

sum_numbers(1, 2, 3)
# returns 6
sum_numbers("1", "2", "3")
# TypeError: unsupported operand type(s) for +=: 'int' and 'str'
```

Consider a scenario where you're passing a list of values to this function by triggering a DAG with a config that holds some numbers:

```python
@dag(
    start_date=datetime.datetime(2021, 1, 1),
    schedule=None,
    catchup=False
)
def failing_template():
    PythonOperator(
        task_id="sumnumbers",
        python_callable=sum_numbers,
        op_args="{{ dag_run.conf['numbers'] }}",
    )


failing_template()

```

You would trigger the DAG with the following JSON to the DAG run configuration:

```json
{"numbers": [1,2,3]}
```

The rendered value is a string. Since the `sum_numbers` function unpacks the given string, it ends up trying to add up every character in the string:

```python
('[', '1', ',', ' ', '2', ',', ' ', '3', ']')
```

This is not going to work, so you must tell Jinja to return a native Python list instead of a string. Jinja supports this with Environments. The [default Jinja environment](https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Environment) outputs strings, but you can configure a [NativeEnvironment](https://jinja.palletsprojects.com/en/3.0.x/nativetypes/#jinja2.nativetypes.NativeEnvironment) to render templates as native Python code.

Support for Jinja's NativeEnvironment was added in [Airflow 2.1.0](https://github.com/apache/airflow/pull/14603) with the `render_template_as_native_obj` argument on the DAG class. This argument takes a boolean value which determines whether to render templates with Jinja's default Environment or NativeEnvironment. For example:

```python
def sum_numbers(*args):
    total = 0
    for val in args:
        total += val
    return total


@dag(
    dag_id="native_templating",
    start_date=datetime.datetime(2021, 1, 1),
    schedule=None,
    # Render templates using Jinja NativeEnvironment
    render_template_as_native_obj=True,
)
def native_templating()
    sumnumbers = PythonOperator(
        task_id="sumnumbers",
        python_callable=sum_numbers,
        op_args="{{ dag_run.conf['numbers'] }}",
    )

native_templating()

```

Passing the same JSON configuration `{"numbers": [1,2,3]}` now renders a list of integers which the `sum_numbers` function processes correctly:

```text
[2021-08-26 11:53:12,872] {python.py:151} INFO - Done. Returned value was: 6
```

The Jinja environment must be configured on the DAG-level. This means that all tasks in a DAG render either using the default Jinja environment or using the NativeEnvironment.
