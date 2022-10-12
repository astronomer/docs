---
sidebar_label: 'Modify a cluster'
title: "Modify a cluster on Astro"
id: modify-cluster
description: Request changes to an existing Astro cluster.
---

Unless otherwise specified, new Clusters on Astro are created with a set of default configurations. Depending on your use case, you may decide that you want to modify an existing Cluster to run a different configuration.

For example, if you have a new set of DAGs that require significantly more CPU and Memory than your existing workloads, you might be interested in modifying a cluster on AWS to run `m5.8xlarge` nodes instead of `m5.4xlarge` nodes. You might also want to modify a cluster's maximum node count from the default of 20 to better fit your expected workload.

## Prerequisites

To complete this setup, you need to have:

- A cluster on Astro.
- Permission from your team.

If you don't have a cluster on Astro, see [Install Astro on AWS](install-aws.md), [Install Astro on Azure](install-azure.md), or [GCP](install-gcp.md). If you have an existing cluster and you want to create additional clusters, see [Create a cluster](create-cluster.md). To view your clusters' current configurations, see [Manage clusters](view-clusters.md).

## Supported cluster modifications

Some cluster and Deployment-level modifications require Astronomer support and cannot be completed with the Cloud UI or CLI. These include requests to:

- [Create a new cluster](create-cluster.md).
- Delete a cluster.
- Create a new node pool. This enables a new worker type for all Deployments in the cluster. See resource references for [AWS](resource-reference-aws.md#worker-node-pools), [Azure](resource-reference-azure.md#deployment-worker-node-pools), and [GCP](resource-reference-gcp.md#deployment-worker-node-pools).
- Update an existing worker node pool, including its node instance type or maximum node count.
- Create a VPC connection or a transit gateway connection between a cluster and a target VPC. See [Connect Astro to external data sources](https://docs.astronomer.io/astro/category/connect-astro).

## Step 1: Submit a request to Astronomer

To modify an existing cluster in your Organization, first verify that the change you want to make is supported by reading the resource reference documentation for either [AWS](resource-reference-aws.md) or [GCP](resource-reference-gcp.md). Then, reach out to [Astronomer support](https://cloud.astronomer.io/support).

## Step 2: Confirm the modification

If the modification you requested is supported, Astronomer will notify you as soon as it's possible to complete the modification.

Most modifications to an existing cluster take only a few minutes to complete and do not incur downtime. In these cases, the Airflow UI and Cloud UI continue to be available and your Airflow tasks are not interrupted.

For modifications that do incur downtime, such as changing your cluster's node instance type, Astronomer support will inform you of the expected impact and ask you to confirm if you want to proceed.

To confirm that the modification was completed, open the **Clusters** tab in the Cloud UI. You should see the updated configuration in the table entry for your cluster.
