---
title: "Custom hooks and operators"
sidebar_label: "Custom hooks and operators"
description: "How to correctly import custom hooks and operators."
id: airflow-importing-custom-hooks-operators
---

import CodeBlock from '@theme/CodeBlock';
import custom_operator_example from '!!raw-loader!../code-samples/dags/airflow-importing-custom-hooks-operators/custom_operator_example.py';

One of the great benefits of Airflow is its vast network of provider packages that provide hooks, operators, and sensors for many common use cases. Another great benefit of Airflow is that it is highly customizable because everything is defined in Python code. If a hook, operator, or sensor you need doesn't exist in the open source, you can easily define your own. 

In this guide, you'll learn how to define your own custom code. Then, you'll make your custom code available to your DAGs. You'll be using custom operators in your primary example, but the same concepts are applicable to custom hooks and sensors.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow hooks. See [Hooks 101](what-is-a-hook.md).
- Managing Airflow project structure. See [Managing Airflow code](managing-airflow-code.md).

## Define a custom operator

At a high level, creating a custom operator is straightforward. At a minimum, all custom operators must:

- Inherit from the `BaseOperator`.
- Define `Constructor` and `Execute` classes.

The code appears similar to the following:

```python
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from hooks.my_hook import MyHook


class MyOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 my_field,
                 *args,
                 **kwargs):
        super(MyOperator, self).__init__(*args, **kwargs)
        self.my_field = my_field

    def execute(self, context):
        hook = MyHook('my_conn')
        hook.my_method()
```

If your custom operator is modifying functionality of an existing operator, your class can inherit from the operator you are building on instead of the `BaseOperator`. For more detailed instructions on defining custom operators, see the [Apache Airflow How-to Guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html).

## Import custom operators

After you've defined your custom operator, you need to make it available to your DAGs. Some legacy Airflow documentation or forums may reference registering your custom operator as an Airflow plugin, but this is not necessary. To import  a custom operator into your DAGs, the file containing your custom operator needs to be in a directory that is present in your `PYTHONPATH`.

By default, Airflow adds the `dags/` and `plugins/` directories in a project to the `PYTHONPATH`, so those are the most natural choices for storing custom operator files (check out the Apache Airflow [Module Management docs](https://airflow.apache.org/docs/apache-airflow/stable/modules_management.html) for more info). Your project structure may vary depending on your team and your use case. Astronomer uses the following structure, where custom operator files live in the `plugins/` directory with sub-folders for readability.

```bash
.
├── dags/                    
│   └── example-dag.py
├── Dockerfile                  
├── include/                 
│   └── sql/
│       └── transforms.sql
├── packages.txt     
├── plugins/             
│   ├── operators/
│   │   └── my_operator.py
│   └── sensors/
│       └── my_sensor.py
└── requirements.txt    
```

For more details on why Astronomer recommends this project structure, see the [Managing Airflow Code guide](managing-airflow-code.md).

:::tip

If you use an IDE and don't want to see import errors, add the `plugins` directory as a source root.

:::

After you've added your custom operators to the project, you can import them into your DAG like you would any other Python package:

<CodeBlock language="python">{custom_operator_example}</CodeBlock>

And that's it! Your DAG will use `MyOperator` and `MySensor` when it runs, giving you full flexibility over what happens in your pipelines.
