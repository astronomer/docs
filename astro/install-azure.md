---
sidebar_label: "Install from the Azure Marketplace"
title: "Install Astro as an Azure Native ISV service"
id: install-azure
---

[Astro](https://docs.astronomer.io/astro) is a managed service for data orchestration that is built for the cloud and powered by Apache Airflow. Your Airflow infrastructure is managed entirely by Astronomer, enabling you to shift your focus from infrastructure to data.

If your company uses Azure or already manages applications using Azure Native ISV Services, Astronomer recommends installing and accessing Astro through the Azure Marketplace. After you install Astro as an Azure Native ISV Service, you can manage resource usage and billing alongside your existing Azure applications. The installation template hosted in the Azure Marketplace guides you to configure all of the essential resources you need to quickly start running your DAGs in Airflow.

## Step 1: Set up Astro on Azure

To run and manage Astro from Azure, you need to create an Astro Azure resource. The resource lets you control your Astro spend directly from Azure. It also contains the configuration for your first Organization and Workspace.

An _Organization_ is the highest management level on Astro. An Organization contains _Workspaces_, which are collections of _Deployments_, or Airflow environments, that are typically owned by a single team. You can manage user roles and permissions both at the Organization and Workspace levels.

1. In the search bar for Azure Portal, search `astro` or `airflow`. Then, select **Apache Airflow™ on Astro - An Azure Native ISV Service.**
    
    ![Azure](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/fcb4122e-35a5-47ad-94a1-e143d4916ef9/Screenshot_2023-08-24_at_9.51.54_AM.png)
        
2. Click **Create**.
    
    ![Screenshot 2023-08-24 at 9.52.32 AM.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/731a6de7-8a8e-41e6-aaaf-19d38d8edd45/Screenshot_2023-08-24_at_9.52.32_AM.png)
    
3. In the **Basics** tab for your resource, configure the following details:
    - **Subscription** Select the subscription you provided to Astronomer.
    - **Resource group** Either create or select a resource group. Astronomer recommends creating a new resource group for Astro.
    - **Resource name** Enter a name for the Astro resource, such as `astro-airflow`.
    - **Region:** Select a region to host a placeholder Astro Azure resource. This should always be `EASTUS`. Note that this region has no effect on your Astro Hosted Airflow environments. You can still create Airflow environments in any supported Azure region.
    - **Astro Organization name:** Enter a name for your Astro Organization. Astronomer recommends using the name of your company or organization.
    - **Workspace name** Enter the name for the Workspace where you will manage and run Deployments.
4. (Optional) Click **Next: Tabs.** Add an Azure tag to the Astro resource to track your resource usage. 
5. Click **Review + create**,  then click **Create**.
6. Wait for the resource to be created. Currently, this process takes about 2 minutes.

## Step 2: Access Astro and get started

1. After the resource is created, click **Go to resource**. On the **Overview** page, copy the **SSO Url**. It should look similar to the following:
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cdc90429-fe4e-4183-a516-bdbc148dfc59/Untitled.png)
    
    Share this URL with anyone at your company who needs to access your newly created Organization. Any users that access Astro with this URL will automatically be added to your Organization as an Organization Member. You can add them to your Workspace from Astro’s Cloud UI so they can start deploying code and running DAGs. See [Manage users in your Astro Workspace](https://docs.astronomer.io/astro/manage-workspace-users).
    
    <aside>
    💡 If a user belongs to the same Azure organization where your created your Astro resource, they can log in without using the SSO URL by entering their email at `cloud.astronomer.io`. Astro will automatically identify their email address as belonging to your organization and log them into Astro as an Organization Member.
    
    </aside>
    
2. Click **Go to Astro**. You will be redirected and logged in to the Cloud UI, which is Astro’s primary interface for managing your Airflow environments. 
3. Follow the [Astro quickstart](https://docs.astronomer.io/astro/first-dag-cli) to run your first DAG on Astro.