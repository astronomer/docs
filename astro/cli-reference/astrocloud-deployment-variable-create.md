---
sidebar_label: "astrocloud deployment variable create"
title: "astrocloud deployment variable create"
id: astrocloud-deployment-variable-create
description: Reference documentation for astrocloud deployment variable create.
---

## Description

For a given Deployment on Astro, create environment variables via the Astro CLI by supplying either a key and value pair or a file (e.g. `.env`) with a list of keys and values. This command is functionally identical to creating an environment variable via the Cloud UI. For more information, see [Set Environment Variables on Astro](environment-variables.md).

If you choose to specify `--key` and `--value` instead of loading a file, you can only create one environment variable at a time.

:::tip

This command has an `--update` flag that allows you to change the `value` of an existing environment variable at any time. For a better user experience, we recommend using the [`astrocloud deployment variable update` command](cli-reference/astrocloud-deployment-variable-update.md) to update environment variables instead.

:::

## Usage

```sh
astrocloud deployment variable create
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |       The Deployment in which to create environment variable(s)                           | Any valid Deployment ID |
| `-e`,`--env`                  | The path to a file that contains a list of environment variables.  If a filepath isn't specified, this looks for a `.env` file in your current directory. If `.env` doesn't exist, this flag will create it for you                                                                 | Any valid filepath       |
| `-k`,`--key`             | The environment variable key                                                  | Any string |
| `-l`,`--load`    | Load new environment variables from a file. Specify this flag if the variables you want to create are in that file. This is an alternative to creating an environment variable by manually specifying `--key` and `--value`             |`` |
| `-s`,`--secret`    | Set the value of the new environment variable as secret      |`` |
| `-u`,`--update`    | Update the value of an existing environment variable. Make sure to specify the `--key` to which this new value will be applied          | Any string |
| `-v`,`--value`    | The environment variable value          |`` |
| `-w`,`--workspace-id`          | Create or update an environment variable for a Deployment that is not in your current Workspace. If this is not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |

## Examples

```sh
# Create a new secret environment variable
$ astrocloud deployment variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv --key AIRFLOW__SECRETS__BACKEND_KWARGS --value <my-secret-value> --secret

# Create multiple environment variables for a Deployment at once by loading them from a .env file
$ astrocloud deployment variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv --load --env .env.dev

# Update the value of an existing environment variable
$ astrocloud deployment variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv --update --key AIRFLOW__CORE__PARALLELISM --value <my-new-value>
```

## Related Commands

- [`astrocloud deployment variable list`](cli-reference/astrocloud-deployment-variable-list.md)
- [`astrocloud deployment variable update`](cli-reference/astrocloud-deployment-variable-update.md)
