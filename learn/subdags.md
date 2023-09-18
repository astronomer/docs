---
title: "Airflow SubDAGs"
sidebar_label: "SubDAGs"
description: "Use SubDAGs to create Airflow modular workflows."
id: subdags
---

SubDAGs are a legacy Airflow feature that allowed the creation of reusable task patterns in DAGs. SubDAGs caused performance and functional issues, and they were [deprecated](https://github.com/apache/airflow/issues/12292) Airflow 2.0. Astronomer recommends that you don't use SubDAGs and instead use an alternative supported Airflow feature.

In this guide, you'll learn about SubDAG alternatives and SubDAG issues.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow task groups. See [Task Groups](task-groups.md).
- Implementing dependencies between DAGs. See [Cross-DAG dependencies](cross-dag-dependencies.md).

## SubDAG alternatives

Don't use SubDAGs. Use one of the following alternatives instead:

- [Task Groups](task-groups.md): Task Groups can be used to organize tasks in the DAG's Graph View. Task Groups simplify the organization, viewing, and monitoring of complex DAGs. To view a video overview of Task Groups, see [Grouping](https://academy.astronomer.io/astro-runtime-task-groups).
- [Cross-DAG dependencies](cross-dag-dependencies.md): Cross-DAG dependencies can be implemented between different DAGs in the same Airflow environment or across separate environments. Cross-DAG dependencies are ideal if you have task dependencies that cannot be implemented within a single DAG. There are multiple methods available to implement cross-DAG dependencies.

## SubDAG issues

SubDAGs DAGs are embedded within other DAGs and this can cause the following issues:

- When a SubDAG is triggered, the SubDAG and child tasks occupy worker slots until the entire SubDAG is complete. This can delay other task processing and, depending on your number of worker slots, can lead to deadlocking.
- SubDAGs have their own parameters, schedule, and enabled settings. When these are not consistent with their parent DAG, unexpected behavior can occur.
