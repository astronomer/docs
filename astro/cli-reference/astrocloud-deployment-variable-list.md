---
sidebar_label: "astrocloud deployment variable list"
title: "astrocloud deployment variable list"
id: astrocloud-deployment-variable-list
description: Reference documentation for astrocloud deployment variable list.
---

## Description

For a given Deployment on Astro, list its running environment variables in your terminal. To test these environment variables locally without having to manually copy them, you can also use this command to save them in a local `.env` file.

If an existing `.env` file already exists in your current directory, `--save` will append environment variables to the bottom of that file. It will not override or replace its contents. If `.env` does not exist, `--save` will create the file for you.

If an environment variable value is set as secret, the CLI will list only its key.

## Usage

```sh
astrocloud deployment variable list
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The Deployment for which to list environment variables                                                | Any valid Deployment ID |
| `-e`,`--env`                  | The directory where a `.env` file will be created if it does not exist. If not specified, it will be created in your current directory                                                                 | Any valid filepath       |
| `-k`,`--key`             | List only the environment variable associated with this key. If not specified, all environment variables are listed                                                  | Any string |
| `-s`,`--save`    | Save environment variables to a local `.env` file               |`` |
| `-w`,`--workspace-id`          | List environment variables for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |

## Examples

```sh
# Save all environment variables currently running on an Astro Deployment to the `.env` file in your current directory
$ astrocloud deployment variable list cl03oiq7d80402nwn7fsl3dmv --save

# Save only a single environment variable from a Deployment on Astro to a `.env` file that is outside of your current directory
$ astrocloud deployment variable list cl03oiq7d80402nwn7fsl3dmv --key AIRFLOW__CORE__PARALLELISM --save --env /users/documents/my-astro-project/.env
```

## Related Commands

- [`astrocloud deployment variable create`](cli-reference/astrocloud-deployment-variable-create.md)
