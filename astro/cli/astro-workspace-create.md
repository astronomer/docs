---
sidebar_label: "astro workspace create"
title: "astro workspace create"
id: astro-workspace-create
description: Reference documentation for astro workspace create.
hide_table_of_contents: true
---

Create an Astro Workspace. 

## Usage

```sh
astro workspace create <options>
```


## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--description`   | The description for the Workspace.                                                                                                      | Any string    |
| `--enforce-ci-cd` | Determines whether users are required to use a Workspace API token or Deployment API key to deploy code.  | `ON` or `OFF` |
| `--name`          | The name for the Workspace.                                                                                                             | Any string    |


## Examples

```sh
$ astro workspace create --name "My Deployment" --enforce-ci-cd ON
```

## Related commands

- [`astro workspace update`](cli/astro-workspace-update.md)
- [`astro workspace delete`](cli/astro-workspace-delete.md)
- [`astro workspace user update`](cli/astro-workspace-user-update.md)