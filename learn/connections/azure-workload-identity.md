---
title: "Create a Microsoft Entra Workload ID connection in Airflow"
id: entra-workload-id
sidebar_label: "Microsoft Entra Workload ID"
description: Learn how to create an Azure Workload Identity connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/azure.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

A [workload identity](https://learn.microsoft.com/en-us/entra/workload-id/workload-identities-overview) is an identity you can assign to your Airflow environment which is authorized to access external services and resources. On Azure, a single workload identity can be authorized to multiple Azure resources through Azure resource groups.

The new generic **Azure** connection type lets you assign a workload identity to your Airflow environment so that Airflow can access multiple Azure resources using a single Airflow connection. This configuration greatly simplifies the number of credentials and connections you need to manage for Azure workflows. 

This guide explains how to set up an Azure Workload Identity connection using the **Azure** connection type. Astronomer recommends using this connection type for most Azure workflows.

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- The [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/) or access to the Azure web portal.
- An [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- (Optional) An [Astro Deployment](https://docs.astronomer.io/astro/create-deployment).
- A Microsoft Entra [managed identity](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp).

:::info 
If you want to use Microsoft Entra Workload ID with a generic Apache Airflow project, your setup steps might vary. See [Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/connections/azure.html).
:::

## Get connection details

In order to create a workload identity for your deployment that leverages your Entra ID managed identity, you'll need to execute an Azure CLI command that links your Airflow deployment and managed identity.  The two required credentials to create this workload identity, Managed Identity Name and Resource Group, are both available from the Azure Managed Identity resource overview screen: 

![identity-details-screen](/img/examples/connection-azure-workload-identity-3.png)

If you're using Astro, follow the steps in [Authorize Deployments to Cloud resources](https://docs.astronomer.io/astro/authorize-deployments-to-your-cloud?tab=azure#setup) to create a workload identity for your Deployment.


## Create your connection

To create your connection in the Airflow UI:

1. In the Airflow UI, go to **Admin** > **Connections**.
2. Click **+** to add a new connection, then select **Azure** as the connection type.
3. Enter the `clientId` and `tenantId` fields you retrieved from [Get connection details](#get-connection-details) and enter them into the **Managed Identity Client ID** and **Workload Identity Tenant ID** fields respectively. You can also specify a **subscriptionId** for a specific service if required.
4. Click **Save**.

To create your connection in Astro, follow the steps to [create a new connection in the Astro Environment Manager](https://docs.astronomer.io/astro/create-and-link-connections). Select the **Azure workload identity** connection type and enter your **Client ID** and **Tenant ID**. If you need to specify a **Subscription ID** for a specific service, you can open up the **More options** dropdown menu and add it there.

![create_connectionmenu](/img/examples/connection-azure-workload-identity-4.png)
![example_conn](/img/examples/connection-azure-workload-identity-5.png)

