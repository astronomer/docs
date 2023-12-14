3---
title: "Create an Azure Workload Identity connection in Airflow"
id: azure-workload-identity
sidebar_label: "Azure Workload Identity"
description: Learn how to create an Azure Workload Identity connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/azure.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

An [Azure Workload Identity](https://learn.microsoft.com/en-us/entra/workload-id/workload-identities-overview) is an identity you assign to a software workload (such as an application, service, script, or container) to authenticate and access other services and resources. This identity can be granted access to multiple Azure services by being assigned Azure resource groups, which is particularly advantageous for users who need to access different Azure services in a single workflow. This is because it eliminates the previous need to create different connections for different Azure services, instead allowing all Azure services to utilize the new generic **Azure** connection type. 

This guide explains how to set up an Azure Workload Identity connection using the **Azure** connection type. Astronomer recommends using this connection type because it utilizes the new Entra ID Workload identities system, which means you can connect with any Azure service using a single connection.

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- An Azure Entra ID Managed Identity that you want your Astro workloads in this deployment to run as. For information on how to create one, please refer to the [Azure documentation](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp)

## Get connection details

In order to create a workload identity for your deployment that leverages your Entra ID managed identity, you'll need to execute an Azure CLI command that links your Airflow deployment and managed identity. To simplify this process, we have created a command generator, located in a pop up menu under the details tab of your deployment screen. 

:::Note
If you plan to use the same workload identity for multiple deployments, you'll need to run this command for each individual deployment. However, all deployments will use the same credentials for their connection, allowing you to share the same connection to multiple deployments at the same time via the [Astro Connection Management System](https://www.astronomer.io/solutions/connection-management/). Currently because of limits Azure has set on the number of resources allowed to leverage the same Workload Identity, the same connection can be shared across 5 deployments last. 
:::


![details-screen](/img/examples/connection-azure-workload-identity-1.png)
![command_creation_popup](/img/examples/connection-azure-workload-identity-2.png)


The two credentials it requires, Managed Identity Name and Resource Group, are both available from the Managed Identity resource overview screen, as shown in the screenshot below: 

![identity-details-screen](/img/examples/connection-azure-workload-identity-3.png)

After you've entered those credentials into the pop up menu, copy the code block from under `Run in terminal:` and either open the Azure CLI directly from the web portal, or from a local terminal window that has the Azure CLI installed. Then, paste the code block and run it to create your Workload Identity. After the Workload Identity has been created and authenticated to the deployments Scheduler, Triggerer, and Worker, you'll be returned a json package that contains all the necessary details for adding the connection to Airflow. Specifically, you'll need to copy the `clientId` and `tenantId` fields. 

```json
{
  "clientId": "clientid",
  "id": "/subscriptions/**subscription-id**/resourcegroups/DemoGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/astrodemoid",
  "location": "eastus",
  "name": "astrodemoid",
  "principalId": "PrincipalID",
  "resourceGroup": "DemoGroup",
  "systemData": null,
  "tags": {},
  "tenantId": "TenantID",
  "type": "Microsoft.ManagedIdentity/userAssignedIdentities"
}

```

## Adding Connection via the Astro UI

To create your connection in Astro, open up the Environment tab and use the `+ connection` button to create a new connection. 

![create_connectionmenu](/img/examples/connection-azure-workload-identity-4.png)

Then, select the Azure workload identity option from the grid menu, where you'll be presented with the following screen to enter the `clientId` and `tenantId` fields from before. If you need to specify a `subscriptionId` for a specific service, you can open up the more options drop down menu to do so. 

![example_conn](/img/examples/connection-azure-workload-identity-5.png)

## Adding Connection via the Airflow UI

To create your connection in Airflow, open up the Connections menu and create a new connection, then select `Azure` as the connection type. Then, enter the `clientId` and `tenantId` fields from before. You can also specify a `subscriptionId` for a specific service if you need to do so. 











