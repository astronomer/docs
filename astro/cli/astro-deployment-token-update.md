---
sidebar_label: "astro deployment token update"
title: "astro deployment token update"
id: astro-deployment-token-update
description: Update your Deployment API tokens.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

:::cliastroonly
:::

Update an Astro [Deployment API Token](deployment-api-tokens.md)

To use your API token in an automated process, see [Authenticate an automation tool](automation-authentication.md).

## Usage

```sh
astro deployment update --deployment-id=<deployment-id> [flags]
```

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
|`--cicd-enforcement`           |    When enabled CI/CD Enforcement where deploys to deployment must use an API Key or Token. This essentially forces Deploys to happen through CI/CD.                                                | `disable` or `enable` |
| `-c`,`--clean-output`           |    Clean output to only include inspect yaml or json file in any situation.                                                | String |
|`--dag-deploy`           |    Description of the token. If the description contains a space, specify the entire description within quotes ""                                                | A string |
| `--default-task-pod-cpu`           |    The Default Task Pod CPU to use for the Deployment.                                                 | Numeric. Example value: `0.25` |
| `--default-task-pod-memory` | The Default Taks Pod Memory to use for the Deployment. | String. Example value: 0.5Gi |
| `--deployment-file` | Location of file containing the deployment to update. File can be in either JSON or YAML format. | Valid file path |
| `--deployment-name` | Description of the Deployment. If the description contains a space, specify the entire description in quotes "". | String |
| `-e`,`--executor`           |    The executor to use for the deployment.                                               | `CeleryExecutor` or `KubernetesExecutor`. |
| `-f`,`--force`           |    Force update: Don't prompt a user before Deployment update.                                                | `True` or `False` |
| `-a`,`--high-availability`           |    Enables High Availability for the Deployment.                                                | `True` or `False` |
| `-n`, `--name` | Update the Deployment's name. If the new name contains a space, specify the entire name within quotes "". | String |
| `--resource-quota-cpu` | The Resource Quota CPU to use for the Deployment. | Numeric. The Resource Quota CPU to use for the Deployment. Example value: `10`. |
| `--scheduler-size` | The size of Scheduler for the Deployment. | `small`, `medium`, `large` |
| `-w`, `--workspace-id` | Workspace where the Deployment is located. | A valid Workspace ID. |

## Examples

```bash
# The CLI prompts you to input a role for a token with Token ID assigned to a specific Deployment
astro deployment token update TOKEN_ID --deployment-id=clukapi6r000008l58530cg8i

# The CLI prompts you to input a role for a token identified by its name
astro deployment token update --deployment-id=clukapi6r000008l58530cg8i -name=TOKEN_NAME

# The CLI prompts you to select the token from a list and input a role
astro deployment token update --deployment-id=clukapi6r000008l58530cg8i

# This command assigns a token with the specified TOKEN_ID the role `Deployment Admin` to a Deployment with the following ID.
astro deployment token update TOKEN_ID --deployment-id=clukapi6r000008l58530cg8i --role=DEPLOYMENT_ADMIN
```

## Related Commands

- [`astro deployment token create`](cli/astro-deployment-create.md)
- [`astro deployment token list`](cli/astro-deployment-token-list.md)
- [`astro deployment token rotate`](cli/astro-deployment-token-rotate.md)
