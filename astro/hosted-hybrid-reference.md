---
sidebar_label: "Hosted vs. Hybrid features"
title: "Astro Hosted vs. Astro Hybrid feature differences"
id: hosted-hybrid-reference
---

[Astro Hosted](astro-architecture.md), also known simply as **Astro**, is a fully-managed SaaS application for Apache Airflow. [Astro Hybrid](hybrid-overview.md) is a self-hosted, Astronomer-managed Airflow service. Due to the difference in architecture between these products, some features are available only on a specific architecture.

Use this guide to understand which features are exclusive to Astro Hosted or Astro Hybrid. If a feature isn't listed here, it's available in both products. 

## Astro Hosted-exclusive features

- [Deployment health incidents](deployment-health-incidents.md)
- Specific resource authorization strategies, such as [attaching a service account to a Deployment](https://www.astronomer.io/docs/astro/authorize-deployments-to-your-cloud?tab=gcp#setup)
- Self-service VPC peering
- [Deploy history and rollbacks](deploy-history.md)
- [Run a deprecated Astro Runtime version](upgrade-runtime.md#run-a-deprecated-astro-runtime-version)
- The [Astro Environment Manager](create-and-link-connections.md)
- **Billing** page in the Astro UI
- The [cost breakdown](organization-dashboard.md#cost-breakdown) Organization dashboard

## Astro Hybrid-exclusive features

- Configurable metadata database instance types. For example, see [available RDS instance types on AWS](resource-reference-aws-hybrid.md#supported-rds-instance-types).
- Some cloud regions for clusters are available only on Astro Hybrid. For example, see [supported cloud regions on AWS](resource-reference-aws-hybrid.md#supported-cluster-regions).
- Configurable cloud-specific machine types for worker queues. For example, see [supported worker node pool instance types on AWS](resource-reference-aws-hybrid.md#supported-worker-node-pool-instance-types).