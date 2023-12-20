---
sidebar_label: "astro deployment airflow upgrade"
title: "astro deployment airflow upgrade"
id: astro-deployment-airflow-upgrade
description: Upgrade Airflow (Software only).
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

:::info 

This command is available only if you're authenticated to an Astronomer Software installation. 

:::

Initializes the Airflow version upgrade process on any Airflow Deployment on Astronomer. See [Upgrade Airflow on Astronomer Software](https://docs.astronomer.io/software/manage-airflow-versions)

## Usage

Run `astro deployment airflow upgrade --deployment-id` to initialize the Airflow upgrade process. To finalize the Airflow upgrade process, complete all of the steps in [Upgrade Airflow on Astronomer Software](https://docs.astronomer.io/software/manage-airflow-versions).

If you do not specify `--desired-airflow-version`, this command creates a list of available Airflow versions that you can select. The Astro CLI lists only the available Airflow versions that are later than the version currently specified in your `Dockerfile`.

## Options

| Option                        | Description                                                                                                                    | Possible values
| --------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| `--cancel` | Cancel the upgrade                                                                | None | 
| `--deployment-id`           | The ID of the Deployment that you want to upgrade the Airflow version. Run `astro deployment list` to retrieve your Deployment ID     | Any Deployment ID |
| `--desired-airflow-version` | The Airflow version you're upgrading to. For example, `2.2.0`                                                                | Any supported Airflow version | 



## Examples 

```sh
# Upgrade to Airflow 2.4 
$ astro deployment airflow --deployment-id telescopic-sky-4599 --desired-airflow-version 2.2.0
```

## Related commands 

- [`astro deployment runtime upgrade`](astro-deployment-runtime-upgrade.md)
- [`astro deployment runtime migrate`](astro-deployment-runtime-migrate.md)