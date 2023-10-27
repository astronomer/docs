---
title: "Integrate OpenLineage and Airflow"
sidebar_label: "OpenLineage"
description: "Learn about OpenLineage concepts and benefits of integrating with Airflow."
id: airflow-openlineage
tags: [Lineage]
---

[Data lineage](https://en.wikipedia.org/wiki/Data_lineage) is the concept of tracking and visualizing data from its origin to wherever it flows and is consumed downstream. Its prominence in the data space is growing rapidly as companies have increasingly complex data ecosystems alongside increasing reliance on accurate data for making business decisions. Data lineage can help with everything from understanding your data sources, to troubleshooting job failures, to managing PII, to ensuring compliance with data regulations.

It follows that data lineage has a natural integration with Apache Airflow. Airflow is often used as a one-stop-shop orchestrator for an organization’s data pipelines, which makes it an ideal platform for integrating data lineage to understand the movement and interactions of your data.

In this guide, you’ll learn about core data lineage concepts and understand how lineage works with Airflow.

Astro offers robust support for extracting and visualizing data lineage. To learn more, see [Data lineage on Astro](https://docs.astronomer.io/astro/data-lineage).

:::tip Other ways to learn:

There are multiple resources for learning about this topic. See also:

- Webinar: [OpenLineage and Airflow: A Deeper Dive](https://www.astronomer.io/events/webinars/openlineage-and-airflow-deeper-dive/).

:::

## Assumed knowledge

To get the most out of this guide, make sure you have an understanding of:

- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## What is data lineage

Data lineage is a way of tracing the complex set of relationships that exist among datasets within an ecosystem.  The concept of data lineage encompasses:

- Lineage metadata - describes your datasets (a table in Snowflake, for example) and jobs (tasks in your DAG, for example).
- A lineage backend - stores and processes lineage metadata.
- A lineage frontend - allows you to view and interact with your lineage metadata, including a graph that visualizes your jobs and datasets and shows how they are connected.

If you want to read more on the concept of data lineage and why it’s important, see this [Astronomer blog post](https://www.astronomer.io/blog/what-is-data-lineage).

Visually, your data lineage graph might look similar to this:

![Lineage Graph](/img/guides/lineage_complex_snowflake_example.png)

If you are using data lineage, you will likely have a lineage tool that collects lineage metadata, as well as a front end for visualizing the lineage graph. There are paid tools (including Astro) that provide these services, or there are open source options that can be integrated with Airflow: namely OpenLineage (the lineage tool) and [Marquez](https://marquezproject.github.io/marquez/) (the lineage front end).

### OpenLineage

[OpenLineage](https://openlineage.io/) is the open source industry standard framework for data lineage. It standardizes the definition of data lineage, the metadata that makes up lineage metadata, and the approach for collecting lineage metadata from external systems. In other words, it defines a [formalized specification](https://github.com/OpenLineage/OpenLineage/blob/main/spec/OpenLineage.md) for all of the core concepts related to data lineage.

The purpose of a standard like OpenLineage is to create a more cohesive lineage experience across the industry and reduce duplicated work for stakeholders. It allows for a simpler, more consistent experience when integrating lineage with many different tools, similar to how Airflow providers reduce the work of DAG authoring by providing standardized modules for integrating Airflow with other tools.

If you are working with lineage metadata from Airflow, the integration is built from OpenLineage using the `openlineage-airflow` package. You can read more about that integration in the [OpenLineage documentation](https://openlineage.io/docs/integrations/airflow/).

### Core concepts

The following terms are used frequently when discussing data lineage and OpenLineage in particular:

- Integration: A means of gathering lineage metadata from a source system such as a scheduler or data platform. For example, the OpenLineage Airflow integration allows lineage metadata to be collected from Airflow DAGs. Existing integrations automatically gather lineage metadata from the source system every time a job runs, preparing and transmitting OpenLineage events to a lineage backend. A full list of OpenLineage integrations can be found [here](https://openlineage.io/docs/integrations/about).
- Extractor: An extractor is a module that gathers lineage metadata from a specific hook or operator. For example, in the `openlineage-airflow` package, extractors exist for the `PostgresOperator` and `SnowflakeOperator`, meaning that if `openlineage-airflow` is installed and running in your Airflow environment, lineage metadata will be generated automatically from those operators when your DAG runs. An extractor must exist for a specific operator to get lineage metadata from it.
- Job: A process which consumes or produces datasets. Jobs can be viewed on your lineage graph. In the context of the Airflow integration, an OpenLineage job corresponds to a task in your DAG. Note that only tasks that come from operators with extractors will have input and output metadata; other tasks in your DAG will show as orphaned on the lineage graph. On Astro, jobs appear as nodes on your lineage graphs in the [lineage UI](https://docs.astronomer.io/astro/data-lineage).
- Dataset: A representation of a set of data in your lineage metadata and graph. For example, it might correspond to a table in your database or a set of data you run a Great Expectations check on. Typically a dataset is registered as part of your lineage metadata when a job writing to the dataset is completed (e.g. data is inserted into a table).
- Run: An instance of a job where lineage metadata is generated. In the context of the Airflow integration, an OpenLineage run will be generated with each DAG run.
- Facet: A piece of lineage metadata about a job, dataset, or run (e.g. you might hear “job facet”).

## Why OpenLineage with Airflow?

In the previous section, you learned *what* lineage is, but a question remains *why* you would want to have data lineage in conjunction with Airflow. Using OpenLineage with Airflow allows you to have more insight into complex data ecosystems and can lead to better data governance. Airflow is a natural place to integrate data lineage, because it is often used as a one-stop-shop orchestrator that touches data across many parts of an organization.

More specifically, OpenLineage with Airflow provides the following capabilities:

- Quickly find the root cause of task failures by identifying issues in upstream datasets (e.g. if an upstream job outside of Airflow failed to populate a key dataset).
- Easily see the blast radius of any job failures or changes to data by visualizing the relationship between jobs and datasets.
- Identify where key data is used in jobs across an organization.

These capabilities translate into real world benefits by:

- Making recovery from complex failures quicker. The faster you can identify the problem and the blast radius, the easier it is to solve and prevent any erroneous decisions being made from bad data.
- Making it easier for teams to work together across an organization. Visualizing the full scope of where a dataset is used reduces “sleuthing” time.
- Helping ensure compliance with data regulations by fully understanding where data is used.

## Lineage on Astro

For Astronomer customers using [Astro](https://www.astronomer.io/product/), OpenLineage integration is built in. The **Lineage** tab in the Astronomer UI provides multiple pages that can help you troubleshoot issues with your data pipelines and understand the movement of data across your organization. For more on lineage capabilities with Astro, see [View lineage on Astro](https://docs.astronomer.io/astro/data-lineage) or [contact Astronomer](https://www.astronomer.io). 

## Getting started

If you are working with open source tools, you can run OpenLineage with Airflow locally using Marquez as the lineage front end. See [Integrate OpenLineage and Airflow locally with Marquez](marquez.md) tutorial to get started.

## Limitations

OpenLineage is rapidly evolving, and new functionality and integrations are being added all the time. At the time of writing, the following are limitations when using OpenLineage with Airflow:

- You must be running Airflow 2.3.0+ with OpenLineage 0.8.1+ to get lineage metadata for *failed* task runs.
- Only some operators have bundled extractors (needed to collect lineage metadata out of the box). To see which extractors currently exist, check out the [OpenLineage repo](https://github.com/OpenLineage/OpenLineage/tree/main/integration/airflow/openlineage/airflow/extractors). To get lineage metadata from other operators, you can create your own [custom extractor](https://openlineage.io/blog/extractors/) or leverage the [default extractor](https://openlineage.io/docs/integrations/airflow/default-extractors) (in Airflow 2.3+) to modify your Airflow operators to gather lineage metadata.
- To get lineage metadata from an external system connected to Airflow, such as [Apache Spark](https://openlineage.io/docs/integrations/spark/), you'll need to configure an [OpenLineage integration](https://openlineage.io/docs/integrations/about) with that system in addition to Airflow.
