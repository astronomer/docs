---
sidebar_label: "Provider package reference"
title: "Astro Runtime provider package reference"
id: runtime-provider-reference
description: View the provider packages and versions included in each release of Astro Runtime
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This page is a reference of the provider packages included in each release of Astro Runtime.

:::tip

To find the version of a provider package installed in an Astro Runtime image, run:

```sh
docker run --rm <runtime-image> pip freeze | grep <provider>
```

For example, to find the version of Celery, run the following command:

```sh
docker run --rm quay.io/astronomer/astro-runtime:11.0.0 pip freeze | grep apache-airflow-providers-celery
```

:::

## Astro Runtime 11.7.0

<Tabs
groupid="astro-runtime-1170"
defaultValue="standard"
values={[
{label: 'Standard', value: 'standard'},
{label: 'Slim', value: 'slim'},
]}>
<TabItem value="standard">
| Package Name | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon | 8.26.0 |
| apache-airflow-providers-celery | 3.7.2 |
| apache-airflow-providers-cncf-kubernetes | 8.3.3 |
| apache-airflow-providers-common-io | 1.3.2 |
| apache-airflow-providers-common-sql | 1.14.2 |
| apache-airflow-providers-datadog | 3.6.1 |
| apache-airflow-providers-elasticsearch | 5.4.1 |
| apache-airflow-providers-fab | 1.2.1 |
| apache-airflow-providers-ftp | 3.10.0 |
| apache-airflow-providers-google | 10.19.0 |
| apache-airflow-providers-http | 4.12.0 |
| apache-airflow-providers-imap | 3.6.1 |
| apache-airflow-providers-microsoft-azure | 9.0.1 |
| apache-airflow-providers-mysql | 5.6.2 |
| apache-airflow-providers-openlineage | 1.9.1 |
| apache-airflow-providers-postgres | 5.11.2 |
| apache-airflow-providers-redis | 3.7.1 |
| apache-airflow-providers-smtp | 1.7.1 |
| apache-airflow-providers-sqlite | 3.8.1 |
| astro-sdk-python | 1.8.1 |
| astronomer-providers | 1.19.1 |
| astronomer-providers-logging | 1.5.1 |

</TabItem>
<TabItem value="slim">

| Package Name                           | Version |
| :------------------------------------- | :------ |
| apache-airflow-providers-celery        | 3.7.2   |
| apache-airflow-providers-common-io     | 1.3.2   |
| apache-airflow-providers-common-sql    | 1.14.2  |
| apache-airflow-providers-elasticsearch | 5.4.1   |
| apache-airflow-providers-fab           | 1.2.1   |
| apache-airflow-providers-ftp           | 3.10.0  |
| apache-airflow-providers-http          | 4.12.0  |
| apache-airflow-providers-imap          | 3.6.1   |
| apache-airflow-providers-mysql         | 5.6.2   |
| apache-airflow-providers-postgres      | 5.11.2  |
| apache-airflow-providers-smtp          | 1.7.1   |
| apache-airflow-providers-sqlite        | 3.8.1   |
| astronomer-providers-logging           | 1.5.1   |

</TabItem>
</Tabs>

## Astro Runtime 11.6.0

<Tabs
groupid="astro-runtime-1160"
defaultValue="standard"
values={[
{label: 'Standard', value: 'standard'},
{label: 'Slim', value: 'slim'},
]}>
<TabItem value="standard">
| Package Name | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon | 8.25.0 |
| apache-airflow-providers-celery | 3.7.2 |
| apache-airflow-providers-cncf-kubernetes | 8.3.2 |
| apache-airflow-providers-common-io | 1.3.2 |
| apache-airflow-providers-common-sql | 1.14.1 |
| apache-airflow-providers-datadog | 3.6.1 |
| apache-airflow-providers-elasticsearch | 5.4.1 |
| apache-airflow-providers-fab | 1.2.0 |
| apache-airflow-providers-ftp | 3.10.0 |
| apache-airflow-providers-google | 10.19.0 |
| apache-airflow-providers-http | 4.12.0 |
| apache-airflow-providers-imap | 3.6.1 |
| apache-airflow-providers-microsoft-azure | 9.0.1 |
| apache-airflow-providers-mysql | 5.6.2 |
| apache-airflow-providers-openlineage | 1.8.0 |
| apache-airflow-providers-postgres | 5.11.2 |
| apache-airflow-providers-redis | 3.7.1 |
| apache-airflow-providers-smtp | 1.7.1 |
| apache-airflow-providers-sqlite | 3.8.1 |
| astro-sdk-python | 1.8.1 |
| astronomer-providers | 1.19.1 |
| astronomer-providers-logging | 1.5.1 |
</TabItem>
<TabItem value="slim">
| Package Name | Version |
|:---------------------------------------|:----------|
| apache-airflow-providers-celery | 3.7.2 |
| apache-airflow-providers-common-io | 1.3.2 |
| apache-airflow-providers-common-sql | 1.14.1 |
| apache-airflow-providers-elasticsearch | 5.4.1 |
| apache-airflow-providers-fab | 1.2.0 |
| apache-airflow-providers-ftp | 3.10.0 |
| apache-airflow-providers-http | 4.12.0 |
| apache-airflow-providers-imap | 3.6.1 |
| apache-airflow-providers-mysql | 5.6.2 |
| apache-airflow-providers-postgres | 5.11.2 |
| apache-airflow-providers-smtp | 1.7.1 |
| apache-airflow-providers-sqlite | 3.8.1 |
| astronomer-providers-logging | 1.5.1 |
</TabItem>
</Tabs>

## Astro Runtime 11.5.0

<Tabs
groupid="astro-runtime-1150"
defaultValue="standard"
values={[
{label: 'Standard', value: 'standard'},
{label: 'Slim', value: 'slim'},
]}>
<TabItem value="standard">
| Package Name | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon | 8.24.0 |
| apache-airflow-providers-celery | 3.7.2 |
| apache-airflow-providers-cncf-kubernetes | 8.3.1 |
| apache-airflow-providers-common-io | 1.3.2 |
| apache-airflow-providers-common-sql | 1.14.0 |
| apache-airflow-providers-datadog | 3.6.1 |
| apache-airflow-providers-elasticsearch | 5.4.1 |
| apache-airflow-providers-fab | 1.1.1 |
| apache-airflow-providers-ftp | 3.9.1 |
| apache-airflow-providers-google | 10.19.0 |
| apache-airflow-providers-http | 4.11.1 |
| apache-airflow-providers-imap | 3.6.1 |
| apache-airflow-providers-microsoft-azure | 9.0.1 |
| apache-airflow-providers-mysql | 5.6.1 |
| apache-airflow-providers-openlineage | 1.8.0 |
| apache-airflow-providers-postgres | 5.11.1 |
| apache-airflow-providers-redis | 3.7.1 |
| apache-airflow-providers-smtp | 1.7.1 |
| apache-airflow-providers-sqlite | 3.8.1 |
| astro-sdk-python | 1.8.0 |
| astronomer-providers | 1.19.1 |
| astronomer-providers-logging | 1.5.1 |

</TabItem>
<TabItem value="slim">

| Package Name                           | Version |
| :------------------------------------- | :------ |
| apache-airflow-providers-celery        | 3.7.2   |
| apache-airflow-providers-common-io     | 1.3.2   |
| apache-airflow-providers-common-sql    | 1.14.0  |
| apache-airflow-providers-elasticsearch | 5.4.1   |
| apache-airflow-providers-fab           | 1.1.1   |
| apache-airflow-providers-ftp           | 3.9.1   |
| apache-airflow-providers-http          | 4.11.1  |
| apache-airflow-providers-imap          | 3.6.1   |
| apache-airflow-providers-mysql         | 5.6.1   |
| apache-airflow-providers-postgres      | 5.11.1  |
| apache-airflow-providers-smtp          | 1.7.1   |
| apache-airflow-providers-sqlite        | 3.8.1   |
| astronomer-providers-logging           | 1.5.1   |

</TabItem>
</Tabs>

## Astro Runtime 11.4.0

<Tabs
groupid="astro-runtime-1140"
defaultValue="standard"
values={[
{label: 'Standard', value: 'standard'},
{label: 'Slim', value: 'slim'},
]}>
<TabItem value="standard">
| Package Name | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon | 8.22.0 |
| apache-airflow-providers-celery | 3.7.0 |
| apache-airflow-providers-cncf-kubernetes | 8.2.0 |
| apache-airflow-providers-common-io | 1.3.1 |
| apache-airflow-providers-common-sql | 1.13.0 |
| apache-airflow-providers-datadog | 3.6.0 |
| apache-airflow-providers-elasticsearch | 5.4.0 |
| apache-airflow-providers-fab | 1.1.0 |
| apache-airflow-providers-ftp | 3.9.0 |
| apache-airflow-providers-google | 10.18.0 |
| apache-airflow-providers-http | 4.11.0 |
| apache-airflow-providers-imap | 3.6.0 |
| apache-airflow-providers-microsoft-azure | 9.0.1 |
| apache-airflow-providers-mysql | 5.6.0 |
| apache-airflow-providers-openlineage | 1.7.1 |
| apache-airflow-providers-postgres | 5.11.0 |
| apache-airflow-providers-redis | 3.7.0 |
| apache-airflow-providers-smtp | 1.7.0 |
| apache-airflow-providers-sqlite | 3.8.0 |
| astro-sdk-python | 1.8.0 |
| astronomer-providers | 1.19.1 |
| astronomer-providers-logging | 1.4.7 |

</TabItem>
<TabItem value="slim">
| Package Name                           | Version |
| :------------------------------------- | :------ |
| apache-airflow-providers-celery        | 3.7.0     |
| apache-airflow-providers-common-io     | 1.3.1     |
| apache-airflow-providers-common-sql    | 1.13.0    |
| apache-airflow-providers-elasticsearch | 5.4.0     |
| apache-airflow-providers-fab           | 1.1.0     |
| apache-airflow-providers-ftp           | 3.9.0     |
| apache-airflow-providers-http          | 4.11.0    |
| apache-airflow-providers-imap          | 3.6.0     |
| apache-airflow-providers-mysql         | 5.6.0     |
| apache-airflow-providers-postgres      | 5.11.0    |
| apache-airflow-providers-smtp          | 1.7.0     |
| apache-airflow-providers-sqlite        | 3.8.0     |
| astronomer-providers-logging           | 1.4.7     |
</TabItem>
</Tabs>

## Astro Runtime 11.3.0

<Tabs
groupid="astro-runtime-1130"
defaultValue="standard"
values={[
{label: 'Standard', value: 'standard'},
{label: 'Slim', value: 'slim'},
]}>
<TabItem value="standard">

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.20.0  |
| apache-airflow-providers-celery          | 3.7.0   |
| apache-airflow-providers-cncf-kubernetes | 8.0.1   |
| apache-airflow-providers-common-io       | 1.3.1   |
| apache-airflow-providers-common-sql      | 1.13.0  |
| apache-airflow-providers-datadog         | 3.6.0   |
| apache-airflow-providers-elasticsearch   | 5.4.0   |
| apache-airflow-providers-fab             | 1.1.0   |
| apache-airflow-providers-ftp             | 3.9.0   |
| apache-airflow-providers-google          | 10.17.0 |
| apache-airflow-providers-http            | 4.11.0  |
| apache-airflow-providers-imap            | 3.6.0   |
| apache-airflow-providers-microsoft-azure | 9.0.1   |
| apache-airflow-providers-mysql           | 5.6.0   |
| apache-airflow-providers-openlineage     | 1.7.1   |
| apache-airflow-providers-postgres        | 5.11.0  |
| apache-airflow-providers-redis           | 3.7.0   |
| apache-airflow-providers-smtp            | 1.7.0   |
| apache-airflow-providers-sqlite          | 3.8.0   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.19.0  |
| astronomer-providers-logging             | 1.4.7   |

</TabItem>
<TabItem value="slim">

| Package Name                           | Version |
| :------------------------------------- | :------ |
| apache-airflow-providers-celery        | 3.7.0   |
| apache-airflow-providers-common-io     | 1.3.1   |
| apache-airflow-providers-common-sql    | 1.13.0  |
| apache-airflow-providers-elasticsearch | 5.4.0   |
| apache-airflow-providers-fab           | 1.1.0   |
| apache-airflow-providers-ftp           | 3.9.0   |
| apache-airflow-providers-http          | 4.11.0  |
| apache-airflow-providers-imap          | 3.6.0   |
| apache-airflow-providers-mysql         | 5.6.0   |
| apache-airflow-providers-postgres      | 5.11.0  |
| apache-airflow-providers-smtp          | 1.7.0   |
| apache-airflow-providers-sqlite        | 3.8.0   |
| astronomer-providers-logging           | 1.4.7   |

</TabItem>
</Tabs>

## Astro Runtime 11.2.0

<Tabs
groupid="astro-runtime-1120"
defaultValue="standard"
values={[
{label: 'Standard', value: 'standard'},
{label: 'Slim', value: 'slim'},
]}>
<TabItem value="standard">
| Package Name | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon | 8.20.0 |
| apache-airflow-providers-celery | 3.6.2 |
| apache-airflow-providers-cncf-kubernetes | 8.0.1 |
| apache-airflow-providers-common-io | 1.3.1 |
| apache-airflow-providers-common-sql | 1.12.0 |
| apache-airflow-providers-datadog | 3.5.1 |
| apache-airflow-providers-elasticsearch | 5.3.4 |
| apache-airflow-providers-fab | 1.0.4 |
| apache-airflow-providers-ftp | 3.8.0 |
| apache-airflow-providers-google | 10.17.0 |
| apache-airflow-providers-http | 4.10.1 |
| apache-airflow-providers-imap | 3.5.0 |
| apache-airflow-providers-microsoft-azure | 9.0.1 |
| apache-airflow-providers-mysql | 5.5.4 |
| apache-airflow-providers-openlineage | 1.7.0 |
| apache-airflow-providers-postgres | 5.10.2 |
| apache-airflow-providers-redis | 3.6.1 |
| apache-airflow-providers-smtp | 1.6.1 |
| apache-airflow-providers-sqlite | 3.7.1 |
| astro-sdk-python | 1.8.0 |
| astronomer-providers | 1.19.0 |
| astronomer-providers-logging | 1.4.7 |
</TabItem>
<TabItem value="slim">
| Package Name | Version |
| :------------------------------------- | :------ |
| apache-airflow-providers-celery | 3.6.2 |
| apache-airflow-providers-common-io | 1.3.1 |
| apache-airflow-providers-common-sql | 1.12.0 |
| apache-airflow-providers-elasticsearch | 5.3.4 |
| apache-airflow-providers-fab | 1.0.4 |
| apache-airflow-providers-ftp | 3.8.0 |
| apache-airflow-providers-http | 4.10.1 |
| apache-airflow-providers-imap | 3.5.0 |
| apache-airflow-providers-mysql | 5.5.4 |
| apache-airflow-providers-postgres | 5.10.2 |
| apache-airflow-providers-smtp | 1.6.1 |
| apache-airflow-providers-sqlite | 3.7.1 |
| astronomer-providers-logging | 1.4.7 |
</TabItem>
</Tabs>

## Astro Runtime 11.1.0

<Tabs
groupid="astro-runtime-1110"
defaultValue="standard"
values={[
{label: 'Standard', value: 'standard'},
{label: 'Slim', value: 'slim'},
]}>
<TabItem value="standard">
| Package Name | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon | 8.20.0 |
| apache-airflow-providers-celery | 3.6.2 |
| apache-airflow-providers-cncf-kubernetes | 8.0.1 |
| apache-airflow-providers-common-io | 1.3.1 |
| apache-airflow-providers-common-sql | 1.12.0 |
| apache-airflow-providers-datadog | 3.5.1 |
| apache-airflow-providers-elasticsearch | 5.3.4 |
| apache-airflow-providers-fab | 1.0.3 |
| apache-airflow-providers-ftp | 3.8.0 |
| apache-airflow-providers-google | 10.17.0 |
| apache-airflow-providers-http | 4.10.1 |
| apache-airflow-providers-imap | 3.5.0 |
| apache-airflow-providers-microsoft-azure | 9.0.1 |
| apache-airflow-providers-openlineage | 1.7.0 |
| apache-airflow-providers-postgres | 5.10.2 |
| apache-airflow-providers-redis | 3.6.1 |
| apache-airflow-providers-smtp | 1.6.1 |
| apache-airflow-providers-sqlite | 3.7.1 |
| astro-sdk-python | 1.8.0 |
| astronomer-providers | 1.19.0 |
| astronomer-providers-logging | 1.4.7 |
</TabItem>
<TabItem value="slim">
| Package Name | Version |
| :------------------------------------- | :------ |
| apache-airflow-providers-celery | 3.6.2 |
| apache-airflow-providers-common-io | 1.3.1 |
| apache-airflow-providers-common-sql | 1.12.0 |
| apache-airflow-providers-elasticsearch | 5.3.4 |
| apache-airflow-providers-fab | 1.0.3 |
| apache-airflow-providers-ftp | 3.8.0 |
| apache-airflow-providers-http | 4.10.1 |
| apache-airflow-providers-imap | 3.5.0 |
| apache-airflow-providers-postgres | 5.10.2 |
| apache-airflow-providers-smtp | 1.6.1 |
| apache-airflow-providers-sqlite | 3.7.1 |
| astronomer-providers-logging | 1.4.7 |
</TabItem>
</Tabs>

## Astro Runtime 11.0.0

<Tabs
groupid="astro-runtime-1100"
defaultValue="standard"
values={[
{label: 'Standard', value: 'standard'},
{label: 'Slim', value: 'slim'},
]}>
<TabItem value="standard">

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.19.0  |
| apache-airflow-providers-celery          | 3.6.1   |
| apache-airflow-providers-cncf-kubernetes | 8.0.1   |
| apache-airflow-providers-common-io       | 1.3.0   |
| apache-airflow-providers-common-sql      | 1.11.1  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.3   |
| apache-airflow-providers-fab             | 1.0.2   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.16.0 |
| apache-airflow-providers-http            | 4.10.0  |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 9.0.1   |
| apache-airflow-providers-openlineage     | 1.6.0   |
| apache-airflow-providers-postgres        | 5.10.2  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-smtp            | 1.6.1   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.19.0  |
| astronomer-providers-logging             | 1.4.7   |

</TabItem>
<TabItem value="slim">

| Package Name                           | Version |
| :------------------------------------- | :------ |
| apache-airflow-providers-celery        | 3.6.1   |
| apache-airflow-providers-common-io     | 1.3.0   |
| apache-airflow-providers-common-sql    | 1.11.1  |
| apache-airflow-providers-elasticsearch | 5.3.3   |
| apache-airflow-providers-fab           | 1.0.2   |
| apache-airflow-providers-ftp           | 3.7.0   |
| apache-airflow-providers-http          | 4.10.0  |
| apache-airflow-providers-imap          | 3.5.0   |
| apache-airflow-providers-postgres      | 5.10.2  |
| apache-airflow-providers-smtp          | 1.6.1   |
| apache-airflow-providers-sqlite        | 3.7.1   |
| astronomer-providers-logging           | 1.4.7   |

</TabItem>
</Tabs>

## Astro Runtime 10.9.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.24.0  |
| apache-airflow-providers-celery          | 3.7.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-io       | 1.3.2   |
| apache-airflow-providers-common-sql      | 1.14.0  |
| apache-airflow-providers-datadog         | 3.6.1   |
| apache-airflow-providers-elasticsearch   | 5.4.1   |
| apache-airflow-providers-ftp             | 3.9.1   |
| apache-airflow-providers-google          | 10.19.0 |
| apache-airflow-providers-http            | 4.11.1  |
| apache-airflow-providers-imap            | 3.6.1   |
| apache-airflow-providers-microsoft-azure | 8.5.1   |
| apache-airflow-providers-openlineage     | 1.8.0   |
| apache-airflow-providers-postgres        | 5.11.1  |
| apache-airflow-providers-redis           | 3.7.1   |
| apache-airflow-providers-smtp            | 1.7.1   |
| apache-airflow-providers-sqlite          | 3.8.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.5.1   |

## Astro Runtime 10.8.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.20.0  |
| apache-airflow-providers-celery          | 3.6.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-io       | 1.3.1   |
| apache-airflow-providers-common-sql      | 1.12.0  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.4   |
| apache-airflow-providers-ftp             | 3.8.0   |
| apache-airflow-providers-google          | 10.17.0 |
| apache-airflow-providers-http            | 4.10.1  |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 8.5.1   |
| apache-airflow-providers-openlineage     | 1.7.0   |
| apache-airflow-providers-postgres        | 5.10.2  |
| apache-airflow-providers-redis           | 3.6.1   |
| apache-airflow-providers-smtp            | 1.6.1   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 10.7.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.19.0  |
| apache-airflow-providers-celery          | 3.6.1   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-io       | 1.3.0   |
| apache-airflow-providers-common-sql      | 1.11.1  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.3   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.16.0 |
| apache-airflow-providers-http            | 4.10.0  |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 8.5.1   |
| apache-airflow-providers-openlineage     | 1.6.0   |
| apache-airflow-providers-postgres        | 5.10.2  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-smtp            | 1.6.1   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 10.6.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.19.0  |
| apache-airflow-providers-celery          | 3.6.1   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-io       | 1.3.0   |
| apache-airflow-providers-common-sql      | 1.11.1  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.3   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.16.0 |
| apache-airflow-providers-http            | 4.10.0  |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 8.5.1   |
| apache-airflow-providers-openlineage     | 1.6.0   |
| apache-airflow-providers-postgres        | 5.10.2  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-smtp            | 1.6.1   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 10.5.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.19.0  |
| apache-airflow-providers-celery          | 3.6.1   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-io       | 1.3.0   |
| apache-airflow-providers-common-sql      | 1.11.1  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.3   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.15.0 |
| apache-airflow-providers-http            | 4.10.0  |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 8.5.1   |
| apache-airflow-providers-openlineage     | 1.6.0   |
| apache-airflow-providers-postgres        | 5.10.2  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-smtp            | 1.6.1   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 10.4.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.18.0  |
| apache-airflow-providers-celery          | 3.6.0   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-io       | 1.3.0   |
| apache-airflow-providers-common-sql      | 1.11.0  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.3   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.15.0 |
| apache-airflow-providers-http            | 4.9.1   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 8.5.1   |
| apache-airflow-providers-openlineage     | 1.5.0   |
| apache-airflow-providers-postgres        | 5.10.1  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 10.3.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.5.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-io       | 1.2.0   |
| apache-airflow-providers-common-sql      | 1.10.1  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.2   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.13.1 |
| apache-airflow-providers-http            | 4.9.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 8.5.1   |
| apache-airflow-providers-openlineage     | 1.5.0   |
| apache-airflow-providers-postgres        | 5.10.0  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-sqlite          | 3.7.0   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 10.2.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.5.1   |
| apache-airflow-providers-cncf-kubernetes | 7.13.0  |
| apache-airflow-providers-common-io       | 1.2.0   |
| apache-airflow-providers-common-sql      | 1.10.0  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.1   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.13.1 |
| apache-airflow-providers-http            | 4.8.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 8.5.1   |
| apache-airflow-providers-openlineage     | 1.4.0   |
| apache-airflow-providers-postgres        | 5.10.0  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-sqlite          | 3.7.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.6   |

## Astro Runtime 10.1.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.15.0  |
| apache-airflow-providers-celery          | 3.5.1   |
| apache-airflow-providers-cncf-kubernetes | 7.13.0  |
| apache-airflow-providers-common-sql      | 1.10.0  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.1   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.13.1 |
| apache-airflow-providers-http            | 4.8.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 8.5.1   |
| apache-airflow-providers-openlineage     | 1.3.1   |
| apache-airflow-providers-postgres        | 5.10.0  |
| apache-airflow-providers-redis           | 3.5.0   |
| apache-airflow-providers-sqlite          | 3.7.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.6   |

## Astro Runtime 10.0.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.13.0  |
| apache-airflow-providers-celery          | 3.5.0   |
| apache-airflow-providers-cncf-kubernetes | 7.11.0  |
| apache-airflow-providers-common-sql      | 1.9.0   |
| apache-airflow-providers-datadog         | 3.5.0   |
| apache-airflow-providers-elasticsearch   | 5.3.0   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.8.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 8.4.0   |
| apache-airflow-providers-openlineage     | 1.3.0   |
| apache-airflow-providers-postgres        | 5.9.0   |
| apache-airflow-providers-redis           | 3.5.0   |
| apache-airflow-providers-sqlite          | 3.6.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.4   |

## Astro Runtime 9.17.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.26.0  |
| apache-airflow-providers-celery          | 3.7.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.14.1  |
| apache-airflow-providers-datadog         | 3.6.1   |
| apache-airflow-providers-elasticsearch   | 5.4.1   |
| apache-airflow-providers-ftp             | 3.10.0  |
| apache-airflow-providers-google          | 10.21.0 |
| apache-airflow-providers-http            | 4.12.0  |
| apache-airflow-providers-imap            | 3.6.1   |
| apache-airflow-providers-microsoft-azure | 10.2.0  |
| apache-airflow-providers-mysql           | 5.6.2   |
| apache-airflow-providers-openlineage     | 1.9.1   |
| apache-airflow-providers-postgres        | 5.11.2  |
| apache-airflow-providers-redis           | 3.7.1   |
| apache-airflow-providers-sqlite          | 3.8.1   |
| astro-sdk-python                         | 1.8.1   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.5.1   |

## Astro Runtime 9.16.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.25.0  |
| apache-airflow-providers-celery          | 3.7.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.14.1  |
| apache-airflow-providers-datadog         | 3.6.1   |
| apache-airflow-providers-elasticsearch   | 5.4.1   |
| apache-airflow-providers-ftp             | 3.10.0  |
| apache-airflow-providers-google          | 10.20.0 |
| apache-airflow-providers-http            | 4.12.0  |
| apache-airflow-providers-imap            | 3.6.1   |
| apache-airflow-providers-microsoft-azure | 10.1.2  |
| apache-airflow-providers-mysql           | 5.6.2   |
| apache-airflow-providers-openlineage     | 1.8.0   |
| apache-airflow-providers-postgres        | 5.11.2  |
| apache-airflow-providers-redis           | 3.7.1   |
| apache-airflow-providers-sqlite          | 3.8.1   |

## Astro Runtime 9.15.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.24.0  |
| apache-airflow-providers-celery          | 3.7.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.14.0  |
| apache-airflow-providers-datadog         | 3.6.1   |
| apache-airflow-providers-elasticsearch   | 5.4.1   |
| apache-airflow-providers-ftp             | 3.9.1   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.11.1  |
| apache-airflow-providers-imap            | 3.6.1   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-mysql           | 5.6.1   |
| apache-airflow-providers-openlineage     | 1.8.0   |
| apache-airflow-providers-postgres        | 5.11.1  |
| apache-airflow-providers-redis           | 3.7.1   |
| apache-airflow-providers-sqlite          | 3.8.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.5.1   |

## Astro Runtime 9.14.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.7.0   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.13.0  |
| apache-airflow-providers-datadog         | 3.6.0   |
| apache-airflow-providers-elasticsearch   | 5.4.0   |
| apache-airflow-providers-ftp             | 3.9.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.11.0  |
| apache-airflow-providers-imap            | 3.6.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-mysql           | 5.6.0   |
| apache-airflow-providers-openlineage     | 1.7.1   |
| apache-airflow-providers-postgres        | 5.11.0  |
| apache-airflow-providers-redis           | 3.7.0   |
| apache-airflow-providers-sqlite          | 3.8.0   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 9.13.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.6.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.12.0  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.4   |
| apache-airflow-providers-ftp             | 3.8.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.9.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.7.0   |
| apache-airflow-providers-postgres        | 5.10.2  |
| apache-airflow-providers-redis           | 3.6.1   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 9.12.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.6.0   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.11.1  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.3   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.9.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.5.0   |
| apache-airflow-providers-postgres        | 5.10.2  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 9.11.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.6.0   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.11.0  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.3   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.9.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.5.0   |
| apache-airflow-providers-postgres        | 5.10.1  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 9.10.2

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.5.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.10.1  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.4   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.9.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.5.0   |
| apache-airflow-providers-postgres        | 5.10.2  |
| apache-airflow-providers-redis           | 3.6.1   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 9.10.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.5.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.10.1  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.3   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.9.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.5.0   |
| apache-airflow-providers-postgres        | 5.10.2  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-sqlite          | 3.7.1   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 9.10.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.5.2   |
| apache-airflow-providers-cncf-kubernetes | 7.14.0  |
| apache-airflow-providers-common-sql      | 1.10.1  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.2   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.9.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.5.0   |
| apache-airflow-providers-postgres        | 5.10.0  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-sqlite          | 3.7.0   |
| astro-sdk-python                         | 1.8.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.7   |

## Astro Runtime 9.9.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.16.0  |
| apache-airflow-providers-celery          | 3.5.1   |
| apache-airflow-providers-cncf-kubernetes | 7.13.0  |
| apache-airflow-providers-common-sql      | 1.10.0  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.1   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.8.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.4.0   |
| apache-airflow-providers-postgres        | 5.10.0  |
| apache-airflow-providers-redis           | 3.6.0   |
| apache-airflow-providers-sqlite          | 3.7.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.6   |

## Astro Runtime 9.8.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.15.0  |
| apache-airflow-providers-celery          | 3.5.1   |
| apache-airflow-providers-cncf-kubernetes | 7.13.0  |
| apache-airflow-providers-common-sql      | 1.10.0  |
| apache-airflow-providers-datadog         | 3.5.1   |
| apache-airflow-providers-elasticsearch   | 5.3.1   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.8.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.3.1   |
| apache-airflow-providers-postgres        | 5.10.0  |
| apache-airflow-providers-redis           | 3.5.0   |
| apache-airflow-providers-sqlite          | 3.7.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.6   |

## Astro Runtime 9.7.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.13.0  |
| apache-airflow-providers-celery          | 3.5.0   |
| apache-airflow-providers-cncf-kubernetes | 7.11.0  |
| apache-airflow-providers-common-sql      | 1.9.0   |
| apache-airflow-providers-datadog         | 3.5.0   |
| apache-airflow-providers-elasticsearch   | 5.3.0   |
| apache-airflow-providers-ftp             | 3.7.0   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.8.0   |
| apache-airflow-providers-imap            | 3.5.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.3.0   |
| apache-airflow-providers-postgres        | 5.9.0   |
| apache-airflow-providers-redis           | 3.5.0   |
| apache-airflow-providers-sqlite          | 3.6.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.4  |
| astronomer-providers-logging             | 1.4.5   |

## Astro Runtime 9.6.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.12.0  |
| apache-airflow-providers-celery          | 3.4.1   |
| apache-airflow-providers-cncf-kubernetes | 7.10.0  |
| apache-airflow-providers-common-sql      | 1.8.1   |
| apache-airflow-providers-datadog         | 3.4.0   |
| apache-airflow-providers-elasticsearch   | 5.2.0   |
| apache-airflow-providers-ftp             | 3.6.1   |
| apache-airflow-providers-google          | 10.12.0 |
| apache-airflow-providers-http            | 4.7.0   |
| apache-airflow-providers-imap            | 3.4.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.2.1   |
| apache-airflow-providers-postgres        | 5.8.0   |
| apache-airflow-providers-redis           | 3.4.1   |
| apache-airflow-providers-sqlite          | 3.5.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.3  |
| astronomer-providers-logging             | 1.4.3   |

## Astro Runtime 9.5.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.10.0  |
| apache-airflow-providers-celery          | 3.4.1   |
| apache-airflow-providers-cncf-kubernetes | 7.8.0   |
| apache-airflow-providers-common-sql      | 1.8.0   |
| apache-airflow-providers-datadog         | 3.4.0   |
| apache-airflow-providers-elasticsearch   | 5.1.0   |
| apache-airflow-providers-ftp             | 3.6.0   |
| apache-airflow-providers-google          | 10.11.0 |
| apache-airflow-providers-http            | 4.6.0   |
| apache-airflow-providers-imap            | 3.4.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.2.0   |
| apache-airflow-providers-postgres        | 5.7.1   |
| apache-airflow-providers-redis           | 3.4.0   |
| apache-airflow-providers-sqlite          | 3.5.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.1  |
| astronomer-providers-logging             | 1.4.1   |

## Astro Runtime 9.4.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.7.1   |
| apache-airflow-providers-celery          | 3.4.0   |
| apache-airflow-providers-cncf-kubernetes | 7.7.0   |
| apache-airflow-providers-common-sql      | 1.8.0   |
| apache-airflow-providers-datadog         | 3.4.0   |
| apache-airflow-providers-elasticsearch   | 5.1.0   |
| apache-airflow-providers-ftp             | 3.6.0   |
| apache-airflow-providers-google          | 10.10.0 |
| apache-airflow-providers-http            | 4.6.0   |
| apache-airflow-providers-imap            | 3.4.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.1.1   |
| apache-airflow-providers-postgres        | 5.7.0   |
| apache-airflow-providers-redis           | 3.4.0   |
| apache-airflow-providers-sqlite          | 3.5.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.0  |
| astronomer-providers-logging             | 1.4.1   |

## Astro Runtime 9.3.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.7.1   |
| apache-airflow-providers-celery          | 3.4.0   |
| apache-airflow-providers-cncf-kubernetes | 7.7.0   |
| apache-airflow-providers-common-sql      | 1.8.0   |
| apache-airflow-providers-datadog         | 3.4.0   |
| apache-airflow-providers-elasticsearch   | 5.1.0   |
| apache-airflow-providers-ftp             | 3.6.0   |
| apache-airflow-providers-google          | 10.10.0 |
| apache-airflow-providers-http            | 4.6.0   |
| apache-airflow-providers-imap            | 3.4.0   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.1.1   |
| apache-airflow-providers-postgres        | 5.7.0   |
| apache-airflow-providers-redis           | 3.4.0   |
| apache-airflow-providers-sqlite          | 3.5.0   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.0  |
| astronomer-providers-logging             | 1.3.0   |

## Astro Runtime 9.2.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.7.1   |
| apache-airflow-providers-celery          | 3.3.4   |
| apache-airflow-providers-cncf-kubernetes | 7.6.0   |
| apache-airflow-providers-common-sql      | 1.7.2   |
| apache-airflow-providers-datadog         | 3.3.2   |
| apache-airflow-providers-elasticsearch   | 5.0.2   |
| apache-airflow-providers-ftp             | 3.5.2   |
| apache-airflow-providers-google          | 10.9.0  |
| apache-airflow-providers-http            | 4.5.2   |
| apache-airflow-providers-imap            | 3.3.2   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-openlineage     | 1.1.0   |
| apache-airflow-providers-postgres        | 5.6.1   |
| apache-airflow-providers-redis           | 3.3.2   |
| apache-airflow-providers-sqlite          | 3.4.3   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.0  |
| astronomer-providers-logging             | 1.3.0   |

## Astro Runtime 9.1.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.6.0   |
| apache-airflow-providers-celery          | 3.3.3   |
| apache-airflow-providers-cncf-kubernetes | 7.5.0   |
| apache-airflow-providers-common-sql      | 1.7.1   |
| apache-airflow-providers-datadog         | 3.3.2   |
| apache-airflow-providers-elasticsearch   | 5.0.1   |
| apache-airflow-providers-ftp             | 3.5.1   |
| apache-airflow-providers-google          | 10.7.0  |
| apache-airflow-providers-http            | 4.5.1   |
| apache-airflow-providers-imap            | 3.3.1   |
| apache-airflow-providers-microsoft-azure | 6.3.0   |
| apache-airflow-providers-postgres        | 5.6.0   |
| apache-airflow-providers-redis           | 3.3.1   |
| apache-airflow-providers-sqlite          | 3.4.3   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.17.3  |
| astronomer-providers-logging             | 1.2.1   |

## Astro Runtime 9.0.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.5.1   |
| apache-airflow-providers-celery          | 3.3.2   |
| apache-airflow-providers-cncf-kubernetes | 7.4.2   |
| apache-airflow-providers-common-sql      | 1.7.0   |
| apache-airflow-providers-datadog         | 3.3.1   |
| apache-airflow-providers-elasticsearch   | 5.0.0   |
| apache-airflow-providers-ftp             | 3.5.0   |
| apache-airflow-providers-google          | 10.6.0  |
| apache-airflow-providers-http            | 4.5.0   |
| apache-airflow-providers-imap            | 3.3.0   |
| apache-airflow-providers-microsoft-azure | 6.2.4   |
| apache-airflow-providers-postgres        | 5.6.0   |
| apache-airflow-providers-redis           | 3.3.1   |
| apache-airflow-providers-sqlite          | 3.4.3   |
| astro-sdk-python                         | 1.6.2   |
| astronomer-providers                     | 1.17.3  |
| astronomer-providers-logging             | 1.1.0   |

## Astro Runtime 8.10.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.7.1   |
| apache-airflow-providers-celery          | 3.3.4   |
| apache-airflow-providers-cncf-kubernetes | 7.6.0   |
| apache-airflow-providers-common-sql      | 1.7.2   |
| apache-airflow-providers-datadog         | 3.3.2   |
| apache-airflow-providers-elasticsearch   | 4.5.1   |
| apache-airflow-providers-ftp             | 3.5.2   |
| apache-airflow-providers-google          | 10.9.0  |
| apache-airflow-providers-http            | 4.5.2   |
| apache-airflow-providers-imap            | 3.3.2   |
| apache-airflow-providers-microsoft-azure | 7.0.0   |
| apache-airflow-providers-postgres        | 5.6.1   |
| apache-airflow-providers-redis           | 3.3.1   |
| apache-airflow-providers-sqlite          | 3.4.3   |
| astro-sdk-python                         | 1.7.0   |
| astronomer-providers                     | 1.18.0  |

## Astro Runtime 8.9.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.3.1   |
| apache-airflow-providers-celery          | 3.2.1   |
| apache-airflow-providers-cncf-kubernetes | 7.3.0   |
| apache-airflow-providers-common-sql      | 1.6.0   |
| apache-airflow-providers-datadog         | 3.3.1   |
| apache-airflow-providers-elasticsearch   | 4.5.1   |
| apache-airflow-providers-ftp             | 3.4.2   |
| apache-airflow-providers-google          | 10.4.0  |
| apache-airflow-providers-http            | 4.5.0   |
| apache-airflow-providers-imap            | 3.2.2   |
| apache-airflow-providers-microsoft-azure | 6.2.4   |
| apache-airflow-providers-postgres        | 5.5.2   |
| apache-airflow-providers-redis           | 3.2.1   |
| apache-airflow-providers-sqlite          | 3.4.2   |
| astro-sdk-python                         | 1.6.2   |
| astronomer-providers                     | 1.17.3  |

## Astro Runtime 8.8.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.3.1   |
| apache-airflow-providers-celery          | 3.2.1   |
| apache-airflow-providers-cncf-kubernetes | 7.3.0   |
| apache-airflow-providers-common-sql      | 1.6.0   |
| apache-airflow-providers-datadog         | 3.3.1   |
| apache-airflow-providers-elasticsearch   | 4.5.1   |
| apache-airflow-providers-ftp             | 3.4.2   |
| apache-airflow-providers-google          | 10.0.0  |
| apache-airflow-providers-http            | 4.5.0   |
| apache-airflow-providers-imap            | 3.2.2   |
| apache-airflow-providers-microsoft-azure | 6.2.1   |
| apache-airflow-providers-postgres        | 5.5.2   |
| apache-airflow-providers-redis           | 3.2.1   |
| apache-airflow-providers-sqlite          | 3.4.2   |
| astro-sdk-python                         | 1.6.1   |
| astronomer-providers                     | 1.17.1  |

## Astro Runtime 8.7.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.3.0   |
| apache-airflow-providers-celery          | 3.2.1   |
| apache-airflow-providers-cncf-kubernetes | 7.2.0   |
| apache-airflow-providers-common-sql      | 1.6.0   |
| apache-airflow-providers-datadog         | 3.3.1   |
| apache-airflow-providers-elasticsearch   | 4.5.1   |
| apache-airflow-providers-ftp             | 3.4.2   |
| apache-airflow-providers-google          | 10.0.0  |
| apache-airflow-providers-http            | 4.4.2   |
| apache-airflow-providers-imap            | 3.2.2   |
| apache-airflow-providers-microsoft-azure | 6.2.0   |
| apache-airflow-providers-postgres        | 5.5.2   |
| apache-airflow-providers-redis           | 3.2.1   |
| apache-airflow-providers-sqlite          | 3.4.2   |
| astro-sdk-python                         | 1.6.1   |
| astronomer-providers                     | 1.17.1  |

## Astro Runtime 8.6.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.2.0   |
| apache-airflow-providers-celery          | 3.2.1   |
| apache-airflow-providers-cncf-kubernetes | 7.1.0   |
| apache-airflow-providers-common-sql      | 1.5.2   |
| apache-airflow-providers-datadog         | 3.3.1   |
| apache-airflow-providers-elasticsearch   | 4.5.1   |
| apache-airflow-providers-ftp             | 3.4.2   |
| apache-airflow-providers-google          | 10.0.0  |
| apache-airflow-providers-http            | 4.4.2   |
| apache-airflow-providers-imap            | 3.2.2   |
| apache-airflow-providers-microsoft-azure | 6.1.2   |
| apache-airflow-providers-postgres        | 5.5.1   |
| apache-airflow-providers-redis           | 3.2.1   |
| apache-airflow-providers-sqlite          | 3.4.2   |
| astro-sdk-python                         | 1.6.1   |
| astronomer-providers                     | 1.17.1  |

## Astro Runtime 8.5.0

| Package Name                             | Version       |
| :--------------------------------------- | :------------ |
| apache-airflow-providers-amazon          | 8.1.0         |
| apache-airflow-providers-celery          | 3.2.0         |
| apache-airflow-providers-cncf-kubernetes | 7.0.0+astro.2 |
| apache-airflow-providers-common-sql      | 1.5.1         |
| apache-airflow-providers-datadog         | 3.3.0         |
| apache-airflow-providers-elasticsearch   | 4.5.0         |
| apache-airflow-providers-ftp             | 3.4.1         |
| apache-airflow-providers-google          | 10.0.0        |
| apache-airflow-providers-http            | 4.4.1         |
| apache-airflow-providers-imap            | 3.2.1         |
| apache-airflow-providers-microsoft-azure | 6.1.1         |
| apache-airflow-providers-postgres        | 5.5.0         |
| apache-airflow-providers-redis           | 3.2.0         |
| apache-airflow-providers-sqlite          | 3.4.1         |
| astro-sdk-python                         | 1.6.1         |
| astronomer-providers                     | 1.16.0        |

## Astro Runtime 8.4.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.1.0   |
| apache-airflow-providers-celery          | 3.2.0   |
| apache-airflow-providers-cncf-kubernetes | 7.0.0   |
| apache-airflow-providers-common-sql      | 1.5.1   |
| apache-airflow-providers-datadog         | 3.3.0   |
| apache-airflow-providers-elasticsearch   | 4.5.0   |
| apache-airflow-providers-ftp             | 3.4.1   |
| apache-airflow-providers-google          | 10.0.0  |
| apache-airflow-providers-http            | 4.4.1   |
| apache-airflow-providers-imap            | 3.2.1   |
| apache-airflow-providers-microsoft-azure | 6.1.1   |
| apache-airflow-providers-postgres        | 5.5.0   |
| apache-airflow-providers-redis           | 3.2.0   |
| apache-airflow-providers-sqlite          | 3.4.1   |
| astro-sdk-python                         | 1.6.1   |
| astronomer-providers                     | 1.16.0  |

## Astro Runtime 8.3.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.0.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 6.1.0   |
| apache-airflow-providers-common-sql      | 1.4.0   |
| apache-airflow-providers-datadog         | 3.2.0   |
| apache-airflow-providers-elasticsearch   | 4.4.0   |
| apache-airflow-providers-ftp             | 3.3.1   |
| apache-airflow-providers-google          | 10.0.0  |
| apache-airflow-providers-http            | 4.3.0   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 6.1.0   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sqlite          | 3.3.2   |
| astro-sdk-python                         | 1.6.1   |
| astronomer-providers                     | 1.16.0  |

## Astro Runtime 8.2.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.0.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 6.1.0   |
| apache-airflow-providers-common-sql      | 1.4.0   |
| apache-airflow-providers-elasticsearch   | 4.4.0   |
| apache-airflow-providers-ftp             | 3.3.1   |
| apache-airflow-providers-google          | 10.0.0  |
| apache-airflow-providers-http            | 4.3.0   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 6.0.0   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sqlite          | 3.3.2   |
| astro-sdk-python                         | 1.6.0   |
| astronomer-providers                     | 1.15.5  |

## Astro Runtime 8.1.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.0.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 6.1.0   |
| apache-airflow-providers-common-sql      | 1.4.0   |
| apache-airflow-providers-elasticsearch   | 4.4.0   |
| apache-airflow-providers-ftp             | 3.3.1   |
| apache-airflow-providers-google          | 10.0.0  |
| apache-airflow-providers-http            | 4.3.0   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 6.0.0   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sqlite          | 3.3.2   |
| astro-sdk-python                         | 1.6.0   |
| astronomer-providers                     | 1.15.5  |

## Astro Runtime 8.0.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 8.0.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 6.1.0   |
| apache-airflow-providers-common-sql      | 1.4.0   |
| apache-airflow-providers-elasticsearch   | 4.4.0   |
| apache-airflow-providers-ftp             | 3.3.1   |
| apache-airflow-providers-google          | 10.0.0  |
| apache-airflow-providers-http            | 4.3.0   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 6.0.0   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sqlite          | 3.3.2   |
| astro-sdk-python                         | 1.5.3   |
| astronomer-providers                     | 1.15.5  |

## Astro Runtime 7.6.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| airflow-provider-duckdb                  | 0.1.0   |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 6.1.0   |
| apache-airflow-providers-apache-livy     | 3.5.0   |
| apache-airflow-providers-celery          | 3.2.0   |
| apache-airflow-providers-cncf-kubernetes | 5.2.2   |
| apache-airflow-providers-common-sql      | 1.5.1   |
| apache-airflow-providers-databricks      | 4.2.0   |
| apache-airflow-providers-dbt-cloud       | 3.2.0   |
| apache-airflow-providers-elasticsearch   | 4.5.0   |
| apache-airflow-providers-ftp             | 3.4.1   |
| apache-airflow-providers-google          | 8.12.0  |
| apache-airflow-providers-http            | 4.4.1   |
| apache-airflow-providers-imap            | 3.2.1   |
| apache-airflow-providers-microsoft-azure | 5.3.1   |
| apache-airflow-providers-microsoft-mssql | 3.4.0   |
| apache-airflow-providers-postgres        | 5.5.0   |
| apache-airflow-providers-redis           | 3.2.0   |
| apache-airflow-providers-sftp            | 4.3.0   |
| apache-airflow-providers-snowflake       | 4.1.0   |
| apache-airflow-providers-sqlite          | 3.4.1   |
| apache-airflow-providers-ssh             | 3.7.0   |
| astro-sdk-python                         | 1.6.1   |
| astronomer-providers                     | 1.16.0  |

## Astro Runtime 7.5.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| airflow-provider-duckdb                  | 0.1.0   |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 6.1.0   |
| apache-airflow-providers-apache-livy     | 3.5.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 5.2.2   |
| apache-airflow-providers-common-sql      | 1.5.1   |
| apache-airflow-providers-databricks      | 4.2.0   |
| apache-airflow-providers-dbt-cloud       | 3.2.0   |
| apache-airflow-providers-elasticsearch   | 4.4.0   |
| apache-airflow-providers-ftp             | 3.3.1   |
| apache-airflow-providers-google          | 8.11.0  |
| apache-airflow-providers-http            | 4.2.0   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 5.2.1   |
| apache-airflow-providers-microsoft-mssql | 3.4.0   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sftp            | 4.3.0   |
| apache-airflow-providers-snowflake       | 4.1.0   |
| apache-airflow-providers-sqlite          | 3.3.1   |
| apache-airflow-providers-ssh             | 3.7.0   |
| astro-sdk-python                         | 1.6.1   |
| astronomer-providers                     | 1.16.0  |

## Astro Runtime 7.4.3

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| airflow-provider-duckdb                  | 0.0.2   |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 6.0.0   |
| apache-airflow-providers-apache-livy     | 3.4.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 5.2.2   |
| apache-airflow-providers-common-sql      | 1.3.4   |
| apache-airflow-providers-databricks      | 4.1.0   |
| apache-airflow-providers-dbt-cloud       | 3.1.1   |
| apache-airflow-providers-elasticsearch   | 4.4.0   |
| apache-airflow-providers-ftp             | 3.3.1   |
| apache-airflow-providers-google          | 8.11.0  |
| apache-airflow-providers-http            | 4.2.0   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 5.2.1   |
| apache-airflow-providers-microsoft-mssql | 3.3.2   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sftp            | 4.2.4   |
| apache-airflow-providers-snowflake       | 4.0.5   |
| apache-airflow-providers-sqlite          | 3.3.1   |
| apache-airflow-providers-ssh             | 3.6.0   |
| astro-sdk-python                         | 1.5.3   |
| astronomer-providers                     | 1.15.5  |

## Astro Runtime 7.4.2

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| airflow-provider-duckdb                  | 0.0.2   |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 5.1.3   |
| apache-airflow-providers-apache-livy     | 3.3.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 5.2.2   |
| apache-airflow-providers-common-sql      | 1.3.4   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 3.1.0   |
| apache-airflow-providers-elasticsearch   | 4.4.0   |
| apache-airflow-providers-ftp             | 3.3.1   |
| apache-airflow-providers-google          | 8.11.0  |
| apache-airflow-providers-http            | 4.2.0   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 5.2.1   |
| apache-airflow-providers-microsoft-mssql | 3.3.2   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sftp            | 4.2.4   |
| apache-airflow-providers-snowflake       | 4.0.4   |
| apache-airflow-providers-sqlite          | 3.3.1   |
| apache-airflow-providers-ssh             | 3.5.0   |
| astro-sdk-python                         | 1.5.3   |
| astronomer-providers                     | 1.15.2  |

## Astro Runtime 7.4.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| airflow-provider-duckdb                  | 0.0.2   |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 5.1.3   |
| apache-airflow-providers-apache-livy     | 3.3.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 5.2.2   |
| apache-airflow-providers-common-sql      | 1.3.4   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 3.1.0   |
| apache-airflow-providers-elasticsearch   | 4.4.0   |
| apache-airflow-providers-ftp             | 3.3.1   |
| apache-airflow-providers-google          | 8.11.0  |
| apache-airflow-providers-http            | 4.2.0   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 5.2.1   |
| apache-airflow-providers-microsoft-mssql | 3.3.2   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sftp            | 4.2.4   |
| apache-airflow-providers-snowflake       | 4.0.4   |
| apache-airflow-providers-sqlite          | 3.3.1   |
| apache-airflow-providers-ssh             | 3.5.0   |
| astro-sdk-python                         | 1.5.3   |
| astronomer-providers                     | 1.15.1  |

## Astro Runtime 7.4.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| airflow-provider-duckdb                  | 0.0.2   |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 5.1.3   |
| apache-airflow-providers-apache-livy     | 3.3.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 5.2.2   |
| apache-airflow-providers-common-sql      | 1.3.4   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 3.1.0   |
| apache-airflow-providers-elasticsearch   | 4.4.0   |
| apache-airflow-providers-ftp             | 3.3.1   |
| apache-airflow-providers-google          | 8.11.0  |
| apache-airflow-providers-http            | 4.2.0   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 5.2.1   |
| apache-airflow-providers-microsoft-mssql | 3.3.2   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sftp            | 4.2.4   |
| apache-airflow-providers-snowflake       | 4.0.4   |
| apache-airflow-providers-sqlite          | 3.3.1   |
| apache-airflow-providers-ssh             | 3.5.0   |
| astro-sdk-python                         | 1.5.3   |
| astronomer-providers                     | 1.15.1  |

## Astro Runtime 7.3.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| airflow-provider-duckdb                  | 0.0.2   |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 5.1.2   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 5.1.1   |
| apache-airflow-providers-common-sql      | 1.3.3   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 3.0.0   |
| apache-airflow-providers-elasticsearch   | 4.3.3   |
| apache-airflow-providers-ftp             | 3.3.0   |
| apache-airflow-providers-google          | 8.8.0   |
| apache-airflow-providers-http            | 4.1.1   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 5.2.0   |
| apache-airflow-providers-microsoft-mssql | 3.3.2   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sftp            | 4.2.2   |
| apache-airflow-providers-snowflake       | 4.0.3   |
| apache-airflow-providers-sqlite          | 3.3.1   |
| apache-airflow-providers-ssh             | 3.4.0   |
| astro-sdk-python                         | 1.5.0   |
| astronomer-providers                     | 1.14.0  |

## Astro Runtime 7.2.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 5.1.1   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 5.1.1   |
| apache-airflow-providers-common-sql      | 1.3.3   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.1   |
| apache-airflow-providers-elasticsearch   | 4.3.3   |
| apache-airflow-providers-ftp             | 3.3.0   |
| apache-airflow-providers-google          | 8.8.0   |
| apache-airflow-providers-http            | 4.1.1   |
| apache-airflow-providers-imap            | 3.1.1   |
| apache-airflow-providers-microsoft-azure | 5.1.0   |
| apache-airflow-providers-postgres        | 5.4.0   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sftp            | 4.2.1   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.3.1   |
| apache-airflow-providers-ssh             | 3.4.0   |
| astro-sdk-python                         | 1.4.0   |
| astronomer-providers                     | 1.14.0  |

## Astro Runtime 7.1.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 5.0.0   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 5.0.0   |
| apache-airflow-providers-common-sql      | 1.3.1   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.0   |
| apache-airflow-providers-elasticsearch   | 4.3.1   |
| apache-airflow-providers-ftp             | 3.2.0   |
| apache-airflow-providers-google          | 8.6.0   |
| apache-airflow-providers-http            | 4.1.0   |
| apache-airflow-providers-imap            | 3.1.0   |
| apache-airflow-providers-microsoft-azure | 5.0.1   |
| apache-airflow-providers-postgres        | 5.3.1   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sftp            | 4.2.0   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.3.1   |
| apache-airflow-providers-ssh             | 3.3.0   |
| astronomer-providers                     | 1.13.0  |

## Astro Runtime 7.0.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 4.1.1   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.1.0   |
| apache-airflow-providers-cncf-kubernetes | 5.0.0   |
| apache-airflow-providers-common-sql      | 1.3.1   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.0   |
| apache-airflow-providers-elasticsearch   | 4.3.1   |
| apache-airflow-providers-ftp             | 3.2.0   |
| apache-airflow-providers-google          | 8.6.0   |
| apache-airflow-providers-http            | 4.1.0   |
| apache-airflow-providers-imap            | 3.1.0   |
| apache-airflow-providers-microsoft-azure | 5.0.0   |
| apache-airflow-providers-postgres        | 5.3.1   |
| apache-airflow-providers-redis           | 3.1.0   |
| apache-airflow-providers-sftp            | 4.2.0   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.3.1   |
| apache-airflow-providers-ssh             | 3.3.0   |
| astronomer-providers                     | 1.11.2  |

## Astro Runtime 6.7.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.2.0   |
| apache-airflow-providers-apache-hive     | 6.1.6   |
| apache-airflow-providers-apache-livy     | 3.5.4   |
| apache-airflow-providers-celery          | 3.3.4   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.7.2   |
| apache-airflow-providers-databricks      | 4.5.0   |
| apache-airflow-providers-dbt-cloud       | 3.3.0   |
| apache-airflow-providers-elasticsearch   | 4.5.1   |
| apache-airflow-providers-ftp             | 3.5.2   |
| apache-airflow-providers-google          | 8.12.0  |
| apache-airflow-providers-http            | 4.5.2   |
| apache-airflow-providers-imap            | 3.3.2   |
| apache-airflow-providers-microsoft-azure | 7.0.0   |
| apache-airflow-providers-postgres        | 5.6.1   |
| apache-airflow-providers-redis           | 3.3.1   |
| apache-airflow-providers-sftp            | 4.6.1   |
| apache-airflow-providers-snowflake       | 5.0.1   |
| apache-airflow-providers-sqlite          | 3.4.3   |
| apache-airflow-providers-ssh             | 3.7.3   |
| astronomer-providers                     | 1.16.0  |

## Astro Runtime 6.6.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.0.0   |
| apache-airflow-providers-apache-hive     | 6.1.0   |
| apache-airflow-providers-apache-livy     | 3.5.0   |
| apache-airflow-providers-celery          | 3.2.0   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.5.1   |
| apache-airflow-providers-databricks      | 4.2.0   |
| apache-airflow-providers-dbt-cloud       | 3.2.0   |
| apache-airflow-providers-elasticsearch   | 4.5.0   |
| apache-airflow-providers-ftp             | 3.4.1   |
| apache-airflow-providers-google          | 8.4.0   |
| apache-airflow-providers-http            | 4.4.1   |
| apache-airflow-providers-imap            | 3.2.1   |
| apache-airflow-providers-microsoft-azure | 6.1.1   |
| apache-airflow-providers-postgres        | 5.5.0   |
| apache-airflow-providers-redis           | 3.2.0   |
| apache-airflow-providers-sftp            | 4.3.0   |
| apache-airflow-providers-snowflake       | 4.1.0   |
| apache-airflow-providers-sqlite          | 3.4.1   |
| apache-airflow-providers-ssh             | 3.7.0   |
| astronomer-providers                     | 1.16.0  |

## Astro Runtime 6.5.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.0.0   |
| apache-airflow-providers-apache-hive     | 6.1.0   |
| apache-airflow-providers-apache-livy     | 3.5.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.5.1   |
| apache-airflow-providers-databricks      | 4.2.0   |
| apache-airflow-providers-dbt-cloud       | 3.2.0   |
| apache-airflow-providers-elasticsearch   | 4.2.1   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.4.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 6.1.1   |
| apache-airflow-providers-postgres        | 5.2.2   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.3.0   |
| apache-airflow-providers-snowflake       | 4.1.0   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| apache-airflow-providers-ssh             | 3.7.0   |
| astronomer-providers                     | 1.16.0  |

## Astro Runtime 6.4.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.0.0   |
| apache-airflow-providers-apache-hive     | 5.1.3   |
| apache-airflow-providers-apache-livy     | 3.3.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.3.4   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 3.1.0   |
| apache-airflow-providers-elasticsearch   | 4.2.1   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.4.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.2.1   |
| apache-airflow-providers-postgres        | 5.2.2   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.4   |
| apache-airflow-providers-snowflake       | 4.0.4   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| apache-airflow-providers-ssh             | 3.5.0   |
| astronomer-providers                     | 1.15.1  |

## Astro Runtime 6.3.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.0.0   |
| apache-airflow-providers-apache-hive     | 5.1.2   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.3.3   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 3.0.0   |
| apache-airflow-providers-elasticsearch   | 4.2.1   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.4.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.2.0   |
| apache-airflow-providers-postgres        | 5.2.2   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.2   |
| apache-airflow-providers-snowflake       | 4.0.3   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| apache-airflow-providers-ssh             | 3.4.0   |
| astronomer-providers                     | 1.14.0  |

## Astro Runtime 6.2.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.0.0   |
| apache-airflow-providers-apache-hive     | 5.1.1   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.3.3   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.1   |
| apache-airflow-providers-elasticsearch   | 4.2.1   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.4.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.1.0   |
| apache-airflow-providers-postgres        | 5.2.2   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.1   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| apache-airflow-providers-ssh             | 3.4.0   |
| astronomer-providers                     | 1.14.0  |

## Astro Runtime 6.2.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.0.0   |
| apache-airflow-providers-apache-hive     | 5.1.1   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.3.3   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.1   |
| apache-airflow-providers-elasticsearch   | 4.2.1   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.4.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.1.0   |
| apache-airflow-providers-postgres        | 5.2.2   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.1   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| apache-airflow-providers-ssh             | 3.4.0   |
| astronomer-providers                     | 1.14.0  |

## Astro Runtime 6.1.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.0.0   |
| apache-airflow-providers-apache-hive     | 5.0.0   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.3.1   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.0   |
| apache-airflow-providers-elasticsearch   | 4.2.1   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.4.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.0.1   |
| apache-airflow-providers-postgres        | 5.2.2   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.0   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| apache-airflow-providers-ssh             | 3.3.0   |
| astronomer-providers                     | 1.13.0  |

## Astro Runtime 6.0.4

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.0.0   |
| apache-airflow-providers-apache-hive     | 4.0.1   |
| apache-airflow-providers-apache-livy     | 3.1.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.2.0   |
| apache-airflow-providers-databricks      | 3.3.0   |
| apache-airflow-providers-dbt-cloud       | 2.2.0   |
| apache-airflow-providers-elasticsearch   | 4.2.1   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.4.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.3.0   |
| apache-airflow-providers-postgres        | 5.2.2   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.1.0   |
| apache-airflow-providers-snowflake       | 3.3.0   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| apache-airflow-providers-ssh             | 3.2.0   |
| astronomer-providers                     | 1.11.1  |

## Astro Runtime 6.0.3

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 6.0.0   |
| apache-airflow-providers-apache-hive     | 4.0.1   |
| apache-airflow-providers-apache-livy     | 3.1.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.4.0   |
| apache-airflow-providers-common-sql      | 1.2.0   |
| apache-airflow-providers-databricks      | 3.3.0   |
| apache-airflow-providers-dbt-cloud       | 2.2.0   |
| apache-airflow-providers-elasticsearch   | 4.2.1   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.4.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.3.0   |
| apache-airflow-providers-postgres        | 5.2.2   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.1.0   |
| apache-airflow-providers-snowflake       | 3.3.0   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| apache-airflow-providers-ssh             | 3.2.0   |
| astronomer-providers                     | 1.10.0  |

## Astro Runtime 6.0.2

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.1.0   |
| apache-airflow-providers-apache-hive     | 4.0.0   |
| apache-airflow-providers-apache-livy     | 3.1.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.2.0   |
| apache-airflow-providers-databricks      | 3.2.0   |
| apache-airflow-providers-dbt-cloud       | 2.1.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.2.0   |
| apache-airflow-providers-postgres        | 5.2.1   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.0.0   |
| apache-airflow-providers-snowflake       | 3.2.0   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| apache-airflow-providers-ssh             | 3.1.0   |
| astronomer-providers                     | 1.10.0  |

## Astro Runtime 6.0.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.1.0   |
| apache-airflow-providers-apache-hive     | 4.0.0   |
| apache-airflow-providers-apache-livy     | 3.1.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.2.0   |
| apache-airflow-providers-databricks      | 3.2.0   |
| apache-airflow-providers-dbt-cloud       | 2.1.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.2.0   |
| apache-airflow-providers-postgres        | 5.2.1   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-snowflake       | 3.2.0   |
| apache-airflow-providers-sqlite          | 3.2.1   |
| astronomer-providers                     | 1.9.0   |

## Astro Runtime 6.0.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 4.0.0   |
| apache-airflow-providers-apache-livy     | 3.1.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.1.0   |
| apache-airflow-providers-databricks      | 3.2.0   |
| apache-airflow-providers-dbt-cloud       | 2.1.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.2.0   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-snowflake       | 3.2.0   |
| apache-airflow-providers-sqlite          | 3.2.0   |
| astronomer-providers                     | 1.9.0   |

## Astro Runtime 5.4.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 5.1.3   |
| apache-airflow-providers-apache-livy     | 3.3.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.3.4   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 3.1.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.2.1   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.4   |
| apache-airflow-providers-snowflake       | 4.0.4   |
| apache-airflow-providers-sqlite          | 3.2.0   |
| apache-airflow-providers-ssh             | 3.5.0   |
| astronomer-providers                     | 1.15.1  |

## Astro Runtime 5.3.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 5.1.2   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.3.3   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 3.0.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.2.0   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.2   |
| apache-airflow-providers-snowflake       | 4.0.3   |
| apache-airflow-providers-sqlite          | 3.2.0   |
| apache-airflow-providers-ssh             | 3.4.0   |
| astronomer-providers                     | 1.14.0  |

## Astro Runtime 5.2.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 5.1.1   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.3.3   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.1   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.1.0   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.1   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.2.0   |
| apache-airflow-providers-ssh             | 3.4.0   |
| astronomer-providers                     | 1.14.0  |

## Astro Runtime 5.2.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 5.1.1   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.3.3   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.1   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.1.0   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.1   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.2.0   |
| apache-airflow-providers-ssh             | 3.4.0   |
| astronomer-providers                     | 1.14.0  |

## Astro Runtime 5.1.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 5.0.0   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.3.1   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.0.1   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.0   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.2.0   |
| apache-airflow-providers-ssh             | 3.3.0   |
| astronomer-providers                     | 1.13.0  |

## Astro Runtime 5.0.13

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 4.1.1   |
| apache-airflow-providers-apache-livy     | 3.2.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.3.1   |
| apache-airflow-providers-databricks      | 4.0.0   |
| apache-airflow-providers-dbt-cloud       | 2.3.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 5.0.0   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.2.0   |
| apache-airflow-providers-snowflake       | 4.0.2   |
| apache-airflow-providers-sqlite          | 3.2.0   |
| apache-airflow-providers-ssh             | 3.3.0   |
| astronomer-providers                     | 1.10.0  |

## Astro Runtime 5.0.10

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 4.0.1   |
| apache-airflow-providers-apache-livy     | 3.1.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.2.0   |
| apache-airflow-providers-databricks      | 3.3.0   |
| apache-airflow-providers-dbt-cloud       | 2.2.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.3.0   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-sftp            | 4.1.0   |
| apache-airflow-providers-snowflake       | 3.3.0   |
| apache-airflow-providers-sqlite          | 3.2.0   |
| apache-airflow-providers-ssh             | 3.2.0   |
| astronomer-providers                     | 1.10.0  |

## Astro Runtime 5.0.9

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 4.0.0   |
| apache-airflow-providers-apache-livy     | 3.1.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.1.0   |
| apache-airflow-providers-databricks      | 3.2.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.2.0   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-snowflake       | 3.2.0   |
| apache-airflow-providers-sqlite          | 3.2.0   |

## Astro Runtime 5.0.8

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 5.0.0   |
| apache-airflow-providers-apache-hive     | 4.0.0   |
| apache-airflow-providers-apache-livy     | 3.1.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.3.0   |
| apache-airflow-providers-common-sql      | 1.1.0   |
| apache-airflow-providers-databricks      | 3.2.0   |
| apache-airflow-providers-elasticsearch   | 4.2.0   |
| apache-airflow-providers-ftp             | 3.1.0   |
| apache-airflow-providers-google          | 8.3.0   |
| apache-airflow-providers-http            | 4.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.2.0   |
| apache-airflow-providers-postgres        | 5.2.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-snowflake       | 3.2.0   |
| apache-airflow-providers-sqlite          | 3.2.0   |

## Astro Runtime 5.0.7

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 4.1.0   |
| apache-airflow-providers-apache-hive     | 4.0.0   |
| apache-airflow-providers-apache-livy     | 3.1.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.1.0   |
| apache-airflow-providers-common-sql      | 1.0.0   |
| apache-airflow-providers-databricks      | 3.1.0   |
| apache-airflow-providers-elasticsearch   | 4.0.0   |
| apache-airflow-providers-ftp             | 3.0.0   |
| apache-airflow-providers-google          | 8.1.0   |
| apache-airflow-providers-http            | 3.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.2.0   |
| apache-airflow-providers-postgres        | 5.0.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-snowflake       | 3.1.0   |
| apache-airflow-providers-sqlite          | 3.0.0   |

## Astro Runtime 5.0.6

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 4.0.0   |
| apache-airflow-providers-apache-hive     | 3.0.0   |
| apache-airflow-providers-apache-livy     | 3.0.0   |
| apache-airflow-providers-celery          | 3.0.0   |
| apache-airflow-providers-cncf-kubernetes | 4.1.0   |
| apache-airflow-providers-databricks      | 3.0.0   |
| apache-airflow-providers-elasticsearch   | 4.0.0   |
| apache-airflow-providers-ftp             | 3.0.0   |
| apache-airflow-providers-google          | 8.1.0   |
| apache-airflow-providers-http            | 3.0.0   |
| apache-airflow-providers-imap            | 3.0.0   |
| apache-airflow-providers-microsoft-azure | 4.0.0   |
| apache-airflow-providers-postgres        | 5.0.0   |
| apache-airflow-providers-redis           | 3.0.0   |
| apache-airflow-providers-snowflake       | 3.0.0   |
| apache-airflow-providers-sqlite          | 3.0.0   |

## Astro Runtime 5.0.5

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.4.0   |
| apache-airflow-providers-apache-hive     | 3.0.0   |
| apache-airflow-providers-apache-livy     | 3.0.0   |
| apache-airflow-providers-celery          | 2.1.4   |
| apache-airflow-providers-cncf-kubernetes | 4.0.2   |
| apache-airflow-providers-databricks      | 3.0.0   |
| apache-airflow-providers-elasticsearch   | 3.0.3   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 7.0.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-microsoft-azure | 4.0.0   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 3.0.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 5.0.4

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.4.0   |
| apache-airflow-providers-apache-hive     | 3.0.0   |
| apache-airflow-providers-apache-livy     | 3.0.0   |
| apache-airflow-providers-celery          | 2.1.4   |
| apache-airflow-providers-cncf-kubernetes | 4.0.2   |
| apache-airflow-providers-databricks      | 3.0.0   |
| apache-airflow-providers-elasticsearch   | 3.0.3   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 7.0.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-microsoft-azure | 4.0.0   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 3.0.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 5.0.3

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.4.0   |
| apache-airflow-providers-apache-hive     | 2.3.3   |
| apache-airflow-providers-apache-livy     | 2.2.3   |
| apache-airflow-providers-celery          | 2.1.4   |
| apache-airflow-providers-cncf-kubernetes | 4.0.2   |
| apache-airflow-providers-databricks      | 2.7.0   |
| apache-airflow-providers-elasticsearch   | 3.0.3   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.8.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-microsoft-azure | 3.9.0   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 2.7.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 5.0.2

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.4.0   |
| apache-airflow-providers-apache-hive     | 2.3.3   |
| apache-airflow-providers-apache-livy     | 2.2.3   |
| apache-airflow-providers-celery          | 2.1.4   |
| apache-airflow-providers-cncf-kubernetes | 4.0.2   |
| apache-airflow-providers-databricks      | 2.7.0   |
| apache-airflow-providers-elasticsearch   | 3.0.3   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.8.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-microsoft-azure | 3.9.0   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 2.7.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 5.0.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.3.0   |
| apache-airflow-providers-apache-livy     | 2.2.3   |
| apache-airflow-providers-celery          | 2.1.4   |
| apache-airflow-providers-cncf-kubernetes | 4.0.1   |
| apache-airflow-providers-databricks      | 2.6.0   |
| apache-airflow-providers-elasticsearch   | 3.0.3   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.8.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 2.6.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 5.0.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.3.0   |
| apache-airflow-providers-celery          | 2.1.4   |
| apache-airflow-providers-cncf-kubernetes | 4.0.1   |
| apache-airflow-providers-databricks      | 2.6.0   |
| apache-airflow-providers-elasticsearch   | 3.0.3   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.8.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 2.6.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 4.2.9

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.2.0   |
| apache-airflow-providers-celery          | 2.1.3   |
| apache-airflow-providers-cncf-kubernetes | 3.0.0   |
| apache-airflow-providers-common-sql      | 1.3.1   |
| apache-airflow-providers-databricks      | 3.3.0   |
| apache-airflow-providers-elasticsearch   | 2.2.0   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.7.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 3.3.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 4.2.7

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.2.0   |
| apache-airflow-providers-celery          | 2.1.3   |
| apache-airflow-providers-cncf-kubernetes | 3.0.0   |
| apache-airflow-providers-common-sql      | 1.2.0   |
| apache-airflow-providers-databricks      | 3.3.0   |
| apache-airflow-providers-elasticsearch   | 2.2.0   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.7.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 3.3.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 4.2.6

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.2.0   |
| apache-airflow-providers-celery          | 2.1.3   |
| apache-airflow-providers-cncf-kubernetes | 3.0.0   |
| apache-airflow-providers-databricks      | 2.5.0   |
| apache-airflow-providers-elasticsearch   | 2.2.0   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.7.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 2.6.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 4.2.5

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.2.0   |
| apache-airflow-providers-celery          | 2.1.3   |
| apache-airflow-providers-cncf-kubernetes | 3.0.0   |
| apache-airflow-providers-databricks      | 2.5.0   |
| apache-airflow-providers-elasticsearch   | 2.2.0   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.8.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 2.6.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 4.2.4

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.2.0   |
| apache-airflow-providers-celery          | 2.1.3   |
| apache-airflow-providers-cncf-kubernetes | 3.0.0   |
| apache-airflow-providers-databricks      | 2.5.0   |
| apache-airflow-providers-elasticsearch   | 3.0.2   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.7.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 2.6.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 4.2.3

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.2.0   |
| apache-airflow-providers-celery          | 2.1.3   |
| apache-airflow-providers-cncf-kubernetes | 3.0.0   |
| apache-airflow-providers-databricks      | 2.5.0   |
| apache-airflow-providers-elasticsearch   | 3.0.2   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.7.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 2.6.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 4.2.2

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.2.0   |
| apache-airflow-providers-celery          | 2.1.3   |
| apache-airflow-providers-cncf-kubernetes | 3.0.0   |
| apache-airflow-providers-databricks      | 2.5.0   |
| apache-airflow-providers-elasticsearch   | 3.0.2   |
| apache-airflow-providers-ftp             | 2.1.2   |
| apache-airflow-providers-google          | 6.7.0   |
| apache-airflow-providers-http            | 2.1.2   |
| apache-airflow-providers-imap            | 2.2.3   |
| apache-airflow-providers-postgres        | 4.1.0   |
| apache-airflow-providers-redis           | 2.0.4   |
| apache-airflow-providers-snowflake       | 2.6.0   |
| apache-airflow-providers-sqlite          | 2.1.3   |

## Astro Runtime 4.2.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.0.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 3.0.2   |
| apache-airflow-providers-databricks      | 2.5.0   |
| apache-airflow-providers-elasticsearch   | 2.2.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-google          | 6.7.0   |
| apache-airflow-providers-http            | 2.0.3   |
| apache-airflow-providers-imap            | 2.2.0   |
| apache-airflow-providers-postgres        | 3.0.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-snowflake       | 2.6.0   |
| apache-airflow-providers-sqlite          | 2.1.0   |

## Astro Runtime 4.2.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.0.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 3.0.2   |
| apache-airflow-providers-databricks      | 2.2.0   |
| apache-airflow-providers-elasticsearch   | 2.2.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-google          | 6.4.0   |
| apache-airflow-providers-http            | 2.0.3   |
| apache-airflow-providers-imap            | 2.2.0   |
| apache-airflow-providers-postgres        | 3.0.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-snowflake       | 2.5.0   |
| apache-airflow-providers-sqlite          | 2.1.0   |

## Astro Runtime 4.1.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 3.0.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 3.0.2   |
| apache-airflow-providers-databricks      | 2.0.2   |
| apache-airflow-providers-elasticsearch   | 2.2.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.3   |
| apache-airflow-providers-imap            | 2.2.0   |
| apache-airflow-providers-postgres        | 3.0.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-snowflake       | 2.5.0   |
| apache-airflow-providers-sqlite          | 2.1.0   |

## Astro Runtime 4.0.11

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.4.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 3.0.2   |
| apache-airflow-providers-databricks      | 2.0.2   |
| apache-airflow-providers-elasticsearch   | 2.1.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.4.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-snowflake       | 2.5.0   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.10

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.4.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 3.0.1   |
| apache-airflow-providers-databricks      | 2.0.2   |
| apache-airflow-providers-elasticsearch   | 2.1.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.4.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-snowflake       | 2.4.0   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.9

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.4.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.2.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.4.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.8

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.4.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.2.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.4.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.7

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.4.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.1.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.3.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.6

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.4.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.1.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.3.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.5

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.4.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.1.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.3.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.4

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.4.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.1.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.3.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.3

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.3.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.1.0   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.3.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.2

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.3.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.0.3   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.3.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.3.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.0.3   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.3.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 4.0.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 2.3.0   |
| apache-airflow-providers-celery          | 2.1.0   |
| apache-airflow-providers-cncf-kubernetes | 2.0.3   |
| apache-airflow-providers-ftp             | 2.0.1   |
| apache-airflow-providers-http            | 2.0.1   |
| apache-airflow-providers-imap            | 2.0.1   |
| apache-airflow-providers-postgres        | 2.3.0   |
| apache-airflow-providers-redis           | 2.0.1   |
| apache-airflow-providers-sqlite          | 2.0.1   |

## Astro Runtime 3.0.4

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 1!2.0.0 |
| apache-airflow-providers-celery          | 1!2.0.0 |
| apache-airflow-providers-cncf-kubernetes | 1!2.0.0 |
| apache-airflow-providers-ftp             | 1!2.0.0 |
| apache-airflow-providers-imap            | 1!2.0.0 |
| apache-airflow-providers-postgres        | 1!2.0.0 |
| apache-airflow-providers-redis           | 1!2.0.0 |
| apache-airflow-providers-sqlite          | 1!2.0.0 |

## Astro Runtime 3.0.3

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 1!2.0.0 |
| apache-airflow-providers-celery          | 1!2.0.0 |
| apache-airflow-providers-cncf-kubernetes | 1!2.0.0 |
| apache-airflow-providers-ftp             | 1!2.0.0 |
| apache-airflow-providers-imap            | 1!2.0.0 |
| apache-airflow-providers-postgres        | 1!2.0.0 |
| apache-airflow-providers-redis           | 1!2.0.0 |
| apache-airflow-providers-sqlite          | 1!2.0.0 |

## Astro Runtime 3.0.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 1!2.0.0 |
| apache-airflow-providers-celery          | 1!2.0.0 |
| apache-airflow-providers-cncf-kubernetes | 1!2.0.0 |
| apache-airflow-providers-ftp             | 1!2.0.0 |
| apache-airflow-providers-imap            | 1!2.0.0 |
| apache-airflow-providers-postgres        | 1!2.0.0 |
| apache-airflow-providers-redis           | 1!2.0.0 |
| apache-airflow-providers-sqlite          | 1!2.0.0 |

## Astro Runtime 3.0.0

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 1!2.0.0 |
| apache-airflow-providers-celery          | 1!2.0.0 |
| apache-airflow-providers-cncf-kubernetes | 1!2.0.0 |
| apache-airflow-providers-ftp             | 1!2.0.0 |
| apache-airflow-providers-imap            | 1!2.0.0 |
| apache-airflow-providers-postgres        | 1!2.0.0 |
| apache-airflow-providers-redis           | 1!2.0.0 |
| apache-airflow-providers-sqlite          | 1!2.0.0 |

## Astro Runtime 2.1.1

| Package Name                             | Version |
| :--------------------------------------- | :------ |
| apache-airflow-providers-amazon          | 1!2.0.0 |
| apache-airflow-providers-celery          | 1!2.0.0 |
| apache-airflow-providers-cncf-kubernetes | 1!2.0.0 |
| apache-airflow-providers-ftp             | 1!2.0.0 |
| apache-airflow-providers-imap            | 1!2.0.0 |
| apache-airflow-providers-postgres        | 1!2.0.0 |
| apache-airflow-providers-redis           | 1!2.0.0 |
| apache-airflow-providers-sqlite          | 1!2.0.0 |
