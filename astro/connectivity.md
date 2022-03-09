---
sidebar_label: "Connect to External Services"
title: "Connect Astro to External Data Services"
id: connectivity
description: Learn how to connect Astro to different types of external data sources.
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

A Cluster VPC has both DNS Hostnames and DNS Resolutions options enabled, as well as the "Requester DNS Resolution" option on the Peering Connection.  

If you have enabled the DNS Hostnames and DNS Resolution options on the target VPC, enabling the "Accepter DNS Resolution" option on the Peering Connection allows the Data Plane to resolve the public DNS names (e.g `ec2-1-2-3-4.compute-1.amazonaws.com`) of a data source to its private IP addresses. Instructions on how to set this up are provided in [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If you are using Private Hosted Zones to resolve DNS names, then you will need to associate your Route53 Private Hosted Zone with the Astronomer VPC using instructions provided in [AWS Documentation](https://aws.amazon.com/premiumsupport/knowledge-center/route53-private-hosted-zone/). You can retrieve the ID of the Astronomer VPC by contacting Astronomer support.

## Transit Gateway

AWS Transit Gateway connects VPCs and on-premises networks through a central hub. This leads to a simplified network architecture and is easier to manage than 1:1 peering relationships.  

To get started, use AWS Resource Access Manager to share the Transit Gateway with the Data Plane AWS account as shown in [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-share.html).

After you complete this step, you can open a support case with Astronomer to request that Astronomer accepts this resource share.  

You will then need to work with the owner of the Transit Gateway to create Transit Gateway Attachments, Route Tables and Associations, as well as Astronomer Support to update the route tables of the Astronomer VPC to route to the Transit Gateway.  AWS Documentation on how to accomplish this is is [here](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-getting-started.html).

### DNS Considerations with Transit Gateway

AWS Transit Gateway does not provide any native support for DNS Resolution. You can use your data sources via their private IP addresses, but if DNS Integration is required, then AWS recommends using the Route53 Resolver.  Your customer success team can help you integrate Route53 Resolver with your Astronomer VPC.

## Private Endpoints (AWS PrivateLink)

AWS PrivateLink provides private connectivity between VPCs and services hosted on AWS or on your premises.  

Astronomer supports the following kinds of PrivateLinks:

- Builtin AWS Endpoints that connect to most AWS managed services
- Custom Endpoint Services that were created to connect an EC2 or RDS service running in your VPC
- Endpoint Services created by a third party service provider (e.g. Snowflake, Databricks)

### Builtin AWS  Endpoints

To add a built-in interface endpoint, please open a ticket with Astronomer support. Astronomer supports the following AWS PrivateLink endpoints:

- S3
- API Gateway
- Athena
- EC2 API
- EFS
- EMR
- EMR on EKS
- Kinesis
- Lambda
- RDS API
- RDS Data Service (NOTE: this only supports Aurora Serverless)
- Redshift

Please note the following when using the builtin endpoints:

- Some services require additional steps to enable and configure the endpoint service. For example, Redshift endpoints need additional configuration steps as described in the [AWS blog](https://aws.amazon.com/blogs/big-data/enable-private-access-to-amazon-redshift-from-your-client-applications-in-another-vpc/).
- The EC2 API is accessible over PrivateLink, but private connectivity to any service running in EC2 instances will require setting up a Custom Interface Endpoint Service.
- The RDS Data API only supports Aurora Serverless. Private data transfers from any other RDS instance can only be done once a Custom Interface Endpoint Service has been set up.

### Custom Interface Endpoint Services

Any EC2 or RDS service that can be placed behind a Network Load Balancer can be set up as an Endpoint Service.  Astronomer supports Interface Endpoint Services but not Gateway Load Balancer Endpoint Services.  

1. Create an Endpoint Service by following the [AWS documentation](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html)
2. Add the Astronomer account to the list of allowed service consumers, as defined in the [AWS documentation](https://docs.aws.amazon.com/vpc/latest/privatelink/add-endpoint-service-permissions.html).  The AWS account number for the Astronomer account is listed in the  [from the Astronomer Cloud Console](https://cloud.astronomer.io/clusters).
3. Reach out to Astronomer support to add this endpoint to the Astronomer VPC.

## Third Party Interface Endpoints

Astronomer will support the following Third Party Interface Endpoints:

- Snowflake
- Databricks (Front End Endpoints only)

Note that both Snowflake and Databricks offer this only in their higher tier offerings; you must be on Business Critical Support with Snowflake or using the E2 platform with Databricks.

The process for adding these is:

- Work with the third party Service Provider to  create the endpoints and authorize the Astronomer account as a consumer.  The AWS account number for the Astronomer account is listed in the  [from the Astronomer Cloud Console](https://cloud.astronomer.io/clusters).
- Contact Astronomer Support to add these endpoints into your VPC and create the associated DNS entries to access these endpoints
