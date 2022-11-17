---
title: 'Install Astro on AWS using a cross-account role'
id: 'cross-account-role-setup'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


:::caution

This feature is in [Private Preview](feature-previews.md) and is an alternative to the standard AWS installation process. For the standard installation steps, see [Install Astro on AWS](install-aws.md)

:::

To install Astro in a dedicated AWS account owned by your organization, you'll complete the following tasks:

- Create an account on Astro.
- Share AWS account information with Astronomer support.
- Create a cross-account IAM role that Astro can assume within your new AWS account.

Astronomer support will create a cluster within your AWS account that hosts the resources and Apache Airflow components necessary to deploy DAGs and execute tasks. If you'd like to support more than 1 Astro cluster, contact [Astronomer support](https://cloud.astronomer.io/support).

## Step 1: Create an IAM role for Astronomer

Astro requires an IAM role that delegates specific permissions for your data plane account to the Astro control plane. These permissions are required to manage the data plane and the data plane account itself.

See the following tables to learn more about each required permission and its purpose. To preview this role in its entirety, see its [CloudFormation template](https://astro-cross-account-role-template.s3.us-east-2.amazonaws.com/customer-account-prerelease.yaml).

### Permissions used to manage data plane resources

As the Astro service changes, Astronomer may change the role policy attached to this cross account role. Astronomer will only make such changes after pre-announcing them via email. Please make sure you are subscribed to the [Status Page](https://status.astronomer.io/) to receive these alerts. 

To perform this function, Astro requires the following permissions to manage the cross account role.

| Permissions                                            | Reason                                                                                                                        |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `cloudformation:*`                                     | Setup, teardown, and update the data plane.                                                                                   |
| `eks:*`                                                | Manage EKS clusters.                                                                                                          |
| `ec2:*`                                                | Manage compute and network infrastructure.                                                                                    |
| `rds:*`                                                | Manage the backing RDS database.                                                                                              |
| `s3:*`                                                 | Manage S3 buckets used by Astro clusters (for example, the bucket used for logging).                                          |
| `sts:* `                                               | Manage tokens required for accessing AWS services.                                                                            |
| `autoscaling:*`                                        | Manage autoscaling policies for Astro infrastructure.                                                                         |
| `cloudwatch:* , logs:* `                               | Monitor health of AWS resources.                                                                                              |
| `kms:*`                                                | Manage keys used by Astro.                                                                                                    |
| `secretsmanager:*`                                     | Store secrets used internally by Astro cluster.                                                                               |
| `lambda:*`                                             | Scripts used to automate internal cluster operations (for example, to issue OIDC tokens to EKS clusters).                     |
| `route53:*`                                            | Resolve DNS names of services used by your data pipelines but running in other AWS accounts.                                  |
| `servicequotas:*`                                      | Monitor Service Quotas to ensure enough resource availability.                                                                |
| `ce:*`                                                 | Monitor costs.                                                                                                                |
| `iam:Get* , iam:List* , iam:Tag*  , iam:Untag*`        | Enumerate and tag IAM objects, such as roles and policies.                                                                    |
| `iam:OpenIDConnectProvider* `                          | Enable IAM Roles for Service Access.                                                                                          |
| `iam:CreateRole iam:DeleteRole`                        | Create Operational Roles for Astro cluster. Note that this policy denies deletion of roles tagged with `customeraudit=TRUE` . |
| iam:AttachRolePolicy , iam:PutRolePolicy , iam:Detach* | Create Operational Boundary and Permissions Policy for operational roles used by Astro clusters.                              |
| iam:*InstanceProfile                                   | Manage instance profiles for cluster nodes.                                                                                   |
| iam:CreateServiceLinkedRole  iam:PassRole              | Manage internal roles used by AWS services.                                                                                   |

### Permissions used to manage the cross-account role

As Astro changes, Astronomer may change the role policy attached to this cross account role. Astronomer will make changes to the role policy only after pre-announcing them through email. Subscribe to the [Status Page](https://status.astronomer.io/) to ensure that you receive these alerts. 

To perform this function, Astro requires the following permissions to manage the cross account role.

| Permissions                                                                               | Reason                                                |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `iam:CreatePolicy , iam:CreatePolicyVersion , iam:DeletePolicy , iam:DeletePolicyVersion` | Manage the policy attached to the cross-account role. |

#### Monitor the cross-account role for changes (optional)

To monitor changes to the cross-account role policy, Astronomer recommends setting up a CloudTrail in the data plane account and monitoring it for the following events: 

| Event Names                              | Resource                                                         |
| ---------------------------------------- | ---------------------------------------------------------------- |
| `AttachRolePolicy , DetachRolePolicy`    | `roleName = astronomer-remote-management`                        |
| `SetPolicyVersion , CreatePolicyVersion` | `policyArn = "arn:aws:iam::*:policy/AstronomerCrossAccountRole"` |

To use CloudWatch to monitor this trail, follow the instructions in [Creating CloudWatch alarms for CloudTrail events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html) to apply the following filter to your CloudWatch metric:

```text
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

## Step 3:Retrieve an external ID from the Cloud UI

You must be an Organization Owner to view the external ID. If you are not an Organization Owner, the field will not appear in the Cloud UI.

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

1. Create a command line-level environment variable named `EXTERNAL_ID` that contains the External ID you copied in the previous step.
2. Open the AWS CLI and run the following command to create a cross-account IAM Role:

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


## Step 4: Provide setup information to Astronomer

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

### VPC peering prerequisites (optional)

If you need to VPC peer with Astronomer, provide the following information to your Astronomer representative:

- Subnet CIDRs (RFC 1918 IP Space).
- VPC Name/ID and region for peering with Astronomer. This is accessible through the [AWS VPC console](https://console.aws.amazon.com/vpc/).
- The IPs of your DNS servers.

## Step 4: Astronomer support creates the cluster

After you've created the cross-account IAM role for Astro, contact [Astronomer support](https://cloud.astronomer.io/support). Astronomer support will finish creating the cluster in your AWS account.

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


### Additional documentation

The following documents include setup steps for key Astro features and tools: 

- [Set up an identity provider](configure-idp.md)
- [Install CLI](cli/overview.md)
- [Configure Deployments](configure-deployment-resources.md)
- [Deploy code](deploy-code.md)
- [Add users](add-user.md)
