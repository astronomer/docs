---
sidebar_label: 'Configure a cluster'
title: "Manage and modify clusters"
id: modify-cluster
description: Learn what you can configure on an existing Astro cluster.
---

Astro cluster runs your Astro Deployments in isolated namespaces on the Kubernetes cluster. Your organization might choose to have one or multiple clusters to meet certain networking, governance, or use case requirements. You can always start with one cluster and [create additional clusters](create-cluster.md) later. New clusters on Astro typically have default configurations that are suitable for standard use cases. You can request [Astronomer support](https://support.astronomer.io) to edit the configuration of an existing cluster. For example, you might need to:

- Add a [worker type](#manage-worker-type), which creates a new [worker node pool](#about-worker-node-pools) in your cluster and allows your team to select that worker type in a Deployment.
- Increase or decrease the maximum number of worker nodes for a given worker type that your cluster can scale-up to. 
- Create a VPC connection or a transit gateway connection between your Astro cluster and a target VPC 

Cluster modifications typically take only a few minutes to complete and don't require downtime. In these cases, the Cloud UI and Airflow UI continue to be available and your Airflow tasks are not interrupted.

If you don't have a cluster on Astro, see [Install Astro](https://docs.astronomer.io/astro/category/install-astro).

## View clusters

1. In the **Cloud UI**, go click the Astronomer logo in the top left corner to go to your Organization's home page. 
2. Click **Clusters** to view a list of the clusters that are available to your Organization. 
3. Click a cluster to view its information. See the following table for more information about each available information page.

| Tab name | Description |
|----------|-------------|
| Details  | General permanent configurations, including cluster name, IDs, and connectivity options.  | 
| Worker Types | The available worker types for configuring worker queues on your cluster. See [Manage worker types](#manage-worker-types). | 
| Tags | (AWS only) Configured cluster tags. See [Add tags to your cluster](#add-tags-to-your-cluster-aws-only).| 
| Workspace Authorization | List of Workspaces that can create Deployments on this cluster. See [Authorize Workspaces to a cluster](modify-cluster.md#authorize-workspaces-to-a-cluster). |


## Manage worker types

On Astro, _worker nodes_ are the nodes that are used to run Airflow workers, which are responsible for executing Airflow tasks in your Deployments. A _worker type_ is one of your cloud provider's available node instance types. This determines how much CPU and memory your workers have for running tasks. Workers are organized using [worker node pools](modify-cluster.md#about-worker-node-pools) that groups together nodes of a specific instance type.

To have a Deployment run Airflow tasks with a specific worker type, you can configure a Worker queue in your Deployment to use that worker type. If the worker type is not available to your cluster, you can contact [Astronomer support](https://support.astronomer.io) and ask to have a worker type enabled for your cluster.

After you make a change to your available worker types, you can [check your cluster settings](modify-cluster.md#view-clusters) to confirm that the change was applied.

### About worker node pools

A Kubernetes _node pool_ is group of nodes within a cluster that share the same configuration. On Astro, a _worker node pool_ is a Kubernetes node pool that's used to run Airflow workers, which are responsible for executing Airflow tasks in your Deployments. Each worker node pool has:

- A _worker type_, which is one of your cloud provider's available node instance types.
- A _maximum node count_, which is the the maximum number of nodes that can run concurrently in the worker node pool across all Deployments.

During the Astro cluster creation process, you provide Astronomer with a default worker type and a maximum node count to configure a default worker node pool. This node pool is used for default Worker queues for all of your Deployments. When you request Astronomer support to add a [new worker type](modify-cluster.md#configure-node-instance-type) to your cluster, new worker node pool is created on the cluster. You can then configure [worker queues](configure-worker-queues.md) that use the new worker type. 

After you configure a worker node pool, you can configure [worker queues](configure-worker-queues.md) that use the node pool's worker type. Each worker in a worker queue uses the entirety of a node in the worker node pool.

Your default worker node pool always runs a minimum of one node, while additional worker node pools can scale to zero. Additional nodes spin up as required based on the auto-scaling logic of your Deployment Airflow executor and your worker queues.

A worker node pool can be shared across multiple Deployments, but each node runs only the work of a single Deployment. A worker node pool's maximum node count applies across all Deployments where the node pool is used. For example, consider two Deployments that share a worker node pool with a maximum node count of 30. If one Deployment is using all 30 of the available worker nodes, the other Deployment can't use any additional nodes and therefore can't run tasks that rely on that worker type.

In the following diagram, you can see the relationship between worker node pools, Deployments, and worker queues. The worker node pools can be assigned to multiple Deployments, but each node in a given worker pool is used in only one Deployment worker queue.

![Worker Node Pool and Worker Queues](/img/docs/worker-node-pool.png)

### Configure node instance type

Each worker type on Astro is configured with a node instance type that is defined by your cloud provider. For example, `m5.2xlarge` on AWS, `Standard_D8_v5` on Azure, or `e2-standard-8` on GCP. Node instance types are comprised of varying combinations of CPU, memory, storage, and networking capacity. By choosing a node instance type for your worker, you can provide the appropriate balance of resources for your Airflow tasks.

How your Airflow tasks use the capacity of a worker node depends on which executor is selected for your Deployment. With the Celery executor, each worker node runs a single worker Pod. A worker Pod's actual available size is equivalent to the total capacity of the instance type minus Astro’s system overhead. With the Kubernetes executor, each worker node can run an unlimited number of Pods as long as the sum of all requests from each Pod doesn't exceed the total capacity of the node minus Astro's system overhead.

To add a new node instance type, contact [Astronomer Support](https://cloud.support.astronomer.io). For the list of worker node pool instance types available on Astro, see [AWS supported worker node pool instance types](resource-reference-aws.md#supported-worker-node-pool-instance-types), [Azure supported worker node pool instance types](resource-reference-azure.md#supported-worker-node-pool-instance-types), or [GCP supported worker node pool instance types](resource-reference-gcp.md#supported-worker-node-pool-instance-types).

### Configure maximum node count

Each worker node pool on Astro has a **Maximum Node Count**, which represents the maximum total number of nodes that a worker node pool can have at any given time across Deployments. The default maximum node count for each worker node pool is 20. When this limit is reached, the worker node pool can't auto-scale and worker Pods may fail to schedule. A cluster's node count is most affected by the number of tasks that are running at the same time across your cluster, and the number of worker Pods that are executing those tasks. See Worker autoscaling logic for [Celery executor](executors.md#celery-worker-autoscaling-logic) and for [Kubernetes executor](executors.md#kubernetes-worker-autoscaling-logic).

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

## Add Tags to your Astronomer Infrastructure (AWS only)

You can request Astronomer Support to add [tags](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-tags.html) to your AWS clusters. Specifically, the tags are applied to the following components in your data plane:

- EKS cluster
- RDS metadata database
- S3 logging bucket
- IAM roles
  
Tags can help your team identify your Astro clusters and associate them with a particular purpose or owner within your cloud provider ecosystem. 

You can raise a request with [Astronomer Support](https://cloud.astronomer.io/support) to add or remove tags. To view your current cluster tags, see [View clusters](#view-clusters).

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
