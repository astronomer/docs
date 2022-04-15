---
sidebar_label: 'Install Astro on AWS'
title: 'Install Astro on AWS'
id: install-aws
description: Get started on Astro by installing your first Astro Cluster on AWS.
---

## Overview

We're excited to get you started with Astro on AWS. Below, you'll find instructions for how to complete the Astro install process, including prerequisites and the steps required for our team to provision resources in your network.

At a high-level, we'll ask that you come prepared with a new AWS account. From there, you can expect to:
- Create an account on Astro.
- Share AWS account information with our team.
- Create a cross-account IAM role that Astro can assume within your new AWS account.

Astronomer will then create a Cluster within your AWS account that hosts the resources and Apache Airflow components necessary to deploy DAGs and execute tasks. If you'd like to support more than 1 Astro Cluster, [reach out to us](https://support.astronomer.io).

For a complete list of the AWS resources that our team will provision in your AWS account, see [Resource Usage](resource-reference-aws.md).

## Prerequisites

Before completing this setup, make sure that you have:

- A dedicated AWS account with minimum EC2 service quotas.
- A user with the following permissions:
    - `cloudformation:*`
    - `GetRole`
    - `GetRolePolicy`
    - `CreateRole`
    - `DeleteRolePolicy`
    - `PutRolePolicy`
    - `ListRoles`
    - `UpdateAssumeRolePolicy`
- A subscription to the [Astro Status Page](https://cloud-status.astronomer.io/). This will ensure that you're alerted in the case of an incident or scheduled maintenance.

Astro requires a clean AWS account with a minimum set of EC2 service quotas. For security reasons, the install process is not currently supported on an AWS account that has other tooling running in it. For instructions on creating a new AWS account, follow [AWS documentation](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).

The required [EC2 service quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html) are:

| QuotaCode  | QuotaName                                                        | Minimum Required Value  |
| -----------| ---------------------------------------------------------------- | ----------------------- |
| L-1216C47A | Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances | 40                      |
| L-43DA4232 | Running On-Demand High Memory instances                          | 40                      |
| L-34B43A08 | All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests  | 40                      |

These are required to mitigate near term capacity risks and ensure a smooth onboarding experience on Astro. If you need to modify or increase a specific quota, see Amazon’s documentation on [requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html).

Once your AWS account is created, proceed to Step 1.

:::tip

If you have one or more existing AWS accounts, you can use [AWS Organizations](https://aws.amazon.com/organizations/) to manage billing, users, and more in a central place. For more information on how to add your Astro AWS account to your AWS Organization, read [Amazon's documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_invites.html).
:::

### VPC Peering Prerequisites (Optional)

If any AWS resources are on a private network, you can choose between two options:

- Allow traffic via the public internet and use allow-lists for communication.
- Create a VPC Peering connection between Astronomer's VPC and the VPCs for your broader network.

If you want to continue with the second option, you'll additionally need:

- A CIDR block (RFC 1918 IP Space) no smaller than a `/19` range. You must ensure it does not overlap with the AWS VPC(s) that you will be peering with later. The default CIDR range is `172.20.0.0/19`.
- VPC Name / ID for peering with Astronomer (accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/)).
- The IP addresses of your DNS servers.

## Step 1: Access Astro

To begin the Astro install process, first create an account at https://cloud.astronomer.io/.

When you first authenticate to Astro, you can sign in with a Google account, a GitHub account, or an email and password.

<div class="text--center">
  <img src="/img/docs/login.png" alt="Astro login screen" />
</div>

If you're the first person from your team to authenticate, the Astronomer team will add you as a Workspace Admin to a new Workspace named after your Organization. From there, you'll be able to add other team members to that Workspace without Astronomer's assistance.

:::tip

After completing your initial installation, we recommend [setting up an identity provider (IdP)](configure-idp.md) so that users can log in to Astro through your IdP.

:::

## Step 2: Share Information with Astronomer

For the AWS account you created as a prerequisite, provide Astronomer with:

- Your AWS Account ID.
- Your preferred Astro Cluster name.
- The AWS region that you want to host your Cluster in.
- Your preferred node instance type.
- Your preferred maximum node count.

If not specified, Astronomer will create a Cluster with two `m5.xlarge` nodes in `us-east-1` and a maximum node count of 20 by default. For information on all supported regions and configurations, see [AWS Resource Reference](resource-reference-aws.md).

From here, our team will provision an Astro Cluster according to the specifications you provided.

## Step 3: Create a Cross-Account IAM Role for Astro

Once your Astro Cluster has been created, an Astronomer team member will provide you with an [External ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html) that will allow Astronomer to connect to your AWS account. Save the External ID as a secret or in an otherwise secure format for use in the AWS CLI.

Then, click the link below to create an [cross-account admin IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html#getting-started_create-admin-group-console) for Astro in your new AWS account:

- [Create cross-account IAM Role](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://astro-cross-account-role-template.s3.us-east-2.amazonaws.com/customer-account.yaml&stackName=AstroCrossAccountIAMRole&param_AstroAccountId=406882777402)

Using this CloudFormation link is the recommended way to create an IAM role for Astro. Alternatively, you can create a cross-account IAM Role by running the following AWS CLI commands:

```bash
$ aws iam create-role --role-name astronomer-remote-management --assume-role-policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
            \"Effect\": \"Allow\",
            \"Principal\": {
                \"AWS\": \"arn:aws:iam::406882777402:root\"
            },
            \"Action\": \"sts:AssumeRole\",
            \"Condition\": {
                \"StringEquals\": {
                \"sts:ExternalId\": \"$EXTERNAL_ID\"
                }
            }
        }
    ]
}"

$ aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AdministratorAccess --role-name astronomer-remote-management
```

The output of the last command is a YAML file containing information about the role:

```yaml
{
  "Role":
    {
      "Path": "/",
      "RoleName": "astronomer-remote-management",
      "RoleId": "AROAZZTAM6QSYIFGCB37R",
      "Arn": "arn:aws:iam::673438299173:role/astronomer-remote-management",
      "CreateDate": "2021-06-30T17:47:39+00:00",
      "AssumeRolePolicyDocument":
        {
          "Version": "2012-10-17",
          "Statement":
            [
              {
                "Effect": "Allow",
                "Principal": { "AWS": "arn:aws:iam::406882777402:root" },
                "Action": "sts:AssumeRole",
                "Condition": { "StringEquals": { "sts:ExternalId": "" } },
              },
            ],
        },
    },
}
```

To provision additional Clusters, complete the setup in [Create a Cluster](create-cluster.md) after completing your initial installation.

:::caution

Some AWS regions that Astronomer supports are disabled by default on AWS, including:

- `af-south-1` - Africa (Cape Town)
- `ap-east-1` - Asia Pacific (Hong Kong)
- `me-south-1` - Middle East (Bahrain)

If you're setting up your first Cluster in any of these regions, you need to complete the additional setup as described in [Create a Cluster](create-cluster.md#additional-setup-for-aws-regions-that-are-disabled-by-default).

:::

## Step 4: Let Astronomer Complete the Install

Let our team know once you've created the cross-account IAM role for Astro. From there, we will finish creating an Astronomer Cluster in your AWS account that supports Apache Airflow environments.

This process can take some time. Wait for confirmation that the installation was successful before proceeding to the next step.

> **Note**: If you need to VPC peer with Astronomer, additionally provide the following information to your Astronomer representative:
>
>- Subnet CIDRs (RFC 1918 IP Space).
>- VPC Name/ID and region for peering with Astronomer. This is accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/).
>- The IPs of your DNS servers.
>
> You then need to accept a VPC peering request from Astronomer after Astro is installed. To accept the request, follow [Creating and accepting a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html) in AWS documentation.
>
> Once VPC peered with Astronomer, configure and validate the following to ensure successful network communications between Astro and your resources:
>
>- Egress Routes on Astronomer Route Table
>- [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html#nacl-tasks) and/or [Security Group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#working-with-security-groups) rules of your resources

## Step 5: Create a Deployment

Once our team confirms that your Astro Cluster has been created, you are ready to create a Deployment and start deploying DAGs. Log in to [the Cloud UI](https://cloud.astronomer.io) again and [create a new Deployment](configure-deployment.md). If the installation was successful, your new Astro Cluster will be listed as an option under the **Cluster** menu:

<div class="text--center">
  <img src="/img/docs/create-new-deployment-select-cluster.png" alt="Cloud UI New Deployment screen" />
</div>

## Next Steps

Now that you have an Astro Cluster up and running, take a look at the docs below for information on how to start working in Astro:

- [Set Up an Identity Provider](configure-idp.md)
- [Install CLI](install-cli.md)
- [Configure Deployments](configure-deployment.md)
- [Deploy Code](deploy-code.md)
- [Add Users](add-user.md)
