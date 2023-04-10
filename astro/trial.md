---
title: 'Start your Astro trial'
id: trial
sidebar_label: 'Start a trial'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Use this guide to get started with Astro, the best place to run Apache Airflow.

## Start a trial

Go to [Try Astro](https://www.astronomer.io/try-astro/) to activate your free 14-day trial. To create your Astro user account, you'll need to provide a valid email address and create a password.

## Create an Organization and Workspace

After you've created your Astro user account, you'll be asked to create an Organization and your first Workspace. 

An **Organization** is the highest management level on Astro. An Organization contains **Workspaces**, which are collections of Deployments, or Airflow environments, that are typically owned by a single team. You can manage user roles and permissions both at the Organization and Workspace levels.

To start your trial, Astronomer recommends using the name of your company as the name of your Organization and naming your first Workspace after your data team or initial business use case with Airflow. You can update these names in the Cloud UI after you finish activating your trial. 

## Create a cluster

To run Astro in your cloud, you'll need to create an Astro cluster. An Astro cluster is a set of infrastructure resources within your organization's data plane that hosts Deployments, or Airflow environments on Astro.

To create a cluster, you first need a dedicated account with your cloud provider that Astronomer can access. This account allows Astronomer to fully manage the infrastructure resources required to run Airflow at scale for your team.

After you've created your Organization and Workspace, your new Workspace homepage appears. Click **Create Cluster** and then complete the setup for your cloud provider.

<Tabs
    defaultValue="aws"
    groupId= "create-a-cluster"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
        {label: 'Azure', value: 'azure'},
    ]}>
<TabItem value="aws">

1. Create a dedicated [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) for Astro. Astro uses this account to provision and manage your cluster resources. For security reasons, you cannot currently create an Astro cluster within an AWS account that has other tooling running in it.

2. Copy the **Account ID** for Step 5.

    When creating your account, specify the following [EC2 service quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html):
    
    | QuotaCode  | QuotaName                                                        | Minimum Value  |
    | -----------| ---------------------------------------------------------------- | ---------------|
    | L-1216C47A | Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances | 40             |
    | L-34B43A08 | All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests  | 40             |
    
    These quotas ensure a smooth onboarding experience on Astro. If you need to modify or increase a specific quota, see [Request a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html)in Amazon’s documentation.

3. On the Astro cluster creation screen, click **Launch AWS stack creation**.
   
4. In AWS CloudFormation, click **Create stack**. A cross-account Identity and Access Management (IAM) role is created to provide Astronomer support with access to the Astro AWS account.
   
5. In the Cloud UI cluster creation screen, enter your AWS account ID in **AWS Account ID**.
   
6. In the **Region** list, select the region where your cluster will be hosted. For trials, Astronomer recommends choosing the region that's closest to you.
   
7. Optional. Click **Advanced** and configure a VPC subnet range for Astro to connect to your AWS account through VPC peering. 
   
8. Click **Create cluster**. 
   
9. Wait for Astronomer to finish creating the cluster. You'll receive an email notification when the process is complete. 

    The cluster is created with a default set of resources that are suitable for most use cases. See [AWS cluster settings](resource-reference-aws.md#default-cluster-values) for a list of all default resources.

</TabItem>
<TabItem value="gcp">

1. Create a dedicated [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) for Astro with billing enabled. Astro uses this account to provision and manage your cluster resources. For security reasons, the install process is not currently supported on a Google Cloud project that has other tooling running in it. 

2. Copy the project ID for step 5.
   
3. In the Cloud UI, click **Launch Google Cloud Shell** on the cluster creation screen.
   
4. In your cloud shell, run `./bootstrap.sh` and follow the steps to grant Astro access to your GCP project. 
   
5. In the Cloud UI cluster creation screen, enter your GCP Project ID in **GCP Project ID**.
   
6. In the **Region** list, select the region where you want to host your cluster. For trials, Astronomer recommends choosing the region that's closest to you.
   
7. Optional. Click **Advanced** and configure VPC subnet ranges for Astro to connect to your GCP project through VPC peering. 
   
8. Click **Create cluster**.
   
9. Wait for Astronomer to finish creating the cluster. You'll receive an email notification when the process is complete. 

    The cluster is created with a default set of resources that are suitable for most use cases. See [GCP cluster settings](resource-reference-gcp.md#default-cluster-values) for a list of all default resources.

</TabItem>
<TabItem value="azure">

1. Create a dedicated [Azure subscription](https://learn.microsoft.com/en-us/dynamics-nav/how-to--sign-up-for-a-microsoft-azure-subscription) for Astro. Astro uses this account to provision and manage your cluster resources. The subscription must be included in an Azure management group that doesn't apply Azure policies. See [What are Azure management groups](https://docs.microsoft.com/en-us/azure/governance/management-groups/overview).

2. Copy the subscription ID for step 5.

3. In the Azure portal for your subscription, find and copy your [Azure Tenant ID](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-how-to-find-tenant#find-tenant-id-through-the-azure-portal) for step 5.

4. Grant Astronomer access to your Azure subscription through either the Azure CLI or Powershell.

    <Tabs
        defaultValue="azure"
        groupId= "create-a-cluster"
        values={[
            {label: 'Azure CLI on Bash', value: 'azure'},
            {label: 'PowerShell', value: 'powershell'},
        ]}>
    <TabItem value="azure">

    1. Run the following command to log in to your Azure account:
    
        ```sh
        az login
        ```

    2. Run the following command to select your Azure subscription:
    
        ```sh
        az account set -s <subscription-id>
        ```

    3. Run the following command to add the Astronomer Service Principal to Azure AD:
    
        ```sh
        az ad sp create --id a67e6057-7138-4f78-bbaf-fd9db7b8aab0
        ```

    4. Run the following commands to get details about the Azure subscription and create a new role assignment for the Astronomer service principal:
    
        ```sh
        subid=$(az account show --query id --output tsv)
        az role assignment create --assignee a67e6057-7138-4f78-bbaf-fd9db7b8aab0 --role Owner --scope /subscriptions/$subid
        ```

    5. Run the following commands to register the `EncryptionAtHost` feature:
    
        ```sh
        az feature register --namespace "Microsoft.Compute" --name "EncryptionAtHost"
        while [ $(az feature list --query "[?contains(name, 'Microsoft.Compute/EncryptionAtHost')].{State:properties.state}" -o tsv) != "Registered" ]
        do
        echo "Still waiting for Feature Registration (EncryptionAtHost) to complete, this can take up to 15 minutes"
        sleep 60
        done
        echo "Registration Complete"
        az provider register --namespace Microsoft.Compute
        ```

    </TabItem>

    <TabItem value="powershell">

    1. Run the following command to log in to your Azure account:
    
        ```sh
        Connect-AzAccount
        ```
    
    2. Run the following command to select your Azure subscription:
    
        ```sh
        Set-AzContext -SubscriptionId <subscription-id>
        ```

    3. Run the following command to create the Astronomer service principal:
    
        ```sh
        $sp = New-AzADServicePrincipal -AppId a67e6057-7138-4f78-bbaf-fd9db7b8aab0
        ```

    4. Run the following commands to get details about the Azure subscription and create a new role assignment for the Astronomer service principal:
    
        ```sh
        $sp = Get-AzADServicePrincipal -ApplicationId a67e6057-7138-4f78-bbaf-fd9db7b8aab0
        ```

        ```sh
        $subid = (Get-AzContext).Subscription.id
        ```

        ```sh
        $ra = New-AzRoleAssignment -ObjectId $sp.id -RoleDefinitionName Owner -Scope "/subscriptions/$subid"
        ```

    5. Run the following commands to register the `EncryptionAtHost` feature:
    
        ```sh
        Register-AzProviderFeature -FeatureName EncryptionAtHost -ProviderNamespace Microsoft.Compute
        while ( (Get-AzProviderFeature -FeatureName EncryptionAtHost -ProviderNamespace Microsoft.Compute).RegistrationState -ne "Registered") {echo "Still waiting for Feature Registration (EncryptionAtHost) to complete, this can take up to 15 minutes"; sleep 60} echo "Registration Complete"
        ```

        ```sh
        Register-AzResourceProvider -ProviderNamespace Microsoft.compute
        ```

    </TabItem>
    </Tabs>

5. In the Cloud UI cluster creation screen, enter your Azure Tenant ID in the **Azure Tenant ID** field.

6. Enter your Azure Subscription ID in **Azure Subscription ID** field.
   
7. In the **Region** list, select the region where you want to host your cluster. For trials, Astronomer recommends choosing the region that's closest to you.
   
8. Optional. Click **Advanced** and configure a VNet subnet range for Astro to connect to your Azure subscription through VPC peering. 
   
9. Click **Create cluster**. 
   
10. Wait for Astronomer to finish creating the cluster. You'll receive an email notification when the process is complete.

    The cluster is created with a default set of resources that are suitable for most use cases. See [Azure cluster settings](resource-reference-azure.md#default-cluster-values) for a list of all default resources.

</TabItem>
</Tabs>

## Next steps

After Astronomer creates your cluster, you're ready to start deploying and running DAGs on Astro. Complete the following tasks to get your first DAG up and running on Astro: 

1. [Install the Astro CLI](cli/install-cli.md). The Astro CLI is an open source command line interface for developing Airflow DAGs on your local machine and deploying them to Astro
2. [Create an Astro project](create-first-dag.md#step-1-create-an-astro-project). An Astro project contains the set of files that you need to run Airflow on Astro. It includes dedicated folders for your Python packages and DAGs.
3. [Create a Deployment](create-deployment.md). A Deployment is an Astro Runtime environment that is powered by the core components of Apache Airflow and where you can run DAGs.
4. [Deploy your Astro project](deploy-code.md). Use the Astro CLI to push code to a Deployment on Astro in just a few minutes.

## After your trial

After your 14-day trial ends, you can no longer access your Deployments and Workspaces from the Cloud UI. You can still access your user account page and Astronomer support forms. Any DAGs you deployed will continue to run for an additional 7-day grace period.

After the 7-day grace period, your cluster and all Deployments within it are automatically deleted. Any code that you deployed to Astro will be lost. If you need additional time to evaluate Astro, or you need to copy your configuration for future use, you can:

- Schedule a call with your point of contact from Astronomer.
- Go to the Cloud UI and schedule a 15 minute call with an Astronomer engineer. This option is available only after your 14-day trial ends.
- Contact [Astronomer support](https://cloud.astronomer.io/support).
