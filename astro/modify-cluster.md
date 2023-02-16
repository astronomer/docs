---
sidebar_label: 'Manage and modify clusters'
title: "Manage and modify clusters"
id: modify-cluster
description: Learn what changes are supported on existing Astro clusters.
---

New clusters on Astro are created with a default configuration that is suitable for standard use cases. However, your organization might need to modify an existing cluster to meet certain networking, governance, or use case requirements. For example, you might need to:

- Add a worker type, which creates a new worker node pool in your cluster and allows your team to select that worker type in a Deployment.
- Update an existing worker node pool, including its node instance type or maximum node count.
- Authorize a Workspace to a cluster, which allows you to ensure that your cluster only host Deployments from a specific Workspace or set of Workspaces.
- Create a VPC connection or a transit gateway connection between your Astro cluster and a target VPC.
- Apply custom tags, which can help your team identify your Astro clusters and associate them with a particular purpose or owner within your cloud provider ecosystem. (AWS only)
- Delete an existing cluster.

Most of these modifications can't be completed in the Cloud UI or with the Astro CLI and require you to contact [Astronomer Support](https://cloud.astronomer.io/support). Cluster modifications typically take only a few minutes to complete and don't require downtime. In these cases, the Airflow UI and Cloud UI continue to be available and your Airflow tasks are not interrupted.

Use this guide to determine which modifications you can make to your clusters on Astro and how to request or apply those modifications.

## View clusters

In the Cloud UI, click the **Clusters** tab to view a list of the clusters owned by your Organization. Click a cluster and then click a tab to view cluster information. For example, you can see:

- The region for the cluster.
- The cloud provider Account ID associated with the cluster.
- The size and type of the cluster's database.
- When the cluster was created and last updated.

## Manage worker types

A worker type on Astro is a node pool in your cluster that consists of worker nodes of the same node instance type. On Astro, worker nodes execute Airflow tasks. Each worker node pool can be configured with a node instance type and a maximum node count.

Create or update a worker type on Astro to:

- Allow users in your organization to configure [worker queues](worker-queues.md) and run Airflow tasks with that worker type. For example, a memory-optimized worker node with a certain amount of CPU.
- Limit infrastructure costs by controlling the maximum number of nodes a worker node pool can scale to.

All Astro clusters have one worker type by default, but you can configure up to 30 additional worker types. If you only have one worker type, all tasks across Deployments in your cluster can only run on that type of worker. Individual worker nodes are dedicated to a single Deployment, but a worker node pool can have worker nodes from multiple Deployments. For example, your cluster can have an `m5.2xlarge` node pool with `m5.2xlarge` nodes that each run tasks for different Deployments.

A worker node pool scales to zero if any of the following is true:

- There are no Deployments in your cluster that have worker queues configured with the worker type.
- There are no default worker queues configured with the worker type.

To create or modify a worker type, contact [Astronomer Support](https://cloud.support.astronomer.io).

### Node instance type

Each worker type on Astro is configured with a node instance type. For example, `m5.2xlarge` on AWS, `Standard_D8_v5` on Azure, or `e2-standard-8` on GCP. Node instance types across cloud providers comprise of varying combinations of CPU, memory, storage, and networking capacity. They give you the flexibility to choose the appropriate balance of resources that your Airflow tasks need.

Using the capacity of a worker node in your tasks and DAGs depends on which executor your Deployment is configured with. With the Celery executor, each worker node runs a single worker Pod. A worker Pod's actual available size is equivalent to the total capacity of the instance type minus Astro’s system overhead. With the Kubernetes executor, each worker node can run an unlimited number of Pods as long as the sum of all requests from each Pod doesn't exceed the total capacity of the node minus Astro's system overhead.

For the list of worker types available on Astro, see [AWS](resource-reference-aws.md#worker-node-pools), [Azure](resource-reference-azure.md#worker-node-pools), or [GCP](resource-reference-gcp.md#worker-node-pools).

### Maximum node count

Each worker node pool on Astro must be configured with a **Maximum Node Count**, which represents the maximum total number of nodes that a worker node pool can have at any given time across Deployments. The default maximum node count for each worker node pool is 20. When this limit is reached, the worker node pool can't auto-scale and worker Pods may fail to schedule. A cluster's node count is most affected by the number of worker Pods that are executing Airflow tasks. See [Worker autoscaling logic](configure-worker-queues.md#worker-autoscaling-logic). 

Maximum node count is different than **Maximum Worker Count**, which is configured for each worker queue and determines the maximum total number of nodes that a worker queue within a single Deployment can scale to. Maximum node count for a worker pool in your cluster must always be equal to or greater than the sum of all maximum worker count values for all worker queues that are configured with that worker type.

For example, if:

- You have 3 Deployments that each have 1 worker queue configured with the `m5.2xlarge` worker type for a total of 3 worker queues.
- 1 of the 3 worker queues has a maximum worker count of 10.
- 2 of the 3 worker queues have a maximum worker count of 5.
- The maximum node count for the `m5.2xlarge` node pool in your cluster must be equal to or greater than 15 to make sure that each worker queue can scale to its limit.

Astronomer regularly monitors your usage and the number of nodes deployed in your cluster. As your usage of Airflow increases, Astronomer support might contact you and recommend that you increase or decrease your maximum node count to limit infrastructure cost or ensure that you can support a growing number of tasks and Deployments. If your maximum node count is reached, you will be contacted.

To change the maximum node count for a node pool, contact [Astronomer Support](https://cloud.astronomer.io/support).

## Configure a Database instance type

Every Astro cluster is created with and requires a managed PostgreSQL database. This database serves as a primary relational database for the data plane and powers the metadata database of each Astro Deployment within a single cluster.

Astro uses the following databases:

- AWS: [Amazon RDS](https://aws.amazon.com/rds/)
- GCP: [Cloud SQL](https://cloud.google.com/sql)
- Azure: [Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/products/postgresql/)

During the cluster creation process, you are asked to specify a **DB Instance Type** according to your use case and expected workload, but it can be modified at any time. Each database instance type comprises of varying combinations of CPU, memory, and network performance. For the list of database instance types available on Astro, see [AWS](resource-reference-aws.md#rds-instance-type), [Azure](resource-reference-azure.md#db-instance-type), or [GCP](resource-reference-gcp.md#db-instance-type).

To request a different database instance type, contact [Astronomer support](https://cloud.astronomer.io/support).

## Configure cluster tags (AWS only)

Custom tags help your organization quickly identify and categorize your AWS clusters by purpose, owner, or other business need. For example, you can request tags that help you quickly identify a production or a test cluster, or tags that assist with cost analysis. For more information about tags, see [Tagging your Amazon EKS resources](https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html).

To view existing tags for a cluster, go to the **Clusters** tab, select a cluster, and click **Tags**. To create a new cluster tag, contact [Astronomer support](https://cloud.astronomer.io/support) and provide the key and value for the tag.

## Related documentation

- [Create a cluster](create-cluster.md)
- [AWS cluster settings](resource-reference-aws.md)
- [Microsoft Azure cluster settings](resource-reference-azure.md)
- [GCP cluster settings](resource-reference-gcp.md)
