---
sidebar_label: 'Deploy DAGs via CLI'
title: 'Deploy DAGs to Astronomer Software via CLI'
id: deploy-cli
description: How to push DAGs to your Airflow Deployment on Astronomer Software using the Astro CLI.
---


If you've used the Astro CLI to develop locally, the process for deploying your DAGs to an Airflow Deployment on Astronomer should be equally familiar. The Astro CLI builds your DAGs into a Docker image alongside all the other files in your Astro project directory, including your Python and OS-level packages, your Dockerfile, and your plugins. The resulting image is then used to generate a set of Docker containers for each core Airflow component.

For guidance on automating this process, refer to [Deploy to Astronomer via CI/CD](ci-cd.md). To learn how to add Python and OS-level packages or otherwise customize your Docker image, read [Customize your image](customize-image.md).

Alternatively, you can configure an external NFS volume for DAG deploys. For more information, read [Deploy DAGs to an NFS volume](deploy-nfs.md).

> **Note:** Astronomer recommends that all users use the Astro CLI to test their code locally before pushing it to an Airflow Deployment on Astronomer. For guidelines on developing locally, see [CLI Quickstart](https://docs.astronomer.io/astro/cli/install-cli).

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

This command returns a list of Airflow Deployments available in your Workspace and prompts you to pick one. Once this command is executed, all files in your Astro project directory are built into a new Docker image and Docker containers for all Airflow components are restarted.

## Step 4: Validate Your Changes

If it's your first time deploying, expect to wait a few minutes for the Docker image to build.

To confirm that your deploy was successful, navigate to your Deployment in the Software UI and click **Open Airflow** to see your changes in the Airflow UI.

### What gets deployed?

Everything in the project directory where you ran `$ astro dev init` is bundled into a Docker image and deployed to your Airflow Deployment on your Astronomer platform. This includes system-level dependencies, Python-level dependencies, DAGs, and your `Dockerfile`.

Astronomer exclusively deploys the code in your project and does not push any of the metadata associated with your local Airflow environment, including task history and Airflow connections or variables set locally in the Airflow UI.

For more information about what gets built into your image, read [Customize your image](customize-image.md).

## Next steps: Organize Astronomer

While the specific needs of your organization might require a slightly different structure than what's described here, these are some general best practices to consider when working with Astronomer:

**Workspaces:** We recommend having 1 Workspace per team of Airflow users, so that anyone on this team has access to the same set of Deployments under that Workspace.

**Deployments:** Most use cases will call for a "Production" and "Dev" Deployment, both of which exist within a single Workspace and are accessible to a shared set of users. From there, you can [set permissions](workspace-permissions.md) to give users in the Workspace access to specific Deployments.

**Code:** As for the code itself, we’ve seen effective organization where external code is partitioned by function and/or business case, so one directly for SQL, one for data processing tasks, one for data validation, etc.
