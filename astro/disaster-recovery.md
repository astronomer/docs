---
sidebar_label: 'Disaster Recovery'
title: 'Disaster Recovery'
id: disaster-recovery
description: Learn how Astronomer handles disaster recovery scenarios and how to best prepare your environment.
---

## Overview

The Astro Data Plane is designed to withstand and survive in-region Availability Zone (AZ) degradations and outages as described in [Resilience](resilience.md).

To withstand a full region outage and achieve near real-time recovery, Astronomer recommends provisioning at least two Astro Clusters in alternate regions. For example, one Cluster in AWS `us-east-1` and another in `us-west-2`. To ensure that both the primary and secondary Clusters are in sync, we recommend deploying all changes to both.

To simplify the responsibility of maintaining two Clusters, Astronomer plans to invest in Cluster and Deployment syncing strategies in 2022. If you're interested in this functionality, please reach out and share feedback with [Astronomer Support](https://support.astronomer.io/).

## Full Region Outages

In the case of a full region outage, Astronomer can re-provision your Cluster(s) and all Deployments in an alternate region. The re-provisioning includes:

- Cluster, including all nodes and most Cluster-level configuration.
- VPC.
- VPC Peering. Customers will need to re-accept peering request.
- Deployments and data pipelines.
- Environment Variables.
- API Keys.
- Alert Emails.

Astronomer will not be able to restore:

- VPC Routes configured by customers via AWS console.
- VPC Security Group rules configured by customers via AWS console.
- DAG history and task logs.
- XComs.
- Airflow configurations (Variables, Connections, Pools) configured via the Airflow UI. Any configurations set via your deployed Astro project image can still be recovered.

Organization settings, Workspace settings, and user management configured in Astro's Control Plane will be unaffected by a region failure in the Data Plane.

Astronomer plans to introduce self-serve and automation enhancements as part of our 2022 roadmap. Please submit feedback to [Astronomer Support](https://support.astronomer.io/) if you are interested in joining the conversation.
