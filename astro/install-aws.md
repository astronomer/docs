---
sidebar_label: 'Install Astro on AWS'
title: 'Install Astro on AWS'
id: install-aws
description: Get started on Astro by installing your first Astro cluster on AWS.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This is where you'll find instructions for completing the Astro installation process, including prerequisites and the steps required for our team to provision resources in your network.

At a high-level, we'll ask that you come prepared with a new AWS account. From there, you can expect to:
- Create an account on Astro.
- Share AWS account information with our team.
- Create a cross-account IAM role that Astro can assume within your new AWS account.

Astronomer will then create a cluster within your AWS account that hosts the resources and Apache Airflow components necessary to deploy DAGs and execute tasks. If you'd like to support more than 1 Astro cluster, [reach out to us](https://support.astronomer.io).

For a complete list of the AWS resources that our team will provision in your AWS account, see [Resource usage](resource-reference-aws.md).

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

| QuotaCode  | QuotaName                                                        | Minimum Value  |
| -----------| ---------------------------------------------------------------- | ---------------|
| L-1216C47A | Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances | 40             |
| L-34B43A08 | All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests  | 40             |

These are required to mitigate near term capacity risks and ensure a smooth onboarding experience on Astro. If you need to modify or increase a specific quota, see Amazon’s documentation on [requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html).

Once your AWS account is created, proceed to Step 1.

:::tip

If you have one or more existing AWS accounts, you can use [AWS Organizations](https://aws.amazon.com/organizations/) to manage billing, users, and more in a central place. For more information on how to add your Astro AWS account to your AWS Organization, read [Amazon's documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_invites.html).
:::

### VPC peering prerequisites (Optional)

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

## Step 2: Provide setup information to Astronomer

For the AWS account you created as a prerequisite, provide Astronomer with:

- Your AWS Account ID.
- Your preferred Astro cluster name.
- The AWS region that you want to host your cluster in.
- Your preferred node instance type.
- Your preferred maximum node count.

If not specified, Astronomer will create a cluster with two `m5.xlarge` nodes in `us-east-1` and a maximum node count of 20 by default. For information on all supported regions and configurations, see [AWS resource reference](resource-reference-aws.md).

From here, our team will provision an Astro cluster according to the specifications you provided.

## Step 3: Create a cross-account IAM role for Astro

After your Astro Cluster is created, Astronomer provides you with an external ID. Save the external ID as a secret or in another secure format. You need to add the external ID to AWS to allow Astronomer to access your AWS resources. For more information, see [How to use an external ID when granting access to your AWS resources to a third party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).

Astronomer recommends using the AWS Management Console to add the external ID to your AWS instance.

<Tabs
    defaultValue="managementconsole"
    values={[
        {label: 'AWS Management Console', value: 'managementconsole'},
        {label: 'AWS Command Line', value: 'commandline'},
    ]}>
<TabItem value="managementconsole">

1. Create an AWS administrator IAM user and user group. See the AWS topic [Creating an administrator IAM user and user group (console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html#getting-started_create-admin-group-console).

2. Open the [Astronomer cross-account role CloudFormation template](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://astro-cross-account-role-template.s3.us-east-2.amazonaws.com/customer-account.yaml&stackName=AstroCrossAccountIAMRole&param_AstroAccountId=406882777402).

3. Enter the external ID provided by Astronomer in the **ExternalId** field.

4. Select the **I acknowledge that AWS CloudFormation might create IAM resources with custom names** checkbox.

5. Click **Create Stack**.

</TabItem>

<TabItem value="commandline">

1. Open the AWS CLI and run the following command to create a cross-account IAM Role:

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
    ```

2. Run the following command to attach a managed policy to the Astronomer remote management role.

    ```bash
    $ aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AdministratorAccess --role-name astronomer-remote-management
    ```
    This command returns a YAML file containing role information:

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

</TabItem>
</Tabs>

To provision additional Clusters after completing your initial installation, see [Create a Cluster](create-cluster.md).

:::caution

Some AWS regions that Astronomer supports are disabled by default on AWS, including:
- `ap-east-1` - Asia Pacific (Hong Kong)
- `me-south-1` - Middle East (Bahrain)

If you're setting up your first cluster in any of these regions, you need to complete the additional setup described in [Create a cluster](create-cluster.md#additional-setup-for-aws-regions-that-are-disabled-by-default).

:::

## Step 4: Let Astronomer complete the install

Contact Astronomer after you've created the cross-account IAM role for Astro. From there, Astronomer will finish creating the cluster in your AWS account.

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

When Astronomer confirms that your Astro cluster has been created, you are ready to create a Deployment and start deploying DAGs. Log in to [the Cloud UI](https://cloud.astronomer.io) again and [create a new Deployment](create-deployment.md). If the installation is successful, your new Astro cluster is listed as an option below the **Cluster** menu:

<div class="text--center">
  <img src="/img/docs/create-new-deployment-select-cluster.png" alt="Cloud UI New Deployment screen" />
</div>

## Next steps

Now that you have an Astro cluster up and running, take a look at the docs below for information on how to start working in Astro:

- [Set up an identity provider](configure-idp.md)
- [Install CLI](cli/get-started.md)
- [Configure Deployments](configure-deployment-resources.md)
- [Deploy code](deploy-code.md)
- [Add users](add-user.md)
