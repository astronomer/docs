---
sidebar_label: "astro workspace token organization-token"
title: "astro workspace token organization-token"
id: astro-workspace-token-organization-token
description: Scope an Organization token to a specific Workspace.
sidebar_custom_props: { icon: "img/term-icon.png" }
---

:::cliastroonly
:::

Manage Organization-level API tokens within a specific Workspace. See [Assign an Organization API token to a Workspace](https://docs.astronomer.io/astro/workspace-api-tokens#assign-an-organization-api-token-to-a-workspace).

There are four sub-commands for managing a Workspace-scoped Organization token.

## astro workspace organization-token add

Add an Organization API token to a Workspace and grant it Workspace-specific permissions.

### Usage

```sh
astro workspace organization-token add <ORG_TOKEN_ID> --org-token-name=ORGANIZATION-NAME --role=WORKSPACE_MEMBER
```

### Options

| Option                   | Description                                    | Valid Values                                                                              |
| ------------------------ | ---------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `-n`, `--org-token-name` | The name of the Oganization API Token.         | Any string. If the name contains a space, specify the entire name within quotes `""`.     |
| `-r`, `--role`           | The role the API token has in the Workspace.   | One of `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER`. |
| `--workspace-id`         | The Workspace to which the Deployment belongs. | Any Workspace ID.                                                                         |

### Example

```sh
astro workspace organization-token add <ORG_TOKEN_ID> --org-token-name="My Organization" --role=WORKSPACE_OWNER
```

## astro workspace organization-token list

List all Organization API tokens that are assigned to a specific Workspace.

### Usage

```sh
astro workspace organization-token list
```

### Options

| Option           | Description                                   | Valid Values      |
| ---------------- | --------------------------------------------- | ----------------- |
| `--workspace-id` | The Workspace to which the API Tokens belong. | Any Workspace ID. |

### Output

| Output           | Description                                      | Data Type |
| ---------------- | ------------------------------------------------ | --------- | ----------------------------------------------------------------------------------------- |
| `ID`             | The API Token ID.                                | String    |
| `NAME`           | The name of the API Token.                       | String    |
| `DESCRIPTION`    | The API Token description.                       | String    |
| `SCOPE`          | The original scope of the API token.             | String    |
| `WORKSPACE_ROLE` | The API token's role in the Workspace.           | String    | One of `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER`. |
| `CREATED`        | How long ago the API Token was created, in days. | String    |
| `CREATED BY`     | The name of the user who created the API Token.  | String    |

## astro workspace organization-token remove

Remove an Organization API token from a Workspace.

### Usage

```sh
astro workspace organization-token remove <ORG_TOKEN_ID> --org-token-name=ORG-TOKEN-NAME
```

### Options

| Option                  | Description                                                                   | Valid Values     |
| ----------------------- | ----------------------------------------------------------------------------- | ---------------- |
| `-n`,`--org-token-name` | The name of the Organization API token you want to remove from the Workspace. | Any string.      |
| `--workspace-id`        | Workspace from where you want to remove an API token.                         | Any Workspace ID |

### Example

```sh
astro workspace organization-token remove --org-token-name="My org token"
```

## astro workspace organization-token update

Update the role an Organization API token has within a Workspace.

### Usage

```sh
astro workspace organization-token add <ORG_TOKEN_ID> --org-token-name=ORGANIZATION-NAME --workspace-id=<workspace-id> --role=WORKSPACE_MEMBER
```

### Options

| Option                   | Description                                                               | Valid Values                                                                              |
| ------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `-n`, `--org-token-name` | The name of the Organization API token you want to add to your Workspace. | Any string.                                                                               |
| `-r`, `--role`           | The role the API token has in the Workspace.                              | One of `WORKSPACE_MEMBER`, `WORKSPACE_AUTHOR`, `WORKSPACE_OPERATOR` or `WORKSPACE_OWNER`. |
| `--workspace-id`         | Workspace where you want to update an API token.                          | Any Workspace ID                                                                          |

### Example

```sh
astro workspace organization-token add <ORG_TOKEN_ID> --workspace-id=clvdx7z3c000008kv5tdw5tc5 --org-token-name=MY-ORGANIZATION --role=WORKSPACE_AUTHOR
```
