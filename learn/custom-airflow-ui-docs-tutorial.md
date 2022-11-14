---
title: 'Add documentation to your DAGs and tasks in the Airflow UI'
sidebar_label: 'DAG Docs - Add docs in the UI'
id: custom-airflow-ui-docs-tutorial
description: 'Use tutorials and guides to make the most out of Airflow and Astronomer.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Adding custom doc strings to your Airflow DAGs and tasks that will be shown in the Airflow UI is a lesser known but powerful Airflow feature.

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

To run Airflow locally, you first need to create an Astro project, which contains the set of files necessary.

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

1. In your `dags` folder add a file called `docs_example_dag.py`. 

2. Copy and paste the DAG code provided below, you can use either the TaskFlowAPI version or the version using traditional operators.

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
from airflow.decorators import task
from pendulum import datetime
import requests

with DAG(
    dag_id="docs_example_dag",
    start_date=datetime(2022,11,1),
    schedule="@daily",
    catchup=False,
):

    @task()
    def tell_me_what_to_do():
        response = requests.get("https://www.boredapi.com/api/activity")
        return response.json()["activity"]

    tell_me_what_to_do()
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

This DAG has only one task called `tell_me_what_to_do` which queries and [API](https://www.boredapi.com/api/activity) that provides a random activity for the day and prints it into the logs. 

## Step 3: Add documentation to an Airflow DAG

Airflow will let you add documentation to your DAGs in Markdown format and render that documentation in both the **Grid**, **Graph** and **Calendar** view.

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

    This doc string is written in Markdown format. It includes a title, a link to an external website, a bulleted list, as well as an image, which has been formatted using HTML. You can learn more about [Markdown Guide](https://www.markdownguide.org/).

2. Add the documentation to your DAG by passing `doc_md_DAG` to the `doc_md` parameter of your DAG class as shown in the code snippet below:

    ```python
    with DAG(
        dag_id="docs_example_dag",
        start_date=datetime(2022,11,1),
        schedule="@daily",
        catchup=False,
        doc_md=doc_md_DAG
    ):
    ```

3. In the **Grid** view click on the **DAG Docs** banner to view the rendered documentation.

    ![DAG Docs](/img/guides/DAG_docs.png)

4. (Optional) It is possible to save the documentation in a markdown file and directly provide the filepath to the `doc_md` parameter of the DAG class. 

    - Create a `documentation` directory within your `dags` folder.
    - Create a markdown file called `my_dag_docs.md` in this folder.
    - Copy and paste the contents of the markdown string into the new file. Delete the wrapping triple quotes.
    - Set the `doc_md` parameter of your DAG to `documenation/my_dag_docs.md`

## Step 4: Add documentation to an Airflow task

Airflow supports adding documentation to Airflow tasks in Markdown, Monospace, JSON, YAML and reStructured text. Note that only Markdown will be rendered, other formats will be displayed as rich content.

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

To add documentation in Markdown format to your task follow these steps:

1. Add the code below above the definition of your task:

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

3. Go to the Airflow UI and run your DAG.

4. In the **Grid** view click on the green square.

5. Click on **Task Instance Details**.

    ![Task Instance Details](/img/guides/task_instance_details.png)

6. See the markdown docs rendered under `Attribute: doc_md`.

    ![Markdown Task Docs](/img/guides/task_docs_markdown.png)

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

3. Go to the Airflow UI and run your DAG.

4. In the **Grid** view click on the green square.

5. Click on **Task Instance Details**.

    ![Task Instance Details](/img/guides/task_instance_details.png)

6. See the Monospace docs as rich content under `Attribute: doc`.

    ![Monospace Task Docs](/img/guides/task_docs_mono.png)

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

3. Go to the Airflow UI and run your DAG.

4. In the **Grid** view click on the green square.

5. Click on **Task Instance Details**.

    ![Task Instance Details](/img/guides/task_instance_details.png)

6. See the JSON docs as rich content under `Attribute: doc_json`.

    ![JSON Task Docs](/img/guides/task_docs_json.png)

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

3. Go to the Airflow UI and run your DAG.

4. In the **Grid** view click on the green square.

5. Click on **Task Instance Details**.

    ![Task Instance Details](/img/guides/task_instance_details.png)

6. See the YAML docs as rich content under `Attribute: doc_yaml`.

    ![YAML Task Docs](/img/guides/task_docs_yaml.png)

</TabItem>

<TabItem value="rst">

To add documentation in reStructuredText format to your task follow these steps:

1. Add the code below above the definition of your task:

    ```python
    doc_rst_task = """
    ===========
    This is feature is pretty neat
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

3. Go to the Airflow UI and run your DAG.

4. In the **Grid** view click on the green square.

5. Click on **Task Instance Details**.

    ![Task Instance Details](/img/guides/task_instance_details.png)

6. See the reStructuredText docs as rich content under `Attribute: doc_yaml`.

    ![rst Task Docs](/img/guides/task_docs_rst.png)

</TabItem>

</Tabs>

## Conclusion

Congratulations! You now know how to add fancy documentation to both your DAGs and your Airflow tasks.