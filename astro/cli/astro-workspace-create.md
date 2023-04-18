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

| Option                | Description                                          | Valid Values                                                                     |
| --------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| `--description`             | The description for the Workspace. | Any string                                                                  |
| `--enforce-ci-cd`| Determines whether users are required to deploy code to Deployments on a Workspace through a Workspace API token or Deployment API key.                   | `ON` or `OFF` |
| `--name`|The name for the Workspace.                  | Any string |


## Examples

```sh
$ astro workspace create --name "My Deployment" --enforce-ci-cd ON
```