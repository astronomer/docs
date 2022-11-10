---
title: "Airflow plugins"
sidebar_label: "Plugins"
description: "How to use Airflow plugins."
id: using-airflow-plugins
---

Plugins are external features that can be added to customize your Airflow installation. They are automatically imported upon starting your Airflow instance if they have been added to `plugins` folder of an Airflow project. 

In this guide you'll learn how to add a plugin to your Airflow instance as well as what components can be part of a plugin.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow core components. See [Airflow's components](airflow-components.md).
- The basics of Flask. See the [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/).

## When to use plugins

Plugins offer a flexible way to customize your Airflow experience by building on top of existing Airflow components. For example you can:

- Add views to your Airflow UI that display contents of the Airflow metadata database in a custom way.
- Build an application that monitors Airflow's functioning itself and sends out custom alerts, for example in case of a certain number of DAGs failing in a specified time frame.
- Add dynamic links to task instances to files and logs in external data tools the task has been performed on.

## How to create a plugin

To add a new plugin to your Airflow instance you need to create a Python file in the `plugins` folder of your Airflow project. Within that file a class which inherits from the `AirflowPlugin` class has to be created to define the plugin. The code snippet below defines a plugin with the name `empty` without any components. 

```python
from airflow.plugins_manager import AirflowPlugin

class MyAirflowPlugin(AirflowPlugin):
    # name your plugin, this is mandatory
    name = "empty"

    ## Add plugin components
    # ...
    # ...
    # ...

    # Add an optional callback to perform actions when airflow starts and
    # the plugin is loaded.
    # NOTE: Ensure your plugin has *args, and **kwargs in the method definition
    #   to protect against extra parameters injected into the on_load()
    #   function in future changes
    def on_load(*args, **kwargs):
        # perform Plugin boot actions
        pass
```

The list of currently active plugins can be viewed in the Airflow UI under **Admin** -> **Plugins**. The code above creates the following entry:

![Empty plugin](/img/guides/empty_plugin.png)

:::info

Airflow needs to be restarted for changes in plugins to be registered. Learn more in the [official Airflow documentation on plugins](https://airflow.apache.org/docs/apache-airflow/stable/plugins.html#when-are-plugins-re-loaded).

:::

## Plugin components

Functionality is added to a plugin by adding components to the class which defines the plugin. There are 10 types of plugin components, in this guide we want to highlight the following:

- appbuilder_menu_items
- flask_blueprints
- appbuilder_views
- operator_extra_links
- global_operator_extra_links
- macros

Other types of plugin components include:

- `timetables`, which offer the option to register custom timetables that define schedules which cannot be expressed in CRON. See the [DAG scheduling and timetables in Airflow guide](https://docs.astronomer.io/learn/scheduling-in-airflow#timetables) for more information and a code example.
- `executors`, which offers the possibility to add a custom [executor](https://docs.astronomer.io/learn/airflow-executors-explained) to your Airflow instance.
- `listeners`, which are an experimental feature to add notifications for events happening in Airflow. Learn more in the [official Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/listeners.html).

:::info

Before Airflow 2.0 custom operators and hooks were added as plugins. This pattern has been deprecated and [custom operators and hooks](https://docs.astronomer.io/learn/airflow-importing-custom-hooks-operators) can now be simply by importing a script located in `include`.

:::

### Appbuilder menu items

You can customize the Airflow menu at the top of the screen to contain custom tabs with links to external websites. Both adding top-level menu items as well as sub-items are supported. 

```python
from airflow.plugins_manager import AirflowPlugin

# creating a new top-level menu item
appbuilder_mitem_toplevel = {
    "name": "Apache",
    "href": "https://www.apache.org/",
}

# creating a new sub-item in the Docs menu item 
appbuilder_mitem_subitem = {
    "name": "Astro SDK Docs",
    "href": "https://astro-sdk-python.readthedocs.io/en/stable/index.html",
    "category": "Docs",
}

# defining the plugin class
class MyMenuItemsPlugin(AirflowPlugin):
    name = "Menu items plugin"

    # adding the menu items to the plugin
    appbuilder_menu_items = [
        appbuilder_mitem_toplevel,
        appbuilder_mitem_subitem
    ]
```

The code above creates a plugin that adds two menu items.

- `appbuilder_mitem_toplevel` is a top-level menu button named **Apache** that links to the [Apache homepage](https://www.apache.org/).
- `appbuilder_mitem_subitem` is a sub-item which is added to the **Docs** menu. It has the name `Astro SDK Docs` and links out to [the documentation for the Astro SDK](https://astro-sdk-python.readthedocs.io/en/stable/index.html).

Both additional menu items are added to the `app_builder_menu_items` component of a plugin called `Menu items plugin` which is defined in the `MyMenuItemsPlugin` class. The screenshot below shows the additional menu items in the Airflow UI.

![Plugins Menu items](/img/guides/plugins_menu_items.png)

### Flask Blueprints

WIP

### Appbuilder views

WIP

### Operator extra links

Operator extra links are additional buttons with links that can be added to specific operators. They can be defined as Python classes derived from the `BaseOperatorLink` class. The example below shows how to create a new operator extra link `MyLink` that is applied to `MyOperator1` and `MyOperator2`. The operator extra link is registered with the `MyAirflowPlugin` by adding it its `operator_extra_links` list. 

```python
from airflow.models.baseoperator import BaseOperatorLink
from include.custom_operators import MyOperator1, MyOperator2
from airflow.plugins_manager import AirflowPlugin

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
The screenshot below shows an operator extra link called "HTTP cat" having been added to the custom CatHttpOperator in this [step-by-step tutorial](operator-extra-link-tutorial.md) on how to add operator extra links.

![Cat Button](/img/guides/extra_links_tutorial_cat_button.png)

### Global operator extra links

Global operator extra links are additional buttons with links that will be added to every operator. This example adds a button named **Airflow docs** to all operators that links out to the Airflow documentation.

```python
class GlobalLink(BaseOperatorLink):
    # name the link button
    name = "Airflow docs"

    # function determining the link
    def get_link(self, operator, *, ti_key=None):
        return "https://airflow.apache.org/"

# add the operator extra link to a plugin
class MyAirflowPlugin(AirflowPlugin):
    name = "my_plugin_name"
    global_operator_extra_links = [
        GlobalLink(),
    ]
```

You can access the button on task instences in both the Graph and Grid view.

![Airflow Docs Button](/img/guides/global_operator_extra_link.png)

### Macros

In Airflow you can define custom macros which can be accessed using Jinja templating. Macros can be added at the dag level by defining them in the DAG parameter `user_defined_macros` as shown in [Using Airflow templates](templating.md)). If you want to make macros available to your whole Airflow instance you can register them as a plugin. 

```python
from airflow.plugins_manager import AirflowPlugin
from random import randint

def random_number_macro():
    return randint(0,1000)

class MyAirflowPlugin(AirflowPlugin):
    name = "my_macro_plugin"
    macros = [
        random_number_macro,
    ]
```

The code above creates a macro that returns a random number between 0 and 1000. It can be referenced using Jinja templating in any templateable parameter of any operator. The code snippet below shows how the macro can be used within the `bash_command` parameter of the BashOperator to print out a random number.

```python
use_plugin_macro = BashOperator(
        task_id="use_plugin_macro",
        bash_command="echo {{ macros.my_macro_plugin.random_number_macro() }}"
    )
```


