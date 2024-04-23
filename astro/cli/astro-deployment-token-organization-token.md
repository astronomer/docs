---
sidebar_label: "astro deployment token organization-token"
title: "astro deployment token organization-token"
id: astro-deployment-token-organization-token
description: Scope an Organization token to a specific Deployment.
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available on Astro.

:::

To centralize API token management, you can add an Organization API token to a Deployment instead of creating a dedicated Deployment API token. Deployment-scoped API tokens are useful if you want to manage API tokens from the Organization level on a single screen, or you want to use a single API token for multiple Deployments.

Deployment-scoped API tokens are functionally identical to dedicated Deployment API tokens, except that you can only rotate, update, or delete them within their original scope.

## `astro deployment organization-token add`

### Usage

```sh
astro deployment organization-token add --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --org-token-name=<org-token-name>
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--deployment-id` | The Deployment ID you want to scope an Organization API Token to. | Any Deployment ID                                                      |
| `--role`           | The type of Deployment Role the API Token has.                | Possible values are `DEPLOYMENT_ADMIN` or the custom role name. The default is `DEPLOYMENT_ADMIN`. |
| `--org-token-name` | The name of the Organization API token you want to add to your Deployment. | Any string                                                        |

### Example

```sh
astro deployment organization-token add --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --org-token-name="My org token"
```

## `astro deployment organization-token list`

### Usage

```sh
astro deployment organization-token list --deployment-id=<your-deployment-id>
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--deployment-id` | Specify a Deployment to list API Tokens outside of your current Deployment. | Any Deployment ID                                                        |

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

## `astro deployment organization-token remove`

### Usage

```sh
astro deployment organization-token remove --deployment-id=<my-deployment-id> --org-token-name=<org-token-name>
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--deployment-id` | The Deployment ID you want to scope an Organization API Token to. | Any Deployment ID                                                      |
| `--org-token-name` | The name of the Organization API token you want to add to your Deployment. | Any string                                                        |

### Example

```sh
astro deployment organization-token remove --deployment-id=<my-deployment-id> --org-token-name=my-org-token
```

## `astro deployment organization-token update`

### Usage

```sh
astro deployment organization-token update --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --org-token-name=<org-token-name>
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--deployment-id` | The Deployment ID you want to scope an Organization API Token to. | Any Deployment ID                                                      |
| `--role`           | The type of Deployment Role the API Token has.                | Possible values are `DEPLOYMENT_ADMIN` or the custom role name. The default is `DEPLOYMENT_ADMIN`. |
| `--org-token-name` | The name of the Organization API token you want to add to your Deployment. | Any string                                                        |

### Example

```sh
astro deployment organization-token update --deployment-id=<my-deployment-id> --role=DEPLOYMENT_ADMIN --org-token-name=My-org-token
```