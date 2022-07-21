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

If you don't have a cluster on Astro, follow the instructions to [Install Astro on AWS](install-aws.md) or [GCP](install-gcp.md). If you have an existing cluster and are interested in creating additional clusters, read [Create a cluster](create-cluster.md).

## Supported cluster modifications

Some cluster and Deployment-level modifications can be completed only by Astronomer support. These include:

- [Creating a new cluster](create-cluster.md).
- Deleting a cluster.
- Updating a cluster's worker instance type. See cloud resource references ([AWS](resource-reference-aws.md#deployment-worker-size-limits), [GCP](resource-reference-gcp.md#deployment-worker-size-limits)).
- Updating the maximum node count of an existing cluster.
- [Creating a VPC connection](connect-external-services.md#vpc-peering) between a cluster and a target VPC.
- Running images from a private registry with the [KubernetesPodOperator](kubernetespodoperator#run-images-from-a-private-registry).

## Step 1: Submit a request to Astronomer

To modify an existing cluster in your Organization, first verify that the change you want to make is supported by reading the resource reference documentation for either [AWS](resource-reference-aws.md) or [GCP](resource-reference-gcp.md). Then, reach out to [Astronomer support](https://support.astronomer.io).

## Step 2: Confirm the modification

If the modification you requested is supported, Astronomer will notify you as soon as it's possible to complete the modification.

Modifications to an existing cluster might take a few minutes to complete, but you can expect no downtime during the process. Astro is built to ensure a graceful rollover, which means that the Airflow and Cloud UIs will continue to be available and your Airflow tasks will not be affected.

To confirm that the modification was completed, open the **Clusters** tab in the Cloud UI. You should see the updated configuration in the table entry for your cluster.
