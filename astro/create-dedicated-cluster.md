---
sidebar_label: 'Create a dedicated Astro cluster'
title: 'Create a dedicated cluster'
id: 'create-dedicated-cluster'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

A _dedicated cluster_ exclusively runs Deployments from your Organization within a single-tenant environment on Astronomer's cloud. Dedicated clusters provide more configuration options for regions, connectivity, and security than standard clusters. You might want to create a dedicated cluster if:

- You need to connect Astronomer's cloud to an external cloud using VPC peering. Standard clusters are compatible with all other supported connection types.
- You want more options for the region your cluster is hosted in. 
- You otherwise want to keep your Deployments as isolated as possible. 

Dedicated clusters offer the self-service convenience of a fully managed service while respecting the need to keep data private, secure, and within a single-tenant environment. If you don't need the aforementioned features, you can use one of the standard clusters when you [Create a Deployment](create-deployment.md).

## Setup

<Tabs
    defaultValue="aws"
    groupId= "create-a-cluster"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
        {label: 'Azure', value: 'azure'},
    ]}>

<TabItem value="aws">

1. In the Cloud UI, click the name of of your Workspace in the upper left corner, then click **Organization Settings**.
   
2. Click **Cluster** > **+ Cluster**.
  
3. Configure the following details about your cluster:

    - **Cloud Provider**: Select **AWS**.
    - **Name**: The name for your cluster.
    - **Region**: Select the region that you want your cluster to run in.
    - **VPC Subnet Range**: Provide a subnet range for Astro to connect to your existing AWS resources through VPC peering. The default is `172.20.0.0/20`.
  
4. Click **Create cluster**. After Astro finishes creating the cluster, users in your Organization can select the cluster when they [create a Deployment](create-deployment.md). 
   
</TabItem>

<TabItem value="gcp">

1. In the Cloud UI, click the name of of your Workspace in the upper left corner, then click **Organization Settings**.
   
2. Click **Cluster** > **+ Cluster**.
   
3. Configure the following details about your cluster:

    - **Cloud Provider**: Select **GCP**.
    - **Name**: The name for your cluster.
    - **Region**: Select the region that your cluster runs in.
    - **Subnet CIDR**: Specify the range used by nodes in your GKE cluster (Default: `172.20.0.0/22`).
    - **Pod CIDR**: Specify the range used by GKE Pods (Default: `172.21.0.0/19`).
    - **Service Address CIDR**: Specify the range used by GKE services (Default: `172.22.0.0/22`).
    - **Service VPC Peering**: Specify the range used by Private Service connections (Default: `172.23.0.0/20`).
   
4. Click **Create cluster**. After Astro finishes creating the cluster, users in your Organization can select the cluster when they [create a Deployment](create-deployment.md). 

</TabItem>

<TabItem value="azure">

1. In the Cloud UI, click the name of of your Workspace in the upper left corner, then click **Organization Settings**.
   
2. Click **Cluster** > **+ Cluster**.
   
3. Configure the following details about your cluster:

    - **Cloud Provider**: Select **Azure**.
    - **Name**: The name for your cluster.
    - **Region**: Select the region that you want your cluster to run in.
    - **VPC Subnet Range**: Provide a subnet range for Astro to connect to your existing AWS resources through VPC peering. The default is `172.20.0.0/19`.
  
4. Click **Create cluster**. After Astro finishes creating the cluster, users in your Organization can select the cluster when they [create a Deployment](create-deployment.md). 

</TabItem>

</Tabs>