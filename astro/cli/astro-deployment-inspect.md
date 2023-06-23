---
sidebar_label: "astro deployment inspect"
title: "astro deployment inspect"
id: astro-deployment-inspect
description: Reference documentation for astro deployment inspect.
hide_table_of_contents: true
---

Inspect an Astro Deployment. This command returns a YAML or JSON representation of a Deployment's current configuration and state as shown in the Cloud UI. When the `--key` flag is used, it returns only the values specified with the flag.

For more information about how to use Deployment files, see [Manage Deployments as Code](manage-deployments-as-code.md).

## Usage

```sh
astro deployment inspect
```

When using the `--key` flag, specify the complete path of the key you want to return the value for, excluding `deployment`. For example, to return the `cluster_id` for a specific Deployment, you would run:

```sh
astro deployment inspect -n <deployment-name> --key metadata.cluster_id
```

See [Template file contents](manage-deployments-as-code.md#template-file-reference) for all possible values to return. 

## Options

| Option                    | Description                                                                                                             | Possible Values          |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `<deployment-id>`   | The ID of the Deployment to inspect.                                                | Any valid Deployment ID   |
| `-n`, `--deployment-name` | Name of the Deployment to inspect. Use as an alternative to `<deployment-id>`.                                                                                     | Any valid Deployment name |
| `-k`, `--key`             | Return only a specific configuration key for a Deployment. For example `--key configuration.cluster_id` to get a Deployment's cluster ID.       | Any valid Deployment configuration key   |
| `-o`, `--output`          | Output format can be one of: YAML or JSON. By default, inspecting a Deployment returns a file in YAML format. | `yaml` or `json`             |
| `-t`, `--template`          | Create a template file for the inspected Deployment. A template file is a configuration file that includes all information about a Deployment except for its name, description field, and unique metadata. | None            |
| `--workspace-id`          | Specify a Workspace to run this command for a Deployment that is outside of your current Workspace.                                               | Any valid Workspace ID   |

## Examples

```sh
# Shows a list of Deployments to inspect and prompts you to choose one
$ astro deployment inspect

# Shows a specific Deployment's configuration
$ astro deployment inspect <deployment-id>

# Shows a specific Deployment's health status
$ astro deployment inspect <deployment-id> --key metadata.status

# Save the current state of a Deployment to a YAML Deployment file
$ astro deployment inspect <deployment-id> > deployment.yaml

# Save a Deployment as a JSON template file
$ astro deployment inspect <deployment-id> --template -o json > deployment.json
```

## Related Commands

- [`astro deployment list`](cli/astro-deployment-list.md)
- [`astro deployment create`](cli/astro-deployment-create.md)
