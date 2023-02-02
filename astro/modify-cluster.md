---
sidebar_label: 'Manage and modify clusters'
title: "Manage and modify clusters"
id: modify-cluster
description: Learn what changes are supported on existing Astro clusters.
---

Use the information provided here to manage and modify your existing clusters. To create a new cluster, see [Create a cluster](create-cluster.md).

## View clusters

In the Cloud UI, click the **Clusters** tab to view a list of the clusters owned by your Organization. Click a cluster and then click a tab to view cluster information. 

## Adjust maximum node count

Each Astro cluster has a limit on how many nodes it can run at a time. This limit includes the worker nodes and system nodes managed by Astronomer.

The default maximum node count for all nodes across your cluster is 20. A cluster's node count is most affected by the number of worker Pods that are executing Airflow tasks. See [Worker autoscaling logic](configure-worker-queues.md#worker-autoscaling-logic).

If the node count for your cluster reaches the maximum node count, new tasks might not run or get scheduled. Astronomer support monitors the maximum node count and will contact your organization if it is reached. To check your cluster's current node count, contact [Astronomer Support](https://cloud.astronomer.io/support).

## Create worker node pools

A node pool is a group of nodes within a cluster that all have the same configuration. On Astro, worker nodes are responsible for running the Pods that execute Airflow tasks. Each worker node pool can be configured with a node instance type and a maximum node count. All Astro clusters have one worker node pool by default, but you can configure additional node pools to optimize resource usage.

If your cluster has multiple worker node pools with different worker node instance types, users in your organization can configure tasks to run on those worker types using [worker queues](configure-deployment-resources.md#worker-queues). To enable a new worker type for your cluster, contact [Astronomer support](https://cloud.astronomer.io/support) with a request to create a new node pool or modify an existing node pool.

Astronomer monitors your usage and the number of nodes deployed in your cluster. As your usage of Airflow increases, Astronomer support might contact you and provide recommendations for updating your node pools to optimize your infrastructure spend or increase the efficiency of your tasks.

## Configure your relational database

Astro clusters are created with and require a relational database. A relational database is required for the data plane and it powers the metadata database of all Astro Deployments within a single cluster. During the cluster creation process, you are asked to specify an relational database instance type according to your use case and expected workload. To modify a cluster's database type, contact [Astronomer support](https://cloud.astronomer.io/support).

## Modify a cluster

New clusters on Astro are created with a default configuration that is suitable for standard use cases. However, your organization might need modifications to an existing cluster to meet specific business requirements. 

The following are some of the cluster and Deployment-level modifications that require Astronomer support and can't be completed in the Cloud UI or with the Astro CLI:

- [Create a new cluster](create-cluster.md).
- Delete a cluster.
- Create a new node pool. This enables a new worker type for all Deployments in the cluster. See [Cluster settings reference](https://docs.astronomer.io/astro/category/cluster-settings-reference).
- Update an existing worker node pool, including its node instance type or maximum node count.
- Create a VPC connection or a transit gateway connection between a cluster and a target VPC. See [Connect Astro to external data sources](https://docs.astronomer.io/astro/category/connect-astro).
- Apply custom tags _(AWS only)_

To modify a cluster, you'll need the following:

- A cluster on Astro.
- Permissions to make changes to cluster configurations.

If you don't have a cluster on Astro, see [Install Astro](install-astro.md). If you have an existing cluster and you want to create additional clusters, see [Create a cluster](create-cluster.md). To view the current configuration for a cluster, see [View Astro clusters](view-clusters.md).

### Request and confirm a cluster change

Before you request a change to a cluster, make sure it's supported. To view the default and supported cluster configuration values for your cloud provider, see [Cluster settings reference](https://docs.astronomer.io/astro/category/cluster-settings-reference). After you've confirmed the change you want to make is supported, contact [Astronomer support](https://cloud.astronomer.io/support).

When Astronomer support receives your change request, it will be reviewed and you'll be notified before it's implemented. Most modifications to an existing cluster take only a few minutes to complete and don't require downtime. In these cases, the Airflow UI and Cloud UI continue to be available and your Airflow tasks are not interrupted.

For modifications that do require downtime, such as changing your cluster's node instance type, Astronomer support will inform you of the expected impact and ask you to confirm if you want to proceed.

To confirm a modification was completed, open the **Clusters** tab in the Cloud UI. You should see the updated configuration in the table entry for your cluster.

## Related documentation

- [Create a cluster](create-cluster.md)
- [AWS cluster settings](resource-reference-aws.md)
- [Microsoft Azure cluster settings](resource-reference-azure.md)
- [GCP cluster settings](resource-reference-gcp.md)
