---
sidebar_label: 'Configure git-sync deploys'
title: 'Configure git-sync code deploys'
id: deploy-git-sync
description: Push DAGs to your Airflow Deployment on Astronomer Software using git-sync.
---

Starting with Astronomer v0.27, you can deploy DAGs to an Astronomer Deployment using [git-sync](https://github.com/kubernetes/git-sync). After setting up this feature, you can deploy DAGs from a Git repository without any additional CI/CD. DAGs deployed via git-sync automatically appear in the Airflow UI without requiring additional action or causing downtime.

This guide provides setup steps for configuring git-sync as a DAG deploy option.

:::warning
This is currently an experimental feature because it relies on very frequent syncs with remote Git servers. If you have conservative rate limits on your Git repos, then we do not recommend using this feature until a more stable git-sync architecture has been implemented. For more information, reach out to [Astronomer support](https://support.astronomer.io/).
:::

## Prerequisites

To enable the git-sync deploy feature, you need:

- A Software installation running an OSS Airflow Chart (this is the default for most installations).
- Permission to push new configuration changes to your Software installation.

To configure a git-sync deploy mechanism for a Deployment on Astronomer, you need Workspace Editor permissions.

To deploy DAGs to a Deployment using a git-sync deploy mechanism, you need permission to push code to a Git repository configured for git-sync deploys.

## Enable git-sync

Git-sync deploys must be explicitly enabled on Astronomer by a System Admin. To enable it, update your `config.yaml` file with the following values:

```yaml
astronomer:
  houston:
    config:
      deployments:
        configureDagDeployment: true
        gitSyncDagDeployment: true
```

## Configure a Git repo for git-sync deploys

The Git repo you want to sync should contain a directory of DAGs that you want to deploy to Astronomer. You can include additional files in the repo, such as your other Astro project files, but note that this might affect performance when deploying new changes to DAGs.

If you want to deploy DAGs via a private Git repo, you additionally need to configure SSH so that your Astronomer Deployment can access the contents of the repo. This process varies slightly between Git repository management tools. For an example of this configuration, read GitLab's [SSH Key](https://docs.gitlab.com/ee/user/ssh.html) documentation.

## Configure your Astronomer Deployment

Workspace editors can configure a new or existing Airflow Deployment to use a git-sync mechanism for DAG deploys. From there, any member of your organization with write permissions to the Git repository can deploy DAGs to the Deployment. To configure a Deployment for git-sync deploys:

1. In the Software UI, create a new Airflow Deployment or open an existing one.
2. Go to the **DAG Deployment** section of the Deployment's Settings page.
3. For your **Mechanism**, select **Git Sync.**
4. Configure the following values:

    - **Repository URL**: The URL for the Git repository that hosts your Astro project
    - **Branch Name**: The name of the Git branch that you want to sync with your Deployment
    - **Sync Interval**: The time interval between checks for updates in your Git repository, in seconds. A sync is only performed when an update is detected. We recommend a 1 second interval
    - **DAGs Directory:** The directory in your Git repository that hosts your DAGs. Specify the directory's path as relative to the repository's root directory. To use your root directory as your DAGs directory, specify this value as `./`. Other changes outside the DAGs directory in your Git repository must be deployed using `astro deploy`
    - **Rev**: The commit reference of the branch that you want to sync with your Deployment
    - **Ssh Key**: The SSH private key for your Git repository
    - **Known Hosts**: The public key for your Git provider, which can be retrieved using `ssh-keyscan -t rsa <provider-domain>`. For an example of how to retrieve GitHub's public key, refer to [Apache Airflow documentation](https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#production-guide-knownhosts).
    - **Ephemeral Storage Overwrite Gigabytes**: The storage limit for your Git repository. If your Git repo is larger than 2GB, we recommend setting this slider to your repo size + 1 Gi
    - **Sync Timeout**: The maximum amount of seconds allowed for a sync. We recommend increasing this value if your repo is larger than 1GB

5. Save your changes.

Once you configure your Deployment, any code pushes to your DAG directory of the specified Git repo and branch will appear in your Deployment with zero downtime.

:::tip
Newly created DAG files can take up to five minutes (default configuration) from syncing to appear in the Airflow UI. To shorten this delay, we recommend tuning `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL` in your Airflow deployment.
:::
