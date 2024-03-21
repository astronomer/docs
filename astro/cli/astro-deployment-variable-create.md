---
sidebar_label: "astro deployment variable create"
title: "astro deployment variable create"
id: astro-deployment-variable-create
description: Reference documentation for astro deployment variable create.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::info

This command is only available on Astro.

:::

For a given Deployment on Astro, create environment variables in the Astro CLI by supplying either a key and value pair or a file (for example, `.env`) with a list of keys and values. This command is functionally identical to creating an environment variable in the Astro UI. See [Set Environment Variables on Astro](environment-variables.md).

## Usage

```sh
astro deployment variable create <key>=<value>
```

:::tip

This command is recommended for automated workflows. To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), you can generate an API token, then specify the `ASTRO_API_TOKEN` environment variable in the system running the Astro CLI:

```bash
export ASTRO_API_TOKEN=<your-token>
```

See [Organization](organization-api-tokens.md), [Workspace](workspace-api-tokens.md), and [Deployment](deployment-api-tokens.md) API token documentation for more details about ways to use API tokens.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-d`,`--deployment-id`           |       The ID of the Deployment in which to create environment variable(s).                           | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment in which to create environment variable(s). Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-e`,`--env`                  | The path to a file that contains a list of environment variables.  If a filepath isn't specified, this looks for a `.env` file in your current directory. If `.env` doesn't exist, this flag will create it for you                                                                 | Any valid filepath       |
| `-l`,`--load`    | Export new environment variables from your Astro project's `.env` file to the Deployment. This is an alternative to creating an environment variable by manually specifying `--key` and `--value`. By default, this flag exports all new environment variables based on the file specified with `--env`            |`` |
| `-s`,`--secret`    | Set the value of the new environment variable as secret      |`` |
| `-w`,`--workspace-id`          | Create or update an environment variable for a Deployment that is not in your current Workspace. If this is not specified, your current Workspace is assumed           | Any valid Workspace ID                                                         |

## Examples

```sh
# Create a new secret environment variable
$ astro deployment variable create --deployment-id cl03oiq7d80402nwn7fsl3dmv AIRFLOW__SECRETS__BACKEND_KWARGS=<my-secret-value> --secret

# Create multiple environment variables for a Deployment at once by specifying multiple keys
$ astro deployment variable create AIRFLOW__CORE__PARALLELISM=32 MAX_ACTIVE_TASKS_PER_DAG=16 --deployment-id cl03oiq7d80402nwn7fsl3dmv

# Create multiple environment variables for a Deployment at once by loading them from a .env file
$ astro deployment variable create --deployment-name="My Deployment" --load --env .env.dev
```

## Related Commands

- [`astro deployment variable list`](cli/astro-deployment-variable-list.md)
- [`astro deployment variable update`](cli/astro-deployment-variable-update.md)
