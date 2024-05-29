---
title: "Integrate OpenLineage and Airflow"
sidebar_label: "OpenLineage"
description: "Learn about OpenLineage concepts and benefits of integrating with Airflow."
id: airflow-openlineage
tags: [Lineage]
---

[Data lineage](https://en.wikipedia.org/wiki/Data_lineage) is the concept of tracking and visualizing data from its origin to wherever it flows and is consumed downstream. Lineage is growing in importance as companies must rely on increasingly complex data ecosystems to make business-critical decisions. Data lineage can help with everything from understanding your data sources, to troubleshooting job failures, to managing PII, to ensuring compliance with data regulations.

It follows that data lineage has a natural integration with Apache Airflow. Airflow is often used as a one-stop-shop orchestrator for an organization’s data pipelines, which makes it an ideal platform for integrating data lineage to understand the movement of and interactions within your data.

In this guide, you’ll learn about core data lineage concepts and understand how lineage works with Airflow.

Astro offers robust support for extracting and visualizing data lineage. To learn more, see [Data lineage on Astro](https://www.astronomer.io/docs/astro/data-lineage).

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Webinar: [OpenLineage and Airflow: A Deeper Dive](https://www.astronomer.io/events/webinars/openlineage-and-airflow-deeper-dive/).

:::

## Assumed knowledge

To get the most out of this guide, make sure you have an understanding of:

- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).

## What is data lineage

Data lineage represents the complex set of relationships that exist among datasets within an ecosystem. Typically, a lineage solution has three basic elements:

- **Lineage metadata**, which describes your datasets (tables in Snowflake, for example) and jobs (tasks in your DAG, for example).
- **A lineage backend**, which stores and processes lineage metadata.
- **A lineage frontend**, which allows you to view and interact with your lineage metadata &ndash; e.g., a visual graph of jobs, datasets and columns that shows how they are connected.

If you want to read more about the concept of data lineage and why it’s important, see this [Astronomer blog post](https://www.astronomer.io/blog/what-is-data-lineage).

Visually, your data lineage graph might look like this:

![Lineage Graph](/img/guides/lineage_complex_snowflake_example.png)

If you are using data lineage, you most likely have a lineage backend that collects and stores lineage metadata and a frontend that visualizes the metadata. There are paid tools (including Astro) that provide these services, and there are open-source options that can be integrated with Airflow: namely OpenLineage, a lineage specification and collection API for getting lineage from tools in your pipelines, and [Marquez](https://marquezproject.ai), a tool for storing and visualizing lineage that includes a metadata repository, query API, and graphical UI.

### OpenLineage

[OpenLineage](https://openlineage.io/) is the open-source industry standard framework for data lineage. It standardizes the definition of data lineage, the metadata that makes up lineage metadata, and the approach to collecting lineage metadata from external systems. In other words, it defines a [formalized specification](https://github.com/OpenLineage/OpenLineage/blob/main/spec/OpenLineage.md) for all the core concepts related to data lineage.

The purpose of an open standard for lineage is to create a more cohesive governance and monitoring experience across the industry and reduce duplicated work for stakeholders. It allows for a simpler, more consistent experience when integrating lineage from many different tools, similarly to how Airflow providers reduce the work of DAG authoring by providing standardized modules for integrating Airflow with other tools.

##### Getting Started

The shortest path to reliable lineage from Airflow using OpenLineage is via the official [OpenLineage Airflow Provider](https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/index.html). Many operators are supported, and more are being added regularly. You can find a list of currently supported operators in the [Provider documentation](https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/supported_classes.html). You won't have to modify your DAGs to start emitting lineage, but some basic configuration is necessary &ndash; specifically, installing a package and setting up a transport. The latter can be done via an environment variable. For more details about configuring the Provider, see the [user guide](https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/guides/user.html).

:::note

Users on earlier versions of Airflow starting with 2.3 should build the integration using the externally maintained `openlineage-airflow` package. You can read more about setting up this plugin in the [OpenLineage documentation](https://openlineage.io/docs/integrations/airflow/).

:::

### Core concepts

The following terms are used frequently when discussing data lineage in general and OpenLineage in particular:

- **Integration**: a means of gathering lineage metadata from a source system such as a scheduler or data platform. For example, the OpenLineage Airflow Provider allows lineage metadata to be collected from Airflow DAGs. Supported operators automatically gather lineage metadata from the source system every time a job runs, preparing and transmitting OpenLineage events to a lineage backend.
- **Extractor**: an extractor is a module that gathers lineage metadata from a specific hook or operator. For example, in the OpenLineage Airflow Provider, extractors exist for the `PythonOperator` and `BashOperator`, meaning that if the provider is installed and running in your Airflow environment, lineage metadata will be generated automatically from these operators when your DAG runs. Also, the provider's `OperatorLineage` extractor class enables custom extraction in many additional operators such as the `SQLExecuteQueryOperator` and AWS `AthenaOperator`. An extractor must exist for a specific operator to get lineage metadata from it.
- **Job**: a process that consumes or produces datasets. Jobs can be viewed on your lineage graph. In the case of the provider, an OpenLineage job corresponds to a task in your DAG. Note that only tasks that come from operators with extractors will have input and output metadata; other tasks in your DAG will show up as orphans on the lineage graph. On Astro, jobs appear as nodes on your lineage graphs in the [lineage UI](https://www.astronomer.io/docs/astro/data-lineage).
- **Dataset**: a representation of a set of data in your lineage metadata and graph. For example, it might correspond to a table in your database or a set of data on which you run a Great Expectations check. Typically, a dataset is registered as part of your lineage metadata when a job writing to the dataset is completed (e.g., data is inserted into a table).
- **Run**: an instance of a job in which lineage metadata is generated. An OpenLineage run is generated with each DAG run, for example.
- **Facet**: a piece of lineage metadata about a job, dataset, or run (e.g., you might hear “job facet” in reference to a piece of metadata attached to a job).

## Why OpenLineage with Airflow?

In the previous section, you learned *what* lineage is, but a question remains: *why* would you want to have data lineage in conjunction with Airflow? Using OpenLineage with Airflow allows you to have more insight into the operation and structure of complex data ecosystems and supports better data governance. Airflow is a natural place to integrate data lineage because it is often used as a one-stop-shop orchestrator that touches data across many parts of an organization.

More specifically, OpenLineage with Airflow provides the following capabilities:

- Quickly find the **root cause** of task failures by identifying issues in upstream datasets (e.g., if an upstream job outside Airflow failed to populate a key dataset).
- Easily see the **blast radius** of any job failures or changes to data by visualizing the relationship between jobs and datasets, including column-level lineage for some operators.
- Identify where **sensitive data** is used in jobs across an organization.

These capabilities translate into real world benefits by:

- Making recovery from complex failures quicker. The faster you can identify the problem and the blast radius, the easier it is to find a solution and prevent erroneous decisions based on bad data.
- Making it easier for teams to work together across an organization. Visualizing the full scope of where a dataset or column is used reduces “sleuthing” time.
- Helping ensure compliance with data regulations by fully understanding where data is used in an organization.

## Lineage on Astro

For Astronomer customers using [Astro](https://www.astronomer.io/product/), OpenLineage is built in. The **Lineage** tab in the Astronomer UI provides multiple pages that can help you troubleshoot issues with your data pipelines and understand the movement of data across your organization. OpenLineage also powers Astro's own [alerts](https://www.astronomer.io/docs/astro/alerts), which is why you need to make sure OpenLineage is enabled to configure them. For more on lineage capabilities with Astro, see [View lineage on Astro](https://www.astronomer.io/docs/astro/data-lineage) or [contact Astronomer](https://www.astronomer.io). 

## Getting started locally

If you are interested in exploring lineage locally with open source tools, you can run OpenLineage with Airflow using [Marquez](https://marquezproject.ai) as your lineage metadata repository and query API (backend) and UI (frontend). See the [Integrate OpenLineage and Airflow locally with Marquez](marquez.md) tutorial to get started. Or, for a configuration-free option for demo purposes, you can explore [Marquez on GitPod](https://gitpod.io/#https://github.com/MarquezProject/marquez).

## Limitations

- Column-level lineage support is currently limited to the `SQLExecuteQueryOperator`-based operators listed in the [OpenLineage Provider docs](https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/supported_classes.html). The Google operators `GCSToBigQueryOperator` and `BigQueryToGCSOperator` also support column-level lineage.
- Two core operators, `PythonOperator` and `BashOperator`, support OpenLineage, but as these are "black boxes" capable of running any code, your mileage may vary.

If you are using lineage prior to Airflow 2.7, there are a few additional limitations:

:::warning

Running OpenLineage with Airflow On Astro prior to Astro Runtime 9 (Airflow 2.7) is not recommended. Prior to Airflow 2.7, OpenLineage could cause tasks to get stuck in the running status indefinitely.

:::

- The external integration (for Airflow 2.3 - 2.6) only bundles extractors for some operators. Extractors are needed in order to collect lineage metadata out of the box. To see which extractors exist, check out the [OpenLineage repo](https://github.com/OpenLineage/OpenLineage/tree/main/integration/airflow/openlineage/airflow/extractors). To get lineage metadata from other operators, you can create your own [custom extractor](https://openlineage.io/blog/extractors/) or leverage the [default extractor](https://openlineage.io/docs/integrations/airflow/default-extractors) (in Airflow 2.3+) to modify your Airflow operators to gather lineage metadata.
- For lineage metadata via the external integration from an external system connected to Airflow, such as [Apache Spark](https://openlineage.io/docs/integrations/spark/), you'll need to configure an [OpenLineage integration](https://openlineage.io/docs/integrations/about) with that system in addition to Airflow.

