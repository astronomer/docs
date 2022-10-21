---
sidebar_label: 'Hosted cloud'
title: 'Install Astro on an Astronomer-hosted cloud'
id: hosted-dataplane
description: Get started with Astro on the Astronomer-hosted cloud.
---

This is where you'll find instructions for completing the Astro installation process on the Astronomer-hosted cloud.

Creating Astro clusters on the Astronomer cloud eliminates the need for your organization to manage a dedicated cloud account for Astro. When hosting your environment, Astronomer adheres to industry best practices and standards including the Health Insurance Portability and Accountability Act (HIPAA), Service Organization Control 2 (SOC2), and  General Data Protection Regulation (GDPR). 


## Prerequisites

The setup process assumes that you've already provided Astronomer support with the following information: 

- Your preferred cloud provider. The supported options are: Amazon Web Services (AWS).
- Your preferred cluster installation region. See the supported region lists for [AWS](resource-reference-aws.md#aws-region).
- Optional. Your preferred worker instance type for your first cluster. See [AWS cluster configurations](resource-reference-aws.md#worker-node-types).
- Optional. Your VPC peering requirements for [AWS](install-aws#vpc-peering-prerequisites-optional).
- The email address of your first Astro user.

If you haven't provided this information to Astronomer support, contact your Astronomer representative. 

## Step 1: Astronomer support creates the cluster

Astronomer support creates your first cluster on the Astronomer cloud after you've provided your setup information.

Wait for confirmation that the installation is successful before you access Astro and create a Deployment.

## Step 2: Access Astro

1. Go to https://cloud.astronomer.io/ and create an Astronomer account.

2. Go to `https://cloud.astronomer.io`, enter your email address, and then click **Continue**.

3. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**.
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in an Organization to authenticate, you're added as a Workspace Admin to a new Workspace named after your Organization. You can add other team members to the Workspace without the assistance of Astronomer support. See [Add a user](add-user.md). To integrate an identity provider (IdP) with Astro, see [Set up an identity provider](configure-idp.md).

## Step 3: Create a Deployment

When Astronomer confirms that your Astro cluster has been created, you are ready to create a Deployment and start deploying DAGs. Log in to [the Cloud UI](https://cloud.astronomer.io) again and [create a new Deployment](create-deployment.md). If the installation is successful, your new Astro cluster is listed as an option below the **Cluster** menu:

![Cloud UI New Deployment screen](/img/docs/create-new-deployment-select-cluster.png)

## Next steps

- [Set up an identity provider](configure-idp.md)
- [Install the Astro CLI](cli/overview.md)
- [Configure Deployments](configure-deployment-resources.md)
- [Deploy code](deploy-code.md)
- [Add users](add-user.md)
