---
sidebar_label: 'AWS Cloudwatch'
title: 'Export logs to AWS Cloudwatch'
id: export-cloudwatch
description: "Configure your Deployment to forward observability data to your AWS Cloudwatch instance."
---

By forwarding Astro data to AWS Cloudwatch, you can integrate Astro into your existing observability practices by analyzing information about your Deployments' performance with Cloudwatch monitoring tools. Currently, you can send the following data to AWS Cloudwatch:

- Airflow task logs

Complete the following setup to authenticate your Deployments to AWS Cloudwatch and forward your observability data to your AWS Cloudwatch instance.

:::info

At this time, you can only export Airflow task logs from Astro to Cloudwatch. Metrics exporting is supported only on [Datadog](export-datadog.md).

:::

## Export task logs to AWS CloudWatch

You can forward Airflow task logs from a Deployment to [AWS Cloudwatch](https://aws.amazon.com/cloudwatch/) using an IAM role or user. This allows you to view and manage task logs across all Deployments from a centralized observability plane.

By default, Astro sets a unique log stream for each Deployment, and log groups are defined to include log streams from Deployments which share the same Workspace and cluster. You can override these definitions using Deployment environment variables if you want to change how your task logs are organized on Cloudwatch. See [AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html) for more information about log groups and log streams.

### Prerequisites

- Your Deployment must run Astro Runtime 9 or later. See [Upgrade Astro Runtime](upgrade-runtime.md).

### Setup

1. On AWS, create an IAM role and a trust policy that allows your Deployment to write logs to Cloudwatch. See [Authorize Deployments to your cloud](authorize-deployments-to-your-cloud.md?tab=aws#step-1-authorize-the-deployment-in-your-cloud).
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

    Attach this policy to your IAM role. See [Creating policies using the JSON editor](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html#access_policies_create-json-editor) and [Adding IAM identity permissions (console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console).

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

4. (Optional) Set the following environment variables if you require custom naming for your log streams or log groups. For example, you might set these names to make them more readable for Cloudwatch admins who need to set targeted policies for task logs, or to organize log streams only by cluster instead of cluster and Workspace:

    - **Key 1**: `ASTRO_CLOUDWATCH_TASK_LOGS_LOG_GROUP`
    - **Value 1**: Your log group name.

    - **Key 2**: `ASTRO_CLOUDWATCH_TASK_LOGS_GROUP_STREAM`
    - **Value 2**: Your log stream name.