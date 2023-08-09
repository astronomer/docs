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


Astro allows you to connect your Astro cluster to your external Azure resources using the external IPs of your Astro cluster. These external IPs are static and different for each Astro cluster. These need to be added to be whitelisted in your cloud account to allow access to your resources. 

A cluster's IP addresses are the same for all Deployments running in that cluster. This is a one-time setup for each Astro cluster. 

Use the following topics to learn aboud different available options to connect to your existing resources from Astro and how to configure them.

## Prerequisites

- External IP address of your Astro cluster
- Permissions to access to your Azure cloud portal 

## Retrieve external IP addresses for a cluster

1. In the Cloud UI, click the Astronomer logo in the top left corner to open your Organization.
2. Click **Clusters**, then select a cluster.
3. In the **Details** page, copy the IP addresses listed under **External IPs**.

## Connection options

The connection option that you choose is determined by the requirements of your organization and your existing infrastructure. You can choose a straightforward implementation, or a more complex implementation that provides enhanced data security. Astronomer recommends that you review all of the available connection options before selecting one for your organization.

<Tabs
    defaultValue="Public endpoints"
    groupId="connection-options"
    values={[
        {label: 'Public endpoints', value: 'Public endpoints'},
        {label: 'VNet peering', value: 'VNet peering'},
        {label: 'Azure Private Link', value: 'Azure Private Link'},
    ]}>
<TabItem value="Public endpoints">

Publicly accessible endpoints allow you to quickly connect Deployments in Astro to AWS using Airflow connections. This does not required any special configuration on Astro or AWS side. See [Manage connections and variables](manage-connections-variables.md) to learn about various strategies to create Airflow connections.

When you use publicly accessible endpoints to connect to AWS, traffic moves directly between your Astro cluster and the AWS API endpoint. Data in this traffic never reaches the control plane, which is managed by Astronomer.

</TabItem>

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

