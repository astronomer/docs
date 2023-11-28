---
sidebar_label: "Install from Azure Marketplace"
title: "Install Astro from the Azure Marketplace as an Azure Native ISV service"
description: "Learn how to install Astro from the Azure marketplace, which is recommended for all Azure-based teams."
id: install-azure
---

[Astro](https://docs.astronomer.io/astro) is a managed service for data orchestration that is built for the cloud and powered by Apache Airflow. Your Airflow infrastructure is managed entirely by Astronomer, enabling you to shift your focus from infrastructure to data.

If your company uses Azure or already manages applications using [Azure Native ISV Services](https://learn.microsoft.com/en-us/azure/partner-solutions/partners), Astronomer recommends installing and accessing Astro through the Azure Marketplace. When you install Astro as an Azure Native ISV Service, you can manage resource usage and billing alongside your existing Azure applications. Additionally, the Azure Native ISV Service is already integrated with Microsoft Entra ID, so you can add users from your team to Astro without any additional single sign-on (SSO) configuration.

The installation template hosted in the Azure Marketplace guides you to configure all of the essential resources you need to start running your DAGs in Airflow.

:::info 

If you want to try Astro using a personal email address, follow the steps in [Install Astro from the Azure Marketplace using a personal email](#install-astro-from-the-azure-marketplace-using-a-personal-email) before completing this setup.

:::

## Step 1: Create an Azure resource for Astro

To run and manage Astro from Azure, you need to create an Astro Azure resource. The resource lets you control your Astro spend directly from Azure. It also contains the configuration for your first Organization and Workspace.

An _Organization_ is the highest management level on Astro. An Organization contains _Workspaces_, which are collections of _Deployments_, or Airflow environments, that are typically owned by a single team. You can manage user roles and permissions both at the Organization and Workspace levels.

1. In the search bar for Azure Portal, search `astro` or `airflow`. Then, select **Apache Airflow™ on Astro - An Azure Native ISV Service.**
    
    ![The Azure marketplace search bar. The text 'astro' is entered and the search bar returns the Astro Azure Native ISC Service as a result.](/img/docs/azure-search.png)
    
2. Click **Create**.
    
    ![The create button in the Azure resource configuration page is highlighted](/img/docs/azure-create.png)
    
3. In the **Basics** tab for your resource, configure the following details:
   
    - **Subscription:** Select the subscription you provided to Astronomer.
    - **Resource group:** Either create or select a resource group. Astronomer recommends creating a new resource group for Astro.
    - **Resource name:** Enter a name for the Astro resource, such as `astro-airflow`.
    - **Region:** Select a region to host a placeholder Astro Azure resource. This should always be `EASTUS`. Note that this region has no effect on your Astro Hosted Airflow environments. You can still create Airflow environments in any supported Azure region.
    - **Astro Organization name:** Enter a name for your Astro Organization. Astronomer recommends using the name of your company or organization.
    - **Workspace name:** Enter the name for the Workspace where you will manage and run Deployments. Astronomer recommends using the name of your team or project.

4. (Optional) Click **Next: Tabs.** Add an Azure tag to the Astro resource to track your resource usage. 
5. Click **Review + create**, then click **Create.**
6. Wait for the resource to be created. Currently, this process takes about 2 minutes.

## Step 2: Access Astro and get started

1. After the resource is created, click **Go to resource**. On the **Overview** page, copy the **SSO Url**. It should look similar to the following:
    
    ![The Azure SSO URL and the 'copy to clipboard' button](/img/docs/azure-sso.png)
    
    Share this URL with anyone at your company who needs to access your newly created Organization. Any users that access Astro with this URL will automatically be added to your Organization as an Organization Member. You can add them to your Workspace from Astro’s Cloud UI so they can start deploying code and running DAGs. See [Manage users in your Astro Workspace](https://docs.astronomer.io/astro/manage-workspace-users).

    :::info 

    Microsoft Entra ID is automatically configured only for the email domain you used to create your Astro Organization. If you need to invite users with emails from other domains to Astro, contact [Astronomer support](https://cloud.astronomer.io/open-support-request) and provide your Organization ID and the email domain you want to manage through Microsoft Entra ID.

    :::
    
    :::tip
    
    If a user belongs to the same Azure organization where your created your Astro resource, they can log in without using the SSO URL by entering their email at `cloud.astronomer.io`. Astro will automatically identify their email address as belonging to your organization and log them into Astro as an Organization Member.
    
    :::
    
2. Click **Go to Astro**. You will be redirected and logged in to the Cloud UI, which is Astro’s primary interface for managing your Airflow environments. 
3. Follow the [Astro quickstart](https://docs.astronomer.io/astro/first-dag-cli) to run your first DAG on Astro.

## Install Astro from the Azure Marketplace using a personal email

Because of the way managed domains work on Astro, you can't install Astro if you're logged into Azure with an email that uses a generic email domain, such as `outlook.com` or `gmail.com`.

If you don't have an email address with a unique domain, such as one provided to you by your company, complete the following setup before you attempt to install Astro. This allows you to log in to Azure using a domain that's generated by your Azure subscription.

1. If you haven't already done so, create an account on `portal.azure.com` using your personal email address.
2. In the Azure portal search bar, search for the **Subscriptions** service.
3. Click **Add**, then create a new Azure subscription.
4. In the Azure portal search bar, search for the **Users** service.
5. Click **New User** > **Create New User**.
6. In the **Basics** tab, fill out all required fields for your user. This is the account you can use to install Astro. Copy the full email address and password for the user.
7. In the **Properties** tab, enter the email address that you copied in the **Email** field.
8. Click **Review + Create**.
9. Go back to the **Subscriptions** service, open the subscription that you created, then click **Access Control (IAM)**.
10. Click **Add** > **Add role assignment**.
11. In the **Privileged administrator roles** tab, click **Owner**.
12. Open the **Members** tab, click **Select Members**. In the menu that appears, add the user account you created in Step 6 and click **Select**.
13. Log out of your personal account, then log in to the new user account that you created in Step 6. 
14. Proceed to [Step 1: Create an Azure resource for Astro](#step-1-create-an-azure-resource-for-astro).