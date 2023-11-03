---
sidebar_label: "astro deployment runtime upgrade"
title: "astro deployment runtime upgrade"
id: astro-deployment-runtime-upgrade
description: Upgrade a Deployment (Software only)
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

:::info 

This command is available only if you're authenticated to an Astronomer Software installation. 

:::

Initializes the Runtime version upgrade process on any Deployment on Astronomer Software.

## Usage

Run `astro deployment runtime upgrade --deployment-id=<deployment-id>` to initialize the Runtime upgrade process. To finalize the Runtime upgrade process, complete all of the steps in [Upgrade Apache Airflow on Astronomer Software](https://docs.astronomer.io/software/manage-airflow-versions).

## Options

| Option                         | Description                                                                                                              | Possible values               |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------- |
| `--cancel`                     | Cancel the upgrade                                                                                                       | None                          |
| `--deployment-id` (_Required_) | The ID of the Deployment for which you want to upgrade Runtime. Run `astro deployment list ` to retrieve the Deployment ID. | Any Deployment ID             |
| `--desired-runtime-version`    | The Runtime version you're upgrading to. For example, `2.2.0`.                                                          | Any supported Runtime version |



## Examples 

```
# Upgrade to Runtime 6.0.0
$ astro deployment runtime --deployment-id telescopic-sky-4599 --desired-runtime-version 6.0.0
```

## Related commands 

- [`astro deployment airflow upgrade`](astro-deployment-airflow-upgrade.md)
- [`astro deployment runtime migrate`](astro-deployment-runtime-migrate.md)