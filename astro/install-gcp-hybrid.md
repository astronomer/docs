---
sidebar_label: 'GCP'
title: 'Install Astro on GCP'
id: install-gcp-hybrid
description: 'Use this document to complete the installation of Astro Hybrid in Google Cloud Project.'
sidebar_custom_props: { icon: 'img/gcp.png' }
toc_min_heading_level: 2
toc_max_heading_level: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::caution

This document applies only to [Astro Hybrid](hybrid-overview.md). To see whether you're an Astro Hybrid user, click the Astronomer logo in the upper left corner of the Cloud UI and go to **Settings** > **General**. Your Astro product type is listed under **Product Type**.

To get started on Astro Hosted, see [Start a trial](trial.md).

:::

To install Astro Hybrid on GCP, Astronomer support creates a cluster in a dedicated GCP account that's hosted and owned by your organization. This ensures that all data remains within your network and allows your organization to manage infrastructure billing.

To complete the installation, you'll:

- Create an Astronomer account.
- Create a new Google Cloud project.
- Enable Google Cloud APIs and add IAM service account that'll be used by Astro.

Astronomer support will create infrastructure within your Google Cloud project to host the resources and Apache Airflow components necessary to deploy DAGs and execute tasks. If you need more than one Astro cluster, contact [Astronomer support](https://cloud.astronomer.io/support).

## Prerequisites

- A [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) with billing enabled. For security reasons, Google Cloud project with existing infrastructure aren't supported.

- A user with [Owner permissions](https://cloud.google.com/iam/docs/understanding-roles) in your project.

- [Google Cloud Shell](https://cloud.google.com/shell).

- CIDR blocks of with ranges `/19`, `/20`, `/22`, and `/22` are required for the Astro Data Plane. If you don't have any preferred CIDR block, Astro will provision VPCs using a [default CIDR ranges](#vpc-peering-prerequisites-optional). See [GCP resource reference](resource-reference-azure-hybrid.md) for details.

- A minimum [CPU](https://cloud.google.com/compute/quotas#cpu_quota) quota of 48. To adjust your project's quota limits, see [Managing your quota using the Cloud console](https://cloud.google.com/docs/quota#managing_your_quota_console). To view the quota limits for a project, run `gcloud services enable compute.googleapis.com` in the Google Cloud CLI.

- A minimum [N2_CPU](https://cloud.google.com/compute/quotas#cpu_quota) quota of 24. To adjust your project's quota limits, see [Managing your quota using the Cloud console](https://cloud.google.com/docs/quota#managing_your_quota_console). To view the quota limits for a project, run `gcloud services enable compute.googleapis.com` in the Google Cloud CLI.

- A subscription to the [Astro Status Page](https://status.astronomer.io). This ensures that you're alerted when an incident occurs or scheduled maintenance is required.

- The following domains added to your organization's allowlist for any user and CI/CD environments:
    - `https://cloud.astronomer.io/`
    - `https://api.astronomer.io/`
    - `https://images.astronomer.cloud/`
    - `https://auth.astronomer.io/`
    - `https://updates.astronomer.io/`
    - `https://install.astronomer.io/`
    - `https://astro-<your-org>.datakin.com/`
    - `https://<your-org>.astronomer.run/`


### VPC peering prerequisites (optional)

If any of your GCP resources are on a private network, you can access them using one of the following options:

- [Private Services Connect](https://cloud.google.com/vpc/docs/private-service-connect)
- A [VPC Peering connection](https://cloud.google.com/vpc/docs/vpc-peering) between Astronomer's VPC and the VPCs for your broader network

Astro uses four different CIDR blocks to create your Astronomer cluster infrastructure. If you plan on peering with an existing VPC and want to use custom values for your CIDRs, then you must additionally provide your own CIDR ranges (RFC 1918 IP Space) for the following services: 

- **Subnet CIDR**: Used by nodes in your GKE cluster (Default: `172.20.0.0/22`)
- **Pod CIDR**: Used by GKE pods (Default: `172.21.0.0/19`)
- **Service Address CIDR**: Used by GKE services (Default: `172.22.0.0/22`)
- **Service VPC Peering**: Used by Private Service Connections (Default: `172.23.0.0/20`)

The CIDR range sizes must be equal to or greater than the default range sizes for each service.

## Access Astro

1. Go to https://cloud.astronomer.io/ and create an account, or enter your email address, and then click **Continue**.

2. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**.
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in an Organization to authenticate, you're added as a Workspace Admin to a new Workspace named after your Organization. You can add other team members to the Workspace without the assistance of Astronomer support. See [Add a user](add-user.md). To integrate an identity provider (IdP) with Astro, see [Set up an identity provider](configure-idp.md).

## Activate the data plane

The data plane is a collection of infrastructure components for Astro that run in your cloud and are fully managed by Astronomer. This includes a central database, storage for Airflow tasks logs, and the resources required for task execution.

Click the following button to open Google Cloud Shell and run a script to activate the data plane:

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/?cloudshell_git_repo=github.com/astronomer/astro-gcp-onboarding&ephemeral=true&cloudshell_print=README.md)

The script uses your owner role to complete following actions:

- Enable the following required services for running the data plane:

    - `storage.googleapis.com`
    - `storage-component.googleapis.com`
    - `storage-api.googleapis.com`
    - `compute.googleapis.com`
    - `container.googleapis.com`
    - `deploymentmanager.googleapis.com`
    - `cloudresourcemanager.googleapis.com`
    - `cloudkms.googleapis.com`
    - `sqladmin.googleapis.com`
    - `servicenetworking.googleapis.com`
    - `dns.googleapis.com`
    - `servicedirectory.googleapis.com`
- Create a service account called `astronomer@astro-remote-mgmt.iam.gserviceaccount.com` that Astro uses to access the data plane.


## Provide setup information to Astronomer

Once you've activated your data plane, provide Astronomer with:

- Your GCP project ID.
- Your preferred Astro cluster name.
- The GCP region that you want to host your cluster in.
- Your preferred node instance type.
- Your preferred CloudSQL instance type.
- Your preferred maximum node count.
- (_Optional_) Your custom CIDR ranges for connecting to Astronomer's services.

If you don't specify your organization's preferred configurations, Astronomer creates a cluster in `us-central1` with a node pool of `e2-standard-4` nodes. For more information, see [GCP resource reference](resource-reference-gcp-hybrid.md).

### Provide VPC peering information (Optional)

Astro supports [Private Services Connect](https://cloud.google.com/vpc/docs/private-service-connect), which allows private consumption of services across VPC networks that belong to different projects or organizations. If you have created custom services that are not published using Private Services Connect, then you might want to peer with Astronomer. To set up peering, provide the following information to Astronomer:

- VPC Name/ID and region for peering with Astronomer.
- The IPs of your DNS servers.

## Astronomer support creates the cluster

After you provide Astronomer support with the setup information for your organization, Astronomer support creates your first cluster on GCP.

Wait for confirmation from Astronomer support that the cluster has been created before creating a Deployment.

If you submitted a VPC peering request, you'll need to accept the request from Astronomer after Astro is installed. To accept the request, see [Use VPC Network Peering](https://cloud.google.com/vpc/docs/using-vpc-peering).

When VPC peering with Astronomer is complete, configure and validate the following items to ensure successful network communications between Astro and your resources:

- [Egress routes](https://cloud.google.com/vpc/docs/routes#routing_in)
- [Network ACLs](https://cloud.google.com/storage/docs/access-control/lists) or [Security Group](https://cloud.google.com/identity/docs/how-to/update-group-to-security-group) rules of your resources

### Create a Deployment and confirm the install

When Astronomer support confirms that your Astro cluster has been created, you can create a Deployment and start deploying DAGs. See [Create a Deployment](create-deployment.md). 

To confirm a successful installation, in the Cloud UI select a Workspace and on the **Deployments** page click **Deployment**. The Astro cluster created by Astronomer support appears as an option in the **Cluster** list.

## Next steps

- [Set up an identity provider](configure-idp.md)
- [Install the Astro CLI](cli/overview.md)
- [Configure Deployments](configure-deployment-resources.md)
- [Deploy code](deploy-code.md)
- [Add users](add-user.md)
