---
sidebar_label: AWS S3 bucket
title: Deploy DAGs from an AWS S3 bucket to Astro using AWS Lambda
id: aws-s3
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using AWS S3 and Lambda.
---

Use the following CI/CD template to automate deploying Apache Airflow DAGs from an S3 bucket to Astro using AWS Lambda.

## Prerequisites

- An AWS S3 bucket
- An [Astro Deployment](create-deployment.md) with [DAG-only deploys enabled](deploy-code.md#enable-dag-only-deploys-on-a-deployment).
- A [Deployment API key ID and secret](api-keys.md).
- An [Astro project](create-first-dag.md) containing your project configurations.

### DAG-based deploy

This CI/CD template can be used to deploy DAGs from a single S3 bucket to a single Astro Deployment. When you create or modify a DAG in the S3 bucket, a Lambda function triggers and initialises an `astro` project to deploy your DAGs using Astro CLI.

:::info

To deploy any non-DAG code changes to Astro, you need to trigger a standard image-only deploy with your Astro project. When you do this, your Astro project must include the latest version of your DAGs from your S3 bucket. If your Astro project `dags` folder isn't up to date with your S3 DAGs bucket when you trigger this deploy, you will revert your DAGs back to the version hosted in your Astro project.

:::

1. Download the latest Astro CLI binary from [GitHub releases](https://github.com/astronomer/astro-cli/releases), then rename the file to, `astro_cli.tar.gz`. For example, to use Astro CLI version 1.13.0 in your template, download `astro_1.13.0_linux_amd64.tar.gz` and rename it to `astro_cli.tar.gz`.
2. In your S3 bucket, create the following new folders:

    - `dags`
    - `cli_binary`

3. Add `astro_cli.tar.gz` to `cli_binary`.
4. In the AWS IAM console, [create a new role for AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html#permissions-executionrole-console) with the following permissions:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "lambdacreateloggroup",
                "Effect": "Allow",
                "Action": "logs:CreateLogGroup",
                "Resource": "arn:aws:logs:us-east-1:123456789012:*"
            },
            {
                "Sid": "lambdaputlogevents",
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": [
                    "arn:aws:logs:us-east-1:123456789012:log-group:/aws/lambda/s3_to_astro:*"
                ]
            },
            {
                "Sid": "bucketpermission",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": "arn:aws:s3:::my-demo-bucket"
            }
        ]
    }
    ```

5. Author a new AWS Lambda function from scratch with the following configurations:

    - **Function name**: Any
    - **Runtime**: Python 3.9
    - **Architecture**: Any
    - **Execution role**: Click **Use an existing role** and enter the role you created.

6. Configure the following [Lambda environment variables](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) for your Lambda function:

    `ASTRO_HOME` = `\tmp`
    `ASTRONOMER_KEY_ID` = `<your-deployment-api-key-id>`
    `ASTRONOMER_KEY_SECRET` = `<your-deployment-api-key-secret>`

7. Add the following code to `lambda_function.py`

    ```python

        import boto3
        import subprocess
        import os
        import tarfile

        BUCKET = os.getenv("BUCKET", "astronomer-field-engineering-demo")
        s3 = boto3.resource('s3')

        def untar(filename: str, destination: str) -> None:
            with tarfile.open(filename) as file:
                file.extractall(destination)


        def run_command(cmd: str) -> None:
            p = subprocess.Popen("set -x; " + cmd, shell=True)
            p.communicate()


        def download_to_local(bucket_name: str, s3_folder: str, local_dir: str = None) -> None:
            """
            Download the contents of a folder directory
            Args:
                bucket_name: the name of the s3 bucket
                s3_folder: the folder path in the s3 bucket
                local_dir: a relative or absolute directory path in the local file system
            """
            bucket = s3.Bucket(bucket_name)
            for obj in bucket.objects.filter(Prefix=s3_folder):
                target = obj.key if local_dir is None \
                    else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
                if not os.path.exists(os.path.dirname(target)):
                    os.makedirs(os.path.dirname(target))
                if obj.key[-1] == '/':
                    continue
                bucket.download_file(obj.key, target)
            print("downloaded file")


        def lambda_handler(event, context) -> None:
            """Triggered by a change to a Cloud Storage bucket.
            :param event: Event payload.
            :param context: Metadata for the event.
            """

            base_dir = '/tmp/astro'
            download_to_local(BUCKET, 'mkdemo/dags/', f'{base_dir}/dags')
            download_to_local(BUCKET, 'mkdemo/cli_binary/', base_dir)
            
            os.chdir(base_dir)
            untar('./astro_cli.tar.gz', '.')
            
            run_command('echo y | ./astro dev init')
            run_command('./astro deploy --dags')
            
            return {"statusCode": 200}
    ```
    
8. [Create a trigger](https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html) for your Lambda function with the following configuration:

    - **Source**: Select **S3**.
    - **Bucket**: Select the bucket that contains your `dags` directory.
    - **Event types**: Select **All object create events**.
    - **Prefix**: Enter `dags/`.
    - **Suffix**: Enter `.py`.

9. If you haven't already, deploy your complete Astro project to your Deployment. See [Deploy code](deploy-code.md).
10. Add your DAGs to the `dags` folder in your storage bucket
11. In the Cloud UI, select a Workspace, click **Deployments**, and then select your Deployment. Confirm that your Lambda function worked by checking the Deployment **DAG bundle version**. The version's name should include the time that you added the DAGs to your S3 bucket. 

