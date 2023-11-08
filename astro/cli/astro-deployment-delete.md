---
sidebar_label: "astro deployment delete"
title: "astro deployment delete"
id: astro-deployment-delete
description: Delete a Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' } 
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info  

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change product contexts. 

:::

<Tabs
    defaultValue="astro"
    values={[
        {label: 'Astro', value: 'astro'},
        {label: 'Software', value: 'software'},
    ]}>
<TabItem value="astro">

Delete a Deployment on Astro. This command is functionally identical to deleting a Deployment in the Cloud UI.

When you run `astro deployment delete`, you are prompted to select from a list of Deployments that you can access in your Workspace. You can bypass this prompt and specify a Deployment name or ID in the command. To retrieve a Deployment ID, open your Deployment in the Cloud UI and copy the value in the **ID** section of the Deployment page. You can also run `astro deployment list` to find a Deployment ID or name.

:::info

To complete this action, [Workspace Owner](user-permissions.md#workspace-roles) permissions are required.

:::

## Usage

```sh
astro deployment delete
```

## Options

| Option              | Description                                                                       | Possible Values           |
| ------------------- | --------------------------------------------------------------------------------- | ------------------------- |
| `<deployment-id>`   | The ID of the Deployment to delete                                                | Any valid Deployment ID   |
| `-f`,`--force`      | Do not include a confirmation prompt before deleting the Deployment               | None                      |
| `--workspace-id`    | Specify a Workspace to delete a Deployment outside of your current Workspace      | Any valid Workspace ID    |
| `--deployment-name` | The name of the Deployment to delete. Use as an alternative to `<deployment-id>`. | Any valid Deployment name |

## Examples

```sh
$ astro deployment delete
# CLI prompts you for a Deployment to delete
$ astro deployment delete ckvvfp9tf509941drl4vela81n -f
# Force delete a Deployment without a confirmation prompt
$ astro deployment delete --deployment-name="My deployment"
# Delete a Deployment by specifying its name.
```

</TabItem>

<TabItem value="software">

Delete a Deployment on Astronomer Software. This command is functionally identical to deleting a Deployment with the Software UI.

## Usage

```sh
astro deployment delete
```

## Options

| Option                         | Description                                                                                                                                                                   | Possible Values         |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `<deployment-id>` (_Required_) | The ID of the Deployment to delete                                                                                                                                            | Any valid Deployment ID |
| `-h`,`--hard`                  | Deletes all infrastructure and records for this Deployment. See [Hard delete a Deployment](https://docs.astronomer.io/software/configure-deployment#hard-delete-a-deployment) | None                    |

</TabItem>
</Tabs>


## Related commands

- [`astro deployment create`](cli/astro-deployment-create.md)
- [`astro deployment list`](cli/astro-deployment-list.md)
