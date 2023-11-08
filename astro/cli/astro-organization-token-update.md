---
sidebar_label: "astro organization token update"
title: "astro organization token update"
id: astro-organization-token-update
description: Update an Organization API token.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

Update an Organization API token.

## Usage

```sh
astro organization token update <flags>
```

## Options

| Option            | Description                                                                                                                             | Valid Values  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `--clean-output`   | Print only the token as output. Use this flag in automated workflows.                                                                                                      | None.   |
| `--description` | The description for the token. | Any string surrounded by quotations. |
| `--expiration` | The expiration date for the token. By default there is no expiration date. | Any integer between 1 and 3650, used to represent days. |
| `--name` | The current name for the token. | Any string surrounded by quotations. |
| `--new-name` | The updated name for the token. | Any string surrounded by quotations. |
| `--role`         | The token's role in the Organization.                                      | Possible values are either `ORGANIZATION_MEMBER`, `ORGANIZATION_BILLING_ADMIN`, or `ORGANIZATION_OWNER`. |

## Examples

```sh
astro organization token update --new-name "My updated API token" --role ORGANIZATION_MEMBER
```

## Related commands

- [astro organization token rotate](cli/astro-organization-token-rotate.md)
- [astro organization token delete](cli/astro-organization-token-delete.md)
- [astro organization switch](cli/astro-organization-switch.md)