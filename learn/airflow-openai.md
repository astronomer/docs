---
title: "Orchestrate OpenAI operations with Apache Airflow"
sidebar_label: "OpenAI"
description: "Learn how to integrate OpenAI and Airflow."
id: airflow-openai
sidebar_custom_props: { icon: 'img/integrations/openai.png' }
---

import CodeBlock from '@theme/CodeBlock';
import captains_dag from '!!raw-loader!../code-samples/dags/airflow-openai/captains_dag.py';

[OpenAI](https://openai.com/) is an AI research and deployment company that provides an API for accessing state of the art models like [GPT-4](https://openai.com/gpt-4) and [DALL·E 3](https://openai.com/dall-e-3). The [OpenAI Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-openai/stable/index.html) offers modules to easily integrate OpenAI with Airflow.

In this tutorial you'll use Airflow and the OpenAI Airflow provider to generate answers to any question you want to ask Star Trek captains, create embeddings of the answers, and plot them in two dimensions. 

## Why use Airflow with OpenAI?

OpenAI offers a variety of powerful model endpoints for different tasks like text generation, vector embedding, and translation tasks. These models are used in both user-facing applications, such as chatbots, and internal applications, such as a smart search for internal knowledge base content.

Integrating OpenAI with Airflow into an end-to-end machine learning pipeline allows you to:

- Use Airflow's [data-driven scheduling](airflow-datasets.md) to run operations using OpenAI model endpoints based on upstream events in your data ecosystem, such as when new user input is ingested or a new dataset is available.
- Send several requests to a model endpoint in parallel based on upstream events in your data ecosystem or user input via [Airflow params](airflow-params.md).
- Monitor the OpenAI service using Airflow [alerts](error-notifications-in-airflow.md) and protect against API rate limits and outages with [Airflow retries](rerunning-dags.md#automatically-retry-tasks).
- Use Airflow to orchestrate the creation of vector embeddings using OpenAI models, which is especially useful for large datasets that can't be processed automatically by vector databases.

## Time to complete

This tutorial takes approximately 15 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of the OpenAI API. See [OpenAI Introduction](https://platform.openai.com/docs/introduction).
- The basics of vector embeddings. See the [OpenAI Embeddings guide](https://platform.openai.com/docs/guides/embeddings).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow hooks. See [Hooks 101](what-is-a-hook.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- An OpenAI API key with at least [tier 1 usage limits](https://platform.openai.com/docs/guides/rate-limits/usage-tiers).

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-openai-tutorial && cd astro-openai-tutorial
    $ astro dev init
    ```

2. Add the following lines to your `requirements.txt` file to install the OpenAI Airflow provider and other supporting packages:

    ```text
    apache-airflow-providers-openai==1.0.0
    openai==0.28.1
    matplotlib==3.8.1
    seaborn==0.13.0
    scikit-learn==1.3.2
    pandas==1.5.3
    numpy==1.26.2
    adjustText==0.8
    ```

3. To create an [Airflow connection](connections.md) to OpenAI, add the following environment variables to your `.env` file. Make sure to replace `<your-openai-api-key>` with your own OpenAI API key.

    ```text
    AIRFLOW_CONN_OPENAI_DEFAULT='{
        "conn_type": "openai",
        "password": "<your-openai-api-key>"
    }'
    ```

## Step 2: Create your DAG

1. In your `dags` folder, create a file called `captains_dag.py`.

2. Copy the following code into the file.

    <CodeBlock language="python">{captains_dag}</CodeBlock>

    This DAG consists of four tasks to make a simple MLOps pipeline.

    - The `get_captains_list` task fetches the list of Star Trek captains you want to ask your question to. You'll provide the list of captains when you run the DAG with [Airflow params](airflow-params.md).
    - The `ask_a_captain` task uses the [OpenAIHook](https://airflow.apache.org/docs/apache-airflow-providers-openai/stable/_api/airflow/providers/openai/hooks/openai/index.html) to connect to the OpenAI API. It then uses the [chat completion endpoint](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) to generate answers to the question you provide. This task is [dynamically mapped](dynamic-tasks.md) over the list of captains to generate one dynamically mapped task instance per captain.
    - The `get_embeddings` task is defined using the [OpenAIEmbeddingOperator](https://airflow.apache.org/docs/apache-airflow-providers-openai/stable/operators/openai.html) to generate vector embeddings of the answers generated by the upstream `ask_a_captain` task. This task is dynamically mapped over the list of answers to retrieve one set of embeddings per answer. This pattern allows for efficient parallelization of the vector embedding generation.
    - The `plot_embeddings` task takes the embeddings created by the upstream task and performs dimensionality reduction using [PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) to plot the embeddings in two dimensions. 

    ![Screenshot of the Airflow UI showing the successful completion of the `captains_dag` DAG in the Grid view with the Graph tab selected. All 8 captains available were selected to be asked the question, which led to 8 mapped task instances of both the `ask_a_captain` and `get_embeddings` task.](/img/tutorials/airflow-openai_dag_completed.png)

## Step 3: Run your DAG

1. Run `astro dev start` in your Astro project to start Airflow, then open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `captains_dag` DAG by clicking the play button. Then, provide [Airflow params](airflow-params.md) for:

    - `Question to ask the captain`: The question you want to ask the captains.
    - `captains_to_ask`: A list of Star Trek captains you want to ask the question to. Make sure to create one line per captain and to provide at least two names.
    - `max_tokens_answer`: The maximum number of tokens available for the answer. 
    - `randomness_of_answer`: The randomness of the answer. The value provided is divided by 10 and given to the `temperature` parameter of the [chat completion endpoint](https://platform.openai.com/docs/guides/text-generation/reproducible-outputs). The scale for the param ranges from 0 to 20, with 0 being the most deterministic and 20 being the most random.

    ![Screenshot of the Airflow UI showing the params available for the `captains_dag` DAG with the default choices.](/img/tutorials/airflow-openai_params.png)

3. After the DAG run completed, go to the `include` folder to view the image file created by the `plot_embeddings` task. The image should look similar to the one below.

    ![Screenshot of the image created by the `plot_embeddings` task showing the two dimensional representation of the closeness of answers associated with different Star Trek captains.](/img/tutorials/airflow-openai_plot.png)

## Conclusion

Congratulations! You used Airflow and OpenAI to get answers from your favorite Star Trek captains and compare them visually. You can now use Airflow to orchestrate OpenAI operations in your own machine learning pipelines. 🖖

