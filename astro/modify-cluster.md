---
sidebar_label: 'Configure a cluster'
title: "Manage and modify clusters"
id: modify-cluster
description: Learn what you can configure on an existing Astro cluster.
---

New clusters on Astro typically have default configurations that are suitable for standard use cases. However, your organization might need to modify an existing cluster to meet certain networking, governance, or use case requirements. For example, you might need to:

- Add a worker type, which creates a new worker node pool in your cluster and allows your team to select that worker type in a Deployment.
- Authorize a Workspace to a cluster, which ensures that your cluster only host Deployments from a specific Workspace or set of Workspaces.
- Create a VPC connection or a transit gateway connection between your Astro cluster and a target VPC.
- Apply custom tags, which can help your team identify your Astro clusters and associate them with a particular purpose or owner within your cloud provider ecosystem. (AWS only)

Most of these modifications can't be completed in the Cloud UI or with the Astro CLI and require you to contact [Astronomer support](https://cloud.astronomer.io/support/). Cluster modifications typically take only a few minutes to complete and don't require downtime. In these cases, the Airflow UI and Cloud UI continue to be available and your Airflow tasks are not interrupted.

The information provided here will help you determine which modifications you can make to your clusters on Astro and how to request or apply the modifications. To create a new cluster, see [Create a cluster](create-cluster.md).

If you don't have a cluster on Astro, see [Install Astro](https://docs.astronomer.io/astro/category/install-astro). If you have an existing cluster and you want to create additional clusters, see [Create a cluster](create-cluster.md).

## View clusters

In the Cloud UI, click the **Clusters** tab to view a list of the clusters that are available to your Organization. Click a cluster and then click the **Worker Types**, **Workspace Authorization**, or **Details** tabs to view cluster information including:

- The region for the cluster.
- The cloud provider Account ID associated with the cluster.
- The size and type of the cluster's database.
- When the cluster was created and last updated.

Some of the configurations in the Cloud UI cannot be changed. Only the listed configurations can be modified by your team.

## Manage worker types

On Astro, worker nodes execute Airflow tasks. Workers are organized through worker node pools, which are sets of configurations that Astro uses to scale up and down workers of a specific instance type. Each worker node pool can be configured with a node instance type and a maximum node count. 

To have a Deployment run Airflow tasks with a specific worker type, you need to work with Astronomer support to create a worker node pool for that worker type on the cluster hosting the Deployment. Then, you can configure a Deployment worker queue to use that worker type. Contact [Astronomer support](https://cloud.astronomer.io/support/) with the name of the worker type(s) you want to enable in your cluster. For example, `m6i.2xlarge`.

To confirm a modification was completed, click the **Clusters** tab in the Cloud UI and then click the **Worker Types** tab to view updated configuration information.

### About worker node pools

All Astro clusters have one worker node pool for one worker type by default, but you can configure up to 30 additional worker types. After Astronomer creates a worker node pool for a cluster, your team can configure a worker queue in any Deployment with that worker type. The worker type appears as a new option on the **Worker Type** page of the Cloud UI and as an option in the Astro CLI. If your cluster only has one worker type, all tasks across Deployments in your cluster can only run on that type of worker. Individual worker nodes run only on a single Deployment, but a worker node pool can have worker nodes spread across multiple Deployments.

Creating a worker node pool does not necessarily mean that the infrastructure is created in your cluster. A worker node pool has zero nodes if any of the following are true:

- There are no Deployments in your cluster that have worker queues configured with the worker type.
- There are no default worker queues configured with the worker type. The default worker queue cannot scale to zero workers, but additional worker queues can scale to zero.

### Configure node instance type

Each worker type on Astro is configured with a node instance type that is defined by your cloud provider. For example, `m5.2xlarge` on AWS, `Standard_D8_v5` on Azure, or `e2-standard-8` on GCP. Node instance types are comprised of varying combinations of CPU, memory, storage, and networking capacity. By choosing a node instance type, you can provide the appropriate balance of resources for your Airflow tasks.

How your Airflow tasks use the capacity of a worker node depends on which executor is selected for your Deployment. With the Celery executor, each worker node runs a single worker Pod. A worker Pod's actual available size is equivalent to the total capacity of the instance type minus Astro’s system overhead. With the Kubernetes executor, each worker node can run an unlimited number of Pods as long as the sum of all requests from each Pod doesn't exceed the total capacity of the node minus Astro's system overhead.

To modify the node instance type of an existing worker node pool, contact [Astronomer Support](https://support.astronomer.io/). For the list of worker node pool instance types available on Astro, see [AWS supported worker node pool instance types](resource-reference-aws.md#supported-worker-node-pool-instance-types), [Azure supported worker node pool instance types](resource-reference-azure.md#supported-worker-node-pool-instance-types), or [GCP supported worker node pool instance types](resource-reference-gcp.md#supported-worker-node-pool-instance-types).

### Configure maximum node count

Each worker node pool on Astro has a **Maximum Node Count**, which represents the maximum total number of nodes that a worker node pool can have at any given time across Deployments. The default maximum node count for each worker node pool is 20. When this limit is reached, the worker node pool can't auto-scale and worker Pods may fail to schedule. A cluster's node count is most affected by the number of tasks that are running at the same time across your cluster, and the number of worker Pods that are executing those tasks. See [Worker autoscaling logic](executors.md#celery-worker-autoscaling-logic).

Maximum node count is different than **Maximum Worker Count**, which is configured within the Cloud UI for each worker queue and determines the maximum total number of nodes that the worker queue can scale to. Maximum node count for a node pool must always be equal to or greater than the sum of all maximum possible workers across all worker queues that are configured with that worker node type.

For example, consider the following configurations within a cluster:

- You have 3 Deployments that each have 1 worker queue configured with the `m5.2xlarge` worker type for a total of 3 worker queues.
- 1 of the 3 worker queues has a maximum worker count of 10.
- 2 of the 3 worker queues have a maximum worker count of 5.

In this scenario, the maximum node count for the `m5.2xlarge` node pool in your cluster must be equal to or greater than 15 to make sure that each worker queue can scale to its limit.

Astronomer regularly monitors your usage and the number of nodes deployed in your cluster. As your usage of Airflow increases, Astronomer support might contact you and recommend that you increase or decrease your maximum node count to limit infrastructure cost or ensure that you can support a growing number of tasks and Deployments. If your maximum node count is reached, you will be contacted.

To change the maximum node count for a node pool, contact [Astronomer Support](https://cloud.astronomer.io/support).

## Configure a Database instance type

Every Astro cluster is created with and requires a managed PostgreSQL database. This database serves as a primary relational database for the data plane and powers the metadata database of each Astro Deployment within a single cluster.

During the cluster creation process, you are asked to specify a **DB Instance Type** according to your use case and expected workload, but it can be modified at any time. Each database instance type costs a different amount of money and comprises of varying combinations of CPU, memory, and network performance.

Astro uses the following databases:

| Cloud          | Database                                                                                | Instance Types                                        |
| -------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| AWS            | [Amazon RDS](https://aws.amazon.com/rds/)                                               | [Supported RDS instance types](resource-reference-aws#supported-rds-instance-types) |
| GCP            | [Cloud SQL](https://cloud.google.com/sql)                                               | [Supported Cloud SQL instance types](resource-reference-gcp#supported-cloud-sql-instance-types) |
| Azure          | [Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/products/postgresql/) | [Supported Azure Database for PostgreSQL instance types](resource-reference-azure#supported-azure-database-for-postgresql-instance-types) |


To request support for a different database instance type or to modify the database instance type after cluster creation, contact [Astronomer support](https://cloud.astronomer.io/support).

## Authorize Workspaces to a cluster

As an Organization Owner, you can keep teams, resources, and projects isolated by authorizing Workspaces only to specific clusters. You can gain greater control over your cloud resources by ensuring that only authorized pipelines are running on specific clusters.

1. In the Cloud UI, click the **Clusters** tab and then select a cluster.
2. Click the **Workspace Authorization** tab and then click **Edit Workspace Authorization**.
3. Click **Restricted** and select the Workspaces that you want to map to the cluster. 
4. Click **Update**.

After you authorize Workspaces to a cluster, Astro treats the cluster as restricted. Restricted clusters appear as an option when creating a new Deployment only if the Deployment's Workspace is authorized to the cluster. 

:::info 

A cluster with authorized Workspaces can't host Deployments from any Workspaces that aren't authorized to the cluster. To map Workspaces to a cluster, you must first transfer any existing Deployments on the cluster to one of these Workspace.

Similarly, to unauthorize a Workspace but keep its Deployments in the cluster, you must transfer your Deployments to a Workspace which is still authorized to the cluster. See [Transfer a Deployment to another Workspace](configure-deployment-resources.md#transfer-a-deployment-to-another-workspace).

:::
