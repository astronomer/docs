---
sidebar_label: "astro deployment variable update"
title: "astro deployment variable update"
id: astro-deployment-variable-update
description: Reference documentation for astro deployment variable update.
---

## Description

For a given Deployment on Astro, use `astro deployment variable update` to update the value of an existing environment variable via the Astro CLI. To do so, you can either:

- Manually enter a new `--value` in your command line for a given `--key`, or
- Modify the value of one or more environment variables in a `.env` file and load that file with `--load`.

If you choose to specify `--key` and `--value` instead of loading a file, you can only update one environment variable at a time.

This command is functionally identical to editing and saving the `value` of an existing environment variable via the Cloud UI. For more information on environment variables, see [Set Environment Variables on Astro](environment-variables.md).

## Usage

```sh
astro deployment variable update
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
$ astro deployment variable update --deployment-id cl03oiq7d80402nwn7fsl3dmv --key AIRFLOW__SECRETS__BACKEND_KWARGS --value <my-new-secret-value> --secret

# Update multiple environment variables for a Deployment at once by loading them from a .env file
$ astro deployment variable update --deployment-id cl03oiq7d80402nwn7fsl3dmv --load --env .env.dev
```

## Related Commands

- [`astro deployment variable create`](cli/astro-deployment-variable-create.md)
- [`astro deployment variable list`](cli/astro-deployment-variable-list.md)
