---
title: "ML Datasets"
description: "Using Airflow Datasets to create a Producer/Consumer ML pipeline in Airflow "
id: use-case-airflow-ml-datasets
sidebar_label: "Multi-Team ML Pipeline with Airflow Datasets"
---




Airflow plays a pivotal role in machine learning workflows as it provides a robust and scalable platform for orchestrating and managing the entire data pipeline. It facilitates the management of complex ML workflows, handling data dependencies, and ensuring fault tolerance, making it easier for data engineers to handle data inconsistencies, reprocess failed tasks, and maintain the integrity of ML pipelines. 

Many times, ML pipelines are run by two teams in a producer/consumer relationship, where one team produces the clean data for the ML team to consume and use for their models. Airflow datasets and data-driven scheduling can be used to implement this relationship by scheduling the consumer DAG to run only when the producer DAG has completed.

This example has two DAGs with a producer/consumer relationship. One DAG extracts and loads housing data into a local S3FileSystem. A dataset is defined on the load task, and the updating of that dataset triggers a second consumer DAG. The second DAG then takes that data and uses it to train and run a predictive model. This set up has two main advantages. One is that two teams can work independently on their specific sections of the pipeline without needing to coordinate with each other outside of the initial set up. The second is that because the consumer DAG will only trigger once the data arrives, you can avoid the situation where the producer DAG takes longer than expected to complete and leads to the consumer DAG running on incomplete data.

![Figma graph screenshot](/img/examples/usecaseconsumerproducerfigma.png)

The Airflow datasets and their relationships with the two DAGs can be seen in the Airflow datasets view:

![Datasets View screenshot](/img/examples/datasetsview.png)

## Before you start

Before you try this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- [Docker Desktop](https://www.docker.com/products/docker-desktop).

## Clone the project

Clone the example project from the [Astronomer GitHub](https://github.com/astronomer/use-case-produce-consume-ml/tree/main/astromlfinal). 

## Run the project

To run the example project, first make sure Docker Desktop is running. Then, open your project directory and run:

```sh
astro dev start
```

This command builds your project and spins up 6 Docker containers on your machine to run it, the 4 standard airflow components as well as a local minio S3Filesystem and an ML flow instance. After the command finishes, open the Airflow UI at `https://localhost:8080/`, turn on the `astro_ml_producer` and `astro_ml_consumer` DAG's. Then trigger the `astro_ml_producer` DAG using the play button, and the `astro_ml_consumer` DAG will start once the producer DAG has completed. 

![Airflow UI View screenshot](/img/examples/airflowuiview.png)

## Project contents

### Data source

This project uses a [Scikit learn dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html#sklearn.datasets.fetch_california_housing) that contains information on the California housing market. The data is automatically retrieved as part of the DAG, and does not need to be downloaded separately.

### Project code 

This project consists of two DAG's. The [astro_ml_producer_DAG](https://github.com/astronomer/use-case-produce-consume-ml/blob/main/astromlfinal/dags/astro_ml_producer.py) extracts the California Housing dataset from Scikit Learn and builds its model features using the Astro Python SDK [@aql.dataframe](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html) decorator before saving the data to the local S3Filesystem. 
The second [astro_ml_consumer_DAG](https://github.com/astronomer/use-case-produce-consume-ml/blob/main/astromlfinal/dags/astro_ml_consumer.py) then takes this data from the local S3Filesystem, and uses it to train a Scikit linear model, before using the model to generate a prediction, which is then saved to the local S3Filesystem as well. 

#### Producer DAG

The producer DAG, `astro_ml_producer`, has three tasks.

The `extract_housing_data` task imports data from SciKit learn using the fetch_california_housing module, and returns it as a dataframe for the next tasks to use using the Astro SDK [@aql.dataframe](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html) decorator.

```python
    @aql.dataframe(task_id='extract')
    def extract_housing_data() -> DataFrame:
        from sklearn.datasets import fetch_california_housing
        return fetch_california_housing(download_if_missing=True, as_frame=True).frame
```

Then, the `build_features` task uses the Astro SDK [@aql.dataframe](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html) decorator to implement a custom Python function that completes the following:

- The necessary libraries are imported within the function, including `StandardScaler` from scikit-learn, `pandas` for DataFrame operations, dump from joblib for serialization, and `S3FileSystem` from s3fs for interacting with an S3-compatible object storage system.

- Then, An instance of an `S3FileSystem` as FS is created, specifying the access key, secret key, and the endpoint URL of the S3-compatible local storage system. 

- Next, this task performs feature engineering by normalizing the input features using a StandardScaler, calculates metrics based on the scaler mean values, saves the scaler object for later monitoring and evaluation, and returns the normalized feature DataFrame `X` with the target column included.

- Finally, if you look at the task decorator, you'll notice an outlets field that references `Dataset(dataset_uri))`. This creates an Airflow Dataset object called `built_features` that references the normalized feature Dataframe `X` that we stored in the S3Filesystem and sets it as an output of this task. We will then use this Dataset in the scheduling parameter of our `astro_ml_consumer` DAG to trigger it to run once this task is complete

```python
    @aql.dataframe(task_id='featurize', outlets=Dataset(dataset_uri))
    def build_features(raw_df:DataFrame, model_dir:str) -> DataFrame:
        from sklearn.preprocessing import StandardScaler
        import pandas as pd
        from joblib import dump
        from s3fs import S3FileSystem

        fs = S3FileSystem(key='minioadmin', secret='minioadmin', client_kwargs={'endpoint_url': "http://host.docker.internal:9000/"})

        target = 'MedHouseVal'
        X = raw_df.drop(target, axis=1)
        y = raw_df[target]

        scaler = StandardScaler()
        X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
        metrics_df = pd.DataFrame(scaler.mean_, index=X.columns)[0].to_dict()

        #Save scalar for later monitoring and eval
        with fs.open(model_dir+'/scalar.joblib', 'wb') as f:
            dump([metrics_df, scaler], f)

        X[target]=y

        return X
```

Finally, the `save_data_to_s3` task uses the Astro SDK [@aql.export_file](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/export.html) decorator to save the raw California Housing Dataset as `housing.csv` to the local S3Filesystem. It runs in parallel to the `build_features` task, both a clean dataset and a feature engineered dataset are saved. 

```python
    loaded_data = aql.export_file(task_id='save_data_to_s3', 
                                     input_data=extract_df, 
                                     output_file=File(os.path.join(data_bucket, 'housing.csv')), 
                                     if_exists="replace")
```


```

The second DAG, [astro_ml_consumer_DAG](https://github.com/astronomer/use-case-produce-consume-ml/blob/main/astromlfinal/dags/astro_ml_consumer.py), consumes the normalized dataset created by the first DAG and uses it to train a model and execute a prediction on the median house value in California. 

#### Consumer DAG

First, the `built_features` Dataset from the previous DAG is instantiated so that it can be used as a scheduling parameter. This DAG will start when the `built_features` Dataset is updated by the [astro_ml_producer_DAG](https://github.com/astronomer/use-case-produce-consume-ml/blob/main/astromlfinal/dags/astro_ml_producer.py). 

```python
    dataset_uri = "built_features"
    ingestion_dataset = Dataset(dataset_uri)

    @dag(dag_id='astro_ml_consumer', schedule=[Dataset(dataset_uri)], start_date=datetime(2023, 1, 1), catchup=False)
    def astro_ml_consumer():
```

The first task `train_model` in this DAG  uses the Astro SDK [@aql.dataframe](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html) decorator to do the following: 

- The necessary libraries are imported, including RidgeCV from scikit-learn for ridge regression, numpy for numerical operations, dump from joblib for serialization, and S3FileSystem from s3fs for interacting with an S3-compatible object storage system.

- An instance of S3FileSystem is created, specifying the access key, secret key, and the endpoint URL of the S3-compatible storage system.

- The target variable is defined as 'MedHouseVal', which represents the column to be predicted.

- A file containing the feature DataFrame from the previous DAG is opened using the S3 file system (fs.open). The file is located at "s3://local-xcom/wgizkzybxwtzqffq9oo56ubb5nk1pjjwmp06ehcv2cyij7vte315r9apha22xvfd7.parquet".

- The feature DataFrame is read from the opened file using pd.read_parquet and assigned to the variable cleanpanda.

- An instance of RidgeCV is created for ridge regression. The alphas parameter specifies a range of alpha values for regularization.

- The ridge regression model is trained (reg = model.fit(...)) using the features obtained from cleanpanda by dropping the target column and the target values from cleanpanda[target].

- The trained model is serialized and saved to the specified model_dir using the dump function from joblib. The file name for the model is set as 'ridgecv.joblib'.

- The function returns the URI of the saved model file (model_file_uri), which is the concatenation of model_dir and 'ridgecv.joblib'.

```python
    @aql.dataframe(task_id='train')
    def train_model(feature_df:ingestion_dataset, model_dir:str) -> str:
        from sklearn.linear_model import RidgeCV
        import numpy as np
        from joblib import dump
        from s3fs import S3FileSystem

        fs = S3FileSystem(key='minioadmin', secret='minioadmin', client_kwargs={'endpoint_url': "http://host.docker.internal:9000/"})
        
        target = 'MedHouseVal'
        pandasfeature = fs.open("s3://local-xcom/wgizkzybxwtzqffq9oo56ubb5nk1pjjwmp06ehcv2cyij7vte315r9apha22xvfd7.parquet")
        cleanpanda = pd.read_parquet(pandasfeature)

        model = RidgeCV(alphas=np.logspace(-3, 1, num=30))

        reg = model.fit(cleanpanda.drop(target, axis=1), cleanpanda[target ])
        model_file_uri = model_dir+'/ridgecv.joblib'

        with fs.open(model_file_uri, 'wb') as f:
            dump(model, f) 

        return model_file_uri
```

Then, the `predict_housing` task uses the Astro SDK [@aql.dataframe](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/dataframe.html) decorator to load the trained model and feature DataFrame from the local S3FileSystem, make predictions on the features DataFrame, add the predicted values to the feature DataFrame, and return the feature DataFrame with the predicted values included.

```python
    @aql.dataframe(task_id='predict')
    def predict_housing(feature_df:DataFrame, model_file_uri:str) -> DataFrame:
        from joblib import load
        from s3fs import S3FileSystem

        fs = S3FileSystem(key='minioadmin', secret='minioadmin', client_kwargs={'endpoint_url': "http://host.docker.internal:9000/"})
        with fs.open(model_file_uri, 'rb') as f:
            loaded_model = load(f) 
        featdf = fs.open("s3://local-xcom/wgizkzybxwtzqffq9oo56ubb5nk1pjjwmp06ehcv2cyij7vte315r9apha22xvfd7.parquet")
        cleandf = pd.read_parquet(featdf)

        target = 'MedHouseVal'

        cleandf['preds'] = loaded_model.predict(cleandf.drop(target, axis=1))

        return cleandf
```

Finally, the `save_predictions` task uses the Astro SDK [@aql.export_file](https://astro-sdk-python.readthedocs.io/en/stable/astro/sql/operators/export.html) decorator to save the predictions dataframe in the local S3FileSystem. 

```python
    pred_file = aql.export_file(task_id='save_predictions', 
                                     input_data=pred_df, 
                                     output_file=File(os.path.join(data_bucket, 'housing_pred.csv')),
                                     if_exists="replace")
```


## See also

- Tutorial: [How to Write a DAG with the Astro SDK](https://docs.astronomer.io/learn/astro-python-sdk).
- Documentation: [Airflow Datasets Guide](https://docs.astronomer.io/learn/airflow-datasets).
- Webinar: [How to Orchestrate Machine Learning Workflows With Airflow](https://www.astronomer.io/events/webinars/how-to-orchestrate-machine-learning-workflows-with-airflow/).


