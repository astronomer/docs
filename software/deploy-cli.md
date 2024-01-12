---
sidebar_label: 'Deploy code using the CLI'
title: 'Deploy code to Astronomer Software using the Astro CLI'
id: deploy-cli
description: How to push DAGs to your Airflow Deployment on Astronomer Software using the Astro CLI.
---

To run your code on Astronomer Software, you need to deploy it to a Deployment. You can deploy part or all of an Astro project to an Astro Deployment using the Astro CLI.

If you've used the Astro CLI to develop locally, the process for deploying your DAGs to an Airflow Deployment on Astronomer should be equally familiar. The Astro CLI builds your DAGs into a Docker image alongside all the other files in your Astro project directory, including your Python and OS-level packages, your Dockerfile, and your plugins. The resulting image is then used to generate a set of Docker containers for each core Airflow component.

For guidance on automating this process, refer to [Deploy to Astronomer via CI/CD](ci-cd.md). To learn how to add Python and OS-level packages or otherwise customize your Docker image, read [Customize your image](customize-image.md).

In addition to deploying using the Astro CLI, you can configure an alternative deploy mechanism for your DAGs. For more information, see: 

- [Deploy DAGs to an NFS volume](deploy-nfs.md)
- [Deploy DAGs using git-sync](deploy-nfs.md).

:::info

Astronomer recommends that all users use the Astro CLI to test their code locally before pushing it to an Airflow Deployment on Astronomer. For guidelines on developing locally, see [CLI Quickstart](https://docs.astronomer.io/astro/cli/install-cli).

:::

## Prerequisites

In order to push up DAGs to a Deployment on Astronomer, you must have:

* [The Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) installed.
* Access to an Astronomer platform at `https://app.BASEDOMAIN`.
* An Astronomer [Workspace](manage-workspaces.md) with at least one active [Airflow Deployment](configure-deployment.md).

## Step 1: Authenticate to Astronomer

To authenticate with the Astro CLI, run:

```sh
astro login BASEDOMAIN
```

## Step 2: Confirm Your Workspace and Deployment

From the Astro CLI, you can push code to any Airflow Deployment you have access to as long as you have the appropriate deployment-level permissions. For more information on both Workspace and Deployment-level permissions on Astronomer, see [User permissions](workspace-permissions.md).

Before you deploy to Astronomer, make sure that the Airflow Deployment you'd like to deploy to is within the Workspace you're operating in.

To see the list of Workspaces you have access to, run:

```sh
astro workspace list
```

To switch between Workspaces, run:

```sh
astro workspace switch
```

To see the list of Deployments within a particular Workspace, run:

```sh
astro deployment list
```

For more specific CLI guidelines and commands, read [CLI quickstart](https://docs.astronomer.io/astro/cli/install-cli).

## Step 3: Deploy to Astronomer

Finally, make sure you're in the correct Astro project directory.

When you're ready to deploy your DAGs, run:

```sh
astro deploy
```

This command returns a list of Airflow Deployments available in your Workspace and prompts you to pick one. After you execute the command, all files in your Astro project directory are built into a new Docker image and Docker containers for all Airflow components are restarted.

:::info

If your code deploy fails and you configured your CLI to use Podman, you might need to set an additional environment variable. See [Troubleshoot your Podman configuration](https://docs.astronomer.io/astro/cli/configure-cli#troubleshoot-your-configuration). 

:::

## Step 4: Validate Your Changes

If it's your first time deploying, expect to wait a few minutes for the Docker image to build.

To confirm that your deploy was successful, navigate to your Deployment in the Software UI and click **Open Airflow** to see your changes in the Airflow UI.

### What gets deployed?

Everything in the project directory where you ran `$ astro dev init` is bundled into a Docker image and deployed to your Airflow Deployment on your Astronomer platform. This includes system-level dependencies, Python-level dependencies, DAGs, and your `Dockerfile`.

Astronomer exclusively deploys the code in your project and does not push any of the metadata associated with your local Airflow environment, including task history and Airflow connections or variables set locally in the Airflow UI.

For more information about what gets built into your image, read [Customize your image](customize-image.md).

## Deploy DAGs only using the Astro CLI

DAG-only deploys are the fastest way to deploy code to Astronomer Software. They are recommended if you only need to deploy changes made to the `dags` directory of your Astro project.

DAG-only deploys are enabled by default on all Deployments on Astronomer Software. When they are enabled, you must still do a full project deploy when you make a change to any file in your Astro project that is not in the `dags` directory, or when you [upgrade Astro Runtime](manage-airflow-versions.md).

DAG-only deploys have the following benefits:

- DAG-only deploys are significantly faster than project deploys.
- Deployments pick up DAG-only deploys without restarting. This results in a more efficient use of workers and no downtime for your Deployments.
- If you have a CI/CD process that includes both DAG and image-based deploys, you can use your repository's permissions to control which users can perform which kinds of deploys.
- You can use DAG deploys to update your DAGs when you have slow upload speed on your internet connection.

### Enable the feature

[Insert instructions]

### Trigger a DAG-only deploy

To trigger a DAG-only deploy, run the following command from the terminal or your CI/CD process:

```sh
astro deploy --dags
```

### How DAG-only deploys work

Each Deployment includes a server that processes DAG only deploys called the `dag-server`. When a user triggers a DAG-only deploy to a Deployment:

- The Astro CLI bundles the DAG code as a TAR file and pushes it to the server.
- The server sends a signal to each Airflow component in the Deployment that there's new code to run.
- The Airflow components download the new DAG code and begin running it. 

If you deploy DAGs to a Deployment that is running a previous version of your code, then the following happens:

- Tasks that are `running` continue to run on existing workers and are not interrupted unless the task does not complete within 24 hours of the code deploy.
- One or more new workers are created alongside your existing workers and immediately start executing scheduled tasks based on your latest code.

    These new workers execute downstream tasks of DAG runs that are in progress. For example, if you deploy to Astronomer when `Task A` of your DAG is running, `Task A` continues to run on an old Celery worker. If `Task B` and `Task C` are downstream of `Task A`, they are both scheduled on new Celery workers running your latest code.

    This means that DAG runs could fail due to downstream tasks running code from a different source than their upstream tasks. DAG runs that fail this way need to be fully restarted from the Airflow UI so that all tasks are executed based on the same source code.
