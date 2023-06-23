---
sidebar_label: "astro deployment create"
title: "astro deployment create"
id: astro-deployment-create
description: Reference documentation for astro deployment create.
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

Create a Deployment on Astro. This command is functionally identical to using the Cloud UI to [create a Deployment](create-deployment.md).

## Usage

```sh
astro deployment create
```

When you use `astro deployment create`, it creates a Deployment with a default Worker Queue that uses default worker types.

Some Deployment configurations, including worker queue and worker type, can be set only by using the `--deployment-file` flag to apply a Deployment file. See [Manage Deployments as code](manage-deployments-as-code.md).

## Options

| Option                      | Description                                                                                                                                 | Possible Values                                                                             |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `-c`, `--cluster-id`        | The cluster in which you want to create a Deployment                                                                                        | The id of any cluster that you can create Deployments in                                  |
| `--cluster-type` | (Astro Hosted only) The type of cluster you want to run the Deployment on. | Either `"dedicated"` or `"hosted"`. |
| `--dag-deploy`        | Enables DAG-only deploys for the Deployment. The default is `disable`                                                                                                        | `enable` or `disable`             |
| `--deployment-file`        | Location of the template file that specifies the configuration of the new Deployment. File can be in either JSON or YAML format. See [Create a Deployment with a Deployment File](manage-deployments-as-code.md#create-a-deployment-with-a-deployment-file)                                                                                                       | A valid file path for YAML or JSON template file             |
| `-d`,`--description`        | The description for the Deployment                                                                                                          | Any string. Multiple-word descriptions should be specified in quotations (`"`)              |
| `--enforce-cicd`     | Specify that the Deployment can only accept code deploys from API tokens and keys. | None|
| `-e`,`--executor`        | The executor to use for the Deployment                                                                                                          |  CeleryExecutor or KubernetesExecutor             |
| `-n`,`--name`               | The name of the Deployment                                                                                                                  | Any string. Multiple-word descriptions should be specified in quotations                    |
| `--region` | The Cloud Provider region to use for the Deployment. This is a mandatory flag for Astro Hosted. | The list of regions supported for your cloud provider. See [Standard cluster configurations for supported regions](resource-reference-hosted?tab=gcp#standard-cluster-configurations). |
| `-v`,`--runtime-version`    | The Astro Runtime version for the Deployment                                                                                                | Any supported version of Astro Runtime. Major, minor, and patch versions must be specified. |
| `-s`,`--scheduler-au`       | The number of AU to allocate towards the Deployment's Scheduler(s). The default is`5`.                                                      | Integer between `0` and `24`                                                                |
| `-r`,`--scheduler-replicas` | The number of scheduler replicas for the Deployment. The default is `1`.                                                                    | Integer between `0` and `4`                                                                 |
| `--wait`                    | The time to wait for the new Deployment to have a [healthy](deployment-metrics.md#deployment-health) status before completing the command . | None                                                                                        |
| `--workspace-id`            | The Workspace in which to create a Deployment. If not specified, your current Workspace is assumed.                                         | Any valid Workspace ID                                                                      |

## Examples

```sh
# CLI prompts you for a Deployment name and cluster
$ astro deployment create

# Create a Deployment with all required information specified. The CLI will not prompt you for more information
$ astro deployment create -d="My Deployment Description" --name="My Deployment Name" --cluster-id="ckwqkz36200140ror6axh8p19"

# Specify the new Deployment's configuration with a yaml file
$ astro deployment create --deployment-file deployment.yaml
```


</TabItem>

<TabItem value="software">

Create a Deployment on Astronomer Software. This command is functionally identical to using the Software UI to create a Deployment.

## Usage

```sh
astro deployment create
```

## Options

| Option                        | Description                                                                                                                                                        | Possible Values                                                                                                                     |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| `-a`,`--airflow-version`      | The Astronomer Certified version to use for the Deployment                                                                                                         | Any supported version of Astronomer Certified                                                                                       |  |
| `-c`, `--cloud-role`          | An AWS or GCP IAM role to append to your Deployment's webserver, scheduler, and worker Pods                                                                        | Any string                                                                                                                          |
| `-t`, `--dag-deployment-type` | The DAG deploy method for the Deployment                                                                                                                           | Can be either `image`, `git_sync`, or `volume`. The default is `image`                                                              |
| `-d`,`--description`          | The description for the Deployment                                                                                                                                 | Any string. Multiple-word descriptions should be specified in quotations (`"`)                                                      |
| `-e`, `--executor`            | The executor type for the Deployment                                                                                                                               | `local`, `celery`, or `kubernetes`. The default value is `celery`                                                                   |
| `-b`, `--git-branch-name`     | The branch name of the git repo to sync your Deployment from. Must be specified with `--dag-deployment-type=git_sync`                                              | Any valid git branch name                                                                                                           |  |
| `-u`, `--git-repository-url`  | The URL for the git repository to sync your Deployment from. Must be specified with `--dag-deployment-type=git_sync`                                               | Any valid git repository URL                                                                                                        |
| `-v`, `--git-revision`        | The commit reference of the branch that you want to sync with your Deployment. Must be specified with `--dag-deployment-type=git_sync`                             | Any valid git revision                                                                                                              |
| `--known-hosts`               | The public key for your Git provider, which can be retrieved using `ssh-keyscan -t rsa <provider-domain>`. Must be specified with `--dag-deployment-type=git_sync` | Any valid public key                                                                                                                |
| `-l`,`--label`                | The label for your Deployment                                                                                                                                      | Any string                                                                                                                          |
| `-n`,`--nfs-location`         | The location for an NFS volume mount. Must be specified with `--dag-deployment-type=volume`.                                                                       | An NFS volume mount specified as: `<IP>:/<path>`. Input is automatically prepended with `nfs:/` - do not include this in your input |
| `-r`,`--release-name`         | A custom release name for the Deployment. See [Customize release names](https://docs.astronomer.io/software/configure-deployment#customize-release-names)          | Any string of alphanumeric and hyphen characters                                                                                    |
| `--runtime-version`           | The Astro Runtime version for the Deployment                                                                                                                       | Any supported version of Astro Runtime. Major, minor, and patch versions must be specified.                                         |
| `--ssh-key`                   | The SSH private key for your Git repository. Must be specified with `--dag-deployment-type=git_sync`                                                               | Any valid SSH key                                                                                                                   |
| `-s`,`--sync-interval`        | The time interval between checks for updates in your Git repository, in seconds. Must be specified with `--dag-deployment-type=git_sync`                           | Any integer                                                                                                                         |
| `-t`,`--triggerer-replicas`   | Number of replicas to use for the Airflow triggerer                                                                                                                | Any integer between 0 - 2. The default value is 1.`                                                                                 |
| `--workspace-id`              | The Workspace in which to create a Deployment. If not specified, your current Workspace is assumed                                                                 | Any valid Workspace ID                                                                                                              |

## Examples

```sh
$ astro deployment create
# CLI prompts you for a Deployment name

$ astro deployment create -l="My Deployment label" --workspace-id="ckwqkz36200140ror6axh8p19"
# Create a Deployment in a separate Workspace. The CLI will not prompt you for more information
```

</TabItem>
</Tabs>

## Related commands

- [`astro deployment delete`](cli/astro-deployment-delete.md)
- [`astro deployment list`](cli/astro-deployment-list.md)
