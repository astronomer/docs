---
sidebar_label: 'AWS'
title: 'Connect Astro to AWS data sources'
id: connect-aws
description: Connect Astro to AWS resources.
sidebar_custom_props: { icon: 'img/aws.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Use this document to learn how you can connect an Astro cluster and its Deployments to your external AWS resources.

## Connection options

Publicly accessible endpoints allow you to quickly connect your Astro clusters or Deployments to AWS through an Airflow connection. If your cloud restricts IP addresses, you can add the external IPs of your Deployment or cluster to an AWS resource's allowlist. 

If you have stricter security requirements, you can [create a private connection](#create-a-private-connection-between-astro-and-aws) to AWS in a few different ways.

After you crate a connection from your Deployment to AWS, you might also have to individually authorize Deployments to access specific resources. See [Authorize your Deployment using workload identity](authorize-deployments-to-your-cloud.md#aws).

### Access a public AWS endpoint

To facilitate communication between your Astro cluster or Deployment and your cloud, you can allowlist the external IPs for your cluster or Deployment in your cloud. If you have no other security restrictions, this means that any Deployment or cluster with an allowlisted external IP address can access your AWS resources through a valid Airflow connection.

#### Allowlist external IP addresses for a cluster

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**.
2. Click **Clusters**, then select a cluster.
3. In the Details page, copy the IP addresses listed under **External IPs**.
4. Add the IP addresses to the allowlist of any external services that you want your cluster to access.

After you allowlist a cluster's IP address, all Deployments in that cluster are allowed to access your AWS resources.

#### Allowlist external IP addresses for a Deployment

To grant access to your external resources on per-Deployment basis, or if you are using a standard cluster, allowlist the IPs only for specific Deployments. For each Deployment that you want to allowlist:

1. In the Cloud UI, select a Deployment, then click Details.
2. Copy the IP addresses under External IPs.
3. Add the IP addresses to the allowlist of any external services that you want your Deployment to access.

When you use publicly accessible endpoints to connect to AWS, traffic moves directly between your Astro cluster and the AWS API endpoint. Data in this traffic never reaches the Astronomer-managed control plane.

### Create a private connection between Astro and AWS

Choose one of the following setups based on the security requirements of your company and your existing infrastructure.

<Tabs
    defaultValue="VPC peering"
    groupId="connection-options"
    values={[
        {label: 'VPC peering', value: 'VPC peering'},
        {label: 'Transit Gateways', value: 'Transit Gateways'},
        {label: 'AWS PrivateLink', value: 'AWS PrivateLink'},
    ]}>

<TabItem value="VPC peering">

:::info 

This connection option is only available for dedicated Astro Hosted clusters and Astro Hybrid.

:::

To set up a private connection between an Astro VPC and an AWS VPC, you can create a VPC peering connection. VPC peering ensures private and secure connectivity, reduces network transit costs, and simplifies network layouts.

To create a VPC peering connection between an Astro VPC and an AWS VPC, you must create a temporary assumable role. The Astro AWS account will assume this role to initiate a VPC peering connection.

1. Open the AWS console of the AWS account with the external VPC and copy the following:

    - AWS account ID 
    - AWS region
    - VPC ID of the external VPC
    - CIDR block of the external VPC
    
2. Create a temporary role using the [role creation stack template](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://cre-addon-infrastructure-us-east-1.s3.amazonaws.com/astro-peering-role.yaml). In the **Quick create stack** template that opens, complete the following fields:

    - **Stack name**: Enter a meaningful name for your stack.
    - **Peer Owner IDs**: Enter your cluster's AWS account ID. To retrieve your cluster's AWS account ID on Astro Hosted, contact [Astronomer support](https://cloud.astronomer.io/support). To retrieve your cluster's AWS account ID on Astro Hybrid, click the name of your Workspace in the upper left corner of the Cloud UI, click **Organization Settings**, then click **Clusters**. Open your cluster and copy its **Account ID**.

3. After the stack is created, go to the **Outputs** tab and copy the value from the **PeerRole ARN** field.

4. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. Click **Clusters**, select your cluster, and copy the **ID** of the cluster.

5. Contact [Astronomer support](https://cloud.astronomer.io/support) and provide the following details:

    - AWS region of the external VPC from Step 1
    - VPC ID of the external VPC from Step 1
    - AWS account ID of the external VPC from Step 1
    - CIDR block of the external VPC from Step 1
    - **Stack ID** from Step 3
    - Astro cluster **ID** from Step 4
    
    Astronomer support will initiate a peering request and create the routing table entries in the Astro VPC.

6. Wait for Astronomer support to send you the Astro VPC CIDR and VPC peering ID. Then, the owner of the external VPC needs to [add a route](https://docs.aws.amazon.com/vpc/latest/userguide/WorkWithRouteTables.html#AddRemoveRoutes) in the external VPC, using the Astro VPC CIDR as the **Destination** and the VPC peering ID as the **Target**.

7. (Optional) Delete the stack that you created. This will delete the temporary assumable role.


#### DNS considerations for VPC peering

To resolve DNS hostnames from your external VPC, every Astro VPC has **DNS Hostnames**, **DNS Resolutions**, and **Requester DNS Resolution** enabled. See AWS [Peering Connection settings](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If your external VPC resolves DNS hostnames using **DNS Hostnames** and **DNS Resolution**, you must also enable the **Accepter DNS Resolution** setting on AWS. This allows Astro clusters to resolve the public DNS hostnames of the external VPC to its private IP addresses. To configure this option, see [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If your external VPC resolves DNS hostnames using [private hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html), then you must associate your Route53 private hosted zone with the Astro VPC using instructions provided in [AWS Documentation](https://aws.amazon.com/premiumsupport/knowledge-center/route53-private-hosted-zone/).

To retrieve the ID of any Astro VPC, contact [Astronomer support](https://cloud.astronomer.io/support). If you have more than one Astro cluster, request the VPC ID of each cluster.

</TabItem>

<TabItem value="Transit Gateways">

:::info 

This connection option is only available for dedicated Astro Hosted clusters and Astro Hybrid.

:::

Use AWS Transit Gateway to connect one or more Astro clusters to other VPCs, AWS accounts, and on-premises networks supported by your organization.

AWS Transit Gateway is an alternative to VPC Peering on AWS. Instead of having to establish a direct connection between two VPCs, you can attach over 5,000 networks to a central transit gateway that has a single VPN connection to your corporate network.

While it can be more costly, AWS Transit Gateway requires less configuration and is often recommended for organizations connecting a larger number of VPCs. For more information, see [AWS Transit Gateway](https://aws.amazon.com/transit-gateway/).

AWS Transit Gateway doesn't provide built-in support for DNS resolution. If you need DNS integration, Astronomer recommends that you use the Route 53 Resolver service. For assistance integrating the Route 53 Resolver service with your Astronomer VPC, contact [Astronomer support](https://cloud.astronomer.io/support).

:::info

If your transit gateway is in a different region than your Astro cluster, contact [Astronomer support](https://cloud.astronomer.io/support). Astronomer support can create a new transit gateway in your AWS account for Astro and set up [a cross-region peering attachment](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-peering.html) with your existing transit gateway.

If Astronomer creates a new transit gateway in your AWS account for Astro, keep in mind that your organization will incur additional AWS charges for the new transit gateway as well as the inter-region transfer costs.

:::

#### Prerequisites

- An Astro cluster
- An existing transit gateway in the same region as your Astro cluster
- Permission to share resources using AWS Resource Access Manager (RAM)

#### Setup

1. In the Cloud UI, click the name of your Workspace in the upper left corner of the Cloud UI, then click **Organization Settings** > **Clusters*. Open your cluster from the table that appears and copy its **ID**.
2. In your AWS console, copy the ID of your existing transit gateway (TGW). 
3. [Create a resource share in AWS RAM](https://docs.aws.amazon.com/ram/latest/userguide/working-with-sharing-create.html) and [share the TGW with your cluster's Astro AWS account](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-transit-gateways.html#tgw-sharing). 

    To retrieve your cluster's AWS account ID on Astro Hosted, contact [Astronomer support](https://cloud.astronomer.io/support). To retrieve your cluster's AWS account ID in the Astro Hybrid, click the name of your Workspace in the upper left corner of the Cloud UI, click **Organization Settings**, then click **Clusters**. Open your cluster and copy its **Account ID**.
    
4. Contact [Astronomer support](https://cloud.astronomer.io/support) and provide the following information:

    - Your cluster **ID** from Step 1.
    - Your TGW ID from Step 2.
    - The CIDR block for the external VPC or on-premises network that you want to connect your Astro cluster with.

    Astronomer support approves the resource sharing request, attaches the Astro private subnets to your transit gateway, and creates routes in the Astro route tables to your transit gateway for each of the CIDR provided. Astronomer support notifies you about the process completion and provides you with the Astro CIDRs.

5. After you receive the confirmation from Astronomer support, use the Astro CIDRs to [create back routes](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-peering.html#tgw-peering-add-route) from your transit gateway to the Astro VPC.

6. Contact [Astronomer support](https://cloud.astronomer.io/support) to confirm that you have created the static route. Astronomer support then tests the connection and confirm.

7. (Optional) Repeat the steps for each Astro cluster that you want to connect to your transit gateway.

</TabItem>

<TabItem value="AWS PrivateLink">

:::info 

This connection option is only available for dedicated Astro Hosted clusters and Astro Hybrid.

:::

Use AWS PrivateLink to create private connections from Astro to your AWS services without exposing your data to the public internet. If your AWS services are located in a different region than Astro, contact [Astronomer support](https://cloud.astronomer.io/support).

All Astro clusters are pre-configured with the following AWS PrivateLink endpoint services:

- Amazon S3 - Gateway Endpoint
- Amazon Elastic Compute Cloud (Amazon EC2) Autoscaling - Interface Endpoint
- Amazon Elastic Container Registry (ECR) - Interface Endpoints for ECR API and Docker Registry API
- Elastic Load Balancing (ELB)  - Interface Endpoint
- AWS Security Token Service (AWS STS) - Interface Endpoint

To request additional endpoints, or assistance connecting to other AWS services, contact [Astronomer support](https://cloud.astronomer.io/support).

To access a service in a different region using PrivateLink endpoints, you must use an inter-Region VPC peering connection. You create an intermediate PrivateLink endpoint in the same region as the targeted service, then connect to that endpoint through an inter-Region VPC peering connection.
    
By default, Astronomer support activates the **Enable DNS Name** option on supported AWS PrivateLink endpoint services.  With this option enabled, you can make requests to the default public DNS service name instead of the public DNS name that is automatically generated by the VPC endpoint service. For example, `*.notebook.us-east-1.sagemaker.aws` instead of `vpce-xxx.notebook.us-east-1.vpce.sagemaker.aws`. For more information about AWS DNS hostnames, see [DNS hostnames](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#:~:text=recursive%20DNS%20queries.-,DNS%20hostnames,-When%20you%20launch).

You'll incur additional AWS infrastructure costs for every AWS PrivateLink endpoint service that you use.  See [AWS PrivateLink pricing](https://aws.amazon.com/privatelink/pricing/).

</TabItem>

</Tabs>

## Hostname resolution options

Securely connect Astro to resources running in other VPCs or on-premises through a resolving service. 

Using Route 53 requires sharing a resolver rule with your Astro account. If this is a security concern, Astronomer recommends using Domain Name System (DNS) forwarding.

<Tabs
    defaultValue="Shared resolver rule"
    groupId="hostname-resolution-options"
    values={[
        {label: 'Shared resolver rule', value: 'Shared resolver rule'},
        {label: 'Domain Name System forwarding', value: 'Domain Name System forwarding'},
    ]}>
<TabItem value="Shared resolver rule">

Use Route 53 Resolver rules to allow Astro to resolve DNS queries for resources running in other VPCs or on-premises.

### Prerequisites

- An Amazon Route 53 Resolver rule. See [Managing forwarding rules](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-rules-managing.html).
- Permission to share resources using the AWS Resource Access Manager (RAM)

### Share the Amazon Route 53 Resolver rule

To allow Astro to access a private hosted zone, you need to share your Amazon Route 53 Resolver rule with your Astro AWS account.

1. In the Route 53 Dashboard, click **Rules** below **Resolver** in the navigation menu.

2. Select a Resolver rule and then click **Details**.

3. Click **Share** and enter `Astro` in the **Name** field.

4. In the **Resources - optional** section, select **Resolver Rules**  in the **Select resource type** list and then select one or more rules.

5. On the **Associate permissions** page, accept the default settings and then click **Next**.

6. On the **Grant access to principals** page, select **Allow sharing only within your organization**, and then enter your Astro AWS account ID for your organization in the **Enter an AWS account ID** field. 

    To get the Astro AWS account ID, click the name of your Workspace in the upper left corner of the Cloud UI, then click **Organization Settings**. From the **General** page, copy the **AWS External ID**.

7. Click **Create resource share**.

#### Contact Astronomer support for rule verification

To verify that the Amazon Route 53 Resolver rule was shared correctly, submit a request to [Astronomer support](https://cloud.astronomer.io/support). With your request, include the Amazon Route 53 Resolver rule ID. To locate the Resolver rule ID, open the Route 53 Dashboard, and in the left menu click **Rules** below **Resolver**. Copy the value in the Resolver **ID** column.

#### Create a connection to confirm connectivity (optional)

When Astronomer support confirms that the Amazon Route 53 Resolver rule was successfully associated with the Astro VPC, you can create a connection to the resource that is resolved by the shared rule. See [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

</TabItem>

<TabItem value="Domain Name System forwarding">

Use Domain Name System (DNS) forwarding to allow Astro to resolve DNS queries for resources running in other VPCs or on-premises. Unlike Route 53, you don't need to share sensitive configuration data with your Astro account. To learn more about DNS forwarding, see [Forwarding outbound DNS queries to your network](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-forwarding-outbound-queries.html).

To use this solution, make sure Astro can connect to the DNS server using a VPC peering or transit gateway connection and then submit a request to [Astronomer support](https://cloud.astronomer.io/support). With your request, include the following information:

- The domain name for forwarding requests
- The IP address of the DNS server where requests are forwarded

#### Create an Airflow connection to confirm connectivity (optional)

When Astronomer support confirms that DNS forwarding was successfully implemented, you can confirm that it works by creating an Airflow connection to a resource running in a VPC or on-premises. See [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

</TabItem>

</Tabs>


## See Also

- [Manage Airflow connections and variables](manage-connections-variables.md)
- [Authorize your Deployment using workload identity](authorize-deployments-to-your-cloud.md#aws)
