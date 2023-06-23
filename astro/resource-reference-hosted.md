---
sidebar_label: "Resource reference"
title: "Astro Hosted resource reference"
id: resource-reference-hosted
description: Reference of all supported infrastructure for new Astro Hosted clusters.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::caution

This document applies only to [Astro Hosted](astro-architecture.md). To see whether you're an Astro Hosted user, click the Astronomer logo in the upper left corner of the Cloud UI and go to **Settings** > **General**. Your Astro product type is listed under **Product Type**.

For Astro Hybrid resource reference material, see:

- [AWS Hybrid cluster settings](resource-reference-gcp-hybrid.md)
- [Azure Hybrid cluster settings](resource-reference-gcp-hybrid.md)
- [GCP Hybrid cluster settings](resource-reference-gcp-hybrid.md)

:::

This page contains reference information for all supported Astro Hosted Deployment and cluster resource configurations. Use this information to determine whether Astro supports the type of Airflow environment you want to run. 

If you're interested in a cloud region or resource size that's not mentioned here, reach out to [Astronomer support](https://cloud.astronomer.io/support).

## Deployment resources

Astro supports Deployments with varying levels of resource usage.

### Scheduler 

Astronomer Deployments run a single scheduler. You can configure your scheduler to have different amounts of resources based on how many tasks you need to schedule. The following table lists all possible scheduler sizes:

| Scheduler size | vCPU | Memory |
| -------------- | ---- | ------ |
| Small          | 1    | 2G     |
| Medium         | 2    | 4G     |
| Large          | 4    | 8G     |

### Worker type

Each Deployment worker queue has a _worker type_ that determines how many resources are available to your Airflow workers for running tasks. A worker type is a virtualized instance of CPU and memory on your cluster that is specific to the Astro platform. The underlying node instance type running your worker can vary based on how Astro optimizes resource usage on your cluster.

Each virtualized instance of your worker type is a _worker_. Celery workers can run multiple tasks at once, while Kubernetes workers only scale up and down to run a single task at a time. For more information about configuring worker behavior, see [Worker queues](configure-worker-queues.md).

The following table lists all available worker types on Astro Deployments. 

| Worker Type | vCPU | Memory |
| ----------- | ---- | ------ |
| A5          | 1    | 2G     |
| A10         | 2    | 4G     |
| A20         | 4    | 8G     |

All worker types additionally have 5 GiB of ephemeral storage that your tasks can use when storing small amounts of data within the worker. 

## Standard cluster configurations

A _standard cluster_ is a multi-tenant cluster that's hosted and managed by Astronomer. Astronomer maintains standard clusters in a limited regions and clouds, with support for more regions and clouds coming soon.

Currently, standard clusters are available on the following clouds and regions:

| Cloud    | Code          | Region                  |
| -------- | ------------- | ----------------------- |
| **GCP** | `us-central1` | Iowa, North America     |
| **GCP** | `us-east4`    | Virginia, North America |


## Dedicated cluster configurations

A _dedicated cluster_ is cluster that Astronomer provisions solely for use by your Organization. You can create new dedicated clusters from the Cloud UI in a variety of clouds and regions. To configure dedicated clusters, see [Create a dedicated cluster](create-dedicated-cluster.md).

Currently, dedicated clusters are available on the following clouds and regions:

<Tabs
    defaultValue="aws"
    groupId= "dedicated-cluster-configurations"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
        {label: 'Azure', value: 'azure'},
    ]}>
<TabItem value="aws">

| Code             | Region                |
| ---------------- | --------------------- |
| `ap-northeast-1` | Asia Pacific (Tokyo)  |
| `ap-southeast-2` | Asia Pacific (Sydney) |
| `eu-central-1`   | Europe (Frankfurt)    |
| `eu-west-1`      | Europe (Ireland)      |
| `us-east-1`      | US East (N. Virginia) |
| `us-west-2`      | US West (Oregon)      |

</TabItem>

<TabItem value="azure">

| Code            | Region         |
| --------------- | -------------- |
| `australiaeast` | Australia East |
| `eastus2`       | East US 2      |
| `japaneast`     | Japan East     |
| `northeurope`   | North Europe   |
| `westeurope`    | West Europe    |
| `westus2`       | West US 2      |

</TabItem>

<TabItem value="gcp">

| Code                   | Region                  |
| ---------------------- | ----------------------- |
| `asia-northeast1`      | Tokyo, Asia             |
| `australia-southeast1` | Sydney, Australia       |
| `europe-west1`         | Belgium, Europe         |
| `europe-west2`         | England, Europe         |
| `us-central1`          | Iowa, North America     |
| `us-east4`             | Virginia, North America |

</TabItem>

</Tabs>
