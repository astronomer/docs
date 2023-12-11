---
sidebar_label: "astro deployment connection update"
title: "astro deployment connection update"
id: astro-deployment-connection-update
description: Update an Airflow connection in a Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

Update the value for a Deployment's Airflow variable.

## Usage

```sh
astro deployment connection update
```

:::tip

This command is recommended for automated workflows. To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), you can generate a Deployment or Workspace API Token, then specify the `ASTRO_API_TOKEN` environment variable in the system running the Astro CLI:

```bash
export ASTRO_API_TOKEN=<your-token>
```

See [Deployment API Tokens](deployment-api-tokens.md) and [Workspace API Tokens](workspace-api-tokens.md) for more details about ways to use tokens.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The ID of the Deployment where you want to create a connection.                                              | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment where you want to create a connection. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | Create a connection for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed.           | Any valid Workspace ID                                                         |
| `-i`,`--conn-id`          | The connection ID. Required.           | string                                                         |
| `-t`,`--conn-type`          | The connection type. Required.           | string                                                         |
| `--description`          | The connection description.           | string                                                         |
| `--extra`          | The extra field configuration, defined as a stringified JSON object.           | string                                                         |
| `--host`          | The connection host.          | string                                                         |
| `--login`          | The connection login or username.          | string                                                         |
| `--password`          | The connection password.         | string                                                         |
| `--port`          | The connection port.        | string                                                         |
| `--schema`          | The connection schema.        | string                                                         |

## Examples

```bash
# update connection called my-connection stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
astro deployment connection update --deployment-id cl03oiq7d80402nwn7fsl3dmv --conn-id my-connection --conn-type http

# update connections stored in the Deployment "My Deployment"
astro deployment connection update --deployment-name="My Deployment" --conn-id my-connection --conn-type http
```

## Related Commands

- [`astro deployment connection create`](cli/astro-deployment-connection-create.md)
- [`astro deployment connection list`](cli/astro-deployment-connection-list.md)
