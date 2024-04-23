---
sidebar_label: "astro workspace token organization-token"
title: "astro workspace token organization-token"
id: astro-workspace-token-organization-token
description: Scope an Organization token to a specific Workspace.
hide_table_of_contents: true
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::info

This command is only available on Astro.

:::

To centralize API token management, you can add an Organization token to a Workspace instead of creating a dedicated Workspace API token. Workspace-scoped API tokens are useful if you want to manage API tokens from the Organization level on a single screen, or you want to use a single API token for multiple Workspaces

There are four sub-commands for managing a Workspace-scoped Organization token.

## `astro workspace organization-token add`

### Usage

```sh
astro workspace organization-token add --org-token-name=ORGANIZATION-NAME --role=WORKSPACE_MEMBER
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--org-token-name` | The name of the Organization API token you want to add to your Workspace. | Any string                                                        |
| `--role`           | The Workspace role to grant to the Organization API token.                | One of `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER`. |

### Example

```sh
astro workspace organization-token add --org-token-name="My Organization" --role=WORKSPACE_OWNER
```

## `astro workspace organization-token list`

### Usage

```sh
astro workspace organization-token list
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--workspace-id` | Specify a Workspace to list Deployments outside of your current Workspace. | Any Workspace ID                                                        |

### Output

| Output           | Description                                                                               | Data Type                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `ID`             | The API Token ID.                                                                         | String                                                                                    |
| `NAME`           | The name of the API Token.                                                                | String                                                                                    |
| `DESCRIPTION`    | The API Token description.                                                                | String                                                                                    |
| `SCOPE`          | The scope level the API Token provides permissions for. Can be `ORGANIZATION` or `WORKSPACE`. | String                                                                                    |
| `WORKSPACE_ROLE` | The type of Workspace Role the API Token has.                                             | One of `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER`. |
| `CREATED`        | How long ago the API Token was created, in days.                                          | String                                                                                    |
| `CREATED BY`     | The name of the user who created the API Token.                                           | String                                                                                    |

### Example

```sh
astro workspace organization-token list
```

## `astro workspace organization-token remove`

### Usage

```sh
astro workspace organization-token remove --org-token-name=ORG-TOKEN-NAME
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--org-token-name` | The name of the Organization API token you want to add to your Workspace. | Any string                                                        |

### Example

```sh
astro workspace organization-token remove --org-token-name=ORG-TOKEN-NAME
```

## `astro workspace organization-token update`

### Usage

```sh
astro workspace organization-token add --org-token-name=ORGANIZATION-NAME --role=WORKSPACE_MEMBER
```

### Options

| Option             | Description                                                               | Valid Values                                                                              |
| ------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `--org-token-name` | The name of the Organization API token you want to add to your Workspace. | Any string                                                        |
| `--role`           | The Workspace role to grant to the Organization API token.                | One of `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER`. |

### Example

```sh
astro workspace organization-token add --org-token-name=MY-ORGANIZATION --role=WORKSPACE_AUTHOR
```