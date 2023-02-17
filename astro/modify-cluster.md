---
sidebar_label: 'Manage and modify clusters'
title: "Manage and modify clusters"
id: modify-cluster
description: Learn what changes are supported on existing Astro clusters.
---

import PremiumBadge from '@site/src/components/PremiumBadge';

New clusters on Astro are created with a default configuration that is suitable for standard use cases. However, your organization might need modifications to an existing cluster to meet specific business requirements. For example:

- Add a worker type, which creates a new worker node pool in your cluster and allows your team to select that worker type in a Deployment.
- Authorize a Workspace to a cluster, which ensures that your cluster only host Deployments from a specific Workspace or set of Workspaces.
- Create a VPC connection or a transit gateway connection between your Astro cluster and a target VPC.
- Apply custom tags, which can help your team identify your Astro clusters and associate them with a particular purpose or owner within your cloud provider ecosystem. (AWS only)

Most of these modifications can't be completed in the Cloud UI or with the Astro CLI and require you to contact [Astronomer support](https://support.astronomer.io). Cluster modifications typically take only a few minutes to complete and don't require downtime. In these cases, the Airflow UI and Cloud UI continue to be available and your Airflow tasks are not interrupted.

The information provided here will help you determine which modifications you can make to your clusters on Astro and how to request or apply those modifications. For instructions on creating a new cluster, see [Create a cluster](create-cluster.md).

## View clusters

If you don't have a cluster on Astro, see [Install Astro](https://docs.astronomer.io/astro/category/install-astro). If you have an existing cluster and you want to create additional clusters, see [Create a cluster](create-cluster.md).

In the Cloud UI, click the **Clusters** tab to view a list of the clusters owned by your Organization. Click a cluster and then click the **Worker Types**, **Workspace Authorization**, or **Details** tabs to view cluster information including:

- The region for the cluster.
- The cloud provider Account ID associated with the cluster.
- The size and type of the cluster's database.
- When the cluster was created and last updated.

Some of the configurations in the Cloud UI cannot be changed. Only the configurations that are listed in this guide can be modified by your team.

## Manage worker types

A worker type on Astro is a node pool in your cluster that consists of worker nodes of the same node instance type. On Astro, worker nodes execute Airflow tasks. Each worker node pool can be configured with a node instance type and a maximum node count. Contact [Astronomer support](https://support.astronomer.io) with the name of the worker type(s) you want to enable in your cluster. For example, `m6i.2xlarge`.

To confirm a modification was completed, click the **Clusters** tab in the Cloud UI and then click the **Worker Types** tab to view updated configuration information.

## Authorize Workspaces to a Cluster

<PremiumBadge />

As an Organization Owner, you can keep teams and projects isolated by authorizing Workspaces only to specific clusters. You can gain greater control over cloud your resources by ensuring that only authorized pipelines are running on specific clusters.

1. In the Cloud UI, click the **Clusters** tab and then select a cluster.
2. Click the **Workspace Authorization** tab and then click **Edit Workspace Authorization**.
3. Click **Restricted** and select the Workspaces that you want to map to the cluster. 
4. Click **Update**.

After you authorize Workspaces to a cluster, Astro treats the Cluster as restricted. Restricted clusters appear as an option when creating a new Deployment only if the Deployment's Workspace is authorized to the cluster. 

:::info 

A cluster with authorized Workspaces can't host Deployments from any Workspaces that aren't authorized to the cluster. To map Workspaces to a cluster, you must first transfer any existing Deployments on the cluster to one of these Workspace.

Similarly, to unauthorize a Workspace but keep its Deployments in the cluster, you must transfer your Deployments to a Workspace which is still authorized to the cluster. See [Transfer a Deployment to another Workspace](configure-deployment-resources.md#transfer-a-deployment-to-another-workspace).

:::
