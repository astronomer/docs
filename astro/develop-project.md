---
sidebar_label: 'Develop a project'
title: 'Develop your Astro project'
id: develop-project
description: Learn how to add Airflow dependencies and customize an Astro project to fit your use case.
---

import {siteVariables} from '@site/src/versions';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This is where you'll find information about:

- Building and running a project
- Deploying changes to a project
- Adding dependencies to a project
- Running on-build commands
- Adding connections, pools, and environment variables locally

## Prerequisites

- An existing [Astro project](create-project.md).
- [The Astro CLI](cli/get-started.md)
- [Docker](https://www.docker.com/products/docker-desktop)

## Build and run a project locally

To run your Astro project locally, run the following command:

```sh
astro dev start
```

This command builds your project and spins up 4 Docker containers on your machine, each for a different Airflow component:

- **Postgres:** Airflow's metadata database
- **Webserver:** The Airflow component responsible for rendering the Airflow UI
- **Scheduler:** The Airflow component responsible for monitoring and triggering tasks
- **Triggerer:** The Airflow component responsible for running triggers and signaling tasks to resume when their conditions have been met. The triggerer is used exclusively for tasks that are run with [deferrable operators](deferrable-operators.md).

Once the project builds, you can access the Airflow UI by going to `http://localhost:8080/` and logging in with `admin` for both your username and password. You can also access your Postgres database at `localhost:5432/postgres`.

:::info

The Astro CLI is a wrapper around [Docker Compose](https://docs.docker.com/compose/), a tool for defining and running multi-container Docker applications. If you're familiar with Docker Compose, you'll recognize that the `astro dev start` command, for example, is functionally equivalent to `docker compose start`.

:::

:::tip

If you see `Error: cannot start, project already running` when you run this command, it means your local Airflow environment is already running your project. If there are changes you'd like to apply to your project, see [Restart your local environment](develop-project.md#make-changes-to-your-project).

:::

### Restart your local environment

To restart your local Airflow environment, run the following command:

```sh
astro dev restart
```

These commands rebuild your image and restart the Docker containers running on your local machine with that new image. Alternatively, you can run just `astro dev stop` to stop your Docker containers without restarting or rebuilding your project.

## Make changes to your project

All Astro projects require you to specify a Debian-based Astro Runtime image in a `Dockerfile`. When you run your project locally or on Astro, all of your DAG code, packages, and configurations are built into a Docker image based on Astro Runtime.

Depending on the change you're making to your Astro project, you might have to rebuild your image to run your changes locally.

### DAG code changes

All changes made to files in the following directories will be live in your local Airflow environment as soon as you save them to your code editor:

- `dags`
- `plugins`
- `include`

Once you save your changes, refresh the Airflow UI in your browser to see them render.

### Environment changes

All changes made to the following files require rebuilding your image:

- `packages.txt`
- `Dockerfile`
- `requirements.txt`
- `airflow_settings.yaml`

To rebuild your project after making a change to any of these files, you must [restart your local environment](develop-project.md#restart-your-local-environment).

## Explore Airflow providers and modules

As you customize your Astro project and expand your use case for Airflow, we recommend exploring the [Astronomer Registry](https://registry.astronomer.io/), a library of Airflow modules, providers, and DAGs that serve as the building blocks for data pipelines.

The Astronomer Registry includes:

- Example DAGs for many data sources and destinations. For example, you can build out a data quality use case with Snowflake and Great Expectations based on the [Great Expectations Snowflake Example DAG](https://registry.astronomer.io/dags/great-expectations-snowflake).
- Documentation for Airflow providers, such as [Databricks](https://registry.astronomer.io/providers/databricks), [Snowflake](https://registry.astronomer.io/providers/snowflake), and [Postgres](https://registry.astronomer.io/providers/postgres). This documentation is comprehensive and based on Airflow source code.
- Documentation for Airflow modules, such as the [PythonOperator](https://registry.astronomer.io/providers/apache-airflow/modules/pythonoperator), [BashOperator](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator), and [S3ToRedshiftOperator](https://registry.astronomer.io/providers/amazon/modules/s3toredshiftoperator). These modules include guidance on how to set Airflow connections and their parameters.

As you browse the Astronomer Registry, follow this document for instructions on how to install providers as Python packages and make other changes to your Astro project.

## Add Python and OS-level packages

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

1. Run `docker ps` to identify the docker containers running on your machine
2. Copy the container ID of the scheduler container
3. Run the following:

```
docker exec -it <scheduler-container-id> pip freeze | grep pymongo

pymongo==3.7.2
```

## Add DAGs

DAGs are stored in the `dags` folder of your Astro project. To add a DAG to your project, simply add its `.py` file to this folder.

### Add DAG helper functions

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

2. [Restart your local environment](develop-project.md#restart-your-local-environment).

To confirm that your helper functions were successfully installed:

1. Run `docker ps` to identify the 3 running docker containers on your machine
2. Copy the container ID of your scheduler container
3. Run the following command to see your new directory in the container:

    ```bash
    $ docker exec -it <scheduler-container-id> /bin/bash
    bash-4.4$ ls
    Dockerfile  airflow_settings.yaml  helper_functions  logs  plugins  unittests.cfg
    airflow.cfg dags  include  packages.txt  requirements.txt
    ```

## Configure `airflow_settings.yaml` (Local development only)

When you first initialize a new Astro project, a file called `airflow_settings.yaml` is automatically generated. With this file, you can configure and programmatically generate Airflow [Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html), [Pools](https://airflow.apache.org/docs/apache-airflow/stable/concepts/pools.html), and [Variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html) so that you don't have to manually redefine these values in the Airflow UI every time you restart your project.

As a security measure, `airflow_settings.yaml` works only in local environments. Once you deploy your project to a Deployment on Astro, the values in this file will not be included. To more easily manage Airflow secrets on Astro, we recommend [configuring a secrets backend](secrets-backend.md).

:::caution

If you are storing your project in a public directory or version control tool, we recommend adding this file to your `.gitignore` or equivalent secret management service.

:::

### Add Airflow connections, pools, and variables

By default, the `airflow_settings.yaml` file includes the following template:

```yaml
airflow:
  connections: ## conn_id and conn_type are required
    - conn_id: my_new_connection
      conn_type: postgres
      conn_host: 123.0.0.4
      conn_schema: airflow
      conn_login: user
      conn_password: pw
      conn_port: 5432
      conn_extra:
  pools: ## pool_name and pool_slot are required
    - pool_name: my_new_pool
      pool_slot: 5
      pool_description:
  variables: ## variable_name and variable_value are required
    - variable_name: my_variable
      variable_value: my_value
```

This template includes default values for all possible configurations. Make sure to replace these default values with your own and specify those that are required to avoid errors at build time. To add another Connection, Pool, or Variable, append it to this file within its corresponding section. To create another Variable, for example, add it under the existing `variables` section of the same file:

```yaml
variables:
  - variable_name: <my-variable-1>
    variable_value: <my-variable-value>
  - variable_name: <my-variable-2>
    variable_value: <my-variable-value-2>
```

Once you save these values in your `airflow_settings.yaml`, [restart your local environment](develop-project.md#restart-your-local-environment). When you access the Airflow UI locally, you should see these values in the **Connections**, **Pools**, and **Variables** tabs.

## Run commands on build

To run additional commands as your Astro project is built into a Docker image, add them to your `Dockerfile` as `RUN` commands. These commands run as the last step in the image build process.

For example, if you want to run `ls` when your image builds, your `Dockerfile` would look like this:

<pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}
RUN ls
`}</code></pre>

This is supported both on Astro and in the context of local development.

## Override the CLI's Docker Compose file (Local development only)

The Astro CLI is built on top of [Docker Compose](https://docs.docker.com/compose/), which is a tool for defining and running multi-container Docker applications. To override CLI Docker Compose configurations, add a `docker-compose.override.yml` file to your Astro project. Any values in this file override the default CLI settings whenever you run `astro dev start`.

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

The Astro CLI does not support overrides to environment variables that are required globally. For the list of environment variables that Astro enforces, see [Global environment variables](platform-variables.md). To learn more about environment variables, read [Environment variables](environment-variables.md).

:::

## Set environment variables locally

For local development, Astronomer recommends setting environment variables in your Astro project's `.env` file. You can then push your environment variables from the `.env` file to a Deployment using the [Astro CLI](cli/astro-deployment-variable-update.md).

If your environment variables contain sensitive information or credentials that you don't want exposed in plain-text, you can add your `.env` file to `.gitignore` when you deploy these changes to your version control tool.

1. Open the `.env` file in your Astro project directory.
2. Add your environment variables to the `.env` file or run `astro deployment variable list --save` to copy environment variables from an existing Deployment to the file.

    Use the following format when you set environment variables in your `.env` file:

    ```text
    KEY=VALUE
    ```

    Environment variables should be in all-caps and not include spaces.

3. Run `astro dev start --env .env` to rebuild your image.
4. Optional. Run `astro deployment variable create/update --load` to export environment variables from your `.env` file to a Deployment. You can view and modify the exported environment variables in the Cloud UI page for your Deployment. To manage environment variables in the Cloud UI, see [Environment Variables](environment-variables.md).

### Confirm your environment variable changes

Confirm that your environment variables were applied in a local environment by running the following commands:

```
$ docker exec -it <scheduler-container-name> /bin/bash
$ env
```

These commands output all environment variables that are running locally. This includes both environment variables set in `.env` and environment variables set on Astro Runtime by default.

:::info

For local environments, the Astro CLI generates an `airflow.cfg` file at runtime based on the environment variables you set in your `.env` file. You can't create or modify `airflow.cfg` in an Astro project.

To view your local environment variables in the context of the generated Airflow configuration, run:

```
$ docker exec -it <scheduler-container-name> /bin/bash
$ cat airflow.cfg
```

These commands output the contents of the generated `airflow.cfg` file, which lists your environment variables as human-readable configurations with inline comments.

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

## Install Python packages from private sources

Python packages can be installed from both public and private locations into your image. To install packages listed on private PyPI indices or a private git-based repository, you need to complete additional configuration in your project.

Depending on where your private packages are stored, use one of the following setups to install these packages to an Astro project by customizing your Runtime image.

:::info

Deploying a custom Runtime image with a CI/CD pipeline requires additional configurations. For an example implementation, see [GitHub Actions CI/CD templates](ci-cd.md#github-actions).

:::

<Tabs
    defaultValue="github"
    values={[
        {label: 'Private GitHub Repo', value: 'github'},
        {label: 'Private PyPi Index', value: 'pypi'},
    ]}>
<TabItem value="github">

#### Install Python packages from private GitHub repositories

This topic provides instructions for building your Astro project with Python packages from a private GitHub repository.

Although this setup is based on GitHub, the high level steps can be completed with any hosted Git repository.

:::info

The following setup has been validated only with a single SSH key. You might need to modify this setup when using more than one SSH key per Docker image.

:::

#### Prerequisites

To install Python packages from a private GitHub repository on Astro, you need:

- The [Astro CLI](cli/get-started.md).
- An [Astro project](create-project.md).
- Custom Python packages that are [installable with pip](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
- A private GitHub repository for each of your custom Python packages.
- A [GitHub SSH private key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) authorized to access your private GitHub repositories.

:::warning

If your organization enforces SAML single sign-on (SSO), you must first authorize your key to be used with that authentication method. For instructions, see [GitHub documentation](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-an-ssh-key-for-use-with-saml-single-sign-on).

:::

This setup assumes that each custom Python package is hosted within its own private GitHub repository. Installing multiple custom packages from a single private GitHub repository is not supported.

#### Step 1: Specify the private repository in your project

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

#### Step 2: Create Dockerfile.build

1. In your Astro project, create a duplicate of your `Dockerfile` and name it `Dockerfile.build`.

2. In `Dockerfile.build`, add `AS stage` to the `FROM` line which specifies your Runtime image. For example, if you use Runtime 5.0.0, your `FROM` line would be:

   ```text
   FROM quay.io/astronomer/astro-runtime:5.0.0-base AS stage1
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
    RUN apt-get update && cat packages.txt | xargs apt-get install -y

    FROM stage1 AS stage2
    USER root
    RUN apt-get -y install git python3 openssh-client \
      && mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
    # Install Python Packages
    COPY requirements.txt .
    RUN --mount=type=ssh,id=github pip install --no-cache-dir -q -r requirements.txt

    FROM stage1 AS stage3
    # Copy requirements directory
    COPY --from=stage2 /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
    COPY . .
    ```

    In order, these commands:

    - Install any OS-level packages specified in `packages.txt`.
    - Securely mount your SSH key at build time. This ensures that the key itself is not stored in the resulting Docker image filesystem or metadata.
    - Install Python-level packages from your private repository as specified in your `requirements.txt` file.

  :::tip

  This example `Dockerfile.build` assumes Python 3.9, but some versions of Astro Runtime may be based on a different version of Python. If your image is based on a version of Python that is not 3.9, replace `python 3.9` in the **COPY** commands listed under the `## Copy requirements directory` section of your `Dockerfile.build` with the correct Python version.

  To identify the Python version in your Astro Runtime image, run:

     ```
     docker run quay.io/astronomer/astro-runtime:<runtime-version>-base python --version
     ```

  Make sure to replace `<runtime-version>` with your own.

  :::

  :::info

  If your repository is hosted somewhere other than GitHub, replace the domain in the `ssh-keyscan` command with the domain where the package is hosted.

  :::

#### Step 3: Build a custom Docker image

1. Run the following command to create a new Docker image from your `Dockerfile.build` file. Replace `<ssh-key>` with your SSH private key file name and `<astro-runtime-image>` with your Astro Runtime image.

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --ssh=github="$HOME/.ssh/<ssh-key>" -t custom-<astro-runtime-image> .
    ```

    For example, if you have `quay.io/astronomer/astro-runtime:5.0.0-base` in your `Dockerfile.build`, this command would be:

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --ssh=github="$HOME/.ssh/<authorized-key>" -t custom-astro-runtime-5.0.0-base .
    ```

2. Update the following entry in the  `Dockerfile`:

   ```
   FROM custom-astro-runtime:5.0.0
   ```
  :::info

    Astro runtime base images are built on AMD64 architecture. You must add the architecture name to the `FROM` statement when your computer and the image architecture are different. For example, this is the format for the Apple M1 architecture:

    ```
   FROM --platform=linux/amd64 custom-astro-runtime:5.0.0
   ```
  :::

  Your Astro project can now utilize Python packages from your private GitHub repository.

3. Optional. Test or deploy your DAGs. See [Build and Run a Project Locally](develop-project.md#build-and-run-a-project-locally) or [Deploy Code to Astro](deploy-code.md).

</TabItem>

<TabItem value="pypi">

#### Install Python packages from a private PyPI index

In some organizations, python packages are prebuilt and pushed to a hosted private pip server (such as pypiserver or Nexus Repository) or managed service (such as PackageCloud or Gitlab).

#### Prerequisites

To build from a private repository, you need:

- An [Astro project](create-project.md).
- A private PyPI index with username and password authentication.

#### Step 1: Add privately hosted packages to requirements.txt

Add the name and, optionally, the version of your packages to `requirements.txt`. This is the same syntax as you would use when adding public packages from [PyPI](https://pypi.org). `requirements.txt` can contain a mixture of both publicly accessible and private packages.

:::caution

Ensure that the name of the package on the private repository does not clash with any existing python packages on [PyPI](https://pypi.org). If pip parses multiple repositories with the same name, it can produce unexpected results.

:::

#### Step 2: Create Dockerfile.build

1. In your Astro project, create a duplicate of your `Dockerfile` named `Dockerfile.build`.

2. In `Dockerfile.build`, add `AS stage` to the `FROM` line which specifies your Runtime image. For example, if you use Runtime 5.0.0, your `FROM` line would be:

   ```text
   quay.io/astronomer/astro-runtime:5.0.0-base AS stage1
   ```

   :::info

   If you use the default distribution of Astro Runtime, replace your existing image with its corresponding `-base` image. The `-base` distribution is built to be customizable and does not include default build logic. For more information on Astro Runtime distributions, see [Distributions](runtime-version-lifecycle-policy.md#distribution).

   :::

3. In `Dockerfile.build` after the `FROM` line specifying your Runtime image, add the following configuration. Make sure to replace `<url-to-packages>` with the URL leading to the directory with your Python packages:

    ```docker
    LABEL maintainer="Astronomer <humans@astronomer.io>"
    ARG BUILD_NUMBER=-1
    LABEL io.astronomer.docker=true
    LABEL io.astronomer.docker.build.number=$BUILD_NUMBER
    LABEL io.astronomer.docker.airflow.onbuild=true
    # Install Python and OS-Level Packages
    COPY packages.txt .
    RUN apt-get update && cat packages.txt | xargs apt-get install -y

    FROM stage1 AS stage2
    # Install Python Packages
    ARG PIP_EXTRA_INDEX_URL
    ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}
    COPY requirements.txt .
    RUN pip install --no-cache-dir -q -r requirements.txt

    FROM stage1 AS stage3
    # Copy requirements directory
    COPY --from=stage2 /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
    COPY . .
    ```

    In order, these commands:

    - Complete the standard installation of OS-level packages in `packages.txt`.
    - Add the environment variable `PIP_EXTRA_INDEX_URL` to instruct pip on where to look for non-public packages.
    - Install public and private Python-level packages from your `requirements.txt` file.

#### Step 3: Build a custom Docker image

1. Run the following command to create a new Docker image from your `Dockerfile.build` file. Replace the pip repository and associated credential values with your own.

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --build-arg PIP_EXTRA_INDEX_URL=https://${<repo-username>}:${<repo-password>}@<private-pypi-repo-domain-name> -t custom-<airflow-image> .
    ```

    For example, if you have `quay.io/astronomer/astro-runtime:5.0.0` in your `Dockerfile.build`, this command would be:

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --build-arg PIP_EXTRA_INDEX_URL=https://${<repo-username>}:${<repo-password>}@<private-pypi-repo-domain-name> -t custom-astro-runtime-5.0.0 .
    ```
2. Update the following entry in the  `Dockerfile`:

  ```
   FROM custom-astro-runtime:5.0.0
   ```
  :::info

    Astro runtime base images are built on the `linux/amd64` architecture. You must add the architecture name to the `FROM` statement when your computer and the image architecture are different. For example, this is the format for the Apple M1 architecture:

    ```
   FROM --platform=linux/amd64 custom-astro-runtime:5.0.0
   ```
  :::

    Your Astro project can now utilize Python packages from your private PyPi index.

3. Optional. Test or deploy your DAGs. See [Build and Run a Project Locally](develop-project.md#build-and-run-a-project-locally) or [Deploy Code to Astro](deploy-code.md).

</TabItem>
</Tabs>
