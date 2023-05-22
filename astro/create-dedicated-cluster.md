---
sidebar_label: 'Create a dedicated Astro cluster'
title: 'Create a dedicated cluster'
id: 'create-dedicated-cluster'
---

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
   
1. In the Cloud UI, open your Organization page by clicking the Astronomer logo in the upper left corner.
   
2. Click **Cluster** > **+ Cluster**.
   
3. Configure the following details about your cluster:

    - **Name**: The name for your cluster.
    - **Region**: Select the region that you want your cluster to run in.
    - **VPC Subnet Range**: Provide a subnet range for Astro to connect to your existing AWS resources through VPC peering. The default is `172.20.0.0/20`.
   
4. Click **Create cluster**. 
   
</TabItem>
<TabItem value="gcp">

1. In the Cloud UI, open your Organization page by clicking the Astronomer logo in the upper left corner.
   
2. Click **Cluster** > **+ Cluster**.
   
3. Configure the following details about your cluster:

    - **Name**: The name for your cluster.
    - **Region**: Select the region that your cluster runs in   
    - **VPC Subnet Range**: Provide a subnet range for Astro to connect to your existing GKE resources through VPC peering. The default is `172.20.0.0/22`.
    - **Pod Subnet Range**: Provide a subnet range for Astro to connect to nodes in your GKE cluster. The default is `172.21.0.0/19`.
    - **Service Subnet Range**: Provide a subnet range for Astro to connect to GKE services. The default is `172.22.0.0/22`.
    - **Service Peering Range**: Provide a subnet range for Astro to connect to GKE services through VPC peering. The default is `172.23.0.0/20`.
   
4. Click **Create cluster**.
   
5. Wait for Astronomer to finish creating the cluster.

    The cluster is created with a default set of resources that are suitable for most use cases. See [GCP cluster settings](resource-reference-gcp.md#default-cluster-values) for a list of all default resources.

</TabItem>
<TabItem value="azure">

You cannot currently create dedicated Azure clusters from the Cloud UI. To create a dedicated Azure cluster, contact [Astronomer support](cloud.astronomer.io/support).

</TabItem>
</Tabs>