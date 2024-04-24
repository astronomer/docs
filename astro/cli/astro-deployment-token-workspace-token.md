---
sidebar_label: "astro deployment token workspace-token"
title: "astro deployment token workspace-token"
id: astro-deployment-token-workspace-token
description: Scope a Workspace token to a specific Deployment.
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::cliastroonly
:::

Manage Workspace-level API tokens within a specific Deployment. See [Assign an Organization or Workspace API token to a Deployment](https://docs.astronomer.io/astro/deployment-api-tokens#assign-an-organization-or-workspace-api-token-to-a-deployment).

## astro deployment workspace-token add

Add a Workspace API token to a Deployment and grant it Deployment-specific permissions.

### Usage

```sh
astro deployment workspace-token add --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --workspace-token-name=<workspace-token-name>
```

### Options

| Option                         | Description                                        | Valid Values                                                                          |
| ------------------------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `--deployment-id`              | The Deployment ID where you want to manage tokens. | Any Deployment ID.                                                                    |
| `-r`, `--role`                 | The role the API token has in the Deployment.      | `DEPLOYMENT_ADMIN` or a custom role name.                                             |
| `-n`, `--workspace-token-name` | The Workspace API token name.                      | Any string. If the name contains a space, specify the entire name within quotes `""`. |
| `--workspace-id`               | The Workspace to which the Deployment belongs.     | Any Workspace ID.                                                                     |

### Example

```sh
astro deployment organization-token add --deployment-id=clvduhrvd000008l842ohcpvb  --role=DEPLOYMENT_ADMIN --workspace-token-name="My workspace token"
```

## astro deployment workspace-token list

List all Workspace API tokens that are assigned to a specific Deployment.

### Usage

```sh
astro deployment workspace-token list --deployment-id=<your-deployment-id> --workspace-id=<your-workspace-ic>
```

### Options

| Option            | Description                                      | Valid Values         |
| ----------------- | ------------------------------------------------ | -------------------- |
| `--deployment-id` | The ID of the Deployment to list API tokens for. | Any Deployment ID.   |
| `--workspace-id`  | The Workspace to which the Deployment belongs.   | Any Workspace ID. ID |

### Output

| Output            | Description                                      | Data Type |
| ----------------- | ------------------------------------------------ | --------- |
| `ID`              | The API Token ID.                                | String    |
| `NAME`            | The name of the API Token.                       | String    |
| `DESCRIPTION`     | The API Token description.                       | String    |
| `SCOPE`           | The original scope of the API token.             | String    |
| `DEPLOYMENT_ROLE` | The API token's role in the Deployment.          | String    |
| `CREATED`         | How long ago the API Token was created, in days. | String    |
| `CREATED BY`      | The name of the user who created the API Token.  | String    |

### Example

```sh
astro deployment workspace-token list --deployment-id=clvduhrvd000008l842ohcpvb
```

## astro deployment workspace-token remove

Remove a Workspace API token from a Deployment.

### Usage

```sh
astro deployment workspace-token remove --deployment-id=<my-deployment-id> --workspace-token-name=<workspace-token-name> --workspace-id=<my-workspace-id>
```

### Options

| Option                         | Description                                                                 | Valid Values       |
| ------------------------------ | --------------------------------------------------------------------------- | ------------------ |
| `--deployment-id`              | The Deployment ID you want to remove an API token from.                     | Any Deployment ID. |
| `-n`, `--workspace-token-name` | The name of the Workspace API token you want to remove from the Deployment. | Any string.        |
| `--workspace-id`               | The Workspace to which the Deployment belongs.                              | Any Workspace ID.  |

### Example

```sh
astro deployment workspace-token remove --deployment-id=clvduhrvd000008l842ohcpvb --workspace-token-name="My workspace token" --workspace-id=clvdwt4z3000008l60ofb6347
```

## astro deployment workspace-token update

Update the role a Workspace API token has within a Deployment.

### Usage

```sh
astro deployment organization-token update --workspace-token-name=<workspace-token-name> --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN
```

### Options

| Option                         | Description                                                             | Valid Values                              |
| ------------------------------ | ----------------------------------------------------------------------- | ----------------------------------------- |
| `--deployment-id`              | The Deployment ID you want to scope a Workspace API Token to.           | Any Deployment ID.                        |
| `-r`, `--role`                 | The Deployment role that you want to assign to the token.                           | `DEPLOYMENT_ADMIN` or a custom role name. |
| `-n`, `--workspace-token-name` | The name of the Workspace API token you want to update. | Any string.                               |
| `--workspace-id`               | The Workspace to which the Deployment belongs.                          | Any Workspace ID.                         |

### Example

```sh
astro deployment organization-token update --deployment-id=clvduhrvd000008l842ohcpvb --role=DEPLOYMENT_ADMIN --workspace-token-name="My workspace token"
```
