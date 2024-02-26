---
sidebar_label: "Resource reference"
title: "Astro Hosted resource reference"
id: resource-reference-hosted
description: Reference of all supported infrastructure for new Astro Hosted clusters.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::warning

This document applies only to [Astro Hosted](astro-architecture.md) and does not apply to Astro Hybrid. To see whether you're an Astro Hosted user, click your Workspace name in the upper left corner of the Astro UI, then click **Organization Settings**. On the **General** page, your Astro product type is listed under **Product Type**.

For Astro Hybrid resource reference material, see:

- [AWS Hybrid cluster settings](resource-reference-aws-hybrid.md)
- [Azure Hybrid cluster settings](resource-reference-azure-hybrid.md)
- [GCP Hybrid cluster settings](resource-reference-gcp-hybrid.md)

:::

This page contains reference information for all supported Astro Hosted Deployment and cluster resource configurations. Use this information to determine whether Astro supports the type of Airflow environment you want to run.

If you're interested in a cloud region or resource size that's not mentioned here, reach out to [Astronomer support](https://cloud.astronomer.io/open-support-request).

## Add domains to allowlist

If you're on your organization's network and can't access Astro, make a request to allowlist the following domains on your network:

- `https://cloud.astronomer.io/`
- `https://api.astronomer.io/`
- `https://images.astronomer.cloud/`
- `https://auth.astronomer.io/`
- `https://updates.astronomer.io/`
- `https://install.astronomer.io/`
- `https://astro-<organization-short-name>.datakin.com/`
- `https://<organization-short-name>.astronomer.run/`

## Standard cluster regions

A _standard cluster_ is a multi-tenant cluster that's hosted and managed by Astronomer. Astronomer maintains standard clusters in a limited regions and clouds, with support for more regions and clouds coming soon.

Currently, standard clusters are available on the following clouds and regions:

<Tabs
    defaultValue="aws"
    groupId= "standard-cluster-regions"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
        {label: 'Azure', value: 'azure'},
    ]}>
<TabItem value="aws">

| Code             | Region                   |
| ---------------- | ------------------------ |
| `ap-southeast-1` | Asia Pacific (Singapore) |
| `eu-central-1`   | Europe (Frankfurt)       |
| `us-east-1`      | US East (N. Virginia)    |
| `us-west-2`      | US West (Oregon)         |

</TabItem>

<TabItem value="gcp">

| Code           | Region                  |
| -------------- | ----------------------- |
| `europe-west4` | Netherlands, Europe     |
| `us-central1`  | Iowa, North America     |
| `us-east4`     | Virginia, North America |

</TabItem>

<TabItem value="azure">

| Code         | Region                    |
| ------------ | ------------------------- |
| `eastus2`    | Virginia, North America   |
| `westus2`    | Washington, North America |
| `westeurope` | Netherlands, Europe       |

</TabItem>

</Tabs>


## Dedicated cluster regions

A _dedicated cluster_ is cluster that Astronomer provisions solely for use by your Organization. You can create new dedicated clusters from the Astro UI in a variety of clouds and regions. To configure dedicated clusters, see [Create a dedicated cluster](create-dedicated-cluster.md).

Currently, dedicated clusters are available on the following clouds and regions:

<Tabs
    defaultValue="aws"
    groupId= "dedicated-cluster-regions"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
        {label: 'Azure', value: 'azure'},
    ]}>
<TabItem value="aws">

| Code             | Name                      |
| ---------------- | ------------------------- |
| `ap-northeast-1` | Asia Pacific (Tokyo)      |
| `ap-southeast-1` | Asia Pacific (Singapore)  |
| `ap-southeast-2` | Asia Pacific (Sydney)     |
| `ap-south-1`     | Asia Pacific (Mumbai)     |
| `eu-central-1`   | Europe (Frankfurt)        |
| `eu-west-1`      | Europe (Ireland)          |
| `eu-west-2`      | Europe (London)           |
| `sa-east-1`      | South America (São Paulo) |
| `us-east-1`      | US East (N. Virginia)     |
| `us-east-2`      | US East (Ohio)            |
| `us-west-1`      | US West (N. California)   |
| `us-west-2`      | US West (Oregon)          |

</TabItem>

<TabItem value="azure">

| Code            | Region         |
| --------------- | -------------- |
| `australiaeast` | Australia East |
| `brazilsouth`   | Brazil South   |
| `canadacentral` | Canada Central |
| `centralindia`  | Central India  |
| `eastus2`       | East US        |
| `eastus2`       | East US 2      |
| `francecentral` | France Central |
| `japaneast`     | Japan East     |
| `northeurope`   | North Europe   |
| `uksouth`       | UK South       |
| `westeurope`    | West Europe    |
| `westus2`       | West US 2      |

</TabItem>

<TabItem value="gcp">

| Code                      | Name                          |
| ------------------------- | ----------------------------- |
| `asia-east1`              | Taiwan, Asia                  |
| `asia-northeast1`         | Tokyo, Asia                   |
| `asia-northeast2`         | Osaka, Asia                   |
| `asia-northeast3`         | Seoul, Asia                   |
| `asia-south1`             | Mumbai, Asia                  |
| `asia-south2`             | Delhi, Asia                   |
| `asia-southeast1`         | Singapore, Asia               |
| `asia-southeast2`         | Jakarta, Asia                 |
| `australia-southeast1`    | Sydney, Australia             |
| `australia-southeast2`    | Melbourne, Australia          |
| `europe-central2`         | Warsaw, Europe                |
| `europe-north1`           | Finland, Europe               |
| `europe-southwest1`       | Madrid, Europe                |
| `europe-west1`            | Belgium, Europe               |
| `europe-west2`            | England, Europe               |
| `europe-west3`            | Frankfurt, Europe             |
| `europe-west4`            | Netherlands, Europe           |
| `europe-west6`            | Zurich, Europe                |
| `europe-west8`            | Milan, Europe                 |
| `europe-west9`            | Paris, Europe                 |
| `northamerica-northeast1` | Montreal, North America       |
| `northamerica-northeast2` | Toronto, North America        |
| `southamerica-east1`      | Sau Paolo, South America      |
| `southamerica-west1`      | Santiago, South America       |
| `us-central1`             | Iowa, North America           |
| `us-east1`                | South Carolina, North America |
| `us-east4`                | Virginia, North America       |
| `us-east5`                | Columbus, North America       |
| `us-south1`               | Dallas, North America         |
| `us-west1`                | Oregon, North America         |
| `us-west2`                | Los Angeles, North America    |
| `us-west3`                | Salt Lake City, North America |
| `us-west4`                | Nevada, North America         |

</TabItem>

</Tabs>
