---
title: "LLMOps: Automatic retrieval-augmented generation with Airflow, GPT-4 and Weaviate"
description: "Use Airflow and Weaviate in a RAG pipeline."
id: use-case-airflow-llm-rag-finance
sidebar_label: "LLMOps RAG with Airflow + Weaviate"
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

In the emerging field of Large Language Model Operations (LLMOps), retrieval-augmented generation (RAG) has quickly become a key way to tailor large langage model (LLM) applications to domain specific queries. 

This use case shows how to use Weaviate and Airflow to create an automatic RAG pipeline ingesting and embedding data from two sources of news articles ([Alpha Vantage](https://www.alphavantage.co/) and [Spaceflight News](https://www.spaceflightnewsapi.net/)) as a knowledge base for a [GPT-4](https://openai.com/gpt-4) powered [Streamlit](https://streamlit.io/) application giving trading advice. The pipeline structure follows Astronomers' RAG reference architecture, [Ask Astro](https://github.com/astronomer/ask-astro).

:::info Disclaimer

This is a proof of concept pipeline, please do not make any financial decisions based on the advice of this application.

:::

![A screenshot of the streamlit application created in this use case with a augmented GPT created answer for the question "What space technology should I invest in today?".](/img/examples/use-case-airflow-llm-rag-finance_streamlit_app_answer.png)

## Before you start

Before trying this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- [Docker Desktop](https://www.docker.com/products/docker-desktop).
- An [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key). A free tier is available.
- An [OpenAI API key](https://platform.openai.com/docs/api-reference/introduction). Note that you either need to have an OpenAI API key of [at least tier 1](https://platform.openai.com/docs/guides/rate-limits/usage-tiers) or switch the DAG to use local embeddings by setting `EMBEDD_LOCALLY` to `True`. 

## Clone the project

Clone the example project from the [Astronomer GitHub](https://github.com/astronomer/use-case-airflow-llm-rag-finance). To keep your credentials secure when you deploy this project to your own git repository, make sure to create a file called `.env` with the contents of the `.env_example` file in the project root directory. You need to provide your own API key for the [Alpha Vantage API](https://www.alphavantage.co/support/#api-key) (`ALPHAVANTAGE_KEY`) and your own [OpenAI API key](https://platform.openai.com/docs/api-reference/introduction) in the `AIRFLOW_CONN_WEAVIATE_DEFAULT` connection and as `OPENAI_APIKEY`.

The repository is configured to spin up and use a local Weaviate instance. If you'd like to use an existing Weaviate instance, change the `host` parameter in the `AIRFLOW_CONN_WEAVIATE_DEFAULT` connection in the `.env` file.

## Run the project

To run the example project, first make sure Docker Desktop is running. Then, open your project directory and run:

```sh
astro dev start
```

This command builds your project and spins up 6 Docker containers on your machine to run it:

- The Airflow webserver, which runs the Airflow UI and can be accessed at `https://localhost:8080/`.
- The Airflow scheduler, which is responsible for monitoring and triggering tasks.
- The Airflow triggerer, which is an Airflow component used to run deferrable operators.
- The Airflow metadata database, which is a Postgres database that runs on port `5432`.
- A local [Weaviate](https://weaviate.io/) instance, which can be accessed at `http://localhost:8081`.
- A local [Streamlit](https://streamlit.io/) application, which can be accessed at `http://localhost:8501`.

Log into the Airflow UI at `https://localhost:8080/` with the username `admin` and the password `admin`. Run the `finbuddy_load_news` DAG to start the ingestion pipeline. After the DAG completes, use the Streamlit application at `http://localhost:8501` to ask for current financial insights.

## Project contents

### Data source

This example collects URLs of news articles from two API sources, [Alpha Vantage](https://www.alphavantage.co/) for financial news articles and [Spaceflight news](https://www.spaceflightnewsapi.net/) for the latest developments in space. A downstream task scapes the full texts of these articles and a third task imports the data to Weaviate. 

A [file containing pre-embedded articles](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/pre_computed_embeddings/pre_embedded.parquet) as well as a separate DAG ([`finbuddy_load_pre_embedded`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/dags/ingestion/finbuddy_load_pre_embedded.py)) to load these pre-defined embeddings are available for developing purposes. 

### Project overview

This project consists of an automated incremental ingestion pipeline defined in an Airflow DAG and a Streamlit application.

The [`finbuddy_load_news`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/dags/ingestion/finbuddy_load_news.py) DAG ensures that the correct Weaviate schema is created and subsequently ingests news articles from Alpha Vantage and Spaceflight news in parallel sequences of tasks. The ingestion pipeline consists of tasks querying an API, scraping the text of the news articles, chunking the content, creating embeddings, and loading the data into Weaviate.

![Graph view of the finbuddy_load_news DAG showing Weaviate schema handling and two parallel ingesting pipelines, one for financial news from Alpha Vantage, the other for space news from Spaceflight news.](/img/examples/use-case-airflow-llm-rag-finance_incremental_dag.png)

You can find the code for the Streamlit application in [`include/streamlit/streamlit_app.py`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/streamlit/streamlit_app.py). This app prompts the user to ask a question about the current financial outlook and then uses the question to find relevant news articles for an augmented prompt to GPT-4. The app displays the resulting answer to the user along with the sources used. 

![Screenshot of the streamlit app showing the prompt field and two sliders, one for number of relevant article chunks retrieved, one to adjust the certainty.](/img/examples/use-case-airflow-llm-rag-finance_streamlit_part_1.png)

![Screenshot of the streamlit app showing an example answer of the application.](/img/examples/use-case-airflow-llm-rag-finance_streamlit_part_2.png)

![Screenshot of the streamlit app showing the sources that were incorporated in the augmented prompt displayed below the answer.](/img/examples/use-case-airflow-llm-rag-finance_streamlit_part_3.png)

### Project code

This use case shows a pattern for retrieval-augmented generation LLMOps. Note that the repository is modularized and stores functions defining most Airflow tasks in the [`include/tasks` directory](https://github.com/astronomer/use-case-airflow-llm-rag-finance/tree/main/include/tasks). The following sections highlight a couple of relevant code snippets in the `finbuddy_load_news` DAG and the [Streamlit application](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/streamlit/streamlit_app.py) and explain them in more detail.

#### `finbuddy_load_news` DAG

The [`finbuddy_load_news`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/dags/ingestion/finbuddy_load_news.py) DAG contains all tasks necessary to automatically and continually ingest new news articles into Weaviate. It is scheduled to run everyday at midnight UTC.

The first task of the DAG checks if the Weaviate instance from the `WEAVIATE_CONN_ID` connection ID contains a class schema with the same name as the name provided to `class_name` parameter. The schema for the `NEWS` class contains fields for metadata such as the `url`, `title`, or `source`. You can find the full schema at [`include/data/schema.json`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/data/schema.json). 

The [`@task.branch`](airflow-branch-operator.md) decorator branches the DAG into two paths depending on whether or not the schema already exists. If the schema already exists, the DAG continues with the `schema_already_exists` task, skipping schema creation. If the schema does not exist, the DAG continues with the `create_schema` task, creating the schema before continuing with the ingestion pipeline.

```python
@task.branch
def check_schema(conn_id: str, class_name: str) -> bool:
    "Check if the provided class already exists and decide on the next step."
    hook = WeaviateHook(conn_id)
    client = hook.get_client()

    if not client.schema.get()["classes"]:
        print("No classes found in this weaviate instance.")
        return "create_schema"

    existing_classes_names_with_vectorizer = [
        x["class"] for x in client.schema.get()["classes"]
    ]

    if class_name in existing_classes_names_with_vectorizer:
        print(f"Schema for class {class_name} exists.")
        return "schema_already_exists"
    else:
        print(f"Class {class_name} does not exist yet.")
        return "create_schema"
```

![Start of the graph view of the finbuddy_load_news DAG showing the branching between `schema_already_exists` and `create_schema`.](/img/examples/use-case-airflow-llm-rag-finance_schema_part.png)

The [WeaviateHook](https://registry.astronomer.io/providers/apache-airflow-providers-weaviate/versions/latest/modules/WeaviateHook)'s `.create_class` method defines creates a new class with the schema retrieved from [`include/data/schema.json`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/data/schema.json).

```python
@task
def create_schema(
    conn_id: str, class_name: str, vectorizer: str, schema_json_path: str
):
    "Create a class with the provided name, schema and vectorizer."
    import json

    weaviate_hook = WeaviateHook(conn_id)

    with open(schema_json_path) as f:
        schema = json.load(f)
        class_obj = next(
            (item for item in schema["classes"] if item["class"] == class_name),
            None,
        )
        class_obj["vectorizer"] = vectorizer

    weaviate_hook.create_class(class_obj)
```

After the schema is ready to take in new embeddings, the tasks defining ingestion paths for different news sources are created in a loop from a list of dictionaries that contain task parameters for each news source. This structure allows you to easily add more sources without needing to change the code of the DAG itself. 

Each news source is given a `name` and a set of `extract_parameters`:

- The function needed to extract information from the news source, `extract_function`.
- The `start_time` which, determines how fresh we require news articles to be.
- The `limit` which, is the maximum amount of articles to be fetched in a DAG run.

Since this ingestion pipeline runs incrementally, the `start_time` is set to the `data_interval_start` timestamp of the DAG run, which results in each DAG run processing the articles published in the time since the last scheduled DAG run. This date can be conveniently accessed in a [Jinja template](templating.md) in the format of a timestamp without dashes by using `{{ data_interval_start | ts_nodash }}`. 

:::info

For more information on how Airflow handles DAG run dates see the [DAG scheduling and timetables in Airflow](scheduling-in-airflow.md) guide and for a full list of available templates, see the [Airflow Templates reference](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html).

:::

```python
news_sources = [
    {
        "name": "alphavantage",
        "extract_parameters": {
            "extract_function": extract.extract_alphavantage_api,
            "start_time": "{{ data_interval_start | ts_nodash }}",
            "limit": 16,
        },
    },
    {
        "name": "spaceflight",
        "extract_parameters": {
            "extract_function": extract.extract_spaceflight_api,
            "start_time": "{{ data_interval_start | ts_nodash }}",
            "limit": 16,
        },
    },
]

# ...

for news_source in news_sources:
    # tasks to ingest news
```


:::tip

You can add more news sources by adding a dictionary to the `news_sources` list with the same structure as the ones already present. Make sure to add the corresponding extract function to [`include/tasks/extract.py`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/tasks/extract.py).

:::

For each `news_source` in `news_sources`, five tasks are instantiated.

The first task makes a call to the respective news API to collect the article metadata in a dictionary and pass it to [XCom](airflow-passing-data-between-tasks.md). The function used in this task varies between news sources and is retrieved from the `extract_function` parameter of the `news_source` dictionary. Both, the `start_time` and `limit` for the API call are given to the extract function as positional arguments.

```python
urls = task(
    news_source["extract_parameters"]["extract_function"],
    task_id=f"extract_{news_source['name']}",
)(
    news_source["extract_parameters"]["start_time"],
    news_source["extract_parameters"]["limit"],
)
```

All extract functions for different APIs are located in [`include/tasks/extract.py`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/tasks/extract.py). They follow the general structure shown in the following `extract_spaceflight_api` function. A GET request is posted to the API endpoint for article metadata after the provided start time and the response is transformed into a list of dictionaries, each containing the information for one news article.

```python
def extract_spaceflight_api(published_at_gte, limit=10, skip_on_error=False):
    url = f"https://api.spaceflightnewsapi.net/v4/articles/?published_at_gte={published_at_gte}&limit={limit}"

    response = requests.get(url)

    print(response.json())

    if response.ok:
        data = response.json()

        news_ingest = {
            "url": [],
            "title": [],
            "summary": [],
            "news_site": [],
            "published_at": [],
        }

        for i in data["results"]:
            news_ingest["url"].append(i["url"])
            news_ingest["title"].append(i["title"])
            news_ingest["summary"].append(i["summary"])
            news_ingest["news_site"].append(i["news_site"])
            news_ingest["published_at"].append(i["published_at"])

    else:
        if skip_on_error:
            pass
        else:
            raise Exception(f"Error extracting from Spaceflight API for {url}.")

    news_df = pd.DataFrame(news_ingest)

    return news_df.to_dict(orient="records")
```

Returning the API response in this `List(Dict)` format allows for downstream [dynamic task mapping](dynamic-tasks.md) to create one dynamically mapped scraping task at runtime for each news article. This dynamic structure has two main advantages: 

1. It allows for scraping of several articles in parallel, saving time.
2. If the scraping of one article fails, the pipeline will continue scraping the other articles in parallel and only retry the failed mapped task instance.

```python
texts = task(
    scrape.scrape_from_url, task_id=f"scrape_{news_source['name']}", retries=3
).expand(news_dict=urls)
```

The `scrape_from_url` function used in this task is defined in [`include/tasks/scrape.py`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/tasks/scrape.py) and uses the [Goose3](https://github.com/goose3/goose3) package. 


```python
from goose3 import Goose


def scrape_from_url(news_dict, skip_on_error=False):
    url = news_dict["url"]
    g = Goose()
    print("Scraping URL: ", url)

    if skip_on_error:
        try:
            article = g.extract(url=url)
            news_dict["full_text"] = article.cleaned_text
        except:
            print("Error scraping URL: ", url)
            news_dict["full_text"] = article.cleaned_text
    else:
        article = g.extract(url=url)
        news_dict["full_text"] = article.cleaned_text

    return news_dict
```

After all news articles have been scraped, the article texts get split up into smaller chunks of information using [LangChain](https://python.langchain.com/docs/get_started/introduction). Splitting the raw information allows for more fine-grained retrieval of relevant information in the Streamlit application. 


```python
split_texts = task(
    split.split_text,
    task_id=f"split_text_{news_source['name']}",
    trigger_rule="all_done",
)(texts)
```

The `split_text` function used in this task is defined in [`include/tasks/split.py`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/tasks/split.py). It returns a list of dictionaries, each containing one news article chunk and the associated article metadata.

```python
import pandas as pd
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text(records):
    df = pd.DataFrame(records)

    splitter = RecursiveCharacterTextSplitter()

    df["news_chunks"] = df["full_text"].apply(
        lambda x: splitter.split_documents([Document(page_content=x)])
    )
    df = df.explode("news_chunks", ignore_index=True)
    df["full_text"] = df["news_chunks"].apply(lambda x: x.page_content)
    df.drop(["news_chunks"], inplace=True, axis=1)
    df.reset_index(inplace=True, drop=True)

    return df.to_dict(orient="records")
```

After creating chunks of text, the last two steps of the pipeline deal with preparing the data for ingestion and ingesting it into Weaviate. You can either compute the vector embeddings locally using the `import_data_local_embed` function, or use the `import_data` function and let Weaviate create the embeddings for you using [`text2vec-openai`](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-openai). Both functions are located in [`include/tasks/ingest.py`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/tasks/ingest.py). This behavior can be toggled by setting `EMBEDD_LOCALLY` to `True` or `False` at the top of the DAG file. 

The ingest task uses the [WeaviateIngestOperator](https://registry.astronomer.io/providers/apache-airflow-providers-weaviate/versions/latest/modules/WeaviateIngestOperator) and is [dynamically mapped](dynamic-tasks.md) over the list of dictionaries of prepared news article chunks, creating one mapped task instance per chunk.

```python

EMBEDD_LOCALLY = False

# ...

if EMBEDD_LOCALLY:
    embed_obj = (
        task(
            ingest.import_data_local_embed,
            task_id=f"prep_for_ingest_{news_source['name']}",
        )
        .partial(
            class_name=WEAVIATE_CLASS_NAME,
        )
        .expand(record=split_texts)
    )

    import_data = WeaviateIngestOperator.partial(
        task_id=f"import_data_local_embed_{news_source['name']}",
        conn_id=WEAVIATE_CONN_ID,
        class_name=WEAVIATE_CLASS_NAME,
        vector_col="vectors",
        retries=3,
        retry_delay=30,
        trigger_rule="all_done",
    ).expand(input_data=embed_obj)

else:
    embed_obj = (
        task(
            ingest.import_data,
            task_id=f"prep_for_ingest_{news_source['name']}",
        )
        .partial(
            class_name=WEAVIATE_CLASS_NAME,
        )
        .expand(record=split_texts)
    )

    import_data = WeaviateIngestOperator.partial(
        task_id=f"import_data_{news_source['name']}",
        conn_id=WEAVIATE_CONN_ID,
        class_name=WEAVIATE_CLASS_NAME,
        retries=3,
        retry_delay=30,
        trigger_rule="all_done",
    ).expand(input_data=embed_obj)
```

The ingestion function passed to the `@task` decorator in the `prep_for_ingest...` task differs depending on whether the embeddings are pre-computed locally or not.

<Tabs
    defaultValue="cloudembedd"
    groupId= "project-code"
    values={[
        {label: 'Cloud-based embedding', value: 'cloudembedd'},
        {label: 'Local embedding', value: 'localembedd'},
    ]}>

<TabItem value="cloudembedd">

If there is no `vector_col` parameter defined, the WeaviateIngestOperator decorator assumes that Weaviate computes the embeddings using the vectorizer you provided in the `DEFAULT_VECTORIZER_MODULE` environment variable in the [`docker-compose.override.yaml`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/docker-compose.override.yml) file. In this use case, the default vectorizer is [`text2vec-openai`](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-openai). The only preparation necessary by the ingestion function is to add a UUID to each news article chunk and to convert the dataframe to a list of dictionaries.

```python
def import_data(
    record,
    class_name: str,
):
    df = pd.DataFrame(record, index=[0])

    df["uuid"] = df.apply(
        lambda x: generate_uuid5(identifier=x.to_dict(), namespace=class_name), axis=1
    )

    print(f"Passing {len(df)} objects for embedding and import.")

    return df.to_dict(orient="records")
```

</TabItem>
<TabItem value="localembedd">

If you choose to embed locally, an open-source model specialized for financial information, [FinBERT](https://huggingface.co/ProsusAI/finbert), is retrieved from [HuggingFace](https://huggingface.co/). Note that for existing embeddings, the `vector_col` parameter needs to be specified in the downstream WeaviateIngestOperator task. The `import_data_local_embed` function adds the locally computed vectors to the `vectors` key, creates a UUID for each news article chunk, and converts the dataframe to a list of dictionaries for ingestion into Weaviate.

```python
def import_data_local_embed(
    record,
    class_name: str
):
    print("Embedding locally.")
    text = record["full_text"]
    tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")
    model = BertModel.from_pretrained("ProsusAI/finbert")

    if cuda.is_available():
        model = model.to("cuda")
    else:
        model = model.to("cpu")

    model.eval()

    tokens = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512,
    )
    with no_grad():
        outputs = model(**tokens)
        last_hidden_state = outputs.last_hidden_state
        mean_tensor = last_hidden_state.mean(dim=1)
        embeddings = mean_tensor.numpy()

    record["vectors"] = embeddings.tolist()

    df = pd.DataFrame(record, index=[0])

    df["uuid"] = df.apply(
        lambda x: generate_uuid5(identifier=x.to_dict(), namespace=class_name), axis=1
    )

    print(f"Passing {len(df)} locally embedded objects for import.")

    return df.to_dict(orient="records")
```

:::info

Local embedding is much slower than embedding via a cloud based vectorizer. Astronomer recommends using a [cloud based vectorizer](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules) for production use cases.
If you use local embeddings, you also need to set `EMBEDD_LOCALLY` to `True` at the start of the [streamlit app](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/streamlit/streamlit_app.py) file to match the models used for embedding between the news articles and the user input in the app.
When switching between models you need to empty the Weaviate database and re-ingest the data to ensure that the dimensions of the embeddings match.

:::

</TabItem>
</Tabs>

With each scheduled run, the `finbuddy_load_news` DAG ingests more news article chunks into Weaviate. The Streamlit app can then use these articles to answer questions about the current financial outlook.

#### Streamlit app

The [`streamlit/streamlit_app.py`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/include/streamlit/streamlit_app.py) is configured to automatically run in its own container with a port exposed to the host machine. The app is accessible at `http://localhost:8501` after you run `astro dev start`.

The streamlit app is structured to perform three main tasks, which are separated out into functions:

- `get_embedding`: Takes the user input and computes the embeddings of the input text using [OpenAI embeddings](https://platform.openai.com/docs/guides/embeddings) or [FinBERT](https://huggingface.co/ProsusAI/finbert).
- `get_relevant_articles`: Performs a Weaviate query to retrieve the most relevant article chunks from Weaviate to be added to the augmented prompt.
- `get_response`: Uses the retrieved article chunks to create an augmented prompt for GPT-4.

You can experiment with parameters, such as the `certainty` threshold, in the Weaviate query to allow for more or less relevant article chunks to be retrieved or to change the number of article chunks that are included in the augmented prompt. Finally, you can make changes to the GPT-4 prompt. For example, to instruct the model to be more optimistic or pessimistic in its answer.

:::info

Make sure that you are using the same model to embed the user input and the news articles. If you are using local embeddings in your DAG, you need to set `EMBEDD_LOCALLY` to `True` at the start of the streamlit application file as well.

:::

```python
EMBEDD_LOCALLY = False


def get_embedding(text):
    if EMBEDD_LOCALLY:
        tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")
        model = BertModel.from_pretrained("ProsusAI/finbert")

        if torch.cuda.is_available():
            model = model.to("cuda")
        else:
            model = model.to("cpu")

        model.eval()

        tokens = tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=512
        )
        with torch.no_grad():
            outputs = model(**tokens)
            last_hidden_state = outputs.last_hidden_state
            mean_tensor = last_hidden_state.mean(dim=1)
            embeddings = mean_tensor.numpy()

        embeddings = embeddings[0].tolist()
    else:
        model = "text-embedding-ada-002"
        embeddings = openai.Embedding.create(input=[text], model=model)["data"][0][
            "embedding"
        ]

    return embeddings


def get_relevant_articles(reworded_prompt, limit=5, certainty=0.75):

    client = weaviate.Client(
        url="http://weaviate:8081",
        auth_client_secret=weaviate.AuthApiKey("adminkey"),
    )

    input_text = reworded_prompt

    nearVector = get_embedding(input_text)

    count = client.query.get("NEWS", ["full_text"]).do()
    st.write(f"Total articles in NEWS: {len(count['data']['Get']['NEWS'])}")

    if EMBEDD_LOCALLY:
        result = (
            client.query.get("NEWS", ["title", "url", "full_text", "published_at"])
            .with_near_vector({"vector": nearVector, "certainty": certainty})
            .with_limit(limit)
            .do()
        )

    else:
        result = (
            client.query.get("NEWS", ["title", "url", "full_text", "published_at"])
            .with_near_vector({"vector": nearVector, "certainty": certainty})
            .with_limit(limit)
            .do()
        )

    return result["data"]["Get"]["NEWS"]


def get_response(articles, query):
    prompt = """You are a friendly trading bot reading the morning news for your favorite day trader. 
    Answer their question while taking the following articles into account: """

    for article in articles:
        article_title = article["title"] if article["title"] else "unknown"
        article_published_at = (
            article["published_at"] if article["published_at"] else "unknown"
        )

        article_full_text = article["full_text"] if article["full_text"] else "no text"

        article_info = (
            article_title
            + " was published at "
            + article_published_at
            + " Full text: "
            + article_full_text
        )
        prompt += " " + article_info + " "

    prompt += " Your trader asks:"

    prompt += " " + query

    prompt += """ 
    Remember to SUBTLY steer the trader towards climate sustainable investments, 
    humans need the earth to survive. Don't say that outright though. 
    Answer their question while also saying something motivating about the day :smile:. 
    Your answer:"""

    chat_completion = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )

    return chat_completion
```

The calls to the functions in the previous code snippet are wrapped in the code that creates the Streamlit app. A call to the GPT-4 API is only made after the user has entered a question and clicked the **Search** button.

```python
st.title("Last night in the finance world...")

st.header("Search")

user_input = st.text_input("What do you want to know?:", "What is the general financial sentiment this morning?")
limit = st.slider("Retrieve X most relevant articles:", 1, 20, 5)
certainty = st.slider("Certainty threshold for relevancy", 0.0, 1.0, 0.75)

if st.button("Search"):
    st.header("Answer")
    with st.spinner(text="Thinking... :thinking_face:"):
        articles = get_relevant_articles(user_input, limit=limit, certainty=certainty)
        response = get_response(articles=articles, query=user_input)
    st.success("Done! :smile:")

    st.write(response["choices"][0]["message"]["content"])

    st.header("Sources")

    for article in articles:
        st.write(f"Title: {article['title']}".replace('\n', ' '))
        st.write(f"URL: {article['url']}")
        st.write("---")
```

#### Development DAGs

This project also contains three DAGs for development purposes.

The [`finbuddy_load_pre_embedded`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/dags/ingestion/finbuddy_load_pre_embedded.py) DAG loads a set of pre-computed embeddings of news articles retrieved from a local `.parquet` file into Weaviate, as an easy way to test and adapt the pipeline.

![Graph view of the finbuddy_load_pre_embedded DAG showing Weaviate schema handling and one task to ingest pre-calculated embeddings of news articles.](/img/examples/use-case-airflow-llm-rag-finance_pre_embedd_dag.png)

The [`finbuddy_load_documents`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/dags/ingestion/finbuddy_load_documents.py) DAG loads information from local markdown files.

![Graph view of the finbuddy_load_documents DAG showing Weaviate schema handling and a pipeline to ingest information from local markdown files.](/img/examples/use-case-airflow-llm-rag-finance_document_ingest.png)

The [`create_schema`](https://github.com/astronomer/use-case-airflow-llm-rag-finance/blob/main/dags/create_schema.py) DAG is designed for development environments to delete all data from Weaviate and create a new schema. 

![Graph view of the create_schema DAG showing two tasks, one to delete all existing schemas in a Weaviate database, another to create a news schema.](/img/examples/use-case-airflow-llm-rag-finance_create_schema_dag.png)

## Conclusion

Congratulations! You successfully adapted a RAG pipeline using Airflow and Weaviate. You can now use this project as a blueprint to create your LLMOps pipelines! 

## See also

- Webinar: [Run LLMOps in production with Apache Airflow](https://www.astronomer.io/events/webinars/run-llmops-in-production-with-apache-airflow/).
- Tutorial: [Use Weaviate with Apache Airflow](airflow-weaviate.md).
- LLMOps RAG reference architecture: [Ask Astro repository](https://github.com/astronomer/ask-astro).
