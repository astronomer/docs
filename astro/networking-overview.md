---
title: 'Create network connections between Astro and external resources'
sidebar_label: 'Overview'
id: networking-overview
description: Learn about the fundamentals of creating network connections from Astro.
---

To maximize the power of Apache Airflow®, your DAGs need to be able access data and services that exist outside of Astro. A _network connection_ is the basic requirement for accessing external resources from Astro. After you create a network connection, you can configure an Airflow connection to access specific resources that are available through the connection.

Network connections can be either public or private, and each type of connection has a different implementation for security and authorization.

In a public connection, data travels over the public internet to publicly accessible IP addresses on either side of the connection. For example, consider a Deployment that accesses an S3 bucket using an AWS connection with a configured AWS access key and secret. Because the only limitation for accessing the S3 bucket is API authentication, this is an example of a public connection.

In a private connection, data travels over a private network through private IP addresses. Private connections have significantly more security requirements and are recommended whenever you're accessing sensitive or private data.

:::info

Astronomer can support alternative networking solutions that are not covered in documentation. If you have specific networking requirements that aren't covered in documentation, or you need help to create a custom network connection, reach out to [Astronomer support](https://cloud.astronomer.io/open-support-request).

:::

## Network connection recommendations

If you're just starting out on Astro and you're working with publicly available services and testing data, you only need a public connection. For example, if you're accessing a publicly available API, you only need to configure an [HTTP Airflow connection](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/connections/http.html) to establish a connection between your Deployment and the API.

To access or write data on your company's cloud, Astronomer strongly recommends establishing a private network connection between Astro and your cloud. For most use cases, Astronomer recommends creating a VPC peering connection between Astro and your cloud. After the connection is established, you can authorize individual Deployments to specific resources using workload identity. This method is simple to set up and ensures private and secure connectivity between Astro and any support cloud provider.

To create a VPC peering connection to Astro, you must use a dedicated cluster. In general, dedicated clusters support more secure networking types, such as AWS PrivateLink and Azure VNet peering. See:

- [AWS: Create a private connection between Astro and AWS](connect-aws.md?tab=VPC%20peering#create-a-private-connection-between-astro-and-aws)
- [GCP: Create a private connection between Astro and GCP](connect-gcp.md?tab=VPC%20peering#create-a-private-connection-between-astro-and-gcp)
- [Azure: Create a private connection between Astro and Azure](connect-azure.md?tab=VNet%20peering#create-a-private-connection-between-astro-and-azure)

After you create your VPC peering connection, follow the steps in [Authorize your Deployment to cloud resources](authorize-deployments-to-your-cloud.md) for each Deployment that needs access to your cloud.

:::info

Astronomer monitors the health of Deployments and DAGs, but it doesn't monitor the status of network connections because they exist outside of Astronomer's observable control plane and data plane.

:::