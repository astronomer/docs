---
sidebar_label: 'AWS'
title: 'Install Astro on AWS'
id: install-aws
sidebar_custom_props: { icon: 'img/aws.png' }
toc_min_heading_level: 2
toc_max_heading_level: 2
---

<head>
  <meta name="description" content="If you have an existing Amazon Web Services (AWS) instance, use these instructions to complete an Astro installation. This is where you’ll find the prerequisites and the process you’ll need to follow to allow Astronomer support to provision your network resources." />
  <meta name="og:description" content="If you have an existing Amazon Web Services (AWS) instance, use these instructions to complete an Astro installation. This is where you’ll find the prerequisites and the process you’ll need to follow to allow Astronomer support to provision your network resources." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

The Astro data plane on Amazon Web Services (AWS) runs on Elastic Kubernetes Service (EKS). You have two options to install Astro on AWS:

- Bring Your Own Cloud -  Create an Astro cluster in a dedicated AWS account that's hosted and owned by your organization. This ensures that all data remains within your network and allows your organization to manage infrastructure billing.
- Hosted - Create an Astro cluster in a dedicated AWS account that's hosted and owned by Astronomer. This removes the complexity of adding another AWS account to your network.

With the two options, the user experience is identical and Astronomer is responsible for managing Astro. The differences between the two options are security and networking.

For a list of the AWS resources and configurations that Astronomer supports, see [AWS resource reference](resource-reference-aws.md). For more information about the shared responsibility model, see [Shared responsibility model](shared-responsibility-model.md).

## Set up

<Tabs
    defaultValue="byoc"
    groupId= "byoc"
    values={[
        {label: 'Bring Your Own Cloud', value: 'byoc'},
        {label: 'Hosted', value: 'astronomer hosted data plane'},
    ]}>
<TabItem value="byoc">

To install Astro in a dedicated AWS account owned by your organization, you'll complete the following tasks:

- Create an account on Astro.
- Share AWS account information with Astronomer support.
- Create a cross-account IAM role that Astro can assume within your new AWS account.

Astronomer support will create a cluster within your AWS account that hosts the resources and Apache Airflow components necessary to deploy DAGs and execute tasks. If you'd like to support more than 1 Astro cluster, contact [Astronomer support](https://cloud.astronomer.io/support).

### Prerequisites

- An AWS IAM user with the following permissions:

    - `cloudformation:*`
    - `GetRole`
    - `GetRolePolicy`
    - `CreateRole`
    - `DeleteRolePolicy`
    - `PutRolePolicy`
    - `ListRoles`
    - `UpdateAssumeRolePolicy`

   See [Creating an administrator IAM user and user group (console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html#getting-started_create-admin-group-console).

- A dedicated AWS account with minimum EC2 service quotas.
- A subscription to the [Astro Status Page](https://status.astronomer.io/). This will ensure that you're alerted in the case of an incident or scheduled maintenance.
- The following domains added to your organization's allowlist for any user and CI/CD environments:
  
    - `https://cloud.astronomer.io/`
    - `https://astro-<your-org>.datakin.com/`
    - `https://<your-org>.astronomer.run/`
    - `https://api.astronomer.io/`
    - `https://images.astronomer.cloud/`
    - `https://auth.astronomer.io/`
    - `https://updates.astronomer.io/`
    - `https://install.astronomer.io/`

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

#### VPC peering prerequisites (Optional)

If any AWS resources are on a private network, you can choose between two options:

- Allow traffic through the public internet and use allow-lists for communication.
- Create a VPC Peering connection between the Astronomer VPC and the VPCs for your broader network.

If you want to continue with the second option, you'll additionally need:

- A CIDR block (RFC 1918 IP Space) no smaller than a `/19` range. You must ensure it does not overlap with the AWS VPC(s) that you will be peering with later. The default CIDR range is `172.20.0.0/19`.
- VPC Name / ID for peering with Astronomer (accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/)).
- The IP addresses of your DNS servers.

### Access Astro

1. Go to https://cloud.astronomer.io/ and create an account, or enter your email address, and then click **Continue**.

2. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**.
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in your Organization to authenticate, you'll be granted Organization owner permissions. You can create a Workspace and add other team members to the Workspace without the assistance of Astronomer support. See [Create a Workspace](manage-workspaces.md#create-a-workspace) and [Add a user](add-user.md). To integrate an identity provider (IdP) with Astro, see [Set up an identity provider](configure-idp.md).

### Retrieve an external ID from the Cloud UI

You must be an Organization Owner to view the external ID. If you are not an Organization Owner, the field will not appear in the Cloud UI.

1. In the Cloud UI, click the **Settings** tab.

2. Click **Show** in the **AWS External ID** field and then click **Copy**. This external ID is a unique identifier that Astro uses to connect to your AWS account. 

3. Save the external ID as a secret or in another secure format. See [How to use an external ID when granting access to your AWS resources to a third party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).

### Create a cross-account IAM role for Astro

Use the external ID to create a cross-account IAM role for Astro. Astronomer recommends using the AWS Management Console to create the role.

<Tabs
    defaultValue="managementconsole"
    groupId= "step-3-create-a-cross-account-iam-role-for-astro"
    values={[
        {label: 'AWS Management Console', value: 'managementconsole'},
        {label: 'AWS Command Line', value: 'commandline'},
    ]}>
<TabItem value="managementconsole">

1. Open the [Astronomer cross-account role CloudFormation template](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://astro-cross-account-role-template.s3.us-east-2.amazonaws.com/customer-account.yaml&stackName=AstroCrossAccountIAMRole&param_AstroAccountId=406882777402).

2. Enter the external ID that you copied in Step 2 in the **ExternalId** field.

3. Select the **I acknowledge that AWS CloudFormation might create IAM resources with custom names** checkbox.

4. Click **Create Stack**.

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

### Provide setup information to Astronomer

After creating the AWS account, provide Astronomer support with the following information:

- Your AWS Account ID.
- Your preferred Astro cluster name.
- The AWS region that you want to host your cluster in.
- Your preferred node instance type.
- Your preferred maximum node count.

If you do not specify configuration preferences, Astronomer creates a cluster with `m5.xlarge` nodes and a maximum node count of 20 in `us-east-1`. For information on all supported regions, configurations, and defaults, see [AWS cluster configurations](resource-reference-aws.md).

To provision additional Clusters after completing your initial installation, see [Create a cluster](create-cluster.md).

:::caution

Some AWS regions that Astronomer supports are disabled by default on AWS, including:
- `ap-east-1` - Asia Pacific (Hong Kong)
- `me-south-1` - Middle East (Bahrain)

If you're setting up your first cluster in any of these regions, you need to complete the additional setup described in [Create a cluster](create-cluster.md#additional-setup-for-aws-regions-that-are-disabled-by-default).

:::

#### Provide VPC peering information (Optional)

If you need to VPC peer with Astronomer, provide the following additional information to Astronomer support:

- Subnet CIDRs (RFC 1918 IP Space).
- VPC Name/ID and region for peering with Astronomer. This is accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/).
- The IPs of your DNS servers.

### Astronomer support creates the cluster

After you've created the cross-account IAM role for Astro, contact [Astronomer support](https://cloud.astronomer.io/support). Astronomer support will finish creating the cluster in your AWS account.

This process can take some time. Wait for confirmation from Astronomer support that the cluster has been created before creating a Deployment.

If you submitted a VPC peering request, you'll need to accept the request from Astronomer after Astro is installed. To accept the request, see [Create a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html).

When VPC peering with Astronomer is complete, configure and validate the following items to ensure successful network communications between Astro and your resources:

- Egress Routes on Astronomer Route Table
- [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html#nacl-tasks) and/or [Security Group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#working-with-security-groups) rules of your resources

</TabItem>

<TabItem value="astronomer hosted data plane">

When providing hosted services, Astronomer adheres to industry best practices and standards, including the Health Insurance Portability and Accountability Act (HIPAA), Service Organization Control 2 (SOC2), and  General Data Protection Regulation (GDPR). 

### Prerequisites

The setup process assumes that you've already provided Astronomer support with the following information: 

- Your preferred cluster installation region. See the supported region lists for [AWS](resource-reference-aws.md#aws-region).
- Optional. Your preferred worker instance type for your first cluster. See [AWS cluster configurations](resource-reference-aws.md#worker-node-types).
- Optional. Your VPC peering requirements for [AWS](install-aws.md#vpc-peering-prerequisites-optional-2).
- The email address of your first Astro user.

If you haven't provided this information to Astronomer support, contact your Astronomer representative.

#### VPC peering prerequisites (Optional)

If any AWS resources are on a private network, you can choose between two options:

- Allow traffic through the public internet and use allow-lists for communication.
- Create a VPC Peering connection between the Astronomer VPC and the VPCs for your broader network.

If you want to continue with the second option, you'll additionally need to provide Astronomer support with:

- A CIDR block (RFC 1918 IP Space) no smaller than a `/19` range. You must ensure it does not overlap with the AWS VPC(s) that you will be peering with later. The default CIDR range is `172.20.0.0/19`.
- VPC Name / ID for peering with Astronomer (accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/)).
- The IP addresses of your DNS servers.

### Astronomer support creates the cluster

Astronomer support creates your first Astro cluster in a dedicated AWS account after you've provided your setup information.

Wait for confirmation that the installation is successful before you access Astro and create a Deployment.

### Access Astro

1. Optional. If you haven't created an Astronomer account, go to https://cloud.astronomer.io/ and create an account.

2. Go to https://cloud.astronomer.io, enter your email address, and then click **Continue**.

3. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**.
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in an Organization to authenticate, you're added as a Workspace Admin to a new Workspace named after your Organization. You can add other team members to the Workspace without the assistance of Astronomer support. See [Add a user](add-user.md). To integrate an identity provider (IdP) with Astro, see [Set up an identity provider](configure-idp.md).

</TabItem>

</Tabs>

### Create a Deployment and confirm the install

When Astronomer support confirms that your Astro cluster has been created, you can create a Deployment and start deploying DAGs. See [Create a Deployment](create-deployment.md). 

To confirm a successful installation, in the Cloud UI select a Workspace and on the **Deployments** page click **Deployment**. The Astro cluster created by Astronomer support appears as an option in the **Cluster** list.

## Next steps

- [Set up an identity provider](configure-idp.md)
- [Install CLI](cli/overview.md)
- [Configure Deployments](configure-deployment-resources.md)
- [Deploy code](deploy-code.md)
- [Add users](add-user.md)
