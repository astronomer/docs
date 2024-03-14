---
sidebar_label: "astro workspace create"
title: "astro workspace create"
id: astro-workspace-create
description: Create an Astro Workspace.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change product contexts.

:::

Create a Workspace.

<Tabs
    defaultValue="astro"
    values={[
        {label: 'Astro', value: 'astro'},
        {label: 'Software', value: 'software'},
    ]}>
<TabItem value="astro">

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

</TabItem>
<TabItem value="software">

## Usage

```sh
astro workspace create <options>
```

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--description`   | The description for the Workspace.                                                                                                      | Any string    |
| `--label`          | The label for the Workspace.                                                                                                             | Any string    |

## Examples

```sh
$ astro workspace create --label "My Deployment" --description "My new Deployment"
```

## Related commands

- [`astro workspace update`](cli/astro-workspace-update.md)
- [`astro workspace delete`](cli/astro-workspace-delete.md)
- [`astro workspace user update`](cli/astro-workspace-user-update.md)

</TabItem>
</Tabs>