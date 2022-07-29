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
| Max Node Count | The maximum number of EC2 nodes that your Astro Cluster can support at any given time. Once this limit is reached, your Cluster cannot auto-scale and worker pods may fail to schedule. | 20 |


## Supported Cluster Configurations

Depending on the needs of your team, you may be interested in modifying certain configurations of a new or existing Cluster on Astro. This section provides a reference for which configuration options are supported during the install process.

To create a new Cluster on Astro with a specified configuration, read [Install on GCP](install-gcp.md) or [Create a Cluster](create-cluster.md). For instructions on how to make a change to an existing Cluster, read [Modify a Cluster](modify-cluster.md).

### GCP Region

Astro supports the following GCP regions:

- `us-central1`
- `us-west1`
- `us-east1`
- `europe-west4`

Modifying the region of an existing Cluster on Astro is not supported. If you're interested in a GCP region that is not on this list, reach out to [Astronomer Support](https://support.astronomer.io).

### Node Instance Type

Astro supports different GCP machine types. Machine types comprise of varying combinations of CPU, memory, storage, and networking capacity. All system and Airflow components within a single Cluster are powered by the nodes specified during the Cluster creation or modification process.

- e2-standard-4
- e2-standard-8

For detailed information on each instance type, see [GCP documentation](https://cloud.google.com/compute/docs/machine-types). If you're interested in a machine type that is not on this list, reach out to [Astronomer Support](https://support.astronomer.io/). Not all machine types are supported in all GCP regions.
