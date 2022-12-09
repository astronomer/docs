---
title: "Authenticate to AWS through Apache Airflow"
sidebar_label: "AWS"
description: "Learn how to connect to a hosted environment on AWS from Apache Airflow. Use AWS credentials to access secrets backends and more from a locally running Airflow environment."
id: airflow-amazon-web-services
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

For initial testing and DAG development, running Airflow with local test data and publicly accessible APIs is often enough. Once you start expanding your Airflow use within your organization, you might need to develop and test DAGs locally with data from your organization's cloud. For example, you might need to test your DAGs using environment variables stored in a secrets backend like AWS Secrets Manager.

You could create access keys for each user developing locally, but service account keys are difficult to track and manage especially on larger teams. Instead, Astronomer recommends exporting credentials for your own AWS account and securely adding these credentials to Airflow. This way, you know which permissions Airflow has without needing to configure a separate access key. 

After you complete this tutorial, you'll be able to: 

- Pull your user credentials from AWS using the AWS CLI.
- Mount your user credentials as a volume when starting Airflow locally.
- Authenticate to AWS through Airflow environment variables that are pulled from your mounted volume.
- Test your credentials by pulling a secret from an AWS secrets backend.

Using these credentials allows you to access information from your AWS cloud, like secret environment variables from AWS Secrets Manager.

## Prerequisites

- An account on AWS.
- The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview)
- Optional. Access to a secrets backend hosted on AWS, such as AWS Secrets Manager or AWS Parameter Store

Step 1:  Retrieve AWS user credentials locally

Run the following command to obtain your user credentials locally:
    
```
aws configure
```    

This command prompts you for your Access Key Id, Secret Access Key, Region, and output format. If you log into AWS using single sign-on (SSO), run `aws configure sso` instead.

The AWS CLI then stores your credentials in two separate files:
    
- `.aws/config`
- `.aws/credentials`

The location of these files depends on your operating system:

- Linux: `/home/<username>/.aws`
- Mac: `/Users/<username>/.aws`
- Windows: `%UserProfile%/.aws`

## Step 2: Configure your Airflow project


The Astro CLI runs Airflow in a Docker-based environment. To give Airflow access to your credential files, you'll mount them as a volume in Docker.

1. Run the following commands to create an Astro project:

    ```sh
    $ mkdir aws-airflow && cd aws-airflow
    $ astro dev init
    ```

2. Add a file named `docker-compose.override.yml` to your project with the following configuration: 


<Tabs
    defaultValue="linuxmac"
    groupId= "configure-your-airflow-project"
    values={[
        {label: 'Linux/ Mac', value: 'linuxmac'},
        {label: 'Windows', value: 'windows'},
    ]}>
<TabItem value="linuxmac">

    ```yaml
    version: "3.1"
    services:
        scheduler:
            volumes:
            - /home/<username>/.aws:/home/astro/.aws:ro
        webserver:
            volumes:
            - /home/<username>/.aws:/home/astro/.aws:ro
        triggerer:
            volumes:
            - /home/<username>/.aws:/home/astro/.aws:ro
    ```
</TabItem>
<TabItem value="windows">

    ```yaml
    version: "3.1"
    services:
        scheduler:
            volumes:
            - /c/Users/<username>/.aws:/home/astro/.aws:ro
        webserver:
            volumes:
            - /c/Users/<username>/.aws:/home/astro/.aws:ro
        triggerer:
            volumes:
            - /c/Users/<username>/.aws:/home/astro/.aws:ro
    ```

</TabItem>
</Tabs>

:::info

Depending on your Docker configurations you might have to add the path to the `.aws` folder to the folders accessible to Docker for mounts. You can do so by opening the Docker Desktop UI and navigating to **Resources** -> **File Sharing**. Add your `.aws` folder with its full file path here. 

:::

3. In your project's `.env` file, add the following environment variables. Make sure that the volume path is the same as the one you configured in the `docker-compose.override.yml`.


    ```
    AWS_CONFIG_FILE=<volume-path>/config
    AWS_SHARED_CREDENTIALS_FILE=<volume-path>/credentials
    ```

The next time you run Airflow, your DAGs will have the same permissions as the user account that you configured in the volume.

## (Optional) Test your credentials with a secrets backend

Now that Airflow has access to your custom credentials, you can use them to connect to AWS services. Use the following example setup to test your credentials by pulling a variable from AWS Secrets Manager. 

1. Create the following directories for Airflow variables and connections in AWS Secrets Manager:

    - `airflow/variables`
    - `airflow/connections`

2. Add a secret to one of these directories. This can be a real or test value. When setting the secret type, choose `Other type of secret` and select the `Plaintext` option. If you're creating a connection URI or a non-dict variable as a secret, remove the brackets and quotations that are pre-populated in the plaintext field.


    Make sure to configure the AIRFLOW__SECRETS__BACKEND_KWARGS environment variables as follows:
    - Remove any mention of `role_arn`.

3. Add the following environment variables to your Astro project `.env` file:

    ```text
    AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables", "region_name": "us-west-2"}
    ```

4. Add a DAG  which uses the secrets backend to your Astro project `dags` directory. You can use the following example DAG to retrieve a value from `airflow/variables` and print it to the terminal:

    ```python
    from airflow import DAG
    from airflow.hooks.base import BaseHook
    from airflow.models import Variable
    from airflow.operators.python import PythonOperator
    from datetime import datetime
    
    def print_var():
        my_var = Variable.get("<your-variable-key>")
        print(f'My variable is: {my_var}')
    
        conn = BaseHook.get_connection(conn_id="<your-connection-key>")
        print(conn.get_uri())
    
    with DAG('example_secrets_dag', start_date=datetime(2022, 1, 1), schedule_interval=None) as dag:
    
      test_task = PythonOperator(
          task_id='test-task',
          python_callable=print_var,
    )
    ```

5. Run the following command to start Airflow locally:

    ```sh
    astro dev start
    ```

6. Access the Airflow UI at `localhost:8080`, unpause your DAG, and click **Play** to trigger a DAG run. 