---
title: "Orchestrate Cohere LLMs with Apache Airflow"
sidebar_label: "Cohere"
description: "Learn how to integrate Cohere and Airflow."
id: airflow-cohere
sidebar_custom_props: { icon: 'img/integrations/cohere.png' }
---

import CodeBlock from '@theme/CodeBlock';
import recipe_suggestions from '!!raw-loader!../code-samples/dags/airflow-cohere/recipe_suggestions.py';

[Cohere](https://cohere.com/) is a natural language processing (NLP) platform that provides an API to access cutting-edge large language models (LLMs). The [Cohere Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-cohere/stable/index.html) offers modules to easily integrate Cohere with Airflow.

In this tutorial, you use Airflow and the Cohere Airflow provider to generate recipe suggestions based on a list of ingredients and countries of recipe origin. Additionally, you create embeddings of the recipes and perform dimensionality reduction using principal component analysis (PCA) to plot recipe similarity in two dimensions.

## Why use Airflow with Cohere?

Cohere provides highly specialized out-of-the box and custom LLMs. Countless applications use these models for both user-facing needs, such as to moderate user-generated content, and internal purposes, like providing insight into customer support tickets.

Integrating Cohere with Airflow into one end-to-end machine learning pipeline allows you to:

- Use Airflow's [data-driven scheduling](airflow-datasets.md) to run operations with Cohere LLM endpoints based on upstream events in your data ecosystem, like when new user input is ingested or a new dataset is available.
- Send several requests to a model endpoint in parallel based on upstream events in your data ecosystem or user input with [Airflow params](airflow-params.md).
- Add Airflow features like [retries](rerunning-dags.md#automatically-retry-tasks) and [alerts](error-notifications-in-airflow.md) to your Cohere operations. This is critical for day 2 MLOps operations, for example, to handle model service outages.
- Use Airflow to orchestrate the creation of vector embeddings with Cohere models, which is especially useful for very large datasets that cannot be processed automatically by vector databases.

## Time to complete

This tutorial takes approximately 15 minutes to complete (cooking your recommended recipe not included).

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of the Cohere API. See [Cohere Documentation](https://docs.cohere.com/reference/about).
- The basics of vector embeddings. See the [Cohere Embeddings guide](https://docs.cohere.com/docs/embeddings).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow hooks. See [Hooks 101](what-is-a-hook.md).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- A Cohere API key. You can generate an API key in the [Cohere dashboard](https://dashboard.cohere.com/api-keys), accessible with a Cohere account. A free tier API key is sufficient for this tutorial.

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-cohere-tutorial && cd astro-cohere-tutorial
    $ astro dev init
    ```

2. Add the following lines to your `requirements.txt` file to install the Cohere Airflow provider and other supporting packages:

    ```text
    apache-airflow-providers-cohere==1.0.0
    matplotlib==3.8.1
    seaborn==0.13.0
    scikit-learn==1.3.2
    pandas==1.5.3
    numpy==1.26.2
    adjustText==0.8
    ```

3. To create an [Airflow connection](connections.md) to Cohere, add the following environment variables to your `.env` file. Make sure to provide `<your-cohere-api-key>`.

    ```text
    AIRFLOW_CONN_COHERE_DEFAULT='{
        "conn_type": "cohere",
        "password": "<your-cohere-api-key>"
    }'
    ```

## Step 2: Create your DAG

1. In your `dags` folder, create a file called `recipe_suggestions.py`.

2. Copy the following code into the file.

    <CodeBlock language="python">{recipe_suggestions}</CodeBlock>

    This DAG consists of five tasks to make a simple MLOps pipeline.

    - The `get_ingredients` task fetches the list of ingredients that the user found in their pantry and wants to use in their recipe. The input `pantry_ingredients` param is provided by [Airflow params](airflow-params.md) when you run the DAG.
    - The `get_countries` task uses [Airflow params](airflow-params.md) to retrieve the list of user-provided countries to get recipes from.
    - The `get_a_recipe` task uses the [CohereHook](https://airflow.apache.org/docs/apache-airflow-providers-cohere/stable/_api/airflow/providers/cohere/hooks/cohere/index.html) to connect to the Cohere API and use the [`/generate` endpoint](https://docs.cohere.com/reference/generate) to get a tasty recipe suggestion based on the user's pantry ingredients and one of the countries they provided. This task is [dynamically mapped](dynamic-tasks.md) over the list of countries to generate one task instance per country. The recipes are saved as `.txt` files in the `include` folder.
    - The `get_embeddings` task is defined using the [CohereEmbeddingOperator](https://airflow.apache.org/docs/apache-airflow-providers-cohere/stable/operators/embedding.html) to generate vector embeddings of the recipes generated by the upstream `get_a_recipe` task. This task is dynamically mapped over the list of recipes to retrieve one set of embeddings per recipe. This pattern allows for efficient parallelization of the vector embedding generation.
    - The `plot_embeddings` task takes the embeddings created by the upstream task and performs dimensionality reduction using [PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) to plot the embeddings in two dimensions. 

    ![Screenshot of the Airflow UI showing the successful completion of the `recipe_suggestions` DAG in the Grid view with the Graph tab selected. 6 countries were provided to get recipes suggestions from, which led to 8 mapped task instances of both the `get_a_recipe` and `get_embeddings` task.](/img/tutorials/airflow-cohere_dag_graph.png)

## Step 3: Run your DAG

1. Run `astro dev start` in your Astro project to start Airflow and open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `recipe_suggestions` DAG by clicking the play button. Then, provide [Airflow params](airflow-params.md) for:

    - `Countries of recipe origin`: A list of the countries you want to get recipe suggestions from. Make sure to create one line per country and to provide at least two countries.
    - `pantry_ingredients`: A list of the ingredients you have in your pantry and want to use in the recipe. Make sure to create one line per ingredient.
    - `type`: Select your preferred recipe type. 
    - `max_tokens_recipe`: The maximum number of tokens available for the recipe. 
    - `randomness_of_recipe`: The randomness of the recipe. The value provided is divided by 10 and given to the [`temperature` parameter](https://docs.cohere.com/docs/temperature) of the of the Cohere API. The scale for the param ranges from 0 to 50, with 0 being the most deterministic and 50 being the most random.

    ![Screenshot of the Airflow UI showing the params available for the `recipe_suggestions` DAG with the default choices.](/img/tutorials/airflow-cohere_params.png)

3. Go to the `include` folder to view the image file created by the `plot_embeddings` task. The image should look similar to the one below.

    ![Screenshot of the image created by the `plot_embeddings` task showing the two dimensional representation of the closeness of recipes associated with different countries.](/img/tutorials/airflow-cohere_recipe_plot.png)

## Step 4: (Optional) Cook your recipe

1. Choose one of the recipes in the `include` folder.
2. Navigate to your kitchen and cook the recipe you generated using Cohere with Airflow.
3. Enjoy!

## Conclusion

Congratulations! You used Airflow and Cohere to get recipe suggestions based on your pantry items. You can now use Airflow to orchestrate Cohere operations in your own machine learning pipelines.