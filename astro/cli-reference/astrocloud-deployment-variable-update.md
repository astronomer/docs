---
sidebar_label: "astrocloud deployment variable update"
title: "astrocloud deployment variable update"
id: astrocloud-deployment-variable-update
description: Reference documentation for astrocloud deployment variable update.
---

## Description

For a given Deployment on Astro, use `astrocloud deployment variable update` to update the value of an existing environment variable via the Astro CLI. You can do so either by:

- Manually entering a new `--value` for a given `--key` in your command line
- Modifying the value of any environment variable in a `.env` file and loading that change with `--load`

If you choose to specify `--key` and `--value` instead of loading a file, you can only update one environment variable at a time.

This command is functionally identical to editing and saving the `value` of an existing environment variable via the Cloud UI. For more information on environment variables, see [Set Environment Variables on Astro](environment-variables.md).

## Usage

```sh
astrocloud deployment variable update
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |       The Deployment whose environment variable(s) you want to update                           | Any valid Deployment ID |
| `-e`,`--env`                  | The path to a file that contains a list of environment variables.  If a filepath isn't specified, this looks for a `.env` file in your current directory. If `.env` doesn't exist, this flag will create it for you                                                                 | Any valid filepath       |
| `-k`,`--key`             | The environment variable key                                                  | Any string |
| `-l`,`--load`    | Load updated environment variables from a file. Specify this flag if the variables you want to update are in that file. This is an alternative to updating an environment variable by manually specifying `--key` and `--value`             |`` |
| `-s`,`--secret`    | Set the value of the updated environment variable as secret      |`` |
| `-v`,`--value`    | The environment variable value          |`` |
| `-w`,`--workspace-id`          | Update an environment variable for a Deployment that is not in your current Workspace. If this is not specified, your current Workspace is assumed           | Any valid Workspace ID

## Examples

```sh
# Update an existing environment variable and set as secret
$ astrocloud deployment variable update --deployment-id cl03oiq7d80402nwn7fsl3dmv --key AIRFLOW__SECRETS__BACKEND_KWARGS --value <my-new-secret-value> --secret

# Update multiple environment variables for a Deployment at once by loading them from a .env file
$ astrocloud deployment variable update --deployment-id cl03oiq7d80402nwn7fsl3dmv --load --env .env.dev
```

## Related Commands

- [`astrocloud deployment variable create`](cli-reference/astrocloud-deployment-variable-create.md)
- [`astrocloud deployment variable list`](cli-reference/astrocloud-deployment-variable-list.md)
