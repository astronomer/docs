---
title: "Import plugins to Airflow"
sidebar_label: "Plugins"
description: "How to use Airflow plugins."
id: using-airflow-plugins
---

Plugins are external features that you can add to customize your Airflow installation. Astro CLI users can import custom plugins by adding them to the `/plugins` folder of their Airflow project. 

In this concept guide you'll learn how to add a plugin to your Airflow instance as well as what components can be part of a plugin.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow core components. See [Airflow's components](airflow-components.md).
- Jinja templating in Airflow. See [Using Airflow templates](templating.md).

## Plugin interface




```python
from airflow.plugins_manager import AirflowPlugin

class MyAirflowPlugin(AirflowPlugin):
    # name your plugin
    name = "my_plugin_name"

    ## Add plugin components
    # ...
    # ...
    # ...

    # Add an optional callback to perform actions when airflow starts and
    # the plugin is loaded.
    # NOTE: Ensure your plugin has *args, and **kwargs in the method definition
    #   to protect against extra parameters injected into the on_load(...)
    #   function in future changes
    def on_load(*args, **kwargs):
        # ... perform Plugin boot actions
        pass
```


## Plugin components



:::info

Before Airflow 2.0 custom operators and hooks were added as plugins. This pattern has been deprecated and [custom operators and hooks](https://docs.astronomer.io/learn/airflow-importing-custom-hooks-operators) can now be simply by importing a script located in `/include`.

:::

### Hooks

### Macros

### Flask Blueprints

### Appbuilder views

### Appbuilder menu items

### Global operator extra links

### Operator extra links

Operator extra links are additional buttons with links that can be added to specific operators. The screenshot below shows an operator extra link called "HTTP cat" having been added to the custom CatHttpOperator. See also this [step-by-step tutorial](operator-extra-link-tutorial.md) on how to add operator extra links.

![Cat Button](/img/guides/extra_links_tutorial_cat_button.png)

The 

```python
# create the operator extra link
class MyLink(BaseOperatorLink):
    
    # name the link button
    name = "My extra link"

    # add the link button to one or more operators
    operators = [MyOperator1, MyOperator2]

    # function determining the link
    def get_link(self, operator, *, ti_key=None):
        return "http://my_link.com/"

# add the operator extra link to a plugin
class MyAirflowPlugin(AirflowPlugin):
    name = "my_plugin_name"
    operator_extra_links = [
        MyLink(),
    ]

```

### Timetables

### Listeners

### .on_load() method



### Macros

[Macros](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#macros) are used to pass dynamic information into task instances at runtime with templating. You can use pre-built macros in Airflow or import custom macros through the `plugins` directory. 

A current limitation of Airflow is that every global variable or top-level method in a DAG file is interpreted every cycle during the DAG processing loop on the scheduler. While the loop execution time can vary from seconds to minutes, the majority of code should only be interpreted in a task at execution time.

Macros are a tool in Airflow that extend Airflow [templating](https://airflow.apache.org/tutorial.html#templating-with-jinja) capabilities to offload runtime tasks to the executor instead of the scheduler loop. The following are some example macros:

- Timestamp formatting of last or next execution for incremental ETL.
- Decryption of a key used for authentication to an external system.
- Accessing custom user-defined params

A template always returns a string.

### Blueprints and views

The Airflow [blueprints](http://flask.pocoo.org/docs/0.12/blueprints/) and [views](http://flask.pocoo.org/docs/0.12/views/) components are extensions of blueprints and views in the Flask web app framework. Developers have extended the Airflow API to include triggering a DAG run remotely, adding new connections, or modifying [Airflow variables](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html). You can extend this to build an entire web app which sits alongside the Airflow webserver. For example, you can use a plugin that allows analysts to use a web UI to input SQL that runs on a scheduled interval.

### Menu items

Developers can add custom [menu items](https://github.com/mik-laj/airflow/blob/10e2a88bdc9668931cebe46deb178ab2315d6e52/airflow/plugins_manager.py#L136 ) to the Airflow navigation menu to allow users to quickly access Airflow pages that are relevant to them. See the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/plugins.html#example) for an example of how to create a custom menu item. 

The Airflow UI is customizable to meet a variety of needs. With menu items, you can provide quick access to Airflow resources for any users in your environment. For example, you can modify the Airflow UI to include a structure similar to the following:

- Developer
    - Plugins repository
    - CI/CD system
- Analyst
    - Organization-specific Domino install
    - CI/CD system
    - AI Management systems



(Intro): What is a plugin, contents of the guide
Assumed knowledge: Templating, Airflow UI, Flask if you want to build something for the UI
Types of plugins: Macros, Blueprints, Views, Menu Links - and what those are on a high level (Have a note here about hooks and operators not being plugins anymore and link to respective guides)
When to use plugins: list of general use cases, hopefully at least one for every type of plugin
How to use plugins: general process of adding a plugin (put into plugin folder, add to plugins manager, remember to restart, other steps I might not be aware of yet)
Example: How to add a macro
Example: How to add a change to the UI