---
sidebar_label: "astro config set"
title: "astro config set"
id: astro-config-set
description: Update Astro CLI configurations.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::info

The behavior and format of this command are the same for both Astro and Software.

:::

Update any part of the current configuration of your Astro project as defined in the `.astro/config.yaml` file. The configuration in this file contains details about how your project runs in a local [Apache Airflow®](https://airflow.apache.org/) environment, including your Postgres username and password, your Webserver port, and your project name.

## Usage

Within your Astro project directory, run:

```sh
astro config set <configuration> <value>
```

## Options

| Option           | Description                               | Possible Values |
| ---------------- | ----------------------------------------- | --------------- |
| `-g`, `--global` | Modify global CLI configuration settings. See [Set global configurations](configure-cli.md#set-global-configurations). | None            |

For a list of available configurations, see [Configure the CLI](configure-cli.md).

## Examples

```sh
## Set your webserver port to 8081
$ astro config set webserver.port 8081
```

## Related Commands

- [astro config get](cli/astro-config-get.md)
