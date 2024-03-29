---
sidebar_label: "astro deployment token list"
title: "astro deployment token list"
id: astro-deployment-token-list
description: List your Deployment API tokens.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available on Astro.

:::

List your Astro [Deployment API Token](deployment-api-tokens.md)

To use your API token in an automated process, see [Authenticate an automation tool](automation-authentication.md).

## Usage

```sh
astro deployment token list
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `--deployment-id` | The Deployment where you would like to manage tokens. | A valid Deployment ID |
| `--verbosity` | The Log level | `debug`, `info`, `warn`, `error`, `fatal`, or `panic`. Default is `warn`. |
| `--workspace-id` | The Workspace ID assigned to a Deployment. | A valid Workspace ID |

## Output

| Output  | Description                                       | Data Type |
| ------- | ------------------------------------------------- | --------- |
|    |    |    |

## Examples

```bash
# create a deployment token
astro deployment token list

```

## Related Commands

- [`astro deployment token create`](cli/astro-deployment-create.md)
- [`astro deployment token update`](cli/astro-deployment-token-update.md)
- [`astro deployment token rotate`](cli/astro-deployment-token-rotate.md)
