---
sidebar_label: 'Azure'
title: 'Install Astro Hybrid on Azure'
id: install-azure-hybrid
sidebar_custom_props: { icon: 'img/azure.png' }
toc_min_heading_level: 2
toc_max_heading_level: 2
description: 'Use this document to complete the installation of Astro Hybrid in a Microsoft Azure subscription.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::caution

This document applies only to [Astro Hybrid](hybrid-overview.md). To see whether you're an Astro Hybrid user, click your Workspace name in the upper left corner of the Cloud UI, then click **Organization Settings**. Your Astro product type is listed under **Product Type** on the **General** page.

To create a cluster on Astro Hosted, see [Create a dedicated cluster](create-dedicated-cluster.md).

:::

To install Astro Hybrid on Azure, Astronomer will create an Astro cluster in a dedicated Azure account that's hosted and owned by your organization. This ensures that all data remains within your network and allows your organization to manage infrastructure billing.

To complete the installation, you'll:

- Create an Astronomer account.
- Create a new Azure subscription with the required Azure resources.
- Add the IAM service principal to Azure AD that'll be used by Astro.

Astronomer support will create infrastructure within your AWS account to host the resources and Apache Airflow components necessary to deploy DAGs and execute tasks. If you need more than one Astro cluster, contact [Astronomer support](https://cloud.astronomer.io/support).

## Prerequisites

- A new [Azure subscription](https://learn.microsoft.com/en-us/dynamics-nav/how-to--sign-up-for-a-microsoft-azure-subscription). For security reasons, Azure subscriptions with existing infrastructure aren't supported. Also, no [Azure policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview) should be applicable to the subscription's [Azure management group](https://docs.microsoft.com/en-us/azure/governance/management-groups/overview).

- An Azure AD user with the following role assignments:

    - `Application Administrator`. See [Understand roles in Azure Active Directory](https://docs.microsoft.com/en-us/azure/active-directory/roles/concept-understand-roles).

    - `Owner` with permission to create and manage subscription resources of all types. See [Azure built-in roles](https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles).

    This Azure AD user is required for data plane activation. You can remove the user or modify their role assignments after the cluster is created.

- [Microsoft Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) or [Azure Az PowerShell module](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps).

- A CIDR block with a range of `/19`. If you don't have any preferred CIDR block, Astro will provision a VPC using a default of `172.20.0.0/19`. Astro uses this VPC for four subnets, one each for database, pods, nodes, and private endpoints. See [Azure resource reference](resource-reference-azure-hybrid.md) for details.

- A minimum quota of 48 Standard Ddv5-series vCPUs in the selected region. You can use Dv5-series vCPUs, but you'll need 96 total vCPUs composed of 48 Ddv5-series vCPUs and 48 Dv5-series vCPUs. To adjust your quota limits up or down, see [Increase VM-family vCPU quotas](https://docs.microsoft.com/en-us/azure/azure-portal/supportability/per-vm-quota-requests).

    Confirm that the VM types are available in all Availability Zones in the selected region. For example, you can run the following Azure Az PowerShell command to confirm that the Standard_D4d_v5 VMs (the default for Astro) are available in the `CentralUS` region: 

    ```  
    az vm list-skus --location centralus --size Standard_D --all --output table | grep -e 'Restrictions\|Standard_D4d_v5'
    ```  
  
    If the VM types are unavailable, the output returns `Restrictions`. Contact Microsoft Support to have these VMs enabled.
  
    ```
    ResourceType     Locations    Name                    Zones    Restrictions
    virtualMachines  centralus    Standard_D4d_v5          1,2,3    NotAvailableForSubscription, type: Zone, locations: centralus, zones: 1
    ```

- A subscription to the [Astro status page](https://status.astronomer.io). This ensures that you're alerted when an incident occurs or when scheduled maintenance is planned.

- The following domains added to your organization's allowlist for any user and CI/CD environments:
    - `https://cloud.astronomer.io/`
    - `https://api.astronomer.io/`
    - `https://images.astronomer.cloud/`
    - `https://auth.astronomer.io/`
    - `https://updates.astronomer.io/`
    - `https://install.astronomer.io/`
    - `https://<your-org>.astronomer.run/`
    - `https://astro-<your-org>.datakin.com/`

### VNet peering prerequisites (Optional)

To give Astro access to any Azure resources on a private network, you must create a VNet peering connection between Astronomer's VNet and the VNets for your broader network. 

To create a VNet peering connection, contact [Astronomer Support](https://support.astronomer.io/) and provide the following details:

- Azure TenantID of the target VNet
- Subscription ID of the target VNet
- Region of the target VNet
- VNet ID of the target VNet
- ResourceGroup of the target VNet
- A CIDR block (RFC 1918 IP Space) no smaller than a `/19` range. This CIDR block can't overlap with any Azure VNet(s) that you will peer with later. The default CIDR range is `172.20.0.0/19`.
- ResourceID, for example: `/subscriptions/<Subscription Id>/resourceGroups/myResourceGroupA/providers/Microsoft.Network/virtualNetworks/myVnetA`. You can find the resource ID in the Azure portal by following step 7 in [Create peering - Azure portal](https://docs.microsoft.com/en-us/azure/virtual-network/create-peering-different-subscriptions#portal).

Additionally, ensure that your Azure AD user has at least one of the following role assignments: 

-  Network Contributor: This permission is required for any VNet deployed through Resource Manager.
-  Classic Network Contributor: This permission is required for any VNet deployed through the classic deployment model.
  
From here, Astronomer support will set up the VNet connection to Astro.

## Access Astro

1. Go to https://cloud.astronomer.io/ and create an account, or enter your email address, and then click **Continue**.

2. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**.
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in an Organization to authenticate, you're added as a Workspace Owner to a new Workspace named after your Organization. You can add other team members to the Workspace without the assistance of Astronomer support. See [Manage Workspace users](manage-workspace-users.md). 
    
    To integrate an identity provider (IdP) with Astro, see [Set up an identity provider](configure-idp.md).

## Prepare for data plane activation

The data plane is a collection of Astro infrastructure components that run in your cloud and are managed by Astronomer. This includes a central database, storage for Airflow tasks logs, and the resources required for task execution.

<Tabs
    defaultValue="azure"
    groupId= "step-2-prepare-for-data-plane-activation"
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

## Provide setup information to Astronomer support

After you've prepared your environment for data plane activation, provide Astronomer support with the following information:

- Your preferred Astro cluster name.
- Your Azure TenantID and SubscriptionID.
- Your preferred region. The default is `centralus`.
- Optional. Your preferred node instance type. The default is Standard_D4d_v5.
- Optional. Your preferred Postgres Flexible Server instance type. The default is Standard_D4ds_v4.
- Optional. Your preferred maximum node count. The default is 20.
- Optional. Your custom CIDR ranges for Astronomer service connections. The default is `172.20.0.0/19`.

See [Azure resource reference](resource-reference-azure-hybrid.md) for all supported cluster configurations.

## Astronomer support creates the cluster

After you provide Astronomer support with the setup information for your cluster, Astronomer support creates the cluster on Azure. Wait for confirmation from Astronomer support that the cluster has been created before creating a Deployment.

## Create a Deployment and confirm the install

When Astronomer support confirms that your Astro cluster has been created, you can confirm it in the [Cloud UI](https://cloud.astronomer.io) by clicking on the Astronomer icon in the top left corner, then click on **Clusters** to see your cluster. You can then [create a Deployment](create-first-DAG#step-1-create-a-deployment) and start to [develop and deploy your DAGs](create-first-DAG#step-2-create-an-astro-project).

## Next steps

- [Set up an identity provider](configure-idp.md)
- [Install CLI](cli/overview.md)
- [Deployment settings](deployment-settings.md)
- [Deploy code](deploy-code.md)
- [Manage Organization users](manage-organization-users.md)
