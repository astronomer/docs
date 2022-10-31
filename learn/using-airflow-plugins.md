---
title: "Import plugins to Airflow"
sidebar_label: "Plugins"
description: "How to use Airflow plugins."
id: using-airflow-plugins
---

Plugins are Airflow components that you can add to your project to customize your Airflow installation. You can import custom plugins to Airflow by adding them to the `plugins` directory of your project. 

In this guide you'll learn about plugin capabilities and review some examples that show how they are used and the benefits they provide.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Airflow core components. See [Airflow's components](airflow-components.md).

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
