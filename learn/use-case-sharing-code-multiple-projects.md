---
title: "How to share code between multiple projects"
description: "In this page we elaborate on various ways to reuse and share code between multiple projects, and explain the pros and cons of each solution."
id: sharing-code-multiple-projects
sidebar_label: "Sharing code between multiple projects"
---

Imagine you've [set up an Astro project](cli/develop-project.md), you're getting into the flow of implementing some pipelines, you're extracting several Python functions for reusability, and things are scaling up. You've now got multiple Airflow deployments, but how do you reuse code between your projects? This is a common question and in this page we'll lay out various options for reusing code and their pros and cons.

Specifically, we'll demonstrate three options, sorted from simple implementation but poor reusability to detailed implementation but excellent reusability:

1. Shared Python code in same file
2. Shared Python code in `/include` folder
3. Shared Python code in Python package in separate project

Let's assume we have multiple tasks querying a database and returning results:

```python
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

# Shared Python code in same file
Let's start with the simplest option for reusing code: the code above performs the same business logic twice. Both functions instantiate a database client, execute a query, and return the result. The only difference is the query being executed. Any change to the database connection logic now requires two changes. If we continue copy-pasting these functions for running more queries, we would end up having X copies of the same business logic, which also requires X code changes when you want to modify the database connection logic. To reduce this maintenance burden, and have only one way of querying the database, let's extract code into a single function:

```python
def query_db(query):
    # Pseudocode:
    client = db.client()
    result = client.execute(query)
    return result
```

This function takes an argument `query`, and the database connection logic is only defined once regardless what query is given. This way you don't have to maintain the same business logic in multiple places anymore. To use this function, you reference it in your DAG script:

```python
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

# Shared Python code in `/include` folder
To reuse a piece of code across scripts it needs to be accessible in a shared location. The Astro Runtime Docker image provides a convenient mechanism for that, the `/include` folder:

Store the function in a separate file, for example `/include/db.py`:
```python
def query_db(query):
    # Pseudocode:
    client = db.client()
    result = client.execute(query)
    return result
```

And then import the function from your DAG in `/dags/example.py`:
```python {6}
import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from include.db import query_db

with DAG(dag_id="example", schedule=None, start_date=datetime.datetime(2023, 1, 1)):
    PythonOperator(task_id="get_locations", python_callable=query_db, op_kwargs={"query": "SELECT store_id, city FROM stores"})
    PythonOperator(task_id="get_purchases", python_callable=query_db, op_kwargs={"query": "SELECT customer_id, string_agg(store_id, ',') FROM customers GROUP BY customer_id"})
```

The benefit of this solution is that the `query_db` function can be imported from multiple scripts (in the same Git repository).

# Shared Python code in Python package in separate project

Now let's say you're onboarding multiple teams to the Astronomer platform, and each team has their own code repository. This means you can't reuse the code in the `/include` folder, because it resides in a different Git repository.

To reuse code over multiple projects, we need to store it in a separate Git repository which can be reused by multiple projects. This takes a bit more work to set up, but enables multiple teams using multiple Git repositories to maintain a single source of code. Take a look at https://github.com/astronomer/custom-package-demo for an example Python package. 

The number of options for developing, building, and releasing a Python package are limitless. Therefore, we can't describe every detail. Setting up a custom Python package requires roughly the following steps:

1. First, create a separate Git repository for your shared code.
2. Write a `pyproject.toml` file. This is a configuration file which contains the build requirements of your Python project. Take a look at https://github.com/astronomer/custom-package-demo/blob/main/pyproject.toml as an example.
3. Create a folder for your code, e.g. `my_company_airflow`.
4. Create a folder for tests, e.g. `tests`.
5. Create a CI/CD pipeline to test, build, and release your package. Take a look at https://github.com/astronomer/custom-package-demo/tree/main/.github/workflows as an example (GitHub Actions).
6. Ensure your setup works correctly by building and releasing a first version of the package.
7. Validate the package by installing it in a project via the `requirements.txt` file.
8. After steps 1-7 validate that you can automatically build and release your package, start adding application code.

The code example must now be added in a module in your Python package, for example `my_company_airflow/db.py`:

```python
def query_db(query):
    # Pseudocode:
    client = db.client()
    result = client.execute(query)
    return result
```

After installing the package, developers can then import the function in their DAGs as:

```python {6}
import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from my_company_airflow.db import query_db

with DAG(dag_id="example", schedule=None, start_date=datetime.datetime(2023, 1, 1)):
    PythonOperator(task_id="get_locations", python_callable=query_db, op_kwargs={"query": "SELECT store_id, city FROM stores"})
    PythonOperator(task_id="get_purchases", python_callable=query_db, op_kwargs={"query": "SELECT customer_id, string_agg(store_id, ',') FROM customers GROUP BY customer_id"})
```

The steps above describe roughly how to set up a Python package. Since the number of options here are limitless, we can't explain every step in detail. However, these are some key pointers/considerations for setting up a custom Python package:

- How will you distribute the Python package? Do you require/have an internal repository for storing Python packages such as [Artifactory](https://jfrog.com/artifactory) or [devpi](https://www.devpi.net)?
- Who is responsible for maintaining the shared Git repository?
- Set developments standards from the beginning (e.g. Flake8 linting and Black formatting).
- Ensure the end-to-end CI/CD pipeline works first, then start developing application code.

# Summary

The solutions above can be applied in the following situations:

| Solution                     | When to use                                                            |
|------------------------------|------------------------------------------------------------------------|
| Code in DAG script           | When reusing code only within a single script                          |
| Code in `/include` folder    | When reusing code in multiple scripts, but within the same Git project |
| Code in separate Git project | When reusing code in multiple Git projects                             |

If you're currently only deploying from a single Git repository to the Astronomer platform but plan for multiple teams in the future, we advise to start with shared code in a separate Git repository from the start. Setting standards from the beginning is easier than introducing changes in hindsight.
