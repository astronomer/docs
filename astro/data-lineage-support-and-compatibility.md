---
sidebar_label: 'Data Lineage Support and Compatibility'
title: "Data Lineage Support and Compatibility Reference"
id: data-lineage-support-and-compatibility
description: A compatibility reference guide for Astro lineage's Airflow support.
---

## Overview

This document contains a list of Airflow operators which are supported with Astro lineage by default.

All Astro Deployments gather lineage data via the [OpenLineage Airflow library](https://openlineage.io/integration/apache-airflow/) (`openlineage-airflow`) that is installed on Astro Runtime by default. This integration includes built-in support for several Apache Airflow operators. These operators emit lineage via tools called extractors without requiring additional configuration. Tasks that run with supported operators will appear as nodes in your data lineage graphs and show connections to any input and output datasets.

If you’re using an operator that isn't currently supported for lineage, we recommend either creating an issue in the [OpenLineage GitHub repository](https://github.com/OpenLineage/OpenLineage) or writing your own custom extractor.

:::info 

This functionality is early access and under active development. If you have any questions or feedback about this feature, reach out to [Astronomer Support](https://support.astronomer.io/).

:::

## Supported Airflow Operators

The following operators are supported in Astro lineage:

- `PostgresOperator`
- `BigQueryOperator`
- `SnowflakeOperator`
- `GreatExpectationsOperator`

:::tip

The `GreatExpectationsOperator` additionally emits data quality information to **Quality** tab in the **Lineage** view of the Cloud UI. For more information, see [Data Lineage on Astro](data-lineage.md).

:::

## Partially Supported Airflow Operators

The following operators are partially supported by the Airflow integration with OpenLineage:

- `PythonOperator`
- `BashOperator`

Airflow tasks that are run with partially supported operators:

- Emit source code to the lineage backend.
- Emit task run data to the lineage backend.
- Appear in the graph view of the **Lineage** tab in the Cloud UI as nodes.
- Do not emit lineage data about input or output datasets.

## Unsupported Operators

If an Airflow task runs with an operator that is not supported, the lineage backend will still receive information about the task duration, status, and parent DAG. However, the backend will not receive any information about the task's input or output datasets. A task running with an unsupported operator will appear as a single node in the lineage graph.

## Other Known Limitations

Lineage on Astro is still in active development. Keep in mind the following limitations when using lineage functionality:

- Source code emitted by partially supported operators does not appear in the lineage UI.
- Airflow operators will emit lineage data about failed task runs only for Deployments on Astro Runtime v5.0+.
- Data Lineage cannot currently be extracted from datasets whose Airflow connections are stored in a [secrets backend](secrets-backend.md).
