---
sidebar_label: "astro deployment token organization-token"
title: "astro deployment token organization-token"
id: astro-deployment-token-organization-token
description: Scope an Organization token to a specific Deployment.
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::cliastroonly
:::

Manage Organization-level API tokens within a specific Deployment. See [Assign an Organization or Workspace API token to a Deployment](https://docs.astronomer.io/astro/deployment-api-tokens#assign-an-organization-or-workspace-api-token-to-a-deployment).

## astro deployment organization-token add

Add an Organization API token to a Deployment and grant it Deployment-specific permissions.

### Usage

```sh
astro deployment organization-token add --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --org-token-name=<org-token-name> --workspace-id=<workspace-id>
```

### Options

| Option                   | Description                                        | Valid Values                                                                          |
| ------------------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `--deployment-id`        | The Deployment ID where you want to manage tokens. | Any Deployment ID.                                                                    |
| `-n`, `--org-token-name` | The name of the Oganization API Token.             | Any string. If the name contains a space, specify the entire name within quotes `""`. |
| `r`, `--role`            | The role the API token has in the Deployment.      | `DEPLOYMENT_ADMIN` or a custom role name.                                             |
| `--workspace-id`         | The Workspace to which the Deployment belongs.     | Any Workspace ID.                                                                     |

### Example

```sh
astro deployment organization-token add --deployment-id=clvduhrvd000008l842ohcpvb --role=DEPLOYMENT_ADMIN --org-token-name="My org token"
```

## astro deployment organization-token list

List all Organization API tokens that are assigned to a specific Deployment.

### Usage

```sh
astro deployment organization-token list --deployment-id=<your-deployment-id>
```

### Options

| Option            | Description                                      | Valid Values       |
| ----------------- | ------------------------------------------------ | ------------------ |
| `--deployment-id` | The ID of the Deployment to list API tokens for. | Any Deployment ID. |
| `--workspace-id`  | The Workspace to which the Deployment belongs.   | Any Workspace ID.  |

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

## astro deployment organization-token remove

Remove an Organization API token from a Deployment.

### Usage

```sh
astro deployment organization-token remove --deployment-id=<my-deployment-id> --org-token-name=<org-token-name>
```

### Options

| Option             | Description                                                                    | Valid Values       |
| ------------------ | ------------------------------------------------------------------------------ | ------------------ |
| `--deployment-id`  | The Deployment ID you want to remove an API token from.                        | Any Deployment ID. |
| `--org-token-name` | The name of the Organization API token you want to remove from the Deployment. | Any string.        |
| `--workspace-id`   | The Workspace to which the Deployment belongs.                                 | Any Workspace ID.  |

### Example

```sh
astro deployment organization-token remove --deployment-id=clvduhrvd000008l842ohcpvb --org-token-name="My org token"
```

## astro deployment organization-token update

Update the role an Organization API token has within a Deployment.

### Usage

```sh
astro deployment organization-token update --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN
```

### Options

| Option                   | Description                                                                | Valid Values                              |
| ------------------------ | -------------------------------------------------------------------------- | ----------------------------------------- |
| `--deployment-id`        | The Deployment ID you want to scope an Organization API Token to.          | Any Deployment ID.                        |
| `-r`, `--role`           | The Deployment role that you want to assign to the token.                              | `DEPLOYMENT_ADMIN` or a custom role name. |
| `-n`, `--org-token-name` | The name of the Organization API token that you want to update. | Any string.                               |
| `--workspace-id`         | The Workspace to which the Deployment belongs.                             | Any Workspace ID.                         |

### Example

```sh
astro deployment organization-token update --deployment-id=clvduhrvd000008l842ohcpvb --org-token-name="My org token" --role=DEPLOYMENT_ADMIN
```
