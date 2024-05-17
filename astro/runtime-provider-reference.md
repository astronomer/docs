---
sidebar_label: 'Provider package reference'
title: 'Astro Runtime provider package reference'
id: runtime-provider-reference
description: View the provider packages and versions included in each release of Astro Runtime
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This page is a reference of the provider packages included in each release of Astro Runtime, starting with Astro Runtime 11.3.0.

:::info

To find the version of a provider package installed in an Astro Runtime image not listed on this page, run:

```sh
docker run --rm <runtime-image> pip freeze | grep <provider>
```

For example, to find the version of Celery, run the following command:

```sh
docker run --rm quay.io/astronomer/astro-runtime:11.0.0 | grep apache-airflow-providers-celery
```

:::

## Astro Runtime 11.3.0

<Tabs
    groupid="astro-runtime-1130"
    defaultValue="standard"
    values={[
        {label: 'Standard', value: 'standard'},
        {label: 'Slim', value: 'slim'},
    ]}>
<TabItem value="standard">

| package_name                             | version   |
|:-----------------------------------------|:----------|
| apache-airflow-providers-amazon          | 8.20.0    |
| apache-airflow-providers-celery          | 3.7.0     |
| apache-airflow-providers-cncf-kubernetes | 8.0.1     |
| apache-airflow-providers-common-io       | 1.3.1     |
| apache-airflow-providers-common-sql      | 1.13.0    |
| apache-airflow-providers-datadog         | 3.6.0     |
| apache-airflow-providers-elasticsearch   | 5.4.0     |
| apache-airflow-providers-fab             | 1.1.0     |
| apache-airflow-providers-ftp             | 3.9.0     |
| apache-airflow-providers-google          | 10.17.0   |
| apache-airflow-providers-http            | 4.11.0    |
| apache-airflow-providers-imap            | 3.6.0     |
| apache-airflow-providers-microsoft-azure | 9.0.1     |
| apache-airflow-providers-mysql           | 5.6.0     |
| apache-airflow-providers-openlineage     | 1.7.1     |
| apache-airflow-providers-postgres        | 5.11.0    |
| apache-airflow-providers-redis           | 3.7.0     |
| apache-airflow-providers-smtp            | 1.7.0     |
| apache-airflow-providers-sqlite          | 3.8.0     |
| astro-sdk-python                         | 1.8.0     |
| astronomer-providers                     | 1.19.0    |
| astronomer-providers-logging             | 1.4.7     |

</TabItem>
<TabItem value="slim">

| package_name                           | version   |
|:---------------------------------------|:----------|
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
