---
sidebar_label: "astro deployment token update"
title: "astro deployment token update"
id: astro-deployment-token-update
description: Update your Deployment API tokens.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::cliastroonly
:::

Update an Astro [Deployment API Token](deployment-api-tokens.md).

To use your API token in an automated process, see [Authenticate an automation tool](automation-authentication.md).

## Usage

```sh
astro deployment token update --deployment-id=MOCK_DEP_ID
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
|`-d`, `--description`           |    Updated description of the token. If the description contains a space, specify the entire description in quotes `""`.                                              | String |
| `-t`,`--name`           |    The current name of the token. If the name contains a space, specify the entire name within quotes `""`.                                                | String |
| `-n`, `--new-name` | The token's new name. If the new name contains a space, specify the entire name within quotes "". | String |
| `-r`, `--role` | The role for the token. Possible values are `DEPLOYMENT_ADMIN` or a custom role name. | Any valid Deployment role. |

## Examples

```bash
# The CLI prompts you to input a role for a token with Token ID assigned to a specific Deployment
astro deployment token update <token-id> --deployment-id=clukapi6r000008l58530cg8i

# The CLI prompts you to input a role for a token identified by its name
astro deployment token update --deployment-id=clukapi6r000008l58530cg8i --name="Token name"

# The CLI prompts you to select the token from a list and input a role
astro deployment token update --deployment-id=clukapi6r000008l58530cg8i

# This command assigns a token with the specified TOKEN_ID the role `Deployment Admin` to a Deployment with the following ID.
astro deployment token update TOKEN_ID --deployment-id=clukapi6r000008l58530cg8i --role=DEPLOYMENT_ADMIN
```

## Related Commands

- [`astro deployment token create`](cli/astro-deployment-create.md)
- [`astro deployment token list`](cli/astro-deployment-token-list.md)
- [`astro deployment token rotate`](cli/astro-deployment-token-rotate.md)
