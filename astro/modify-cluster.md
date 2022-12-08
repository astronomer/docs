---
sidebar_label: 'Modify a cluster'
title: "Modify a cluster"
id: modify-cluster
description: Learn what changes are supported on existing Astro clusters.
---

New clusters on Astro are created with a default configuration that is suitable for standard use cases. However, your organization might need modifications to an existing cluster to meet specific business requirements. 

The following are some of the cluster and Deployment-level modifications that require Astronomer support and can't be completed in the Cloud UI or with the Astro CLI:

- [Create a new cluster](create-cluster.md).
- Delete a cluster.
- Create a new node pool. This enables a new worker type for all Deployments in the cluster. See [Cluster settings reference](https://docs.astronomer.io/astro/category/cluster-settings-reference).
- Update an existing worker node pool, including its node instance type or maximum node count.
- Create a VPC connection or a transit gateway connection between a cluster and a target VPC. See [Connect Astro to external data sources](https://docs.astronomer.io/astro/category/connect-astro).

To modify a cluster, you'll need the following:

- A cluster on Astro.
- Permissions to make changes to cluster configurations.

If you don't have a cluster on Astro, see [Install Astro](install-astro.md). If you have an existing cluster and you want to create additional clusters, see [Create a cluster](create-cluster.md). To view the current configuration for a cluster, see [View Astro clusters](view-clusters.md).

## Request and confirm a cluster change

Before you request a change to a cluster, make sure it's supported. To view the default and supported cluster configuration values for your cloud provider, see [Cluster settings reference](https://docs.astronomer.io/astro/category/cluster-settings-reference). After you've confirmed the change you want to make is supported, contact [Astronomer support](https://cloud.astronomer.io/support).

When Astronomer support receives your change request, it will be reviewed and you'll be notified before it's implemented. Most modifications to an existing cluster take only a few minutes to complete and don't require downtime. In these cases, the Airflow UI and Cloud UI continue to be available and your Airflow tasks are not interrupted.

For modifications that do require downtime, such as changing your cluster's node instance type, Astronomer support will inform you of the expected impact and ask you to confirm if you want to proceed.

To confirm a modification was completed, open the **Clusters** tab in the Cloud UI. You should see the updated configuration in the table entry for your cluster.
