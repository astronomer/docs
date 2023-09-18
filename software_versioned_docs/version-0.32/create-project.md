---
title: 'Create an Astronomer Software project'
sidebar_label: 'Create a project'
id: create-project
description: Get started on Astronomer Software.
---

This is where you'll find information about creating a project and running it in a local Airflow environment.

## Prerequisites

Creating an Astro project requires the [Astro CLI](https://docs.astronomer.io/astro/cli/overview).

## Step 1: Create a project directory

Before you create a Software project, create an empty directory and open it:

 ```sh
mkdir <your-new-directory> && cd <your-new-directory>
 ```

From this directory, run the following Astro CLI command:

```sh
astro dev init
```

This generates the following files:

```py
.
├── .env # Local environment variables
├── dags # Where your DAGs go
│   └── example-dag.py # An example DAG that comes with the initialized project
├── Dockerfile # For the Astronomer Runtime Docker image and runtime overrides
├── include # For any other files you'd like to include
├── plugins # For any custom or community Airflow plugins
├── airflow_settings.yaml # For your Airflow connections, variables and pools (local only)
├── packages.txt # For OS-level packages
└── requirements.txt # For any Python packages
```

A few of these files are essential for deploying your Airflow image for the first time:

### Dockerfile

Your Dockerfile will include reference to an Astro Runtime Docker image. [Astro Runtime](runtime-image-architecture.md) is a production ready data orchestration tool based on Apache Airflow that includes additional features and undergoes additional levels of rigorous testing conducted by Astronomer.

This Docker image is hosted on [Astronomer's Quay.io registry](https://quay.io/repository/astronomer/runtime?tab=tags) and allows you to run Airflow on Astronomer. Additionally, the image you include in your Dockerfile dictates the version of Airflow you'd like to run both when you're developing locally and pushing up to Astro.

Because Astro Runtime releases more frequently than Apache Airflow, a Runtime image's version number will be different than the Apache Airflow version it supports. See [Astro Runtime and Apache Airflow parity](runtime-image-architecture.md#Astro-Runtime-and-Apache-Airflow-parity).

By default, the Docker image in your Dockerfile is:

```
FROM quay.io/astronomer/astro-runtime:<latest-runtime-version>
```

This command installs a Debian-based Astro Runtime image that supports the latest version of Airflow. To use a specific Airflow version, read [Upgrade Airflow](manage-airflow-versions.md).

### Example DAG

To help you get started, your initialized project includes an `example-dag` in `/dags`. This DAG simply prints today's date, but it'll give you a chance to become familiar with how to deploy on Astronomer.

If you'd like to deploy some more functional DAGs, upload your own or check out [example DAGs we've open sourced](https://github.com/airflow-plugins/example-dags).

## Step 2: Build your project locally

To confirm that you successfully initialized an Astro project, run the following command from your project directory:

```sh
astro dev start
```

This command builds your project and spins up 4 Docker containers on your machine, each for a different Airflow component:

- **Postgres:** Airflow's metadata database
- **Webserver:** The Airflow component responsible for rendering the Airflow UI
- **Scheduler:** The Airflow component responsible for monitoring and triggering tasks
- **Triggerer:** The Airflow component responsible for running Triggers and signaling tasks to resume when their conditions have been met. The triggerer is used exclusively for tasks that are run with deferrable operators.

## Step 3: Access the Airflow UI

Once your project builds successfully, you can access the Airflow UI by going to `http://localhost:8080/` and logging in with `admin` for both your username and password.

:::info

It might take a few minutes for the Airflow UI to be available. As you wait for the webserver container to start up, you might need to refresh your browser.

:::

After logging in, you should see the DAGs from your `dags` directory in the Airflow UI.

![Example DAG in the Airflow UI](/img/software/sample-dag.png)

## What's next?

Once you've successfully created a Software project on your local machine, we recommend reading the following:

* [Customize image](customize-image.md)
* [Configure a Deployment](configure-deployment.md)
* [Deploy code](deploy-cli.md)
