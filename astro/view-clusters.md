---
sidebar_label: "View clusters"
title: "View Astro clusters"
id: view-clusters
description: View information about clusters in the Cloud UI.
---

In the Cloud UI, the **Clusters** page lists the clusters owned by your Organization. You can click a cluster in the list to retrieve cluster information that might be required by Astronomer support. All users in your Organization can access this page. 

## View clusters

In the Cloud UI, click the **Clusters** tab to view a list of the clusters owned by your Organization. Click a cluster and then click a tab to view cluster information. 

The following information is provided at the top of the **Clusters** page for quick access: 

- **ID**: The ID for the cluster 
- **Cloud Provider**: The cloud provider that hosts the cluster
- **Template**: The template version used to create the cluster
- **Updated**: The date and time the cluster's settings were last updated 
- **Created**: The date and time the cluster was created

The **Worker Types** tab displays the following information:

- **Node Instance Type**: The instance type used for the cluster's worker nodes
- **ID**: The ID of the node instance type used for the cluster's worker nodes
- **Max Node Count**: The maximum number of worker nodes supported across all Deployments in the cluster

The **Workspace Authorization** tab lets you define what Workspaces can create Deployments on the cluster.

The **Tags** tab displays custom tags for the cluster created by Astronomer support.

The **Details** tab displays the following information:

- **Name**: The name of the cluster 
- **Account ID**: The AWS account ID, Azure account ID, or Google Cloud project ID of the account that hosts the cluster
- **External IPs**: The public IP addresses for connecting the cluster to external services 
- **Template Version**: The template version used to create the cluster
- **Region**: The cloud provider region where the cluster is hosted 
- **VPC Subnet Range**: The range of IP addresses that can be used to connect to the cluster's VPC
- **DB Instance Type**: The type of instance used for the cluster's primary database

## Related documentation

- [Modify a Cluster](modify-cluster.md)
- [Resources required for Astro on AWS](https://docs.astronomer.io/astro/resource-reference-aws)
- [Resources required for Astro on Azure](https://docs.astronomer.io/astro/resource-reference-azure)
- [Resources required for Astro on GCP](https://docs.astronomer.io/astro/resource-reference-gcp)