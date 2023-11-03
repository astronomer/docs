---
sidebar_label: 'Azure'
title: 'Connect Astro to Azure data sources'
id: connect-azure
description: Connect Astro to Microsoft Azure.
sidebar_custom_props: { icon: 'img/azure.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Use this document to learn how you can grant an Astro cluster and its Deployments access to your external Azure resources.

## Connection options

Publicly accessible endpoints allow you to quickly connect your Astro clusters or Deployments to Azure through an Airflow connection. If your cloud restricts IP addresses, you can add the external IPs of your Deployment or cluster to an Azure resource's allowlist. 

If you have stricter security requirements, you can [create a private connection](#create-a-private-connection-between-astro-and-azure) to Azure in a few different ways.

After you crate a connection from your Deployment to Azure, you might also have to individually authorize Deployments to access specific resources. See [Authorize your Deployment using workload identity](authorize-deployments-to-your-cloud.md#azure).

### Access a public Azure endpoint

To facilitate communication between your Astro cluster or Deployment and your cloud, you can allowlist the external IPs for your cluster or Deployment on your cloud. If you have no other security restrictions, this means that any Deployment or cluster with an allowlisted external IP address can access your Azure resources through a valid Airflow connection.

#### Allowlist external IP addresses for a cluster

1. In the Cloud UI, click your Workspace name in the upper left corner, click **Organization Settings**, then click **Clusters**.
2. Select a cluster.
3. In the **Details** page, copy the IP addresses listed under **External IPs**.

A cluster's IP addresses are the same for all the Deployments running in that cluster. This is a one-time setup for each Astro cluster.

#### Allowlist external IP addresses for a Deployment

To allow to access to your external resource on per Deployment basis or if you are using a standard cluster, you need the external IPs of your Deployment.

1. In the Cloud UI, select a Deployment, then click **Details**.
2. Copy the IP addresses under **External IPs**.
3. (Optional) Add the IP addresses to the allowlist of any external services that need to interact with Astro.

When you use publicly accessible endpoints to connect to Azure, traffic moves directly between your Astro cluster and the Azure API endpoint. Data in this traffic never reaches the Astronomer managed control plane.

### Create a private connection between Astro and Azure

The option that you choose is determined by the security requirements of your company and your existing infrastructure.

<Tabs
    defaultValue="VNet peering"
    groupId="connection-options"
    values={[
        {label: 'VNet peering', value: 'VNet peering'},
        {label: 'Azure Private Link', value: 'Azure Private Link'},
    ]}>

<TabItem value="VNet peering">

:::info 

This connection option is only available for dedicated Astro Hosted clusters and Astro Hybrid.

:::

To set up a private connection between an Astro Virtual Network (VNet) and an Azure VNet, you can create a VNet peering connection. VNet peering ensures private and secure connectivity, reduces network transit costs, and simplifies network layouts.

To create a VNet peering connection between an Astro VNet and an Azure VNet, contact [Astronomer support](https://cloud.astronomer.io/support) and provide the following information:

- Astro cluster ID and name
- Azure TenantID and Subscription ID of the target VNet
- Region of the target VNet
- VNet ID of the target VNet
- Classless Inter-Domain Routing (CIDR) block of the target VNet

After receiving your request, Astronomer support initiates a peering request and creates the routing table entries in the Astro VNet. To allow multidirectional traffic between Airflow and your organization's data sources, the owner of the target VNet needs to accept the peering request and create the routing table entries in the target VNet.

</TabItem>

<TabItem value="Azure Private Link">

:::info 

This connection option is only available for dedicated Astro Hosted clusters and Astro Hybrid.

:::

Use Azure Private Link to create private connections from Astro to your Azure services without exposing your data to the public internet.

Astro clusters are pre-configured with the Azure blob private endpoint.

To request additional endpoints, or assistance connecting to other Azure services, provide [Astronomer support](https://cloud.astronomer.io/support) with the following information for the resource you want to connect to using Private Link:

- Resource name
- Resource ID
- Private endpoint

For example, to connect with Azure Container Registry:

1. Follow the [Azure documentation](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal?tabs=azure-cli) to create the [container registry](https://portal.azure.com/#create/Microsoft.ContainerRegistry). Copy the name of container registry.
2. Follow the [Azure documentation](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-private-link#create-a-private-endpoint---new-registry) to create a private endpoint for your container registry. Then, copy the name of the **Data endpoint**.
3. Then, from the left panel, go to **Overview** menu, and click on JSON view in **Essentials**, to copy the resource ID. You can also run Azure CLI command `az acr show -n myRegistry` to get the resource ID.
4. Contact [Astronomer Support](https://cloud.astronomer.io/support) with your request to connect. Provide the resource name, data endpoint name, and resource ID.
5. When Astronomer support adds an Azure private endpoint, corresponding private DNS zone and Canonical Name (CNAME) records are created to allow you to address the service by its private link name. Astronomer support will send the connection request in Azure Portal's [Private Link Center](https://portal.azure.com/#view/Microsoft_Azure_Network/PrivateLinkCenterBlade/~/pendingconnections). 
6. Approve the connection requests from your Azure portal, then confirm that you've completed this in your support ticket. Astronomer support will then test whether the DNS resolves the endpoint correctly.

After Astronomer configures the connection, you can create Airflow connections to your resource. In some circumstances, you might need to modify your DAGs to address the service by its private link name (For example, `StorageAccountA.privatelink.blob.core.windows.net` instead of `StorageAccountA.blob.core.windows.net`).

Note that you'll incur additional Azure infrastructure costs for every Azure private endpoint that you use. See [Azure Private Link pricing](https://azure.microsoft.com/en-us/pricing/details/private-link/).

</TabItem>

</Tabs>

## See Also

- [Manage Airflow connections and variables](manage-connections-variables.md)