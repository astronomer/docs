---
sidebar_label: "astro deploy"
title: "astro deploy"
id: astro-deploy
description: Reference documentation for astro deploy.
---

[Deploy code](deploy-code.md) to a Deployment on Astro.

This command bundles all files in your Astro project and pushes them to Astro. Before completing the process, it tests your DAGs in your Astro project for errors. If this test fails, the deploy to Astro will also fail. This is the same test which runs locally with `astro dev parse`.

When you run `astro deploy`, you'll be prompted to select from a list of all Deployments that you have access to across Workspaces. To bypass this prompt, you can also specify a Deployment ID in the command. To retrieve a Deployment ID, go to your Deployment's information page in the Cloud UI and copy the value after the last `/` in the URL. You can also find a Deployment's ID by running `astro deployment list`.

For teams operating at scale, this command can be automated via a [CI/CD pipeline](ci-cd.md) by using [Deployment API keys](api-keys.md) in the request. When `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET` are specified as OS-level environment variables on your local machine or in a CI tool, `astro deploy <deployment-id>` can be run without requiring user authentication.

:::tip

To skip the parsing process before deploys, complete one of the following setups:

- Add `skip_parse: true` to `.astro/config.yaml` in your Astro project.
- Add `ASTRONOMER_SKIP_PARSE=true` as an environment variable to your local environment or CI/CD pipeline.

:::

## Usage

```sh
astro deploy <options>
```

## Options

| Option                    | Description                                                                                    | Possible Values                                        |
| ------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `<deployment-id>`         | Specify the Deployment to deploy to, bypass Deployment selection prompt                        | Any valid Deployment ID                                |
| `-e`,`--env`              | Location of the file containing environment variables for pytests. By default, this is `.env`. | Any valid filepath to an `.env` file                   |
| `-f`,`--force`            | Force deploy even if your project contains errors or uncommitted changes                       | ``                                                     |
| `-p`,`--prompt`           | Force the Deployment selection prompt even if a Deployment ID is specified                     | ``                                                     |
| `--pytest`                | Deploy code to Astro only if the specified pytests are passed                                  | ``                                                     |
| `-s`,`--save`             | Save the current Deployment and working directory combination for future deploys               | ``                                                     |
| `-t`,`--test`             | The filepath to an alternative pytest file or directory                                        | Valid filepath within your Astro project               |
| `--workspace-id <string>` | In the prompt to select a Deployment, only show Deployments within this Workspace              | Any valid Workspace ID                                 |
| `-i`, `--image-name`      | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine                                      | A valid name for a pre-built Docker image based on Astro Runtime |

## Examples

```sh
# List of Deployments appears
$ astro deploy

# Deploy directly to a specific Deployment
$ astro deploy ckvvfp9tf509941drl4vela81n

# The CLI automatically selects this Deployment for your Astro project
$ astro deploy ckvvfp9tf509941drl4vela81n --save

# The CLI looks for a Docker image with a matching name in your local Docker registry and builds your project with it
$ astro deploy --image-name my-custom-runtime-image
```

## Related Commands

- [`astro login`](cli/astro-login.md)
- [`astro deployment list`](cli/astro-deployment-list.md)
- [`astro dev parse`](cli/astro-dev-parse.md)
