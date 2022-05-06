---
sidebar_label: 'Modify a Cluster'
title: "Modify a Cluster on Astro"
id: modify-cluster
description: Request changes to an existing Astro Cluster.
---

## Overview

Unless otherwise specified, new Clusters on Astro are created with a set of default configurations. Depending on your use case, you may decide that you want to modify an existing Cluster to run a different configuration.

For example, if you have a new set of DAGs that require significantly more CPU and Memory than your existing workloads, you may be interested in modifying a Cluster on AWS to run `m5.8xlarge` nodes instead of `m5.4xlarge` nodes. You might also want to modify a Cluster's maximum node count from the default of 20 to better fit your expected workload.

## Prerequisites

To complete this setup, you need to have:

- A Cluster on Astro.
- Permission from your team.

If you don't have a Cluster on Astro, follow the instructions to [Install Astro on AWS](install-aws.md) or [GCP](install-gcp.md). If you have an existing Cluster and are interested in creating additional Clusters, read [Create a Cluster](create-cluster.md).

## Step 1: Submit a Request to Astronomer

To modify an existing Cluster in your Organization, first verify that the change you want to make is supported by reading the resource reference documentation for either [AWS](resource-reference-aws.md) or [GCP](resource-reference-gcp.md). Then, reach out to [Astronomer Support](https://support.astronomer.io).

## Step 2: Confirm with Astronomer

Once our team validates that the Cluster configuration you requested is supported, we will let you know as soon as we are able to perform the change.

Modifications to an existing Cluster may take a few minutes to complete, but you can expect no downtime during the process. Astro is built to ensure a graceful rollover, which means that the Airflow and Cloud UIs will continue to be available and your Airflow tasks will not be affected.
