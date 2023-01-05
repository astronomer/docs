---
sidebar_label: 'GCP'
title: 'Connect Astro to GCP data sources'
id: connect-gcp
description: Connect your Astro data plane to GCP.
sidebar_custom_props: { icon: 'img/gcp.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Use the information provided here to learn how you can securely connect your Astro data plane to your existing Google Cloud Platform (GCP) instance. A connection to GCP allows Astro to access data stored on your GCP instance and is a necessary step to running pipelines in a production environment.

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

When you use publicly accessible endpoints to connect Astro and GCP, traffic moves directly between your Astro data plane and the GCP API endpoint. Data in this traffic never reaches the control plane, which is managed by Astronomer.

</TabItem>

<TabItem value="VPC peering">

Every Astro cluster runs in a dedicated Virtual Private Cloud (VPC). To set up a private connection between an Astro VPC and a GCP VPC, you can create a VPC peering connection. VPC peering ensures private and secure connectivity, reduces network transit costs, and simplifies network layouts.

To create a VPC peering connection between an Astro VPC and a GCP VPC, contact [Astronomer support](https://cloud.astronomer.io/support) and provide the following information:

- Astro cluster ID and name
- Google Cloud project ID of the target VPC
- VPC ID of the target VPC
- Classless Inter-Domain Routing (CIDR) block of the target VPC

After receiving your request, Astronomer support initiates a peering request and creates the routing table entries in the Astro VPC. To allow multidirectional traffic between Airflow and your organization's data sources, the owner of the target VPC needs to accept the peering request and create the routing table entries in the target VPC.

</TabItem>

<TabItem value="Private Service Connect">

Private Service Connect allows Astro to access GCP data that belongs to different groups, teams, projects, and organizations. To learn more about Private Service Connect, see [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect).

All Astro data planes on GCP are configured with a private services connection that accepts all Google APIs. All connections to Google services use the `googleapis.com` domain to ensure the privacy and security of communications within the Google network. A list of Google services and their associated service names are provided in the [Google APIs Explorer Directory](https://developers.google.com/apis-explorer). Alternatively, you can run the following command in the Google Cloud CLI to return a list of Google services and their associated service names:

```sh
gcloud services list --available --filter="name:googleapis.com"
```
You can use the default GCP DNS name in your DAGS to simplify the implementation of GCP private services connections. Astronomer has implemented a default GCP DNS zone and resource record that routes the default GCP DNS name through the private services connection.

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

1. In the Cloud UI, select a Workspace, select a Deployment, and then copy the value in the **Namespace** field.

2. Use the Deployment namespace value and the name of your Google Cloud project to identify the Google service account for your Deployment.

    Google service accounts for Astro Deployments are formatted as follows:

    ```text
    astro-<deployment-namespace>@<gcp-account-id>.iam.gserviceaccount.com
    ```
    
    To locate your Google Cloud account ID, in the Cloud UI click **Clusters**. The Google Cloud account ID is located in the **Account ID** column.

    For example, for a Google Cloud project named `astronomer-prod` and a Deployment namespace defined as `nuclear-science-2730`, the service account for the Deployment would be:

    ```text
    astro-nuclear-science-2730@astronomer-prod.iam.gserviceaccount.com
    ```
  :::info

  GCP has a 30-character limit for service account names. For Deployment namespaces which are longer than 24 characters, use only the first 24 characters when determining your service account name.

  For example, if your Google Cloud project is named `astronomer-prod` and your Deployment namespace is `nuclear-scintillation-2730`, the service account name is:

  ```text
  astro-nuclear-scintillation-27@astronomer-prod.iam.gserviceaccount.com

3. Grant the Google service account for your Astro Deployment an IAM role that has access to your external data service. With the Google Cloud CLI, run:

    ```text
    gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:astro-<deployment-namespace>@<gcp-project-name>.iam.gserviceaccount.com --role=roles/viewer
    ```

    For instructions on how to grant your service account an IAM role in the Google Cloud console, see [Grant an IAM role](https://cloud.google.com/iam/docs/grant-role-console#grant_an_iam_role).

4. Optional. Repeat these steps for every Astro Deployment that requires access to external data services on GCP.

</TabItem>

<TabItem value="Service account keys">

When you create a connection from Astro to GCP, you can specify the service account key in JSON format, or you can create a secret to hold the service account key. For more information about creating and managing GCP service account keys, see [Create and manage service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and [Creating and accessing secrets](https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets).

Astronomer recommends using Google Cloud Secret Manager to store your GCP service account keys and other secrets. See [Google Cloud Secret Manager](secrets-backend.md#setup).

</TabItem>

</Tabs>
