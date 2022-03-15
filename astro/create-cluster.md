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

If not specified, we will create a Cluster with two `m5.xlarge` nodes in `us-east-1` by default. For information on all supported regions, configurations, and defaults, see [AWS Resource Reference](resource-reference-aws.md).

From there, your Astronomer representative will provide you with a unique `External ID` for each new Cluster. Make note of this value for the next step.

## Step 2: Edit Your AWS Trust Policy

In the AWS IAM console, [edit the `astronomer-remote-management` trust relationship](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/edit_trust.html) to include trust policies for your new Cluster.

If you only have 1 existing Cluster, you will see the following under **Policy Document**:

```yaml
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
          "sts:ExternalId": "<External-ID-1>"
        }
      }
    }
  ]
}
```

Now, add the External ID that corresponds to your new Cluster to the bottom of the existing trust policy such that the External IDs for all of your Clusters are listed.

For example, your policy for two Astro Clusters might look like the following:

```yaml
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

## Step 3: Confirm with Astronomer

Once you have finished configuring the trust policy, notify Astronomer that you have done so. From here, the Astronomer team will finish creating the Cluster in your AWS account and notify you when it's complete.


Once your Cluster is available, you should be able to create a new Deployment within that cluster. To do so, go to your Workspace and select **Create Deployment** > **Deployment Location**.

For more information, read [creating a new Deployment](configure-deployment.md).
