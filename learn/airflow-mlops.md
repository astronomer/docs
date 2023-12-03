---
title: "Use Apache Airflow for Machine Learning Operations (MLOps)"
sidebar_label: "MLOps"
description: "Learn best practice patterns to run machine learning in production."
id: airflow-mlops
---

Machine Learning Operations (MLOps) is a rapidly evolving set of best practices and behaviors that allow organizations to run machine learning (ML) models in production. The field of MLOps lies at the intersection of software development operations (DevOps), ML, and data engineering and is a critical component of any data strategy that involves machine learning and artificial intelligence (AI).

In this guide, we'll cover the basics of MLOps and how to use Apache Airflow to implement MLOps best practices. 

## Assumed Knowledge

To get the most out of this guide, you should have an understanding of:

- The basics of Machine Learning.
- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).

## Components of MLOps

MLOps is an umbrella term which is used to describe different patterns in how organizations can productionize machine learning models. [Gift and Deza (2021)](https://www.oreilly.com/library/view/practical-mlops/9781098103002/) coined the "Rule of 25%" for MLOps, suggesting that MLOps consists of:

- 25% DevOps
- 25% Data (Engineering)
- 25% Models
- 25% Business

### DevOps for MLOps

DevOps best practices are based on all aspects of your data and machine learning pipeline being expressed as code and a set of behaviors when interacting with your code base. These behaviors include:

- **Version control**. All code and configuration should be stored in a version control system like [Git](https://git-scm.com/). Version control allows you to track all changes of your ML model and environment over time and roll back to previous versions if needed.
- **Continuous integration/ continuous delivery** ([CI/CD](https://resources.github.com/ci-cd/)). All code undergoes automatic testing, linting and deployment. This ensures that your code is always in a working state and that any changes are automatically deployed to production.
- **Infrastructure as code** ([IaC](https://en.wikipedia.org/wiki/Infrastructure_as_code)). All infrastructure is defined as code and follows the same CI/CD process as your pipeline and model code. This allows you to control and if necessary roll back environment changes as well as quickly deploy new instances of your model. 

### Data Engineering for MLOps

All ML models need data to be trained and perform predictions on. You need a robust data engineering workflows in place in order to confidently train and deploy ML models in production. Special considerations should be given to:

- [**Data quality**](data-quality.md) and data cleaning. Remember the old saying "Garbage in, garbage out"? This is especially true for ML models. If your data is of bad quality, your model predictions will be too. Astronomer recommends to incorporate data quality checks and data cleaning steps into your data pipelines to define and monitor the requirements your data has to fulfill in order for downstream ML operations to be successful.
- **Data preprocessing and feature engineering**. It is common for data to undergo several transformation steps before it is ready to be used as input for an ML model. These steps can include simple [preprocessing steps](https://scikit-learn.org/stable/modules/preprocessing.html) like scaling, one-hot-encoding or imputation of missing values. It can also include more complex steps like [feature selection](https://scikit-learn.org/stable/modules/feature_selection.html#feature-selection), [dimensionality reduction](https://en.wikipedia.org/wiki/Dimensionality_reduction) or [feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html). 
- **Data storage**. 
    - Training and testing data. The best way to store your data highly depends on your data and type of ML. Data engineering includes ingesting data and moving it to the ideal platform for your ML model to access. This can for example be an object storage solution, a relational database management system (RDBMS) or a vector database. 
    - Model artifacts. Model artifacts include model parameters, hyperparameters and other metadata. They are often stored in a specialisied version control system like [MLFlow](airflow-mlflow.md) or [Weights & Biases](airflow-weights-and-biases.md).

Apart from the foundations mentioned above, second day data quality operations in MLOps often include advanced topics like data governance, [data lineage](airflow-openlineage.md) and data cataloging as well as monitoring of data drift.

### Model operations

Once strong DevOps and data engineering foundations are in place you can start to implement the actual ML operations. These include:

![Graph showing different ML operations and how they interrelate.](/img/guides/airflow-mlops_modelling_components.png) 

- Model selection: Decide which model to use. Often this task is performed as part of local testing with a subset of the data by a data scientist.
- **Model training**: Training a machine learning model is the process of using data as input to adjust the parameters of an ML model in order to optimize its performance according to a selected metric, for example accuracy in classification tasks.  
- **Model fine-tuning**: In the age of transfer learning, it is common to use pre-trained models and fine-tune them to your specific use case. Fine-tuning is the process of adjusting the parameters of a pre-trained model to optimize its performance according to a selected metric. You can find many pre-trained models on [HuggingFace](https://huggingface.co/models) or [OpenAI](https://platform.openai.com/docs/models).
- **Model testing**: Before the deploying a model to production you usually want to know how it performs on unseen data. This is called model testing and includes creating predictions on never before seen data and then scoring a model based on chosen metrics.
- **Model versioning**: In order to keep track of changes to your model over time, it is common to version your model. This allows you to roll back to previous versions if needed and to compare different versions of your model.
- **Hyperparameter tuning**: Aside from the parameters of the model itself, there are also hyperparameters which define how a model is trained. For example its learning rate or the number of epochs. Hyperparameter tuning is the process of finding the hyperparameters with which the optimal model can be created for a given dataset.
- **Model deployment**: Once you created a model and are confident on its performance on the test set, you will want to deploy it into production to make it available to other services.
- **Model monitoring**: Models running in production are not static. On one hand their performance might change if the underlying data changes, a phenomenon called data drift. On the other hand you might want to incorporate feedback from users and automatically retrain the model if the performance drops below a certain threshold. Model monitoring is the process of monitoring data drift and model performance and automatically alert stakeholders and/or retrain the model if needed.

### Business

The final component of MLOps is the business side. This component will vary widely depending on your organization and use case and can include:

- **Business strategy**: Defining what ML is used for in an organization and what trade-offs are acceptable. Often, models can be optimized for different metrics, for example high recall or high precision. Often, domain experts are needed to determine the right metrics and model strategy.
- **Model governance**: Creating and following regulations around how machine learning is used in an organization. This often heavily depends on relevant regulations like GDPR or HIPAA.

## How Airflow addresses MLOps challenges

When using Apache Airflow for MLOps there are three main patterns you can follow:

- Using Apache Airflow for ML orchestration (MLOx). Airflow is a tool agnostic orchestrator, which means it can also orchestrate all actions in ML specific tools like [MLFlow](airflow-mlflow.md) or [AWS SageMaker](airflow-sagemaker.md). 
- Combine orchestration of actions in other tools with ML operations running within Airflow. For example you could create vector embeddings in a Python function in Airflow and then use these embeddings to train a model in [Google Datalab](https://cloud.google.com/monitoring/datalab/set-up-datalab).
- Run all your MLOps using Airflow. Since Airflow is able to run any Python code, you can use it as an all-purpose MLOps tool.

### Airflow features for MLOps

There is a set of specific Airflow features that can help you implement MLOps best practices:

- [Setup/ teardown](airflow-setup-teardown.md): Airflow allows you to define setup and teardown tasks which create and tear down resources used for machine learning, extending the concept of infrastructure as code to your ML environment, by making the exact state of your environment for a specific ML operation reproducible.

    ![DAG with setup/ teardown tasks creating and tearing down an ML cluster.](/img/guides/airflow-mlops_setup_teardown.png)

- [Dynamic task mapping](dynamic-tasks.md): In Airflow tasks and task groups can be mapped dynamically at runtime. This allows you to run similar operations in parallel without knowing in advance how many operations will be run in any given DAGrun. For example you could dynamically run a set of model training tasks in parallel, each with different hyperparameters.

    ![DAG with a dynamically mapped task group training and evaluating a model with different dynamically changing sets of hyperparameters, then selecting and deploying the best model.](/img/guides/airflow-mlops_dynamic_task.png)

- [Branching](airflow-branch-operator.md): Airflow allows you to branch your DAG based on the outcome of a task. This allows you to create different paths in your DAG based on the outcome of a task. For example you could branch your DAG based on the performance of a model on a test set and only deploy the model if it performs above a certain threshold.

    ![DAG with a branching task deciding whether or not a model is retrained and redeployed.](/img/guides/airflow-mlops_branching.png)

- [Data driven scheduling](airflow-datasets): With Airflow datasets, DAGs can be scheduled to run once a specific dataset has been updated by any task in the DAG. For example, you can schedule your model training DAG to run once the training dataset has been updated by the data engineering DAG. See also [Orchestrate machine learning pipelines with Airflow datasets](use-case-airflow-datasets-multi-team-ml.md).

    ![Screenshot of the Datasets view showing the dataset_de_dag as the producing DAG to the postgres://prodserver:2319/trainset dataset. The dataset_ml_dag is the consuming DAG.](/img/guides/airflow-mlops_datasets.png) 

### Airflow integrations for MLOps

With Airflow you can orchestrate actions in any MLOps tool that has an API. For many MLOps tools there are integrations available with pre-defined modules like operators, decorators and hooks to interact with the tool. For example, there are integrations for:

- [MLFlow](airflow-mlflow.md). An open source tool to track and version data preprocessing and machine learning models.
- [Weaviate](airflow-weaviate.md). An open source vector database.
- [Weights & Biases](airflow-weights-and-biases.md). A tool to track and visualize machine learning experiments.
- [AWS SageMaker](airflow-sagemaker.md). A tool to train and deploy machine learning models on AWS.
- Snowpark. A interface to run non-SQL code in Snowflake, includes the machine learning library [Snowpark ML](https://docs.snowflake.com/developer-guide/snowpark-ml/index).


## MLOps patterns with Airflow

with code examples


## Resources

To learn more about using Airflow for MLOps, check out the following resources:

- Reference implementations:
    - [Ask Astro a reference LLM implementation](https://github.com/astronomer/ask-astro).
    - [Airflow MLOps customer analytics application: Sissy-G Toys](https://github.com/astronomer/airflow-llm-demo).
- Webinars:
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
- Tutorials:
    - [Train a machine learning model with SageMaker and Airflow](airflow-sagemaker.md).
    - [Use MLflow with Apache Airflow](airflow-mlflow.md).
    - [Orchestrate Weaviate operations with Apache Airflow](airflow-weaviate.md).
    - [Manage your ML models with Weights and Biases and Airflow](airflow-weights-and-biases.md).
- Use Cases:
    - [Run an integrated ELT and ML pipeline on Stripe data in Airflow](use-case-elt-ml-finance.md).
    - [Predict possum tail length using MLflow, Airflow, and linear regression](use-case-airflow-mlflow.md)
    - [Use Airflow setup/ teardown to run data quality checks in an MLOps pipeline](use-case-setup-teardown-data-quality.md)
    - [Orchestrate machine learning pipelines with Airflow datasets](use-case-airflow-datasets-multi-team-ml.md).

At Astronomer our goal is to help you succeed with Airflow. We continuously create resources on how to use Airflow for MLOps. If you have any questions or suggestions for additional topics to cover, please reach out to us in the `#airflow-astronomer` channel in the [Apache Airflow Slack](https://apache-airflow-slack.herokuapp.com/).
