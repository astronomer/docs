---
sidebar_label: "Azure cluster settings"
title: "Microsoft Azure cluster settings"
id: resource-reference-azure
description: Reference of all supported configurations for new Astro clusters on Microsoft Azure.
sidebar_custom_props: { icon: 'img/azure.png' }
---

Unless otherwise specified, new clusters on Astro are created with a set of default Azure resources that should be suitable for most use cases.

Read the following document for a reference of our default resources as well as supported cluster configurations.

## Default cluster values

| Resource                                                                                                                 | Description                                                                                                                                                                                                                                                                               | Quantity/ Default Size                                                                        | Configurable |
| ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------ |
| [Azure Kubernetes Service (AKS) Cluster](https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes)                    | Runs the Astro Data Plane, which hosts the resources and data required to execute Airflow tasks.                                                                                                                                                                                          | 1x                                                                                            | Yes. See [Manage clusters](modify-cluster.md).            |
| [Resource Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal) | A container for cluster resources.                                                                                                                                                                                                                                                        | 1x                                                                                            |              |
| Worker node pool                                                                                                         | A node pool that hosts all workers with the `default` worker type for all Deployments in the cluster. The number of nodes in the pool auto-scales based on the demand for workers in your cluster. You can configure additional worker node pools to run tasks on different worker types. | 1x pool of Standard_D4d_v5 nodes                                                              | Yes. See [Manage worker node pools](modify-cluster.md#about-worker-node-pools).             |
| Airflow node pool                                                                                                        | A node pool that runs all core Airflow components, including the scheduler and webserver, for all Deployments in the cluster. This node pool is fully managed by Astronomer.                                                                                                              | 1x pool of Standard_D4d_v5 nodes                                                              |              |
| Astro system node pool                                                                                                   | A node pool that runs all other system components required in Astro. The availability zone determines how many nodes are created. This node pool is fully managed by Astronomer.                                                                                                          | 1x pool of Standard_D4d_v5 nodes                                                              |              |
| [Azure Database for PostgreSQL Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/)      | The flexible server is the primary database of the Astro data plane. It hosts a metadata database for each Deployment in the cluster.                                                                                                                                                     | Standard_D4ds_v4                                                                              |              |
| [Azure Virtual Network (VNet)](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)         | A virtual network that hosts Azure resources.                                                                                                                                                                                                                                             | 1x /19                                                                                        |              |
| [Subnets](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-subnet)                          | Created in the VNet and used for the backing database, Pod, node, and private endpoints.                                                                                                                                                                                                  | <br />/28 for database <br />/21 for pods <br />/21 for nodes <br />/22 for private endpoints |              |
| Private DNS Zone for Database                                                                                            | Provides access to the private database instance.                                                                                                                                                                                                                                         | 1x                                                                                            |              |
| Azure Storage Account (Standard)                                                                                         | Stores Azure Blobs.                                                                                                                                                                                                                                                                       | 1x                                                                                            |              |
| [Azure Blob Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)                    | Stores Airflow task logs.                                                                                                                                                                                                                                                                 | 1x                                                                                            |              |
| [Private Endpoint for Blob Storage](https://docs.microsoft.com/en-us/azure/storage/common/storage-private-endpoints)     | Provides access to Azure Blob storage task logs.                                                                                                                                                                                                                                          | 1x                                                                                            |              |
| [Private DNS Zone for Blob Storage](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-dns)            | Provides access to Azure Blob storage task logs.                                                                                                                                                                                                                                          | 1x                                                                                            |              |
| Public IP Address                                                                                                        | Required for connectivity to the control plane and other services.                                                                                                                                                                                                                        | 1x                                                                                            |              |

## Supported cluster regions

Depending on how you installed Astro, you can host Astro clusters in the following Azure regions:

| Code               | Name               | Astro - Bring Your Own Cloud | Astro - Hosted      |
| ------------------ | ------------------ | ---------------------------- | ------------------- |
| `australiaeast`    | Australia East     | ✔️                            |                     |
| `canadacentral`    | Canada Central     | ✔️                            | ✔️                   |
| `centralindia`     | Central India      | ✔️                            |                     |
| `centralus`        | Central US         | ✔️                            |                     |
| `eastasia`         | East Asia          | ✔️                            |                     |
| `eastus`           | East US            | ✔️                            |                     |
| `eastus2`           | East US 2          | ✔️ <sup>1</sup>                            | ✔️ (Private Preview) |
| `francecentral`     | France Central     | ✔️ <sup>1</sup>                         |                     |
| `japaneast`        | Japan East         | ✔️                            |                     |
| `koreacentral`     | Korea Central      | ✔️                            |                     |
| `northeurope`      | North Europe       | ✔️                            | ✔️                   |
| `southafricanorth` | South Africa North | ✔️                            |                     |
| `southcentralus`   | South Central US   | ✔️                            |                     |
| `southeastasia`     | South East Asia    | ✔️ <sup>1</sup>                           | ✔️ (Private Preview) |
| `uksouth`          | UK South           | ✔️                            |                     |
| `westeurope`       | West Europe        | ✔️  <sup>1</sup>                           | ✔️                   |
| `westus2`           | West US 2          | ✔️ <sup>1</sup>                           | ✔️ (Private preview) |
| `westus3`          | West US 3          | ✔️                            |                     |

Modifying the region of an existing Astro cluster isn't supported. If you're interested in a region that isn't listed, contact [Astronomer support](https://cloud.astronomer.io/support).

¹ If you want to host Astro in a dedicated account owned by your organization (Bring Your Own Cloud) in one of these regions, you'll need to contact [Microsoft Azure Support](https://support.microsoft.com/en-us/topic/contact-microsoft-azure-support-2315e669-8b1f-493b-5fb1-d88a8736ffe4) to enable the regions. If you require clarification about this requirement, contact [Astronomer support](https://cloud.astronomer.io/support). 

## DB Instance Type

The following Azure Database for PostgreSQL instance types are supported on Astro: 

- Standard_D4ds_v4 (CPU 4, 16 GiB MEM)
- Standard_D2ds_v4 (CPU 2, 8 GiB MEM)
- Standard_E2ds_v4 (CPU 2, 16 GiB MEM)
- Standard_E4ds_v4 (CPU 4, 32 GiB MEM)

For more information about configuring Azure Database for PostgreSQL, see the [Azure Database for PostgreSQL documentation](https://learn.microsoft.com/en-us/azure/postgresql/).

## Supported worker node pool instance types

Each worker node in a pool runs a single worker Pod. A worker Pod's actual available size is equivalent to the total capacity of the instance type minus Astro’s system overhead.

The following table lists all available instance types for worker node pools, as well as the Pod size that is supported for each instance type. As the system requirements of Astro change, these values can increase or decrease.

| Node Instance Type | CPU      | Memory      |
| ------------------ | -------- | ----------- |
| Standard_D4_v5     | 2.5 CPUs | 9.3 GiB MEM |
| Standard_D8_v5     | 6.4 CPUs | 24 GiB MEM  |
| Standard_D4d_v5    | 2.5 CPUs | 9.3 GiB MEM |
| Standard_D8d_v5    | 6.4 CPUs | 24 GiB MEM  |
| Standard_B4ms      | 2.5 CPUs | 9.3 GiB MEM |
| Standard_B8ms      | 6.4 CPUs | 24 GiB MEM  |

If your Organization needs an instance type that supports a larger worker size, contact [Astronomer support](https://support.astronomer.io). For more information about configuring worker size on Astro, see [Configure a Deployment](configure-deployment-resources.md).

## Related documentation

- [Create a new cluster on Astro](create-cluster.md)
- [Manage and modify clusters](modify-cluster.md)