---
sidebar_label: "Manage clusters"
title: "Manage Astro clusters"
id: manage-clusters
description: View information about clusters in the Cloud UI.
---

Use the Cloud UI to get an overview of your Organization's clusters and retrieve cluster information for Astronomer support.

## View clusters

In the Cloud UI, open the **Clusters** tab. This tab contains information about all clusters in your Organization. The following table contains more information about each available cluster value:

| Value              | Definition                                                                                     |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| Name               | The name of the cluster                                                                        |
| ID                 | The unique ID of the cluster                                                                   |
| Provider           | The type of cloud that the cluster is hosted on                                                |
| Tenant ID          | Azure only. The Azure Active Directory (Azure AD) tenant ID for your cluster                   |
| Account ID         | The ID of the dedicated Astronomer-managed cloud account for your cluster                      |
| Region             | The region your cluster is hosted in                                                           |
| VPC subnet         | The range of IP addresses that can be used to connect to your cluster's VPC                    |
| Pod subnet         | GCP only. The range of IP addresses that can be used to connect to your cluster's Pods         |
| Service subnet     | GCP only. The range of IP addresses that can be used to connect to your cluster's GCP services |
| Service peering    | GCP only. The range of IP addresses that can be used to peer with your cluster's VPC           |
| DB instance type   | The type of instance used for the cluster's metadata database                                  |
| Node instance type | The type of instance used for the cluster's worker nodes                                       |
| Max node count     | The maximum number of worker nodes supported across all Deployments in the cluster             |
| Updated            | The last time a cluster's settings were updated                                                |
| Created            | When the cluster was created                                                                   |
