---
sidebar_label: 'Data lineage support and compatibility'
title: "Data lineage support and compatibility reference"
id: data-lineage-support-and-compatibility
description: A compatibility reference guide for Astro lineage's Airflow support.
---

## Overview

All Astro Deployments use the [OpenLineage Airflow library](https://openlineage.io/integration/apache-airflow/) (`openlineage-airflow`) to gather lineage data. The OpenLineage Airflow library is installed on Astro Runtime by default. This integration includes built-in support for several Apache Airflow operators. These operators use tools called extractors to emit lineage data and they don't require additional configuration. Tasks that run with supported operators appear as nodes in your data lineage graphs and show connections to any input and output datasets.

If you’re using an unsupported operator, create an issue in the [OpenLineage GitHub repository](https://github.com/OpenLineage/OpenLineage) or write your own custom extractor.

:::info

This functionality is early access. If you have questions or feedback, contact [Astronomer support](https://support.astronomer.io/).

:::

## Supported Airflow operators

The following operators are supported in Astro lineage:

- `PostgresOperator`
- `BigQueryOperator`
- `SnowflakeOperator`
- `GreatExpectationsOperator`

:::tip

The `GreatExpectationsOperator` additionally emits data quality information to the **Quality** tab in the **Lineage** view of the Cloud UI. For more information, see [Data lineage on Astro](data-lineage.md).

:::

## Partially supported Airflow operators

The following operators are partially supported by the Airflow integration with OpenLineage:

- `PythonOperator`
- `BashOperator`

Airflow tasks that are run with partially supported operators:

- Emit source code to the lineage backend.
- Emit task run data to the lineage backend.
- Appear in the graph view of the **Lineage** tab in the Cloud UI as nodes.
- Do not emit lineage data about input or output datasets.

## Unsupported operators

Airflow tasks that run with unsupported operators send information about the task duration, status, and parent DAG to the lineage backend. However, information about the task's input or output datasets isn't sent to the backend. A task running with an unsupported operator appears as a single node in the lineage graph.

## Other known limitations

Lineage on Astro is in active development. Keep in mind the following limitations when using lineage functionality:

- Source code emitted by partially supported operators doesn't appear in the lineage UI.
- Airflow operators emit lineage data about failed task runs only for Deployments on Astro Runtime v5.0+.
- Data lineage cannot be extracted from datasets whose Airflow connections are stored in a [secrets backend](secrets-backend.md).
