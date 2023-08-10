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

To allow your Astro cluster to connect to your external data sources, you can either rely on public network or communicate using a private network. If you want to use a private network, there are multiple options to choose from. 

Use the following topics to learn about configuring various options available for connecting to your existing resources from Astro.

## Connection options

The option that you choose is determined by the security requirements of your company and your existing infrastructure.

<Tabs
    defaultValue="Public endpoints"
    groupId="connection-options"
    values={[
        {label: 'Public endpoints', value: 'Public endpoints'},
        {label: 'VPC peering', value: 'VPC peering'},
        {label: 'Private Service Connect', value: 'Private Service Connect'},
    ]}>
<TabItem value="Public endpoints">

Publicly accessible endpoints allow you to quickly connect your Astro Deployments to GCP. In certain cases, you might need to whitelist your Astro cluster or Deployment to facilitate communication with your external GCP resources. You can choose to whitelist either your Astro cluster or just your Deployment by retrieveing the external IPs from your Cloud UI.

### Retrieve IP addresses for a cluster to whitelist

1. In the Cloud UI, click the Astronomer logo in the top left corner to open your Organization.
2. Click **Clusters**, then select a cluster.
3. In the **Details** page, copy the IP addresses listed under **External IPs**.

A cluster's IP addresses are the same for all the Deployments running in that cluster. This is a one-time setup for each Astro cluster.

### Retrieve external IP addresses for a Deployment to whitelist

To allow to access to your external resource on per Deployment basis or if you are using a standard cluster, you need the external IPs of your Deployment.

1. In the Cloud UI, select a Deployment, then click **Details**.
2. Copy the IP addresses under **External IPs**.
3. (Optional) Add the IP addresses to the allowlist of any external services that need to interact with Astro.

When you use publicly accessible endpoints to connect to GCP, traffic moves directly between your Astro cluster and the GCP API endpoint. Data in this traffic never reaches the Astronomer managed control plane.

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

## See Also

- [Manage Airflow connections and variables](manage-connections-variables.md)
- [Authorize your Deployment using workload identity](authorize-using-workload-identity.md#gcp)