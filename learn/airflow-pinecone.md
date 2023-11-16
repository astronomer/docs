---
title: "Orchestrate Pinecone operations with Apache Airflow"
sidebar_label: "Pinecone"
description: "Learn how to integrate Pinecone and Airflow."
id: airflow-pinecone
sidebar_custom_props: { icon: 'img/integrations/pinecone.png' }
---

[Pinecone](https://www.pinecone.io/) is a vector database platform designed for handling large-scale vector search and similarity search applications, leveraging machine learning models. The [Pinecone Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-pinecone/stable/index.html) offers modules to easily integrate Pinecone with Airflow.

In this tutorial you'll use Airflow to create vectors out of movie descriptions using [Sci-kit learn](https://pypi.org/project/scikit-learn/), create an index within Pinecone, upload those vectors into your index, and query the uploaded vectors with a movie ID to find similar movies!

## Why use Airflow with Pinecone? 
Integrating Pinecone with Airflow provides a robust solution for managing large-scale vector search workflows in machine learning applications. Pinecone specializes in efficient vector storage and similarity search, essential for leveraging advanced models like language transformers or deep neural networks.

By combining Pinecone with Airflow, you can:

- Use Airflow's [data-driven scheduling](airflow-datasets.md) to run operations on Pinecone based on upstream events in your data ecosystem, such as when a new model is trained or a new dataset is available.
- Run dynamic queries based on upstream events in your data ecosystem or user input via [Airflow params](airflow-params.md) against Pinecone to retrieve objects with similar vectors.
- Add Airflow features like [retries](rerunning-dags.md#automatically-retry-tasks) and [alerts](error-notifications-in-airflow.md) to your Pinecone operations.

## Time to complete 

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Pinecone. See [Pinecone Introduction](https://docs.pinecone.io/docs/overview).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow decorators. [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- Airflow hooks. See [Hooks 101](what-is-a-hook.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- A Pinecone account with an API key. You can use a free tier account for this example.

## Step 1: Configure your Astro project 

1. Create a new Astro project:

    ```sh
    $ mkdir astro-pinecone-tutorial && cd astro-pinecone-tutorial
    $ astro dev init
    ```

2. Add the following two packages to your `requirements.txt` file to install the [Pinecone Airflow Provider](https://airflow.apache.org/docs/apache-airflow-providers-pinecone/stable/index.html) and [scikit-learn](https://pypi.org/project/scikit-learn/) in your Astro project:

    ```text
    apache-airflow-providers-pinecone
    scikit-learn
    ```

## Step 2: Add your data

The DAG in this tutorial runs a query on vectorized movie descriptions from [IMDB](https://www.imdb.com/). 
Create a new file called `movie_data.txt` in the `include` directory, then copy and paste the following information:

```text
1 ::: Arrival (2016) ::: sci-fi ::: A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.
2 ::: Don't Look Up (2021) ::: drama ::: Two low-level astronomers must go on a giant media tour to warn humankind of an approaching comet that will destroy planet Earth.
3 ::: Primer (2004) ::: sci-fi ::: Four friends/fledgling entrepreneurs, knowing that there's something bigger and more innovative than the different error-checking devices they've built, wrestle over their new invention.
4 ::: Serenity (2005) ::: sci-fi ::: The crew of the ship Serenity try to evade an assassin sent to recapture telepath River.
5 ::: Upstream Colour (2013) ::: romance ::: A man and woman are drawn together, entangled in the life cycle of an ageless organism. Identity becomes an illusion as they struggle to assemble the loose fragments of wrecked lives.
6 ::: The Matrix (1999) ::: sci-fi ::: When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.
7 ::: Inception (2010) ::: sci-fi ::: A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster.
```

## Step 3 Create your DAG

1. In your `dags` folder, create a file called `pinecone_example.py`.

2. Copy the following code into the file.

```python
import json
from pendulum import datetime
from airflow.operators.empty import EmptyOperator
from airflow.decorators import (
    dag,
    task,
)  
from airflow.providers.pinecone.operators.pinecone import PineconeIngestOperator
from airflow.providers.pinecone.hooks.pinecone import PineconeHook
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import uuid

name_for_index = "testindex"


@dag(schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["pinecone"],
)  # If set, this tag is shown in the DAG view of the Airflow UI
def pinecone_example_dag():
    file_path = "include/moviedata.txt"

    start = EmptyOperator(task_id="start")

    def generate_uuid5(identifier):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, '/'.join([str(i) for i in identifier])))
    
    def get_vector_dimensions(data):
        return len(data[0]['vector'][0])

    def import_data_func(text_file_path: str):
        with open(text_file_path, "r") as f:
            lines = f.readlines()
            num_skipped_lines = 0
            descriptions = []
            data = []
            for line in lines:
                parts = line.split(":::")
                title_year = parts[1].strip()
                match = re.match(r"(.+) \((\d{4})\)", title_year)
                try:
                    title, year = match.groups()
                    year = int(year)
                except:
                    num_skipped_lines += 1
                    continue
                
                genre = parts[2].strip()
                description = parts[3].strip()
                descriptions.append(description)
                data.append(
                    {
                        "movie_id": generate_uuid5(
                            identifier=[title, year, genre, description]
                            ),
                            "title": title,
                            "year": year,
                            "genre": genre,
                            "description": description,
                        }
                    )
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(descriptions)
        for i, item in enumerate(data):
            item['vector'] = vectors[i].toarray().tolist()
        
        return data
        
    vector_data = import_data_func('include/moviedata.txt')
    vector_dims = get_vector_dimensions(vector_data)

    @task
    def createindex(vector_size: int):
        hook = PineconeHook(conn_id="pinecone")
        newindex = hook.create_index(index_name=name_for_index,
                                     dimension=vector_size)
        return newindex

    
    indexcreator = createindex(vector_size=vector_dims)

    @task
    def convert_to_pinecone_format(data):
        pinecone_data = []
        for item in data:
            if 'vector' in item and item['vector']:
                pinecone_data.append({
                    'id': item['movie_id'],
                    'values': item['vector'][0]
                    })
        return pinecone_data
    
    data_conversion = convert_to_pinecone_format(vector_data)


    ingestion = PineconeIngestOperator(task_id="pinecone_vector_ingest",
                                       conn_id="pinecone",
                                       index_name=name_for_index,
                                       input_vectors=data_conversion,)
    
    @task
    def query_pinecone(vector_data: list):
        hook = PineconeHook(conn_id="pinecone")

        query_vector = vector_data[0]['values']
        query_response = hook.query_vector(
            index_name=name_for_index,
            top_k=10,
            include_values=True,
            include_metadata=True,
            vector=query_vector
            )
        print(query_response)
    
    querytask = query_pinecone(vector_data=data_conversion)

    @task
    def delete_pinecone_index():
        hook = PineconeHook(conn_id="pinecone")
        deletion = hook.delete_index(index_name=name_for_index)

    clean_up_task = delete_pinecone_index()
    clean_up_task.as_teardown(setups=[indexcreator])

    
    start >> indexcreator >> data_conversion >> ingestion >> querytask >> clean_up_task



pinecone_example_dag()
```

This DAG consists of six Tasks and one function

- `Start Task` (EmptyOperator):This is a placeholder task that acts as the starting point of the DAG. It does not perform any action but is useful for structuring the workflow.
- `import_data_func` Function: This function reads movie data from a text file, processes it to extract titles, years, genres, and descriptions, and then vectorizes the descriptions using TF-IDF (Term Frequency-Inverse Document Frequency) from Scikit learn.
- `createindex` Task: This task creates a new index in Pinecone using the PineconeHook. It sets the dimension of the index to be the same as the dimension of the vectors created by the import_data_func.
- `convert_to_pinecone_format` Task: This task converts the data into a format compatible with Pinecone, where each movie's data is represented as a dictionary with an 'id' and 'values' (the vector).
- `ingestion` (PineconeIngestOperator): This operator handles the ingestion of the vector data into the Pinecone index. It uses the data converted into Pinecone format by the convert_to_pinecone_format task.
- `query_pinecone` Task: This task performs a vector search query in the Pinecone index. It uses the vector of the first movie as the query vector to find the top 10 most similar movies.
- `delete_pinecone_index` Task: This task deletes the Pinecone index that was created earlier in the DAG. It's set as a [teardown task](https://docs.astronomer.io/learn/airflow-setup-teardown), ensuring that the index is cleaned up after the DAG runs regardless of any other task success. This is done because the free tier of Pinecone only supports one index, so in order to be able to run the DAG multiple times, the index needs to be deleted between runs. 


## Step 4: Run your DAG

1. Run `astro dev start` in your Astro project to start Airflow and open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, go to the connections managment UI and create a new pinecone connection following the example in the screenshot below:

3. In the Airflow UI, run the `pinecone_example_dag` DAG by clicking the play button.

4. View your movie suggestion in the task logs of the `query_embeddings` task:

```text
    [2023-11-16, 18:42:32 UTC] {base.py:73} INFO - Using connection ID 'pinecone' for task execution.
    [2023-11-16, 18:42:32 UTC] {logging_mixin.py:154} INFO - {'matches': [], 'namespace': ''}
```

## Conclusion

Congrats! You've now successfully integrated Airflow and Pinecone! 



