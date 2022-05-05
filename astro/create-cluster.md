---
sidebar_label: 'Create a Cluster'
title: "Create a New Cluster on Astro"
id: create-cluster
description: Create a new Astro Cluster for your Organization.
---

## Overview

The Astro install process on AWS typically starts with 1 Cluster per Organization. Depending on your use case, however, your team can choose to configure multiple Astro Clusters. This could enable a few benefits, including:

- Clusters in multiple AWS regions
- Different Clusters for Development and Production

Within a single Workspace, you can host Deployments across multiple Clusters. For example, you can have Production Deployments running in your Production Cluster and Development Deployments running in your Development Cluster.

This guide provides instructions for provisioning additional Clusters within your Astro Organization.

## Prerequisites

To complete this setup, you need to have:

- Completed the initial Astro install process as described in [Install on AWS](install-aws.md).
- Permissions to edit trust policies in your AWS account for Astro.

## Step 1: Submit a Request to Astronomer

To create a new Cluster in your Organization, you must first reach out to your Astronomer representative. For each new Cluster that you want to provision, you'll need to provide our team with the following information:

- Your AWS Account ID.
- Your preferred Astro Cluster name.
- The AWS region that you want to host your Cluster in.
- Your preferred node instance type.
- Your preferred max node count (the default is 20).

If not specified, we will create a Cluster with two `m5.xlarge` nodes in `us-east-1` by default. For information on all supported regions, configurations, and defaults, see [AWS Resource Reference](resource-reference-aws.md).

From there, your Astronomer representative will provide you with a unique `External ID` for each new Cluster. Make note of this value for the next step.

## Step 2: Edit Your AWS Trust Policy

In the AWS IAM console, [edit the `astronomer-remote-management` trust relationship](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/edit_trust.html) to include new trust policies and ensure that Astronomer has permission to manage your new Cluster.

To do this, add the External ID that corresponds to your new Cluster to the existing `sts:ExternalId` grouping. For example, your policy for two Astro Clusters might look like the following, with `<External-ID-2>` being the External ID for your new Cluster:

```yaml {14}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::406882777402:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": [
            "<External-ID-1>",
            "<External-ID-2>"
          ]
        }
      }
    }
  ]
}
```

Once you've modified your trust policy, click **Update Trust Policy** in the AWS Console to apply the new trust relationship.

### Additional Setup for AWS Regions that are Disabled by Default

Some AWS regions that Astronomer supports are [disabled by default on AWS](https://docs.aws.amazon.com/general/latest/gr/rande-manage.html#rande-manage-enable). These regions are:

- `af-south-1` - Africa (Cape Town)
- `ap-east-1` - Asia Pacific (Hong Kong)
- `me-south-1` - Middle East (Bahrain)

To create a cluster in one of these regions, complete the following additional setup in your AWS account:

1. In the AWS IAM console, update the `astronomer-remote-management` trust relationship to include permissions for enabling and disabling your desired region as described in the [AWS Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws-enable-disable-regions.html):

    ```YAML
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::406882777402:root"
          },
          "Action": "sts:AssumeRole",
          "Condition": {
            "StringEquals": {
              "sts:ExternalId": [
                "<External-ID-1>",
                "<External-ID-2>"
              ]
            }
          }
        }
        {
            "Sid": "EnableDisableRegion",
            "Effect": "Allow",
            "Action": [
                "account:EnableRegion",
                "account:DisableRegion"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {"account:TargetRegion": "<your-aws-region>"}
            }
        },
        {
            "Sid": "ViewConsole",
            "Effect": "Allow",
            "Action": [
                "aws-portal:ViewAccount",
                "account:ListRegions"
            ],
            "Resource": "*"
        }
      ]
    }
    ```

2. In the AWS Management Console, enable the desired region as described in [AWS documentation](https://docs.aws.amazon.com/general/latest/gr/rande-manage.html#rande-manage-enable).
3. Upgrade your [global endpoint session token](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html#sts-regions-manage-tokens) to version 2, which is valid in all AWS regions, by running the following command via the [AWS CLI](https://aws.amazon.com/cli/):

    ```sh
    aws iam set-security-token-service-preferences --global-endpoint-token-version v2Token
    ```

## Step 3: Confirm with Astronomer

Once you have finished configuring the trust policy, notify Astronomer that you have done so. From here, the Astronomer team will finish creating the Cluster in your AWS account and notify you when it's complete.


Once your Cluster is available, you should be able to create a new Deployment within that cluster. To do so, go to your Workspace and select **Create Deployment** > **Deployment Location**.

For more information, read [creating a new Deployment](configure-deployment.md).
