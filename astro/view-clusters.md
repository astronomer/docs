---
sidebar_label: "View clusters"
title: "View Astro clusters"
id: view-clusters
description: View information about clusters in the Cloud UI.
---

In the Cloud UI, you can view the clusters owned by your Organization and retrieve cluster information that might be required by Astronomer support. All users in your Organization can access this page. 

To make a change to an existing cluster, see [Modify a Cluster](modify-cluster.md).

## View clusters

In the Cloud UI, click the **Clusters** tab to view a list of the clusters owned by your Organization. Click a cluster and then click a tab to view cluster information. 

The following information is provided at the top of the **Clusters** page for quick access: 

| Value              | Description                                                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| ID                 | The ID for the cluster                                                                                                      |
| Cloud Provider     | The cloud provider that hosts the cluster                                                                                   |
| Template           | The template version used to create the cluster                                                                             |
| Updated            | The date and time the cluster's settings were last updated                                                                  |
| Created            | The date and time the cluster was created                                                                                   |

The **Worker Types** tab displays the following information:

| Value              | Description                                                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Node instance type | The instance type used for the cluster's worker nodes                                                                       |
| ID                 | The ID of the cloud provider account that hosts the cluster. This is either an AWS account ID or a Google Cloud project ID  |
| Max node count     | The maximum number of worker nodes supported across all Deployments in the cluster                                          |

The **Workspace Authorization** tab lets you define what Workspaces can create Deployments on the cluster.

The **Tags** tab displays the following information about the custom tags created by Astronomer support:

| Value              | Description                                                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Key                | The custom tag name                                                                                                         |
| Value              | The custom tag value                                                                                                        |

The **Details** tab displays the following information:

| Value              | Description                                                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Name               | The name of the cluster                                                                                                     |
| Account ID         | The AWS account ID, Azure account ID, or Google Cloud project ID of the account that hosts the cluster.                     |
| External IPs       | The public IP addresses for connecting the cluster to external services                                                     |
| Template Version   | The template version used to create the cluster                                                                             |
| Region             | The cloud provider region where the cluster is hosted                                                                       |
| VPC Subnet Range   | The range of IP addresses that can be used to connect to the cluster's VPC                                                  |
| DB Instance Type   | The type of instance used for the cluster's primary database                                                                |

## Related documentation

- [Resources required for Astro on AWS](https://docs.astronomer.io/astro/resource-reference-aws)
- [Resources required for Astro on Azure](https://docs.astronomer.io/astro/resource-reference-azure)
- [Resources required for Astro on GCP](https://docs.astronomer.io/astro/resource-reference-gcp)