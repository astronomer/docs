---
sidebar_label: "Connect to external services"
title: "Connect Astro to external data services"
id: connect-external-services
description: Learn how to connect your Astro data plane to different types of external data services.
---

Before you can run pipelines on Astro with real data, you first need to make your data services accessible to your Data Plane and the Deployments running within it. This guide explains how to securely connect Astro to external data services using the following methods:

- Public Endpoints
- Virtual Private Cloud (VPC) Peering
- AWS Transit Gateway
- Workload Identity (_GCP only_)
- AWS IAM roles

If you need to connect to a type of data service that requires a connectivity method that is not documented here, reach out to [Astronomer support](https://support.astronomer.io).

## Public endpoints

The fastest and easiest way to connect Astro to an external data service is by using the data service's publicly accessible endpoints.

These endpoints can be configured by:

- Setting [environment variables](environment-variables.md) on Astro with your endpoint information.
- Creating an [Airflow connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) with your endpoint information.

Public connection traffic moves directly between your data plane and the external data service's API endpoint. This means that the data in this traffic never reaches the control plane, which is managed by Astronomer.

### IP allowlist

Some data services, including Snowflake and Databricks, provide an additional layer of security by requiring you to allowlist a specific IP address before you can access the service.

On Astro, each cluster has a pair of unique external IP address that will persist throughout the lifetime of the cluster. These IP addresses are assigned for network address translation, which means that they are responsible for all outbound traffic from your Astro cluster to the internet. To retrieve the IP addresses for a given cluster, open a ticket with [Astronomer support](https://support.astronomer.io) and request it. If you have more than one cluster, you will need to allowlist each cluster individually on your data service provider.

## VPC peering

Each cluster on Astro runs in a dedicated VPC. To set up private connectivity between an Astro VPC and another VPC, you can set up a VPC peering connection. Peered VPCs provide additional security by ensuring private connectivity, reduced network transit costs, and simplified network layouts.

To create a VPC peering connection between an Astro cluster's VPC and a target VPC, reach out to [Astronomer support](https://support.astronomer.io) and provide the following information:

- Astro cluster ID and Name
- Amazon Web Services (AWS) Account ID or Google Cloud Platform (GCP) Project ID of the target VPC
- Region of the target VPC (_AWS only_)
- VPC ID of the target VPC
- CIDR of the target VPC

From there, Astronomer will initiate a peering request. To connect successfully, this peering request must be accepted by the owner of the target VPC.

Once peering is set up, the owner of the target VPC can expect to continue to work with our team to update the routing tables of both VPCs to direct traffic to each other.

### DNS considerations with VPC peering (_AWS only_)

To resolve DNS hostnames from your target VPC, your cluster VPC has **DNS Hostnames**, **DNS Resolutions**, and **Requester DNS Resolution** enabled. See AWS [Peering Connection settings](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).  

If your target VPC resolves DNS hostnames using **DNS Hostnames** and **DNS Resolution**, you must also enable the **Accepter DNS Resolution** setting. This allows the data plane to resolve the public DNS hostnames of the target VPC to its private IP addresses. To configure this option, see [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html).

If your target VPC resolves DNS hostnames using [private hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html), then you must associate your Route53 private hosted zone with the Astronomer VPC using instructions provided in [AWS Documentation](https://aws.amazon.com/premiumsupport/knowledge-center/route53-private-hosted-zone/). You can retrieve the ID of the Astronomer VPC by contacting [Astronomer support](https://support.astronomer.io).

## AWS Transit Gateway

Use AWS Transit Gateways to connect your Astro clusters to your VPCs and on-premises networks.

### Prerequisites

- An Astro cluster
- A transit gateway in the same region as your Astro cluster
- Permission to share resources using AWS Resource Access Manager (RAM)

:::info

If your transit gateway is in a different region than your Astro cluster, contact [Astronomer support](https://support.astronomer.io). Astronomer can create a new transit gateway and set up cross-region peering with your existing transit gateway. With this configuration your organization can incur AWS charges for a new transit gateway hosted in the Astro account, as well as inter-region transfer costs.
:::

### Setup

1. In the Cloud UI, click the **Clusters** tab and copy the **Account ID** for the cluster.
2. Create a resource share in AWS RAM. See [Creating a resource share in AWS RAM](https://docs.aws.amazon.com/ram/latest/userguide/working-with-sharing-create.html)  The account ID that you need to share with is the value that you copied in Step 1.
3. Contact [Astronomer support](https://support.astronomer.io) and provide the destination CIDR block of the VPC or on-premises network that should be routed through the transit gateway. From here, Astronomer approves the resource sharing request and creates a transit gateway peering attachment request to your on-premises network.
4. Accept the Transit Gateway peering attachment request from your on-premises network. See [Accept or reject a peering attachment request](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-peering.html#tgw-peering-accept-reject).
5. Create a static route from your CIDR block to the transit gateway. See [Add a route to the transit gateway route table](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-peering.html#tgw-peering-add-route).
6. Contact [Astronomer support](https://support.astronomer.io) to confirm that you have created the static route. From here, Astronomer updates the routing table of the Astro cluster's VPC to send traffic from your CIDR block through the transit gateway.

## Workload Identity (_GCP only_)

[Workload Identity](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity) is recommended by Google as the best way for data pipelines running on GCP to access Google Cloud services in a secure and manageable way. All Astro clusters on GCP have Workload Identity enabled by default. Each Astro Deployment is associated with a Kubernetes service account that's created by Astronomer and is bound to an identity from your Google Cloud project's fixed workload identity pool.

To grant a Deployment on Astro access to GCP services such as BigQuery, you must:

- Go to the Google Cloud project in which your external data service is hosted
- Add the Kubernetes service account for your Astro Deployment to the principal of that Google Cloud project
- Bind the service account to a role that has access to your external data service

Kubernetes service accounts for Astro Deployments are formatted as follows:

```text
astro-<deployment-namespace>@<gcp-project-name>.iam.gserviceaccount.com
```

To find the namespace of your Deployment, go to your Deployment page in the Cloud UI and copy paste the value in the **Namespace** field.

For a Google Cloud project called `astronomer-prod` and a Deployment namespace called `nuclear-science-2730`, for example, the service account for the Deployment would be:

```text
astro-nuclear-science-2730@astronomer-prod.iam.gserviceaccount.com
```

:::info

GCP has a 30 character limit for service account names. For Deployment namespaces which are longer than 24 characters, use only the first 24 characters when determining your service account name. For example, if your GCP project was called `astronomer-prod` and your Deployment namespace was `nuclear-scintillation-2730`, your service account would be:

```text
astro-nuclear-scintillation-27@astronomer-pmm.iam.gserviceaccount.com
```

:::

For more information about configuring service accounts on GCP, see [GCP documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to).

## Use AWS IAM roles to authorize access to Astro

To grant an Astro cluster access to a service that is running in an AWS account not managed by Astronomer, use AWS IAM roles. IAM roles on AWS are often used to manage the level of access a specific user, object, or group of users has to a resource. This includes an Amazon S3 bucket, Redshift instance, or secrets backend.

1. In the Cloud UI, click **Clusters** and then copy the value displayed in the **Cluster ID** column for the Astro cluster that needs access to AWS service resources.

2. Create an IAM role in the AWS account that contains your AWS service. See [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).

3. In the AWS Management Console, go to the Identity and Access Management (IAM) dashboard.

4. Click **Roles** and in the **Role name** column select the role you created in step 2.

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
                    "arn:aws:iam::<dataplane-AWS-account-ID>:role/AirflowS3Logs-<cluster-ID>",
                ]
            },
            "Action": "sts:AssumeRole"
        },
    ]
}
```
7. Click **Update policy**.

8. Create an Airflow connection to AWS for each Deployment that requires the resources you connected. See [Managing connections to Apache Airflow](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html).
