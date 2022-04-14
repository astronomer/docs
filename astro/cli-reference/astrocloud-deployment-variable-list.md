---
sidebar_label: "astrocloud deployment variable list"
title: "astrocloud deployment variable list"
id: astrocloud-deployment-variable-list
description: Reference documentation for astrocloud deployment variable list.
---

## Description

List a Deployment's environment variables and save them to a local `.env` file. If an environment variable is secret, the CLI will list only its key.

## Usage

```sh
astrocloud deployment variable list
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |     The Deployment to list variables for                                                | Any valid Deployment ID |
| `-e`,`--env`                  | The directory where the `.env` file will be generated (default is your current directory)                                                                 | Any valid filepath       |
| `-k`,`--key`             | Only list the variable with the provided key                                                  | Any string |
| `-s`,`--save`    | Save environment variables to an environment file               |`` |
| `-w`,`--workspace-id`          | List environment variables for a Deployment outside of your current Workspace           | Any valid Workspace ID                                                         |

## Examples

```sh
# Save environment variables from a specific Directory as an `.env` file in your current directory
$ astrocloud deployment variable list cl03oiq7d80402nwn7fsl3dmv --save

# Save a single variable to an `.env` file outside of your current directory
$ astrocloud deployment variable list cl03oiq7d80402nwn7fsl3dmv --save --env /users/myaccount/documents/myproject --key AIRFLOW_VAR_MY_VAR
```

## Related Commands

- [`astrocloud deployment variable create`](cli-reference/astrocloud-deployment-variable-create.md)
