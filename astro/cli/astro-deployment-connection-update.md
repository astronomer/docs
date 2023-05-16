---
sidebar_label: "astro deployment connection update"
title: "astro deployment connection update"
id: astro-deployment-connection-update
description: Reference documentation for astro deployment connection update.
hide_table_of_contents: true
---

For a given Deployment on Astro, update connections that are stored in the Airflow metadata database.

## Usage

```sh
astro deployment connection update
```

:::tip

To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), set the following OS-level environment variables in a way that the Astro CLI can access them:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

After setting the variables, this command works for a Deployment without you having to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The ID of the Deployment for which to update connections                                                | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment for which to update Conections. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-w`,`--workspace-id`          | update connections for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |
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

```sh
# update connection called my-connection stored in the Deployment with an ID of cl03oiq7d80402nwn7fsl3dmv
$ astro deployment connection update --deployment-id cl03oiq7d80402nwn7fsl3dmv --conn-id my-connection --conn-type http

# update connections stored in the Deployment "My Deployment"
$ astro deployment connection update --deployment-name="My Deployment" --conn-id my-connection --conn-type http
```

## Related Commands

- [`astro deployment connection create`](cli/astro-deployment-connection-create.md)
- [`astro deployment connection list`](cli/astro-deployment-connection-list.md)
