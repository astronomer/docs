---
sidebar_label: "astro workspace user list"
title: "astro workspace user list"
id: astro-workspace-user-list
description: Reference documentation for astro workspace user list.
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

Outputs a list of all users with access to your current Workspace.

## Usage

```sh
astro workspace user list
```

Outputs a list of all users with access to your current Workspace.

</TabItem>
<TabItem value="software">

## Usage

```sh
astro workspace user list
```

## Options

| Option           | Description                                                                                                                                             | Possible Values        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `--workspace-id` | The Workspace that you're searching in. Specify this flag if you want to search for users in a Workspace that is different than your current Workspace. | Any valid Workspace ID |
| `--email`        | The email for the user you're searching for.                                                                                                            | Any string             |
| `--name`         | The name of the user to search for.                                                                                                                     | Any string             |
| `--paginated `   | Paginate the list of users. If `--page-size` is not specified, the default page size is 20.                                                             | None                   |
| `--page-size`    | The page size for paginated lists.                                                                                                                      | Any integer            |


## Related documentation

- [Manage Workspaces and Deployments on Astronomer](https://docs.astronomer.io/software/manage-workspaces)
- [Manage User Permissions on Astronomer](https://docs.astronomer.io/software/workspace-permissions)

</TabItem>
</Tabs>