---
sidebar_label: "astro deployment token rotate"
title: "astro deployment token rotate"
id: astro-deployment-token-rotate
description: Rotate your Deployment API tokens.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available on Astro.

:::

Rotate an Astro [Deployment API Token](deployment-api-tokens.md)

To use your API token in an automated process, see [Authenticate an automation tool](automation-authentication.md).

## Usage

```sh
astro deployment token roate <token-ID> [flags]
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-c`,`--clean-output`           |    Print only the token as output. For use of the command in scripts.                                              | N/A |
| `-f`, `--force` | Rotate the Deployment API token without showing a warning. | N/A                                          |
| `-t`,`--name`          | The name of the token to be rotated. If the name contains a space, specify the entire name within quotes "".          | String                                                         |

## Examples

```bash
astro deployment token rotate [flags]
```

## Related Commands

- [`astro deployment token create`](cli/astro-deployment-create.md)
- [`astro deployment token list`](cli/astro-deployment-token-list.md)
- [`astro deployment token update`](cli/astro-deployment-token-update.md)
