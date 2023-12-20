---
title: "Train a machine learning model with SageMaker and Airflow"
sidebar_label: "Amazon SageMaker"
description: "Follow a step-by-step tutorial for using Airflow to orchestrate the training and testing of a SageMaker model."
id: airflow-sagemaker
sidebar_custom_props: { icon: 'img/integrations/sagemaker.png' }
---

[Amazon SageMaker](https://aws.amazon.com/sagemaker/) is a comprehensive AWS machine learning (ML) service that is frequently used by data scientists to develop and deploy ML models at scale. With Airflow, you can orchestrate every step of your SageMaker pipeline, integrate with services that clean your data, and store and publish your results using only Python code.

This tutorial demonstrates how to orchestrate a full ML pipeline including creating, training, and testing a new SageMaker model. This use case is relevant if you want to automate the model training, testing, and deployment components of your ML pipeline.

:::tip Other ways to learn

There are multiple resources for learning about this topic. See also:

- Webinar: [Batch Inference with Airflow and SageMaker](https://www.astronomer.io/events/webinars/batch-inference-with-airflow-and-sagemaker/).

:::

## Time to complete

This tutorial takes approximately 60 minutes to complete.

## Assumed knowledge

To get the most out of this tutorial, make sure you have an understanding of:

- The basics of [Amazon S3](https://aws.amazon.com/s3/getting-started/) and [Amazon SageMaker](https://aws.amazon.com/sagemaker/getting-started/).
- Airflow fundamentals, such as writing DAGs and defining tasks. See [Get started with Apache Airflow](get-started-with-airflow.md).
- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow connections. See [Managing your Connections in Apache Airflow](connections.md).

## Prerequisites

To complete this tutorial, you need:

- An AWS account with:

  - Access to an S3 [storage bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html). If you don't already have an account, Amazon offers 5GB of free storage in S3 for 12 months. This should be more than enough for this tutorial.
  - Access to [AWS SageMaker](https://aws.amazon.com/sagemaker/). If you don't already use SageMaker, Amazon offers a free tier for the first month.

- The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started).

## Step 1: Create a role to access SageMaker

For this tutorial, you will need to access SageMaker from your Airflow environment.  There are multiple ways to do this, but for this tutorial you will create an AWS role that can access SageMaker and create temporary credentials for that role.

:::info

If you are uncertain which method you use to connect to AWS, contact your AWS Administrator. These steps may not fit your desired authentication mechanism.

:::

1. From the AWS web console, go to **IAM** service page and create a new execution role for SageMaker. See [Create execution roles](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html#sagemaker-roles-create-execution-role) in the AWS documentation.

2. Add your AWS user and `sagemaker.amazonaws.com` as a trusted entity to the role you just created. See [Editing the trust relationship for an existing role](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/edit_trust.html). Note that this step might not be necessary depending on how IAM roles are managed for your organization's AWS account.

3. Using the ARN of the role you just created, generate temporary security credentials for your role. There are multiple methods for generating the credentials. For detailed instructions, see [Using temporary credentials with AWS resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html). You will need the access key ID, secret access key, and session token in Step 5.

## Step 2: Create an S3 bucket

Create an S3 bucket in the `us-east-2` region that will be used for storing data and model training results. Make sure that your bucket is accessible by the role you created in Step 1. See [Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html).

Note that if you need to create a bucket in a different region than `us-east-2`, you will need to modify the region specified in the environment variables created in Step 3 and in the DAG code in Step 6.

## Step 3: Configure your Astro project

Now that you have your AWS resources configured, you can move on to Airflow setup. Using the Astro CLI:

1. Create a new Astro project:

    ```sh
    $ mkdir astro-sagemaker-tutorial && cd astro-sagemaker-tutorial
    $ astro dev init
    ```

2. Add the following line to the `requirements.txt` file of your Astro project:

    ```text
    apache-airflow-providers-amazon>=5.1.0
    astronomer-providers[amazon]>=1.11.0
    ```

    This installs the AWS provider package which contains relevant S3 and SageMaker modules. It also installs the `astronomer-providers` package, which contains [deferrable](deferrable-operators.md) versions of some SageMaker modules that can help you save costs for long-running jobs. If you use an older version of the AWS provider, some of the DAG configuration in later steps may need to be modified. Deferrable SageMaker operators are not available in older versions of the `astronomer-providers` package.

3. Add the following environment variables to the `.env` file of your project:

    ```text
    AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
    AWS_DEFAULT_REGION=us-east-2
    ```

    These variables ensure that all SageMaker operators will work in your Airflow environment. Some require XCom pickling to be turned on in order to work because they return objects that are not JSON serializable.

4. Run the following command to start your project in a local environment:

    ```sh
    astro dev start
    ```

## Step 4: Add Airflow Variables

Add two Airflow variables that will be used by your DAG. In the Airflow UI, go to **Admin** -> **Variables**.

1. Add a variable with the ARN of the role you created in Step 1.

    - **Key**: `role`
    - **Val**: `<your-role-arn>`

2. Add a variable with the name of the S3 bucket you created in Step 2.

    - **Key**: `s3_bucket`
    - **Val**: `<your-s3-bucket-name>`

## Step 5: Add an Airflow connection to SageMaker

Add a connection that Airflow will use to connect to SageMaker and S3. In the Airflow UI, go to **Admin** -> **Connections**.

Create a new connection named `aws-sagemaker` and choose the `Amazon Web Services` connection type. Fill in the **AWS Access Key ID** and **AWS Secret Access Key** with the access key ID and secret access key you generated in Step 1.

In the **Extra** field, provide your AWS session token generated in Step 1 using the following format:

```text
{
    "aws_session_token": "<your-session-token>"
}
```

:::warning

Your AWS credentials will only last one day using this authentication method. If you return to this step after your credentials have expired, you will need to edit the details in the connection with updated credentials.

:::

Your connection should look like this:

![SageMaker Connection](/img/guides/sagemaker_connection.png)

:::info

As mentioned in Step 1, there are multiple ways of connecting Airflow to AWS resources. If you are using a method other than the one described in this tutorial, such as having your Airflow environment assume an IAM role, you may need to update your connection accordingly.

:::

## Step 6: Create your DAG

In your Astro project `dags/` folder, create a new file called `sagemaker_pipeline.py`. Paste the following code into the file:

```python
"""
This DAG shows an example implementation of machine learning model orchestration using Airflow
and AWS SageMaker. Using the AWS provider's SageMaker operators, Airflow orchestrates getting data
from an API endpoint and pre-processing it (task-decorated function), training the model (SageMakerTrainingOperatorAsync),
creating the model with the training results (SageMakerModelOperator), and testing the model using
a batch transform job (SageMakerTransformOperatorAsync).

The example use case shown here is using a built-in SageMaker K-nearest neighbors algorithm to make
predictions on the Iris dataset. To use the DAG, add Airflow variables for `role` (Role ARN to execute SageMaker jobs) 
then fill in the information directly below with the target AWS S3 locations, and model and training job names.
"""
import textwrap
from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.providers.amazon.aws.operators.sagemaker import SageMakerModelOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from astronomer.providers.amazon.aws.operators.sagemaker import (
    SageMakerTrainingOperatorAsync, 
    SageMakerTransformOperatorAsync
)
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from sagemaker import image_uris

from datetime import datetime
import requests
import io
import pandas as pd
import numpy as np
import os

# Define variables used in configs
data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"  # URL for Iris data API
date = "{{ ts_nodash }}"  # Date for transform job name

input_s3_key = 'iris/processed-input-data'  # Train and test data S3 path
output_s3_key = 'iris/results'  # S3 path for output data
model_name = f"Iris-KNN-{date}"  # Name of model to create
training_job_name = f'train-iris-{date}'  # Name of training job
region = "us-east-2"

with DAG('sagemaker_pipeline',
         start_date=datetime(2022, 1, 1),
         max_active_runs=1,
         schedule=None,
         default_args={'retries': 0, },
         catchup=False,
         doc_md=__doc__
) as dag:
    @task
    def data_prep(data_url, s3_bucket, input_s3_key, aws_conn_id):
        """
        Grabs the Iris dataset from API, splits into train/test splits, and saves CSV's to S3 using S3 Hook
        """
        # Get data from API
        iris_response = requests.get(data_url).content
        columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
        iris = pd.read_csv(io.StringIO(iris_response.decode('utf-8')), names=columns)

        # Process data
        iris['species'] = iris['species'].replace({'Iris-virginica': 0, 'Iris-versicolor': 1, 'Iris-setosa': 2})
        iris = iris[['species', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width']]

        # Split into test and train data
        iris_train, iris_test = np.split(iris.sample(frac=1, random_state=np.random.RandomState()),
                                         [int(0.7 * len(iris))])
        iris_test.drop(['species'], axis=1, inplace=True)

        # Save files to S3
        iris_train.to_csv('iris_train.csv', index=False, header=False)
        iris_test.to_csv('iris_test.csv', index=False, header=False)
        s3_hook = S3Hook(aws_conn_id=aws_conn_id)
        s3_hook.load_file('iris_train.csv', f'{input_s3_key}/train.csv', bucket_name=s3_bucket, replace=True)
        s3_hook.load_file('iris_test.csv', f'{input_s3_key}/test.csv', bucket_name=s3_bucket, replace=True)
        
        # cleanup
        os.remove('iris_train.csv')
        os.remove('iris_test.csv')

    data_prep = data_prep(data_url, "{{ var.value.get('s3_bucket') }}", input_s3_key)

    train_model = SageMakerTrainingOperatorAsync(
        task_id='train_model',
        doc_md=textwrap.dedent("""
        Train the KNN algorithm on the data using the `SageMakerTrainingOperatorAsync`. We use a deferrable version of this operator to save resources on potentially long-running training jobs. The configuration for this operator requires:
        - Information about the algorithm being used.
        - Any required hyper parameters.
        - The input data configuration.
        - The output data configuration.
        - Resource specifications for the machine running the training job.
        - The Role ARN for execution.
        For more information about submitting a training job, check out the [API documentation](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateTrainingJob.html).
        """), 
        aws_conn_id='aws-sagemaker',
        config={
            "AlgorithmSpecification": {
                "TrainingImage": image_uris.retrieve(framework='knn',region=region),
                "TrainingInputMode": "File"
            },
            "HyperParameters": {
                "predictor_type": "classifier",
                "feature_dim": "4",
                "k": "3",
                "sample_size": "150"
            },
            "InputDataConfig": [
                {"ChannelName": "train",
                 "DataSource": {
                     "S3DataSource": {
                         "S3DataType": "S3Prefix",
                         "S3Uri": f"s3://{bucket}/{input_s3_key}/train.csv"
                     }
                 },
                 "ContentType": "text/csv",
                 "InputMode": "File"
                 }
            ],
            "OutputDataConfig": {
                "S3OutputPath": f"s3://{bucket}/{output_s3_key}"
            },
            "ResourceConfig": {
                "InstanceCount": 1,
                "InstanceType": "ml.m5.large",
                "VolumeSizeInGB": 1
            },
            # We are using a Jinja Template to fetch the Role name dynamically at runtime via looking up the Airflow Variable
            "RoleArn": "{{ var.value.get('role') }}",
            "StoppingCondition": {
                "MaxRuntimeInSeconds": 6000
            },
            "TrainingJobName": training_job_name
        },
        wait_for_completion=True
    )

    create_model = SageMakerModelOperator(
        task_id='create_model',
        aws_conn_id='aws-sagemaker',
        doc_md=textwrap.dedent("""
        Create a SageMaker model based on the training results using the `SageMakerModelOperator`. This step creates a model artifact in SageMaker that can be called on demand to provide inferences. The configuration for this operator requires:
        - A name for the model.
        - The Role ARN for execution.
        - The image containing the algorithm (in this case the pre-built SageMaker image for KNN).
        - The S3 path to the model training artifact.
        For more information on creating a model, check out the API documentation [here](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateModel.html).
        """),
        config={
            # We are using a Jinja Template to fetch the Role name dynamically at runtime via looking up the Airflow Variable
            "ExecutionRoleArn": "{{ var.value.get('role') }}",
            "ModelName": model_name,
            "PrimaryContainer": {
                "Mode": "SingleModel",
                "Image": image_uris.retrieve(framework='knn',region=region),
                # We are using a Jinja Template to pull the XCom output of the 'train_model' task to use as input for this task 
                "ModelDataUrl": "{{ ti.xcom_pull(task_ids='train_model')['Training']['ModelArtifacts']['S3ModelArtifacts'] }}"
            },
        }
    )

    test_model = SageMakerTransformOperatorAsync(
        task_id='test_model',
        doc_md=textwrap.dedent("""
        Evaluate the model on the test data created in task 1 using the `SageMakerTransformOperatorAsync`. This step runs a batch transform to get inferences on the test data from the model created in task 3. The DAG uses a deferrable version of `SageMakerTransformOperator` to save resources on potentially long-running transform jobs. The configuration for this operator requires:
        - Information about the input data source.
        - The output results path.
        - Resource specifications for the machine running the training job.
        - The name of the model.
        For more information on submitting a batch transform job, check out the [API documentation](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateTransformJob.html).
        """),
        aws_conn_id='aws-sagemaker',
        config={
            "TransformJobName": f"test-knn-{date}",
            "TransformInput": {
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": f"s3://{bucket}/{input_s3_key}/test.csv"
                    }
                },
                "SplitType": "Line",
                "ContentType": "text/csv",
            },
            "TransformOutput": {
                "S3OutputPath": f"s3://{bucket}/{output_s3_key}"
            },
            "TransformResources": {
                "InstanceCount": 1,
                "InstanceType": "ml.m5.large"
            },
            "ModelName": model_name
        },
    )

    data_prep >> train_model >> create_model >> test_model
```

The graph view of the DAG should look similar to this:

![SageMaker DAG graph](/img/guides/sagemaker_pipeline.png)

This DAG uses the [@task decorator](airflow-decorators.md) and several SageMaker operators to get data from an API endpoint, train a model, create a model in SageMaker, and test the model.  See [How it works](#how-it-works) for more information about each task in the DAG and how the different SageMaker operators work.

## Step 7: Run your DAG to train the model

Go to the Airflow UI, unpause your `sagemaker_pipeline` DAG, and trigger it to train, create and test the model in SageMaker. Note that the `train_model` and `test_model` tasks may take up to 10 minutes each to complete.

In the SageMaker console, you should see your completed training job.

![SageMaker training job](/img/guides/sagemaker_training_job.png)

In your S3 bucket, you will have a folder called `processed-input-data/` containing the processed data from the `data_prep` task, and a folder called `results/` that contains a `model.tar.gz` file with the trained model and a csv with the output of the model testing.

![SageMaker results](/img/guides/sagemaker_s3_results.png)

## How it works

This example DAG acquires and pre-processes data, trains a model, creates a model from the training results, and evaluates the model on test data using a batch transform job. This example uses the [Iris dataset](https://archive.ics.uci.edu/ml/datasets/iris), and trains a built-in SageMaker K-Nearest Neighbors (KNN) model. The general steps in the DAG are:

1. Using a `PythonOperator`, grab the data from the API, complete some pre-processing so the data is compliant with KNN requirements, split into train and test sets, and save them to S3 using the `S3Hook`.

2. Train the KNN algorithm on the data using the `SageMakerTrainingOperatorAsync`. We use a deferrable version of this operator to save resources on potentially long-running training jobs. The configuration for this operator requires:

    - Information about the algorithm being used.
    - Any required hyper parameters.
    - The input data configuration.
    - The output data configuration.
    - Resource specifications for the machine running the training job.
    - The Role ARN for execution.

    For more information about submitting a training job, check out the [API documentation](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateTrainingJob.html).

3. Create a SageMaker model based on the training results using the `SageMakerModelOperator`. This step creates a model artifact in SageMaker that can be called on demand to provide inferences. The configuration for this operator requires:

    - A name for the model.
    - The Role ARN for execution.
    - The image containing the algorithm (in this case the pre-built SageMaker image for KNN).
    - The S3 path to the model training artifact.

    For more information on creating a model, check out the API documentation [here](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateModel.html).

4. Evaluate the model on the test data created in task 1 using the `SageMakerTransformOperatorAsync`. This step runs a batch transform to get inferences on the test data from the model created in task 3. The DAG uses a deferrable version of `SageMakerTransformOperator` to save resources on potentially long-running transform jobs. The configuration for this operator requires:

    - Information about the input data source.
    - The output results path.
    - Resource specifications for the machine running the training job.
    - The name of the model.

    For more information on submitting a batch transform job, check out the [API documentation](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateTransformJob.html).

:::info

To clone the entire repo used to create this tutorial as well as an additional DAG that performs batch inference using an existing SageMaker model, check out the [Astronomer Registry](https://legacy.registry.astronomer.io/dags/sagemaker-pipeline).

:::

In addition to the modules shown in this tutorial, the [AWS provider](https://registry.astronomer.io/providers/amazon) contains multiple other SageMaker operators and sensors that are built on the [SageMaker API](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_Operations_Amazon_SageMaker_Service.html) and cover a wide range of SageMaker features. In general, documentation on what should be included in the configuration of each operator can be found in the corresponding Actions section of the [API documentation](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_Operations.html).

## Conclusion

In this tutorial, you learned how to use Airflow with SageMaker to automate an end-to-end ML pipeline. A natural next step would be to deploy this model to a SageMaker endpoint using the `SageMakerEndpointConfigOperator` and `SageMakerEndpointOperator`, which provisions resources to host the model. In general, the SageMaker modules in the [AWS provider](https://registry.astronomer.io/providers/amazon) allow for many possibilities when using Airflow to orchestrate ML pipelines.
