---
title: "Airflow plugins"
sidebar_label: "Plugins"
description: "How to use Airflow plugins."
id: using-airflow-plugins
---

Plugins are external features that can be added to customize your Airflow installation. They are automatically imported upon starting your Airflow instance if they have been added to `plugins` folder of an Airflow project. 

In this guide, you'll learn how to add a plugin to your Airflow instance and what Airflow components can be part of a plugin.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow core components. See [Airflow's components](airflow-components.md).
- The basics of Flask. See the [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/).

## When to use plugins

Plugins offer a flexible way to customize your Airflow experience by building on top of existing Airflow components. For example, you can:

- Add views to your Airflow UI that display contents of the Airflow metadata database in a custom way.
- Build an application that monitors Airflow's functioning and sends out custom alerts, for example in case of a certain number of DAGs failing in a specified time frame.
- Add a button to the task instance **Details** view that dynamically links to files or logs in external data tools relevant to the task.

## How to create a plugin

To add a new plugin to your Airflow instance, you need to create a Python file in the `plugins` folder of your Airflow project. Within that file, create a class which inherits from the `AirflowPlugin` to define the plugin. The code snippet below defines a plugin with the name `empty` without any components. 

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

In order for changes to your plugin to be registered, you will need to restart any Airflow components (e.g. the webserver or scheduler) that use the plugin. Learn more in the [official Airflow documentation on plugins](https://airflow.apache.org/docs/apache-airflow/stable/plugins.html#when-are-plugins-re-loaded).

:::

## Plugin components

Functionality is added to a plugin by adding components to the class which defines the plugin. There are 10 types of plugin components that can be added to Airflow. In this guide we will show the more commonly used components, including:

- `appbuilder_menu_items` allow you to add additional sections and links to the Airflow menu.
- `flask_blueprints` and `appbuilder_views` offer the possibility to build a Flask project on top of Airflow.
- `operator_extra_links` and `global_operator_extra_links` are ways to add links to Airflow task instances.
- `macros` expand upon existing Jinja templates using custom functions.

Other types of plugin components not covered in this guide include:

- `timetables` offer the option to register custom timetables that define schedules which cannot be expressed in CRON. See the [DAG scheduling and timetables in Airflow guide](https://docs.astronomer.io/learn/scheduling-in-airflow#timetables) for more information and a code example.
- `executors` add the possibility to use a custom [executor](https://docs.astronomer.io/learn/airflow-executors-explained) in your Airflow instance.
- `listeners` are an experimental feature to add notifications for events happening in Airflow. Learn more in the [official Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/listeners.html).

:::info

Before Airflow 2.0 custom operators and hooks were added as plugins. This pattern has been deprecated and [custom operators and hooks](https://docs.astronomer.io/learn/airflow-importing-custom-hooks-operators) can now be used simply by importing a script located in `include`.

:::

### Appbuilder menu items

You can update the menu at the top of the Airflow UI to contain custom tabs with links to external websites. Adding top-level menu items and adding sub-items are both supported. 

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
    appbuilder_menu_items = [appbuilder_mitem_toplevel, appbuilder_mitem_subitem]
```

The code above creates a plugin that adds two menu items.

- `appbuilder_mitem_toplevel` is a top-level menu button named **Apache** that links to the [Apache homepage](https://www.apache.org/).
- `appbuilder_mitem_subitem` is a sub-item which is added to the **Docs** menu. It has the name `Astro SDK Docs` and links out to [the documentation for the Astro SDK](https://astro-sdk-python.readthedocs.io/en/stable/index.html).

Both additional menu items are added to the `app_builder_menu_items` component of a plugin called `Menu items plugin` which is defined in the `MyMenuItemsPlugin` class. The screenshot below shows the additional menu items in the Airflow UI.

![Plugins Menu items](/img/guides/plugins_menu_items.png)

### Flask Blueprints and Appbuilder views

Flask blueprints and views are plugin components that allow you to add more elaborate customization to the Airflow UI. A Flask blueprint functions as an organizational tool to group related views and supporting code while Flask views render webpages from html templates. 

:::info

To learn more check out the [Blueprints and Views tutorial](https://flask.palletsprojects.com/en/2.2.x/tutorial/views/) in the official Flask documentation.

:::

You can add a view to render a simple templated HTML file on top of the Airflow UI by following these steps:

1. Create a folder within the `plugins` directory called `templates`.
2. Within that folder create a HTML file called `test.html` and copy the collowing code into it:

    ```html
    <!DOCTYPE html>
    <p>Airflow is {{ content }}!</p>
    ```

3. In the `plugins` directory, add a Python file called `my_first_view_plugin.py`. Copy the code below.

    ```python
    from airflow.plugins_manager import AirflowPlugin
    from flask import Blueprint
    from flask_appbuilder import expose, BaseView as AppBuilderBaseView

    # define a Flask blueprint
    my_blueprint = Blueprint(
        "test_plugin",
        __name__,
        # register airflow/plugins/templates as a Jinja template folder
        template_folder="templates",
    )

    # create a flask appbuilder BaseView
    class MyBaseView(AppBuilderBaseView):
        default_view = "test"

        @expose("/")
        def test(self):
            # render the HTML file from the templates directory with content
            return self.render_template("test.html", content="awesome")

    # instantiate MyBaseView
    my_view = MyBaseView()

    # define the path to my_view in the Airflow UI
    my_view_package = {
        # define the menu sub-item name
        "name": "Test View",
        # define the top-level menu item
        "category": "My Extra View",
        "view": my_view,
    }

    # define the plugin class
    class MyViewPlugin(AirflowPlugin):
        # name the plugin
        name = "My appbuilder view"
        # add the blueprint and appbuilder_views components
        flask_blueprints = [my_blueprint]
        appbuilder_views = [my_view_package]
    ```

4. Start your Airflow instance using `astro dev start` or `astro dev restart` if you were already running Airflow.

This plugin will add a top-level menu item called **My Extra View** which contains the sub-item **Test View**.

![Test View Menu](/img/guides/plugins_test_view_menu.png)

By clicking on **Test View** you can access the Flask View that was defined as `my_view`. It shows the HTML template (`test.html`) rendered with the provided content.

![Test View](/img/guides/plugins_test_view.png)

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
class MyOperatorExtraLink(AirflowPlugin):
    name = "my_plugin_name"
    operator_extra_links = [
        MyLink(),
    ]
```
The screenshot below shows an operator extra link called "HTTP cat" that was added to the custom CatHttpOperator. For more instructions, see this [step-by-step tutorial](operator-extra-link-tutorial.md) on how to add operator extra links.

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
class MyGlobalLink(AirflowPlugin):
    name = "my_plugin_name"
    global_operator_extra_links = [
        GlobalLink(),
    ]
```

You can access the button on task instances in both the **Graph** and **Grid** views.

![Airflow Docs Button](/img/guides/global_operator_extra_link.png)

### Macros

In Airflow you can define custom macros which can be accessed using Jinja templating. Macros can be added at the DAG level by defining them in the DAG parameter `user_defined_macros` as shown in [Using Airflow templates](templating.md). If you want to make macros available to your whole Airflow instance you can register them as a plugin. 

Common use cases for custom macros include:

- Injecting dynamic datetime objects into DAG code in formats not available in pre-defined macros. For example, converting the `{{ ts }}` predefined macro, which provides the logical date of the DAG as a timestamp from `YYYY-MM-DDThh:mm:ss+00:00` to `hh:mm`. 
- Injecting dynamic arguments into DAG code based on Python logic. For example, passing a different argument to a function on weekdays versus the weekend.
- Injecting dynamic arguments into DAG code based on XCom values. For example, using a different target blob storage depending on how many files will be ingested, a count determined and pushed to XCom by an upstream task.

```python
from airflow.plugins_manager import AirflowPlugin
from random import randint


def random_number_macro():
    return randint(0, 1000)


class MyAirflowMacro(AirflowPlugin):
    name = "my_macro_plugin"
    macros = [
        random_number_macro,
    ]
```

The code above creates a macro that returns a random number between 0 and 1000. It can be referenced using Jinja templating in any templateable parameter of any operator. The code snippet below shows how the macro can be used within the `bash_command` parameter of the BashOperator to print out a random number.

```python
use_plugin_macro = BashOperator(
    task_id="use_plugin_macro",
    bash_command="echo {{ macros.my_macro_plugin.random_number_macro() }}",
)
```

### Airflow listeners

[Airflow listeners](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/listeners.html#listeners) allow you to execute custom code when certain events occur anywhere in your Airflow instance, for example whenever any DAG run fails or an update to a Dataset is detected. 

You can create a listener using the `@hookimpl` decorator on functions defined with the same name and parameters as listed in the [listeners spec](https://github.com/apache/airflow/tree/main/airflow/listeners/spec) source code. 

For example, the [@hookspec of the `on_task_instance_failed` function](https://github.com/apache/airflow/blob/main/airflow/listeners/spec/taskinstance.py) is:

```python
@hookspec
def on_task_instance_failed(
    previous_state: TaskInstanceState | None, task_instance: TaskInstance, session: Session | None
):
    """Execute when task state changes to FAIL. previous_state can be None."""
```

In order to create a listener that executes whenever any task instance fails in your whole Airflow environment, you need to define a function called `on_task_instance_failed` that takes three parameters: `previous_state`, `task_instance` and `session`. Then, you decorate it with `@hookimpl`.

```python
from airflow.listeners import hookimpl

@hookimpl
def on_task_instance_failed(
    previous_state: TaskInstanceState | None, task_instance: TaskInstance, session: Session | None
):
    # Your code here
```

The listener file can then be registered as a plugin by adding it to the `listeners` component of the plugin class. 

```python
from airflow.plugins_manager import AirflowPlugin
from plugins import listener_code


class MyListenerPlugin(AirflowPlugin):
    name = "my_listener_plugin"
    listeners = [listener_code]
```

To see a full example of how to create and register a listener, check out the [Use a listener to send a Slack notification when a Dataset is updated](airflow-listeners.md) tutorial.