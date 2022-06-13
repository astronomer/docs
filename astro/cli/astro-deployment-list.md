---
sidebar_label: "astro deployment list"
title: "astro deployment list"
id: astro-deployment-list
description: Reference documentation for astro deployment list.
---

## Description

List all Deployments within your current Workspace.

## Usage

```sh
astro deployment list
```

:::tip

To run this command in an automated process such as a [CI/CD pipeline](ci-cd.md), set the following OS-level environment variables in a way that the Astro CLI can access them:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

After setting the variables, this command works for a Deployment and you don't need to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

:::

## Options

| Option  | Description                             | Possible Values |
| ------- | --------------------------------------- | --------------- |
| `-a`,`--all` | Show Deployments across all Workspaces that you have access to. | ``              |
| `--workspace-id` | Specify a Workspace to list Deployments outside of your current Workspace | Any valid Workspace ID                                            |

## Examples

```sh
$ astro deployment list --all
# Shows Deployments from all Workspaces that you're authenticated to
```

## Related Commands

- [`astro login`](cli/astro-login.md)
- [`astro deploy`](cli/astro-deploy.md)
