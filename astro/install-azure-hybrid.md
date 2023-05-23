---
sidebar_label: 'Azure'
title: 'Install Astro Hybrid on Azure'
id: install-azure-hybrid
sidebar_custom_props: { icon: 'img/azure.png' }
toc_min_heading_level: 2
toc_max_heading_level: 2
---

<head>
  <meta name="description" content="Instructions for completing an Astro installation on an existing Microsoft Azure instance. This is where you’ll find the prerequisites and the process you’ll need to follow to allow Astronomer support to provision your network resources." />
  <meta name="og:description" content="Instructions for completing an Astro installation on an existing Microsoft Azure instance. This is where you’ll find the prerequisites and the process you’ll need to follow to allow Astronomer support to provision your network resources." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::caution

This document applies only to [Astro Hybrid](hybrid-overview.md). To see whether you're an Astro Hybrid user, click the Astronomer logo in the upper left corner of the Cloud UI and go to **Settings** > **General**. Your Astro product type is listed under **Product Type**.

To get started on Astro Hosted, see [Start a trial](trial.md).

:::

To install Astro Hybrid on Azure, Astronomer will create an Astro cluster in a dedicated Azure account that's hosted and owned by your organization. This ensures that all data remains within your network and allows your organization to manage infrastructure billing.

To complete the installation process, you'll:

- Add the Astronomer Service Principal to your Azure Active Directory (Azure AD) instance.
- Assign the Astronomer Service Principal an Owner role to your subscription.
- Register Microsoft Azure features.

When you've completed the installation process, Astronomer support creates a cluster within your Azure subscription to host the resources and Apache Airflow components necessary to deploy DAGs and execute tasks.

For more information about managing Azure subscriptions with the Azure CLI, see [How to manage Azure subscriptions with the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/manage-azure-subscriptions-azure-cli).

## Set up

<Tabs
    defaultValue="byoc"
    groupId= "byoc"
    values={[
        {label: 'Bring Your Own Cloud', value: 'byoc'},
        {label: 'Hosted', value: 'astronomer hosted data plane'},
    ]}>
<TabItem value="byoc">

### Prerequisites

- A clean Azure subscription. For security reasons, Azure subscriptions with existing tooling running aren't supported. Also, the subscription must be included in an Azure management group that doesn't apply Azure policies. See [What are Azure management groups](https://docs.microsoft.com/en-us/azure/governance/management-groups/overview).
- An Azure AD user with the following role assignments:

    - `Application Administrator`. See [Understand roles in Azure Active Directory](https://docs.microsoft.com/en-us/azure/active-directory/roles/concept-understand-roles).
    - `Owner` with permission to create and manage subscription resources of all types. See [Azure built-in roles](https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles).

    This Azure AD user is required for data plane activation. You can remove the user or modify their role assignments after the cluster is created.

- Microsoft Azure CLI or Azure Az PowerShell module.  See [How to install the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) and [Install the Azure Az PowerShell module](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps).
- A minimum quota of 48 Standard Ddv5-series vCPUs in the deployment region. You can use Dv5-series vCPUs, but you'll need 96 total vCPUs composed of 48 Ddv5-series vCPUs and 48 Dv5-series vCPUs. To adjust your quota limits up or down, see [Increase VM-family vCPU quotas](https://docs.microsoft.com/en-us/azure/azure-portal/supportability/per-vm-quota-requests).
- Confirmation that the VM types are available in all Availability Zones in the selected region. For example, you run the following Azure Az PowerShell command to confirm that the Standard_D4d_v5 VMs (the default for Astro) are available in the Central US region: 

    ```  
    az vm list-skus --location centralus --size Standard_D --all --output table | grep -e 'Restrictions\|Standard_D4d_v5'
    ```  
  
    If the VM types are unavailable, the output returns `Restrictions`. Contact Microsoft Support and ask to have the VMs enabled.
  
    ```
    ResourceType     Locations    Name                    Zones    Restrictions
    virtualMachines  centralus    Standard_D4d_v5          1,2,3    NotAvailableForSubscription, type: Zone, locations: centralus, zones: 1
    ```

- A subscription to the [Astro status page](https://status.astronomer.io). This ensures that you're alerted when an incident occurs or when scheduled maintenance is planned.
- The following domains added to your organization's allowlist for any user and CI/CD environments:
    - `https://cloud.astronomer.io/`
    - `https://astro-<your-org>.datakin.com/`
    - `https://<your-org>.astronomer.run/`
    - `https://api.astronomer.io/`
    - `https://images.astronomer.cloud/`
    - `https://auth.astronomer.io/`
    - `https://updates.astronomer.io/`
    - `https://install.astronomer.io/`

For more information about the resources required to run Astro on Azure, see [Azure Resource Reference](resource-reference-azure-hybrid.md).

#### VNet peering prerequisites (Optional)

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

### Access Astro

1. Go to https://cloud.astronomer.io/ and create an account, or enter your email address, and then click **Continue**.

2. Select one of the following options to access the Cloud UI:

    - Enter your password and click **Continue**.
    - To authenticate with an identity provider (IdP), click **Continue with SSO**, enter your username and password, and then click **Sign In**.
    - To authenticate with your GitHub account, click **Continue with GitHub**, enter your username or email address, enter your password, and then click **Sign in**.
    - To authenticate with your Google account, click **Continue with Google**, choose an account, enter your username and password, and then click **Sign In**.

    If you're the first person in an Organization to authenticate, you're added as a Workspace Admin to a new Workspace named after your Organization. You can add other team members to the Workspace without the assistance of Astronomer support. See [Add a user](add-user.md). To integrate an identity provider (IdP) with Astro, see [Set up an identity provider](configure-idp.md).

### Prepare for data plane activation

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

### Provide setup information to Astronomer support

After you've prepared your environment for data plane activation, provide Astronomer support with the following information:

- Your preferred Astro cluster name.
- Your Azure TenantID and SubscriptionID.
- Optional. Your preferred node instance type. The default is Standard_D4d_v5.
- Optional. Your preferred Postgres Flexible Server instance type. The default is Standard_D4ds_v4.
- Optional. Your preferred maximum node count.
- Optional. Your custom CIDR ranges for Astronomer service connections. The default is `172.20.0.0/19`.

If you don't specify a preferred configuration for your organization, Astronomer support creates a cluster in `CentralUS` with the default configurations for Astro on Azure. See [Azure resource reference](resource-reference-azure-hybrid.md).

### Astronomer support creates the cluster

After you provide Astronomer support with the setup information for your organization, Astronomer support creates your first cluster on Azure.

Wait for confirmation from Astronomer support that the cluster has been created before creating a Deployment.

</TabItem>

<TabItem value="astronomer hosted data plane">

:::info

This feature is currently Private Preview. Contact [Astronomer support](https://cloud.astronomer.io/support) to enable it.

:::

When providing hosting services, Astronomer adheres to industry best practices and standards including the Health Insurance Portability and Accountability Act (HIPAA), Service Organization Control 2 (SOC2), and  General Data Protection Regulation (GDPR). 

### Prerequisites

The setup process assumes that you've already provided Astronomer support with the following information: 

- Your preferred cluster installation region. See the supported region lists for [Azure](resource-reference-azure-hybrid.md#supported-regions).
- Optional. Your preferred worker instance type for your first cluster. See [Azure cluster configurations](resource-reference-azure-hybrid.md#worker-node-pools).
- Optional. Your VNet peering requirements for [Azure](install-azure-hybrid.md#vnet-peering-prerequisites-optional).
- The email address of your first Astro user.

If you haven't provided this information to Astronomer support, contact your Astronomer representative. 

### Astronomer support creates the cluster

Astronomer support creates your first Astro cluster in a dedicated Azure account after you've provided your setup information.

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
