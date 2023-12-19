---
title: 'Create DAG documentation in Apache Airflow'
sidebar_label: 'Write DAG documentation'
id: custom-airflow-ui-docs-tutorial
description: "Use Apache Airflow's built-in documentation features to generate documentation for your DAGs in the Airflow UI."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

One of the more powerful and lesser-known features of Airflow is that you can create Markdown-based DAG documentation that appears in the Airflow UI

![DAG Docs Intro Example](/img/guides/DAG_docs_intro_example.png)

After you complete this tutorial, you'll be able to:

- Add custom doc strings to an Airflow DAG.
- Add custom doc strings to an Airflow task.

## Time to complete

This tutorial takes approximately 15 minutes to complete.

## Assumed knowledge

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli).

## Step 1: Create an Astro project

To run Airflow locally, you first need to create an Astro project.

1. Create a new directory for your Astro project:

    ```sh
    mkdir <your-astro-project-name> && cd <your-astro-project-name>
    ```

2. Run the following Astro CLI command to initialize an Astro project in the directory:

    ```sh
    astro dev init
    ```

3. To enable raw HTML in your Markdown DAG descriptions, add the following Airflow config environment variable to your `.env` file. This will allow you to use HTML in your DAG descriptions. If you don't want to enable this setting due to security concerns you will still be able to use Markdown in your DAG descriptions and the HTML shown in this tutorial will be displayed as raw content.

    ```text
    AIRFLOW__WEBSERVER__ALLOW_RAW_HTML_DESCRIPTIONS=True
    ```

4. Start your Airflow instance by running:

    ```sh
    astro dev start
    ```

## Step 2: Create a new DAG

1. In your `dags` folder, create a file named `docs_example_dag.py`. 

2. Copy and paste one of the following DAGs based on which coding style you're most comfortable with.

<Tabs
    defaultValue="TaskFlowAPI"
    groupId="step-2-create-a-new-dag"
    values={[
        {label: 'TaskFlow API', value: 'TaskFlowAPI'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="TaskFlowAPI">

```python
from airflow.decorators import task, dag
from pendulum import datetime
import requests

@dag(
    start_date=datetime(2022,11,1),
    schedule="@daily",
    catchup=False
)
def docs_example_dag():

    @task
    def tell_me_what_to_do():
        response = requests.get("https://www.boredapi.com/api/activity")
        return response.json()["activity"]

    tell_me_what_to_do()

docs_example_dag()
```

</TabItem>

<TabItem value="traditional">

```python
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime
import requests

def query_api():
    response = requests.get("https://www.boredapi.com/api/activity")
    return response.json()["activity"]

with DAG(
    dag_id="docs_example_dag",
    start_date=datetime(2022,11,1),
    schedule=None,
    catchup=False,
):

    tell_me_what_to_do = PythonOperator(
        task_id="tell_me_what_to_do",
        python_callable=query_api,
    )
```

</TabItem>

</Tabs>

This DAG has one task called `tell_me_what_to_do`, which queries an [API](https://www.boredapi.com/api/activity) that provides a random activity for the day and prints it to the logs. 

## Step 3: Add docs to your DAG

You can add Markdown-based documentation to your DAGs that will render in the **Grid**, **Graph** and **Calendar** pages of the Airflow UI.

1. In your `docs_example_dag.py` file, add the following doc string above the definition of your DAG:

    ```python
    doc_md_DAG = """
    ### The Activity DAG

    This DAG will help me decide what to do today. It uses the [BoredAPI](https://www.boredapi.com/) to do so.

    Before I get to do the activity I will have to:

    - Clean up the kitchen.
    - Check on my pipelines.
    - Water the plants.

    Here are some happy plants:

    <img src="https://www.publicdomainpictures.net/pictures/80000/velka/succulent-roses-echeveria.jpg" alt="plants" width="300"/>
    """
    ```

    This doc string is written in Markdown. It includes a title, a link to an external website, a bulleted list, as well as an image which has been formatted using HTML. To learn more about Markdown, see [The Markdown Guide](https://www.markdownguide.org/).

2. Add the documentation to your DAG by passing `doc_md_DAG` to the `doc_md` parameter of your DAG class as shown in the code snippet below:

<Tabs
    defaultValue="TaskFlowAPI"
    groupId="step-3-add-docs-to-your-dag"
    values={[
        {label: 'TaskFlow API', value: 'TaskFlowAPI'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="TaskFlowAPI">

```python
@dag(
    start_date=datetime(2022,11,1),
    schedule="@daily",
    catchup=False,
    doc_md=doc_md_DAG
)
def docs_example_dag():
```

</TabItem>

<TabItem value="traditional">

```python
with DAG(
    dag_id="docs_example_dag",
    start_date=datetime(2022,11,1),
    schedule="@daily",
    catchup=False,
    doc_md=doc_md_DAG
):
```

</TabItem>

</Tabs>

3. Go to the **Grid** view and click on the **DAG Docs** banner to view the rendered documentation.

    ![DAG Docs](/img/guides/DAG_docs.png)

:::tip

Airflow will automatically pick up a doc string written directly beneath the definition of the DAG context and add it as **DAG Docs**.
Additionally, using `with DAG():` lets you pass the filepath of a markdown file to the `doc_md` parameter. This can be useful if you want to add the same documentation to several of your DAGs.

:::

## Step 4: Add docs to a task

You can also add docs to specific Airflow tasks using Markdown, Monospace, JSON, YAML or reStructuredText. Note that only Markdown will be rendered and other formats will be displayed as rich content. 

To add documentation to your task, follow these steps:

1. Add the following code with a string in Markdown format:

    ```python
    doc_md_task = """

    ### Purpose of this task

    This task **boldly** suggests a daily activity.
    """
    ```

2. Add the following code with a string written in monospace format:

    ```python
    doc_monospace_task = """
    If you don't like the suggested activity you can always just go to the park instead.
    """
    ```

3. Add the following code with a string in JSON format:

    ```python
    doc_json_task = """
    {
        "previous_suggestions": {
            "go to the gym": ["frequency": 2, "rating": 8],
            "mow your lawn": ["frequency": 1, "rating": 2],
            "read a book": ["frequency": 3, "rating": 10],
        }
    }
    """
    ```

4. Add the following code with a string written in YAML format:

    ```python
    doc_yaml_task = """
    clothes_to_wear: sports
    gear: |
        - climbing: true
        - swimming: false
    """
    ```

5. Add the following code containing reStructuredText:

    ```python
    doc_rst_task = """
    ===========
    This feature is pretty neat
    ===========

    * there are many ways to add docs
    * luckily Airflow supports a lot of them

    .. note:: `Learn more about rst here! <https://gdal.org/contributing/rst_style.html#>`__
    """
    ```

6. Create a task definition as shown in the following snippet. The task definition includes parameters for specifying each of the documentation strings you created. Pick the coding style you're most comfortable with.

<Tabs
    defaultValue="TaskFlowAPI"
    groupId="step-4-add-docs-to-a-task"
    values={[
        {label: 'TaskFlow API', value: 'TaskFlowAPI'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="TaskFlowAPI">

```python
@task(
    doc_md=doc_md_task,
    doc=doc_monospace_task,
    doc_json=doc_json_task,
    doc_yaml=doc_yaml_task,
    doc_rst=doc_rst_task
)
def tell_me_what_to_do():
    response = requests.get("https://www.boredapi.com/api/activity")
    return response.json()["activity"]

tell_me_what_to_do()
```

</TabItem>

<TabItem value="traditional">

```python
tell_me_what_to_do = PythonOperator(
    task_id="tell_me_what_to_do",
    python_callable=query_api,
    doc_md=doc_md_task,
    doc=doc_monospace_task,
    doc_json=doc_json_task,
    doc_yaml=doc_yaml_task,
    doc_rst=doc_rst_task
)
```

</TabItem>

</Tabs>

3. Go to the Airflow UI and run your DAG.

4. In the **Grid** view, click on the green square for your task instance.

5. Click on **Task Instance Details**.

    ![Task Instance Details](/img/guides/task_instance_details.png)

6. See the docs under their respective attribute:

    ![All Task Docs](/img/guides/task_docs_all.png)

## Step 5: Add notes to a task instance and DAG run

Starting in Airflow 2.5, you can add notes to task instances and DAG runs from the **Grid** view in the Airflow UI. This feature is useful if you need to share contextual information about a DAG or task run with your team, such as why a specific run failed.

1. Go to the **Grid View** of the `docs_example_dag` DAG you created in [Step 2](#step-2-create-a-new-dag).

2. Select a task instance or DAG run.

3. Click **Details** > **Task Instance Notes** or **DAG Run notes** > **Add Note**.

4. Write a note and click **Save Note**.

 ![Add task note](/img/guides/2_5_task_notes.png)

## Conclusion

Congratulations! You now know how to add fancy documentation to both your DAGs and your Airflow tasks.