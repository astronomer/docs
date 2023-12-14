---
title: "Create an Azure Blob Storage connection in Airflow"
id: azure-blob-storage
sidebar_label: "Azure Blob Storage"
description: Learn how to create an Azure Blob Storage connection in Airflow.
sidebar_custom_props: { icon: 'img/integrations/azure-blob-storage.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

An [Azure Workload Identity](https://learn.microsoft.com/en-us/entra/workload-id/workload-identities-overview) is an identity you assign to a software workload (such as an application, service, script, or container) to authenticate and access other services and resources. This identity acts as an Azure user, and can be granted access to multiple Azure services through one connection, which is particularly advantageous for users who need to access different Azure services in a single workflow. It also eliminates the need to create multiple connections for different services, allowing all Azure services to utilize the new generic **Azure** connection type. 

This guide explains how to set up an Azure Workload Identity connection using the **Azure** connection type. Astronomer recommends using this connection type because it utilizes the new Entra ID Workload identities system, which means you can connect with any Azure service using a single connection.

## Prerequisites

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- A locally running [Astro project](https://docs.astronomer.io/astro/cli/get-started-cli).
- An Azure Entra ID Managed Identity that you want your Astro workloads in this deployment to run as. For information on how to create one, please refer to the [Azure documentation](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp)

## Get connection details

In order to create a workload identity for your deployment that leverages your Entra ID managed identity, you'll need to execute an Azure CLI command. To simplify this process, we have created a command generator 












