---
sidebar_label: 'Manage and modify clusters'
title: "Manage and modify clusters"
id: modify-cluster
description: Learn what changes are supported on existing Astro clusters.
---

New clusters on Astro are created with a default configuration that is suitable for standard use cases. However, your organization might need modifications to an existing cluster to meet specific business requirements. 

Most cluster and Deployment level modifications can't be completed in the Cloud UI or with the Astro CLI. You'll need to contact [Astronomer Support](https://cloud.astronomer.io/support) to make the following changes:

- [Create a new cluster](create-cluster.md)
- Delete a cluster.
- Create a new node pool. This enables a new worker type for all Deployments in the cluster. See [Cluster settings reference](https://docs.astronomer.io/astro/category/cluster-settings-reference).
- Update an existing worker node pool, including its node instance type or maximum node count.
- Create a VPC connection or a transit gateway connection between a cluster and a target VPC. See [Connect Astro to external data sources](https://docs.astronomer.io/astro/category/connect-astro).
- Apply custom tags _(AWS only)_

When Astronomer support receives your change request, it will be reviewed and you'll be notified before it's implemented.
For modifications that do require downtime, such as changing your cluster's node instance type, Astronomer support will inform you of the expected impact and ask you to confirm if you want to proceed.

Most cluster modifications take only a few minutes to complete and don't require downtime. In these cases, the Airflow UI and Cloud UI continue to be available and your Airflow tasks are not interrupted.

## View your clusters and cluster information

In the Cloud UI, click the **Clusters** tab to view a list of the clusters owned by your Organization. Click a cluster and then click a tab to view cluster information. 

## Manage worker node pools

A node pool is a group of nodes within a cluster that all have the same configuration. On Astro, worker nodes are responsible for running the Pods that execute Airflow tasks. Each worker node pool can be configured with a node instance type and a maximum node count. All Astro clusters have one worker node pool by default, but you can configure additional node pools to optimize resource usage. The following resources are available to help you determine which node pool is suitable for your business needs:

- [Supported AWS worker node pool instance types](resource-reference-aws.md#supported-worker-node-pool-instance-types)
- [Supported Azure worker node pool instance types](resource-reference-azure.md#supported-worker-node-pool-instance-types)
- [Supported GCP worker node pool instance types](resource-reference-gcp.md#supported-worker-node-pool-instance-types)

If your cluster has multiple worker node pools with different worker node instance types, users in your organization can configure tasks to run on those worker types using [worker queues](configure-deployment-resources.md#worker-queues). 

Astronomer monitors your usage and the number of nodes deployed in your cluster. As your usage of Airflow increases, Astronomer support might contact you and provide recommendations for updating your node pools to optimize your infrastructure spend or increase the efficiency of your tasks.

To enable a new worker type for your cluster, contact [Astronomer support](https://cloud.astronomer.io/support) with a request to create a new node pool or modify an existing node pool.

### Adjust maximum node count for worker node pools

Each worker nope pool in a cluster has a limit for how many nodes it can run at a time. If the node count for your cluster reaches the maximum node count, new tasks might not run or get scheduled. Astronomer support monitors the maximum node count and will contact your organization if it is reached. 

The default maximum node count for new node pools is 20. A cluster's node count is most affected by the number of worker Pods that are executing Airflow tasks. See [Worker autoscaling logic](configure-worker-queues.md#worker-autoscaling-logic).

To check the maximum node count for each worker node pool in a Cluster, go to the **Clusters** tab, select a cluster, and click **Worker Types**. To adjust the maximum node count for a node pool, contact [Astronomer Support](https://cloud.astronomer.io/support).

## Configure your relational database

Astro clusters are created with and require a relational database. A relational database is required for the data plane and it powers the metadata database of all Astro Deployments within a single cluster. During the cluster creation process, you are asked to specify an relational database instance type according to your use case and expected workload. 

To modify a cluster's database type, contact [Astronomer support](https://cloud.astronomer.io/support).

## Configure cluster tags (AWS only)

Custom tags help your organization quickly identify and categorize your AWS clusters by purpose, owner, or other business need. For example, you can request tags that help you quickly identify a production or a test cluster, or tags that assist with cost analysis. For more information about tags, see [Tagging your Amazon EKS resources](https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html).

To view existing tags for a cluster, go to the **Clusters** tab, select a cluster, and click **Tags**. To create a new cluster tag, contact [Astronomer support](https://cloud.astronomer.io/support) and provide the key and value for the tag.

## Related documentation

- [Create a cluster](create-cluster.md)
- [AWS cluster settings](resource-reference-aws.md)
- [Microsoft Azure cluster settings](resource-reference-azure.md)
- [GCP cluster settings](resource-reference-gcp.md)
