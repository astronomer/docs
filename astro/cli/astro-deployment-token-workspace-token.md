---
sidebar_label: "astro deployment token workspace-token"
title: "astro deployment token workspace-token"
id: astro-deployment-token-workspace-token
description: Scope a Workspace token to a specific Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available on Astro.

:::

To centralize API token management, you can add a Workspace API token to a Deployment instead of creating a dedicated Deployment API token. Deployment-scoped API tokens are useful if you want to manage API tokens from the Organization level on a single screen, or you want to use a single API token for multiple Deployments.

Deployment-scoped API tokens are functionally identical to dedicated Deployment API tokens, except that you can only rotate, update, or delete them within their original scope.

## `astro deployment workspace-token add`

### Usage

```sh
astro deployment workspace-token add --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --workspace-token-name=<workspace-token-name>
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--deployment-id` | The Deployment ID you want to scope an Organization API Token to. | Any Deployment ID                                                      |
| `-r`, `--role`           | The type of Deployment Role the API Token has.                | Possible values are `DEPLOYMENT_ADMIN` or the custom role name. The default is `DEPLOYMENT_ADMIN`. |
| `-n`, `--workspace-token-name` | The name of the Workspace API token you want to add to your Deployment. | Any string                                                        |
| `--workspace-id` | The Workspace assigned to the Deployment. | Any Workspace ID                                                      |

### Example

```sh
astro deployment organization-token add --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --workspace-token-name="My workspace token"
```

## `astro deployment workspace-token list`

### Usage

```sh
astro deployment workspace-token list --deployment-id=<your-deployment-id> --workspace-id=<your-workspace-ic>
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--deployment-id` | Specify a Deployment to list API Tokens outside of your current Deployment. | Any Deployment ID                                                        |
| `--workspace-id` | The Workspace assigned to the Deployment. | Any Workspace ID                                                      |

### Output

| Output           | Description                                                                               | Data Type                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `ID`             | The API Token ID.                                                                         | String                                                                                    |
| `NAME`           | The name of the API Token.                                                                | String                                                                                    |
| `DESCRIPTION`    | The API Token description.                                                                | String                                                                                    |
| `SCOPE`          | The scope level the API Token provides permissions for. Can be `ORGANIZATION` or `WORKSPACE`. | String                                                                                    |
| `DEPLOYMENT_ROLE` | The type of Deployment Role the API Token has.                                             | Possible values are `DEPLOYMENT_ADMIN` or the custom role name. The default is `DEPLOYMENT_ADMIN`. |
| `CREATED`        | How long ago the API Token was created, in days.                                          | String                                                                                    |
| `CREATED BY`     | The name of the user who created the API Token.                                           | String                                                                                    |

### Example

```sh
astro deployment workspace-token list --deployment-id=<your-deployment-id>
```

## `astro deployment workspace-token remove`

### Usage

```sh
astro deployment workspace-token remove --deployment-id=<my-deployment-id> --workspace-token-name=<workspace-token-name> --workspace-id=<my-workspace-id>
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--deployment-id` | The Deployment ID you want to scope an Organization API Token to. | Any Deployment ID                                                      |
| `-n`, `--workspace-token-name` | The name of the Workspace API token you want to add to your Deployment. | Any string                                                        |
| `--workspace-id` | The Workspace ID your API Token is scoped to. | Any Workspace ID                                                      |

### Example

```sh
astro deployment workspace-token remove --deployment-id=<my-deployment-id> --workspace-token-name=<workspace-token-name> --workspace-id=<my-workspace-id>
```

## `astro deployment workspace-token update`

### Usage

```sh
astro deployment organization-token update --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --workspace-token-name=<workspace-token-name>
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--deployment-id` | The Deployment ID you want to scope an Organization API Token to. | Any Deployment ID                                                      |
| `-r`, `--role`           | The type of Deployment Role the API Token has.                | Possible values are `DEPLOYMENT_ADMIN` or the custom role name. The default is `DEPLOYMENT_ADMIN`. |
| `-n`, `--workspace-token-name` | The name of the Workspace API token you want to add to your Deployment. | Any string                                                        |
| `--workspace-id` | The Workspace ID your API Token is scoped to. | Any Workspace ID                                                      |

### Example

```sh
astro deployment organization-token update --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --workspace-token-name="My workspace token"
```