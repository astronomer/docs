---
sidebar_label: "astrocloud deploy"
title: "astrocloud deploy"
id: astrocloud-deploy
description: Reference documentation for astrocloud deploy.
---

## Description

[Deploy code](deploy-code.md) to a Deployment on Astro.

This command bundles all files in your Astro project and pushes them to Astro. Before completing the process, it tests your DAGs in your Astro project for errors. If this test fails, the deploy to Astro will also fail. This is the same test which runs locally with `astrocloud dev parse`.

When you run `astrocloud deploy`, you'll be prompted to select from a list of all Deployments that you have access to across Workspaces. To bypass this prompt, you can also specify a Deployment ID in the command. To retrieve a Deployment ID, go to your Deployment's information page in the Cloud UI and copy the value after the last `/` in the URL. You can also find a Deployment's ID by running `astrocloud deployment list`.

For teams operating at scale, this command can be automated via a [CI/CD pipeline](ci-cd.md) by using [Deployment API keys](api-keys.md) in the request. When `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET` are specified as OS-level environment variables on your local machine or in a CI tool, `astrocloud deploy <deployment-id>` can be run without requiring user authentication.

## Usage

```sh
astrocloud deploy <options>
```

## Options

| Option                    | Description                                                                                                       | Possible Values                          |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `<deployment-id>`         | Specify the Deployment to deploy to, bypass Deployment selection prompt                                                                             | Any valid Deployment ID           |
| `-e`,`--env`              | Location of the file containing environment variables for Pytests. By default, this is `.env`.                                 | Any valid filepath to an `.env` file     |
| `-f`,`--force`            | Force deploy even if your project contains errors or uncommitted changes                                                               | ``                                       |
| `-p`,`--prompt`            | Force the Deployment selection prompt even if a Deployment ID is specified                           | ``                                       |
| `--pytest`                | Deploy code to Astro only if the specified Pytests are passed                                                     | ``                                       |
| `-s`,`--save`              | Save the current Deployment and working directory combination for future deploys                                              | ``                                       |
| `-t`,`--test`              | The filepath to an alternative pytest file or directory | Valid filepath within your Astro project |
| `--workspace-id <string>` | In the prompt to select a Deployment, only show Deployments within this Workspace                                                                             | Any valid Workspace ID                                |

## Examples

```sh
# List of Deployments appears
$ astrocloud deploy

# Deploy directly to a specific Deployment
$ astrocloud deploy ckvvfp9tf509941drl4vela81n

# Running `astrocloud deploy` will now automatically select this Deployment for your Astro project
$ astrocloud deploy ckvvfp9tf509941drl4vela81n --save
```

## Related Commands

- [`astrocloud auth login`](cli-reference/astrocloud-auth-login.md)
- [`astrocloud deployment list`](cli-reference/astrocloud-deployment-list.md)
- [`astrocloud dev parse`](cli-reference/astrocloud-dev-parse.md)
