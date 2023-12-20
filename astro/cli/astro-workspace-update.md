---
sidebar_label: "astro workspace update"
title: "astro workspace update"
id: astro-workspace-update
description: Update an Astro Workspace. 
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

Update an Astro Workspace. 

## Usage

```sh
astro workspace update <workspace-id> <options>
```

You can find a Workspace's ID by running `astro workspace list`, or by opening your Workspace and going to **Workspace Settings** > **General** in the Cloud UI. If you do not provide a Workspace ID, the CLI prompts you to pick from a list of Workspaces that you belong to in your current Organization. 

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--description`   | The description for the Workspace.                                                                                                      | Any string    |
| `--enforce-ci-cd` | Determines whether users are required to use a Workspace API token or Deployment API key to deploy code. | `ON` or `OFF` |
| `--name`          | The name for the Workspace.                                                                                                             | Any string    |


## Examples

```sh
$ astro workspace update --name "My Deployment" --enforce-ci-cd OFF
```

## Related commands

- [`astro workspace create`](cli/astro-workspace-create.md)
- [`astro deployment update`](cli/astro-deployment-update.md)
