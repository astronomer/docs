---
sidebar_label: "Connect to External Services"
title: "Connect Astro to External Data Services"
id: connectivity
description: Learn how to connect Astro to different types of external data sources.
---

## Overview

Before you can orchestrate your data in Astro, you first need to make your data accessible to your Astro Deployments running in the Data Plane. This guide explains how to connect your Astro Clusters to external data sources using the following methods:

- Public Endpoints
- VPC

If you need to connect to a different type of data source than the ones documented here, reach out to [Astronomer support](https://support.astronomer.io).

## Public Endpoints

The fastest and easiest way to connect Astro to an external data source is by using the data source's publicly accessible endpoints.

These endpoints can be configured by:

- Setting [Environment Variables](environment-variables.md) with your endpoint information.
- Creating an [Airflow Connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

Public connection traffic moves directly between your Data Plane and the external data source's API endpoint, meaning that the data in this traffic never reaches your Astronomer-managed Control Plane.

### IP Allowlist

Some data services, such as Snowflake and Databricks, provide an additional layer of security by requiring you to allowlist a specific IP address before you can access the service.

Each Cluster has a pair of unique external IP address that will persist for the life of the Cluster. These IP addresses are assigned for network address translation, meaning that they're responsible for all outbound traffic from your Cluster to the internet. To retrieve an IP for a given Cluster, open a ticket with [Astronomer support](https://support.astronomer.io) and request it. If you have more than one Cluster, you will need to allowlist each Cluster individually on your data service provider.

## VPC Peering

Each Cluster runs in a dedicated VPC. To set up private connectivity between the Astro VPC and a target VPC, you can set up a VPC peering connection. Peered VPCs provide additional security by ensuring private connectivity, reduced network transit costs, and simplified network layouts.

To create a VPC peering connection between a Cluster's VPC and a target VPC, open a support ticket with Astronomer and provide the following information about your Cluster:

- Name of your Cluster
- AWS account
- AWS Region
- VPC CIDR

In response, Astronomer will initiate a peering request. This peering request must be accepted by the owner of the target VPC.

Once peering is set up, continue to work with [Astronomer support](https://support.astronomer.io) and the owner of the target VPC to update the routing tables of both VPCs to direct traffic to each other.

### DNS Considerations with VPC Peering

To resolve DNS hostnames from your target VPC, your Cluster VPC has **DNS Hostnames**, **DNS Resolutions**, and **Requester DNS Resolution** enabled via AWS [Peering Connection settings](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).  

If your target VPC also resolves DNS hostnames via **DNS Hostnames** and **DNS Resolution**, you must also enable the **Accepter DNS Resolution** setting. This allows the Data Plane to resolve the public DNS hostnames of the target VPC to its private IP addresses. To configure this option, see [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If your target VPC resolves DNS hostnames using [private hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html), then you must associate your Route53 private hosted zone with the Astronomer VPC using instructions provided in [AWS Documentation](https://aws.amazon.com/premiumsupport/knowledge-center/route53-private-hosted-zone/). You can retrieve the ID of the Astronomer VPC by contacting [Astronomer support](https://support.astronomer.io).
