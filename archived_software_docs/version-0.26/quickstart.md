---
title: 'Astronomer Software Quickstart'
sidebar_label: 'Quickstart'
id: quickstart
description: Get started on Astronomer Software.
---

Welcome to Astronomer.

This guide will help you get started on Astronomer by walking through a sample DAG deployment from start to finish.

Whether you're exploring our Software or Cloud offering, we've designed this to be a great way to become familiar with our platform.

## Step 1: Install the Astronomer CLI

The [Astronomer CLI](https://github.com/astronomer/astro-cli) is the easiest way to run Apache Airflow® on your machine. From the CLI, you can establish a local testing environment and deploy to Astro whenever you're ready.

There are two ways to install any version of the Astronomer CLI:

- cURL
- [Homebrew](https://brew.sh/)

> **Note:** If you're running on Windows, check out our [Windows Install Guide](cli-install-windows-10.md).

### Prerequisites

The CLI installation process requires [Docker](https://www.docker.com/) (v18.09 or higher).

#### Install the CLI via cURL

To install the latest version of the Astronomer CLI via cURL, run:

```bash
curl -ssl https://install.astronomer.io | sudo bash
```

#### Install the CLI via Homebrew

To install the latest version of the Astronomer CLI via [Homebrew](https://brew.sh/), run:

```bash
brew install astro
```

For more information on the Astronomer CLI, read [CLI Quickstart](cli-quickstart.md).

## Step 2: Install Astronomer Software

If you are in charge of setting up Astronomer for your team, follow one of our Software installation guides to get Astronomer running on your Kubernetes Cluster.

We have documentation for deploying Astronomer on:

- Amazon Elastic Kubernetes Service (EKS) (via [Helm](install-aws-standard.md))
- [Google Kubernetes Engine (GKE)](install-gcp-standard.md)
- [Azure Kubernetes Service (AKS)](install-azure-standard.md)

## Step 3: Create a Project

Using the Astronomer CLI, create an Airflow project to work from that lives on your local machine:

 ```sh
mkdir <your-new-directory> && cd <your-new-directory>
 ```

Then, run:

```
astro dev init
```

This will generate the following files:

```py
.
├── dags # Where your DAGs go
│   ├── example-dag.py # An example dag that comes with the initialized project
├── Dockerfile # For Astronomer's Docker image and runtime overrides
├── include # For any other files you'd like to include
├── plugins # For any custom or community Apache Airflow® plugins
├──airflow_settings.yaml #For your Airflow Connections, Variables and Pools (local only)
├──packages.txt # For OS-level packages
└── requirements.txt # For any Python packages
```

A few of these files are essential for deploying your Airflow image for the first time:

### Dockerfile

Your Dockerfile includes a reference to an Astronomer Certified Docker Image. Astronomer Certified (AC) is a Debian-based, production-ready distribution of Apache Airflow that mirrors the open source project and undergoes additional levels of rigorous testing conducted by our team.

This Docker image is hosted on [Astronomer's Docker Registry](https://quay.io/repository/astronomer/ap-airflow?tab=tags) and allows you to run Airflow on Astronomer. Additionally, the image you include in your Dockerfile dictates the version of Airflow you'd like to run both when you're developing locally and pushing up to Astro.

The Docker image you'll find in your Dockerfile by default is:

```
FROM quay.io/astronomer/ap-airflow:latest-onbuild
```

This will install a Debian-based AC image for the latest version of Airflow we support. To specify a particular Airflow version, read [Upgrade Airflow](manage-airflow-versions.md) and the _Customize your Image_ topic below.

### Example DAG

To help you get started, your initialized project includes an `example-dag` in `/dags`. This DAG simply prints today's date, but it'll give you a chance to become familiar with how to deploy on Astronomer.

If you'd like to deploy some more functional DAGs, upload your own or check out [example DAGs we've open sourced](https://github.com/airflow-plugins/example-dags).

## Step 4: Identify your Base Domain and Log in

Since Astronomer is running entirely on your infrastructure, the Software UI will be located at a base domain specific to your organization. Head to `app.BASEDOMAIN` in your web browser and log in. You're in the right place if you see the following login screen:

![Log In](/img/software/log_into_astro.png)

> **Note:** If you are not the first person to log in, you will need an email invite to the platform.

## Step 5: Create a Workspace

If you're the first person to log in to the Software UI, click **New Workspace** to create a Workspace.

![Create a Workspace on Astronomer](/img/software/create-workspace.png)

You can think of Workspaces the same way you'd think of teams - a space that specific user groups have access to with varying levels of permissions. From within a Workspace you can create one or more Airflow Deployments, each of which hosts a collection of DAGs.

For more information, read [Manage Workspaces and Deployments](manage-workspaces.md).

## Step 6: Authenticate to Astronomer from the CLI

You can authenticate to Astronomer using the following command:

```sh
astro auth login BASEDOMAIN
```

You'll be prompted to authenticate and select the Workspace that you want to operate in.

The first user to log in to the Astronomer platform will become a System Admin by default. Additional users can be added via the Software UI or CLI. For more information on user permissions at the platform level, read [Manage Users on Astronomer Software](manage-platform-users.md).

## Step 7: Create an Apache Airflow® Deployment

In the Software UI, use the **New Deployment** menu to configure the following:

* **Name**
* **Description** (Optional)
* **Airflow Version**: We recommend using the latest version.
* **Executor**: We recommend starting with the Local Executor.

Once you've finished, click **Create Deployment**. After it spins up, your new Deployment should look something like this:

![Create an Airflow Deployment on Astronomer](/img/software/create-deployment.png)

For a production environment, you'll likely need to set resources and configure your Airflow Deployment to fit the needs of your organization. For more information on configuring Deployments, read [Configure an Airflow Deployment on Astronomer](configure-deployment.md).

## Step 8: Deploy a DAG

You can now use Astronomer to start Airflow locally and deploy code. To do so:

1. Go to the Airflow project directory you created in **Step 4** and run the following command:

    ```sh
    astro dev start
    ```

    This command spins up 3 Docker containers on your machine, each for a different Airflow component:

    - **Postgres:** [Airflow's Metadata Database](access-airflow-database.md)
    - **Webserver:** The Airflow component responsible for rendering the Airflow UI
    - **Scheduler:** The Airflow component responsible for monitoring and triggering tasks

    > **Note:** If you’re running the Astronomer CLI with the [buildkit](https://docs.docker.com/develop/develop-images/build_enhancements/) feature enabled in Docker, you may see an error (`buildkit not supported by daemon`). Learn more in [this forum post](https://forum.astronomer.io/t/buildkit-not-supported-by-daemon-error-command-docker-build-t-airflow-astro-bcb837-airflow-latest-failed-failed-to-execute-cmd-exit-status-1/857).

2. Verify that all 3 Docker containers were created by running the following command:

    ```sh
    docker ps
    ```

    > **Note**: Running `$ astro dev start` will start your project with the Apache Airflow® Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop existing docker containers](https://forum.astronomer.io/t/docker-error-in-cli-bind-for-0-0-0-0-5432-failed-port-is-already-allocated/151) or [change the port](https://forum.astronomer.io/t/i-already-have-the-ports-that-the-cli-is-trying-to-use-8080-5432-occupied-can-i-change-the-ports-when-starting-a-project/48).


3. Deploy the `example-dag` from `hello-astro` to Airflow by running the following command:

    ```sh
    astro deploy
    ```

4. Confirm the deploy was successful by going to your local Airflow instance at `http://localhost:8080`.

    You should be able to view `example-dag` in the Airflow UI. You should also be able to turn on `example-dag` and see task runs begin to accumulate in the **Recent Tasks** column.

## Step 9: Access Metrics

Once you've turned on the `example-dag` in the Airflow UI, go to the **Metrics** tab in the Software UI to see metrics for your Deployment in real time.

The **Metrics** tab only shows metrics for a given Deployment. If you are the first user to authenticate to Astronomer, you'll additionally have access to administrative views of Grafana and Kibana via the dropdown menu in the Software UI:

![Admin](/img/software/admin_panel.png)

These views show logs and metrics across all Deployments running on your Astronomer platform. To learn more about using Grafana, read [Metrics in Astronomer Software](grafana-metrics.md). To learn more about using Kibana, read [Logging in Astronomer Software](kibana-logging.md).

## Video Tutorial

Watch our video tutorial for a brief review of the workflows and concepts described in this quickstart:

<iframe width="560" height="315" src="https://www.youtube.com/embed/OihokE8u9D0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

## What's Next?

Once you've successfully installed your Astronomer platform, we recommend doing the following:

* [Invite new users to Astronomer](manage-platform-users.md)
* [Manage permissions](workspace-permissions.md) for your new users
* Integrate an [Auth System](integrate-auth-system.md)
* Set up [CI/CD](ci-cd.md)
