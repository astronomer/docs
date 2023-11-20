---
title: "Orchestrate pgvector operations with Apache Airflow"
sidebar_label: "pgvector"
description: "Learn how to integrate pgvector and Airflow."
id: airflow-pgvector
sidebar_custom_props: { icon: 'img/integrations/postgres.png' }
---

import CodeBlock from '@theme/CodeBlock';
import query_book_vectors from '!!raw-loader!../code-samples/dags/airflow-pgvector/query_book_vectors.py';

[Pgvector](https://github.com/pgvector/pgvector) is an open source extension for PostgreSQL databases that adds the possibility to store and query high-dimensional object embeddings. The [Pgvector Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-pgvector/stable/index.html) offers modules to easily integrate Pgvector with Airflow.

In this tutorial you'll use Airflow to orchestrate the embedding of book descriptions with the OpenAI API, ingest the embeddings into a PostgreSQL database with pgvector installed, and query the database for books that match a user-provided mood.

## Why use Airflow with pgvector?

Pgvector allows you to store objects alongside their vector embeddings and to query these objects based on their similarity. Vector embeddings are key components of many modern machine learning models such as [LLMs](https://en.wikipedia.org/wiki/Large_language_model) or [ResNet](https://arxiv.org/abs/1512.03385).

Integrating PostgreSQL with pgvector and Airflow into one end-to-end machine learning pipeline allows you to:

- Use Airflow's [data-driven scheduling](airflow-datasets.md) to run operations involving vectors stored in PostgreSQL based on upstream events in your data ecosystem, such as when a new model is trained or a new dataset is available.
- Run dynamic queries based on upstream events in your data ecosystem or user input via [Airflow params](airflow-params.md) on vectors stored in PostgreSQL to retrieve similar objects.
- Add Airflow features like [retries](rerunning-dags.md#automatically-retry-tasks) and [alerts](error-notifications-in-airflow.md) to your pgvector operations.
- Check your vector database for existence of a unique key before running potentially costly embedding operations on your data.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of pgvector. See the [README of the pgvector repository](https://github.com/pgvector/pgvector/blob/master/README.md).
- Basic SQL. See [SQL Tutorial](https://www.w3schools.com/sql/sql_intro.asp).
- Vector embeddings. See [Vector Embeddings](https://tembo.io/blog/pgvector-and-embedding-solutions-with-postgres/).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow decorators. [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- An OpenAI API key of at least [tier 1](https://platform.openai.com/docs/guides/rate-limits/usage-tiers) if you want to use OpenAI for vectorization. If you do not want to use OpenAI you can adapt the `create_embeddings` function at the start of the DAG to use a different vectorizer. Note that you will likely need to adjust the `MODEL_VECTOR_LENGTH` parameter in the DAG if you use a different vectorizer.

This tutorial uses a local PostgreSQL database created as a Docker container. [The image](https://hub.docker.com/r/ankane/pgvector) comes with pgvector preinstalled.

:::info

The example code from this tutorial is also available on [GitHub](https://github.com/astronomer/airflow-pgvector-tutorial). 

:::

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-pgvector-tutorial && cd astro-pgvector-tutorial
    $ astro dev init
    ```

2. Add the following two packages to your `requirements.txt` file to install the [pgvector Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-pgvector/stable/index.html) and the [OpenAI Python client](https://platform.openai.com/docs/libraries) in your Astro project:

    ```text
    apache-airflow-providers-pgvector==1.0.0
    openai==1.3.2
    ```

3. This tutorial uses a local PostgreSQL database running in a Docker container. To add a second PostgreSQL container to your Astro project, create a new file in your project's root directory called `docker-compose.override.yml` and add the following. The `ankane/pgvector` image builds a PostgreSQL database with pgvector preinstalled.

    ```yaml
    version: '3.1'
    services:
      postgres_pgvector:
        image: ankane/pgvector
        volumes:
          - ${PWD}/include/postgres:/var/lib/postgresql/data
          - ${PWD}/include:/include
        networks:
          - airflow
        ports:
          - 5433:5432
        environment:
          - POSTGRES_USER=postgres
          - POSTGRES_PASSWORD=postgres
    # Airflow containers
      scheduler:
        networks:
          - airflow
      webserver:
        networks:
          - airflow
      triggerer:
        networks:
          - airflow
      postgres:
        networks:
          - airflow
    ```


4. To create an [Airflow connection](connections.md) to the PostgreSQL database, add the following environment variable to your `.env` file. If you are using the OpenAI API for embeddings you also need to add your OpenAI API key to `OPENAI_API_KEY`.

    ```text
    AIRFLOW_CONN_POSTGRES_DEFAULT='{
        "conn_type": "postgres",
        "login": "postgres",
        "password": "postgres",
        "host": "host.docker.internal",
        "port": 5433,
        "schema": "postgres"
    }'
    OPENAI_API_KEY="<your-openai-api-key>"
    ```

## Step 2: Add your data

The DAG in this tutorial runs a query on vectorized book descriptions from [Goodreads](https://www.goodreads.com/), but you can adjust the DAG to use any data you want. 

1. Create a new file called `book_data.txt` in the `include` directory. 

2. Copy the book description from the [book_data.txt](https://github.com/astronomer/airflow-pgvector-tutorial/blob/main/include/book_data.txt) file in Astronomer's GitHub for a list of great books.

:::tip

If you want to add your own books make sure the data is in the following format:

```text
<index integer> ::: <title> (<year of publication>) ::: <author> ::: <description>
```

One book corresponds to one line in the file.

:::

## Step 3: Create your DAG

1. In your `dags` folder, create a file called `query_book_vectors.py`.

2. Copy the following code into the file. If you want to use a vectorizer other than OpenAI make sure to adjust both the `create_embeddings` function at the start of the DAG and provide the correct `MODEL_VECTOR_LENGTH`. 

    <CodeBlock language="python">{query_book_vectors}</CodeBlock>

    This DAG consists of nine tasks to make a simple ML orchestration pipeline.

    - The `enable_vector_extension_if_not_exists` task uses a [PostgresOperator](https://registry.astronomer.io/providers/apache-airflow-providers-postgres/versions/latest/modules/PostgresOperator) to enable the pgvector extension in the PostgreSQL database.
    - The `create_table_if_not_exists` task creates the `Book` table in PostgreSQL. Note the `VECTOR()` datatype used for the `vector` column. This datatype is added to PostgreSQL by the pgvector extension and needs to be defined with the vector length of the vectorizer you use as an argument. In this example we use the OpenAI's `text-embedding-ada-002` to create 1536-dimensional vectors, so we define the columns with the type `VECTOR(1536)` using parameterized SQL.
    - The `get_already_imported_book_ids` task queries the `Book` table to return all `book_id` values of books that were already stored with their vectors in previous DAG runs. 
    - The `import_book_data` task uses the [`@task` decorator](airflow-decorators.md) to read the book data from the `book_data.txt` file and return it as a list of dictionaries with keys corresponding to the columns of the `Book` table.

    - The `create_embeddings_book_data` task is [dynamically mapped](dynamic-tasks.md) over the list of dictionaries returned by the `import_book_data` task to parallelize vector embedding of all book descriptions that have not been added to the `Book` table in previous DAG runs. The `create_embeddings` function defines how the embeddings are computed and can be modified to use other embedding models. If all books in the list have already been added to the `Book` table all mapped task instances are skipped.
    - The `create_embeddings_query` task applies the same `create_embeddings` function to the desired book mood the user provided via [Airflow params](airflow-params.md). 
    - The `import_embeddings_to_pgvector` task uses the [PgVectorIngestOperator](https://registry.astronomer.io/providers/apache-airflow-providers-pgvector/versions/latest/modules/PgVectorIngestOperator) to insert the book data including the embedding vectors into the PostgreSQL database. This task is dynamically mapped to import the embeddings from one book at a time. The dynamically mapped task instances of books that have already been imported in previous DAG runs are skipped.

    - The `get_a_book_suggestion` task queries the PostgreSQL database for the book that is most similar to the user-provided mood using nearest neighbor search. Note how the vector of the user-provided book mood (`query_vector`) is cast to the `VECTOR` datatype before similarity search: `ORDER BY vector <-> CAST(%(query_vector)s AS VECTOR)`.  
    - The `print_book_suggestion` task prints the book suggestion to the task logs.

    ![Screenshot of the Airflow UI showing the successful completion of the `query_book_vectors` DAG in the Grid view with the Graph tab selected.](/img/tutorials/airflow-pgvector_successful_dag.png)

:::tip

For information on more advanced search techniques in pgvector, see the [pgvector README](https://github.com/pgvector/pgvector/blob/master/README.md).

:::

## Step 4: Run your DAG

1. Run `astro dev start` in your Astro project to start Airflow and open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `query_book_vectors` DAG by clicking the play button. Then, provide [Airflow params](airflow-params.md) for `book_mood`.

    ![Screenshot of the Airflow UI showing the input form for the book_mood param.](/img/tutorials/airflow-pgvector_params.png)

3. View your book suggestion in the task logs of the `print_book_suggestion` task:

    ```text
    [2023-11-20, 10:09:43 UTC] {logging_mixin.py:154} INFO - Book suggestion for 'A philosophical book about consciousness.':
    [2023-11-20, 10:09:43 UTC] {logging_mixin.py:154} INFO - You should read The Idea of the World by Bernardo Kastrup, published in 2019!
    [2023-11-20, 10:09:43 UTC] {logging_mixin.py:154} INFO - Goodreads describes the book as: A rigorous case for the primacy of mind in nature, from philosophy to neuroscience, psychology and physics. [...]
    ```

## Step 5: (Optional) Fetch and read the book

1. Go to the website of your local library and search for the book. If it is available, order it and wait for it to arrive. You will likely need a library card to check out the book.
2. Make sure to prepare an adequate amount of tea for your reading session. Astronomer recommends [Earl Grey](https://en.wikipedia.org/wiki/Earl_Grey_tea), but you can use any tea you like.
3. Enjoy your book!

## Conclusion

Congratulations! You used Airflow and pgvector to get get a book suggestion! You can now use Airflow to orchestrate pgvector operations in your own machine learning pipelines. Additionally you remembered the satisfaction and joy of spending hours reading a good book and supported your local library.