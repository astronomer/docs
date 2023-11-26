---
title: "Orchestrate OpenSearch operations with Apache Airflow"
sidebar_label: "OpenSearch"
description: "Learn how to integrate OpenSearch and Airflow."
id: airflow-opensearch
sidebar_custom_props: { icon: 'img/integrations/opensearch.png' }
---

import CodeBlock from '@theme/CodeBlock';
import search_hamilton from '!!raw-loader!../code-samples/dags/airflow-opensearch/search_hamilton.py';

[OpenSearch](https://opensearch.org/) is an open source distributed search and analytics engine based on [Apache Lucene](https://lucene.apache.org/). It offers advanced search capabilities on large bodies of text alongside powerful machine learning plugins. The [OpenSearch Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-opensearch/stable/index.html) offers modules to easily integrate OpenSearch with Airflow.

In this tutorial you'll use Airflow to create an index in OpenSearch, ingest the lyrics of the musical Hamilton into the index, and run a search query on the index to see which character most often sings a specific word.

## Why use Airflow with OpenSearch?

OpenSearch allows you to perform complex search queries on indexed text documents. Additionally, the tool comes with a variety of plugins for use cases such as security analytics, semantic search, and neural search. 

Integrating OpenSearch with Airflow allows you to:

- Use Airflow's [data-driven scheduling](airflow-datasets.md) to run operations involving documents stored in OpenSearch based on upstream events in your data ecosystem, such as when a new model is trained or a new dataset is available.
- Run dynamic queries based on upstream events in your data ecosystem or user input via [Airflow params](airflow-params.md) on documents and vectors OpenSearch to retrieve relevant objects.
- Add Airflow features like [retries](rerunning-dags.md#automatically-retry-tasks) and [alerts](error-notifications-in-airflow.md) to your OpenSearch operations.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of OpenSearch. See the [OpenSearch documentation](https://opensearch.org/docs/latest/about/).
- Vector embeddings. See [Using OpenSearch as a Vector Database](https://opensearch.org/platform/search/vector-database.html).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow decorators. [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

This tutorial uses an OpenSearch instance created as a [Docker container](https://hub.docker.com/r/opensearchproject/opensearch). You do not need to install OpenSearch on your machine.

:::info

The example code from this tutorial is also available on [GitHub](https://github.com/astronomer/airflow-opensearch-tutorial). 

:::

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-opensearch-tutorial && cd astro-opensearch-tutorial
    $ astro dev init
    ```

2. Add the following two lines to your Astro project `requirements.txt` file to install the [OpenSearch Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-opensearch/stable/index.html) and pin the [pandas](https://pandas.pydata.org/) version in your Astro project:

    ```text
    apache-airflow-providers-opensearch==1.0.0
    pandas==1.5.3
    ```

3. This tutorial uses a local OpenSearch instance running in a Docker container. To run an OpenSearch container as part of your Airflow environment, create a new file in your Astro project root directory called `docker-compose.override.yml` and copy and paste the following into it:

    ```yaml
    version: '3.1'
    services:
      opensearch:
        image: opensearchproject/opensearch:2
        ports:
          - "9200:9200"  # OpenSearch REST API
          - "9300:9300"  # OpenSearch Node-to-Node communication
        environment:
          - discovery.type=single-node
          - plugins.security.ssl.http.enabled=false
        volumes:
          - opensearch-data:/usr/share/opensearch/data
        networks:
          - airflow
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

    # volume for OpenSearch
    volumes:
      opensearch-data:
    ```


4. Add the following configuration to your `.env` file to create an [Airflow connection](connections.md) between Astro and your OpenSearch instance. If you already have a cloud-based OpenSearch instance, you can connect to that instead of the local instance by adjusting the values in the connection.

    ```text
    AIRFLOW_CONN_OPENSEARCH_DEFAULT='{
        "conn_type": "opensearch",
        "host": "opensearch",
        "port": 9200,
        "login": "admin",
        "password": "admin"
    }'
    ```

## Step 2: Add your data

The DAG in this tutorial uses a  [Kaggle](https://www.kaggle.com/datasets/lbalter/hamilton-lyrics) dataset that contains the lyrics of the musical [Hamilton](https://hamiltonmusical.com/new-york/). 

1. Download the [hamilton_lyrics.csv](https://github.com/astronomer/airflow-opensearch-tutorial/blob/main/include/hamilton_lyrics.csv) from Astronomer's GitHub.

2. Save the file in your Astro project `include` folder.

## Step 3: Create your DAG

1. In your `dags` folder, create a file called `search_hamilton.py`.

2. Copy the following code into the file.

    <CodeBlock language="python">{search_hamilton}</CodeBlock>

    This DAG consists of seven tasks to make a simple ML orchestration pipeline.

    - The `check_if_index_exists` task uses a [`@task.branch`](airflow-branch-operator.md#taskbranch-branchpythonoperator) decorator to check if the index `OPENSEARCH_INDEX_NAME` exists in your OpenSearch instance. If it does not exist, the task returns the string `create_index` causing the downstream `create_index` task to run. If the index exists, the task causes the empty `index_exists` task to run instead.
    - The `create_index` task defined with the [OpenSearchCreateIndexOperator](https://registry.astronomer.io/providers/apache-airflow-providers-opensearch/versions/latest/modules/OpenSearchCreateIndexOperator) creates the index `OPENSEARCH_INDEX_NAME` in your OpenSearch instance with the three properties `title`, `speaker` and `lines`.
    - The `csv_to_dict_list` task uses the [`@task`](airflow-decorators.md) decorator to ingest the lyrics of the musical Hamilton from the `hamilton_lyrics.csv` file into a list of Python dictionaries. Each dictionary represents a line of the musical and will be one document in the OpenSearch index.
    - The `add_lines_as_documents` task is a [dynamically mapped task](dynamic-tasks.md) using the [OpenSearchAddDocumentOperator](https://registry.astronomer.io/providers/apache-airflow-providers-opensearch/versions/latest/modules/OpenSearchAddDocumentOperator) to create one mapped task instance for each document to ingest.
    - The `search_for_keyword` is defined with the [OpenSearchQueryOperator](https://registry.astronomer.io/providers/apache-airflow-providers-opensearch/versions/latest/modules/OpenSearchQueryOperator) and performs a [fuzzy query](https://opensearch.org/docs/latest/query-dsl/term/fuzzy/) on the OpenSearch index to find the character and song that mention the `KEYWORD_TO_SEARCH` the most.
    - The `print_query_result` prints the query results to the task logs.

    ![Screenshot of the Airflow UI showing the successful completion of the `search_hamilton` DAG in the Grid view with the Graph tab selected.](/img/tutorials/airflow-opensearch_dag.png)

:::tip

For information on more advanced search techniques in OpenSearch, see the [OpenSearch documentation](https://opensearch.org/docs/latest/).

:::

## Step 4: Run your DAG

1. Run `astro dev start` in your Astro project to start Airflow and open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `search_hamilton` DAG by clicking the play button. By default the DAG will search the lyrics for the word `write`, but you can change the search term by updating the `KEYWORD_TO_SEARCH` variable in your DAG file.

3. View your song results in the task logs of the `print_query_result` task:

    ```text
    [2023-11-22, 14:01:58 UTC] {logging_mixin.py:154} INFO - 
     Top 3 Hamilton characters that mention 'write' the most:
      Character  Number of lines that include 'write'
      HAMILTON                                    15
         ELIZA                                     8
          BURR                                     4
    [2023-11-22, 14:01:58 UTC] {logging_mixin.py:154} INFO - 
     Top 3 Hamilton songs that mention 'write' the most:
         Song  Number of lines that include 'write'
      Non-Stop                                    11
     Hurricane                                    10
          Burn                                     3
    ```

4. (Optional) Listen to the [song](https://open.spotify.com/track/7qfoq1JFKBUEIvhqOHzuqX?si=49a2e7c259ad43e2) that mentions your keyword the most.

## Conclusion

Congratulations! You used Airflow and OpenSearch to analyze the lyrics of Hamilton! You can now use Airflow to orchestrate OpenSearch operations in your own machine learning pipelines. History has its eyes on you.