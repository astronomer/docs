---
sidebar_label: 'AWS'
title: 'Connect Astro to AWS data sources'
id: connect-aws
description: Connect your Astro data plane to AWS.
sidebar_custom_props: { icon: 'img/aws.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Use the information provided here to learn how you can securely connect your Astro data plane to your existing AWS instance. A connection to AWS allows Astro to access data stored on your AWS instance and is a necessary step to running pipelines in a production environment.

## Connection options

The connection option that you choose is determined by the requirements of your organization and your existing infrastructure. You can choose a straightforward implementation, or a more complex implementation that provides enhanced data security. Astronomer recommends that you review all of the available connection options before selecting one for your organization.

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

When you use publicly accessible endpoints to connect Astro and AWS, traffic moves directly between your Astro data plane and the AWS API endpoint. Data in this traffic never reaches the control plane, which is managed by Astronomer.

</TabItem>

<TabItem value="VPC peering">

Every Astro cluster runs in a dedicated Virtual Private Network (VPC). To set up a private connection between an Astro VPC and an AWS VPC, you can create a VPC peering connection. VPC peering ensures private and secure connectivity, reduces network transit costs, and simplifies network layouts.

To create a VPC peering connection between an Astro VPC and an AWS VPC, contact [Astronomer support](https://cloud.astronomer.io/support) and provide the following information:

- Astro cluster ID and name
- AWS Account ID of the target VPC
- Region of the target VPC
- VPC ID of the target VPC
- Classless Inter-Domain Routing (CIDR) block of the target VPC

After receiving your request, Astronomer support initiates a peering request and creates the routing table entries in the Astro VPC. To allow multidirectional traffic between Airflow and your organization's data sources, the owner of the target VPC needs to accept the peering request and create the routing table entries in the target VPC.

#### DNS considerations for VPC peering

To resolve DNS hostnames from your target VPC, every Astro VPC has **DNS Hostnames**, **DNS Resolutions**, and **Requester DNS Resolution** enabled. See AWS [Peering Connection settings](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If your target VPC resolves DNS hostnames using **DNS Hostnames** and **DNS Resolution**, you must also enable the **Accepter DNS Resolution** setting on AWS. This allows the data plane to resolve the public DNS hostnames of the target VPC to its private IP addresses. To configure this option, see [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If your target VPC resolves DNS hostnames using [private hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html), then you must associate your Route53 private hosted zone with the Astro VPC using instructions provided in [AWS Documentation](https://aws.amazon.com/premiumsupport/knowledge-center/route53-private-hosted-zone/).

To retrieve the ID of any Astro VPC, contact [Astronomer support](https://cloud.astronomer.io/support). If you have more than one Astro cluster, request the VPC ID of each cluster.

</TabItem>

<TabItem value="Transit Gateways">

Use AWS Transit Gateway to connect one or more Astro clusters to other VPCs, AWS accounts, and on-premises networks supported by your organization.

AWS Transit Gateway is an alternative to VPC Peering on AWS. Instead of having to establish a direct connection between two VPCs, you can attach over 5,000 networks to a central transit gateway that has a single VPN connection to your corporate network.

While it can be more costly, AWS Transit Gateway requires less configuration and is often recommended for organizations connecting a larger number of VPCs. For more information, see [AWS Transit Gateway](https://aws.amazon.com/transit-gateway/).

AWS Transit Gateway doesn't provide built-in support for DNS resolution. If you need DNS integration, Astronomer recommends that you use the Route 53 Resolver service. For assistance integrating the Route 53 Resolver service with your Astronomer VPC, contact [Astronomer support](https://cloud.astronomer.io/support).

:::info

If your transit gateway is in a different region than your Astro cluster, contact [Astronomer support](https://cloud.astronomer.io/support). Astronomer support can create a new transit gateway in your AWS account for Astro and set up a cross-region peering connection with your existing transit gateway.

If Astronomer creates a new transit gateway in your AWS account for Astro, keep in mind that your organization will incur additional AWS charges for the new transit gateway as well as the inter-region transfer costs.

:::

#### Prerequisites

- An Astro cluster
- An existing transit gateway in the same region as your Astro cluster
- Permission to share resources using AWS Resource Access Manager (RAM)

#### Setup

1. In the Cloud UI, click the **Clusters** tab and copy the **Account ID** for your Astro cluster. This is an AWS account ID.
2. Create a resource share in AWS RAM with the account ID from step 1. See [Creating a resource share in AWS RAM](https://docs.aws.amazon.com/ram/latest/userguide/working-with-sharing-create.html).
3. Contact [Astronomer support](https://cloud.astronomer.io/support) and provide the CIDR block of the target VPC or on-premises network that you want to connect your Astro cluster with. From here, Astronomer approves the resource sharing request and creates a transit gateway peering attachment request to your network.
4. Accept the transit gateway peering attachment request from your network. See [Accept or reject a peering attachment request](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-peering.html#tgw-peering-accept-reject).
5. Create a static route from your CIDR block to the transit gateway and a static route from the transit gateway to the Astro VPC. See [Add a route to the transit gateway route table](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-peering.html#tgw-peering-add-route).
6. Contact [Astronomer support](https://cloud.astronomer.io/support) to confirm that you have created the static route. Astronomer support will update the Astro VPC routing table to send traffic from your CIDR block through the transit gateway.
7. Optional. Repeat the steps for each Astro cluster that you want to connect to your transit gateway.

</TabItem>

<TabItem value="AWS PrivateLink">

Use AWS PrivateLink to create private connections from Astro to your AWS services without exposing your data to the public internet.

Astro clusters are pre-configured with the following AWS PrivateLink endpoint services:

- Amazon S3 - Gateway Endpoint
- Amazon Elastic Compute Cloud (Amazon EC2) Autoscaling - Interface Endpoint
- Amazon Elastic Container Registry (ECR) - Interface Endpoints for ECR API and Docker Registry API
- Elastic Load Balancing (ELB)  - Interface Endpoint
- AWS Security Token Service (AWS STS) - Interface Endpoint

To request additional endpoints, or assistance connecting to other AWS services, contact [Astronomer support](https://cloud.astronomer.io/support).

By default, Astronomer support activates the **Enable DNS Name** option on supported AWS PrivateLink endpoint services.  With this option enabled, you can make requests to the default public DNS service name instead of the public DNS name that is automatically generated by the VPC endpoint service. For example, `*.notebook.us-east-1.sagemaker.aws` instead of `vpce-xxx.notebook.us-east-1.vpce.sagemaker.aws`. For more information about AWS DNS hostnames, see [DNS hostnames](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#:~:text=recursive%20DNS%20queries.-,DNS%20hostnames,-When%20you%20launch).

You'll incur additional AWS infrastructure costs for every AWS PrivateLink endpoint service that you use.  See [AWS PrivateLink pricing](https://aws.amazon.com/privatelink/pricing/).

</TabItem>

</Tabs>

## Authorization options

Authorization is the process of verifying a user or service's permissions before allowing them access to organizational applications and resources. Astro clusters must be authorized to access external resources from your cloud. Which authorization option that you choose is determined by the requirements of your organization and your existing infrastructure. Astronomer recommends that you review all of the available authorization options before selecting one for your organization.

<Tabs
    defaultValue="AWS IAM roles"
    groupId="authentication-options"
    values={[
        {label: 'AWS IAM roles', value: 'AWS IAM roles'},
        {label: 'AWS access keys', value: 'AWS access keys'},
    ]}>
<TabItem value="AWS IAM roles">

To grant an Astro cluster access to a service that is running in an AWS account not managed by Astronomer, use AWS IAM roles. IAM roles on AWS are often used to manage the level of access a specific user, object, or group of users has to a resource. This includes an Amazon S3 bucket, Redshift instance, or secrets backend.

1. In the Cloud UI, click **Clusters** and then copy the value displayed in the **Cluster ID** column for the Astro cluster that needs access to AWS service resources.
2. Create an IAM role in the AWS account that contains your AWS service. See [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).
3. In the AWS Management Console, go to the Identity and Access Management (IAM) dashboard.
4. Click **Roles** and in the **Role name** column, select the role you created in step 2.
5. Click the **Trust relationships** tab.
6. Click **Edit trust policy** and update the `arn` value:

    ```text {8}
        {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "arn:aws:iam::<dataplane-AWS-account-ID>:role/AirflowS3Logs-<cluster-ID>"
                    ]
                },
                "Action": "sts:AssumeRole"
            },
        ]
    }
    ```

    Your Astro cluster's data plane account includes the `AirflowLogsS3-<clusterid>` role. When you configure an Airflow connection for a Deployment, specify this role in an [AWS Airflow Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html) to allow your Deployment access your service.

7. Click **Update policy**.
8. In the Airflow UI or as an environment variable on Astro, create an Airflow connection to AWS for each Deployment that requires the resources you connected. See [Managing connections to Apache Airflow](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html).
9. Optional. Repeat these steps for each Astro cluster that requires access to external data services on AWS.

</TabItem>

<TabItem value="AWS access keys">

Astro supports all Airflow AWS connection types. For more information about the available AWS connection types, see [Amazon Web Services Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html). When you create your Airflow AWS connection, you'll need your AWS access key ID and secret access key. 

Astronomer recommends using an external secrets backend to store your AWS access key ID and secret access key. See [Configure an external secrets backend on Astro](secrets-backend.md).

</TabItem>

</Tabs>