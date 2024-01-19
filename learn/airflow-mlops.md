---
title: "Best practices for orchestrating MLOps pipelines with Airflow"
sidebar_label: "MLOps"
description: "Learn how to use Airflow to run machine learning in production."
id: airflow-mlops
---

**Machine Learning Operations** (MLOps) is an umbrella term encompassing everything needed to run machine learning models in production. MLOps is a rapidly evolving field with many different best practices and behavioral patterns with Apache Airflow providing tool agnostic orchestration capabilities for all steps.

In this guide you learn:

- How Airflow fits into the MLOps landscape.
- How Airflow can help you implement best practices for different MLOps components.
- Which Airflow features and integrations are especially useful for MLOps.
- Where to find additional resources and reference implementations on using Airflow for MLOps.

:::tip  

Ready to get started? Check out the recommended resources showcasing ML implementations with Airflow:

- [Ask Astro](https://github.com/astronomer/ask-astro) LLM Retrieval Augmented Generation pipeline reference architecture ([Blog post deep dive](https://www.astronomer.io/blog/ask-astro-operationalizing-data-ingest-for-retrieval-augmented-generation-with-llms-part-3/)).
- [The Laurel Algorithm: MLOps, AI, and Airflow for Perfect Timekeeping](https://www.astronomer.io/events/webinars/the-laurel-algorithm-mlops-ai-and-airflow-for-perfect-timekeeping/) webinar.
- [Run an integrated ELT and ML pipeline on Stripe data in Airflow](use-case-elt-ml-finance.md) use case.

:::

## Assumed Knowledge

To get the most benefits from this guide, you need an understanding of:

- The basics of [Machine Learning](https://mlu-explain.github.io/).
- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).

## Why use Airflow for MLOps?

Apache Airflow sits at the heart of the modern MLOps stack. Because it is tool agnostic, Airflow can orchestrate all actions in any MLOps tool that has an API. Combined with already being the de-facto standard for orchestrating data pipelines, Airflow is the perfect tool for data engineers and machine learning engineers to standardize their workflows and collaborate on pipelines.

The benefits of using Airflow for MLOps are:

- **Python native**: You use Python code to define Airflow pipelines, which makes it easy to integrate the most popular machine learning tools and embed your ML operations in a best practice CI/CD workflow. By using the [decorators](airflow-decorators.md) of the TaskFlow API you can turn existing scripts into Airflow tasks.
- **Extensible**: Airflow itself is written in Python, which makes it extensible with [custom modules](airflow-importing-custom-hooks-operators.md) and [Airflow plugins](using-airflow-plugins.md).
- **Monitoring and alerting**: Airflow comes with production-ready monitoring and alerting modules like [Airflow notifiers](error-notifications-in-airflow.md#notifiers), [extensive logging features](logging.md), and [Airflow listeners](airflow-listeners.md). They enable you to have fine-grained control over how you monitor your ML operations and how Airflow alerts you if something goes wrong.
- **Pluggable compute**: When using Airflow you can [pick and choose](#model-operations-and-compute-considerations) the compute you want to use for each task. This allows you to use the the perfect environment and resources for every single action in your ML pipeline. For example, you can run your data engineering tasks on a Spark cluster and your model training tasks on a GPU instance.
- **Data agnostic**: Airflow is data agnostic, which means it can be used to orchestrate any data pipeline, regardless of the data format or storage solution. You can plug in any new data storage, such as the latest vector database or your favorite RDBMS, with minimal effort.
- **Ready for day 2 Ops**: Airflow is a mature orchestrator, coming with built-in functionality such as [automatic retries](rerunning-dags.md#automatically-retry-tasks), complex [dependencies](managing-dependencies.md) and [branching](airflow-branch-operator.md) logic, as well as the option to make pipelines [dynamic](dynamic-tasks.md).
- **Integrations**: Airflow has a large ecosystem of [integrations](https://registry.astronomer.io/providers), including many popular [MLOps tools](#airflow-integrations-for-mlops).
- **Shared platform**: Airflow is used by both data engineers and ML engineers, which allows teams to create direct dependencies between their pipelines, for example by using [Airflow Datasets](airflow-datasets.md).

## Components of MLOps

MLOps describes different patterns in how organizations can productionize machine learning models. [Gift and Deza (2021)](https://www.oreilly.com/library/view/practical-mlops/9781098103002/) coined the _Rule of 25%_ for MLOps, suggesting that MLOps best practices can be divided into four components:

- 25% DevOps
- 25% Data (Engineering)
- 25% Models
- 25% Business

### DevOps for MLOps

Since you define Airflow pipelines in Python code, you can apply DevOps best practices when using Airflow. This includes:

- **Version control**. All code and configuration should be stored in a version control system like [Git](https://git-scm.com/). Version control allows you to track all changes of your pipeline, ML model and environment over time and roll back to previous versions if needed. Astro customers can take advantage of [Deployment rollbacks](https://docs.astronomer.io/astro/deploy-history).
- **Continuous integration/ continuous delivery** ([CI/CD](https://resources.github.com/ci-cd/)). It is a standard Software best practice for all code to undergo automatic testing, linting, and deployment. This ensures that your code is always in a working state and that any changes are automatically deployed to production. Airflow integrates with all major CI/CD tools, see [CI/CD templates](https://docs.astronomer.io/astro/ci-cd-templates/template-overview) for popular templates.
- **Infrastructure as code** ([IaC](https://en.wikipedia.org/wiki/Infrastructure_as_code)). Ideally, all infrastructure is defined as code and follows the same CI/CD process as your pipeline and model code. This allows you to control and, if necessary, roll back environment changes or quickly deploy new instances of your model.

In practice, following modern DevOps patterns when using Airflow for MLOps means:

- Storing all Airflow code and configuration in a version control system like Git. 
- Setting up development, staging, and production branches in your version control system and also connecting them to different Airflow environments. For Astro customers, see [Manage Astro connections in branch-based deploy workflows](https://docs.astronomer.io/astro/astro-use-case/use-case-astro-connections).
- Use automatic testing and linting for all Airflow code before deployment.
- Define all infrastructure as code and use the same CI/CD process for infrastructure as for your Airflow code.
- Store model artifacts in a versioned system. This can be a dedicated tool like MLFlow or an object storage solution.

![Diagram showing how Airflow code and configuration is stored in a version control system and deployed to different Airflow environments.](/img/guides/airflow-mlops_devops.png)

### Data Engineering for MLOps

There is no MLOps without data. You need to have robust data engineering workflows in place in order to confidently train, test, and deploy ML models in production. Apache Airflow has been used by millions of data engineers to create reliable best practice data pipelines, providing a strong foundation for you MLOps workflows.

Give special considerations to the following:

- [**Data quality**](data-quality.md) and data cleaning. If your data is of bad quality, your model predictions will be too. Astronomer recommends incorporating data quality checks and data cleaning steps into your data pipelines to define and monitor the requirements your data has to fulfill in order for downstream ML operations to be successful. Airflow supports integration with any data quality tool that has an API, and has pre-built integrations for tools such as [Great Expectations](airflow-great-expectations.md) and [Soda Core](soda-data-quality.md).
- **Data preprocessing and feature engineering**. It is common for data to undergo several transformation steps before it is ready to be used as input for an ML model. These steps can include simple [preprocessing steps](https://scikit-learn.org/stable/modules/preprocessing.html) like scaling, one-hot-encoding, or imputation of missing values. It can also include more complex steps like [feature selection](https://scikit-learn.org/stable/modules/feature_selection.html#feature-selection), [dimensionality reduction](https://en.wikipedia.org/wiki/Dimensionality_reduction), or [feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html). Airflow allows you to run preprocessing and feature engineering steps in a pythonic way using [Airflow decorators](airflow-decorators.md).
- **Data storage**. 
    - Training and testing data. The best way to store your data highly depends on your data and type of ML. Data engineering includes ingesting data and moving it to the ideal platform for your ML model to access. This can, for example, be an object storage solution, a relational database management system (RDBMS), or a vector database. Airflow integrates with all these options, with tools such as [Airflow object storage](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/objectstorage.html) and the [Astro Python SDK](https://docs.astronomer.io/learn/astro-python-sdk) simplifying common operations. 
    - Model artifacts. Model artifacts include model parameters, hyperparameters, and other metadata. Airflow integrates with specialized version control systems such as [MLFlow](airflow-mlflow.md) or [Weights & Biases](airflow-weights-and-biases.md).

Apart from the foundations mentioned above, second day data quality operations in MLOps often include advanced topics like data governance, [data lineage](airflow-openlineage.md) and data cataloging as well as monitoring of data drift.

In practice, following modern data engineering patterns when using Airflow for MLOps means:

- Following general [Airflow best practices](dag-best-practices.md) for DAG writing, such as keeping tasks atomic and idempotent.
- Using Airflow to orchestrate data ingestion from sources such as APIs, source databases and object storage into a working location for your ML model. This might be a vector database, a relational database, or an object storage solution depending on your use case.
- Incorporating data quality checks into your Airflow pipelines, with critical data quality checks halting the pipeline or alerting you if they fail.
- Using Airflow to orchestrate data preprocessing and feature engineering steps.
- Moving data to permanent cold storage after it has been used for training and testing.

![Diagram showing an example ETL/ELT pipeline for Machine Learning.](/img/guides/airflow-mlops_de.png)

### Model operations and compute considerations

After you establish strong DevOps and data engineering foundations, you can start to implement model operations.

With Airflow you can use your ML tools and compute locations of choice. Some organizations choose to use external compute for all of their heavy workloads, for example:

- **External Kubernetes clusters**: with the [KubernetesPodOperator](kubepod-operator.md) (and its decorator version `@task.kubernetes`).
- **Databricks**: with the [Astro Databricks provider](https://github.com/astronomer/astro-provider-databricks) and [Databricks Airflow provider](https://registry.astronomer.io/providers/apache-airflow-providers-databricks/versions/latest).
- **Spark**: with modules from the [Spark Airflow provider](https://registry.astronomer.io/providers/apache-airflow-providers-apache-spark/versions/latest).
- **External compute**: in [AWS](https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/latest), [Azure](https://registry.astronomer.io/providers/apache-airflow-providers-microsoft-azure/versions/latest) and [Google Cloud](https://registry.astronomer.io/providers/apache-airflow-providers-google/versions/latest) using the respective Airflow providers.

Other Airflow users decide to [scale up](airflow-scaling-workers.md) their Airflow infrastructure with larger worker nodes for compute intensive tasks. Astro customers can leverage the [worker queues](https://docs.astronomer.io/astro/configure-worker-queues) feature, which lets them decide the exact specifications for the workers each task can run on. This means that Airflow only uses large workers for the biggest workloads, saving compute and cost.

In practice, following modern model operations patterns when using Airflow for MLOps means:

- Using Airflow to orchestrate model training, fine-tuning, testing and deployment. 
- Having Airflow tasks monitor the performance of your model and perform automated actions such as re-training, re-deploying, or alerting if the performance drops below a certain threshold.

![Diagram showing different Airflow DAGs relating to model operations in an MLOps pipeline](/img/guides/airflow-mlops_ml_dags.png)

### Business

The final component of MLOps is the business side. This component will vary widely depending on your organization and use case and can include:

- **Business strategy**: Defining what ML is used for in an organization and what trade-offs are acceptable. Often, models can be optimized for different metrics, for example high recall or high precision, and domain experts are needed to determine the right metrics and model strategy. 
- **Model governance**: Creating and following regulations for how your organization uses machine learning. This often depends on relevant regulations like GDPR or HIPAA. Airflow has a built-in integration option with [Open Lineage](airflow-openlineage.md), the open-source standard for tracking data lineage, which is a key component of model governance.

## How Airflow addresses MLOps challenges

When using Apache Airflow for MLOps, there are three main patterns you can follow:

- Using Apache Airflow to orchestrate actions in other MLOps tools. Airflow is a tool agnostic orchestrator, which means it can also orchestrate all actions in ML specific tools like [MLFlow](airflow-mlflow.md) or [AWS SageMaker](airflow-sagemaker.md). 
- Combine orchestration of actions in other tools with ML operations running within Airflow. For example, you can create vector embeddings in a Python function in Airflow and then use these embeddings to train a model in [Google Datalab](https://cloud.google.com/monitoring/datalab/set-up-datalab). Modules like the [`@task.kubernetes`](kubepod-operator.md#use-the-taskkubernetes-decorator) or [`@task.external_python_operator`](external-python-operator) make it easy to run any Python code in isolation with optimized environments and resources.
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

- [Automatic retries](rerunning-dags.md#automatically-retry-tasks): Airflow allows you to configure tasks to automatically retry if they fail according to custom set delays. This feature is critical to protect your pipeline against outages of external tools or rate limits and can be configured at the global, DAG, or the individual task level.

### Airflow integrations for MLOps

With Airflow, you can orchestrate actions in any MLOps tool that has an API. Many MLOps tools have integrations available with pre-defined modules like operators, decorators, and hooks to interact with the tool. For example, there are integrations for:

- [AWS SageMaker](airflow-sagemaker.md). A tool to train and deploy machine learning models on AWS.
- [Databricks](airflow-databricks.md). A tool to run Apache Spark workloads.
- [Cohere](airflow-cohere.md). A tool to train and deploy LLMs.
- [OpenAI](airflow-openai.md). A tool to train and deploy large models, including `GPT4` and `DALLE3`.
- [MLFlow](airflow-mlflow.md). An open source tool to track and version data preprocessing and machine learning models.
- [Weights & Biases](airflow-weights-and-biases.md). A tool to track and visualize machine learning experiments.
- [Weaviate](airflow-weaviate.md). An open source vector database. 
- [OpenSearch](airflow-opensearch.md). An open source search engine with advanced ML features.
- [Pgvector](airflow-pgvector.md). A extension enabling vector operations in PostgreSQL.
- [Pinecone](airflow-pinecone.md). A vector proprietary database.
- (Beta) [Snowpark](https://registry.astronomer.io/providers/astro-provider-snowflake/versions/latest). A interface to run non-SQL code in Snowflake, includes the machine learning library [Snowpark ML](https://docs.snowflake.com/developer-guide/snowpark-ml/index).

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