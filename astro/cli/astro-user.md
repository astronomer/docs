---
sidebar_label: "astro user"
title: "astro user"
id: astro-user
description: Reference documentation for astro user commands.
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

Manage users in your current Astro Organization.

## Usage

This command includes three subcommands:

- `astro user list`: List all users in your Organization
- `astro user invite`: Invite a new user to your Astronomer Organization. The CLI prompts you for the user's email.
- `astro user update`: Update a user's Organization-level role.

## Options 

| Option    | Description                                                  | Possible Values                                                                                                                             |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `<email>` | Specify the email for the user you want to invite or update. Use only with `astro user update` and `astro user invite`. | Any valid email                                                                                                                             |
| `--role`  | The user's role in the Organization. Use only with `astro user update` and `astro user invite`.                         | Possible values are either `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`.   Default is `ORGANIZATION_MEMBER` |

## Examples

```sh
# Invite a user to your Organization
astro user invite user@cosmicenergy.org --role ORGANIZATION_BILLING_ADMIN

# Update a user's role. The CLI prompts you for the user's email
astro user update --role ORGANIZATION_MEMBER
```

</TabItem>
<TabItem value="software">

Create a new user profile on Astronomer Software. 

## Usage 

```sh
astro user invite
```

## Options 

| Option              | Description                                                                                   | Possible Values                                 |
| ------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `-e`, `--email` | The email for the user           | Any valid email address |
| `-p`, `--password` | The password for the user           | Any string |

</TabItem>
</Tabs>


## Related Commands

- [`astro login`](cli/astro-login.md)
