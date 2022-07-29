---
sidebar_label: "Azure"
title: "Resources required for Astro on Azure"
id: resource-reference-azure
description: Reference information for new Astro on Azure clusters.
---

Unless otherwise specified, new clusters on Microsoft Azure are created with a set of default resources that are considered appropriate for most use cases.

## Default cluster values

| Resource                | Description                                                                                          | Quantity/Default Size        |
| ----------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------- |
| Resource Group          | A container for cluster resources.                                   | 1x                            |
| Azure Virtual Network (VNet)                    | A virtual network that hosts Azure resources.                                                         | 1x /19                        |
| Subnets                 | Created in the VNet and used for the backing database, Pod, node, and private endpoints. | <br />/28 for database <br />/21 for pods <br />/21 for nodes <br />/22 for private endpoints |
| Azure Database for PostgreSQL Flexible Server   | A private database instance and the Astro data plane primary database. Hosts a metadata database for each hosted Airflow Deployment.                      | Standard_D4ds_v4                             |
| Private DNS Zone for Database            | Provides access to the private database instance. | 1x |
| Azure Kubernetes Service (AKS) Cluster | Runs the Astro Data Plane, which hosts the resources and data required to execute Airflow tasks. | 1x 
| Virtual Machines (nodes)  | Hosts all system and Airflow components on Astro, including workers and schedulers. Auto-scale based on the demand for nodes in your cluster. | Standard_D4d_v5 |
| Azure Storage Account (Standard) | Stores Azure Blobs. | 1x |
| Azure Blob Storage | Stores Airflow task logs.  | 1x |
| Private Endpoint for Blob Storage | Provides access to Azure Blob storage task logs. | 1x |
| Private DNS Zone for Blob Storage | Provides access to Azure Blob storage task logs. | 1x |
| Public IP Address | Required for connectivity to the control plane and other services. | 1x |

## Supported cluster configurations

Depending on the needs of your organization, you may be interested in modifying certain configurations of a new or existing cluster on Astro.

To create a new cluster on Astro with a specified configuration, see [Install Astro on Azure](install-azure.md) or [Create a cluster](create-cluster.md). To make changes to an existing cluster, see [Modify a cluster](modify-cluster.md).

### Supported regions

Astro supports the following Azure regions:

- Central US
- East US
- West US 3
- Canada Central
- West Europe

Modifying the region of an existing Astro cluster isn't supported. If you're interested in a region that isn't on this list, contact [Astronomer support](https://support.astronomer.io).

### Node instance type

Astro supports different machine types and combinations of CPU, memory, storage, and networking capacity. All system and Airflow components within a single cluster are powered by the nodes specified during the cluster creation or modification process.

#### System nodes

- Standard_D4d_v5

#### Worker nodes

- Standard_D4d_v5
- Standard_D8d_v5
- Standard_D4_v5 
- Standard_D8_v5

For detailed information on each instance type, see [Virtual machines in Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/). If you're interested in a machine type that isn't on this list, contact [Astronomer support](https://support.astronomer.io/). Not all machine types are supported in all regions.

### Maximum node count

Each Astro cluster has a limit on how many nodes it can run at once. This maximum includes worker nodes as well as system nodes managed by Astronomer.

The default maximum node count for all nodes across your cluster is 20. A cluster's node count is most affected by the number of worker Pods that are executing Airflow tasks. See [Worker autoscaling logic](configure-deployment-resources.md#worker-autoscaling-logic).

If the node count for your cluster reaches the maximum node count, new tasks might not run or get scheduled. Astronomer monitors maximum node count and is responsible for contacting your organization if it is reached. To check your cluster's current node count, contact [Astronomer Support](https://support.astronomer.io).

### Deployment Worker Size Limits

You can use the **Worker Resources** setting in the Cloud UI to allocate worker Pod CPU and memory.

The following table lists the maximum worker size that is supported on Astro for each worker node instance type. As the system requirements of Astro change, these values can increase or decrease. If you try to set **Worker Resources** to a size that exceeds the maximum for your cluster's worker node instance type, an error message appears in the Cloud UI.

| Node Instance Type | Maximum AU | CPU       | Memory       |
|--------------------|------------|-----------|--------------|
|Standard_D4_v5 - 4/16      | 25         | 2.5 CPUs | 9.3    GiB MEM |
|Standard_D8_v5 - 8/32     | 64         | 6.4 CPUs | 24   GiB MEM |
|Standard_D4d_v5 - 4/16 (Default)      | 25         | 2.5 CPUs  | 9.3   GiB MEM |
|Standard_D8d_v5 - 8/32      | 64         | 6.4 CPUs | 24   GiB MEM |

If your Organization needs an instance type that supports a worker size limit higher than 64 AU, contact [Astronomer support](https://support.astronomer.io). For more information about configuring worker size on Astro, see [Configure a Deployment](configure-deployment-resources.md#worker-resources).

:::info

The size limits defined here also apply to **Scheduler Resources**, which determines the CPU and memory allocated to the Airflow Scheduler(s) of each Deployment. The maximum scheduler size on Astro is 30 AU, which means there are some node instance types for which that maximum size is not supported.

For more information about the scheduler, see [Configure a Deployment](configure-deployment-resources.md#scheduler-resources).

:::