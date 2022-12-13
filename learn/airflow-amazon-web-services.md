---
title: "Add AWS user credentials to a local Apache Airflow environment"
sidebar_label: "Authenticate to AWS locally"
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

- A user account on AWS with access to AWS cloud resources

- The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview)
- Optional. Access to a secrets backend hosted on AWS, such as AWS Secrets Manager or AWS Parameter Store

## Step 1:  Retrieve AWS user credentials locally

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

## Step 2: Configure your Astro project


The Astro CLI runs Airflow in a Docker-based environment. To give Airflow access to your credential files, you'll mount them as a volume in Docker.

1. Run the following commands to create an Astro project:

    ```sh
    $ mkdir aws-airflow && cd aws-airflow
    $ astro dev init
    ```

2. Add a file named `docker-compose.override.yml` to your project with the following configuration: 


<Tabs
    defaultValue="mac"
    groupId= "step-2-configure-your-astro-project"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Linux', value: 'linux'},
        {label: 'Windows', value: 'windows'},
    ]}>
<TabItem value="mac">

```yaml
version: "3.1"
services:
    scheduler:
        volumes:
        - /Users/<username>/.aws:/home/astro/.aws:ro
    webserver:
        volumes:
        - /Users/<username>/.aws:/home/astro/.aws:ro
    triggerer:
        volumes:
        - /Users/<username>/.aws:/home/astro/.aws:ro
```

</TabItem>
<TabItem value="linux">

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

Depending on your Docker configurations, you might have to make your `.aws` folder accessible to Docker. To do this, open **Preferences** in Docker Desktop and go to **Resources** -> **File Sharing**. Add the full path of your `.aws` folder to the list of shared folders.

:::

3. In your project's `.env` file, add the following environment variables. Make sure that the volume path is the same as the one you configured in the `docker-compose.override.yml`.


    ```text
    AWS_CONFIG_FILE=/usr/local/airflow/.aws/config
    AWS_SHARED_CREDENTIALS_FILE=/usr/local/airflow/.aws/credentials
    ```

When you run Airflow locally, all AWS connections without defined credentials automatically fall back to your user credentials when connecting to AWS.

## Step 3: Test your credentials with a secrets backend (Optional)


Now that Airflow has access to your user credentials, you can use them to connect to AWS services. Use the following example setup to test your credentials by pulling a variable from AWS Secrets Manager. 

1. Create a secret for an Airflow variable or connection in AWS Secrets Manager. All Airflow variables and connection keys must be prefixed with the following strings respectively:

    - `airflow/variables`
    - `airflow/connections`

    When setting the secret type, choose `Other type of secret` and select the `Plaintext` option. If you're creating a connection URI or a non-dict variable as a secret, remove the brackets and quotations that are pre-populated in the plaintext field.

2. Add the following environment variables to your Astro project `.env` file:

    ```text
    AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
    AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables", "region_name": "<your-aws-region>"}
    ```

4. Run the following command to start Airflow locally:

    ```sh
    astro dev start
    ```

5. Access the Airflow UI at `localhost:8080` and create an Airflow AWS connection named `aws_standard` with no credentials. See [Connections](connections.md).

   When you use this connection in your DAG, it will fall back to using your configured user credentials. 

6. Add a DAG  which uses the secrets backend to your Astro project `dags` directory. You can use the following example DAG to retrieve a value from `airflow/variables` and print it to the terminal:

    ```python
    from airflow import DAG
    from airflow.hooks.base import BaseHook
    from airflow.models import Variable
    from airflow.operators.python import PythonOperator
    from datetime import datetime
    
    def print_var():
        my_var = Variable.get("<your-variable-key>")
        print(f'My variable is: {my_var}')
    
        conn = BaseHook.get_connection(conn_id="aws_standard")
        print(conn.get_uri())
    
    with DAG(
        dag_id='example_secrets_dag',
        start_date=datetime(2022, 1, 1),
        schedule=None
    ):
    
        test_task = PythonOperator(
            task_id='test-task',
            python_callable=print_var
        )

    ```

7. In the Airflow UI, unpause your DAG and click **Play** to trigger a DAG run. 
8. View logs for your DAG run. If the connection was successful, the value of your secret appears in your logs. See [Airflow logging](https://docs.astronomer.io/learn/logging).
