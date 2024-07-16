---
sidebar_label: 'Deploy a project image'
title: 'Deploy code to Astronomer Software using the Astro CLI'
id: deploy-cli
description: How to push DAGs to your Airflow Deployment on Astronomer Software using the Astro CLI.
---

To run your code on Astronomer Software, you need to deploy it to an Airflow Deployment. You can deploy part or all of an Astro project to an Airflow Deployment using the Astro CLI.

When you deploy a project, the Astro CLI builds your all files in your Astro project, including DAGs, into a Docker image. It then pushes this image to an image registry on your Astronomer Software cluster where your Deployment accesses the image and uses it to run Airflow containers.

For guidance on automating this process, refer to [Deploy to Astronomer via CI/CD](ci-cd.md). To learn how to add Python and OS-level packages or otherwise customize your Docker image, read [Customize your image](customize-image.md).

This document covers deploying a complete project image to Astro. To deploy DAGs only, see:

- [Deploy DAGs using the Astro CLI](deploy-dags.md)
- [Deploy DAGs to an NFS volume](deploy-nfs.md)
- [Deploy DAGs using git-sync](deploy-nfs.md).

:::info

Astronomer recommends that all users use the Astro CLI to test their code locally before pushing it to an Airflow Deployment on Astronomer. For guidelines on developing locally, see [CLI Quickstart](https://www.astronomer.io/docs/astro/cli/install-cli).

:::

## Prerequisites

In order to push up DAGs to a Deployment on Astronomer, you must have:

* [The Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli) installed.
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

For more specific CLI guidelines and commands, read [CLI quickstart](https://www.astronomer.io/docs/astro/cli/install-cli).

## Step 3: Deploy to Astronomer

Finally, make sure you're in the correct Astro project directory.

When you're ready to deploy your DAGs, run:

```sh
astro deploy
```

This command returns a list of Airflow Deployments available in your Workspace and prompts you to pick one. After you execute the command, all files in your Astro project directory are built into a new Docker image, the image is pushed to the Astronomer Software registry, and the containers for all Airflow components in the Deployment are restarted.

:::info

If your code deploy fails and you configured your CLI to use Podman, you might need to set an additional environment variable. See [Troubleshoot your Podman configuration](https://www.astronomer.io/docs/astro/cli/configure-cli#troubleshoot-your-configuration).

:::

## Step 4: Validate Your Changes

If it's your first time deploying, expect to wait a few minutes for the Docker image to build.

To confirm that your deploy was successful, navigate to your Deployment in the Software UI and click **Open Airflow** to see your changes in the Airflow UI.

### What gets deployed?

Everything in the project directory where you ran `$ astro dev init` is bundled into a Docker image and deployed to your Airflow Deployment on your Astronomer platform. This includes system-level dependencies, Python-level dependencies, DAGs, and your `Dockerfile`.

Astronomer exclusively deploys the code in your project and does not push any of the metadata associated with your local Airflow environment, including task history and Airflow connections or variables set locally in the Airflow UI.

For more information about what gets built into your image, read [Customize your image](customize-image.md).
