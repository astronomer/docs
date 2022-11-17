---
title: 'Install Astro on AWS using a cross-account role'
id: 'cross-account-role-setup'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


:::caution

This feature is in [Private Preview](feature-previews.md) and is an alternative to the standard AWS installation process. For the standard installation, see [Install Astro on AWS](install-aws.md)

:::

To install Astro in a dedicated AWS account owned by your organization, you'll complete the following tasks:

- Create an account on Astro.
- Share AWS account information with Astronomer support.
- Create a cross-account IAM role that Astro can assume within your new AWS account.

Astronomer support will create a cluster within your AWS account to host the resources and Airflow components necessary to deploy DAGs and execute tasks. If you need more than one Astro cluster, contact [Astronomer support](https://cloud.astronomer.io/support).

## Prerequisites

- A dedicated AWS account with the minimum EC2 service quotas.
- A subscription to the [Astro Status Page](https://status.astronomer.io/). This ensures that you'll be notified when there are incidents or when maintenance is scheduled.
- The following domains added to your organization's allowlist for any user and CI/CD environments:
   
    - `https://cloud.astronomer.io/`
    - `https://astro-<your-org>.datakin.com/`
    - `https://<your-org>.astronomer.run/`
    - `https://api.astronomer.io/`
    - `https://images.astronomer.cloud/`
    - `https://auth.astronomer.io/`
    - `https://updates.astronomer.io/`
    - `https://install.astronomer.io/`

Astro requires a clean AWS account with the minimum EC2 service quotas. For security reasons, the install process is not currently supported on an AWS account that has other tooling running in it. For instructions on creating a new AWS account, see [How do I create and activate a new AWS account?](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).

The following table lists the required [EC2 service quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html).

| QuotaCode  | QuotaName                                                        | Minimum Value  |
| -----------| ---------------------------------------------------------------- | ---------------|
| L-1216C47A | Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances | 40             |
| L-34B43A08 | All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests  | 40             |

These quotas are required to mitigate near term capacity risks and simplify the Astro onboarding experience. If you need to modify or increase a specific quota, see [Request a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html).

:::tip

If you have one or more existing AWS accounts, you can use [AWS Organizations](https://aws.amazon.com/organizations/) to manage billing, users, and more in a central place. For more information on how to add your Astro AWS account to your AWS Organization, see [Inviting an AWS account to join your organization](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_invites.html).

:::

### VPC peering prerequisites (Optional)

The following options are available when your AWS resources are on a private network:

- Allow traffic through the public internet and use allow-lists for communication.
- Create a VPC Peering connection between the Astronomer VPC and the VPCs for your network.

If you want to continue with the second option, you'll additionally need:

- A CIDR block (RFC 1918 IP Space) no smaller than a `/19` range. You must ensure it does not overlap with the AWS VPC(s) that you will be peering with later. The default CIDR range is `172.20.0.0/19`.
- VPC Name / ID for peering with Astronomer (accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/)).
- The IP addresses of your DNS servers.

## Step 1: Create an IAM role for Astronomer

Astro requires an IAM role that delegates specific permissions for your data plane account to the Astro control plane. These permissions are required to manage the data plane and the data plane account.

To preview this role in its entirety, see its [CloudFormation template](https://astro-cross-account-role-template.s3.us-east-2.amazonaws.com/customer-account-prerelease.yaml).

### Permissions used to manage data plane resources

As the Astro service changes, Astronomer support might change the role policy attached to the cross-account role. Astronomer support informs all organizations by email before implementing any changes. To make sure you receive these notifications, subscribe to the [Status Page](https://status.astronomer.io/). 

The following table lists the permissions required by Astro to manage the cross-account role.

| Permissions                                           | Purpose                                                                                                                        |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `cloudformation:*`                                     | Setup, teardown, and update the data plane.                                                                                   |
| `eks:*`                                                | Manage EKS clusters.                                                                                                          |
| `ec2:*`                                                | Manage the compute and network infrastructure.                                                                                    |
| `rds:*`                                                | Manage the Amazon Relational Database Service (RDS).                                                                                              |
| `s3:*`                                                 | Manage S3 buckets used by Astro clusters. For example, the bucket used for logging.                                          |
| `sts:* `                                               | Manage the tokens required for accessing AWS services.                                                                            |
| `autoscaling:*`                                        | Manage the autoscaling policies for Astro infrastructure.                                                                         |
| `cloudwatch:* , logs:* `                               | Monitor the health of AWS resources.                                                                                              |
| `kms:*`                                                | Manage the keys used by Astro.                                                                                                    |
| `secretsmanager:*`                                     | Store the secrets used internally by the Astro cluster.                                                                               |
| `lambda:*`                                             | Scripts used to automate internal cluster operations. For example, to issue OIDC tokens to EKS clusters.                     |
| `route53:*`                                            | Resolve the DNS names of the services used by your data pipelines but running in other AWS accounts.                                  |
| `servicequotas:*`                                      | Monitor Service Quotas to ensure resource availability.                                                                |
| `ce:*`                                                 | Monitor costs.                                                                                                                |
| `iam:Get* , iam:List* , iam:Tag*  , iam:Untag*`        | Enumerate and tag IAM objects, such as roles and policies.                                                                    |
| `iam:OpenIDConnectProvider* `                          | Enable IAM Roles for Service Access.                                                                                          |
| `iam:CreateRole iam:DeleteRole`                        | Create Operational Roles for the Astro cluster. This policy denies deletion of roles tagged with `customeraudit=True`. |
| iam:AttachRolePolicy , iam:PutRolePolicy , iam:Detach* | Create the Operational Boundary and Permissions Policy for operational roles used by Astro clusters.                              |
| iam:*InstanceProfile                                   | Manage the instance profiles for cluster nodes.                                                                                   |
| iam:CreateServiceLinkedRole  iam:PassRole              | Manage the internal roles used by AWS services.                                                                                   |

### Permissions used to manage the cross-account role

As the Astro service changes, Astronomer support might change the role policy attached to the cross-account role. Astronomer support informs all organizations by email before implementing any changes. To make sure you receive these notifications, subscribe to the [Status Page](https://status.astronomer.io/). 

The following table lists the permissions required by Astro to manage the cross-account role.

| Permissions                                                                               | Purpose                                                |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `iam:CreatePolicy , iam:CreatePolicyVersion , iam:DeletePolicy , iam:DeletePolicyVersion` | Manage the policy attached to the cross-account role. |

#### Monitor the cross-account role for changes (optional)

Astronomer recommends setting up a CloudTrail in the data plane account to monitor changes to the cross-account role policy. The following table lists the events that you should monitor. 

| Event Names                              | Resource                                                         |
| ---------------------------------------- | ---------------------------------------------------------------- |
| `AttachRolePolicy , DetachRolePolicy`    | `roleName = astronomer-remote-management`                        |
| `SetPolicyVersion , CreatePolicyVersion` | `policyArn = "arn:aws:iam::*:policy/AstronomerCrossAccountRole"` |

To monitor changes to the cross-account role policy, create an Amazon CloudWatch alarm. See [Creating CloudWatch alarms for CloudTrail events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html).  When you create the metric filter, on the Define pattern page, in Create filter pattern, enter the following for Filter pattern:

```
{ ($.eventName = AttachRolePolicy || $.eventName = DetachRolePolicy || $.eventName = SetPolicyVersion || $.eventName = CreatePolicyVersion) && ($.requestParameters.policyArn = "*AstronomerCrossAccountRole"  || $.requestParameters.roleName = astronomer-remote-management) }
```

## Step 2: Access Astro

1. Go to https://cloud.astronomer.io/ and create an account, or enter your email address, and then click **Continue**.

2. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**.
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in your Organization to authenticate, you'll be granted Organization owner permissions. You can create a Workspace and add other team members to the Workspace without the assistance of Astronomer support. See [Create a Workspace](manage-workspaces.md#create-a-workspace) and [Add a user](add-user.md). To integrate an identity provider (IdP) with Astro, see [Set up an identity provider](configure-idp.md).

## Step 3: Retrieve an external ID from the Cloud UI

You must be an Organization Owner to view the external ID. If you are not an Organization Owner, the **AWS External ID** field will not appear in the Cloud UI.

1. In the Cloud UI, click the **Settings** tab.

2. Click **Show** in the **AWS External ID** field and then click **Copy**. This external ID is a unique identifier that Astro uses to connect to your AWS account. 

3. Save the external ID as a secret or in another secure format. See [How to use an external ID when granting access to your AWS resources to a third party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).


## Step 4: Create a cross-account role

Use the external ID to create a cross-account IAM role for Astro. Astronomer recommends using the AWS Management Console to create the role.

<Tabs
    defaultValue="managementconsole"
    groupId= "step-3-create-a-cross-account-iam-role-for-astro"
    values={[
        {label: 'AWS Management Console', value: 'managementconsole'},
        {label: 'AWS Command Line', value: 'commandline'},
    ]}>
<TabItem value="managementconsole">

1. Open the [Astronomer cross-account role CloudFormation template](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?templateURL=https://astro-cf-templates-main.s3.us-east-2.amazonaws.com/customer-account-prerelease.yaml&stackName=AstroPreReleaseCrossAcccount).

2. Enter the external ID that you copied in Step 2 in the **ExternalId** field.

3. Select the **I acknowledge that AWS CloudFormation might create IAM resources with custom names** checkbox.

4. Click **Create Stack**.

</TabItem>

<TabItem value="commandline">

1. Create a command line-level environment variable named `EXTERNAL_ID` that contains the External ID you copied in step 2.
2. Run the following command to create the Astronomer remote management role.
    
    ```sh
    #!/bin/sh
    
    set -eo pipefail
    
    if [ -z "$EXTERNAL_ID" ]
    then
      echo 'Missing required variable EXTERNAL_ID' >&2
      exit 1
    fi
    
    POLICY_NAME='AstronomerCrossAccountRole'
    POLICY_DESCRIPTION='Permissions boundary for Astronomer cross-account management role'
    POLICY_URL='https://astro-cross-account-role-template.s3.us-east-2.amazonaws.com/customer-account-prerelease.json'
    POLICY_FILE='/tmp/policy.json'
    
    if [ ! -f "$POLICY_FILE" ]
    then
      echo "Download $POLICY_NAME policy document"
    
      ACCOUNT_ID="$(aws sts get-caller-identity --query 'Account' --output text)"
      curl "$POLICY_URL" | sed "s/{{.AWSAccount}}/$ACCOUNT_ID/" > "$POLICY_FILE"
    fi
    
    echo "Create $POLICY_NAME policy"
    # Retrieve the new policy's ARN, but also print the output of aws iam create-policy to stdout
    { POLICY_ARN=$( \
      aws iam create-policy --policy-name "$POLICY_NAME" --policy-document "$(cat "$POLICY_FILE")" --description "$POLICY_DESCRIPTION" \
      | tee /dev/fd/3 \
      | sed -rn 's/"Arn"://p' \
      | tr -d '[:space:]",'); } 3>&1
    
    ROLE_NAME='astronomer-remote-management'
    ASSUME_ROLE_POLICY=$(cat << EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::406882777402:root"
          },
          "Action": "sts:AssumeRole",
          "Condition": {
            "StringEquals": {
            "sts:ExternalId": "$EXTERNAL_ID"
            }
          }
        }
      ]
    }
    EOF
    )
    
    echo "Create $ROLE_NAME role"
    aws iam create-role --role-name "$ROLE_NAME" --assume-role-policy-document "$ASSUME_ROLE_POLICY"
    
    echo "Attach $POLICY_NAME to $ROLE_NAME"
    aws iam attach-role-policy --policy-arn "$POLICY_ARN" --role-name "$ROLE_NAME"
    
    echo 'Setup complete'
    ```

</TabItem>
</Tabs>


## Step 5: Provide setup information to Astronomer

After creating the AWS account, provide Astronomer support with the following information:

- Your AWS Account ID.
- Your preferred Astro cluster name.
- The AWS region that you want to host your cluster in.
- Your preferred node instance type.
- Your preferred maximum node count.

If you do not specify configuration preferences, Astronomer creates a cluster with `m5.xlarge` nodes and a maximum node count of 20 in `us-east-1`. For information on all supported regions, configurations, and defaults, see [AWS cluster configurations](resource-reference-aws.md).

To provision additional clusters after completing your initial installation, see [Create a cluster](create-cluster.md).

:::caution

Some AWS regions that Astronomer supports are disabled by default on AWS, including:
- `ap-east-1` - Asia Pacific (Hong Kong)
- `me-south-1` - Middle East (Bahrain)

If you're setting up your first cluster in any of these regions, you need to complete the additional setup described in [Create a cluster](create-cluster.md#additional-setup-for-aws-regions-that-are-disabled-by-default).

:::

### Provide VPC peering information (optional)

If you need to VPC peer with Astronomer, provide the following information to your Astronomer representative:

- Subnet CIDRs (RFC 1918 IP Space).
- VPC Name/ID and region for peering with Astronomer. This is accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/).
- The IPs of your DNS servers.

## Step 5: Astronomer support creates the cluster

After you've created the cross-account IAM role for Astro, contact [Astronomer support](https://cloud.astronomer.io/support). Astronomer support creates the cluster in your AWS account.

This process can take some time. Wait for confirmation from Astronomer support that the cluster has been created before creating a Deployment.

If you submitted a VPC peering request, you'll need to accept the request from Astronomer after Astro is installed. To accept the request, see [Create a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html).

When VPC peering with Astronomer is complete, configure and validate the following items to ensure successful network communications between Astro and your resources:

- Egress Routes on Astronomer Route Table
- [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html#nacl-tasks) and/or [Security Group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#working-with-security-groups) rules of your resources

## Next steps

Congratulations on installing Astro on AWS! Astronomer recommends completing some of the following actions to make the most of your new installation.

### Create a Deployment

When Astronomer support confirms that your Astro cluster has been created, you can create a Deployment and start deploying DAGs. See [Create a Deployment](create-deployment.md). When you create your Deployment, the Astro cluster created by Astronomer support appears as an option in the **Cluster** list as shown in the following image.

![Cloud UI New Deployment screen](/img/docs/create-new-deployment-select-cluster.png)


### Read the documentation

The following documents include setup steps for key Astro features and tools: 

- [Set up an identity provider](configure-idp.md)
- [Install CLI](cli/overview.md)
- [Configure Deployments](configure-deployment-resources.md)
- [Deploy code](deploy-code.md)
- [Add users](add-user.md)
