---
sidebar_label: 'Create a Project'
title: 'Create an Astro project'
id: 'create-project'
description: Create an Astro project and run it locally with the Astro CLI.
---

import {siteVariables} from '@site/src/versions';

## Overview

To run Airflow pipelines on Astro, you first need to create an Astro project. An Astro project contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. Once you've tested these files locally, the Astro project structure makes it easy to deploy your pipelines to Astro.

This guide provides instructions for creating a new Astro project, as well as information about the default Astro project structure.

## Prerequisites

To create an Astro project, you need:

- [The Astro CLI](install-cli.md)
- [Docker](https://www.docker.com/products/docker-desktop)

## Step 1: Create an Astro project

To create a new Astro project:

1. Create a new directory for your Astro project:

    ```sh
    mkdir <your-astro-project-name>
    ```

2. Open the directory:

    ```sh
    cd <your-astro-project-name>
    ```

3. Run the following Astro CLI command to initialize an Astro project in the directory:

    ```sh
    astrocloud dev init
    ```

    This command generates the following files in the directory:

    ```
    .
    ├── dags # Where your DAGs go
    │   └── example-dag-basic.py # Example DAG that showcases a simple ETL data pipeline
    |   └── example-dag-advanced.py # Example DAG that showcases more advanced Airflow features, such as the TaskFlow API
    ├── Dockerfile # For the Astro Runtime Docker image, environment variables, and overrides
    ├── include # For any other files you'd like to include
    ├── plugins # For any custom or community Airflow plugins
    |   └── example-plugin.py
    ├── tests # For any DAG unit test files to be run with pytest
    |   └── test_dag_integrity.py # Test that checks for basic errors in your DAGs
    ├── airflow_settings.yaml # For your Airflow Connections, Variables and Pools (local only)
    ├── packages.txt # For OS-level packages
    └── requirements.txt # For Python packages
    ```

    This set of files will build into a Docker image that you can both run on your local machine and deploy to Astro.

### Astro Runtime

Your `Dockerfile` includes a reference to Astro Runtime. Packaged into a Debian-based Docker image, Astro Runtime extends the Apache Airflow open source project to provide you with differentiated functionality that centers around reliability, efficiency, and performance. For more information on what's included in Runtime and how it's versioned, see [Runtime Versioning](runtime-version-lifecycle-policy.md).

By default, the Docker image in your Dockerfile is:

<pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}
`}</code></pre>

## Step 2: Build Your Project Locally

To confirm that you successfully initialized an Astro project, run the following command from your project directory:

```sh
astrocloud dev start
```

This command builds your project and spins up 3 Docker containers on your machine, each for a different Airflow component:

- **Postgres:** Airflow's metadata database
- **Webserver:** The Airflow component responsible for rendering the Airflow UI
- **Scheduler:** The Airflow component responsible for monitoring and triggering tasks
- **Triggerer:** The Airflow component responsible for running Triggers and signaling tasks to resume when their conditions have been met. The Triggerer is used exclusively for tasks that are run with [deferrable operators](deferrable-operators.md)

As your project builds locally, you should see the following output:

<pre><code parentName="pre">{`% astrocloud dev start
Env file ".env" found. Loading...
Sending build context to Docker daemon  10.75kB
Step 1/1 : FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}

# Executing 5 build triggers
---> Using cache
---> Using cache
---> Using cache
---> Using cache
---> Using cache
---> 5160cfd00623
Successfully built 5160cfd00623
Successfully tagged astro-trial_705330/airflow:latest
INFO[0000] [0/4] [postgres]: Starting
INFO[0002] [1/4] [postgres]: Started
INFO[0002] [1/4] [scheduler]: Starting
INFO[0003] [2/4] [scheduler]: Started
INFO[0003] [2/4] [webserver]: Starting
INFO[0004] [3/4] [webserver]: Started
INFO[0003] [3/4] [triggerer]: Starting
INFO[0004] [4/4] [triggerer]: Started
Airflow Webserver: http://localhost:8080
Postgres Database: localhost:5432/postgres
The default credentials are admin:admin
`}</code></pre>

:::info

By default, the Astro CLI uses port `8080` for the Airflow Webserver and port `5432` for the Airflow metadata database. If these ports are already in use on your local machine, you can change the default ports for these components by following these steps:

1. In your Astro project directory, open `.astrocloud/config.yaml`. This file might be hidden in graphical file browsers. You can show hidden files using `⌘ + Shift + .` on Mac or by selecting **View** > **Hidden items** in Windows file explorer.
2. Specify alternative ports for your Webserver and/or metadata database in `config.yaml`. For example, to use `8081` for your Webserver port and `5435` for your database port, you would specify the following:

    ```yaml
    project:
      name: <your-directory-name>
    webserver:
      port: 8081
    postgres:
      port: 5435
    ```

3. Run `astrocloud dev restart` to rebuild and rerun your project.

:::

## Step 3: Access the Airflow UI

Once your project builds successfully, you can access the Airflow UI by going to `http://localhost:8080/` and logging in with `admin` for both your username and password.

:::info

It might take a few minutes for the Airflow UI to be available. As you wait for the Webserver container to start up, you may need to refresh your browser.

:::

After logging in, you should see the DAGs from your `dags` directory in the Airflow UI.

<div class="text--center">
<img src="/img/docs/sample-dag.png" alt="Example DAG in the Airflow UI" />
</div>

## Next Steps

Running your project locally is the best way to test your DAGs before pushing them to Astro. For more information on running a local Airflow environment, read:

- [Develop your Astro Project](develop-project.md)
- [Test and Troubleshoot Locally](test-and-troubleshoot-locally.md#run-a-project-locally)
