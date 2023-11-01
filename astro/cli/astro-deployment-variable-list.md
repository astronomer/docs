---
sidebar_label: "astro deployment variable list"
title: "astro deployment variable list"
id: astro-deployment-variable-list
description: List Deployment environment variables.
hide_table_of_contents: true
---

For a given Deployment on Astro, list its running environment variables in your terminal. To test these environment variables locally without having to manually copy them, you can also use this command to save them in a local `.env` file.

If an existing `.env` file already exists in your current directory, `--save` will append environment variables to the bottom of that file. It will not override or replace its contents. If `.env` does not exist, `--save` will create the file for you.

If an environment variable value is set as secret, the CLI will list only its key.

## Usage

```sh
astro deployment variable list
```

:::tip

To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), set the following OS-level environment variables in a way that the Astro CLI can access them:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

After setting the variables, this command works for a Deployment without you having to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |    The ID of the Deployment for which to list environment variables                                                | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment for which to list environment variable(s). Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-e`,`--env`                  | The directory where a `.env` file will be created if it does not exist. If not specified, it will be created in your current directory                                                                 | Any valid filepath       |
| `-k`,`--key`             | List only the environment variable associated with this key. If not specified, all environment variables are listed                                                  | Any string |
| `-s`,`--save`    | Save environment variables to a local `.env` file               |`` |
| `-w`,`--workspace-id`          | List environment variables for a Deployment that is not in your current Workspace. If not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |

## Examples

```sh
# Save all environment variables currently running on an Astro Deployment to the `.env` file in your current directory
$ astro deployment variable list --deployment-id cl03oiq7d80402nwn7fsl3dmv --save

# Save only a single environment variable from a Deployment on Astro to a `.env` file that is outside of your current directory
$ astro deployment variable list --deployment-name="My Deployment" --key AIRFLOW__CORE__PARALLELISM --save --env /users/documents/my-astro-project/.env
```

## Related Commands

- [`astro deployment variable create`](cli/astro-deployment-variable-create.md)
- [`astro deployment variable update`](cli/astro-deployment-variable-update.md)
