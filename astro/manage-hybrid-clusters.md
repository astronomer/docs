---
sidebar_label: 'Manage Hybrid clusters'
title: "Manage Hybrid clusters"
id: manage-hybrid-clusters
description: Learn what you can configure on an Astro cluster.
---

:::warning

This document applies only to [Astro Hybrid](hybrid-overview.md). To see whether you're an Astro Hybrid user, click your Workspace name in the upper left corner of the Cloud UI, then click **Organization Settings**. Your Astro product type is listed under **Product Type** on the **General** page.

To create a cluster on Astro Hosted, see [Create a dedicated cluster](create-dedicated-cluster.md).

:::

An Astro Hybrid cluster runs your Astro Deployments in isolated namespaces on your cloud. Your organization might choose to have one or multiple clusters to meet certain networking, governance, or use case requirements. You can always start with one cluster and [create additional clusters](#create-a-cluster) later. New clusters on Astro typically have default configurations that are suitable for standard use cases. You can request [Astronomer support](https://support.astronomer.io) to edit the configuration of an existing cluster. For example, you might need to:

- Add a [worker type](#manage-worker-type), which creates a new [worker node pool](#about-worker-node-pools) in your cluster and allows your team to select that worker type in a Deployment.
- Increase or decrease the maximum number of worker nodes for a given worker type that your cluster can scale-up to. 
- Create a VPC connection or a transit gateway connection between your Astro cluster and a target VPC.

Cluster modifications typically take only a few minutes to complete and don't require downtime. In these cases, the Cloud UI and Airflow UI continue to be available and your Airflow tasks are not interrupted.

If you don't have a cluster on Astro, see [Install Astro](https://docs.astronomer.io/astro/category/install-astro-hybrid).

## Create a cluster

The Astro install typically starts with one cluster for each Organization. However, your organization can choose to configure multiple Astro clusters. This could enable a few benefits, including:

- Clusters in different regions
- Different clusters for development and production environments

Within a single Workspace, you can host Deployments across multiple clusters. For example, you might have a production Deployment running in a production cluster and a development Deployment running in a development cluster. Both of those Deployments can be in the same Workspace.

This guide provides instructions for provisioning additional clusters within your Astro Organization.

### Prerequisites

To create an Astro cluster on AWS, Microsoft Azure, or Google Cloud Platform (GCP), you'll need the following:

- An activated data plane.
- Permissions to configure IAM in the dedicated account for Astro on your cloud.

### AWS

To create a new Astro cluster on AWS for your Organization, submit a request to [Astronomer support](astro-support.md). In your request, provide the following information for every new cluster that you want to provision:

- Your Astro AWS Account ID.
- Your preferred Astro cluster name.
- The AWS region that you want to host your cluster in.
- Your preferred node instance type.
- Your preferred max node count.
- Your preferred VPC CIDR.

If you don't specify configuration preferences, Astronomer support creates a cluster with a VPC CIDR of 172.20.0.0/20,`m5.xlarge` nodes, and a maximum node count of 20 in `us-east-1`. For information about supported regions, configurations, and defaults, see [Resources required for Astro on AWS](resource-reference-aws-hybrid.md).

#### Additional set up for AWS regions that are disabled by default

Some AWS regions that Astronomer supports are [disabled by default on AWS](https://docs.aws.amazon.com/general/latest/gr/rande-manage.html#rande-manage-enable). These regions are:

- `af-south-1` - Africa (Cape Town)
- `ap-east-1` - Asia Pacific (Hong Kong)
- `me-south-1` - Middle East (Bahrain)

To create a cluster in one of these regions, complete the following additional set up in your AWS account:

1. In the AWS IAM console, update the `astronomer-remote-management` trust relationship to include permissions for enabling and disabling your desired region as described in the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws-enable-disable-regions.html):

    ```YAML
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::406882777402:root"
          },
          "Action": "sts:AssumeRole",
          "Condition": {
            "StringEquals": {
              "sts:ExternalId": "<External-ID>"
            }
          }
        }
        {
            "Sid": "EnableDisableRegion",
            "Effect": "Allow",
            "Action": [
                "account:EnableRegion",
                "account:DisableRegion"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {"account:TargetRegion": "<your-aws-region>"}
            }
        },
        {
            "Sid": "ViewConsole",
            "Effect": "Allow",
            "Action": [
                "aws-portal:ViewAccount",
                "account:ListRegions"
            ],
            "Resource": "*"
        }
      ]
    }
    ```

2. In the AWS Management Console, enable the desired region as described in [AWS documentation](https://docs.aws.amazon.com/general/latest/gr/rande-manage.html#rande-manage-enable).
3. Upgrade your [global endpoint session token](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html#sts-regions-manage-tokens) to version 2, which is valid in all AWS regions, by running the following command in the [AWS CLI](https://aws.amazon.com/cli/):

    ```sh
    aws iam set-security-token-service-preferences --global-endpoint-token-version v2Token
    ```

### Azure

To create a new Astro cluster on Azure for your Organization, submit a request to [Astronomer support](astro-support.md). In your request, provide the following information for every new cluster that you want to provision:

- Your Azure Tenant ID and Subscription ID.
- Your preferred Astro cluster name.
- The Azure region that you want to host your cluster in.
- Your preferred node instance type. See [Azure Hybrid cluster resource reference](resource-reference-azure-hybrid.md#supported-worker-node-pool-instance-types).
- Your preferred maximum node count.

If you don't specify configuration preferences, Astronomer support creates a cluster with `Standard_D4d_v5 nodes`, one Postgres Flexible Server instance (`D4ds_v4`), and a maximum node count of 20 in `CentralUS`. If you're using Virtual Network (VNet) peering, a CIDR block (RFC 1918 IP Space) with the default CIDR range `172.20.0.0/19` is implemented.

For information on all supported regions and configurations, see [Resources required for Astro on Azure](resource-reference-azure-hybrid.md).  

### GCP

To create a new Astro cluster on Google Cloud Platform (GCP) for your Organization, submit a request to [Astronomer support](astro-support.md). In your request, provide the following information for every new cluster that you want to provision:

- Your preferred Astro cluster name.
- The GCP region that you want to host your cluster in.
- Your preferred node instance type.
- Your preferred CloudSQL instance type.
- Your preferred maximum node count.
- Your preferred VPC CIDR.

If you don't specify configuration preferences, Astronomer support creates a cluster with a VPC CIDR of 172.20.0.0/22, `e2-standard-4` nodes, one Small General Purpose CloudSQL instance (2vCPU, 8GB), and a maximum node count of 20 in `us-central1`.  For information on all supported regions and configurations, see [Resources required for Astro on GCP](resource-reference-gcp-hybrid.md). 

:::info Configure cluster maintenance windows

All GCP dedicated clusters are subscribed to the [GKE regular release channel](https://cloud.google.com/kubernetes-engine/docs/concepts/release-channels), meaning that Google automatically upgrades the cluster and its nodes whenever an upgrade is available.

After you create a GCP cluster, you can control when these upgrades happen by requesting a [maintenance window](https://cloud.google.com/kubernetes-engine/docs/how-to/maintenance-windows-and-exclusions#maintenance-window) for the cluster. Maintenance windows determine when and how Google updates your cluster. You can use maintenance windows to ensure that upgrades don't happen while critical DAGs are running on your cluster. 

To set a maintenance window, first choose a maintenance window time and read through the [maintenance window considerations](https://cloud.google.com/kubernetes-engine/docs/how-to/maintenance-windows-and-exclusions#considerations) to make sure that the time is optimized for your cluster. Then, contact [Astronomer Support](https://cloud.astronomer.io/open-support-request) and provide your cluster ID and desired maintenance window.

:::

### Confirm cluster creation

Astronomer support sends you a notification when your cluster is created. After your cluster is created, you can create a new Deployment in the cluster and start deploying pipelines. See [Create a Deployment](create-deployment.md).

## View clusters

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. 
2. Click **Clusters** to view a list of the clusters that are available to your Organization. 
3. Click a cluster to view its information. See the following table for more information about each available information page.

| Tab name | Description |
|----------|-------------|
| Details  | General permanent configurations, including cluster name, IDs, and connectivity options.  | 
| Worker Types | The available worker types for configuring worker queues on your cluster. See [Manage worker types](#manage-worker-types). | 
| Tags | (AWS only) Configured cluster tags. See [Add tags to your cluster](#add-tags-to-your-cluster-aws-only).| 
| Workspace Authorization | List of Workspaces that can create Deployments on this cluster. See [Authorize Workspaces to a cluster](#authorize-workspaces-to-a-cluster). |

## Manage worker types

On Astro, _worker nodes_ are the nodes that are used to run Airflow workers, which are responsible for executing Airflow tasks in your Deployments. A _worker type_ is one of your cloud provider's available node instance types. This determines how much CPU and memory your workers have for running tasks. Workers are organized using [worker node pools](#about-worker-node-pools) that groups together nodes of a specific instance type.

To have a Deployment run Airflow tasks with a specific worker type, you can configure a worker queue in your Deployment to use that worker type. If the worker type is not available to your cluster, you can contact [Astronomer support](https://support.astronomer.io) and ask to have a worker type enabled for your cluster.

After you make a change to your available worker types, you can [check your cluster settings](#view-clusters) to confirm that the change was applied.

### About worker node pools

A Kubernetes _node pool_ is a group of nodes within a cluster that share the same configuration. On Astro, a _worker node pool_ is a Kubernetes node pool that's used to run Airflow workers, which are responsible for executing Airflow tasks in your Deployments. Each worker node pool has:

- A _worker type_, which is one of your cloud provider's available node instance types.
- A _maximum node count_, which is the maximum number of nodes that can run concurrently in the worker node pool across all Deployments.

During the Astro cluster creation process, you provide Astronomer with a default worker type and a maximum node count to configure a default worker node pool. This node pool is used for the default worker queues for all of your Deployments. When you request Astronomer support to add a [new worker type](#configure-node-instance-type) to your cluster, a new worker node pool of that type is created on the cluster. You can then configure [worker queues](configure-worker-queues.md) that use the new worker type. 

Your default worker node pool always runs a minimum of one node, while additional worker node pools can scale to zero. Additional nodes spin up as required based on the auto-scaling logic of your Deployment Airflow executor and your worker queues.

A worker node pool can be shared across multiple Deployments, but each node runs only the work of a single Deployment. A worker node pool's maximum node count applies across all Deployments where the node pool is used. For example, consider two Deployments that share a worker node pool with a maximum node count of 30. If one Deployment is using all 30 of the available worker nodes, the other Deployment can't use any additional nodes and therefore can't run tasks that rely on that worker type.

In the following diagram, you can see the relationship between worker node pools, Deployments, and worker queues. The worker node pools can be assigned to multiple Deployments, but each node in a given worker pool is used in only one Deployment worker queue.

![Worker Node Pool and Worker Queues](/img/docs/worker-node-pool.png)

### Configure node instance type

Each worker type on Astro is configured with a node instance type that is defined by your cloud provider. For example, `m5.2xlarge` on AWS, `Standard_D8_v5` on Azure, or `e2-standard-8` on GCP. Node instance types consist of varying combinations of CPU, memory, storage, and networking capacity. By choosing a node instance type for your worker, you can provide the appropriate balance of resources for your Airflow tasks.

How your Airflow tasks use the capacity of a worker node depends on which executor is selected for your Deployment. With the Celery executor, each worker node runs a single worker Pod. A worker Pod's actual available size is equivalent to the total capacity of the instance type minus Astro’s system overhead. With the Kubernetes executor, each worker node can run an unlimited number of Pods (one Pod per Airflow task) as long as the sum of all requests from each Pod doesn't exceed the total capacity of the node minus Astro's system overhead.

To add a new node instance type, contact [Astronomer Support](https://cloud.astronomer.io/open-support-request). For the list of worker node pool instance types available on Astro, see [AWS supported worker node pool instance types](resource-reference-aws-hybrid.md#supported-worker-node-pool-instance-types), [Azure supported worker node pool instance types](resource-reference-azure-hybrid.md#supported-worker-node-pool-instance-types), or [GCP supported worker node pool instance types](resource-reference-gcp-hybrid.md#supported-worker-node-pool-instance-types).

### Configure maximum node count

Each worker node pool on Astro has a **Maximum Node Count**, which represents the maximum total number of nodes that a worker node pool can have at any given time across Deployments. The default maximum node count for each worker node pool is 20. When this limit is reached, the worker node pool can't auto-scale and worker Pods may fail to schedule. A cluster's node count is most affected by the number of tasks that are running at the same time across your cluster, and the number of worker Pods that are executing those tasks. See Worker autoscaling logic for [Celery executor](celery-executor.md#celery-worker-autoscaling-logic) and for [Kubernetes executor](kubernetes-executor.md#kubernetes-worker-autoscaling-logic).

Maximum node count is different than **Maximum Worker Count**, which is configured within the Cloud UI for each worker queue and determines the maximum total number of nodes that the worker queue can scale to. Maximum node count for a node pool must always be equal to or greater than the sum of all maximum possible workers across all worker queues that are configured with that worker node type.

For example, consider the following configurations within a cluster:

- You have 3 Deployments that each have 1 worker queue configured with the `m5.2xlarge` worker type for a total of 3 worker queues.
- 1 of the 3 worker queues has a maximum worker count of 10.
- 2 of the 3 worker queues have a maximum worker count of 5.

In this scenario, the maximum node count for the `m5.2xlarge` node pool in your cluster must be equal to or greater than 15 to make sure that each worker queue can scale to its limit.

Astronomer regularly monitors your usage and the number of nodes deployed in your cluster. As your usage of Airflow increases, Astronomer support might contact you and recommend that you increase or decrease your maximum node count to limit infrastructure cost or ensure that you can support a growing number of tasks and Deployments. If your maximum node count is reached, you will be contacted.

To change the maximum node count for a node pool, contact [Astronomer Support](https://cloud.astronomer.io/open-support-request).

## Configure a Database instance type

Every Astro cluster is created with and requires a managed PostgreSQL database. This database serves as a primary relational database for the data plane and powers the metadata database of each Astro Deployment within a single cluster.

During the cluster creation process, you are asked to specify a **DB Instance Type** according to your use case and expected workload, but it can be modified at any time. Each database instance type costs a different amount of money and comprises of varying combinations of CPU, memory, and network performance.

Astro uses the following databases:

| Cloud          | Database                                                                                | Instance Types                                        |
| -------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| AWS            | [Amazon RDS](https://aws.amazon.com/rds/)                                               | [Supported RDS instance types](resource-reference-aws-hybrid.md#supported-rds-instance-types) |
| GCP            | [Cloud SQL](https://cloud.google.com/sql)                                               | [Supported Cloud SQL instance types](resource-reference-gcp-hybrid.md#supported-cloud-sql-instance-types) |
| Azure          | [Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/products/postgresql/) | [Supported Azure Database for PostgreSQL instance types](resource-reference-azure-hybrid.md#supported-azure-database-for-postgresql-instance-types) |


To request support for a different database instance type or to modify the database instance type after cluster creation, contact [Astronomer support](https://cloud.astronomer.io/open-support-request).

## Add tags to your cluster (AWS only)

You can request Astronomer Support to add [tags](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-tags.html) to your AWS clusters. Specifically, the tags are applied to the following components in your data plane:

- EKS cluster
- RDS metadata database
- S3 logging bucket
- IAM roles
  
Tags can help your team identify your Astro clusters and associate them with a particular purpose or owner within your cloud provider ecosystem. 

You can raise a request with [Astronomer Support](https://cloud.astronomer.io/open-support-request) to add or remove tags. To view your current cluster tags, see [View clusters](#view-clusters).
