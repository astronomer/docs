---
sidebar_label: 'Authorize Workspaces to a cluster'
title: "Authorize Workspaces to a cluster"
id: authorize-workspaces-to-a-cluster
description: Learn how to configure a cluster so that only specific Workspaces can use it.
---

To provide greater control over your cloud resources, you can set a rule so that only specific Workspaces can use a dedicated cluster. For example, you can configure a cluster so that only production-level Workspaces can create Deployments in the cluster.

Use this document to learn restrict a cluster so that only authorized Workspaces can use it.

## Prerequisites

- [Organization Owner](user-permissions.md#organization-roles) permissions.
- A [dedicated cluster](create-dedicated-cluster.md).

## Authorize your workspace

1. In the Cloud UI, click your Workspace name to view more options, then click **Organization Settings**.
2. Click **Clusters** and then select a cluster.
3. Go to the **Workspace Authorization** tab and then click **Edit Workspace Authorization**.
4. Click **Restricted** and select the Workspaces that you want to authorize to the cluster.
5. Click **Update**.

After you authorize Workspaces to a cluster, Astro treats the cluster as restricted. Restricted clusters do not appear in the dedicated cluster drop-down menu within the **Create Deployment** view of Workspaces that have not been authorized.

:::info

A restricted cluster can't host Deployments from an unauthorized Workspace. To restrict a cluster that's currently running Deployments from unauthorized Workspaces, you must transfer the Deployments from these Workspaces to the Workspaces you want to authorize.

Similarly, to unauthorize a Workspace but still keep its Deployments in the cluster, you must transfer your Deployments to a Workspace that is still authorized to the cluster. See [Transfer a Deployment to another Workspace](deployment-settings.md#transfer-a-deployment-to-another-workspace).

:::
