---
title: 'Add documentation to your DAGs and tasks in the Airflow UI'
sidebar_label: 'Add docs to DAGs'
id: custom-airflow-ui-docs-tutorial
description: 'Use tutorials and guides to make the most out of Airflow and Astronomer.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Adding custom doc strings that will be shown in the Airflow UI to your DAGs and tasks is a lesser known but powerful Airflow feature.

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

3. Start your Airflow instance by running:

    ```sh
    astro dev start
    ```

## Step 2: Create a new DAG

1. In your `dags` folder, add a file called `docs_example_dag.py`. 

2. Copy and paste the DAG code provided below. Choose one of either the TaskFlowAPI or traditional operators DAGs.

<Tabs
    defaultValue="TaskFlowAPI"
    groupId= "code-variations"
    values={[
        {label: 'TaskFlowAPI', value: 'TaskFlowAPI'},
        {label: 'Traditional Operator', value: 'traditional'},
    ]}>

<TabItem value="TaskFlowAPI">

```python
from airflow import DAG
from airflow.decorators import task, dag
from pendulum import datetime
import requests

@dag(
    start_date=datetime(2022,11,1),
    schedule="@daily",
    catchup=False
)
def docs_example_dag():

    @task()
    def tell_me_what_to_do():
        response = requests.get("https://www.boredapi.com/api/activity")
        return response.json()["activity"]

    tell_me_what_to_do()

docs_example_dag()
```

</TabItem>

<TabItem value="traditional">

```python
from airflow import DAG
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

In Airflow you can add custom documentation to your DAGs in Markdown format that will render in the **Grid**, **Graph** and **Calendar** views.

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

    <img src="https://www.publicdomainpictures.net/pictures/80000/velka/succulent-roses-echeveria.jpg" alt="drawing" width="300"/>
    """
    ```

    This doc string is written in Markdown format. It includes a title, a link to an external website, a bulleted list, as well as an image, which has been formatted using HTML. To learn more about Markdown, check out this [Markdown Guide](https://www.markdownguide.org/).

2. Add the documentation to your DAG by passing `doc_md_DAG` to the `doc_md` parameter of your DAG class as shown in the code snippet below:

<Tabs
    defaultValue="TaskFlowAPI"
    groupId= "code-variations"
    values={[
        {label: 'DAG decorator', value: 'TaskFlowAPI'},
        {label: 'Traditional DAG context', value: 'traditional'},
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

## Step 4: Add docs to your DAG using doc strings

Many users use doc strings to document their DAG code. Airflow is able to pick up those strings and turn them into DAG Docs.

1. Remove the `doc_md` parameter from your DAG code.

2. Copy and paste the doc string as shown in the code snippets below:

<Tabs
    defaultValue="TaskFlowAPI"
    groupId= "code-variations"
    values={[
        {label: 'DAG decorator', value: 'TaskFlowAPI'},
        {label: 'Traditional DAG context', value: 'traditional'},
    ]}>

<TabItem value="TaskFlowAPI">

```python
@dag(
    start_date=datetime(2022,11,1),
    schedule="@daily",
    catchup=False,
)
def docs_example_dag():

    """
    ### The Activity DAG

    This DAG will help me decide what to do today. It uses the [BoredAPI](https://www.boredapi.com/) to do so.

    My favorite suggestions so far were:

    - Make bread from scratch
    - Make a couch fort
    - Take your cat on a walk
    """
```

</TabItem>

<TabItem value="traditional">

```python
with DAG(
    dag_id="docs_example_dag",
    start_date=datetime(2022,11,1),
    schedule="@daily",
    catchup=False,
):
    """
    ### The Activity DAG

    This DAG will help me decide what to do today. It uses the [BoredAPI](https://www.boredapi.com/) to do so.

    My favorite suggestions so far were:

    - Make bread from scratch
    - Make a couch fort
    - Take your cat on a walk
    """
```

</TabItem>

</Tabs>

3. In the **Graph** view of your DAG click on **DAG docs** to view your documentation.

    ![DAG Docs 2](/img/guides/DAG_docs_2.png)

:::info

When using the `with DAG():` syntax it is possible to pass the filepath to a markdown file to the `doc_md` parameter. This can be useful if you want to add the same documentation to several of your DAGs.

:::

## Step 5: Add docs to a task

You can also add docs to specific Airflow tasks using Markdown, Monospace, JSON, YAML or reStructured text. Note that only Markdown will be rendered, other formats will be displayed as rich content.

<Tabs
    defaultValue="markdown"
    groupId= "DAG-docs"
    values={[
        {label: 'Markdown', value: 'markdown'},
        {label: 'Monospace', value: 'monospace'},
        {label: 'JSON', value: 'json'},
        {label: 'YAML', value: 'yaml'},
        {label: 'reStructuredText', value: 'rst'},
    ]}>


<TabItem value="markdown">

To add documentation to your task in Markdown format, follow these steps:

1. Add the following code above the definition of your task:

    ```python
    doc_md_task = """

    ### Purpose of this task

    This task **boldly** suggests a daily activity.
    """
    ```

2. Provide `doc_md_task` to the `doc_md` parameter of your task definition. If you are using traditional operators simply add it below the `python_callable` parameter.

    ```python
    @task(
        doc_md=doc_md_task
    )
    def tell_me_what_to_do():
        response = requests.get("https://www.boredapi.com/api/activity")
        return response.json()["activity"]

    tell_me_what_to_do()
    ```

    ```python
    tell_me_what_to_do = PythonOperator(
        task_id="tell_me_what_to_do",
        python_callable=query_api,
        doc_md=doc_md_task
    )
    ```

</TabItem>

<TabItem value="monospace">

To add documentation in Monospace format to your task follow these steps:

1. Add the code below above the definition of your task:

    ```python
    doc_task = """
    If you don't like the suggested activity you can always just go to the park instead.
    """
    ```

2. Provide `doc_task` to the `doc` parameter of your task definition. If you are using traditional operators simply add it below the `python_callable` parameter.

    ```python
    @task(
        doc=doc_task
    )
    def tell_me_what_to_do():
        response = requests.get("https://www.boredapi.com/api/activity")
        return response.json()["activity"]

    tell_me_what_to_do()
    ```

    ```python
    tell_me_what_to_do = PythonOperator(
        task_id="tell_me_what_to_do",
        python_callable=query_api,
        doc=doc_task
    )
    ```

</TabItem>

<TabItem value="json">

To add documentation in JSON format to your task follow these steps:

1. Add the code below above the definition of your task:

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

2. Provide `doc_json_task` to the `doc_json` parameter of your task definition. If you are using traditional operators simply add it below the `python_callable` parameter.

    ```python
    @task(
        doc_json=doc_json_task
    )
    def tell_me_what_to_do():
        response = requests.get("https://www.boredapi.com/api/activity")
        return response.json()["activity"]

    tell_me_what_to_do()
    ```

    ```python
    tell_me_what_to_do = PythonOperator(
        task_id="tell_me_what_to_do",
        python_callable=query_api,
        doc_json=doc_json_task
    )
    ```

</TabItem>

<TabItem value="yaml">

To add documentation in YAML format to your task follow these steps:

1. Add the code below above the definition of your task:

    ```python
    doc_yaml_task = """
    clothes_to_wear: sports
    gear: |
        - climbing: true
        - swimming: false
    """
    ```

2. Provide `doc_yaml_task` to the `doc_yaml` parameter of your task definition. If you are using traditional operators simply add it below the `python_callable` parameter.

    ```python
    @task(
        doc_yaml=doc_yaml_task
    )
    def tell_me_what_to_do():
        response = requests.get("https://www.boredapi.com/api/activity")
        return response.json()["activity"]

    tell_me_what_to_do()
    ```

    ```python
    tell_me_what_to_do = PythonOperator(
        task_id="tell_me_what_to_do",
        python_callable=query_api,
        doc_yaml=doc_yaml_task
    )
    ```

</TabItem>

<TabItem value="rst">

To add documentation in reStructuredText format to your task follow these steps:

1. Add the code below above the definition of your task:

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

2. Provide `doc_rst_task` to the `doc_rst` parameter of your task definition. If you are using traditional operators simply add it below the `python_callable` parameter.

    ```python
    @task(
        doc_rst=doc_rst_task
    )
    def tell_me_what_to_do():
        response = requests.get("https://www.boredapi.com/api/activity")
        return response.json()["activity"]

    tell_me_what_to_do()
    ```

    ```python
    tell_me_what_to_do = PythonOperator(
        task_id="tell_me_what_to_do",
        python_callable=query_api,
        doc_rst=doc_rst_task
    )
    ```

</TabItem>

</Tabs>

3. Go to the Airflow UI and run your DAG.

4. In the **Grid** view, click on the green square for your task instance.

5. Click on **Task Instance Details**.

    ![Task Instance Details](/img/guides/task_instance_details.png)

6. See the Docs under their respective attribute:

<Tabs
    defaultValue="markdown"
    groupId= "DAG-docs"
    values={[
        {label: 'Markdown', value: 'markdown'},
        {label: 'Monospace', value: 'monospace'},
        {label: 'JSON', value: 'json'},
        {label: 'YAML', value: 'yaml'},
        {label: 'reStructuredText', value: 'rst'},
    ]}>


<TabItem value="markdown">

![Markdown Task Docs](/img/guides/task_docs_markdown.png)

</TabItem>

<TabItem value="monospace">

![Monospace Task Docs](/img/guides/task_docs_mono.png)

</TabItem>

<TabItem value="json">

![JSON Task Docs](/img/guides/task_docs_json.png)

</TabItem>

<TabItem value="yaml">

![YAML Task Docs](/img/guides/task_docs_yaml.png)

</TabItem>

<TabItem value="rst">

![rst Task Docs](/img/guides/task_docs_rst.png)

</TabItem>

</Tabs>

## Conclusion

Congratulations! You now know how to add fancy documentation to both your DAGs and your Airflow tasks.