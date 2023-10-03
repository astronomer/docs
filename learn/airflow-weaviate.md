---
title: "Orchestrate Weaviate operations with Apache Airflow"
sidebar_label: "Weaviate"
description: "Learn how to integrate Weaviate and Airflow."
id: airflow-weaviate
sidebar_custom_props: { icon: 'img/integrations/weaviate.png' }
---

import CodeBlock from '@theme/CodeBlock';
import query_movie_vectors from '!!raw-loader!../code-samples/dags/airflow-weaviate/query_movie_vectors.py';

[Weaviate](https://weaviate.io/developers/weaviate) is an open source vector database. Vector databases are powerful tools to store high-dimensional embeddings of objects like text, images, audio or video. The Weaviate Airflow provider offers operators and decorators to easily integrate Weaviate with Airflow.

In this tutorial you'll use Airflow to ingest movie descriptions into Weaviate, use Weaviate's automatic vectorization to create vectors for the descriptions, and query Weaviate for movies that are thematically close to user-provided concepts.

:::caution

The provider used in this tutorial is currently in beta and subject to change. Once the provider is released, this tutorial will be updated and the provider source code will be available. The example code from this tutorial is also available on [GitHub](https://github.com/astronomer/airflow-weaviate-tutorial). 

:::

## Why use Airflow with Weaviate?

Weaviate allows you to store and search for objects with vectors based on object-similarity. Many modern machine learning models use vector embeddings, such as [LLMs](https://en.wikipedia.org/wiki/Large_language_model) or [ResNet](https://arxiv.org/abs/1512.03385).

Integrating Weaviate with Airflow into one end-to-end machine learning pipeline allows you to:

- Use Airflow's [data-driven scheduling](airflow-datasets.md) to run operations on Weaviate based on upstream events in your data ecosystem (e.g. when a new model is trained, or a new dataset is available).
- Run dynamic queries based on upstream events in your data ecosystem or user input via [Airflow params](airflow-params.md) against Weaviate to retrieve objects with similar vectors.
- Add Airflow features like [retries](rerunning-dags.md#automatically-retry-tasks) and [alerts](error-notifications-in-airflow.md) to your Weaviate operations.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Weaviate. See [Weaviate Introduction](https://weaviate.io/developers/weaviate).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow decorators. [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- Airflow hooks. See [Hooks 101](what-is-a-hook.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

This tutorial uses a local Weaviate instance created as a Docker container. You do not need to install the Weaviate client locally.

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-weaviate-tutorial && cd astro-weaviate-tutorial
    $ astro dev init
    ```

2. Download the `whl` file for the Airflow Weaviate provider beta version from the [Astronomer Github repository](https://github.com/astronomer/learn-tutorials-data/blob/main/wheel_files/airflow_provider_weaviate-0.0.1-py3-none-any.whl) and save it in your Astro project's `include` directory.


3. Change the content of the `Dockerfile` of your Astro project to the following statement importing the`whl` file:

    ```dockerfile
    # syntax=quay.io/astronomer/airflow-extensions:latest

    FROM quay.io/astronomer/astro-runtime:9.1.0-base

    COPY include/airflow_provider_weaviate-0.0.1-py3-none-any.whl /tmp
    ```

4. Add the following install statement to your `requirements.txt` file to install the Airflow Weaviate provider from the `whl` file:

    ```text
    /tmp/airflow_provider_weaviate-0.0.1-py3-none-any.whl
    ```

:::caution

The Airflow Weaviate provider is currently in beta and not yet available on PyPI.

:::

5. This tutorial uses a local Weaviate instance and a text2vec-transformer model, each running in a Docker container. To add additional containers to your Astro project, create a new file in your project's root directory called `docker-compose.override.yml` and add the following:

    ```yaml
    version: '3.1'
    services:           
    weaviate:
      image: semitechnologies/weaviate:latest
      command: "--host 0.0.0.0 --port '8081' --scheme http"
      ports:
        - 8081:8081
      environment:
      QUERY_DEFAULTS_LIMIT: 25
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'text2vec-transformers'
      ENABLE_MODULES: 'text2vec-transformers'
      CLUSTER_HOSTNAME: 'node1'
      AUTHENTICATION_APIKEY_ENABLED: 'true'
      AUTHENTICATION_APIKEY_ALLOWED_KEYS: 'readonlykey,adminkey'
      AUTHENTICATION_APIKEY_USERS: 'jane@doe.com,john@doe.com'
      TRANSFORMERS_INFERENCE_API: 'http://t2v-transformers:8080'
      networks:
        - airflow
    t2v-transformers:
      image: semitechnologies/transformers-inference:sentence-transformers-multi-qa-MiniLM-L6-cos-v1
      environment:
      ENABLE_CUDA: 0 # set to 1 to enable
      ports:
        - 8082:8080
      networks:
        - airflow
    ```

:::info

Note that it is possible to use a remote transformer model by changing the `TRANSFORMERS_INFERENCE_API` value in the `docker-compose.override.yml` file. See the Weaviate documentation on [modules](https://weaviate.io/developers/weaviate/modules) for more information. When a remote model is used the `t2v-transformers` container can be removed from the `docker-compose.yaml` file.

:::

6. To create an [Airflow connection](connections.md) to Weaviate, add the following to your `.env` file:

    ```text
    AIRFLOW_CONN_WEAVIATE_ADMIN='{"conn_type": "weaviate", "host": "http://weaviate:8081/", "extra": {"token": "adminkey"}}'
    AIRFLOW_CONN_WEAVIATE_USER='{"conn_type": "weaviate", "host": "http://weaviate:8081/", "extra": {"token": "readonlykey"}}'
    ```

:::tip

See the Weaviate documentation on [environment variables](https://weaviate.io/developers/weaviate/config-refs/env-vars) and [modules](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules) for more information on configuring a Weaviate instance.

:::

## Step 2: Add your data

The DAG in this tutorial runs a query on vectorized movie descriptions from [IMDB](https://www.imdb.com/). If you are running the project locally, we recommend testing the pipeline with a small subset of the data. If you are running the project on a remote server, you can use the [full dataset](https://github.com/astronomer/learn-tutorials-data/blob/main/movie_descriptions.txt).

1. To make the data available to your Astro project, create a new folder called `movie_data` in your project's `include` directory.

2. Create a new file called `movie_data.txt` in the `movie_data` directory and copy and paste the following information:

    ```text
    1 ::: Arrival (2016) ::: sci-fi ::: A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.
    2 ::: Don't Look Up (2021) ::: drama ::: Two low-level astronomers must go on a giant media tour to warn humankind of an approaching comet that will destroy planet Earth.
    3 ::: Primer (2004) ::: sci-fi ::: Four friends/fledgling entrepreneurs, knowing that there's something bigger and more innovative than the different error-checking devices they've built, wrestle over their new invention.
    4 ::: Serenity (2005) ::: sci-fi ::: The crew of the ship Serenity try to evade an assassin sent to recapture telepath River.
    ```

3. Create a new file called `text_to_parquet_script.py` in the `movie_data` directory. Copy the script below which contains a function to create a [parquet file](https://parquet.apache.org/docs/) from `movie_data.txt`.

    ```python
    import pandas as pd
    import re
    from uuid import uuid4

    def create_parquet_file_from_txt(text_file_path, parquet_file_path):
        with open(text_file_path, "r") as f:
            lines = f.readlines()

        num_skipped_lines = 0
        data = []
        for line in lines:
            parts = line.split(":::")
            title_year = parts[1].strip()
            match = re.match(r"(.+) \((\d{4})\)", title_year)
            try:
                title, year = match.groups()
                year = int(year)
            # skip malformed lines
            except:
                num_skipped_lines += 1
                continue

            genre = parts[2].strip()
            description = parts[3].strip()

            year = int(year)

            data.append((str(uuid4()), title, year, genre, description))

        df = pd.DataFrame(
            data, columns=["movie_id", "title", "year", "genre", "description"]
        )

        print(df.head())
        print(
            f"Created a dataframe with shape {df.shape} while skipping {num_skipped_lines} lines."
            f"Saving to {parquet_file_path}."
        )

        df.to_parquet(parquet_file_path, index=False)
    ```

## Step 3: Define your vector schema

In order to prepare Weaviate to ingest your data, you need to define a [schema](https://weaviate.io/developers/weaviate/tutorials/schema). The WeaviateCreateSchemaOperator allows you to do so based on a JSON file. Vector embeddings will later be added to the schema by Weaviate.

1. In your `include/movie_data` folder, create a new file called `movie_schema.json`.

2. Add the following schema definition to the file:

    ```json
    {
        "classes": [
            {
                "class": "Movie",
                "description": "A movie",
                "properties": [
                    {
                        "name": "movie_id",
                        "description": "Primary Key, unique id",
                        "dataType": [
                            "text"
                        ]
                    },
                    {
                        "name": "title",
                        "description": "The title of the movie",
                        "dataType": [
                            "text"
                        ]
                    },
                    {
                        "name": "year",
                        "description": "The year when the movie was released",
                        "dataType": [
                            "int"
                        ]
                    },
                    {
                        "name": "genre",
                        "description": "The genre of the movie",
                        "dataType": [
                            "text"
                        ]
                    },
                    {
                        "name": "description",
                        "description": "The IMDB description of the movie",
                        "dataType": [
                            "text"
                        ]
                    }
                ]
            }
        ]
    }
    ```

## Step 4: Create your DAG

1. In your `dags` folder, create a file called `query_movie_vectors.py`.

2. Copy the following code into the file.

    <CodeBlock language="python">{query_movie_vectors}</CodeBlock>

    This DAG consists of seven tasks comprising a simple ML orchestration pipeline.

    - The `check_schema` task uses the [WeaviateCheckSchemaOperator](https://registry.astronomer.io/) to check if the schema defined in `movie_schema.json` already exists in Weaviate.
    - The `branch_create_schema` is defined with a `@task.branch` operator to decide whether the `create_schema` task should be run based on the result of the `check_schema` task. If the schema already exists, the empty `schema_exists` task is run instead.
    - The `create_schema` task uses the [WeaviateCreateSchemaOperator](https://registry.astronomer.io/) to create the schema defined in `movie_schema.json` in Weaviate. 
    - The `create_parquet_file` task runs the function defined in the `text_to_parquet_script.py` file to create a parquet file from the `movie_data.txt` file.
    - The `ingest_data` task defined using the [@task.weaviate_import](https://registry.astronomer.io/) decorator ingests the data into Weaviate. Note that you can run any Python code on the data before ingesting it into Weaviate, making it possible to create your own embeddings or complete other transformations before it is ingested. To import your own vectors, specify the column containing vectors in the dictionary that is returned by the task with the key `embedding_column`:

    ```python
    @task.weaviate_import(
        weaviate_conn_id=WEAVIATE_ADMIN_CONN_ID, trigger_rule="none_failed"
    )
    def import_data(class_name):
        """Import the movie data into Weaviate using automatic weaviate embeddings."""
        import pandas as pd

        df = pd.read_parquet(PARQUET_FILE_PATH)

        df["vectors"] = # code generating vectors

        return {
            "data": df,
            "class_name": class_name,
            "uuid_column": "movie_id",
            "embedding_column": "vectors",
        }
    ```

    - The `query_embeddings` task uses the [WeaviateHook](https://registry.astronomer.io/) to connect to the Weaviate instance and run a GraphQL query on the vector embeddings created by Weaviate using the `text2vec-transformers` module running in the `t2v-transformers` container. The query returns the most similar movies to the concepts provided by the user when running the DAG in the next step.

## Step 5: Run your DAG

1. Run `astro dev start` in your Astro project to start up Airflow and open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `query_movie_vectors` DAG by clicking the play button. You will be prompted to provider [Airflow params](airflow-params.md) for `movie_concepts` and the `certainty_threshold_percent`.

    Note that if you are running the project locally on a larger dataset, the `import_data` task might take a longer time to complete because Weaviate generates the vector embeddings in this task.

    ![Screenshot of the Airflow UI showing the `query_movie_vectors` DAG having completed successfully in the Grid view with the Graph tab selected. Since this was the first run of the DAG the schema had to be newly created which was enabled by the branching task `branch_create_schema` selecting the downstream `create_schema` task to run.](/img/tutorials/airflow-weaviate_successful_dag.png)


3. View your movie suggestion in the task logs of the `query_embeddings` task:

    ```text
    [2023-09-21, 11:45:30 UTC] {logging_mixin.py:151} INFO - The top result for the concept(s) ['innovation', 'ensemble'] is:
    [2023-09-21, 11:45:30 UTC] {logging_mixin.py:151} INFO - The movie Primer, released in 2004.
    [2023-09-21, 11:45:30 UTC] {logging_mixin.py:151} INFO - IMDB describes the movie as: Four friends/fledgling entrepreneurs, knowing that there's something bigger and more innovative than the different error-checking devices they've built, wrestle over their new invention.
    [2023-09-21, 11:45:30 UTC] {logging_mixin.py:151} INFO - The certainty of the result is 0.624.
    ```

## Conclusion

Congratulations! You used Airflow and Weaviate to get your next movie suggestion! This beta tutorial showed the use of three different Weaviate operators and decorators and the WeaviateHook, more operators and decorators will be available upon the release of the provider.

