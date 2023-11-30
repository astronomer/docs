---
sidebar_label: "astro organization token create"
title: "astro organization token create"
id: astro-organization-token-create
description: Create an Organization API token.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

Create an Organization API token.

## Usage

```sh
astro organization token create
```

## Options

| Option           | Description                                                                | Valid Values                                                                                             |
| ---------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `--clean-output` | Print only the token as output. Use this flag in automated workflows.      | None.                                                                                                     |
| `--description`  | The description for the token.                                              | Any string surrounded by quotations.                                                                      |
| `--expiration`   | The expiration date for the token. By default there is no expiration date. | Any integer between 1 and 3650, used to represent days.                                                   |
| `--name`         | The name for the token.                                                    | Any string surrounded by quotations.                                                                      |
| `--role`         | The token's role in the Organization.                                      | Possible values are either `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`. |

## Examples

```sh
astro organization token create --name "My Org Owner API token" --role ORGANIZATION OWNER
```

## Related commands

- [astro organization token update](cli/astro-organization-token-update.md)
- [astro organization token rotate](cli/astro-organization-token-rotate.md)
- [astro organization switch](cli/astro-organization-switch.md)