---
sidebar_label: "astro dev bash"
title: "astro dev bash"
id: astro-dev-bash
description: Run a bash command in an Airflow component's Docker container.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

Run a bash command in a locally running Docker container for an Airflow component. This command is equivalent to running `docker exec -it <container-id>`.

## Usage

In a locally running Astro project, run:

```sh
astro dev bash
```

By default, the command execs into the scheduler container and prompts you to run a bash command. To run a command in a different container, you have to specify a different container flag.

## Options

| Option              | Description                                           | Possible Values |
| ------------------- | ----------------------------------------------------- | --------------- |
| `-p`, `--postgres`  | Run a bash command in the metadata database container | None            |
| `-s`,`--scheduler`  | Run a bash command in the scheduler container         | None            |
| `-t`, `--triggerer` | Run a bash command in the triggerer container         | None            |
| `-w`, `--webserver` | Run a bash command in the webserver container         | None            |

## Examples

```sh
$ astro dev bash --webserver
$ ls -al
# View all files in the webserver container

$ astro dev bash --scheduler
$ pip-freeze | grep pymongo
# Check the version of the pymongo package running in the scheduler
```

## Related Commands

- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev run`](cli/astro-dev-run.md)
- [`astro dev ps`](cli/astro-dev-ps.md)
