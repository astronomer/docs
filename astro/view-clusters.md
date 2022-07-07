---
sidebar_label: "View clusters"
title: "View Astro clusters"
id: view-clusters
description: View information about clusters in the Cloud UI.
---

Use the Cloud UI to get an overview of your Organization's clusters and retrieve cluster information for use by Astronomer support.

## View clusters

In the Cloud UI, click the **Clusters** tab to view information about the clusters in your Organization. The following table provides descriptions for each cluster value.

| Value              | Description                                                                                     |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| Name               | The name of the cluster                                                                        |
| Provider           | The type of cloud that the cluster is hosted on                                                |
| Account ID         | The ID of the dedicated Astronomer-managed cloud account for the cluster                      |
| Region             | The region where the cluster is hosted in                                                           |
| VPC subnet         | The range of IP addresses that can be used to connect to the cluster's VPC                    |
| Pod subnet         | GCP only. The range of IP addresses that can be used to connect to the cluster's Pods         |
| Service subnet     | GCP only. The range of IP addresses that can be used to connect to the cluster's GCP services |
| Service peering    | GCP only. The range of IP addresses that can be used to peer with the cluster's VPC           |
| DB instance type   | The type of instance used for the cluster's metadata database                                  |
| Node instance type | The type of instance used for the cluster's worker nodes                                       |
| Max node count     | The maximum number of worker nodes supported across all Deployments in the cluster.               |
| Updated            | The last time the cluster's settings were updated                                                |
| Created            | When the cluster was created                                                                   |

For more information about each value, see [AWS resource reference](https://docs.astronomer.io/astro/resource-reference-aws) and [GCP resource reference](https://docs.astronomer.io/astro/resource-reference-gcp)
