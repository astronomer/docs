---
sidebar_label: "GCP Resource Reference"
title: "Resources Required for Astro on GCP"
id: resource-reference-gcp
description: Reference of all supported configurations for new Clusters on Astro in Google Cloud Platform (GCP).
---

## Overview

Unless otherwise specified, new Clusters on Google Cloud Platform (GCP) are created with a set of default resources that our team has deemed appropriate for most use cases.

Read the following document for a reference of our default resources as well as supported Cluster configurations.

## Default Cluster Values

| Resource                | Description                                                                                          | Quantity/Default Size        |
| ----------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------- |
| [VPC](https://cloud.google.com/vpc/docs/vpc)                     | Virtual private network for hosting GCP resources                                                                | 1x /19                            |
| [Subnet](https://cloud.google.com/vpc/docs/subnets)                  | A single subnet is provisioned in the VPC                                                            | 1, IP Range is `172.20.0.0/19` |
| [Service Network Peering](https://cloud.google.com/vpc/docs/configure-private-services-access) | The Astro VPC is peered to the Google Service Networking VPC                                         | 1, IP Range is `172.23.0.0/19` |
| [NAT Router (External)](https://cloud.google.com/nat/docs/overview)   | Required for connectivity with the Astro Control Plane and other public services                     | 1                            |
| [GKE Cluster](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview)             | A GKE cluster is required to run the Astro Data Plane. Workload Identity is enabled on this cluster. | 1, IP Ranges are `172.21.0.0/19` for Cluster IPs and `172.22.0.0/19` for Cluster Services |
| [Workload Identity Pool](https://cloud.google.com/iam/docs/manage-workload-identity-pools-providers) | Astro uses the fixed Workload Identity Pool for your project; one is created if it does not exist | The default pool (PROJECT_ID.svc.id.goog) is used |
| [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres) | The Cloud SQL instance is the primary database for the Astro Data Plane. It hosts the metadata database for each Airflow Deployment hosted on the GKE cluster | 1 Regional Instance with 4 vCPUs, 16GB Memory |
| Storage Bucket | GCS Bucket for storage of Airflow task logs | 1 bucket with name `airflow-logs-<clusterid>` |
| Nodes | Nodes power the Data Plane and Airflow components. Nodes autoscale as deployments are added. | 3x n2-medium-4 for the system nodes; worker nodes default to e2-medium-4 and are provisioned as required, up to Max Node Count |
| Max Node Count | The maximum number of worker nodes that your Astro Cluster can support at any given time. Once this limit is reached, your Cluster cannot auto-scale and worker pods may fail to schedule. | 20 |


## Supported Cluster Configurations

Depending on the needs of your team, you may be interested in modifying certain configurations of a new or existing Cluster on Astro. This section provides a reference for which configuration options are supported during the install process.

To create a new Cluster on Astro with a specified configuration, read [Install on GCP](install-gcp.md) or [Create a Cluster](create-cluster.md). For instructions on how to make a change to an existing Cluster, read [Modify a Cluster](modify-cluster.md).

### GCP Region

Astro supports the following GCP regions:

- `asia-southeast1` - Singapore, Asia
- `australia-southeast1` - Sydney, Australia
- `europe-west1` - Belgium, Europe
- `europe-west2` - England, Europe
- `europe-west3` - Frankfurt, Europe
- `europe-west4` - Netherlands, Europe
- `southamerica-east1` - Sau Paolo, South America
- `us-central1` - Iowa, North America
- `us-west1` - Oregon, North America
- `us-west2` - Los Angeles, North America
- `us-west4` - Nevada, North America
- `us-east1` - South Carolina, North America
- `us-east4` - Virginia, North America

Modifying the region of an existing Astro Cluster isn't supported. If you're interested in a GCP region that isn't on this list, contact [Astronomer Support](https://support.astronomer.io).

### Node Instance Type

Astro supports different GCP machine types. Machine types comprise of varying combinations of CPU, memory, storage, and networking capacity. All system and Airflow components within a single Cluster are powered by the nodes specified during the Cluster creation or modification process.

- e2-standard-4
- e2-standard-8

For detailed information on each instance type, see [GCP documentation](https://cloud.google.com/compute/docs/machine-types). If you're interested in a machine type that is not on this list, reach out to [Astronomer Support](https://support.astronomer.io/). Not all machine types are supported in all GCP regions.

### Maximum Node Count

Each Astro cluster has a maximum node count, which is the maximum number of worker nodes that can run at any given time on a cluster. This limit does not apply to other nodes such as RDS instances or Astronomer-managed node pools.

The default maximum node count for a cluster is 20. This value can be changed for any cluster by Astronomer.

The number of worker nodes in your cluster [autoscales](configure-deployment-resources.md#worker-autoscaling-logic) based on how many tasks are currently queued or running. If a cluster's worker node count scales to the maximum node count, new tasks can't run or be scheduled.

Reaching the maximum node count also results in the following error in a Deployment's [scheduler logs](view-logs.md):

```text
│   Warning  FailedScheduling  6s (x10 over 11m)  default-scheduler  0/6 nodes are available: 6 Insufficient cpu.                                                                                                                                                                                                    │
│ I1110 19:41:16.548235       1 static_autoscaler.go:392] Max total nodes in cluster reached       
```

If you see this error in a Deployment, reach out to [Astronomer Support](https://support.astronomer.io) and request an increase to your cluster's maximum node count.

### Deployment Worker Size Limits

Worker nodes can be further configured at a Deployment level using the **Worker Resources** setting in the Cloud UI. Using this setting, you can determine how much CPU and memory a worker node uses out of its maximum possible usage.

This following table lists the maximum worker size that is supported on Astro for each worker node instance type. These values can increase or decrease over time as the system requirements of Astro change. If you try to set **Worker Resources** to a size that exceeds the maximum for your Cluster's worker node instance type, an error message appears in the Cloud UI.

| Node Instance Type | Maximum AU | CPU       | Memory       |
|--------------------|------------|-----------|--------------|
| e2-standard-4      | 24         | 2.4 CPUs  | 9    GiB MEM |
| e2-standard-8      | 64         | 6.4 CPUs  | 24   GiB MEM |

If your Organization is interested in using an instance type that supports a worker size limit higher than 64 AU, contact [Astronomer Support](https://support.astronomer.io). For more information about configuring worker size on Astro, see [Configure a Deployment](configure-deployment-resources.md#worker-resources).

:::info

The size limits defined here currently also apply to **Scheduler Resources**, which determines the CPU and memory allocated to the Airflow Scheduler(s) of each Deployment. The maximum Scheduler size on Astro is 30 AU, which means there are some node instance types for which that maximum size is not supported.

For more information about the Scheduler, see [Configure a Deployment](configure-deployment-resources.md#scheduler-resources).

:::
