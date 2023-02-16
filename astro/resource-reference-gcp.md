---
sidebar_label: "GCP cluster settings"
title: "GCP cluster settings"
id: resource-reference-gcp
description: Reference of all supported infrastructure and configurations for new Astro clusters on Google Cloud Platform (GCP).
sidebar_custom_props: { icon: 'img/gcp.png' }
---

Unless otherwise specified, new Clusters on Google Cloud Platform (GCP) are created with a set of default resources that our team has deemed appropriate for most use cases.

Read the following document for a reference of our default resources as well as supported cluster configurations.

## Default cluster values

| Resource                                                                                             | Description                                                                                                                                                                                                                                                                               | Quantity/ Default Size                                                                     | Configurable  |
| ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------- |
| [GKE Cluster](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview)   | A GKE cluster is required to run the Astro data plane, which hosts the resources and data required to execute Airflow tasks. Workload Identity is enabled on this cluster.                                                                                                                | 1x, IP Ranges are `172.21.0.0/19` for cluster IPs and `172.22.0.0/19` for cluster services |               |
| Worker node pool                                                                                     | A node pool that hosts all workers with the `default` worker type for all Deployments in the cluster. The number of nodes in the pool auto-scales based on the demand for workers in your cluster. You can configure additional worker node pools to run tasks on different worker types. | 1x pool of e2-standard-4 nodes                                                             | ✔️             |
| Airflow node pool                                                                                    | A node pool that runs all core Airflow components, including the scheduler and webserver, for all Deployments in the cluster. This node pool is fully managed by Astronomer.                                                                                                              | 1x pool of n2-standard-4 nodes                                                             |               |
| Astro system node pool                                                                               | A node pool that runs all other system components required in Astro. The availability zone determines how many nodes are created. This node pool is fully managed by Astronomer.                                                                                                          | 1x pool of n2-standard-4 nodes                                                             |               |
| [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres)                               | The Cloud SQL instance is the primary database for the Astro data plane. It hosts the metadata database for each Airflow Deployment hosted on the GKE cluster.                                                                                                                            | 1x regional instance with 4 vCPUs, 16GB memory                                             |               |
| [VPC](https://cloud.google.com/vpc/docs/vpc)                                                         | Virtual private network for hosting GCP resources                                                                                                                                                                                                                                         | 1x /19                                                                                     | ✔️             |
| [Subnet](https://cloud.google.com/vpc/docs/subnets)                                                  | A single subnet is provisioned in the VPC.                                                                                                                                                                                                                                                | 1, IP Range is `172.20.0.0/19`                                                             |               |
| [Service Network Peering](https://cloud.google.com/vpc/docs/configure-private-services-access)       | The Astro VPC is peered to the Google Service Networking VPC.                                                                                                                                                                                                                             | 1, IP Range is `172.23.0.0/19`                                                             |               |
| [NAT Router (External)](https://cloud.google.com/nat/docs/overview)                                  | Required for connectivity with the Astro control plane and other public services                                                                                                                                                                                                          | 1.                                                                                         |               |
| [Workload Identity Pool](https://cloud.google.com/iam/docs/manage-workload-identity-pools-providers) | Astro uses the fixed Workload Identity Pool for your cluster. One is created if it does not exist.                                                                                                                                                                                        | `PROJECT_ID.svc.id.goog`                                                                   |               |
| [Google Cloud Storage (GCS) Bucket](https://cloud.google.com/storage/docs/creating-buckets)          | Stores Airflow task logs.                                                                                                                                                                                                                                                                 | 1 bucket with name `airflow-logs-<clusterid>`                                              |
| Maximum Node Count                                                                                   | The maximum number of worker nodes that your Astro cluster can support. When this limit is reached, your Astro cluster can't auto-scale and worker Pods may fail to schedule.                                                                                                             | 20                                                                                         | ✔️             |

## Supported cluster configurations

You might need to modify configurations of a new or existing cluster on Astro. This section provides a reference for cluster configuration options.

To create a new cluster on Astro with a specified configuration, see [Create a cluster](create-cluster.md). To request a change to an existing cluster, see [Modify a cluster](modify-cluster.md). Astronomer is currently responsible for completing all cluster configuration changes.

### Cluster regions

Depending on how you installed Astro, you can host Astro clusters in the following GCP regions:

| Code                      | Name                          | Astro - Bring Your Own Cloud | Astro - Hosted |
| ------------------------- | ----------------------------- | ---------------------------- | -------------- |
| `asia-east1`              | Taiwan, Asia                  | ✔️                            |                |
| `asia-northeast1`         | Tokyo, Asia                   | ✔️                            | ✔️              |
| `asia-northeast2`         | Osaka, Asia                   | ✔️                            |                |
| `asia-northeast3`         | Seoul, Asia                   | ✔️                            |                |
| `asia-south1`             | Mumbai, Asia                  | ✔️                            |                |
| `asia-south2`             | Delhi, Asia                   | ✔️                            |                |
| `asia-southeast1`         | Singapore, Asia               | ✔️                            |                |
| `asia-southeast2`         | Jakarta, Asia                 | ✔️                            |                |
| `australia-southeast1`    | Sydney, Australia             | ✔️                            | ✔️              |
| `australia-southeast2`    | Melbourne, Australia          | ✔️                            |                |
| `europe-central2`         | Warsaw, Europe                | ✔️                            |                |
| `europe-north1`           | Finland, Europe               | ✔️                            |                |
| `europe-southwest1`       | Madrid, Europe                | ✔️                            |                |
| `europe-west1`            | Belgium, Europe               | ✔️                            | ✔️              |
| `europe-west2`            | England, Europe               | ✔️                            | ✔️              |
| `europe-west3`            | Frankfurt, Europe             | ✔️                            |                |
| `europe-west4`            | Netherlands, Europe           | ✔️                            |                |
| `europe-west6`            | Zurich, Europe                | ✔️                            |                |
| `europe-west8`            | Milan, Europe                 | ✔️                            |                |
| `europe-west9`            | Paris, Europe                 | ✔️                            |                |
| `northamerica-northeast1` | Montreal, North America       | ✔️                            |                |
| `northamerica-northeast2` | Toronto, North America        | ✔️                            |                |
| `southamerica-east1`      | Sau Paolo, South America      | ✔️                            |                |
| `southamerica-west1`      | Santiago, South America       | ✔️                            |                |
| `us-central1`             | Iowa, North America           | ✔️                            | ✔️              |
| `us-east1`                | South Carolina, North America | ✔️                            |                |
| `us-east4`                | Virginia, North America       | ✔️                            | ✔️              |
| `us-east5`                | Columbus, North America       | ✔️                            |                |
| `us-south1`               | Dallas, North America         | ✔️                            |                |
| `us-west1`                | Oregon, North America         | ✔️                            |                |
| `us-west2`                | Los Angeles, North America    | ✔️                            |                |
| `us-west3`                | Salt Lake City, North America | ✔️                            |                |
| `us-west4`                | Nevada, North America         | ✔️                            |                |

Modifying the region of an existing Astro cluster isn't supported. If you're interested in a GCP region that isn't listed, contact [Astronomer support](https://cloud.astronomer.io/support).

### Worker node pools

A node pool is a group of nodes within a cluster that all have the same configuration. On Astro, worker nodes are responsible for running the Pods that execute Airflow tasks. Each worker node pool can be configured with a node instance type and a maximum node count. All Astro clusters have one worker node pool by default, but you can configure additional node pools to optimize resource usage.

If your cluster has multiple worker node pools with different worker node instance types, users in your organization can configure tasks to run on those worker types using [worker queues](configure-deployment-resources.md#worker-queues). To enable a new worker type for your cluster, contact [Astronomer support](https://cloud.astronomer.io/support) with a request to create a new node pool or modify an existing node pool.

Astronomer monitors your usage and the number of nodes deployed in your cluster. When your Airflow use increases, Astronomer support might contact you and provide recommendations for updating your node pools to optimize your infrastructure costs or increase the efficiency of your tasks.

### Worker node resource reference

Each worker node in a pool runs a single worker Pod. A worker Pod's actual available size is equivalent to the total capacity of the instance type minus Astro’s system overhead.

The following table lists all available instance types for worker node pools, as well as the Pod size that is supported for each instance type. As the system requirements of Astro change, these values can increase or decrease.

| Node Instance Type | CPU    | Memory       |
| ------------------ | ------ | ------------ |
| e2-standard-4      | 3 CPUs | 13 GiB MEM   |
| e2-standard-8      | 7 CPUs | 29 GiB MEM   |
| e2-standard-16     | 15 CPUs| 61 GiB MEM   |
| e2-highmem-4       | 3 CPUs | 29 GiB MEM   |
| e2-highmem-8       | 7 CPUs | 61 GiB MEM   |
| e2-highmem-16      | 15 CPUs| 125 GiB MEM  |
| e2-highcpu-4       | 3 CPUs | 1 GiB MEM    |
| e2-highcpu-8       | 7 CPUs | 5 GiB MEM    |
| e2-highcpu-16      | 15 CPUs| 13 GiB MEM   |
| n2-standard-4      | 3 CPUs | 13 GiB MEM   |
| n2-standard-8      | 7 CPUs | 29 GiB MEM   |
| n2-standard-16     | 15 CPUs| 61 GiB MEM   |
| n2-highmem-4       | 3 CPUs | 29 GiB MEM   |
| n2-highmem-8       | 7 CPUs | 61 GiB MEM   |
| n2-highmem-16      | 15 CPUs| 125 GiB MEM  |
| n2-highcpu-4       | 3 CPUs | 1 GiB MEM    |
| n2-highcpu-8       | 7 CPUs | 5 GiB MEM    |
| n2-highcpu-16      | 15 CPUs| 13 GiB MEM   |
| c2-standard-4      | 3 CPUs | 13 GiB MEM   |
| c2-standard-8      | 7 CPUs | 29 GiB MEM   |

If your Organization is interested in using an instance type that supports a larger worker size, contact [Astronomer support](https://cloud.astronomer.io/support). For more information about configuring worker size on Astro, see [Configure a Deployment](configure-deployment-resources.md).

### Maximum node count

Each Astro cluster has a limit on how many nodes it can run at once. This maximum includes worker nodes as well as system nodes managed by Astronomer.

The default maximum node count for all nodes across your cluster is 20. A cluster's node count is most affected by the number of worker Pods that are executing Airflow tasks. See [Worker autoscaling logic](configure-worker-queues.md#worker-autoscaling-logic).

If the node count for your cluster reaches the maximum node count, new tasks might not run or get scheduled. Astronomer monitors maximum node count and is responsible for contacting your organization if it is reached. To check your cluster's current node count, contact [Astronomer Support](https://cloud.astronomer.io/support).
