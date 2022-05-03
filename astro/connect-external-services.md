---
sidebar_label: "Connect to External Services"
title: "Connect Astro to External Data Services"
id: connect-external-services
description: Learn how to connect your Astro Data Plane to different types of external data services.
---

## Overview

Before you can run pipelines on Astro with real data, you first need to make your data services accessible to your Data Plane and the Deployments running within it. This guide explains how to securely connect Astro to external data services using the following methods:

- Public Endpoints
- VPC Peering

If you need to connect to a type of data service that requires a connectivity method that is not documented here, reach out to [Astronomer support](https://support.astronomer.io).

## Public Endpoints

The fastest and easiest way to connect Astro to an external data service is by using the data service's publicly accessible endpoints.

These endpoints can be configured by:

- Setting [environment variables](environment-variables.md) on Astro with your endpoint information.
- Creating an [Airflow Connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) with your endpoint information.

Public connection traffic moves directly between your Data Plane and the external data service's API endpoint. This means that the data in this traffic never reaches the Control Plane, which is managed by Astronomer.

### IP Allowlist

Some data services, including Snowflake and Databricks, provide an additional layer of security by requiring you to allowlist a specific IP address before you can access the service.

On Astro, each Cluster has a pair of unique external IP address that will persist throughout the lifetime of the Cluster. These IP addresses are assigned for network address translation, which means that they are responsible for all outbound traffic from your Astro Cluster to the internet. To retrieve the IP addresses for a given Cluster, open a ticket with [Astronomer support](https://support.astronomer.io) and request it. If you have more than one Cluster, you will need to allowlist each Cluster individually on your data service provider.

## VPC Peering

Each Cluster on Astro runs in a dedicated VPC. To set up private connectivity between an Astro VPC and another VPC, you can set up a VPC peering connection. Peered VPCs provide additional security by ensuring private connectivity, reduced network transit costs, and simplified network layouts.

To create a VPC peering connection between an Astro Cluster's VPC and a target VPC, reach out to [Astronomer support](https://support.astronomer.io) and provide the following information:

- Astro Cluster ID and Name
- AWS Account ID of the target VPC
- AWS Region of the target VPC
- VPC ID of the target VPC
- CIDR of the target VPC

From there, Astronomer will initiate a peering request. To connect successfully, this peering request must be accepted by the owner of the target VPC.

Once peering is set up, the owner of the target VPC can expect to continue to work with our team to update the routing tables of both VPCs to direct traffic to each other.

### DNS Considerations with VPC Peering

To resolve DNS hostnames from your target VPC, your Cluster VPC has **DNS Hostnames**, **DNS Resolutions**, and **Requester DNS Resolution** enabled via AWS [Peering Connection settings](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).  

If your target VPC resolves DNS hostnames via **DNS Hostnames** and **DNS Resolution**, you must also enable the **Accepter DNS Resolution** setting. This allows the Data Plane to resolve the public DNS hostnames of the target VPC to its private IP addresses. To configure this option, see [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If your target VPC resolves DNS hostnames using [private hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html), then you must associate your Route53 private hosted zone with the Astronomer VPC using instructions provided in [AWS Documentation](https://aws.amazon.com/premiumsupport/knowledge-center/route53-private-hosted-zone/). You can retrieve the ID of the Astronomer VPC by contacting [Astronomer support](https://support.astronomer.io).
