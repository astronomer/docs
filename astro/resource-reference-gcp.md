---
sidebar_label: "GCP"
title: "GCP cluster configurations"
id: resource-reference-gcp
description: Reference of all supported infrastructure and configurations for new Astro clusters on Google Cloud Platform (GCP).
sidebar_custom_props: { icon: 'img/gcp.png' }
---

Unless otherwise specified, new Clusters on Google Cloud Platform (GCP) are created with a set of default resources that our team has deemed appropriate for most use cases.

Read the following document for a reference of our default resources as well as supported cluster configurations.

## Default cluster values

| Resource                | Description                                                                                          | Quantity/Default Size        |
| ----------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------- |
| [GKE Cluster](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview)             | A GKE cluster is required to run the Astro data plane, which hosts the resources and data required to execute Airflow tasks. Workload Identity is enabled on this cluster. | 1x, IP Ranges are `172.21.0.0/19` for cluster IPs and `172.22.0.0/19` for cluster services |
| [VPC](https://cloud.google.com/vpc/docs/vpc)                     | Virtual private network for hosting GCP resources                                                                | 1x /19                            |
| [Subnet](https://cloud.google.com/vpc/docs/subnets)                  | A single subnet is provisioned in the VPC.                                                            | 1, IP Range is `172.20.0.0/19` |
| Worker node pool | Worker node pools run all Airflow workers or node pools that run all Airflow workers. The number of nodes in the pool auto-scales based on the demand for workers in your cluster. You can configure multiple worker node pools to run tasks on different instance types.| 1x pool of e2-standard-4 nodes |
| Astro system node pool | A node pool that runs all proprietary Astronomer components. The availability zone determines how many nodes are created. This node pool is fully managed by Astronomer.| 1x pool of n2-standard-4 nodes |
| Airflow node pool | A node pool runs all core Airflow components such as the scheduler and webserver. This node pool is fully managed by Astronomer. | 1x pool of n2-standard-4 nodes |
| [Service Network Peering](https://cloud.google.com/vpc/docs/configure-private-services-access) | The Astro VPC is peered to the Google Service Networking VPC.                                         | 1, IP Range is `172.23.0.0/19` |
| [NAT Router (External)](https://cloud.google.com/nat/docs/overview)   | Required for connectivity with the Astro control plane and other public services                     | 1.                            |
| [Workload Identity Pool](https://cloud.google.com/iam/docs/manage-workload-identity-pools-providers) | Astro uses the fixed Workload Identity Pool for your project. One is created if it does not exist. | The default pool (`PROJECT_ID.svc.id.goog`) is used |
| [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres) | The Cloud SQL instance is the primary database for the Astro data plane. It hosts the metadata database for each Airflow Deployment hosted on the GKE cluster. | 1x regional instance with 4 vCPUs, 16GB memory |
| [Google Cloud Storage (GCS) Bucket](https://cloud.google.com/storage/docs/creating-buckets) | GCS bucket to store Airflow task logs. | 1 bucket with name `airflow-logs-<clusterid>` |
| Maximum Node Count | The maximum number of worker nodes that your Astro cluster can support. When this limit is reached, your Astro cluster can't auto-scale and worker Pods may fail to schedule. | 20 |
| [Workload Identity Pool](https://cloud.google.com/iam/docs/manage-workload-identity-pools-providers) | Astro uses the fixed Workload Identity Pool for your project. One is created if it does not exist | The default pool (`PROJECT_ID.svc.id.goog`) is used |
| [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres) | The Cloud SQL instance is the primary database for the Astro data plane. It hosts the metadata database for each Airflow Deployment hosted on the GKE cluster | 1x regional instance with 4 vCPUs, 16GB memory |
| Google Cloud Storage (GCS) Bucket | GCS bucket to store Airflow task logs | 1 bucket with name `airflow-logs-<clusterid>` |
| Worker node pools | Node pools run all Airflow workers. The number of nodes in the pool auto-scales based on the demand for workers in your cluster. You can configure multiple worker node pools to run tasks on different instance types| 1x pool of e2-standard-4 nodes |
| Astro node pool | A node pool runs all proprietary Astronomer components. This node pool is fully managed by Astronomer| 1x pool of e2-standard-4 nodes |
| Airflow node pool | A node pool runs all core Airflow components such as the scheduler and webserver. This node pool is fully managed by Astronomer | 1x pool of e2-standard-4 nodes |
| Maximum Node Count | The maximum number of worker nodes that your Astro cluster can support. When this limit is reached, your cluster can't auto-scale and worker Pods may fail to schedule. | 20 |


## Supported cluster configurations

Depending on the needs of your team, you may be interested in modifying certain configurations of a new or existing cluster on Astro. This section provides a reference for which configuration options are supported during the install process.

To create a new cluster on Astro with a specified configuration, read [Install on GCP](install-gcp.md) or [Create a cluster](create-cluster.md). For instructions on how to make a change to an existing cluster, see [Modify a cluster](modify-cluster.md).

### Supported regions

Astro supports the following Google Cloud Platform (GCP) regions:

- `asia-east1` - Taiwan, Asia
- `asia-northeast1` - Tokyo, Asia
- `asia-northeast2` - Osaka, Asia
- `asia-northeast3` - Seoul, Asia
- `asia-south1` - Mumbai, Asia
- `asia-south2` - Delhi, Asia
- `asia-southeast1` - Singapore, Asia
- `asia-southeast2` - Jakarta, Asia
- `australia-southeast1` - Sydney, Australia
- `australia-southeast2` - Melbourne, Australia
- `europe-central2` - Warsaw, Europe
- `europe-north1` - Finalnd, Europe
- `europe-southwest1` - Madrid, Europe
- `europe-west1` - Belgium, Europe
- `europe-west2` - England, Europe
- `europe-west3` - Frankfurt, Europe
- `europe-west4` - Netherlands, Europe
- `europe-west6` - Zurich, Europe
- `europe-west8` - Milan, Europe
- `europe-west9` - Paris, Europe
- `northamerica-northeast1` - Montreal, North America
- `northamerica-northeast2` - Toronto, North America
- `southamerica-east1` - Sau Paolo, South America
- `southamerica-west1` - Santiago, South America
- `us-central1` - Iowa, North America
- `us-east1` - South Carolina, North America
- `us-east4` - Virginia, North America
- `us-east5` - Columbus, North America
- `us-south1` - Dallas, North America
- `us-west1` - Oregon, North America
- `us-west2` - Los Angeles, North America
- `us-west3` - Salt Lake City, North America
- `us-west4` - Nevada, North America

Modifying the region of an existing Astro cluster isn't supported. If you're interested in a GCP region that isn't on this list, contact [Astronomer support](https://cloud.astronomer.io/support).

### Worker node pools

Node pools are a scalable collection of worker nodes with the same instance type. These nodes are responsible for running the Pods that execute Airflow tasks. If your cluster has a node pool for a specific instance type, you can configure tasks to run on those instance types using [worker queues](configure-deployment-resources.md#worker-queues). To make an instance type available in a cluster, reach out to [Astronomer support](https://cloud.astronomer.io/support) with a request to create a new node pool for the specific instance type. Note that not all machine types are supported in all GCP regions.

Astronomer monitors your usage and number of nodes deployed in your cluster. As your usage of Airflow increases, Astronomer might reach out with recommendations for updating your node pools to optimize your infrastructure spend or increase the efficiency of your tasks.

### Worker node size resource reference

Each worker node in a pool runs a single worker Pod. A worker Pod's actual available size is equivalent to the total capacity of the instance type minus Astro’s system overhead.

The following table lists all available instance types for worker node pools, as well as the Pod size that is supported for each instance type. As the system requirements of Astro change, these values can increase or decrease.

| Node Instance Type | CPU       | Memory       |
|--------------------|-----------|--------------|
| e2-standard-4      | 2 CPUs    | 7.5  GiB MEM |
| e2-standard-8      | 6 CPUs    | 22.5 GiB MEM |

If your Organization is interested in using an instance type that supports a larger worker size, contact [Astronomer support](https://cloud.astronomer.io/support). For more information about configuring worker size on Astro, see [Configure a Deployment](configure-deployment-resources.md).

### Maximum node count

Each Astro cluster has a limit on how many nodes it can run at once. This maximum includes worker nodes as well as system nodes managed by Astronomer.

The default maximum node count for all nodes across your cluster is 20. A cluster's node count is most affected by the number of worker Pods that are executing Airflow tasks. See [Worker autoscaling logic](configure-deployment-resources.md#worker-autoscaling-logic).

If the node count for your cluster reaches the maximum node count, new tasks might not run or get scheduled. Astronomer monitors maximum node count and is responsible for contacting your organization if it is reached. To check your cluster's current node count, contact [Astronomer Support](https://cloud.astronomer.io/support).
