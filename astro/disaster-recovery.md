---
sidebar_label: 'Disaster recovery'
title: 'Disaster recovery'
id: disaster-recovery
description: Learn how Astronomer handles disaster recovery scenarios and how to best prepare your environment.
---

The Astro Data Plane is designed to withstand and survive in-region Availability Zone (AZ) degradations and outages as described in [Resilience](resilience.md).

To withstand a full region outage and achieve near real-time recovery, Astronomer recommends provisioning at least two Astro clusters in alternate regions. For example, one cluster in AWS `us-east-1` and another in `us-west-2`. To ensure that both the primary and secondary clusters are in sync, we recommend deploying all changes to both.

## Full region outages

In the case of a full region outage, Astronomer can re-provision your Cluster(s) and all Deployments in an alternate region. The re-provisioning includes:

- Cluster, including all nodes and most cluster-level configuration.
- VPC.
- VPC peering. Customers will need to re-accept peering request.
- Deployments and data pipelines.
- Environment variables.
- API keys.
- Alert emails.

Astronomer will not be able to restore:

- VPC Routes configured by customers with the AWS console.
- VPC Security Group rules configured by customers with the AWS console.
- The Airflow metadata database for Deployments, including:
    - DAG history and task logs.
    - XComs.
    - Airflow configurations (Variables, Connections, Pools) configured with the Airflow UI. Any configurations set with your deployed Astro Runtime image or environment variables can be recovered.

Organization settings, Workspace settings, and user management configured in Astro's control plane will be unaffected by a region failure in the data plane.

Astronomer plans to introduce self-serve and automation enhancements as part of its product roadmap. Please submit feedback to [Astronomer support](https://support.astronomer.io/) if you are interested in joining the conversation.
