---
sidebar_label: 'AWS'
title: 'Install Astro Hybrid on AWS'
id: install-aws-hybrid
sidebar_custom_props: { icon: 'img/aws.png' }
toc_min_heading_level: 2
toc_max_heading_level: 2
description: 'Use this document to complete the installation of Astro Hybrid in an Amazon Web Services (AWS) account.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::caution

This document applies only to [Astro Hybrid](hybrid-overview.md). To see whether you're an Astro Hybrid user, click the Astronomer logo in the upper left corner of the Cloud UI and go to **Settings** > **General**. Your Astro product type is listed under **Product Type**.

To get started on Astro Hosted, see [Start a trial](trial.md).

:::

The Astro Hybrid data plane on Amazon Web Services (AWS) runs on Elastic Kubernetes Service (EKS). 

To install Astro, Astronomer will create an Astro cluster in a dedicated AWS account that's hosted and owned by your organization. This ensures that all data remains within your network and allows your organization to manage infrastructure billing.

For a list of the AWS resources and configurations that Astronomer supports, see [AWS resource reference](resource-reference-aws-hybrid.md). For more information about the shared responsibility model, see [Shared responsibility model](shared-responsibility-model.md).

To complete the installation, you'll:

- Create an Astronomer account.
- Create a new AWS account with the required AWS resources.
- Create the IAM policies used by Astro. This includes a cross-account IAM role that Astro can assume and [permissions boundaries for IAM entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html).

Astronomer support will create infrastructure within your AWS account to host the resources and Apache Airflow components necessary to deploy DAGs and execute tasks. If you need more than one Astro cluster, contact [Astronomer support](https://cloud.astronomer.io/support).

## Prerequisites

- A [new AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) with the minimum EC2 service quotas. For security reasons, AWS accounts with existing infrastructure aren't supported.

    The following table lists the required [EC2 service quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html).

    | QuotaCode  | QuotaName                                                        | Minimum Value  |
    | -----------| ---------------------------------------------------------------- | ---------------|
    | L-1216C47A | Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances | 40             |
    | L-34B43A08 | All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests  | 40             |

  These quotas are required to mitigate near term capacity risks and simplify the Astro onboarding experience. Refer to [AWS documentation](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) to modify or increase a specific quota.

- A CIDR block with a range of `/20`. If you don't have a preferred CIDR block, Astro will provision a VPC using a default of `172.20.0.0/20`. Astro uses this VPC for 2 public subnets and 2 private subnets. See [AWS resource reference](resource-reference-aws-hybrid.md).

- Permissions to create a stack using [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-cli-creating-stack.html).

- The following domains added to your organization's allowlist for any user and CI/CD environments:
    - `https://cloud.astronomer.io/`
    - `https://api.astronomer.io/`
    - `https://images.astronomer.cloud/`
    - `https://auth.astronomer.io/`
    - `https://updates.astronomer.io/`
    - `https://install.astronomer.io/`
    - `https://astro-<your-org>.datakin.com/`
    - `https://<your-org>.astronomer.run/`

- A subscription to the [Astro Status Page](https://status.astronomer.io/). This ensures that you'll be notified when there are incidents or when maintenance is scheduled.

:::tip

If you have one or more existing AWS accounts, you can use [AWS Organizations](https://aws.amazon.com/organizations/) to manage billing, users, and more in a central place. For more information on how to add your Astro AWS account to your AWS Organization, see [Inviting an AWS account to join your organization](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_invites.html).

:::

#### VPC peering prerequisites (Optional)

The following options are available to connect Astro to AWS resources on a private network:

- Allow traffic through the public internet and use allowlists for communication.
- Create a VPC Peering connection between the dedicated Astro data plane VPC and your existing AWS account VPCs.

If you want to continue with the second option, you'll additionally need:

- A CIDR block (RFC 1918 IP Space) no smaller than a `/20` range. You must ensure it does not overlap with the AWS VPC(s) that you will be peering with later. The default CIDR range is `172.20.0.0/20`.
- VPC Name / ID for peering with Astronomer (accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/)).
- The IP addresses of your DNS servers.

## Access Astro

1. Go to https://cloud.astronomer.io/ and create an account, or enter your email address, and then click **Continue**.

2. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**.
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in your Organization to authenticate, you'll be granted Organization Owner permissions. You can create a Workspace and add other team members to the Workspace without the assistance of Astronomer support. See [Manage Workspace users](manage-workspace-users.md). 
    
    To integrate an identity provider (IdP) with Astro, see [Set up an identity provider](configure-idp.md).

## Retrieve an external ID from the Cloud UI

You must be an Organization Owner to view the external ID. If you are not an Organization Owner, the **AWS External ID** field will not appear in the Cloud UI.

1. In the Cloud UI, click the **Settings** tab.

2. Click **Show** in the **AWS External ID** field and then click **Copy**. This external ID is a unique identifier that Astro uses to connect to your AWS account. 

3. Save the external ID as a secret or in another secure format. See [How to use an external ID when granting access to your AWS resources to a third party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).

## Create a cross-account role

Use the external ID to create a cross-account IAM role for Astro.

1. Log in to your [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation).

2. Open the [Astronomer cross-account role CloudFormation template](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://astro-cross-account-role-template.s3.us-east-2.amazonaws.com/astronomer-remote-management-stack.yaml&stackName=AstroCrossAccountRole).

3. Enter the external ID that you copied in Step 2 in the **ExternalId** field.

4. Select the **I acknowledge that AWS CloudFormation might create IAM resources with custom names** checkbox.

5. Click **Create Stack**.

### Cross-account role modifications

When new features or functionality are added to Astro, Astronomer might need to modify cross-account role permissions. When setting permissions, Astronomer adheres to the least-privilege permissions standard and adds only the permissions necessary for new features or functionality.

Astronomer support notifies your Organization when any changes are made to the policies that expand cross-account role access. Notifications will include an explanation of the changes being made and why the change was necessary. 

Astronomer can reduce the access available to the policies without notification.

### Monitor the policies for changes (optional)

You can use CloudTrail to monitor changes to Astro policies. Access to CloudTrail has been limited to prevent the accidental modification or deletion of CloudTrail logs by Astronomer support. The following table lists the events that you should monitor. 

| Event Names                              | Resource                                                         |
| ---------------------------------------- | ---------------------------------------------------------------- |
| `AttachRolePolicy , DetachRolePolicy`    | `roleName = astronomer-remote-management`                        |
| `SetPolicyVersion` | `policyArn = "arn:aws:iam::*:policy/AstronomerCrossAccountRole"` |

To monitor changes to the cross-account role policy and permissions boundaries, create an Amazon CloudWatch alarm. See [Creating CloudWatch alarms for CloudTrail events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html).  When you create the metric filter in the CloudWatch console, on the **Define pattern** page, in **Create filter pattern**, enter the following for **Filter pattern**:

```text
{ ($.eventName = AttachRolePolicy || $.eventName = DetachRolePolicy || $.eventName = SetPolicyVersion) && ($.requestParameters.policyArn = "*OperationalBoundary*" || $.requestParameters.policyArn = "*AstronomerCrossAccountRole"  || $.requestParameters.roleName = astronomer-remote-management) }
```

## Provide setup information to Astronomer

After creating the AWS account, provide Astronomer with the following information:

- Your AWS Account ID.
- Your preferred Astro cluster name.
- The AWS region that you want to host your cluster in.
- Your preferred node instance type.
- Your preferred maximum node count.
- An instance type for the Airflow metadata database.

If you do not specify configuration preferences, Astronomer creates a cluster with `m5.xlarge` nodes and a maximum node count of 20 in `us-east-1` and a default `db.m6g.large` Amazon RDS instance type. For information on all supported regions, configurations, and defaults, see [AWS cluster configurations](resource-reference-aws-hybrid.md).

To provision additional clusters after completing your initial installation, see [Create a cluster](manage-hybrid-clusters.md#create-a-cluster).

:::caution

Some AWS regions that Astronomer supports are disabled by default on AWS, including:
- `ap-east-1` - Asia Pacific (Hong Kong)
- `me-south-1` - Middle East (Bahrain)

If you're setting up your first cluster in any of these regions, you need to complete the additional setup described in [Create a cluster](manage-hybrid-clusters.md#additional-setup-for-aws-regions-that-are-disabled-by-default).

:::

### Provide VPC peering information (optional)

If you need to VPC peer with Astronomer, provide the following information to your Astronomer representative:

- Subnet CIDRs (RFC 1918 IP Space).
- VPC Name/ID and region for peering with Astronomer. This is accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/).
- The IPs of your DNS servers.

## Astronomer creates the cluster

After you've created the cross-account IAM role for Astro, contact your Astronomer representative. Astronomer creates the cluster in your AWS account.

This process can take some time. Wait for confirmation from Astronomer that the cluster has been created before creating a Deployment.

If you submitted a VPC peering request, you'll need to accept the request from Astronomer after Astro is installed. To accept the request, see [Create a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html).

When VPC peering with Astronomer is complete, configure and validate the following items to ensure successful network communications between Astro and your resources:

- Egress Routes on Astronomer Route Table
- [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html#nacl-tasks) and/or [Security Group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#working-with-security-groups) rules of your resources

## Create a Deployment and confirm the install

When you receive confirmation that your Astro cluster has been created, Astronomer recommends that you create a Deployment and deploy DAGs. See [Create a Deployment](create-deployment.md). 

To confirm a successful installation, in the Cloud UI select a Workspace and on the **Deployments** page click **Deployment**. The Astro cluster created by Astronomer support appears as an option in the **Cluster** list.

## Next steps

- [Set up an identity provider](configure-idp.md)
- [Install CLI](cli/overview.md)
- [Configure Deployments](configure-deployment-resources.md)
- [Deploy code](deploy-code.md)
- [Manage Organization users](manage-organization-users.md)
