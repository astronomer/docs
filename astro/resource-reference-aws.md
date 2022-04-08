---
sidebar_label: "AWS Resource Reference"
title: "Resources Required for Astro on AWS"
id: resource-reference-aws
description: Reference of all supported configurations for new Clusters on Astro in AWS.
---

## Overview

Unless otherwise specified, new Clusters on Astro are created with a set of default AWS resources that our team has deemed appropriate for most use cases.

Read the following document for a reference of our default resources as well as supported Cluster configurations, including **AWS Region** and **Node Instance Type**.

## Default Cluster Values

| Resource                                  | Description                                                                                                                   | Quantity / Default Size |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| [EKS Cluster](https://aws.amazon.com/eks) | An EKS cluster is required to run the Astro Data Plane, which hosts the resources and data required to execute Airflow tasks. | 1x                      |
| [EC2 Instances](https://aws.amazon.com/ec2/instance-types/) | EC2 instances (nodes) power the system and Airflow components (Webserver, Scheduler, Workers). EC2 instances auto-scale for additional Airflow Deployments. | 2x m5.xlarge |
| [RDS for PostgreSQL Instance](https://aws.amazon.com/rds/) | The RDS instance is the primary database of the Astro Data Plane. It hosts a metadata database for each Airflow Deployment hosted on the EKS cluster. | 1x db.r5.large |
| [Elastic IPs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) | Elastic IPs are required for connectivity with the Control Plane, and other public services. | 2x |
| [Subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html) | Subnets are provisioned in 2 different [Availability Zones (AZs)](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/) for redundancy, with 1 public and 1 private subnet per AZ. Public subnets are required for the NAT and Internet gateways, while private subnets are required for EC2 nodes. | 2x /26 and 2x /22 |
| [Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html) | Required for connectivity with the Control Plane and other public services. | 1x |
| [NAT Gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) | NAT Gateways translate outbound traffic from private subnets to public subnets. | 2x |
| [Routes](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html#route-table-routes) | Routes are necessary to direct network traffic from the subnets and gateways. | 2x |
| [Route Tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html) | Home for the routes. | 2x |
| [VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) | Virtual network for launching and hosting AWS resources. | 1x /19 |
| [S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide//Welcome.html) | S3 bucket for storage of Airflow task logs. | 1x |
| Max Node Count | The maximum number of EC2 nodes that your Astro Cluster can support at any given time. Once this limit is reached, your Cluster cannot auto-scale and worker pods may fail to schedule. | 20 |

## Supported Cluster Configurations

Depending on the needs of your team, you may be interested in modifying certain configurations of a new or existing Cluster on Astro. This section provides a reference for which configuration options are supported during the install process.

To create a new Cluster on Astro with a specified configuration, read [Install on AWS](install-aws.md) or [Create a Cluster](create-cluster.md). For instructions on how to make a change to an existing Cluster, read [Modify a Cluster](modify-cluster.md).

### AWS Region

Astro supports the following AWS regions:

- `af-south-1` - Africa (Cape Town)
- `ap-east-1` - Asia Pacific (Hong Kong)
- `ap-northeast-1` - Asia Pacific (Tokyo)
- `ap-northeast-2` - Asia Pacific (Seoul)
- `ap-northeast-3` - Asia Pacific (Osaka)
- `ap-southeast-1` - Asia Pacific (Singapore)
- `ap-southeast-2` - Asia Pacific (Sydney)
- `ap-south-1` - Asia Pacific (Mumbai)
- `ca-central-1` - Canada (Central)
- `me-south-1` - Middle East (Bahrain)
- `sa-east-1` - South America (São Paulo)
- `us-east-1` - US East (N. Virginia)
- `us-east-2` - US East (Ohio)
- `us-west-1` - US West (N. California)
- `us-west-2` - US West (Oregon)

Modifying the region of an existing Cluster on Astro is not supported. If you're interested in an AWS region that is not on this list, reach out to [Astronomer Support](https://support.astronomer.io).

### Node Instance Type

Astro supports a variety of AWS EC2 instance types. Instance types comprise of varying combinations of CPU, memory, storage, and networking capacity. All system and Airflow components within a single Cluster are powered by the nodes specified during the Cluster creation or modification process.

For detailed information on each instance type, reference [AWS documentation](https://aws.amazon.com/ec2/instance-types/). If you're interested in a node type that is not on this list, reach out to [Astronomer Support](https://support.astronomer.io). Not all instance types are supported in all AWS regions.

#### m5

- m5.xlarge (_default_)
- m5.2xlarge
- m5.4xlarge
- m5.8xlarge
- m5.12xlarge
- m5.16xlarge
- m5.24xlarge
- m5.metal

#### m5d

- m5d.large
- m5d.xlarge
- m5d.2xlarge
- m5d.4xlarge
- m5d.8xlarge
- m5d.12xlarge
- m5d.16xlarge
- m5d.24xlarge
- m5d.metal

#### t2

- t2.xlarge

#### t3

- t3.large
- t3.2xlarge

:::info

Currently, a single Cluster on Astro cannot be configured with more than one node instance type. In early 2022, we expect to introduce support for Worker Queues, which will allow you to run Airflow Workers of varying node types and sizes within a single Deployment. If this is something your team is interested in, reach out to us - we'd love to hear from you.

:::

:::tip

With the exception of `m5d` nodes, all suppported node types have a maximum of 20GB of storage per node for system use only. If you need locally attached storage for task execution, we recommend modifying your cluster to run `m5d` nodes, which Astronomer provisions with NVMe SSD volumes out of the box.

Astronomer plans to support optional ephemeral storage for all node instance types in the first half of 2022.

If you need to pass significant data between Airflow tasks, we recommend using an [XCom backend](https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcoms.html) such as [AWS S3](https://aws.amazon.com/s3/) or [Google Cloud Storage (GCS)](https://cloud.google.com/storage). For more information and best practices, read our Airflow Guide on [Passing Data Between Airflow Tasks](https://www.astronomer.io/guides/airflow-passing-data-between-tasks).

:::

### RDS Instance Type

Every Astro Cluster on AWS is created with and requires an [RDS instance](https://aws.amazon.com/rds/). RDS serves as a primary relational database for the Data Plane and powers the metadata database of each Airflow Deployment within a single Cluster. During the Cluster creation process, you'll be asked to specify an RDS instance type according to your use case and expected workload, but it can be modified at any time.

Astro supports a variety of AWS RDS instance types. Instance types comprise of varying combinations of CPU, memory, storage, and networking capacity. For detailed information on each instance type, reference [AWS documentation](https://aws.amazon.com/rds/instance-types/). If you're interested in an RDS instance type that is not on this list, reach out to [Astronomer Support](https://support.astronomer.io).

#### db.r5

- db.r5.large (_default_)
- db.r5.xlarge
- db.r5.2xlarge
- db.r5.4xlarge
- db.r5.8xlarge
- db.r5.12xlarge
- db.r5.16xlarge
- db.r5.24xlarge

#### db.m5

- db.m5.large
- db.m5.xlarge
- db.m5.2xlarge
- db.m5.4xlarge
- db.m5.8xlarge
- db.m5.12xlarge
- db.m5.16xlarge
- db.m5.24xlarge
