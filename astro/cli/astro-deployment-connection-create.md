---
sidebar_label: "astro deployment connection create"
title: "astro deployment connection create"
id: astro-deployment-connection-create
description: Reference documentation for astro deployment connection create.
hide_table_of_contents: true
---

List the Airflow connections stored in a Deployment's metadata database. 

## Usage

```sh
astro deployment connection list
```

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
# create connection called my-connection stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
astro deployment connection create --deployment-id cl03oiq7d80402nwn7fsl3dmv --conn-id my-connection --conn-type http

# create connections stored in the Deployment "My Deployment"
astro deployment connection create --deployment-name="My Deployment" --conn-id my-connection --conn-type http
```

## Related Commands

- [`astro deployment connection create`](cli/astro-deployment-connection-create.md)
- [`astro deployment connection update`](cli/astro-deployment-connection-update.md)
