---
title: "How to share code between multiple Airflow projects"
description: "A description of the various ways to reuse and share code between multiple projects, with pros and cons of each solution."
id: sharing-code-multiple-projects
sidebar_label: "Sharing code between multiple projects"
---

After you [set up an Astro project](https://docs.astronomer.io/astro/cli/develop-project), and you start implementing some pipelines, extracting several Python functions for reusability, and scaling other operations, you've now got multiple Airflow deployments. How do you reuse code between your projects? In this guide, you'll learn about various options for reusing code and their pros and cons.

Specifically, this guide demonstrates three options, ordered from simple implementation, but poor reusability, to comprehensive implementation, but excellent reusability:

| Solution                                                 | When to use                                                               |
|----------------------------------------------------------|---------------------------------------------------------------------------|
| Shared Python code in same file                          | When reusing code only within a single script                             |
| Shared Python code in `/include` folder                  | When reusing code in multiple scripts, but within the same Git repository |
| Shared Python code in Python package in separate project | When reusing code in multiple Git projects                                |

The following DAG, which queries a database and returns results, is used in each section below to highlight the different solutions. The tasks in this DAG perform the same business logic twice. Both functions (`_get_locations()` and `_get_purchases()`) instantiate a database client, execute a query, and return the result. The only difference is the query being executed. Any change to the database connection logic now requires two changes. If you continue copy-pasting these functions for running more queries, you have multiple copies of the same business logic, which also requires multiple code changes when you want to modify the database connection logic.

```python {7-9,11-12,14-16,18-19}
import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(dag_id="example", schedule=None, start_date=datetime.datetime(2023, 1, 1)):
    def _get_locations():
        # Pseudocode:
        client = db.client()
        query = "SELECT store_id, city FROM stores"
        result = client.execute(query)
        return result
        
    def _get_purchases():
        # Pseudocode:
        client = db.client()
        query = "SELECT customer_id, string_agg(store_id, ',') FROM customers GROUP BY customer_id"
        result = client.execute(query)
        return result
        
    PythonOperator(task_id="get_locations", python_callable=_get_locations)
    PythonOperator(task_id="get_purchases", python_callable=_get_purchases)
```

## Shared Python code in same file

To reduce the burden of maintaining the same business logic multiple times, and have only one way of querying the database, you can extract the code into a single function within the same DAG file:

```python
def query_db(query):
    # Pseudocode:
    client = db.client()
    result = client.execute(query)
    return result
```

This function takes an argument `query`, and the database connection logic is only defined once, regardless what query is given. This way you don't have to maintain the same business logic in multiple places anymore. To use this function, reference it in your DAG script:

```python {6-10}
import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

def query_db(query):
    # Pseudocode:
    client = db.client()
    result = client.execute(query)
    return result

with DAG(dag_id="example", schedule=None, start_date=datetime.datetime(2023, 1, 1)):
    PythonOperator(task_id="get_locations", python_callable=query_db, op_kwargs={"query": "SELECT store_id, city FROM stores"})
    PythonOperator(task_id="get_purchases", python_callable=query_db, op_kwargs={"query": "SELECT customer_id, string_agg(store_id, ',') FROM customers GROUP BY customer_id"})
```

This solution is technically simple; you define one single function and reference that function in multiple Airflow tasks, in the same script. This improves the code because a change to the database connection logic requires only a single change instead of two. However, this solution is limited to a single script. You cannot reuse the function in another script (without importing). Let's look at a solution in the next section.

## Shared Python code in `/include` folder
To reuse a piece of code across multiple scripts it needs to be accessible in a shared location. The Astro Runtime Docker image provides a convenient mechanism for that, the `/include` folder:

You can store the function in a separate file, for example `/include/db.py`:
```python
def query_db(query):
    # Pseudocode:
    client = db.client()
    result = client.execute(query)
    return result
```

And then import the function from your DAG:

```python {6}
import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from include.db import query_db

with DAG(dag_id="example", schedule=None, start_date=datetime.datetime(2023, 1, 1)):
    PythonOperator(task_id="get_locations", python_callable=query_db, op_kwargs={"query": "SELECT store_id, city FROM stores"})
    PythonOperator(task_id="get_purchases", python_callable=query_db, op_kwargs={"query": "SELECT customer_id, string_agg(store_id, ',') FROM customers GROUP BY customer_id"})
```

The benefit of this solution is that the `query_db` function can be imported from multiple scripts (within the same Git repository).

## Shared Python code in Python package in separate project

In some cases, you might have code that needs to be shared across different Airflow deployments. For example, if you're onboarding multiple teams to the Astronomer platform and each team has their own code repository. This means you can't reuse the code in the `/include` folder, because it resides in a different Git repository.

To reuse code over multiple projects, you need to store it in a separate Git repository which can be reused by multiple projects. The best way to do this is to create your own Python package from the repository you want to be available to multiple projects. This takes a bit more work to set up, but enables multiple teams using multiple Git repositories to maintain a single source of code. You can see an example Python package in [this repo](https://github.com/astronomer/custom-package-demo). 

The number of options for developing, building, and releasing a Python package are limitless and this guide only provides general guidance. See [**Structuring your project**](https://docs.python-guide.org/writing/structure) and [**Packaging Python projects**](https://packaging.python.org/en/latest/tutorials/packaging-projects) for more information on Python packaging. 

Setting up a custom Python package requires roughly the following steps:

1. Create a separate Git repository for your shared code.
2. Write a `pyproject.toml` file. This is a configuration file which contains the build requirements of your Python project. You can find an example [here](https://github.com/astronomer/custom-package-demo/blob/main/pyproject.toml).
3. Create a folder for your code, e.g. `my_company_airflow`.
4. Create a folder for tests, e.g. `tests`.
5. Create a CI/CD pipeline to test, build, and release your package. You can see an example GitHub Actions workflow in the [custom package demo](https://github.com/astronomer/custom-package-demo/tree/main/.github/workflows).
6. Ensure your setup works correctly by building and releasing a first version of the package.
7. Validate the package by installing it in a project via the `requirements.txt` file.

After completing the preceding steps, you can now add shared code to the Python package so that other projects can use it. The code example must be added in a module in your Python package, for example `my_company_airflow/db.py`:

```python
def query_db(query):
    # Pseudocode:
    client = db.client()
    result = client.execute(query)
    return result
```

After installing the package, you can then import the function in your DAGs as:

```python {6}
import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from my_company_airflow.db import query_db

with DAG(dag_id="example", schedule=None, start_date=datetime.datetime(2023, 1, 1)):
    PythonOperator(task_id="get_locations", python_callable=query_db, op_kwargs={"query": "SELECT store_id, city FROM stores"})
    PythonOperator(task_id="get_purchases", python_callable=query_db, op_kwargs={"query": "SELECT customer_id, string_agg(store_id, ',') FROM customers GROUP BY customer_id"})
```

The previous steps describe roughly how to set up a Python package, but your process might differ depending on your setup and how your organization manages code. In general, these are some key pointers and considerations for setting up a custom Python package:

- Think about how you distribute the Python package. Do you require/have an internal repository for storing Python packages such as [Artifactory](https://jfrog.com/artifactory) or [devpi](https://www.devpi.net)?
- Determine who is responsible for maintaining the shared Git repository.
- Set developments standards from the beginning, such as Flake8 linting and Black formatting.
- Ensure the end-to-end CI/CD pipeline works first, then start developing application code.

## Planning for the future

This guide demonstrates several solutions for sharing code, from code in a single file to code across multiple Git repositories. If you're currently only deploying from a single Git repository to the Astronomer platform, but plan for multiple teams in the future, we advise you start with shared code in a separate Git repository. Setting standards and best practices from the beginning is easier than introducing changes in hindsight.
