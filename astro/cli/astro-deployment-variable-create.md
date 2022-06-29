---
sidebar_label: "astro deployment variable create"
title: "astro deployment variable create"
id: astro-deployment-variable-create
description: Reference documentation for astro deployment variable create.
---

## Description

For a given Deployment on Astro, create environment variables via the Astro CLI by supplying either a key and value pair or a file (e.g. `.env`) with a list of keys and values. This command is functionally identical to creating an environment variable via the Cloud UI. For more information, see [Set environment variables on Astro](environment-variables.md).

If you choose to specify `--key` and `--value` instead of loading a file, you can only create one environment variable at a time.

## Usage

```sh
astro deployment variable create
```

:::tip

To run this command in an automated process such as a [CI/CD pipeline](ci-cd.md), set the following OS-level environment variables in a way that the Astro CLI can access them:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

After setting the variables, this command works for a Deployment and you don't need to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |       The Deployment in which to create environment variable(s)                           | Any valid Deployment ID |
| `-e`,`--env`                  | The path to a file that contains a list of environment variables.  If a filepath isn't specified, this looks for a `.env` file in your current directory. If `.env` doesn't exist, this flag will create it for you                                                                 | Any valid filepath       |
| `-k`,`--key`             | The environment variable key                                                  | Any string |
| `-l`,`--load`    | Export new environment variables from your Astro project's `.env` file to the Deployment. This is an alternative to creating an environment variable by manually specifying `--key` and `--value`. By default, this flag exports all new environment variables based on the file specified with `--env`            |`` |
| `-s`,`--secret`    | Set the value of the new environment variable as secret      |`` |
| `-v`,`--value`    | The environment variable value          |`` |
| `-w`,`--workspace-id`          | Create or update an environment variable for a Deployment that is not in your current Workspace. If this is not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |

## Examples

```sh
# Create a new secret environment variable
$ astro deployment variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv --key AIRFLOW__SECRETS__BACKEND_KWARGS --value <my-secret-value> --secret

# Create multiple environment variables for a Deployment at once by loading them from a .env file
$ astro deployment variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv --load --env .env.dev

# Update the value of an existing environment variable
$ astro deployment variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv --update --key AIRFLOW__CORE__PARALLELISM --value <my-new-value>
```

## Related Commands

- [`astro deployment variable list`](cli/astro-deployment-variable-list.md)
- [`astro deployment variable update`](cli/astro-deployment-variable-update.md)
