---
sidebar_label: 'GCP'
title: 'Connect Astro to GCP data sources'
id: connect-gcp
description: Connect Astro to GCP.
sidebar_custom_props: { icon: 'img/gcp.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Astro allows you to connect your Astro cluster to your external GCP resources using the external IPs of your Astro cluster. These external IPs are static and different for each Astro cluster. These need to be added to be whitelisted in your cloud account to allow access to your resources. 

A cluster's IP addresses are the same for all Deployments running in that cluster. This is a one-time setup for each Astro cluster. 

Use the following topics to learn aboud different available options to connect to your existing resources from Astro and how to configure them.

## Prerequisites

- External IP address of your Astro cluster
- Permissions to access to your GCP cloud console

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
        {label: 'VPC peering', value: 'VPC peering'},
        {label: 'Private Service Connect', value: 'Private Service Connect'},
    ]}>
<TabItem value="Public endpoints">

Publicly accessible endpoints allow you to quickly connect Deployments in Astro to AWS using Airflow connections. This does not required any special configuration on Astro or AWS side. See [Manage connections and variables](manage-connections-variables.md) to learn about various strategies to create Airflow connections.

When you use publicly accessible endpoints to connect to AWS, traffic moves directly between your Astro cluster and the AWS API endpoint. Data in this traffic never reaches the control plane, which is managed by Astronomer.

</TabItem>

<TabItem value="VPC peering">

:::info 

This connection option is available only for dedicated Astro Hosted clusters and Astro Hybrid.

:::

VPC peering ensures private and secure connectivity, reduces network transit costs, and simplifies network layouts.

To create a VPC peering connection between an Astro VPC and a GCP VPC: 
 
1. Contact [Astronomer support](https://cloud.astronomer.io/support) and provide the following information:

    - Astro cluster ID and name.
    - Google Cloud project ID of the target VPC.
    - VPC NAME of the target VPC.
    - Classless Inter-Domain Routing (CIDR) block of the target VPC.

    After receiving your request, Astronomer support will create a VPC peering connection from your Astro VPC to your target VPC. The support team will then provide you with your Astro cluster GCP project ID and VPC name.
    
2. Using the information provided by Astronomer support, [create a peering connection](https://cloud.google.com/vpc/docs/using-vpc-peering#creating_a_peering_configuration) from your target VPC to your Astro cluster VPC. For example, you can use the following gcloud CLI command to create the connection:

   ```sh
   gcloud compute networks peerings create <choose-any-name> --network=<your-target-vpc-network-name>  --peer-project=<your-cluster-project-id> --peer-network=<your-cluster-vpc-name>
   ```

After both VPC peering connections have been created, the connection becomes active.

</TabItem>

<TabItem value="Private Service Connect">

Use Private Service Connect (PSC) to create private connections from Astro to GCP services without connecting over the public internet. See [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) to learn more.

Astro clusters are by default configured with a PSC endpoint with a target of [All Google APIs](https://cloud.google.com/vpc/docs/configure-private-service-connect-apis#supported-apis). To provide a secure-by-default configuration, a DNS zone is created with a resource record that will route all requests made to `*.googleapis.com` through this PSC endpoint. This ensures that requests made to these services are made over PSC without any additional user configuration. As an example, requests to `storage.googleapis.com` will be routed through this PSC endpoint.

A list of Google services and their associated service names are provided in the [Google APIs Explorer Directory](https://developers.google.com/apis-explorer). Alternatively, you can run the following command in the Google Cloud CLI to return a list of Google services and their associated service names:

```sh
gcloud services list --available --filter="name:googleapis.com"
```

</TabItem>

</Tabs>
