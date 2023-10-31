---
sidebar_label: 'AWS Cloudwatch'
title: 'Export metrics and logs to AWS Cloudwatch'
id: export-cloudwatch
description: "Configure your Deployment to forward observability data to your AWS Cloudwatch instance."
---

Using AWS Cloudwatch with Astro allows you to observe your Deployments directly from your AWS console. Currently, Astro supports sending the following information to Cloudwatch:

- Airflow task logs

Complete the following setup to authenticate your Deployments to Astro and forward their observability data to your AWS Cloudwatch instance.

## Export task logs to AWS CloudWatch 

You can forward Airflow task logs from a Deployment to [AWS Cloudwatch](https://aws.amazon.com/cloudwatch/) using an IAM role or user. This allows you to view and manage task logs across all Deployments from a centralized observability plane.

### Prerequisites

- Your Deployment must be running Astro Runtime 9.4+. See [Upgrade Astro Runtime](upgrade-runtime.md).

### Setup

1. Create an IAM role and a trust policy that allows your Deployment to write logs to Cloudwatch. See [Authorize Deployments to your cloud](authorize-deployments-to-your-cloud.md?tab=aws#step-1-authorize-the-deployment-in-your-cloud).
2. Create a permissions policy with the following configuration: 

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:DescribeLogStreams"
                ],
                "Resource": "*"
            }
        ]
    }
    ```

    Attach this policy to your IAM role. See [Creating policies using the JSON editor](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html#access_policies_create-json-editor) and [Adding IAM identity permissions (console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console)   

3. Set the following [environment variables](environment-variables.md) in your Deployment:

    - **Key 1**: `ASTRO_CLOUDWATCH_TASK_LOGS_ENABLED`
    - **Value 1**: `True`

    - **Key 2**: `ASTRO_CLOUDWATCH_ROLE_ARN`
    - **Value 2**: The ARN for your IAM role. It should look similar to `arn:aws:iam::123456789012:role/rolename`

    :::info

    If your CloudWatch instance is not in the same region as your Deployment, you must also set the following variable:

    - **Key**: `ASTRO_CLOUDWATCH_AWS_REGION`
    - **Value**: `<your-cloudwatch-region>`

    :::
