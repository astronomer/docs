---
sidebar_label: 'Authorize workspaces to a cluster'
title: "Authorize Workspaces to a cluster"
id: authorize-workspaces-to-a-cluster
description: Authorize your workspace to a cluster
---

To provide greater control over your cloud resources, Astro provides you the capability to authorize selective Workspaces to your clusters. This feature is available to Astro Hosted customers using dedicated clusters and Astro Hybrid. For example, you might choose to restrict the dedicated cluster only to your production pipelines within the production Workspace. Meanwhile, your non-production Workspaces can continue to use a standard cluster. 

Use this document to understand how to restrict your cluster to selective Workspaces.

## Prerequisites

- [Organization Owner](user-permissions.md#organization-roles) role
- [A dedicated cluster on Astro Hosted](create-dedicated-cluster.md) or Astro Hybrid

## Authorize your workspace

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**.
2. Click **Clusters** in the left pane and then select a cluster.
3. Go to the **Workspace Authorization** tab and then click **Edit Workspace Authorization**.
4. Click **Restricted** and select the Workspaces that you want to give selective access to the cluster.
5. Click **Update**.

After you authorize Workspaces to a cluster, Astro treats the cluster as restricted. Restricted clusters do not appear in the dedicated cluster drop-down menu within the **Create Deployment** view of Workspaces that have not been authorized.

:::tip important

Note that a restricted cluster can't host Deployments from any non-authorized Workspaces. If your cluster has Deployments running across multiple Workspaces, and you want to restrict to just one Workspace, you must first transfer the existing Deployments from other Workspaces to the Workspace you want to authorize.

Similarly, to unauthorize a Workspace but keep its Deployments in the cluster, you must transfer your Deployments to a Workspace which is still authorized to the cluster. See [Transfer a Deployment to another Workspace](configure-deployment-resources.md#transfer-a-deployment-to-another-workspace).

:::