---
title: "Orchestrate semantic querying in Qdrant with Apache Airflow®"
sidebar_label: "Qdrant"
description: "Learn how to integrate Qdrant and Apache Airflow®."
id: airflow-qdrant
sidebar_custom_props: { icon: 'img/integrations/qdrant-logo.png' }
---

import CodeBlock from '@theme/CodeBlock';
import recommend_books_dag from '!!raw-loader!../code-samples/dags/airflow-qdrant/recommend_books_dag.py';

[Qdrant](https://qdrant.tech/) is an open-source vector database and similarity search engine designed for AI applications.

In this tutorial, you'll use the [Qdrant Apache Airflow® provider](https://airflow.apache.org/docs/apache-airflow-providers-qdrant/stable/index.html) to write a DAG that generates embeddings in parallel and performs semantic retrieval based on user input.

Airflow provides useful operational and orchestration when running operations in Qdrant based on data events or building parallel tasks for generating vector embeddings. By using Airflow, you can set up monitoring and alerts for your pipelines for full observability.

## Time to complete

This tutorial takes approximately 30 minutes to complete.

## Prerequisites

- A running Qdrant instance. A [free instance](https://cloud.qdrant.io) is available.
- The Astro CLI. See [Install the Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli).
- A [HuggingFace token](https://huggingface.co/docs/hub/en/security-tokens) to generate embeddings.

## Step 1: Set up the project

1. Create a new Astro project:

    ```bash
    mkdir qdrant-airflow-tutorial && cd qdrant-airflow-tutorial
    astro dev init
    ```

2. To use Qdrant in Airflow, install the Qdrant Airflow provider by adding the following to your `requirements.txt` file:

    ```text
    apache-airflow-providers-qdrant==1.1.0
    ```

## Step 2: Configure credentials

Add the following code to your `.env` file to create Airflow connections between Airflow and HuggingFace and Qdrant. Make sure to update the sample code with your HuggingFace access token and Qdrant instance details.

    ```text
    HUGGINGFACE_TOKEN="<YOUR_HUGGINGFACE_ACCESS_TOKEN>"
    AIRFLOW_CONN_QDRANT_DEFAULT='{
        "conn_type": "qdrant",
        "host": "xyz-example.eu-central.aws.cloud.qdrant.io:6333",
        "password": "<YOUR_QDRANT_API_KEY>"
    }'
    ```

## Step 3: Add your data

Paste the following sample data into a file called `books.txt` in your `include` directory.

    ```text
    1 | To Kill a Mockingbird (1960) | fiction | Harper Lee's Pulitzer Prize-winning novel explores racial injustice and moral growth through the eyes of young Scout Finch in the Deep South.
    2 | Harry Potter and the Sorcerer's Stone (1997) | fantasy | J.K. Rowling's magical tale follows Harry Potter as he discovers his wizarding heritage and attends Hogwarts School of Witchcraft and Wizardry.
    3 | The Great Gatsby (1925) | fiction | F. Scott Fitzgerald's classic novel delves into the glitz, glamour, and moral decay of the Jazz Age through the eyes of narrator Nick Carraway and his enigmatic neighbour, Jay Gatsby.
    4 | 1984 (1949) | dystopian | George Orwell's dystopian masterpiece paints a chilling picture of a totalitarian society where individuality is suppressed and the truth is manipulated by a powerful regime.
    5 | The Catcher in the Rye (1951) | fiction | J.D. Salinger's iconic novel follows disillusioned teenager Holden Caulfield as he navigates the complexities of adulthood and society's expectations in post-World War II America.
    6 | Pride and Prejudice (1813) | romance | Jane Austen's beloved novel revolves around the lively and independent Elizabeth Bennet as she navigates love, class, and societal expectations in Regency-era England.
    7 | The Hobbit (1937) | fantasy | J.R.R. Tolkien's adventure follows Bilbo Baggins, a hobbit who embarks on a quest with a group of dwarves to reclaim their homeland from the dragon Smaug.
    8 | The Lord of the Rings (1954-1955) | fantasy | J.R.R. Tolkien's epic fantasy trilogy follows the journey of Frodo Baggins to destroy the One Ring and defeat the Dark Lord Sauron in the land of Middle-earth.
    9 | The Alchemist (1988) | fiction | Paulo Coelho's philosophical novel follows Santiago, an Andalusian shepherd boy, on a journey of self-discovery and spiritual awakening as he searches for a hidden treasure.
    10 | The Da Vinci Code (2003) | mystery/thriller | Dan Brown's gripping thriller follows symbologist Robert Langdon as he unravels clues hidden in art and history while trying to solve a murder mystery with far-reaching implications.
    ```

## Step 4: Create your DAG

1. In your `dags` folder, create a file called `books_recommend.py`.

2. Copy the following **Recommend books DAG** code into the `books_recommend.py` file.

    <details>
    <summary><strong>Recommend books DAG</strong></summary>
    <CodeBlock language="python">{recommend_books_dag}</CodeBlock>
    </details>

This QDrant Demo DAG consists of six tasks that generate embeddings in parallel for the data corpus and perform semantic retrieval based on user input.
- `import_books`: This task reads a text file containing information about the books (such as title, genre, and description) and then returns the data as a list of dictionaries.

- `init_collection`: This task initializes a collection in the Qdrant database, where you store the vector representations of the book descriptions. The `recreate_collection()` function deletes a collection first if it already exists. Trying to create a collection that already exists throws an error.

- `embed_description`: This is a dynamic task that creates one mapped task instance for each book in the list. The task uses the `embed` function to generate vector embeddings for each description. To use a different embedding model, you can adjust the `EMBEDDING_MODEL_ID` and `EMBEDDING_DIMENSION` values.

- `embed_user_preference`: This task takes a user’s input and converts it into a vector using the same pre-trained model used for the book descriptions.

- `qdrant_vector_ingest`: This task ingests the book data into the Qdrant collection using the `QdrantIngestOperator`, associating each book description with its corresponding vector embeddings.

- `search_qdrant`: Finally, this task performs a search in the Qdrant database using the vectorized user preference. It finds the most relevant book in the collection based on vector similarity.

    ![Screenshot of the graph view for the Qdrant demo DAG, with the each of the six steps shown.](/img/integrations/qdrant-demo-dag.png)

## Step 5: Run your DAG

1. Run `astro dev start` in your Astro project to start Airflow and open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `books_recommend` DAG by clicking the play button. You'll be asked for input about your book preference.

    ![Qdrant reference input shows an example of the UI where Apache Airflow® prompts you to enter your book preference.](/img/integrations/qdrant-reference-input.png)

3. View the output of your search in the logs of the `search_qdrant` task.

    ![Screenshot of the Qdrant output example, that shows the title and description of the book recommendation.](/img/integrations/qdrant-output.png)
