---
sidebar_label: 'Develop a Project'
title: 'Develop Your Astro project'
id: develop-project
description: Learn how to add Airflow dependencies and customize an Astro project to fit your use case.
---

import {siteVariables} from '@site/src/versions';

## Overview

This document explains the various ways you can modify and build your Astro project to fit your team's use case. Specifically, this guide provides instructions on how to:

- Build and run a project
- Deploy changes to a project
- Add dependencies to your project
- Run on-build commands
- Add connections, pools, and environment variables locally

## Prerequisites

To develop an Astro project and test it locally, you need:

- An existing [Astro project](create-project.md).
- [The Astro CLI](install-cli.md)
- [Docker](https://www.docker.com/products/docker-desktop)

## Build and Run a Project Locally

To run your Astro project locally, run the following command:

```sh
astrocloud dev start
```

This command builds your project and spins up 4 Docker containers on your machine, each for a different Airflow component:

- **Postgres:** Airflow's metadata database
- **Webserver:** The Airflow component responsible for rendering the Airflow UI
- **Scheduler:** The Airflow component responsible for monitoring and triggering tasks
- **Triggerer:** The Airflow component responsible for running Triggers and signaling tasks to resume when their conditions have been met. The Triggerer is used exclusively for tasks that are run with [deferrable operators](deferrable-operators.md).

Once the project builds, you can access the Airflow UI by going to `http://localhost:8080/` and logging in with `admin` for both your username and password. You can also access your Postgres database at `localhost:5432/postgres`.

:::info

The Astro CLI is a wrapper around [Docker Compose](https://docs.docker.com/compose/), a tool for defining and running multi-container Docker applications. If you're familiar with Docker Compose, you'll recognize that the `astrocloud dev start` command, for example, is functionally equivalent to `docker compose start`.

:::

:::tip

If you see `Error: cannot start, project already running` when you run this command, it means your local Airflow environment is already running your project. If there are changes you'd like to apply to your project, see [restart your local environment](develop-project.md#make-changes-to-your-project).

:::

### Restart Your Local Environment

To restart your local Airflow environment, run the following command:

```sh
astrocloud dev restart
```

These commands rebuild your image and restart the Docker containers running on your local machine with that new image. Alternatively, you can run just `astrocloud dev stop` to stop your Docker containers without restarting or rebuilding your project.

## Make Changes to Your Project

All Astro projects require you to specify a Debian-based Astro Runtime image in a `Dockerfile`. When you run your project locally or on Astro, all of your DAG code, packages, and configurations are built into a Docker image based on Astro Runtime.

Depending on the change you're making to your Astro project, you might have to rebuild your image to run your changes locally.

### DAG Code Changes

All changes made to files in the following directories will be live in your local Airflow environment as soon as you save them to your code editor:

- `dags`
- `plugins`
- `include`

Once you save your changes, refresh the Airflow UI in your browser to see them render.

### Environment Changes

All changes made to the following files require rebuilding your image:

- `packages.txt`
- `Dockerfile`
- `requirements.txt`
- `airflow_settings.yaml`

To rebuild your project after making a change to any of these files, you must [restart your local environment](develop-project.md#restart-your-local-environment).

## Explore Airflow Providers and Modules

As you customize your Astro project and expand your use case for Airflow, we recommend exploring the [Astronomer Registry](https://registry.astronomer.io/), a library of Airflow modules, providers, and DAGs that serve as the building blocks for data pipelines.

The Astronomer Registry includes:

- Example DAGs for many data sources and destinations. For example, you can build out a data quality use case with Snowflake and Great Expectations based on the [Great Expectations Snowflake Example DAG](https://registry.astronomer.io/dags/great-expectations-snowflake).
- Documentation for Airflow providers, such as [Databricks](https://registry.astronomer.io/providers/databricks), [Snowflake](https://registry.astronomer.io/providers/snowflake), and [Postgres](https://registry.astronomer.io/providers/postgres). This documentation is comprehensive and based on Airflow source code.
- Documentation for Airflow modules, such as the [PythonOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonoperator), [BashOperator](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator), and [S3ToRedshiftOperator](https://registry.astronomer.io/providers/amazon/modules/s3toredshiftoperator). These modules include guidance on how to set Airflow connections and their parameters.

As you browse the Astronomer Registry, follow this document for instructions on how to install providers as Python packages and make other changes to your Astro project.

## Add Python and OS-level Packages

To build Python and OS-level packages into your Astro project, add them to your `requirements.txt` and `packages.txt` files. Add Python packages to your `requirements.txt` and OS-level packages to your `packages.txt` file.

To pin a version of a package, use the following syntax:

```text
<package-name>==<version>
```

To exclusively use Pymongo 3.7.2, for example, add the following line to your `requirements.txt` file:

```text
pymongo==3.7.2
```

If you don't pin a package to a version, the latest version of the package that's publicly available is installed by default.

Once you've saved these packages in your project files, [restart your local environment](develop-project.md#restart-your-local-environment).

### Confirm your package was installed

If you added `pymongo` to your `requirements.txt` file, for example, you can confirm that it was properly installed by running a `docker exec` command into your Scheduler:

1. Run `docker ps` to identify the 3 running docker containers on your machine
2. Copy the container ID of your Scheduler container
3. Run the following:

```
docker exec -it <scheduler-container-id> pip freeze | grep pymongo

pymongo==3.7.2
```

## Add DAGs

DAGs are stored in the `dags` folder of your Astro project. To add a DAG to your project, simply add its `.py` file to this folder.

### Add DAG Helper Functions

To build additional helper functions for DAGs into your Astro project, we recommend adding a folder with a set of files that can be used by Airflow DAGs.

To do this:

1. Add your directory of helper functions to your local project:

    ```bash
    .
    ├── airflow_settings.yaml
    ├── dags
    │   └── example-dag-basic.py
    │   └── example-dag-advanced.py
    ├── Dockerfile
    ├── helper_functions
    │   └── helper.py
    ├── include
    ├── tests
    │   └── test_dag_integrity.py
    ├── packages.txt
    ├── plugins
    │   └── example-plugin.py
    └── requirements.txt
    ```

    In this example, the directory is named `helper_functions`. You can give it any name.

2. [Restart Your Local Environment](develop-project.md#restart-your-local-environment).

To confirm that your helper functions were successfully installed:

1. Run `docker ps` to identify the 3 running docker containers on your machine
2. Copy the container ID of your Scheduler container
3. Run the following command to see your new directory in the container:

    ```bash
    $ docker exec -it <scheduler-container-id> /bin/bash
    bash-4.4$ ls
    Dockerfile  airflow_settings.yaml  helper_functions  logs  plugins  unittests.cfg
    airflow.cfg  dags  include  packages.txt  requirements.txt
    ```

## Configure `airflow_settings.yaml` (Local Development Only)

When you first initialize a new Astro project, a file called `airflow_settings.yaml` is automatically generated. With this file, you can configure and programmatically generate Airflow [Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html), [Pools](https://airflow.apache.org/docs/apache-airflow/stable/concepts/pools.html), and [Variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html) so that you don't have to manually redefine these values in the Airflow UI every time you restart your project.

As a security measure, `airflow_settings.yaml` works only in local environments. Once you deploy your project to a Deployment on Astro, the values in this file will not be included. To more easily manage Airflow secrets on Astro, we recommend [configuring a secrets backend](https://docs.astronomer.io/astro/secrets-backend).

:::caution
If you are storing your project in a public directory or version control tool, we recommend adding this file to your `.gitignore` or equivalent secret management service.
:::

### Add Airflow Connections, Pools, and Variables

By default, the `airflow_settings.yaml` file includes the following template:

```yaml
airflow:
  connections:
    - conn_id: my_new_connection
      conn_type: postgres
      conn_host: 123.0.0.4
      conn_schema: airflow
      conn_login: user
      conn_password: pw
      conn_port: 5432
      conn_extra:
  pools:
    - pool_name: my_new_pool
      pool_slot: 5
      pool_description:
  variables:
    - variable_name: my_variable
      variable_value: my_value
```

This template includes all possible configuration values. If you want to add another Connection, Pool, or Variable, you can copy the existing fields for the given resource and replace the default values with your own. For instance, to create another Variable, you can add its values under the existing default Variable like so:

```yaml
variables:
  - variable_name: my_variable
    variable_value: my_value
  - variable_name: my_second_variable
    variable_value: value987
```

Once you've saved these values in your `airflow_settings.yaml`, [restart your local environment](develop-project.md#restart-your-local-environment). When you access the Airflow UI for your project at `localhost:8080`, you should see these values in the **Connections**, **Pools**, and **Variables** tabs.

## Run Commands on Build

To run extra system commands when your Airflow image builds, add them to your `Dockerfile` as a `RUN` command. These commands run as the last step in the image build process.

For example, if you want to run `ls` when your image builds, your `Dockerfile` would look like this:

<pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}
RUN ls
`}</code></pre>

## Override the CLI's Docker Compose File (Local Development Only)

The Astro CLI is built on top of [Docker Compose](https://docs.docker.com/compose/), which is a tool for defining and running multi-container Docker applications. You can override the CLI's Docker Compose configurations by adding a `docker-compose.override.yml` file to your Astro project. Any values in this file override the CLI's default settings whenever you run `astrocloud dev start`.

To see what values you can override, reference the CLI's [Docker Compose file](https://github.com/astronomer/astro-cli/blob/main/airflow/include/composeyml.go). The linked file is for the original Astro CLI, but the values here are identical to those used in the Astro CLI. Common use cases for Docker Compose overrides include:

- Adding extra containers to mimic services that your Airflow environment needs to interact with locally, such as an SFTP server.
- Change the volumes mounted to any of your local containers.

For example, to add another volume mount for a directory named `custom_dependencies`, add the following to your `docker-compose.override.yml` file:

```yaml
version: "3.1"
services:
  scheduler:
    volumes:
      - /home/astronomer_project/custom_dependencies:/usr/local/airflow/custom_dependencies:ro
```

Make sure to specify `version: "3.1"` and follow the format of the source code file linked above.

To see your override file live in your local Airflow environment, run the following command for any container running Airflow:

```sh
docker exec -it <container-name> ls -al
```

:::info

The Astro CLI does not support overrides to environment variables that are required globally. For the list of environment variables that Astro enforces, see [Global Environment Variables](platform-variables.md). To learn more about environment variables, read [Environment Variables](environment-variables.md).

:::

## Set Environment Variables via .env (Local Development Only)

For Astro projects deployed on Astro, we generally recommend [setting environment variables via the Cloud UI](environment-variables.md#set-environment-variables-via-the-astro-ui). For local development, you can use the [Astro CLI](install-cli.md) to set environment variables in your project's `.env` file.

To add Environment Variables locally:

1. Open the `.env` file in your Astro project directory.
2. Add your environment variables to the `.env` file.
3. Rebuild your image by running `astrocloud dev start --env .env`.

When setting environment variables in your `.env` file, use the following format:

```
AIRFLOW__CORE__DAG_CONCURRENCY=5
```

:::tip

If your environment variables contain sensitive information or credentials that you don't want to expose in plain-text, you may want to add your `.env` file to `.gitignore` when you deploy these changes to your version control tool.

:::

### Confirm your environment variables were applied

By default, Airflow environment variables are hidden in the Airflow UI for both local environments and Astro Deployments. To confirm your environment variables via the Airflow UI, set `AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True` in either your Dockerfile or `.env` file.

Alternatively, you can run:

```
docker ps
```

This will output the 3 Docker containers that comprise the Airflow environment on your local machine: the Airflow Scheduler, Webserver, and Postgres metadata database.

Now, create a [Bash session](https://docs.docker.com/engine/reference/commandline/exec/#examples) in your scheduler container by running:

```
docker exec -it <scheduler-container-name> /bin/bash
```

If you run `ls -1` following this command, you'll see a list of running files:

```
bash-5.0$ ls -1
Dockerfile             airflow.cfg            airflow_settings.yaml  dags                   include                logs                   packages.txt           plugins                requirements.txt       unittests.cfg
```

Now, run:

```
env
```

This should output all Environment Variables that are running locally, some of which are set by you and some of which are set by Astronomer by default.

:::tip

You can also run `cat airflow.cfg` to output _all_ contents in that file.

:::

### Use multiple .env files

The Astro CLI will look for `.env` by default, but if you want to specify multiple files, make `.env` a top-level directory and create sub-files within that folder.

A project with multiple `.env` files might look like the following:

```
my_project
  ├── Dockerfile
  └──  dags
    └── my_dag
  ├── plugins
    └── my_plugin
  ├── airflow_settings.yaml
  ├── .env
    └── dev.env
    └── prod.env
```

## Install Python Packages from a Private GitHub Repository

This topic provides instructions for building your Astro project with Python packages from a private GitHub repository.  At a high level, this setup entails specifying your private packages in `requirements.txt`, creating a custom Docker image that mounts a GitHub SSH key for your private GitHub repositories, and building your project with this Docker image.

Although this setup is based on GitHub, the general steps can be completed with any hosted Git repository.

:::info

The following setup has been validated only with a single SSH key. Due to the nature of `ssh-agent`, you might need to modify this setup when using more than one SSH key per Docker image.

:::

### Prerequisites

To install Python packages from a private GitHub repository on Astro, you need:

- The [Astro CLI](install-cli.md).
- An [Astro project](create-project.md).
- Custom Python packages that are [installable via pip](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
- A private GitHub repository for each of your custom Python packages.
- A [GitHub SSH Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) authorized to access your private GitHub repositories.

This setup assumes that each custom Python package is hosted within its own private GitHub repository. Installing multiple custom packages from a single private GitHub repository is not supported.

### Step 1: Specify the Private Repository in Your Project

To add a Python package from a private repository to your Astro project, specify the repository's SSH URL in your project's `requirements.txt` file. This URL should be formatted as:

```
git+ssh://git@github.com/<your-github-organization-name>/<your-private-repository>.git
```

For example, to install `mypackage1` & `mypackage2` from `myorganization`, as well as `numpy v 1.22.1`, you would add the following to your `requirements.txt` file:

```
git+ssh://git@github.com/myorganization/mypackage1.git
git+ssh://git@github.com/myorganization/mypackage2.git
numpy==1.22.1
```

This example assumes that the name of each of your Python packages is identical to the name of its corresponding GitHub repository. In other words,`mypackage1` is both the name of the package and the name of the repository.

### Step 2: Create Dockerfile.build

1. In your Astro project, create a duplicate of your `Dockerfile` and name it `Dockerfile.build`.

2. In `Dockerfile.build`, add `AS stage` to the `FROM` line which specifies your Runtime image. For example, if you use Runtime 4.2.10, your `FROM` line would be:

   ```text
   FROM quay.io/astronomer/astro-runtime:4.2.10-base AS stage1
   ```

  :::info

  If you currently use the default distribution of Astro Runtime, replace your existing image with its corresponding `-base` image as demonstrated in the example above. The `-base` distribution is built to be customizable and does not include default build logic. For more information on Astro Runtime distributions, see [Distributions](runtime-version-lifecycle-policy.md#distribution).

  :::

3. In `Dockerfile.build` after the `FROM` line specifying your Runtime image, add the following configuration:

    ```docker
    LABEL maintainer="Astronomer <humans@astronomer.io>"
    ARG BUILD_NUMBER=-1
    LABEL io.astronomer.docker=true
    LABEL io.astronomer.docker.build.number=$BUILD_NUMBER
    LABEL io.astronomer.docker.airflow.onbuild=true
    # Install Python and OS-Level Packages
    COPY packages.txt .
    RUN cat packages.txt | xargs apk add --no-cache

    FROM stage1 AS stage2
    RUN --mount=type=ssh,id=github apk add --no-cache --virtual .build-deps \
        build-base \
        git \
        python3 \
        openssh-client \
    && mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts \
    # Install Python Packages
    COPY requirements.txt .
    RUN pip install --no-cache-dir -q -r requirements.txt

    FROM stage1 AS stage3
    # Copy requirements directory
    COPY --from=stage2 /usr/lib/python3.9/site-packages/ /usr/lib/python3.9/site-packages/
    COPY . .
    ```

    In order, these commands:

    - Install any OS-level packages specified in `packages.txt`.
    - Securely mount your SSH key at build time. This ensures that the key itself is not stored in the resulting Docker image filesystem or metadata.
    - Install Python-level packages from your private repository as specified in your `requirements.txt` file.

  :::tip

  If you don't want keys in this file to be pushed back up to your GitHub repository, consider adding this file to `.gitignore`.

  :::

  :::info

  If your repository is hosted somewhere other than GitHub, replace the location of your SSH key in the `ssh-keyscan` command.

  :::

### Step 3: Build a Custom Docker Image

1. Run the following command to create a new Docker image from your `Dockerfile.build` file, making sure to replace `<ssh-key>` with your SSH key file name and `<astro-runtime-image>` with your Astro Runtime image:

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --ssh=github="$HOME/.ssh/<ssh-key>" -t custom-<astro-runtime-image> .
    ```

    For example, if you have `quay.io/astronomer/astro-runtime:4.2.10-base` in your `Dockerfile.build`, this command would be:

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --ssh=github="$HOME/.ssh/<authorized-key>" -t custom-astro-runtime-4.2.10-base .
    ```

  :::info

  If your repository is hosted somewhere other than GitHub, replace the location of your SSH key in the `--ssh` flag.

  :::

2. Replace the contents of your Astro project's `Dockerfile` with the following:

   ```
   FROM custom-<runtime-image>
   ```

   For example, if your base Runtime image was `quay.io/astronomer/astro-runtime:4.2.10-base`, this line would be:

   ```
   FROM custom-astro-runtime:4.2.10-base
   ```

Your Astro project can now utilize Python packages from your private GitHub repository. To test your DAGs, you can either [run your project locally](develop-project.md#build-and-run-a-project-locally) or [deploy to Astro](deploy-code.md).
