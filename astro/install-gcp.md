---
sidebar_label: 'Install Astro on GCP'
title: 'Install Astro on GCP'
id: install-gcp
description: Get started on Astro by installing your first Astro Cluster on GCP.
---

## Overview

This guide provides steps for getting started with Astro on your Google Cloud . Below, you'll find instructions for how to complete the Astro install process, including prerequisites and the steps required for our team to provision resources in your network.

## Prerequisites

To install Astro on GCP, you need:

- A clean [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects). For security reasons, the install process is not currently supported on an Google Cloud project that has other tooling running in it.
- A minimum [CPU](https://cloud.google.com/compute/quotas#cpu_quota) quota of 36.
- A minimum [N2_CPU](https://cloud.google.com/compute/quotas#cpu_quota) quota of 24.
- A subscription to the Astro Status Page. This will ensure that you're alerted in the case of an incident or scheduled maintenance.

For more information about the resources required to run Astro on GCP, see [GCP Resource Reference](resource-reference-gcp.md).

### VPC Peering Prerequisites (Optional)

If any of your GCP resources are on a private network, you can access them using one of the following options:

- Private Services Connect
- A VPC Peering connection between Astronomer's VPC and the VPCs for your broader network

If you want to access resources using a VPC peering connection additionally need to provide a CIDR block (RFC 1918 IP Space) no smaller than a `/19` range for each of the following services:

- **Subnet CIDR**: Used by nodes in your GKE cluster
- **Pod CIDR**: Used by GKE pods
- **Service Address CIDR**: Used by GKE services
- **Service VPC Peering**: Used by Private Service Connections

## Step 1: Access Astro

To begin the Astro install process, first create an account at https://cloud.astronomer.io/.

When you first authenticate to Astro, you can sign in with a Google account, a GitHub account, or an email and password.

<div class="text--center">
  <img src="/img/docs/login.png" alt="Astro login screen" />
</div>

If you're the first person from your team to authenticate, the Astronomer team will add you as a Workspace Admin to a new Workspace named after your Organization. From there, you'll be able to add other team members to that Workspace without Astronomer's assistance.

:::tip

After completing your initial installation, we recommend [setting up an identity provider (IdP)](configure-idp.md) so that users can log in to Astro through your IdP.

:::

## Step 2: Activate the Data Plane

The Data Plane in a core component of Astro that runs in your cloud. It's responsible for provisioning, scaling, and managing the resources required to run your Airflow tasks. To activate the Data Plane on your GCP project:

1. Run the following commands in your Google Cloud Shell:

    ```sh
    $ gcloud services enable storage-component.googleapis.com
    $ gcloud services enable storage-api.googleapis.com
    $ gcloud services enable compute.googleapis.com
    $ gcloud services enable container.googleapis.com
    $ gcloud services enable deploymentmanager.googleapis.com
    $ gcloud services enable cloudresourcemanager.googleapis.com
    $ gcloud services enable cloudkms.googleapis.com
    $ gcloud services enable sqladmin.googleapis.com
    $ gcloud services enable servicenetworking.googleapis.com
    ```

    Occasionally, `storage-component.googleapis.com` won't be available after running these commands. If this happens, additionally run the following API call from your Google Cloud Shell:

    ```sh
    $ curl \
    https://storage.googleapis.com/storage/v1/projects/$GOOGLE_CLOUD_PROJECT/serviceAccount \
    --header "Authorization: Bearer `gcloud auth application-default print-access-token`"   \
    --header 'Accept: application/json'   --compressed
    ```

2. Run the following commands in your Google Cloud Shell:

    ```sh
    $ export MY_PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
    $ gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:$MY_PROJECT_NUMBER@cloudservices.gserviceaccount.com --role=roles/owner
    $ gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:astronomer@astro-remote-mgmt-dev.iam.gserviceaccount.com --role=roles/owner
    ```

## Step 3: Provide Setup Information with Astronomer

Provide Astronomer with the following details about your installation:

- Your preferred Astro Cluster name
- The GCP region that you want to host your Cluster in
- Your preferred node instance type
- Your preferred CloudSQL instance type
- Your preferred maximum node count

If you have no preferred values for your first Cluster, Astronomer will create a Cluster with e2-medium-4 nodes, one Medium General Purpose (4vCPU, 16GB) CloudSQL instance, and a maximum node count of 20 in `us-central1`.

For information on all supported regions and configurations, see [GCP Resource Reference](resource-reference-gcp.md).  

:::info

If you need to VPC peer with Astronomer, additionally provide the following information to your Astronomer representative:

- Subnet CIDRs (RFC 1918 IP Space).
- VPC Name/ID and region for peering with Astronomer.
- The IPs of your DNS servers.

You then need to accept a VPC peering request from Astronomer after Astro is installed. To accept the request, follow [Using VPC Network Peering](https://cloud.google.com/vpc/docs/using-vpc-peering) in GCP documentation.

Once VPC peered with Astronomer, configure and validate the following to ensure successful network communications between Astro and your resources:

- Egress Routes on Astronomer Route Table
- [Network ACLs](https://cloud.google.com/storage/docs/access-control/lists) and/or [Security Group](https://cloud.google.com/identity/docs/how-to/update-group-to-security-group) rules of your resources

:::

## Step 4: Let Astronomer Complete the Install

Once you've provided Astronomer with the information for your setup, the Astronomer team will finish the installation of Astro in GCP.

This process can take some time. Wait for confirmation that the installation was successful before proceeding to the next step.

## Step 5: Create a Deployment

Once Astronomer confirms that your Astro Cluster has been created, you are ready to create a Deployment and start deploying DAGs. Log in to [the Cloud UI](https://cloud.astronomer.io) again and [create a new Deployment](configure-deployment.md). If the installation was successful, your new Astro Cluster will be listed as an option under the **Cluster** menu:

<div class="text--center">
  <img src="/img/docs/create-new-deployment-select-cluster.png" alt="Cloud UI New Deployment screen" />
</div>

:::info Connecting Astro Deployments to External GCP Services

By default, all Deployments have [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity) enabled. This means that you can grant your Deployment access to GCP services such as BigQuery via a service account that's automatically created by Astro.

To grant your Deployment access to a GCP service, you need to attach an IAM policy the Deployment's service account. All Deployment service accounts are formatted as follows:

```text
astro-<deployment-namespace>@<gcp-project-name>.iam.gserviceaccount.com
```

You can find a Deployment's namespace in the **Deployments** menu and on the Deployment information screen in the Cloud UI. For example, if your GCP project was called `astronomer-prod-deployment` and your Deployment namespace was `geometrical-gyroscope-9932`, your service account would be:

```text
astro-geometrical-gyroscope-9932@astronomer-prod-deployment.iam.gserviceaccount.com
```

For more information about configuring service accounts on GCP, read [GCP documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to)

:::

## Next Steps

Now that you have an Astro Cluster up and running, take a look at the docs below for information on how to start working in Astro:

- [Set Up an Identity Provider](configure-idp.md)
- [Install CLI](install-cli.md)
- [Configure Deployments](configure-deployment.md)
- [Deploy Code](deploy-code.md)
- [Add Users](add-user.md)
