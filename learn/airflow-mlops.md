---
title: "Best practices for orchestrating MLOps pipelines with Airflow"
sidebar_label: "MLOps"
description: "Learn how to use Airflow to run machine learning in production."
id: airflow-mlops
---

**Machine Learning Operations** (MLOps) is a broad term encompassing everything needed to run machine learning models in production. MLOps is a rapidly evolving field with many different best practices and behavioral patterns, with Apache Airflow providing tool agnostic orchestration capabilities for all steps.

In this guide you learn:

- How Airflow fits into the MLOps landscape.
- How Airflow can be used for large language model operations (LLMOps).
- How Airflow can help you implement best practices for different MLOps components.
- Which Airflow features and integrations are especially useful for MLOps.
- Where to find additional resources and reference implementations on using Airflow for MLOps.

:::tip

Ready to get started? Check out the recommended resources that showcase machine learning (ML) implementations with Airflow:

- [Ask Astro](https://github.com/astronomer/ask-astro) LLM Retrieval Augmented Generation pipeline reference architecture ([Blog post deep dive](https://www.astronomer.io/blog/ask-astro-operationalizing-data-ingest-for-retrieval-augmented-generation-with-llms-part-3/)).
- [The Laurel Algorithm: MLOps, AI, and Airflow for Perfect Timekeeping](https://www.astronomer.io/events/webinars/the-laurel-algorithm-mlops-ai-and-airflow-for-perfect-timekeeping/) webinar.
- [Run an integrated ELT and ML pipeline on Stripe data in Airflow](use-case-elt-ml-finance.md) use case.

:::

## Assumed Knowledge

To get the most benefits from this guide, you need an understanding of:

- The basics of [Machine Learning](https://www.coursera.org/specializations/machine-learning-introduction).
- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).

## Why use Airflow for MLOps?

**Machine learning operations** (MLOps) encompasses all patterns, tools, and best practices related to running machine learning models in production.

Apache Airflow sits at the heart of the modern MLOps stack. Because it is tool agnostic, Airflow can orchestrate all actions in any MLOps tool that has an API. Combined with already being the de-facto standard for orchestrating data pipelines, Airflow is the perfect tool for data engineers and machine learning engineers to standardize their workflows and collaborate on pipelines.

The benefits of using Airflow for MLOps are:

- **Python native**: You use Python code to define Airflow pipelines, which makes it easy to integrate the most popular machine learning tools and embed your ML operations in a best practice CI/CD workflow. By using the [decorators](airflow-decorators.md) of the TaskFlow API you can turn existing scripts into Airflow tasks.
- **Extensible**: Airflow itself is written in Python, which makes it extensible with [custom modules](airflow-importing-custom-hooks-operators.md) and [Airflow plugins](using-airflow-plugins.md).
- **Monitoring and alerting**: Airflow comes with production-ready monitoring and alerting modules like [Airflow notifiers](error-notifications-in-airflow.md#notifiers), [extensive logging features](logging.md), and [Airflow listeners](airflow-listeners.md). They enable you to have fine-grained control over how you monitor your ML operations and how Airflow alerts you if something goes wrong.
- **Pluggable compute**: When using Airflow you can [pick and choose](#model-operations-and-compute-considerations) the compute you want to use for each task. This allows you to use the the perfect environment and resources for every single action in your ML pipeline. For example, you can run your data engineering tasks on a Spark cluster and your model training tasks on a GPU instance.
- **Data agnostic**: Airflow is data agnostic, which means it can be used to orchestrate any data pipeline, regardless of the data format or storage solution. You can plug in any new data storage, such as the latest vector database or your favorite RDBMS, with minimal effort.
- **Incremental and idempotent pipelines**: Airflow allows you to define pipelines that operate on data collected in a specified timeframe and to perform [backfills and reruns](rerunning-dags.md#backfill) of a set of idempotent tasks. This lends itself well to creating feature stores, especially for time-dimensioned features, which form the basis of advanced model training and selection.
- **Ready for day 2 Ops**: Airflow is a mature orchestrator, coming with built-in functionality such as [automatic retries](rerunning-dags.md#automatically-retry-tasks), complex [dependencies](managing-dependencies.md) and [branching](airflow-branch-operator.md) logic, as well as the option to make pipelines [dynamic](dynamic-tasks.md).
- **Integrations**: Airflow has a large ecosystem of [integrations](https://registry.astronomer.io/providers), including many popular [MLOps tools](#airflow-integrations-for-mlops).
- **Shared platform**: Both data engineers and ML engineers use Airflow, which allows teams to create direct dependencies between their pipelines, such as using [Airflow Datasets](airflow-datasets.md).
- **Use existing expertise**: Many organizations are already using Apache Airflow for their data engineering workflows and have developed best practices and custom tooling around it. This means that data engineers and ML engineers alike can build upon existing processes and tools to orchestrate and monitor ML pipelines.

## Why use Airflow for LLMOps?

**Large Language Model Operations** (LLMOps) is a subset of MLOps that describes interactions with large language models (LLMs). In contrast to traditional ML models, LLMs are often too large to be trained from scratch and LLMOps techniques instead revolve around adapting existing LLMs to new use cases.

The three main techniques for LLMOps are:

- **Prompt engineering**: This is the simplest technique to influence the output of an LLM. You can use Airflow to create a pipeline that ingests user prompts and modifies them according to your needs, before sending them to the LLM inference endpoint.
- **Retrieval augmented generation** (RAG): RAG pipelines retrieve relevant context from domain-specific and often proprietary data to improve the output of an LLM. See [Ask Astro](https://github.com/astronomer/ask-astro) for an Airflow RAG reference architecture.
- **Fine-tuning**: Fine-tuning LLMs typically involves retraining the final layers of an LLM on a specific dataset. This often requires more complex pipelines and a larger amount of [compute](#model-operations-and-compute-considerations) that can be orchestrated with Airflow.

## Components of MLOps

MLOps describes different patterns in how organizations can productionize machine learning models. MLOps consists of four main components:

- **BusinessOps**: the processes and activities in an organization that are needed to deliver any outcome, including successful MLOps workflows.
- **DevOps**: the software development (dev) and IT operations (ops) practices that are needed for the delivery of any high quality software, including machine learning based applications.
- **DataOps**: the practices and tools surrounding data engineering and data analytics to build the foundation for machine learning implementations.
- **ModelOps**: automated governance, management and monitoring of machine learning models in production.

Organizations are often at different stages of maturity for each of these components when starting their MLOps journey. Using Apache Airflow to orchestrate MLOps pipelines can help you progress in all of them.

### BusinessOps

The first component of MLOps is to make sure there is strategic aligment with all stakeholders. This component varies widely depending on your organization and use case and can include:

- **Business strategy**: Defining what ML is used for in an organization and what trade-offs are acceptable. Often, models can be optimized for different metrics, for example high recall or high precision, and domain experts are needed to determine the right metrics and model strategy.
- **Model governance**: Creating and following regulations for how your organization uses machine learning. This often depends on relevant regulations, like GDPR or HIPAA. Airflow has a built-in integration option with [Open Lineage](airflow-openlineage.md), the open-source standard for tracking data lineage, which is a key component of model governance.

### DevOps

Since you define Airflow pipelines in Python code, you can apply DevOps best practices when using Airflow. This includes:

- **Version control**. All code and configuration should be stored in a version control system like [Git](https://git-scm.com/). Version control allows you to track all changes of your pipeline, ML model, and environment over time and roll back to previous versions if needed. Astro customers can take advantage of [Deployment rollbacks](https://www.astronomer.io/docs/astro/deploy-history).
- **Continuous integration/ continuous delivery** ([CI/CD](https://resources.github.com/ci-cd/)). It is a standard Software best practice for all code to undergo automatic testing, linting, and deployment. This ensures that your code is always in a working state and that any changes are automatically deployed to production. Airflow integrates with all major CI/CD tools, see [CI/CD templates](https://www.astronomer.io/docs/astro/ci-cd-templates/template-overview) for popular templates.

:::info

Astronomer customers can use the Astro GitHub integration, which allows you to automatically deploy code from a GitHUb repository to an Astro deployment, viewing Git metadata in the Astro UI. See [Deploy code with the Astro GitHub integration](https://www.astronomer.io/docs/astro/deploy-github-integration).

:::

- **Infrastructure as code** ([IaC](https://en.wikipedia.org/wiki/Infrastructure_as_code)). Ideally, all infrastructure is defined as code and follows the same CI/CD process as your pipeline and model code. This allows you to control and, if necessary, roll back environment changes, or quickly deploy new instances of your model.

In practice, following modern DevOps patterns when using Airflow for MLOps means:

- Storing all Airflow code and configuration in a version control system like Git.
- Setting up development, staging, and production branches in your version control system and also connecting them to different Airflow environments. For Astro customers, see [Manage Astro connections in branch-based deploy workflows](https://www.astronomer.io/docs/astro/astro-use-case/use-case-astro-connections).
- Use automatic testing and linting for all Airflow code before deployment.
- Define all infrastructure as code and use the same CI/CD process for infrastructure as for your Airflow code.
- Store model artifacts in a versioned system. This can be a dedicated tool like MLFlow or an object storage solution.

![Diagram showing how Airflow code and configuration is stored in a version control system and deployed to different Airflow environments.](/img/guides/airflow-mlops_devops.png)

### DataOps

There is no MLOps without data. You need to have robust data engineering workflows in place in order to confidently train, test, and deploy ML models in production. Apache Airflow has been used by millions of data engineers to create reliable best practice data pipelines, providing a strong foundation for your MLOps workflows.

Give special considerations to the following:

- [**Data quality**](data-quality.md) and data cleaning. If your data is of bad quality, your model predictions will be too. Astronomer recommends incorporating data quality checks and data cleaning steps into your data pipelines to define and monitor the requirements your data has to fulfill in order for downstream ML operations to be successful. Airflow supports integration with any data quality tool that has an API, and has pre-built integrations for tools such as [Great Expectations](airflow-great-expectations.md) and [Soda Core](soda-data-quality.md).
- **Data preprocessing and feature engineering**. It is common for data to undergo several transformation steps before it is ready to be used as input for an ML model. These steps can include simple [preprocessing steps](https://scikit-learn.org/stable/modules/preprocessing.html) like scaling, one-hot-encoding, or imputation of missing values. It can also include more complex steps like [feature selection](https://scikit-learn.org/stable/modules/feature_selection.html#feature-selection), [dimensionality reduction](https://en.wikipedia.org/wiki/Dimensionality_reduction), or [feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html). Airflow allows you to run preprocessing and feature engineering steps in a pythonic way using [Airflow decorators](airflow-decorators.md).
- **Data storage**.
    - Training and testing data. The best way to store your data highly depends on your data and type of ML. Data engineering includes ingesting data and moving it to the ideal platform for your ML model to access. This can, for example, be an object storage solution, a relational database management system (RDBMS), or a vector database. Airflow integrates with all these options, with tools such as [Airflow object storage](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html) and the [Astro Python SDK](https://www.astronomer.io/docs/learn/astro-python-sdk) simplifying common operations.
    - Model artifacts. Model artifacts include model parameters, hyperparameters, and other metadata. Airflow integrates with specialized version control systems such as [MLFlow](airflow-mlflow.md) or [Weights and Biases](airflow-weights-and-biases.md).

Apart from the foundations mentioned above, second day data quality operations in MLOps often include advanced topics like data governance, [data lineage](airflow-openlineage.md), and data cataloging as well as monitoring of data drift.

In practice, following modern data engineering patterns when using Airflow for MLOps means:

- Following general [Airflow best practices](dag-best-practices.md) for DAG writing, such as keeping tasks atomic and idempotent.
- Using Airflow to orchestrate data ingestion from sources such as APIs, source databases, and object storage into a working location for your ML model. This might be a vector database, a relational database, or an object storage solution depending on your use case.
- Incorporating data quality checks into your Airflow pipelines, with critical data quality checks halting the pipeline or alerting you if they fail.
- Using Airflow to orchestrate data preprocessing and feature engineering steps.
- Moving data to permanent cold storage after it has been used for training and testing.

![Diagram showing an example ETL/ELT pipeline for Machine Learning.](/img/guides/airflow-mlops_de.png)

### ModelOps

After you establish strong DevOps and data engineering foundations, you can start to implement model operations.

With Airflow you can use the ML tools and compute locations of your choice. Some organizations choose to use external compute for all of their heavy workloads, for example:

- **External Kubernetes clusters**: with the [KubernetesPodOperator](kubepod-operator.md) (and its decorator version `@task.kubernetes`).
- **Databricks**: with the [Astro Databricks provider](https://github.com/astronomer/astro-provider-databricks) and [Databricks Airflow provider](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest).
- **Spark**: with modules from the [Spark Airflow provider](https://registry.astronomer.io/providers/apache-airflow-providers-apache-spark/versions/latest).
- **External compute**: in [AWS](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest), [Azure](https://registry.astronomer.io/providers/apache-airflow-providers-microsoft-azure/versions/latest) and [Google Cloud](https://registry.astronomer.io/providers/apache-airflow-providers-google/versions/latest) using the respective Airflow providers.

Other Airflow users decide to [scale up](airflow-scaling-workers.md) their Airflow infrastructure with larger worker nodes for compute intensive tasks. Astro customers can leverage the [worker queues](https://www.astronomer.io/docs/astro/configure-worker-queues) feature, which lets them decide the exact specifications for the workers each task can run on. This means that Airflow only uses large workers for the biggest workloads, saving compute and cost.

In practice, following modern model operations patterns when using Airflow for MLOps means:

- Performing exploratory data analysis and test potential ML applications on small subsets of data in a notebook environment before moving to production. Tools like [Jupyter notebooks](https://jupyter.org/) are widely used and run Python code you can later convert to tasks in Airflow DAGs.
- Using Airflow to orchestrate model training, fine-tuning, testing, and deployment.
- Having Airflow tasks monitor the performance of your model and perform automated actions such as re-training, re-deploying, or alerting if the performance drops below a certain threshold.

![Diagram showing different Airflow DAGs relating to model operations in an MLOps pipeline](/img/guides/airflow-mlops_ml_dags.png)

## How Airflow addresses MLOps challenges

When using Apache Airflow for MLOps, there are three main patterns you can follow:

- Using Apache Airflow to orchestrate actions in other MLOps tools. Airflow is a tool-agnostic orchestrator, which means it can also orchestrate all actions in ML specific tools like [MLFlow](airflow-mlflow.md) or [AWS SageMaker](airflow-sagemaker.md).
- Combine orchestration of actions in other tools with ML operations running within Airflow. For example, you can create vector embeddings in a Python function in Airflow and then use these embeddings to train a model in [Google Datalab](https://cloud.google.com/monitoring/datalab/set-up-datalab). Modules like the [`@task.kubernetes`](kubepod-operator.md#use-the-taskkubernetes-decorator) or [`@task.external_python_operator`](airflow-isolated-environments.md) make it easy to run any Python code in isolation with optimized environments and resources.
- Run all your MLOps using Python modules inside Airflow tasks. Since Airflow can run any Python code and [scale indefinitely](airflow-scaling-workers.md), you can use it as an all-purpose MLOps tool.

### Airflow features for MLOps

A specific set of Airflow features can help you implement MLOps best practices:

- [Data driven scheduling](airflow-datasets): With Airflow datasets, you can schedule DAGs to run after a specific dataset is updated by any task in the DAG. For example, you can schedule your model training DAG to run after the training dataset is updated by the data engineering DAG. See [Orchestrate machine learning pipelines with Airflow datasets](use-case-airflow-datasets-multi-team-ml.md).

    ![Screenshot of the Datasets view showing the dataset_de_dag as the producing DAG to the postgres://prodserver:2319/trainset dataset. The dataset_ml_dag is the consuming DAG.](/img/guides/airflow-mlops_datasets.png)

- [Dynamic task mapping](dynamic-tasks.md): In Airflow, you can map tasks and task groups dynamically at runtime. This allows you to run similar operations in parallel without knowing in advance how many operations run in any given DAGrun. For example, you can dynamically run a set of model training tasks in parallel, each with different hyperparameters.

    ![DAG with a dynamically mapped task group training and evaluating a model with different dynamically changing sets of hyperparameters, then selecting and deploying the best model.](/img/guides/airflow-mlops_dynamic_task.png)

- [Setup and teardown](airflow-setup-teardown.md): Airflow allows you to define setup and teardown tasks which create and remove resources used for machine learning. This extends the concept of infrastructure as code to your ML environment, by making the exact state of your environment for a specific ML operation reproducible.

    ![DAG with setup/ teardown tasks creating and tearing down an ML cluster.](/img/guides/airflow-mlops_setup_teardown.png)

- [Branching](airflow-branch-operator.md): Airflow allows you to branch your DAG based on the outcome of a task. You can use this to create different paths in your DAG based on the outcome of a task. For example, you can branch your DAG based on the performance of a model on a test set and only deploy the model if it performs above a certain threshold.

    ![DAG with a branching task deciding whether or not a model is retrained and redeployed.](/img/guides/airflow-mlops_branching.png)

- [Alerts and Notifications](error-notifications-in-airflow.md): Airflow has a wide variety of options to alert you of events in your pipelines, such as DAG or task failures. It is a best practice to set up alerts for critical events in your ML pipelines, such as a drop in model performance or a data quality check failure. Astronomer customers can use [Astro Alerts](https://www.astronomer.io/docs/astro/alerts).

    ![Screenshot of an Astro alert in a Slack channel.](/img/guides/airflow-mlops_alerts.png)

- [Automatic retries](rerunning-dags.md#automatically-retry-tasks): Airflow allows you to configure tasks to automatically retry if they fail according to custom set delays. This feature is critical to protect your pipeline against outages of external tools or rate limits and can be configured at the global, DAG, or the individual task level.

- [Backfills and Reruns](rerunning-dags.md#backfill): In Airflow, you can rerun previous DAG runs and create backfill DAG runs for any historical period. If your DAGs run on increments of time-dimensioned data and are idempotent, you can retroactively change features and create new ones based on historical data. This is a key pattern for creating feature stores containing time-dimensioned features to train and test your models.

### Airflow integrations for MLOps

With Airflow, you can orchestrate actions in any MLOps tool that has an API. Many MLOps tools have integrations available with pre-defined modules like operators, decorators, and hooks to interact with the tool. For example, there are integrations for:

- [AWS SageMaker](airflow-sagemaker.md). A tool to train and deploy machine learning models on AWS.
- [Databricks](airflow-databricks.md). A tool to run Apache Spark workloads.
- [Cohere](airflow-cohere.md). A tool to train and deploy LLMs.
- [OpenAI](airflow-openai.md). A tool to train and deploy large models, including `GPT-4` and `DALL·E 3`.
- [MLFlow](airflow-mlflow.md). An open source tool to track and version data preprocessing and machine learning models.
- [Weights & Biases](airflow-weights-and-biases.md). A tool to track and visualize machine learning experiments.
- [Weaviate](airflow-weaviate.md). An open source vector database.
- [OpenSearch](airflow-opensearch.md). An open source search engine with advanced ML features.
- [Pgvector](airflow-pgvector.md). A extension enabling vector operations in PostgreSQL.
- [Pinecone](airflow-pinecone.md). A vector proprietary database.
- (Beta) [Snowpark](https://registry.astronomer.io/providers/astro-provider-snowflake/versions/latest). A interface to run non-SQL code in Snowflake, includes the machine learning library [Snowpark ML](https://docs.snowflake.com/developer-guide/snowpark-ml/index).
- [Azure ML](https://azure.microsoft.com/en-us/free/machine-learning). A tool to train and deploy machine learning models on Azure.

Additionally, the provider packages for the main cloud providers include modules to interact with their ML tools and compute options:

- [AWS](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest)
- [Azure](https://registry.astronomer.io/providers/apache-airflow-providers-microsoft-azure/versions/latest)
- [Google Cloud](https://registry.astronomer.io/providers/apache-airflow-providers-google/versions/latest)

## Other Resources

To learn more about using Airflow for MLOps, check out the following resources:

- Reference architectures:
    - [Ask Astro: LLM Retrieval Augmented Generation pipeline](https://github.com/astronomer/ask-astro).
- Webinars:
    - [Orchestrate next-generation AI tools: Explore six new Airflow providers](https://www.astronomer.io/events/webinars/orchestrate-next-generation-ai-tools-explore-six-new-airflow-providers/).
    - [Airflow at Faire: Democratizing Machine Learning at Scale](https://www.astronomer.io/events/webinars/airflow-at-faire-democratizing-machine-learning-at-scale/).
    - [Run LLMOps in production with Apache Airflow](https://www.astronomer.io/events/webinars/run-llmops-in-production-with-apache-airflow/).
    - [Power your LLMOps with Airflow’s Weaviate Provider](https://www.astronomer.io/events/webinars/power-your-llmops-with-airflows-weaviate-provider/).
    - [How to use Snowpark with Airflow](https://www.astronomer.io/events/webinars/how-to-use-snowpark-with-airflow/).
    - [How to Orchestrate Machine Learning Workflows with Airflow](https://www.astronomer.io/events/webinars/how-to-orchestrate-machine-learning-workflows-with-airflow/).
    - [Batch Inference with Airflow and SageMaker](https://www.astronomer.io/events/webinars/batch-inference-with-airflow-and-sagemaker/).
    - [Using Airflow with Tensorflow and MLFlow](https://www.astronomer.io/events/webinars/using-airflow-with-tensorflow-mlflow/).
- Blog posts:
    - [Ask Astro: An open source LLM Application with Apache Airflow](https://www.astronomer.io/blog/ask-astro-open-source-llm-application-apache-airflow/).
    - [Day 2 Operations for LLMs with Apache Airflow: Going Beyond the Prototype](https://www.astronomer.io/blog/day-2-operations-for-llms-with-apache-airflow/).
    - [Orchestrating Machine Learning Pipelines with Airflow](https://www.astronomer.io/blog/orchestrating-machine-learning-pipelines-with-airflow/).
    - [Mind the Gap: Seamless data and ML pipelines with Airflow and Metaflow](https://medium.com/apache-airflow/mind-the-gap-seamless-data-and-ml-pipelines-with-airflow-and-metaflow-7e40213dd719).
- Use Cases:
    - [Use Cohere and OpenSearch to analyze customer feedback in an MLOps pipeline](use-case-llm-customer-feedback).
    - [Run an integrated ELT and ML pipeline on Stripe data in Airflow](use-case-elt-ml-finance.md).
    - [Predict possum tail length using MLflow, Airflow, and linear regression](use-case-airflow-mlflow.md).
    - [Use Airflow setup/ teardown to run data quality checks in an MLOps pipeline](use-case-setup-teardown-data-quality.md).
    - [Orchestrate machine learning pipelines with Airflow datasets](use-case-airflow-datasets-multi-team-ml.md).

Astronomer wants to help you succeed with Airflow by continuously creating resources on how to use Airflow for MLOps. If you have any questions or suggestions for additional topics to cover, please contact us in the `#airflow-astronomer` channel in the [Apache Airflow Slack](https://apache-airflow-slack.herokuapp.com/).