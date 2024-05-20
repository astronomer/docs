---
sidebar_label: "astro organization role list"
title: "astro organization role list"
id: astro-organization-role-list
description: Reference documentation for the astro organization role list command.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---


:::cliastroonly
:::

View a list of all roles in an Organization.

## Usage

Run `astro organization role list` to view a list of the custom and default user roles in your Organization and their IDs. By default, only custom roles are displayed. To create a custom role, see [Create and assign custom Deployment roles](customize-deployment-roles.md)

If you want to view the Astro-defined user roles and their IDs, you need to add the `--include-default-roles` flag. For example,

```sh

astro organization role list --include-default-roles

```

## Options

| Option                  | Description                                                                      | Possible Values                  |
| ----------------------- | -------------------------------------------------------------------------------- | -------------------------------- |
| `--include-default-roles` | Display the Astro-defined [user roles](user-permissions.md) in the organization. | Any of the available user roles. |

## Output

| Output        | Description                     | Data Type |
| ------------- | ------------------------------- | --------- |
| `NAME`        | The name of the role.           | String    |
| `ID`          | The custom role ID.             | String    |
| `DESCRIPTION` | A description of the user role. | String    |

