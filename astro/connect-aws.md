---
sidebar_label: 'AWS'
title: 'Connect Astro to AWS data sources'
id: connect-aws
description: Connect Astro to AWS resources.
toc_min_heading_level: 2
toc_max_heading_level: 2
sidebar_custom_props: { icon: 'img/aws.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

You have a number of options for connecting Deployments on an AWS cluster to external data sources. Use the following topics to learn about each available connection option and how to configure them.

## Connection options

The connection option that you choose is determined by the requirements of your company and your existing infrastructure. You can choose a straightforward implementation, or a more complex implementation that provides enhanced data security. 

<Tabs
    defaultValue="Public endpoints"
    groupId="connection-options"
    values={[
        {label: 'Public endpoints', value: 'Public endpoints'},
        {label: 'VPC peering', value: 'VPC peering'},
        {label: 'Transit Gateways', value: 'Transit Gateways'},
        {label: 'AWS PrivateLink', value: 'AWS PrivateLink'},
    ]}>
<TabItem value="Public endpoints">

Publicly accessible endpoints allow you to quickly connect Astro to AWS. To configure these endpoints, you can use one of the following methods:

- Set environment variables on Astro with your endpoint information. See [Set environment variables on Astro](environment-variables.md).
- Create an Airflow connection with your endpoint information. See [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

When you use publicly accessible endpoints to connect Astro and AWS, traffic moves directly between your Astro cluster and the AWS API endpoint. Data in this traffic never reaches the control plane, which is managed by Astronomer.

</TabItem>

<TabItem value="VPC peering">

:::info 

This connection option is only available for dedicated Astro Hosted clusters and Astro Hybrid.

:::

To set up a private connection between an Astro VPC and an AWS VPC, you can create a VPC peering connection. VPC peering ensures private and secure connectivity, reduces network transit costs, and simplifies network layouts.

To create a VPC peering connection between an Astro VPC and an AWS VPC, contact [Astronomer support](https://cloud.astronomer.io/support) and provide the following information:

- Astro cluster ID and name
- AWS Account ID of the target VPC
- Region of the target VPC
- VPC ID of the target VPC
- Classless Inter-Domain Routing (CIDR) block of the target VPC

After receiving your request, Astronomer support initiates a peering request and creates the routing table entries in the Astro VPC. To allow multidirectional traffic between Airflow and your organization's data sources, the owner of the target VPC needs to accept the peering request and create the routing table entries in the target VPC.

#### DNS considerations for VPC peering

To resolve DNS hostnames from your target VPC, every Astro VPC has **DNS Hostnames**, **DNS Resolutions**, and **Requester DNS Resolution** enabled. See AWS [Peering Connection settings](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If your target VPC resolves DNS hostnames using **DNS Hostnames** and **DNS Resolution**, you must also enable the **Accepter DNS Resolution** setting on AWS. This allows Astro clusters to resolve the public DNS hostnames of the target VPC to its private IP addresses. To configure this option, see [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If your target VPC resolves DNS hostnames using [private hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html), then you must associate your Route53 private hosted zone with the Astro VPC using instructions provided in [AWS Documentation](https://aws.amazon.com/premiumsupport/knowledge-center/route53-private-hosted-zone/).

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
    - The CIDR block for the target VPC or on-premises network that you want to connect your Astro cluster with.

    Astronomer support approves the resource sharing request, attaches the Astro private subnets to your transit gateway, and creates routes in the Astro route tables to your transit gateway for each of the CIDR provided. Astronomer support notifies you about the process completion and provides you with the Astro CIDRs.

5. After you receive the confirmation from Astronomer support, use the Astro CIDRs to [create back routes](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-peering.html#tgw-peering-add-route) from your transit gateway to the Astro VPC.

6. Contact [Astronomer support](https://cloud.astronomer.io/support) to confirm that you have created the static route. Astronomer support then tests the connection and confirm.

7. (Optional) Repeat the steps for each Astro cluster that you want to connect to your transit gateway.

</TabItem>

<TabItem value="AWS PrivateLink">


Use AWS PrivateLink to create private connections from Astro to your AWS services without exposing your data to the public internet. If your AWS services are located in a different region than Astro, contact [Astronomer support](https://cloud.astronomer.io/support).

Astro clusters are pre-configured with the following AWS PrivateLink endpoint services:

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

## Authorization options

Authorization is the process of verifying a user or service's permissions before allowing them access to organizational applications and resources. Astro clusters must be authorized to access external resources from your cloud. Which authorization option that you choose is determined by the requirements of your organization and your existing infrastructure. Astronomer recommends that you review all of the available authorization options before selecting one for your organization.

<Tabs
    defaultValue="AWS IAM roles"
    groupId="authorization-options"
    values={[
        {label: 'AWS IAM roles', value: 'AWS IAM roles'},
        {label: 'AWS access keys', value: 'AWS access keys'},
    ]}>
<TabItem value="AWS IAM roles">

To grant an Astro Deployment access to a service that is running in an AWS account not managed by Astronomer, use AWS IAM roles. IAM roles on AWS are often used to manage the level of access a specific user, object, or group of users has to a resource. This includes an Amazon S3 bucket, Redshift instance, or secrets backend.

1. In the Cloud UI, select your Deployment and then click **Details**. Copy the `arn` given under **Workload Identity**.
2. Create an IAM role in the AWS account that contains your AWS service. See [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).
3. In the AWS Management Console, go to the Identity and Access Management (IAM) dashboard.
4. Click **Roles** and in the **Role name** column, select the role you created in step 2.
5. Click the **Trust relationships** tab.
6. Click **Edit trust policy** and paste the `arn` you copied from Step 1 in the trust policy.

    ```text {8}
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "<workload-identity-role>"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    ```
    When you configure an [AWS Airflow Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html) for a Deployment, specify the ARN of the role that you would like to assume (the role created in step 2) as the value for `aws_arn`.

7. Click **Update policy**.
8. In the Airflow UI or as an environment variable on Astro, create an Airflow connection to AWS for each Deployment that requires the resources you connected. See [Managing connections to Apache Airflow](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html).
9. Optional. Repeat these steps for each Astro Deployment that requires access to external data services on AWS.

</TabItem>

<TabItem value="AWS access keys">

Astro supports all Airflow AWS connection types. For more information about the available AWS connection types, see [Amazon Web Services Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html). When you create your Airflow AWS connection, you'll need your AWS access key ID and secret access key. 

Astronomer recommends using an external secrets backend to store your AWS access key ID and secret access key. See [Configure an external secrets backend on Astro](secrets-backend.md).

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

6. On the **Grant access to principals** page, select **Allow sharing only within your organization**, and then enter your Astro AWS account ID for your organization in the **Enter an AWS account ID** field. To get the Astro AWS account ID, go to the Cloud UI, click **Settings**, and then copy the value in the **ID** column for the Astro AWS account you want to share the Resolver rule with.

7. Click **Create resource share**.

### Contact Astronomer support for rule verification

To verify that the Amazon Route 53 Resolver rule was shared correctly, submit a request to [Astronomer support](https://cloud.astronomer.io/support). With your request, include the Amazon Route 53 Resolver rule ID. To locate the Resolver rule ID, open the Route 53 Dashboard, and in the left menu click **Rules** below **Resolver**. Copy the value in the Resolver **ID** column.

### Create a connection to confirm connectivity (optional)

When Astronomer support confirms that the Amazon Route 53 Resolver rule was successfully associated with the Astro VPC, you can create a connection to the resource that is resolved by the shared rule. See [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

</TabItem>

<TabItem value="Domain Name System forwarding">

Use Domain Name System (DNS) forwarding to allow Astro to resolve DNS queries for resources running in other VPCs or on-premises. Unlike Route 53, you don't need to share sensitive configuration data with your Astro account. To learn more about DNS forwarding, see [Forwarding outbound DNS queries to your network](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-forwarding-outbound-queries.html).

To use this solution, make sure Astro can connect to the DNS server using a VPC peering or transit gateway connection and then submit a request to [Astronomer support](https://cloud.astronomer.io/support). With your request, include the following information:

- The domain name for forwarding requests
- The IP address of the DNS server where requests are forwarded

### Create an Airflow connection to confirm connectivity (optional)

When Astronomer support confirms that DNS forwarding was successfully implemented, you can confirm that it works by creating an Airflow connection to a resource running in a VPC or on-premises. See [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

</TabItem>

</Tabs>
