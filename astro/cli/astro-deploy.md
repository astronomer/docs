---
sidebar_label: "astro deploy"
title: "astro deploy"
id: astro-deploy
description: Deploy a local project to an Astro Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change between product contexts.

:::

<Tabs
defaultValue="astro"
values={[
{label: 'Astro', value: 'astro'},
{label: 'Software', value: 'software'},
]}>
<TabItem value="astro">

[Deploy code](deploy-code.md) to a Deployment on Astro.

This command bundles all files in your Astro project and pushes them to Astro. Before completing the process, it tests your DAGs in your Astro project for errors. If this test fails, the deploy to Astro will also fail. This is the same test which runs locally with `astro dev parse`.

When you run `astro deploy`, you'll be prompted to select from a list of all Deployments that you can access across Workspaces. To bypass this prompt, you can also specify a Deployment ID in the command. To retrieve a Deployment ID, open your Deployment in the Cloud UI and copy the value in the **ID** section of the Deployment page. You can also run `astro deployment list` to find a Deployment ID or name.

For teams operating at scale, this command can be automated with a [CI/CD pipeline](set-up-ci-cd.md) by using [Deployment API keys](api-keys.md) in the request. When `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET` are specified as OS-level environment variables on your local machine or in a CI tool, `astro deploy <deployment-id>` can be run without requiring user authentication.

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

| Option                    | Description                                                                                                                                           | Possible Values                                                  |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `<deployment-id>`         | Specifies the Deployment to deploy to and bypasses the Deployment selection prompt                                                                    | Any valid Deployment ID                                          |
| `-d`, `--dags`            | Deploy only your `dags` directory. See [DAG-only deploys](deploy-code.md#dag-only-deploys)                                                            | None                                                             |
| `-n`, `--deployment-name` | The name of the Deployment to deploy to. Use as an alternative to `<deployment-id>`                                                                   | Any valid Deployment name                                        |
| `--description`           | A description for your code deploy. Descriptions appear in the Cloud UI in your Deployment's **Deploy History**                                       | None                                                             |
| `-e`,`--env`              | Location of the file containing environment variables for pytests. By default, this is `.env`.                                                        | Any valid filepath to an `.env` file                             |
| `-f`,`--force`            | Force deploy even if your project contains errors or uncommitted changes                                                                              | None                                                             |
| `-p`,`--prompt`           | Force the Deployment selection prompt even if a Deployment ID is specified                                                                            | None                                                             |
| `--pytest`                | Deploy code to Astro only if the specified pytests are passed                                                                                         | None                                                             |
| `-s`,`--save`             | Save the current Deployment and working directory combination for future deploys                                                                      | None                                                             |
| `-t`,`--test`             | The filepath to an alternative pytest file or directory                                                                                               | Valid filepath within your Astro project                         |
| `--workspace-id <string>` | In the prompt to select a Deployment, only show Deployments within this Workspace                                                                     | Any valid Workspace ID                                           |
| `-i`, `--image-name`      | The name of a pre-built custom Docker image to use with your project. The image must be available from a Docker registry hosted on your local machine | A valid name for a pre-built Docker image based on Astro Runtime |
| `-w`, `--wait`            | Wait for the Deployment to become healthy before completing the command                                                                                   | None                                                             |

## Examples

To deploy directly to a specific Deployment:

```bash
astro deploy ckvvfp9tf509941drl4vela81n
```

To configure the Astro CLI to use a given Deployment and directory as a default for future deploys:

```bash
astro deploy ckvvfp9tf509941drl4vela81n --save
```

To [use a custom Docker image](release-notes.md#deploy-a-custom-docker-image-with-new---image-name-flag) from your local Docker registry to build your Astro project:

```bash
astro deploy --image-name your-custom-runtime-image
```

To deploy only DAGs from your Astro project to a specific Deployment:

```bash
astro deploy ckvvfp9tf509941drl4vela81n --dags
```

:::info

If you have uncommitted changes in your working directory, you must use the `-f` or `--force` flag with this command or commit changes to your code repository.

:::

</TabItem>

<TabItem value="software">

[Deploy code](deploy-code.md) to a Deployment on Astronomer Software.

This command bundles all files in your Astro project and pushes them to Astronomer Software.

When you run `astro deploy`, you'll be prompted to select from a list of all Deployments that you can access in all Workspaces. To bypass this prompt, you can specify a Deployment ID in the command. To retrieve a Deployment ID, go to your Deployment's information page in the Cloud UI and copy the value after the last `/` in the URL. You can also run `astro deployment list` to retrieve a Deployment ID .

## Options

| Option                    | Description                                                                        | Possible Values         |
| ------------------------- | ---------------------------------------------------------------------------------- | ----------------------- |
| `<deployment-id>`         | Specifies the Deployment to deploy to and bypasses the Deployment selection prompt | Any valid Deployment ID |
| `-f`,`--force`            | Force deploy even if your project contains errors or uncommitted changes           | None                    |
| `-p`,`--prompt`           | Force the Deployment selection prompt even if a Deployment ID is specified         | None                    |
| `-s`,`--save`             | Save the current Deployment and working directory combination for future deploys   | None                    |
| `--no-cache`              | Do not use any images from the container engine's cache when building your project | None                    |
| `--workspace-id <string>` | In the prompt to select a Deployment, only show Deployments within this Workspace  | Any valid Workspace ID  |

## Examples

```sh
# List of Deployments appears
$ astro deploy

# Deploy directly to a specific Deployment
$ astro deploy ckvvfp9tf509941drl4vela81n

# The CLI automatically selects this Deployment for your Astro project
$ astro deploy ckvvfp9tf509941drl4vela81n --save
```
</TabItem>
</Tabs>

:::info

The following error can sometimes occur when the CLI tries to build your Astro Runtime image using Podman:

```bash
WARN[0010] SHELL is not supported for OCI image format, [/bin/bash -o pipefail -e -u -x -c] will be ignored. Must use `docker` format 
```
You can resolve this issue by exporting the `BUILDAH_FORMAT` [environment variable](astro/environment-variables.md) to Podman:

```dockerfile
export BUILDAH_FORMAT=docker
```
:::

## Related commands

- [`astro login`](cli/astro-login.md)
- [`astro deployment list`](cli/astro-deployment-list.md)
- [`astro dev parse`](cli/astro-dev-parse.md)
