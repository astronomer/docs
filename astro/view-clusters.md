---
sidebar_label: "View clusters"
title: "View Astro clusters"
id: view-clusters
description: View information about clusters in the Cloud UI.
---

Use the Cloud UI to get an overview of your Organization's clusters and retrieve cluster information that may be required by Astronomer support.

For instructions on how to make a change to an existing cluster, see [Modify a Cluster](modify-cluster.md).

## View clusters

In the Cloud UI, click the **Clusters** tab to view information about the clusters in your Organization. The following table provides descriptions for each cluster value.

| Value              | Description                                                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Name               | The name of the cluster                                                                                                     |
| Provider           | The cloud provider that hosts the cluster                                                                            |
| Account ID         | The ID of the cloud provider account that hosts the cluster. This is either an AWS account ID or a Google Cloud project ID |
| Region             | The cloud provider region where the cluster is hosted                                                                       |
| VPC subnet         | The range of IP addresses that can be used to connect to the cluster's VPC                                                  |
| Pod subnet         | GCP only. The range of IP addresses that can be used to connect to the cluster's Pods                                       |
| Service subnet     | GCP only. The range of IP addresses that can be used to connect to the cluster's GCP services                               |
| Service peering    | GCP only. The range of IP addresses that can be used to peer with the cluster's VPC                                         |
| DB instance type   | The type of instance used for the cluster's primary database                                                                |
| Node instance type | The instance type used for the cluster's worker nodes                                                                       |
| Max node count     | The maximum number of worker nodes supported across all Deployments in the cluster                                          |
| External IPs       | The public IP addresses for connecting the cluster to external services                                                         |
| Updated            | The date and time the cluster's settings were last updated                                                                  |
| Created            | The date and time the cluster was created                                                                          |

 All users in your Organization have access to this view. For more information about each value, see [Resources required for Astro on AWS](https://docs.astronomer.io/astro/resource-reference-aws), [Resources required for Astro on Azure](https://docs.astronomer.io/astro/resource-reference-azure), or [Resources required for Astro on GCP](https://docs.astronomer.io/astro/resource-reference-gcp)
