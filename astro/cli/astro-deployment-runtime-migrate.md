---
sidebar_label: "astro deployment runtime migrate"
title: "astro deployment runtime migrate"
id: astro-deployment-runtime-migrate
description: Migrate a Software Deployment to Astro Runtime.
hide_table_of_contents: true
---

:::info 

This command is available only if you're authenticated to an Astronomer Software installation. 

:::

Initializes the Runtime migration upgrade process on any Deployment on Astronomer Software.

## Usage

Run `astro deployment runtime migrate --deployment-id=<deployment-id>` to initialize the Runtime upgrade process. To finalize the Runtime upgrade process, complete all of the steps in [Migrate to Astro Runtime](https://docs.astronomer.io/software/migrate-to-runtime).

The Astro CLI lists only the available Runtime versions that are later than the version currently specified in your `Dockerfile`.

## Options

| Option                        | Description                                                                                                                    | Possible values
| --------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| `--cancel` | Cancel the migration                                                                | None | 
| `--deployment-id` (_Required_)           | The ID of the Deployment which you want to migrate to Runtime. To find your Deployment ID, run `astro deployment list`.     | Any Deployment ID |


## Related commands 

- [`astro deployment airflow upgrade`](astro-deployment-airflow-upgrade.md)
- [`astro deployment runtime upgrade`](astro-deployment-runtime-upgrade.md)