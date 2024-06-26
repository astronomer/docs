---
title: "Orchestrate Weaviate operations with Apache Airflow"
sidebar_label: "Weaviate"
description: "Learn how to integrate Weaviate and Airflow."
id: airflow-weaviate
sidebar_custom_props: { icon: 'img/integrations/weaviate.png' }
---

import CodeBlock from '@theme/CodeBlock';
import query_movie_vectors from '!!raw-loader!../code-samples/dags/airflow-weaviate/query_movie_vectors.py';

[Weaviate](https://weaviate.io/developers/weaviate) is an open source vector database, which store high-dimensional embeddings of objects like text, images, audio or video. The [Weaviate Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-weaviate/stable/index.html) offers modules to easily integrate Weaviate with Airflow.

In this tutorial you'll use Airflow to ingest movie descriptions into Weaviate, use Weaviate's automatic vectorization to create vectors for the descriptions, and query Weaviate for movies that are thematically close to user-provided concepts.

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Webinar: [Power your LLMOps with Airflow’s Weaviate Provider](https://www.astronomer.io/events/webinars/power-your-llmops-with-airflows-weaviate-provider/).

:::

## Why use Airflow with Weaviate?

Weaviate allows you to store objects alongside their vector embeddings and to query these objects based on their similarity. Vector embeddings are key components of many modern machine learning models such as [LLMs](https://en.wikipedia.org/wiki/Large_language_model) or [ResNet](https://arxiv.org/abs/1512.03385).

Integrating Weaviate with Airflow into one end-to-end machine learning pipeline allows you to:

- Use Airflow's [data-driven scheduling](airflow-datasets.md) to run operations on Weaviate based on upstream events in your data ecosystem, such as when a new model is trained or a new dataset is available.
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

- The [Astro CLI](https://www.astronomer.io/docs/astro/cli/get-started).
- (Optional) An OpenAI API key of at least [tier 1](https://platform.openai.com/docs/guides/rate-limits/usage-tiers) if you want to use OpenAI for vectorization. The tutorial can be completed using local vectorization with `text2vec-transformers` if you don't have an OpenAI API key.

This tutorial uses a local Weaviate instance created as a Docker container. You do not need to install the Weaviate client locally.

:::info

The example code from this tutorial is also available on [GitHub](https://github.com/astronomer/airflow-weaviate-tutorial). 

:::

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-weaviate-tutorial && cd astro-weaviate-tutorial
    $ astro dev init
    ```

2. Add the following two packages to your `requirements.txt` file to install the [Weaviate Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-weaviate/stable/index.html) and the [Weaviate Python client](https://weaviate.io/developers/weaviate/client-libraries/python) in your Astro project:

    ```text
    apache-airflow-providers-weaviate==1.0.0
    weaviate-client==3.25.3 
    ```

3. This tutorial uses a local Weaviate instance and a [text2vec-transformer model](https://hub.docker.com/r/semitechnologies/transformers-inference/), with each running in a Docker container. To add additional containers to your Astro project, create a new file in your project's root directory called `docker-compose.override.yml` and add the following:

    ```yaml
    version: '3.1'
    services:           
      weaviate:
        image: cr.weaviate.io/semitechnologies/weaviate:latest
        command: "--host 0.0.0.0 --port '8081' --scheme http"
        ports:
          - 8081:8081
        environment:
          QUERY_DEFAULTS_LIMIT: 25
          PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
          DEFAULT_VECTORIZER_MODULE: 'text2vec-transformers'
          ENABLE_MODULES: 'text2vec-transformers, text2vec-openai'
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

4. To create an [Airflow connection](connections.md) to the local Weaviate instance, add the following environment variable to your `.env` file. You only need to provide an `X-OpenAI-Api-Key` if you plan on using the OpenAI API for vectorization.

    ```text
    AIRFLOW_CONN_WEAVIATE_DEFAULT='{
        "conn_type": "weaviate",
        "host": "http://weaviate:8081/",
        "extra": {
            "token": "adminkey",
            "additional_headers": {
                "X-OpenAI-Api-Key": "YOUR OPEN API KEY" # optional
            }
        }
    }'
    ```

:::tip

See the Weaviate documentation on [environment variables](https://weaviate.io/developers/weaviate/config-refs/env-vars), [modules](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules), and [client instantiation](https://weaviate.io/developers/weaviate/client-libraries/python#instantiate-a-client) for more information on configuring a Weaviate instance and connection.

:::

## Step 2: Add your data

The DAG in this tutorial runs a query on vectorized movie descriptions from [IMDB](https://www.imdb.com/). If you run the project locally, Astronomer recommends testing the pipeline with a small subset of the data. If you use a remote vectorizer like `text2vec-openai`, you can use larger parts of the [full dataset](https://github.com/astronomer/learn-tutorials-data/blob/main/movie_descriptions.txt).

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

## Step 3: Create your DAG

1. In your `dags` folder, create a file called `query_movie_vectors.py`.

2. Copy the following code into the file. If you want to use `text2vec-openai` for vectorization, change the `VECTORIZER` variable to `text2vec-openai` and make sure you provide an OpenAI API key in the `AIRFLOW_CONN_WEAVIATE_DEFAULT` in your `.env` file. 

    <CodeBlock language="python">{query_movie_vectors}</CodeBlock>

    This DAG consists of five tasks to make a simple ML orchestration pipeline.

    - The `check_for_class` task uses the [WeaviateHook](https://airflow.apache.org/docs/apache-airflow-providers-weaviate/stable/_api/airflow/providers/weaviate/hooks/weaviate/index.html) to check if a class of the name `CLASS_NAME` already exists in your Weaviate instance. The task is defined using the [`@task.branch` decorator](airflow-branch-operator.md#taskbranch-branchpythonoperator) and returns the the id of the task to run next based on whether the class of interest exists. If the class exists, the DAG runs the empty `class_exists` task. If the class does not exist, the DAG runs the `create_class` task.
    - The `create_class` task uses the WeaviateHook to create a class with the `CLASS_NAME` and specified `VECTORIZER` in your Weaviate instance.
    - The `import_data` task is defined using the [WeaviateIngestOperator](https://airflow.apache.org/docs/apache-airflow-providers-weaviate/stable/operators/weaviate.html) and ingests the data into Weaviate. You can run any Python code on the data before ingesting it into Weaviate by providing a callable to the `input_json` parameter. This makes it possible to create your own embeddings or complete other transformations before ingesting the data. In this example we use automatic schema inference and vector creation by Weaviate.
    - The `query_embeddings` task uses the WeaviateHook to connect to the Weaviate instance and run a query. The query returns the most similar movie to the concepts provided by the user when running the DAG in the next step.

## Step 4: Run your DAG

1. Run `astro dev start` in your Astro project to start Airflow and open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `query_movie_vectors` DAG by clicking the play button. Then, provide [Airflow params](airflow-params.md) for `movie_concepts`.

    Note that if you are running the project locally on a larger dataset, the `import_data` task might take a longer time to complete because Weaviate generates the vector embeddings in this task.

    ![Screenshot of the Airflow UI showing the successful completion of the `query_movie_vectors` DAG in the Grid view with the Graph tab selected. Since this was the first run of the DAG, the schema had to be newly created. The schema creation was enabled when the branching task `branch_create_schema` selected the downstream `create_schema` task to run.](/img/tutorials/airflow-weaviate_successful_dag.png)


3. View your movie suggestion in the task logs of the `query_embeddings` task:

    ```text
    [2023-11-13, 13:29:56 UTC] {logging_mixin.py:154} INFO - Your movie query was for the following concepts: innovation friends
    [2023-11-13, 13:29:56 UTC] {logging_mixin.py:154} INFO - You should watch the following movie(s): Primer (2004)
    [2023-11-13, 13:29:56 UTC] {logging_mixin.py:154} INFO - Description: Four friends/fledgling entrepreneurs, knowing that there's something bigger and more innovative than the different error-checking devices they've built, wrestle over their new invention.
    ```

## Conclusion

Congratulations! You used Airflow and Weaviate to get your next movie suggestion!