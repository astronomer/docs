---
sidebar_label: "astro deployment variable update"
title: "astro deployment variable update"
id: astro-deployment-variable-update
description: Update Deployment environment variables.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

For a given Deployment on Astro, use `astro deployment variable update` to update the value of an existing environment variable with the Astro CLI. To do so, you can either:

- Manually enter a new `key=value` pair for an existing key directly in the command.
- Modify the value of one or more environment variables in a `.env` file and load that file with `--load`.

This command is functionally identical to editing and saving the value of an existing environment variable in the Cloud UI. For more information on environment variables, see [Set environment variables on Astro](manage-env-vars.md).

## Usage

```sh
astro deployment variable update
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
| `-d`,`--deployment-id`           |       The ID of the Deployment whose environment variable(s) you want to update.                           | Any valid Deployment ID |
| `--deployment-name` | The name of the Deployment whose environment variable(s) you want to update. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-e`,`--env`                  | The path to a file that contains a list of environment variables.  If a filepath isn't specified, this looks for a `.env` file in your current directory. If `.env` doesn't exist, this flag will create it for you                                                                 | Any valid filepath       |
| `-l`,`--load`    | Export updated environment variables from your Astro project's `.env` file to the Deployment. This is an alternative to updating an environment variable by manually specifying `--key` and `--value`. By default, this flag updates all environment variables based on the file specified with `--env`            |`` |
| `-s`,`--secret`    | Set the value of the updated environment variable as secret      |`` |
| `-w`,`--workspace-id`          | Update an environment variable for a Deployment that is not in your current Workspace. If this is not specified, your current Workspace is assumed           | Any valid Workspace ID

## Examples

```sh
# Update an existing environment variable and set as secret
$ astro deployment variable update --deployment-id cl03oiq7d80402nwn7fsl3dmv AIRFLOW__SECRETS__BACKEND_KWARGS=<my-new-secret-value> --secret

# Update multiple environment variables for a Deployment at once by loading them from a .env file
$ astro deployment variable update --deployment-id cl03oiq7d80402nwn7fsl3dmv --load --env .env.dev
```

## Related Commands

- [`astro deployment variable create`](cli/astro-deployment-variable-create.md)
- [`astro deployment variable list`](cli/astro-deployment-variable-list.md)
