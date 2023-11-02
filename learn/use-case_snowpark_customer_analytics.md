---
title: "Predict possum tail length using MLflow, Airflow, and linear regression"
description: "Use Airflow and MLflow to conduct and track a regression model."
id: use-case-airflow-mlflow
sidebar_label: "Regression with Airflow + MLflow"
sidebar_custom_props: { icon: 'img/integrations/mlflow.png' }
---

[Snowpark ML](https://docs.snowflake.com/en/developer-guide/snowpark-ml/index) (in public preview) is a python framework for Machine Learning workloads with [Snowpark](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html).  Currently Snowpark ML provides a model registry (storing ML tracking data and models in Snowflake tables and stages), feature engineering primitives similar to scikit-learn (ie. LabelEncoder, OneHotEncoder, etc.) and support for training and deploying [certain model types](https://docs.snowflake.com/en/developer-guide/snowpark-ml/snowpark-ml-modeling#snowpark-ml-modeling-classes) as well as deployments as user-defined functions (UDFs).

This guide demonstrates how to use Apache Airflow to orchestrate a machine learning pipeline leveraging the Snowpark provider and Snowpark ML for feature engineering and model tracking. While Snowpark ML has its own support for models similar to scikit-learn this code demonstrates a "bring-your-own" model approach showing the use of open-source scikit-learn along with Snowpark ML model registry and model serving in an Airflow task rather than Snowpark user-defined function (UDF).  

This demonstration shows how to build a customer analytics dashboard.  Sissy-G Toys is a fictitious online retailer for toys and games.  The GroundTruth customer analytics application provides marketing, sales and product managers with a one-stop-shop for analytics.  The application uses machine learning models for audio transcription, natural language embeddings and sentiment analysis on structured, semi-structured and unstructured data. 

This demo also shows the use of the Snowflake XCOM backend which supports security and governance by serializing all task in/output to Snowflake tables and stages while storing in the Airflow XCOM table a URI pointer to the data.

This workflow includes:
- sourcing structured, unstructured and semistructured data from different systems
- extract, transform and load with [Snowpark Python provider for Airflow](https://github.com/astronomer/astro-provider-snowflake)
- ingest with Astronomer's [python SDK for Airflow](https://github.com/astronomer/astro-sdk)
- audio file transcription with [OpenAI Whisper](https://github.com/openai/whisper)
- natural language embeddings with [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) and the [Weaviate provider for Airflow](https://github.com/astronomer/airflow-provider-weaviate)
- vector search with [Weaviate](https://weaviate.io/)
- sentiment classification with [LightGBM](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html)  
- ML model management with [Snowflake ML](https://docs.snowflake.com/LIMITEDACCESS/snowflake-ml-modeling)
  
All of the above are presented in a [Streamlit](http://www.streamlit.io) application.  

## Before you start

Before trying this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- [Docker Desktop](https://www.docker.com/products/docker-desktop).
- A [Snowflake](https://www.snowflake.com/en/) Account with AccountAdmin permissions
- (Optional) OpenAI account or [Trial Account](https://platform.openai.com/signup)

## Clone the project

Clone the example project from the [Astronomer GitHub](https://github.com/astronomer/use-case-mlflow). To keep your credentials secure when you deploy this project to your own git repository, make sure to create a file called `.env` with the contents of the `.env_example` file in the project root directory. 

