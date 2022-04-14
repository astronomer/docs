---
sidebar_label: "astrocloud deployment variable create"
title: "astrocloud deployment variable create"
id: astrocloud-deployment-variable-create
description: Reference documentation for astrocloud deployment variable create.
---

## Description

Create Deployment-level environment variables by supplying either a key and value or an environment file with a list of keys and values.

## Usage

```sh
astrocloud deployment variable create
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |       The Deployment to create variable(s) for                             | Any valid Deployment ID |
| `-e`,`--env`                  | Location of file to load environment variables from (default is `.env` in your current directory)                                                                  | Any valid filepath       |
| `-k`,`--key`             | The key for a new variable                                                  | Any string |
| `-l`,`--load`    | Create environment variables based on an `.env` file             |`` |
| `-s`,`--secret`    | Set the new environment variable as a secret          |`` |
| `-u`,`--update`    | Update an existing variable with the specified key         |Any string |
| `-v`,`--value`    | Value for the new variable          |`` |
| `-w`,`--workspace-id`          | List environment variables for a Deployment outside of your current Workspace           | Any valid Workspace ID                                                         |

## Examples

```sh
# Create a new secret environment variable
$ astrocloud deployment variable create cl03oiq7d80402nwn7fsl3dmv --key AIRFLOW_VAR_MY_VAR --value my-secret-value --secret

# Set multiple variables at once using an .env file
$ astrocloud deployment variable create cl03oiq7d80402nwn7fsl3dmv --load --env /users/documents/my-astro-project/.my-env

# Update an existing variable
$ astrocloud deployment variable create cl03oiq7d80402nwn7fsl3dmv --update AIRFLOW_VAR_MY_VAR --value my-updated-value
```

## Related Commands

- [`astrocloud deployment variable list`](cli-reference/astrocloud-deployment-variable-list.md)
