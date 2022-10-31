---
sidebar_label: "Azure"
title: "Microsoft Azure cluster configurations"
id: resource-reference-azure
description: Reference of all supported configurations for new Astro clusters on Microsoft Azure.
sidebar_custom_props: { icon: 'img/azure.png' }
---

Unless otherwise specified, new clusters on Microsoft Azure are created with a set of default resources that are considered appropriate for most use cases.

## Default cluster values

| Resource                                      | Description                                                                                                                                   | Quantity/Default Size                                                                         |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [Azure Kubernetes Service (AKS) Cluster](https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes)        | Runs the Astro Data Plane, which hosts the resources and data required to execute Airflow tasks.                                              | 1x  |
| [Resource Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal)                                | A container for cluster resources.                                                                                                            | 1x                                                                                            |
| Worker node pool | A node pool that runs all workers across Deployments in the cluster. The number of nodes in the pool auto-scales based on the demand for workers in your cluster. You can configure multiple worker node pools to run tasks on different worker types. This node pool is fully managed by Astronomer. | 1x pool of Standard_D4d_v5 nodes |
| Airflow node pool | A node pool that runs all core Airflow components, including the scheduler and webserver. This node pool is fully managed by Astronomer. | 1x pool of Standard_D4d_v5 nodes |
| Astro system node pool | A node pool that runs all other system components required in Astro. The availability zone determines how many nodes are created. This node pool is fully managed by Astronomer.| 1x pool of Standard_D4d_v5 nodes |
| [Azure Virtual Network (VNet)](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)                  | A virtual network that hosts Azure resources.                                                                                                 | 1x /19                                                                                        |
| [Subnets](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-subnet)                                     | Created in the VNet and used for the backing database, Pod, node, and private endpoints.                                                      | <br />/28 for database <br />/21 for pods <br />/21 for nodes <br />/22 for private endpoints |
| [Azure Database for PostgreSQL Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/) | A private database instance and the Astro data plane primary database. Hosts a metadata database for each hosted Airflow Deployment.          | Standard_D4ds_v4                                                                              |
| Private DNS Zone for Database                 | Provides access to the private database instance.                                                                                             | 1x                                                                                            |                                                                                           |
| Azure Storage Account (Standard)              | Stores Azure Blobs.                                                                                                                           | 1x                                                                                            |
| [Azure Blob Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)                            | Stores Airflow task logs.                                                                                                                     | 1x                                                                                            |
| [Private Endpoint for Blob Storage](https://docs.microsoft.com/en-us/azure/storage/common/storage-private-endpoints)             | Provides access to Azure Blob storage task logs.                                                                                              | 1x                                                                                            |
| [Private DNS Zone for Blob Storage](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-dns)             | Provides access to Azure Blob storage task logs.                                                                                              | 1x                                                                                            |
| Public IP Address                             | Required for connectivity to the control plane and other services.                                                                            | 1x                                                                                            |
| Maximum Node Count | The maximum number of worker nodes that your Astro cluster can support. When this limit is reached, your cluster can't auto-scale and worker Pods may fail to schedule. | 20 |

## Supported cluster configurations

Depending on the needs of your organization, you may be interested in modifying certain configurations of a new or existing cluster on Astro.

To create a new cluster on Astro with a specified configuration, see [Install Astro on Azure](install-azure.md) or [Create a cluster](create-cluster.md). To make changes to an existing cluster, see [Modify a cluster](modify-cluster.md).

### Supported regions

Astro supports the following Azure regions:

- Australia East
- Canada Central
- Central US
- East US
- Japan East
- South Africa North
- South Central US
- West Europe
- West US 3

Modifying the region of an existing Astro cluster isn't supported. If you're interested in a region that isn't on this list, contact [Astronomer support](https://cloud.astronomer.io/support).

### Worker node pools

Node pools are a scalable collection of worker nodes with the same instance type. These nodes are responsible for running the Pods that execute Airflow tasks. If your cluster has a node pool for a specific instance type, you can configure tasks to run on those instance types using [worker queues](configure-deployment-resources.md#worker-queues). To make an instance type available in a cluster, contact [Astronomer support](https://support.astronomer.io) with a request to create a new node pool for the specific instance type. Not all instance types are supported in all AWS regions.

Astronomer monitors your usage and the number of nodes deployed in your cluster. As your usage of Airflow increases, Astronomer support might contact you and provide recommendations for updating your node pools to optimize your infrastructure spend or increase the efficiency of your tasks.

For detailed information on each instance type, see [Virtual machines in Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/). If you're interested in a machine type that isn't on this list, contact [Astronomer support](https://cloud.astronomer.io/support). Not all machine types are supported in all regions.

### Worker node size resource reference

Each worker node in a pool runs a single worker Pod. A worker Pod's actual available size is equivalent to the total capacity of the instance type minus Astro’s system overhead.

The following table lists all available instance types for worker node pools, as well as the Pod size that is supported for each instance type. As the system requirements of Astro change, these values can increase or decrease.

| Node Instance Type               | CPU      | Memory      |
| -------------------------------- | -------- | ----------- |
| Standard_D4_v5           | 2.5 CPUs | 9.3 GiB MEM |
| Standard_D8_v5         | 6.4 CPUs | 24 GiB MEM  |
| Standard_D4d_v5 | 2.5 CPUs | 9.3 GiB MEM |
| Standard_D8d_v5         | 6.4 CPUs | 24 GiB MEM  |

If your Organization needs an instance type that supports a larger worker size, contact [Astronomer support](https://support.astronomer.io). For more information about configuring worker size on Astro, see [Configure a Deployment](configure-deployment-resources.md).

### Maximum node count

Each Astro cluster has a limit on how many nodes it can run at a time. This limit includes the worker nodes and system nodes managed by Astronomer.

The default maximum node count for all nodes across your cluster is 20. A cluster's node count is most affected by the number of worker Pods that are executing Airflow tasks. See [Worker autoscaling logic](configure-worker-queues.md#worker-autoscaling-logic).

If the node count for your cluster reaches the maximum node count, new tasks might not run or get scheduled. Astronomer support monitors the maximum node count and will contact your organization if it is reached. To check your cluster's current node count, contact [Astronomer Support](https://cloud.astronomer.io/support).
