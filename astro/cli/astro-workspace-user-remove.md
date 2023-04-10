---
sidebar_label: "astro workspace user remove"
title: "astro workspace user remove"
id: astro-workspace-user-remove
description: Reference documentation for astro workspace.
hide_table_of_contents: true
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info  

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change product contexts. 

:::

<Tabs
    defaultValue="astro"
    values={[
        {label: 'Astro', value: 'astro'},
        {label: 'Software', value: 'software'},
    ]}>
<TabItem value="astro">

Remove a user from your current Workspace. 

## Usage

```sh
astro workspace user remove
```

## Options

| Option    | Description                                | Possible Values |
| --------- | ------------------------------------------ | --------------- |
| `<email>` | The email for the user you want to remove. | Any valid email |

## Related commands

- [`astro workspace user add`](cli/astro-workspace-user-add.md)
- [`astro organization user update`](cli/astro-organization-user-update.md)

</TabItem>
<TabItem value="software">

Removes a user from your current Workspace.

## Usage

```sh
astro workspace user remove --email <user-email-address>
```

## Options

| Option                 | Description       | Possible Values         |
| ---------------------- | ----------------- | ----------------------- |
| `--email` (_Required_) | The user's email. | Any valid email address |


</TabItem>
</Tabs>
