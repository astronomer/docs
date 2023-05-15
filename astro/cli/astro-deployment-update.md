---
sidebar_label: "astro deployment update"
title: "astro deployment update"
id: astro-deployment-update
description: Reference documentation for astro deployment update.
hide_table_of_contents: true
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


Update the configuration for a Deployment on Astro. 

:::info

To update existing worker queues or to create new queues for an existing Deployment, you must update your Deployment by using the `--deployment-file` flag to update a [Deployment file](manage-deployments-as-code.md#create-a-template-file-from-an-existing-deployment).

:::

## Usage

```sh
astro deployment update <deployment-id> <flags>
```

:::tip

To run this command in an automated process such as a [CI/CD pipeline](set-up-ci-cd.md), set the following OS-level environment variables in a way that the Astro CLI can access them:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

After setting the variables, this command works for a Deployment and you don't need to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

:::

## Options

| Option                         | Description                                                                            | Possible Values                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `--dag-deploy` |Enable or disable DAG-only deploys for the Deployment.                                                                                                                         | Either `enable` or `disable`. Contact [Astronomer support](https://cloud.astronomer.io/support) before using `disable` to disable the feature.                                                             |
| `--deployment-file`        | Location of the Deployment file to update the Deployment with. The file format can be JSON or YAML. See [Create a Deployment with a Deployment File](manage-deployments-as-code.md#create-a-template-file-from-an-existing-deployment).                                                                                                        | A valid file path to any YAML or JSON Deployment file             |
| `<deployment-id>` (_Required_) | The ID of the Deployment to update                                                               | Any valid Deployment ID                                                        |
| `--deployment-name` | The name of the Deployment to update. Use as an alternative to `<deployment-id>`. | Any valid Deployment name                                            |
| `-d`,`--description`           | The description for the Deployment                                                     | Any string. Multiple-word descriptions should be specified in quotations (`"`) |
| `-l`,`--name`                  | The Deployment's name                                                                  | Any string. Multiple-word descriptions should be specified in quotations       |
| `-s`,`--scheduler-au`          | The number of AU to allocate towards the Deployment's Scheduler(s). The default is`5`. | Integer between `0` and `24`                                                   |
| `-r`,`--scheduler-replicas`    | The number of scheduler replicas for the Deployment. The default is `1`.               | Integer between `0` and `4`                                                    |
| `-f`,`--force`          | Force a Deployment update                             | None                                                                             |
| `-w`,`--workspace-id`          | Specify a Workspace to update a Deployment outside of your current Workspace           | Any valid Workspace ID                                                         |

## Examples

```sh
# Update a Deployment's name and description
$ astro deployment update cl03oiq7d80402nwn7fsl3dmv -d="My Deployment Description" --name="My Deployment Name"

# Force update a Deployment
$ astro deployment update cl03oiq7d80402nwn7fsl3dmv -d="My Deployment Description" --force

# Update the Deployment according to the configurations specified in the YAML Deployment file
$ astro deployment update --deployment-file deployment.yaml
```

</TabItem>

<TabItem value="software">

Create a Deployment on Astronomer Software. This command is functionally identical to using the Software UI to create a Deployment.

## Usage

```sh
astro deployment update <deployment-id>
```

## Options

| Option                        | Description                                                                                                                                                        | Possible Values                                                                                                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| `<deployment-id>` (_Required_) | The ID for the Deployment to update | Any valid Deployment ID |
| `-a`,`--airflow-version`      | The version of Astronomer Certified to use for the Deployment                                                                                                      | Any supported version of Astronomer Certified                                                                                        |  |
| `-c`, `--cloud-role`          | An AWS or GCP IAM role to append to your Deployment's webserver, scheduler, and worker Pods                                                                      | Any string                                                                                                                           |
| `-t`, `--dag-deployment-type` | The DAG deploy method for the Deployment                                                                                                                         | Can be either `image`, `git_sync`, or `volume`. The default is `image`                                                             |
| `-d`,`--description`          | The description for the Deployment                                                                                                                                 | Any string. Multiple-word descriptions should be specified in quotations (`"`)                                                       |
| `-e`, `--executor`            | The executor type for the Deployment                                                                                                                              | `local`, `celery`, or `kubernetes`. The default value is `celery`                                                                    |
| `-b`, `--git-branch-name`     | The branch name of the git repo to sync your Deployment from. Must be specified with `--dag-deployment-type=git_sync`                                              | Any valid git branch name                                                                                                            |  |
| `-u`, `--git-repository-url`  | The URL for the git repository to sync your Deployment from. Must be specified with `--dag-deployment-type=git_sync`                                               | Any valid git repository URL                                                                                                         |
| `-v`, `--git-revision`        | The commit reference of the branch that you want to sync with your Deployment. Must be specified with `--dag-deployment-type=git_sync`                             | Any valid git revision                                                                                                               |
| `--known-hosts`               | The public key for your Git provider, which can be retrieved using `ssh-keyscan -t rsa <provider-domain>`. Must be specified with `--dag-deployment-type=git_sync` | Any valid public key                                                                                                                 |
| `-l`,`--label`                | The label for your Deployment                                                                                                                                      | Any string                                                                                                                           |
| `-n`,`--nfs-location`         | The location for an NFS volume mount. Must be specified with `--dag-deployment-type=volume`                                                                       | An NFS volume mount specified as: `<IP>:/<path>`. Input is automatically prepended with `nfs:/` - do not include this in your input |
| `-r`,`--release-name`         | A custom release name for the Deployment. See [Customize release names](https://docs.astronomer.io/software/configure-deployment#customize-release-names)          | Any string of alphanumeric and hyphen characters                                                                                     |
| `--runtime-version`           | The Astro Runtime version for the Deployment                                                                                                                       | Any supported version of Astro Runtime. Major, minor, and patch versions must be specified                                          |
| `--ssh-key`                   | The SSH private key for your Git repository. Must be specified with `--dag-deployment-type=git_sync`                                                               | Any valid SSH key                                                                                                                    |
| `-s`,`--sync-interval`        | The time interval between checks for updates in your Git repository, in seconds. Must be specified with `--dag-deployment-type=git_sync`                           | Any integer                                                                                                                          |
| `-t`,`--triggerer-replicas`   | Number of replicas to use for the Airflow triggerer                                                                                                                | Any integer between 0 - 2. The default value is 1                                                                                 |
| `--workspace-id`              | The Workspace in which to create a Deployment. If not specified, your current Workspace is assumed                                                                | Any valid Workspace ID                                                                                                               |

## Examples

```sh
$ astro deployment update telescopic-sky-4599 --executor kubernetes
# Change the executor for a Deployment

$ astro deployment update telescopic-sky-4599 -l="My Deployment label" --workspace-id="ckwqkz36200140ror6axh8p19"
# Update a Deployment in a separate Workspace. The CLI will not prompt you for more information
```

</TabItem>
</Tabs>

## Related commands

- [`astro deployment delete`](cli/astro-deployment-delete.md)
- [`astro deployment list`](cli/astro-deployment-list.md)
