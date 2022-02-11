---
sidebar_label: "astrocloud deploy"
title: "astrocloud deploy"
id: astrocloud-deploy
description: Reference documentation for astrocloud deploy.
---

## Description

[Deploy your Astronomer project](deploy-code.md) to a Deployment on Astronomer Cloud.

If you run `astrocloud deploy`, you'll be prompted to select from a list of all Deployments that you have access to across Workspaces. Alternatively, you can bypass this prompt and specify a Deployment's namespace in the command. To retrieve a Deployment's namespace, go to the Deployment's information page in the Astronomer UI and copy the value under **Namespace**.

## Usage

```sh
astrocloud deploy <options>
```

## Options

| Option                    | Description                                                                            | Possible Values                |
| ------------------------- | -------------------------------------------------------------------------------------- | ------------------------------ |
| `<deployment-namespace>`  | Specify the Deployment to deploy to.                                                   | Any valid Deployment namespace |
| `-f`,`--force`               | Force the deploy even if uncommitted changes exist                                     | ``                             |
| `p`,`--prompt`                | Force the prompt for selecting deployments to appear even if a Deployment is specified | ``                             |
| `s`,`--save`                  | Save the current directory/Deployment combination for future deploys                   | ``                             |
| `--workspace-id <string>` |Workspace assigned to the Deployment                  | Any value                      |

## Examples

```sh
$ astrocloud deploy
# List of Deployments appears
$ astrocloud deploy asteroidic-vacuum-4865
# Deploy directly to a specific Deployment
$ astrocloud deploy asteroidic-vacuum-4865 --save
# Running `astrocloud deploy` will now automatically select this Deployment for your Astronomer project
```

## Related Commands

- [`astrocloud auth login`](cli-reference/astrocloud-auth-login.md)
- [`astrocloud deployment list`](cli-reference/astrocloud-deployment-list.md)
