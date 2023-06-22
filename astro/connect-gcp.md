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

Use the information provided here to learn how you can securely connect Astro to your existing Google Cloud Platform (GCP) instance. A connection to GCP allows Astro to access data stored on your GCP instance and is a necessary step to running pipelines in a production environment.

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

Publicly accessible endpoints allow you to quickly connect Astro to GCP. To configure these endpoints, you can use one of the following methods:

- Set environment variables on Astro with your endpoint information. See [Set environment variables on Astro](environment-variables.md).
- Create an Airflow connection with your endpoint information. See [Managing Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

When you use publicly accessible endpoints to connect Astro and GCP, traffic moves directly between your Astro clusters and the GCP API endpoint. Data in this traffic never reaches the control plane, which is managed by Astronomer.

</TabItem>

<TabItem value="VPC peering">

:::info 

This connection option is only available for dedicated Astro Hosted clusters.

:::

VPC peering ensures private and secure connectivity, reduces network transit costs, and simplifies network layouts.

To create a VPC peering connection between an Astro VPC and a GCP VPC: 
 
1. Contact [Astronomer support](https://cloud.astronomer.io/support) and provide the following information:

    - Astro cluster ID and name.
    - Google Cloud project ID of the target VPC.
    - VPC NAME of the target VPC.
    - Classless Inter-Domain Routing (CIDR) block of the target VPC.

    After receiving your request, Astronomer support will create a VPC peering connection from your Astro VPC to your target VPC. The support team will then provide you with your Astro cluster GCP project ID and VPC name.
    
2. Using the information provided by Astronomer support, [create a peering connection request](https://cloud.google.com/vpc/docs/using-vpc-peering#creating_a_peering_configuration) from your target VPC to your Astro cluster VPC. For example, you can use the following gcloud CLI command to create the connection:

   ```sh
   gcloud compute networks peerings create <choose-any-name> --network=cloud-composer-vpc-network  --peer-project=<your-cluster-project-id> --peer-network=<your-cluster-vpc-name>
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

## Authorization options

Authorization is the process of verifying a user or service's permissions before allowing them access to organizational applications and resources. Astro clusters must be authorized to access external resources from your cloud. Which authorization option that you choose is determined by the requirements of your organization and your existing infrastructure. Astronomer recommends that you review all of the available authorization options before selecting one for your organization.

<Tabs
    defaultValue="Workload Identity"
    groupId="authentication-options"
    values={[
        {label: 'Workload Identity', value: 'Workload Identity'},
        {label: 'Service account keys', value: 'Service account keys'},
    ]}>
<TabItem value="Workload Identity">

To allow data pipelines running on GCP to access Google Cloud services in a secure and manageable way, Google recommends using [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity). All Astro clusters on GCP have Workload Identity enabled by default. Each Astro Deployment is associated with a Google service account that's created by Astronomer and is bound to an identity from your Google Cloud project's fixed workload identity pool.

To grant a Deployment on Astro access to external data services on GCP, such as BigQuery:

1. In the Cloud UI, select your Deployment, then click **Details**

2. Copy the service account shown under **Workload Identity**.

3. Grant the Google service account for your Astro Deployment an IAM role that has access to your external data service. With the Google Cloud CLI, run:

    ```text
    gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:<your-astro-service-account> --role=roles/viewer
    ```

    For instructions on how to grant your service account an IAM role in the Google Cloud console, see [Grant an IAM role](https://cloud.google.com/iam/docs/grant-role-console#grant_an_iam_role).

4. Optional. Repeat these steps for every Astro Deployment that requires access to external data services on GCP.

</TabItem>

<TabItem value="Service account keys">

When you create a connection from Astro to GCP, you can specify the service account key in JSON format, or you can create a secret to hold the service account key. For more information about creating and managing GCP service account keys, see [Create and manage service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and [Creating and accessing secrets](https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets).

Astronomer recommends using Google Cloud Secret Manager to store your GCP service account keys and other secrets. See [Google Cloud Secret Manager](secrets-backend?tab=gcp#setup).

</TabItem>

</Tabs>
