---
title: "Use Airflow Object Storage to interact with cloud storage in an ML pipeline"
sidebar_label: "Object Storage"
description: "Learn how to use Airflow Object Storage."
id: airflow-object-storage-tutorial
---

import CodeBlock from '@theme/CodeBlock';
import object_storage_use_case from '!!raw-loader!../code-samples/dags/airflow-object-storage-tutorial/object_storage_use_case.py';

Airflow 2.8 introduced the [Airflow Object Storage](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/stable/core-concepts/objectstorage.html#object-storage) feature to simplify interaction with different remote and local object storage systems from within your DAGs. 

This tutorial walks you through how to use the Object Storage to interact with files in cloud and local storage in a simple machine learning pipeline training a classifier to predict whether a sentence is more likely to have been said by Captain Kirk or Captain Picard.

:::caution

The Airflow Object Storage is currently considered experimental and might be subject to breaking changes in future releases. For more information see [AIP-58](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=263430565).

:::

## Why use Airflow Object Storage?

Object stores are ubiquitous in modern data pipelines. They are used to store raw data, model-artifacts, image, video, text and audio files, and more. 

The Airflow Object Storage feature allows you to: 

- Interact with object stores in a simple and consistent way from within your DAGs with an abstraction implemented as a [Path API](https://docs.python.org/3/library/pathlib.html). Note that some limitations apply due to the nature of different remote object storage systems, see [Cloud Object Stores are not real file systems](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/stable/core-concepts/objectstorage.html#cloud-object-stores-are-not-real-file-systems).
- Easily switch between different object storage systems without having to change your DAG code.
- Transfer files between different object storage systems without having to reply on XToYTransferOperator operators.
- Transfer large files efficiently, as the Airflow Object Storage feature uses [shutil.copyfileobj()](https://docs.python.org/3/library/shutil.html#shutil.copyfileobj) to stream files in chunks instead of loading them into memory in their entirety.

## Time to complete

This tutorial takes approximately 20 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Task Flow API. See [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- The Basics of [pathlib](https://docs.python.org/3/library/pathlib.html).

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).
- A object storage system to interact with. This tutorial uses [Amazon S3](https://aws.amazon.com/s3/), but you can use [Google Cloud Storage](https://cloud.google.com/storage), [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/) or local file storage as well.

## Step 1: Configure your Astro project

1. Create a new Astro project:

    ```sh
    $ mkdir astro-object-storage-tutorial && cd astro-object-storage-tutorial
    $ astro dev init
    ```

2. Add the following line to your `requirements.txt` file to install the Amazon provider with the `s3fs` extension, as well as the [scikit-learn](https://scikit-learn.org/stable/) package. If you are using Google Cloud Storage or Azure Blob Storage, install the [Google provider](https://registry.astronomer.io/providers/apache-airflow-providers-google/versions/latest) or [Azure provider](https://registry.astronomer.io/providers/apache-airflow-providers-microsoft-azure/versions/latest) instead.

    ```text
    apache-airflow-providers-amazon[s3fs]==8.12.0
    scikit-learn==1.3.2
    ```

3. To create an [Airflow connection](connections.md) to AWS S3, add the following environment variable to your `.env` file. Make sure to replace `<your-aws-access-key-id>` and `<your-aws-secret-access-key>` with your own AWS credentials.

    ```text
    AIRFLOW_CONN_MY_AWS_CONN='{
        "conn_type": "aws",
        "login": "<your-aws-access-key-id>",
        "password": <your-aws-secret-access-key>",
    }'
    ```

## Step 2: Prepare your data

In this example pipeline you will train a classifier to predict whether a sentence is more likely to have been said by Captain Kirk or Captain Picard. The training set consists of 3 quotes from each captain stored in `.txt` files. 

1. Create a new bucket in your S3 account called `astro-object-storage-tutorial`.
2. In the bucket, create a folder called `ingest` with two subfolders `kirk_quotes` and `picard_quotes`.
3. Upload the files from Astronomer's [GitHub repository](https://github.com/astronomer/2-8-example-dags/tree/main/include/ingestion_data_object_store_use_case) into the respective folders.

## Step 3: Create your DAG

1. In your `dags` folder, create a file called `object_storage_use_case.py`.

2. Copy the following code into the file.

    <CodeBlock language="python">{object_storage_use_case}</CodeBlock>

    This DAG uses three different Object Storage locations, which can be aimed at different object storage systems simply by changing the `OBJECT_STORAGE_X`, `PATH_X` and `CONN_ID_X` for each location.

    - `base_path_ingest`: The base path for the ingestion data. This is the path to the training quotes you uploaded in [Step 2](#step-2-prepare-your-data). 
    - `base_path_train`: The base path for the training data, this is the location from which data for training the model will be read.
    - `base_path_archive`: The base path for the archive location where data that has been previously been used for training will be moved to.

    The DAG consists of eight tasks to make a simple MLOps pipeline.

    - The `list_files_ingest` task takes the `base_path_ingest` as an input and iterates through the subfolders `kirk_quotes` and `picard_quotes` to return all files in the folders as individual `ObjectStoragePath` objects.
    - The `copy_files_ingest_to_train` task is [dynamically mapped](dynamic-tasks.md) over the list of files returned by the `list_files_ingest` task. It takes the `base_path_train` as an input and copies the files from the `base_path_ingest` to the `base_path_train` location, providing an example of using Object Storage to transfer files between different object storage systems.
    - The `list_files_train` task lists all files in the `base_path_train` location.
    - The `get_text_from_file` task is dynamically mapped over the list of files returned by the `list_files_train` task to read the text from each file using the `.read_blocks()` method of the `ObjectStoragePath` object. The file name provides the label for the text and both, label and full quote are returned as a dictionary to be passed via [XCom](airflow-passing-data-between-tasks.md) to the next task. 
    - The `train_model` task trains a [Naive Bayes classifier](https://scikit-learn.org/stable/modules/naive_bayes.html) on the data returned by the `get_text_from_file` task. The fitted model is serialized as a base64 encoded string and passed via XCom to the next task.
    - The `use_model` task deserializes the trained model to run a prediction on a user-provided quote, determining whether the quote is more likely to have been said by Captain Kirk or Captain Picard. The prediction is printed to the logs.
    - The `copy_files_train_to_archive` task copies the files from the `base_path_train` to the `base_path_archive` location analogous to the `copy_files_ingest_to_train` task.
    - The `empty_train` task deletes all files from the `base_path_train` location.

    ![Screenshot of the Airflow UI showing the successful completion of the `object_storage_use_case` DAG in the Grid view with the Graph tab selected.](/img/tutorials/airflow-object-storage-tutorial_dag.png)

## Step 4: Run your DAG

1. Run `astro dev start` in your Astro project to start Airflow, then open the Airflow UI at `localhost:8080`.

2. In the Airflow UI, run the `object_storage_use_case` DAG by clicking the play button. Provide any quote you like to the `my_quote` [Airflow param](airflow-params.md).

3. After the DAG run completed, go to the task logs of the `use_model` task to see the prediction made by the model.

```text
[2023-12-11, 00:19:22 UTC] {logging_mixin.py:188} INFO - The quote: 'Time and space are creations of the human mind.'
[2023-12-11, 00:19:22 UTC] {logging_mixin.py:188} INFO - sounds like it could have been said by Picard
```

## Conclusion

Congratulations! You got your first experience using the Airflow Object Storage to interact with files in different locations. To learn more about other methods and capabilities of this feature see the [OSS Airflow documentation](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/stable/core-concepts/objectstorage.html#basic-use).
