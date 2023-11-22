---
title: "Orchestrate Pinecone operations with Apache Airflow"
sidebar_label: "Pinecone"
description: "Learn how to integrate Pinecone and Airflow."
id: airflow-pinecone
sidebar_custom_props: { icon: 'img/integrations/pinecone.png' }
---

import CodeBlock from '@theme/CodeBlock';
import query_series_vectors from '!!raw-loader!../code-samples/dags/airflow-pinecone/query_series_vectors.py';

[Pinecone](https://www.pinecone.io/) is a proprietary vector database platform designed for handling large-scale vector based AI applications. The [Pinecone Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-pinecone/stable/index.html) offers modules to easily integrate Pinecone with Airflow.

In this tutorial you'll use Airflow to create vectors embeddings of series descriptions, create an index in your Pinecone project, ingest the vector embeddings into that index, and query Pinecone to get a suggestion for your next binge-watchable series based on your current mood.

## Why use Airflow with Pinecone?

Integrating Pinecone with Airflow provides a robust solution for managing large-scale vector search workflows in your AI applications. Pinecone specializes in efficient vector storage and similarity search, which is essential for leveraging advanced models like language transformers or deep neural networks.

By combining Pinecone with Airflow, you can:

- Use Airflow's [data-driven scheduling](airflow-datasets.md) to run operations in Pinecone based on upstream events in your data ecosystem, such as when a new model is trained or a new dataset is available.
- Run dynamic queries with [dynamic task mapping](dynamic-tasks.md), for example to parallelize vector ingestion or search operations to improve performance.
- Add Airflow features like [retries](rerunning-dags.md#automatically-retry-tasks) and [alerts](error-notifications-in-airflow.md) to your Pinecone operations. Retries protect your MLOps pipelines from transient failures, and alerts notify you of events like task failures or missed service level agreements (SLAs).

## Time to complete 

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of Pinecone. See [Pinecone Introduction](https://docs.pinecone.io/docs/overview).
- The basics of vector embeddings. See [Vector Embeddings for Developers: The Basics](https://www.pinecone.io/learn/vector-embeddings-for-developers/).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow decorators. See [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow hooks. See [Hooks 101](what-is-a-hook.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- A [Pinecone account](https://app.pinecone.io/?sessionType=signup) with an [API key](https://docs.pinecone.io/docs/authentication). You can use a free tier account for this tutorial.
- An OpenAI API key of at least [tier 1](https://platform.openai.com/docs/guides/rate-limits/usage-tiers) if you want to use OpenAI for vectorization. If you do not want to use OpenAI you can adapt the `create_embeddings` function at the start of the DAG to use a different vectorizer. Note that you will likely need to adjust the `EMBEDDING_MODEL_DIMENSIONS` parameter in the DAG if you use a different vectorizer.

:::info

The example code from this tutorial is also available on [GitHub](https://github.com/astronomer/airflow-pinecone-tutorial). 

:::

## Step 1: Configure your Astro project 

1. Create a new Astro project:

    ```sh
    $ mkdir astro-pinecone-tutorial && cd astro-pinecone-tutorial
    $ astro dev init
    ```

2. Add the following two lines to your `requirements.txt` file to install the [Pinecone Airflow Provider](https://airflow.apache.org/docs/apache-airflow-providers-pinecone/stable/index.html) and [OpenAI Python client](https://platform.openai.com/docs/libraries) in your Astro project:

    ```text
    apache-airflow-providers-pinecone==1.0.0
    openai==1.3.2
    ```

3. Add the following environment variables to your Astro project `.env` file. These variables store the configuration for an [Airflow connection](connections.md) to your Pinecone account and allow you to use the OpenAI API. Provide your own values for `<your-pinecone-environment>`, `<your-pinecone-api-key>` and `<your-openai-api-key>`:

    ```text
    AIRFLOW_CONN_PINECONE_DEFAULT='{
        "conn_type": "pinecone",
        "login": "<your-pinecone-environment>",  # for example `gcp-starter`
        "password": "<your-pinecone-api-key>"
    }'
    OPENAI_API_KEY="<your-openai-api-key>"
    ```

## Step 2: Add your data

The DAG in this tutorial runs a query on vectorized series descriptions, which were mostly retrieved from [IMDB](https://www.imdb.com/) with added domain expert inputs. 

1. In your Astro project `include` directory, create a file called `series_data.txt`. 
2. Copy and paste the following text into the file:

    ```text
    1 ::: Star Trek: Discovery (2017) ::: sci-fi ::: Ten years before Kirk, Spock, and the Enterprise, the USS Discovery discovers new worlds and lifeforms using a new innovative mushroom based propulsion system. 
    2 ::: Feel Good (2020) ::: romance ::: The series follows recovering addict and comedian Mae, who is trying to control the addictive behaviors and intense romanticism that permeate every facet of their life.
    3 ::: For All Mankind (2019) ::: sci-fi ::: The series dramatizes an alternate history depicting "what would have happened if the global space race had never ended" after the Soviet Union succeeds in the first crewed Moon landing ahead of the United States.
    4 ::: The Legend of Korra (2012) ::: anime ::: Avatar Korra fights to keep Republic City safe from the evil forces of both the physical and spiritual worlds.
    5 ::: Mindhunter (2017) ::: crime ::: In the late 1970s, two FBI agents broaden the realm of criminal science by investigating the psychology behind murder and end up getting too close to real-life monsters.
    6 ::: The Umbrella Academy (2019) ::: adventure ::: A family of former child heroes, now grown apart, must reunite to continue to protect the world.
    7 ::: Star Trek: Picard (2020) ::: sci-fi ::: Follow-up series to Star Trek: The Next Generation (1987) and Star Trek: Nemesis (2002) that centers on Jean-Luc Picard in the next chapter of his life.
    8 ::: Invasion (2021) ::: sci-fi ::: Earth is visited by an alien species that threatens humanity's existence. Events unfold in real time through the eyes of five ordinary people across the globe as they struggle to make sense of the chaos unraveling around them.
    ```

## Step 3: Create your DAG

1. In your Astro project `dags` folder, create a file called `query_series_vectors.py`.

2. Copy the following code into the file:

    <CodeBlock language="python">{query_series_vectors}</CodeBlock>

    This DAG consists of six tasks to make a simple ML orchestration pipeline.

    - The `import_data_func` task defined with the [`@task` decorator](airflow-decorators.md) reads the data from the `series_data.txt` file and returns a list of dictionaries containing the series title, year, genre, and description. Note that the task will create a UUID for each series using the `create_uuid` function and add it to the `id` key. Having a unique ID for each series is required for the Pinecone ingestion task.
    - The `vectorize_series_data` task is a [dynamic task](dynamic-tasks.md) that creates one mapped task instance for each series in the list returned by the `import_data_func` task. The task uses the `create_embeddings` function to generate vector embeddings for each series' description. Note that if you want to use a different vectorizer than OpenAI's `text-embedding-ada-002` you can adjust this function to return your preferred vectors and the `EMBEDDING_MODEL_DIMENSIONS` parameter in the DAG to the vector size of your model.
    - The `vectorize_user_mood` task calls the `create_embeddings` function to generate vector embeddings for the mood the user can provide as an [Airflow param](airflow-params.md).
    - The `create_index_if_not_exists` task uses the [PineconeHook](https://registry.astronomer.io/providers/apache-airflow-providers-pinecone/versions/latest/modules/PineconeHook) to connect to your Pinecone instance and retrieve the current list of indexes in your Pinecone environment. No index of the name `PINECONE_INDEX_NAME` exists yet, the task will create it. Note that with a free tier Pinecone account you can have one index.
    - The `pinecone_vector_ingest` task uses the [PineconeIngestOperator](https://registry.astronomer.io/providers/apache-airflow-providers-pinecone/versions/latest/modules/PineconeIngestOperator) to ingest the vectorized series data into the index created by the `create_index_if_not_exists` task.
    - The `query_pinecone` task performs a vector search in Pinecone to get the series most closely matching the user-provided mood and prints the result to the task logs.

    ![A screenshot from the Airflow UI's Grid view with the Graph tab selected showing a successful run of the query_series_vectors DAG.](/img/tutorials/airflow-pinecone_query_series_vectors_dag.png)

## Step 4: Run your DAG

1. Open your Astro project, then run `astro dev start` to run Airflow locally.

2. Open the Airflow UI at `localhost:8080`, then run the `query_series_vectors` DAG by clicking the play button. Provide your input to the [Airflow param](airflow-params.md) for `series_mood`.

    ![A screenshot of the Trigger DAG view in the Airflow UI showing the mood `A series about Astronauts` being provided to the `series_mood` param.](/img/tutorials/airflow-pinecone_params.png)

3. View your series suggestion in the task logs of the `query_pinecone` task:

    ```text
    [2023-11-20, 14:03:48 UTC] {logging_mixin.py:154} INFO - You should watch: For All Mankind
    [2023-11-20, 14:03:48 UTC] {logging_mixin.py:154} INFO - Description: The series dramatizes an alternate history depicting "what would have happened if the global space race had never ended" after the Soviet Union succeeds in the first crewed Moon landing ahead of the United States.
    ```

:::tip

When watching `For All Mankind`, make sure to have a tab with [Wikipedia](https://en.wikipedia.org) open to compare the alternate timeline with ours. And don't forget to hydrate and move around every once in a while!

:::

## Conclusion

Congrats! You've now successfully integrated Airflow and Pinecone! You can now use this tutorial as a starting point to build you own AI applications with Airflow and Pinecone.