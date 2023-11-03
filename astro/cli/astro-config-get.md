---
sidebar_label: "astro config get"
title: "astro config get"
id: astro-config-get
description: View current Astro CLI configurations.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

View the current configuration of your Astro project as defined in the `.astro/config.yaml` file. The configuration in this file contains details about how your project runs in a local Airflow environment, including your Postgres username and password, your Webserver port, and your project name.

## Usage

Within your Astro project directory, run:

```sh
astro config get <option>
```

## Options

For a list of available configurations, see [Configure the CLI](configure-cli.md).

## Examples

```sh
## View the username for your project's postgres user
$ astro config get postgres.user
```

## Related Commands

- [astro config set](cli/astro-config-set.md)
