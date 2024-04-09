---
sidebar_label: "astro deployment token list"
title: "astro deployment token list"
id: astro-deployment-token-list
description: List your Deployment API tokens.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::info

This command is only available on Astro.

:::

List your Astro [Deployment API Token](deployment-api-tokens.md)

To use your API token in an automated process, see [Authenticate an automation tool](automation-authentication.md).

## Usage

```sh
astro deployment token list --deployment-id=<deployment-id>
```

## Options

| Option            | Description                                           | Possible Values                                                           |
| ----------------- | ----------------------------------------------------- | ------------------------------------------------------------------------- |
| `--deployment-id` | The Deployment to list tokens for. | A valid Deployment ID                                                     |
| `--verbosity`     | The log level.                                         | `debug`, `info`, `warn`, `error`, `fatal`, or `panic`. Default is `warn`. |
| `--workspace-id`  | The Workspace ID for the Deployment.            | A valid Workspace ID                                                      |

## Output

| Output        | Description                                                          | Data Type |
| ------------- | -------------------------------------------------------------------- | --------- |
| `ID`          | The token ID.                                                        | String    |
| `NAME`        | The name of the token.                                               | String    |
| `DESCRIPTION` | The description of the API Token.                           | String    |
| `SCOPE`       | Whether the API Token is scoped to a Deployment, Workspace, or Organization. | String    |
| `CREATED`     | How long ago the token was created in days.                          | String    |
| `CEATED BY`   | The name of the user entity who created the token.                        | String    |

## Examples

```bash
# List tokens for a single Deployment
astro deployment token list --deployment-id=clukapi6r000008l58530cg8i
```

## Related Commands

- [`astro deployment token create`](cli/astro-deployment-create.md)
- [`astro deployment token update`](cli/astro-deployment-token-update.md)
- [`astro deployment token rotate`](cli/astro-deployment-token-rotate.md)
