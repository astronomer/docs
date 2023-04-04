---
title: "Airflow Quickstart"
sidebar_label: "Quickstart"
id: airflow-quickstart
---

A great way to explore Airflow features and use cases is using Astronomer's [Airflow Quickstart](https://github.com/astronomer/airflow-quickstart).

This quickstart uses open source tools Airflow, [DuckDB](https://duckdb.org/), [Streamlit](https://streamlit.io/), and the [Astro Python SDK](https://astro-sdk-python.readthedocs.io/en/stable/index.html) to implement an ELT pipeline that creates an interactive dashboard showing global and local temperature changes over time.

![Interactive dashboard](/img/guides/quickstart_streamlit_result_1.png)

You can run the quickstart without installing anything locally by using [GitHub Codespaces](https://github.com/features/codespaces), or you can run locally using the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli).

This project is designed to show what Airflow can do and provide a sandbox for you to explore important Airflow concepts. The repository contains one pre-built pipeline that will create and populate the interactive dashboard with no user code changes, as well as several exercises that will enhance the dashboard when completed. For more instructions on using the quickstart, see the [project Readme](https://github.com/astronomer/airflow-quickstart/blob/main/README.md).

:::tip

If you are new to Airflow and want more instructions for getting started, check out our step-by-step [Get Started with Airflow](get-started-with-airflow.md) tutorial.

:::

## Concepts covered

The pre-built pipeline and exercises in this quickstart show the implementation of several key Airflow features, which you can learn more about in our Learn resources:

- [Datasets](https://docs.astronomer.io/learn/airflow-datasets): This feature helps make Airflow data-aware and expands Airflow scheduling capabilities. Using datasets, you can schedule DAGs to run only when other tasks that update shared data have completed.
- [Dynamic task mapping](https://docs.astronomer.io/learn/dynamic-tasks): This feature allows you to write DAGs that dynamically generate parallel tasks at runtime based on the results of previous tasks or external criteria. 
- The [Astro Python SDK](https://docs.astronomer.io/learn/astro-python-sdk): This open source package built on top of Airflow provides functions and classes that simplify common ELT operations such as loading files or using SQL or Pandas to transform data.
