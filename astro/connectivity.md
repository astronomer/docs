---
sidebar_label: "Connect to External Services"
title: "Connect Astro to External Data Services"
id: connectivity
description: Learn how to connect Astro to external data sources
---

## Overview

Before you can complete production-level work in Astro, you need to connect your cloud to external data sources. There are multiple options for connecting an Airflow deployment to data sources:

- Public Endpoints
- VPC Peering
- Transit Gateways
- Private Endpoints (AWS PrivateLink)

## Public Endpoints

The fastest and easiest way to connect Astro to an external data source is by using the data source's publicly accessible API endpoints.

These endpoints can be configured via [Environment Variables](environment-variables.md) or via an [Airflow Connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

### IP Whitelisting

Some data services, such as Snowflake and Databricks, provide an additional layer of security by requiring you to whitelist a specific IP address before that address can access the service.

Each Cluster has a unique external IP address that will persist for the life of the Cluster. To retrieve the IP for your Cluster, open a ticket with Astronomer Support. If you have more than one Cluster, you will need to whitelist each Cluster on your data service provider.

## VPC Peering

Each Cluster runs in a dedicated VPC. To set up private connectivity between the Astro VPC and your VPC, you can set up a VPC peering connection. Peered VPCs provide additional security by ensuring private connectivity, reduced network transit costs, and simplified network layouts.

To create a VPC peering connection between a Cluster's VPC and a target VPC:

1. Open a support ticket with Astronomer and provide the following information for the target VPC:

- AWS account
- AWS Region
- Cluster ID
- CIDR of the target VPC

In response, Astronomer will initiate a peering request. This peering request must be accepted by the owner of the target VPC.

Once peering is set up, continue to work with Astronomer support and the owner of the target VPC to update the routing tables of both VPCs to direct traffic to each other.

### DNS Considerations with VPC Peering

The Astronomer VPC has both DNS Hostnames and DNS Resolutions options enabled, as well as the "Requester DNS Resolution" option on the Peering Connection.  

If you have enabled the DNS Hostnames and DNS Resolution options on the target VPC, enabling the "Accepter DNS Resolution" option on the Peering Connection will allow the Airflow instances to resolve the public DNS names (e.g ec2-1-2-3-4.compute-1.amazonaws.com) of the data source to their private IP addresses. Instructions on how to set this up are provided in [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html). 

If you are using Private Hosted Zones to resolve DNS names, then you will need to associate your Route53 Private Hosted Zone with the Astronomer VPC using instructions provided [here](https://aws.amazon.com/premiumsupport/knowledge-center/route53-private-hosted-zone/). You can get the id of the Astronomer VPC by contacting Astronomer support.
