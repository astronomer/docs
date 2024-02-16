---
title: 'How to write best practice Airflow DAGs for Astro'
sidebar_label: 'DAG writing on Astro'
id: dag-writing-on-astro
---

You can run any valid Airflow DAG on Astro. 

However, there are a couple of best practices surrounding Astronomer tools and features that help you to:

- Improve your development workflow.
- Organize your deployment and DAGs. 
- Optimize task execution efficiency.

This best practice doc provides additional guidance on how to write Airflow DAGs for Astro, all [general Airflow best practices](https://docs.astronomer.io/learn/dag-best-practices) apply.

:::info New to Airflow?

If you are new to Airflow in general, we recommend starting with the following resources:

- Hands-on tutorial: [Get started with Apache Airflow](https://docs.astronomer.io/learn/get-started-with-airflow).
- Astronomer Academy: [Airflow 101 Learning Path](https://academy.astronomer.io/path/airflow-101).
- Webinar: Airflow 101: How to get started writing data pipelines with Apache Airflow.

:::

## Feature overview

- [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- [Worker queues](https://docs.astronomer.io/astro/configure-worker-queues).
- [Astro Cloud UI Environment Manager](https://docs.astronomer.io/astro/manage-connections-variables)
- [Astro alerts](https://docs.astronomer.io/astro/alerts)

## Best practice guidance 





Use the Astro CLI for local development 
keep Astro project organized
Unit tests for custom code and astro dev pytest 
integrate these tests into CI/CD
DAG validation and best practice recommendations (owner link?, DAG docs, docstring up front for DAGs view, tag owner retry). for guidance on alerts see X
Use worker queues (combination with pools?) 

DAG notes when rerunning 
Use the CLoud IDE 
Use the Astro environment manager for connections. Use deployment variables for Env vars and Airflow variables -> because easy to mark as secret, because can be pulled by the CLI programmatic import/export.

leverage in cluster for KPO


## Example 


### Prerequisites

### Implementation


## See also 

- Webinar: [Best practices for managing Airflow across teams](https://www.astronomer.io/events/webinars/best-practices-for-managing-airflow-across-teams-video/).
- Webinar: [DAG writing for data engineers and data scientists](https://www.astronomer.io/events/webinars/dag-writing-for-data-engineers-and-data-scientists-video/).
- OSS Learn guide: [DAG writing best practices in Apache Airflow](https://docs.astronomer.io/learn/dag-best-practices).