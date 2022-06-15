---
sidebar_label: 'Install Astro on GCP'
title: 'Install Astro on GCP'
id: install-gcp
description: Get started on Astro by creating your first Astro Cluster on Google Cloud Platform (GCP).
---

## Overview

This is where you'll find instructions for installing Astro on the Google Cloud Platform (GCP).

To complete the installation process, you'll:

- Create an account on Astro.
- Activate your Astro Data Plane by enabling Google Cloud APIs and adding service accounts to your project's IAM.
- Share information about your Google Cloud project with Astronomer.

When you've completed the installaion process, Astronomer will create a Cluster within your Google Cloud project to host the resources and Apache Airflow components necessary to deploy DAGs and execute tasks.

For more information about managing Google Cloud projects, see [GCP documentation](https://cloud.google.com/resource-manager/docs/creating-managing-projects).

## Prerequisites

- A [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) with billing enabled. For security reasons, the install process is not currently supported on a Google Cloud project that has other tooling running in it.
- A user with [Owner permissions](https://cloud.google.com/iam/docs/understanding-roles) in your project.
- [Google Cloud Shell](https://cloud.google.com/shell).
- A minimum [CPU](https://cloud.google.com/compute/quotas#cpu_quota) quota of 36. To adjust your project's quota limits up or down, see [Managing your quota using the Cloud console](https://cloud.google.com/docs/quota#managing_your_quota_console).
- A minimum [N2_CPU](https://cloud.google.com/compute/quotas#cpu_quota) quota of 24. To adjust your project's quota limits up or down, see [Managing your quota using the Cloud console](https://cloud.google.com/docs/quota#managing_your_quota_console).
- A subscription to the [Astro Status Page](https://status.astronomer.io). This ensures that you're alerted when an incident occurs or scheduled maintenance is required.

For more information about the resources required to run Astro on GCP, see [GCP Resource Reference](resource-reference-gcp.md).

### VPC Peering Prerequisites (Optional)

If any of your GCP resources are on a private network, you can access them using one of the following options:

- [Private Services Connect](https://cloud.google.com/vpc/docs/private-service-connect)
- A [VPC Peering connection](https://cloud.google.com/vpc/docs/vpc-peering) between Astronomer's VPC and the VPCs for your broader network

Astro uses 4 different CIDR blocks for creating the infrastructure for your Astronomer Cluster.  If you plan on peering with an existing VPC and want to use custom values for your CIDRs, then you must additionally provide your own CIDR ranges (RFC 1918 IP Space) of `/19` or better for the following services:

- **Subnet CIDR**: Used by nodes in your GKE cluster (Default: `172.20.0.0/19`)
- **Pod CIDR**: Used by GKE pods (Default: `172.21.0.0/19`)
- **Service Address CIDR**: Used by GKE services (Default: `172.22.0.0/19`)
- **Service VPC Peering**: Used by Private Service Connections (Default: `172.23.0.0/19`)

## Step 1: Access Astro

To get started with Astro, create an account at https://cloud.astronomer.io/.

When you first authenticate to Astro, you can sign in with a Google account, a GitHub account, or an email and password.

<div class="text--center">
  <img src="/img/docs/login.png" alt="Astro login screen" />
</div>

If you're the first person from your team to authenticate, Astronomer adds you as a Workspace Admin to a new Workspace named after your Organization. From there, you'll be able to add other team members to that Workspace without the assistance of Astronomer.

:::tip

After completing your initial installation, we recommend [setting up an identity provider (IdP)](configure-idp.md) so that users can log in to Astro through your IdP.

:::

## Step 2: Activate the Data Plane

The Data Plane is a collection of infrastructure components for Astro that run in your cloud and are fully managed by Astronomer. This includes a central database, storage for Airflow tasks logs, and the resources required for task execution.

To activate the Data Plane on your GCP project:

1. Run the following commands in your Google Cloud Shell:

    ```sh
    gcloud services enable storage-component.googleapis.com
    gcloud services enable storage-api.googleapis.com
    gcloud services enable compute.googleapis.com
    gcloud services enable container.googleapis.com
    gcloud services enable deploymentmanager.googleapis.com
    gcloud services enable cloudresourcemanager.googleapis.com
    gcloud services enable cloudkms.googleapis.com
    gcloud services enable sqladmin.googleapis.com
    gcloud services enable servicenetworking.googleapis.com
    gcloud services enable dns.googleapis.com
    curl \
    https://storage.googleapis.com/storage/v1/projects/$GOOGLE_CLOUD_PROJECT/serviceAccount \
    --header "Authorization: Bearer `gcloud auth application-default print-access-token`"   \
    --header 'Accept: application/json'   --compressed
    ```

2. Run the following commands in your Google Cloud Shell:

    ```sh
    export MY_PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
    gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:$MY_PROJECT_NUMBER@cloudservices.gserviceaccount.com --role=roles/owner
    gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:astronomer@astro-remote-mgmt.iam.gserviceaccount.com --role=roles/owner
    ```

## Step 3: Provide Setup Information to Astronomer

Once you've activated your Data Plane, provide Astronomer with:

- Your preferred Astro Cluster name.
- The GCP region that you want to host your Cluster in.
- Your preferred node instance type.
- Your preferred CloudSQL instance type.
- Your preferred maximum node count.
- (_Optional_) Your custom CIDR ranges for connecting to Astronomer's services.

If you don't specify your organization's preferred configurations, Astronomer creates a Cluster in `us-central1` with default configurations for Astro on GCP. For more information, see [GCP Resource Reference](resource-reference-gcp.md).

:::info

If you need to VPC peer with Astronomer, additionally provide the following information to Astronomer:

- VPC Name/ID and region for peering with Astronomer.
- The IPs of your DNS servers.

You then need to accept a VPC peering request from Astronomer after Astro is installed. To accept the request, follow [Using VPC Network Peering](https://cloud.google.com/vpc/docs/using-vpc-peering) in GCP documentation.

Once VPC peered with Astronomer, configure and validate the following to ensure successful network communications between Astro and your resources:

- [Egress routes](https://cloud.google.com/vpc/docs/routes#routing_in) on Astronomer's route table
- [Network ACLs](https://cloud.google.com/storage/docs/access-control/lists) and/or [Security Group](https://cloud.google.com/identity/docs/how-to/update-group-to-security-group) rules of your resources

:::

## Step 4: Let Astronomer Complete the Install

Once you've provided Astronomer with the information for your setup, Astronomer finishes creating your first Cluster on GCP.

This process can take some time. Wait for confirmation that the installation is successful before proceeding to the next step.

## Step 5: Create a Deployment

When Astronomer confirms that your Astro Cluster has been created, you are ready to create a Deployment and start deploying DAGs. Log in to [the Cloud UI](https://cloud.astronomer.io) again and [create a new Deployment](create-deployment.md). If the installation is successful, your new Astro Cluster is listed as an option below the **Cluster** menu:

<div class="text--center">
  <img src="/img/docs/create-new-deployment-select-cluster.png" alt="Cloud UI New Deployment screen" />
</div>

## Next Steps

Now that you have an Astro Cluster up and running, take a look at the docs below for information on how to start working in Astro:

- [Set Up an Identity Provider](configure-idp.md)
- [Install CLI](cli/get-started.md)
- [Configure Deployments](configure-deployment-resources.md)
- [Deploy Code](deploy-code.md)
- [Add Users](add-user.md)
