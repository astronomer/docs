---
sidebar_label: ‘Develop a project’
title: ‘Develop your Astro project’
id: develop-project
---

<head>
  <meta name=“description” content=“Learn how to add Airflow dependencies and customize an Astro project to meet the unique requirements of your organization.” />
  <meta name=“og:description” content=“Learn how to add Airflow dependencies and customize an Astro project to meet the unique requirements of your organization.” />
</head>

import {siteVariables} from ‘@site/src/versions’;
import Tabs from ‘@theme/Tabs’;
import TabItem from ‘@theme/TabItem’;

An Astro project contains all of the files necessary to test and run DAGs in a local Airflow environment and on Astro. This guide contains information about how to add or modify files in your Astro project and apply changes. It includes how to:

- Add DAGs
- Add Python and OS-level packages
- Set environment variables
- Apply changes
- Run on-build commands

For guidelines on testing DAGs once you’ve built your Astro project, see [Test and troubleshoot locally](test-and-troubleshoot-locally.md).

## Prerequisites

- An [Astro project](create-project.md).
- [The Astro CLI](cli/overview.md)
- [Docker](https://www.docker.com/products/docker-desktop)

## Build and run a project locally

Making changes to your Astro project and testing them locally requires an Airflow environment on your computer. To start an Astro project in a local Airflow environment, run the following command:

```
astro dev start
```

This command builds your Astro project into a Docker image and creates 4 Docker containers on your computer, each for a different Airflow component:

- **Postgres:** Airflow's metadata database
- **Webserver:** The Airflow component responsible for rendering the Airflow UI
- **Scheduler:** The Airflow component responsible for monitoring and triggering tasks
- **Triggerer:** The Airflow component responsible for running triggers and signaling tasks to resume when their conditions have been met. The triggerer is used exclusively for tasks that are run with deferrable operators.

Once the project builds, you can access the Airflow UI by going to `http://localhost:8080/` and logging in with `admin` for both your username and password. You can also access your Postgres database at `localhost:5432/postgres`.

## Add DAGs

In Apache Airflow, data pipelines are defined in Python code as Directed Acyclic Graph (DAGs). A DAG is a collection of tasks and dependencies between tasks that are defined as code. See [Introduction to Airflow DAGs](learn/dags.md).

DAGs are stored in the `dags` folder of your Astro project. To add a DAG to your project:

1. Add the `.py` file to this folder. The name of the file is what appears in the Airflow UI as the `dag_id`, or the name of the DAG. You cannot have more than one DAG with the same `dag_id`.
2. Save your changes to your code editor. If you're using a Mac, use **Command-S**.
3. Refresh your Airflow browser.

### Add DAG helper functions

Some DAGs may need helper functions to run. For example, custom functions used in operators or callbacks that you can write once and reference across DAGs within a single Astro project.

Because this is repeatable code that that is across DAGs, Astronomer recommends creating a dedicated folder called `helper_functions` that is separate from the `dags` directory.

1. Add your directory of helper functions to your local project. You can give it any name:

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
    
2. [Restart your local environment](develop-project.md#restart-your-local-environment).

3. To confirm that your helper functions were successfully installed, run the following command:

   ```sh

    astro dev bash --scheduler “/bin/bash”

   ```

    The command should output a list of files in the scheduler container including your helper functions:

   ```bash

    $ astro dev bash --scheduler “/bin/bash”
    bash-4.4$ ls
    Dockerfile  airflow_settings.yaml  helper_functions  logs  plugins  unittests.cfg
    airflow.cfg dags  include  packages.txt  requirements.txt

   ```

## Add Airflow connections, pools, variables

Airflow connections are necessary to connect to external tools, such as a database or other third-party service. See [Manage connections in Apache Airflow](learn/connections.md#airflow-connection-basics) or [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

To add Airflow [connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html), [pools](https://airflow.apache.org/docs/apache-airflow/stable/concepts/pools.html), and [variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html) to your local Airflow environment, you can do any of the following:

- Go to the **Admin** menu of the Airflow UI in a local Airflow environment. Click **Connections**, **Variables**, or **Pools** and add your values. These values are stored in the metadata database and are deleted when you run the [`astro dev kill` command](cli/astro-dev-kill.md), which can sometimes be used for troubleshooting.
- Use the `airflow_settings.yaml` file of your Astro project. This file is included in every Astro project and permanently stores your values in plain-text. To prevent you from committing sensitive credentials or passwords to your version control tool, Astronomer recommends adding this file to `.gitignore`.
- Use a secret backend, such as AWS Secrets Manager, and access the secret backend locally. See [Configure an external secrets backend on Astro](secrets-backend.md).

When you add Airflow objects to the Airflow UI of a local environment or to your `airflow_settings.yaml` file, your values can only be used locally. When you deploy your project to a Deployment on Astro, the values in this file are not included.

Astronomer recommends using the `airflow_settings.yaml` file so that you don’t have to manually redefine Airflow objects in the Airflow UI every time you restart your project. For security conscious organizations, Astronomer recommends [configuring a secrets backend](secrets-backend.md) or testing all DAGs on Astro instead of in a local Airflow environment.

### Configure `airflow_settings.yaml` (Local development only)

The `airflow_settings.yaml` file includes a template with default values for all possible configurations. To add or change a connection, variable, or pool:

1. Open the `airflow_settings.yaml` file and replace the default value with your own.

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

2. Save the modified `airflow_settings.yaml` file in your code editor. If you use a Mac computer, for example, use **Command-S**.
3. Import these objects to the Airflow UI. Run:

    ```sh
    astro dev object import
    ```
    
4. In the Airflow UI, click either the **Connections**, **Pools**, or **Variables** tab to see your new or modified objects.
5. Optional. To add another connection, pool, or variable, append it to this file within its corresponding section. To create another variable, for example, add it under the existing `variables` section of the same file:

  ```yaml
  variables:
    - variable_name: <my-variable-1>
      variable_value: <my-variable-value>
    - variable_name: <my-variable-2>
      variable_value: <my-variable-value-2>
  ```
  
## Add Python, OS-level packages, and Airflow providers

Most DAGs need a Python package or OS-level package to run. If you’re using Airflow for a data science project, for example, you might need to install popular data science libraries such as [pandas](https://pandas.pydata.org/) or [NumPy (`numpy`)](https://numpy.org/). Adding a Python package to your Astro project is equivalent to running `pip install`.

Airflow providers are Python packages that contain all relevant Airflow modules for a third-party service. For example, `apache-airflow-providers-amazon` includes all hooks, operators, and integrations you need to access services on Amazon Web Services (AWS) with Airflow. See [Provider packages](https://airflow.apache.org/docs/apache-airflow-providers/).

1. Add the package name to your Astro project. If it’s a Python package, add it to `requirements.txt`. If it’s an OS-level package, add it to `packages.txt`. The latest version of the package that’s publicly available is installed by default.

    To pin a version of a package, use the following syntax:
      ```text
      <package-name>==<version>
      ```
    To install NumPy version 1.23.0, for example, add the following to your `requirements.txt` file:

      ```text
      numpy==1.23.0
      ```
2. [Restart your local environment](develop-project.md#restart-your-local-environment).
3. Confirm that your package was installed:

    ```sh
    astro dev bash --scheduler “pip freeze | grep <package-name>”
    ```
    This command outputs the version number of the installed package.

## Add DAG utility files

Use the `include` folder to store additional utilities required by your DAGs. For example, templated SQL scripts and custom operators.

In most cases, Astronomer recommends moving the `include` folder into the `dags` directory so that your DAGs can access your utility files.

:::tip

When you use the `astro deploy -—dags` command to deploy to Astro, the `include` folder in the Astro project directory is not deployed with your DAGs unless it is in the `dags` directory. Instead, it is built into the Docker image with your other project files and requires running `astro deploy`. See [Deploy DAGs only](deploy-code.md#deploy-dags-only).

:::

## Set environment variables locally

For local development, Astronomer recommends setting environment variables in your Astro project’s `.env` file. You can then push your environment variables from the `.env` file to a Deployment on Astro. To manage environment variables in the Cloud UI, see [Environment variables](environment-variables.md).

If your environment variables contain sensitive information or credentials that you don’t want to expose in plain-text, you can add your `.env` file to `.gitignore` when you deploy these changes to your version control tool.

1. Open the `.env` file in your Astro project directory.
2. Add your environment variables to the `.env` file or run `astro deployment variable list --save` to copy environment variables from an existing Deployment to the file.

    Use the following format when you set environment variables in your `.env` file:

    ```text
    KEY=VALUE
    ```

    Environment variables should be in all-caps and not include spaces.

3. [Restart your local environment](develop-project.md#restart-your-local-environment).
4. Confirm that your environment variables were applied in a local environment by running:
    ```sh
    astro dev bash --scheduler “/bin/bash && env”
    ```
   These commands output all environment variables that are running locally. This includes environment variables set on Astro Runtime by default.
5. Optional. Run `astro deployment variable create --load` or `astro deployment variable update --load` to export environment variables from your `.env` file to a Deployment. You can view and modify the exported environment variables in the Cloud UI page for your Deployment.

:::info

For local environments, the Astro CLI generates an `airflow.cfg` file at runtime based on the environment variables you set in your `.env` file. You can’t create or modify `airflow.cfg` in an Astro project.

To view your local environment variables in the context of the generated Airflow configuration, run:

```
astro dev bash --scheduler “/bin/bash && cat airflow.cfg”
```

These commands output the contents of the generated `airflow.cfg` file, which lists your environment variables as human-readable configurations with inline comments.

:::

### Use multiple .env files

The Astro CLI looks for `.env` by default, but if you want to specify multiple files, make `.env` a top-level directory and create sub-files within that folder.

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

## Run commands on build

To run additional commands as your Astro project is built into a Docker image, add them to your `Dockerfile` as `RUN` commands. These commands run as the last step in the image build process.

For example, if you want to run `ls` when your image builds, your `Dockerfile` would look like this:

<pre><code parentName=“pre”>{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}
RUN ls
`}</code></pre>

This is supported both on Astro and in the context of local development.

## Add a CA certificate to an Astro Runtime image

If you need your Astro Deployment to communicate securely with a remote service using a certificate signed by an untrusted or internal certificate authority (CA), you need to add the CA certificate to the trust store inside your Astro project's Docker image.

1. In your Astro project `Dockerfile`, add the following entry below the existing `FROM` statement which specifies your Astro Runtime image version:

    ```docker
    USER root
    COPY <internal-ca.crt>/usr/local/share/ca-certificates/<your-company-name>/
    RUN update-ca-certificates
    USER astro
    ```
2. Optional. Add additional `COPY` statements before the `RUN update-ca-certificates` stanza for each CA certificate your organization is using for external access.

3. [Restart your local environment](develop-project.md#restart-your-local-environment) or deploy to Astro. See [Deploy code](deploy-code.md).

## Apply changes to your project

The Astro CLI makes it easy to quickly apply and test changes to your Astro project. Depending on the file that you change, you might have to restart your local Aiflow environment to apply the change.

### DAG code changes

Changes made to the following directories in your Astro project don’t require rebuilding your project:

- `dags`
- `plugins`
- `include`

To apply a change to these files:

1. Save the latest version of the file to your local version control tool, such as VSCode.
2. Refresh the Airflow UI in your browser.

### Environment changes

All changes made to the following files require rebuilding your Astro project into a Docker image and restarting your Airflow environment.

- `packages.txt`
- `Dockerfile`
- `requirements.txt`
- `airflow_settings.yaml`

1. Save the change to your local version control tool, such as VSCode.
2. [Restart your local environment](develop-project.md#restart-your-local-environment).

### Restart your local environment

To restart your local Airflow environment, run:

```sh
astro dev restart
```

These commands rebuild your image and restart the Docker containers running on your local machine with that new image. Alternatively, you can run just `astro dev stop` to stop your Docker containers without restarting or rebuilding your project.

## Install Python packages from private sources

Python packages can be installed from both public and private locations into your image. To install packages listed on private PyPI indices or a private git-based repository, you need to complete additional configuration in your project.

Depending on where your private packages are stored, use one of the following setups to install these packages to an Astro project by customizing your Runtime image.

:::info

Deploying a custom Runtime image with a CI/CD pipeline requires additional configurations. For an example implementation, see [GitHub Actions CI/CD templates](ci-cd.md#github-actions).

:::

<Tabs
    defaultValue=“github”
    groupId= “install-python-packages-from-private-sources”
    values={[
        {label: ‘Private GitHub Repo’, value: ‘github’},
        {label: ‘Private PyPi Index’, value: ‘pypi’},
    ]}>
<TabItem value=“github”>

#### Install Python packages from private GitHub repositories

This topic provides instructions for building your Astro project with Python packages from a private GitHub repository.

Although this setup is based on GitHub, the high level steps can be completed with any hosted Git repository.

:::info

The following setup has been validated only with a single SSH key. You might need to modify this setup when using more than one SSH key per Docker image.

:::

#### Prerequisites

- The [Astro CLI](cli/overview.md).
- An [Astro project](create-project.md).
- Custom Python packages that are [installable with pip](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
- A private GitHub repository for each of your custom Python packages.
- A [GitHub SSH private key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) authorized to access your private GitHub repositories.

:::warning

If your organization enforces SAML single sign-on (SSO), you must first authorize your key to be used with that authentication method. For instructions, see [GitHub documentation](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-an-ssh-key-for-use-with-saml-single-sign-on).

:::

This setup assumes that each custom Python package is hosted within its own private GitHub repository. Installing multiple custom packages from a single private GitHub repository is not supported.

#### Step 1: Specify the private repository in your project

To add a Python package from a private repository to your Astro project, specify the repository’s SSH URL in your project’s `requirements.txt` file. This URL should be formatted as:

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

#### Step 2: Update Dockerfile

1. Optional. Copy any build steps you already have in your `Dockerfile` and save them for later.

2. In your `Dockerfile`, add `AS stage` to the `FROM` line which specifies your Runtime image. For example, if you use Runtime 5.0.0, your `FROM` line would be:

   ```text
   FROM quay.io/astronomer/astro-runtime:5.0.0-base AS stage1
   ```

  :::info

  If you currently use the default distribution of Astro Runtime, replace your existing image with its corresponding `-base` image as demonstrated in the example above. The `-base` distribution is built to be customizable and does not include default build logic. For more information on Astro Runtime distributions, see [Distributions](runtime-image-architecture.md#distribution).

  :::

3. After the `FROM` line specifying your Runtime image, add the following configuration:

    ```docker
    LABEL maintainer=“Astronomer <humans@astronomer.io>”
    ARG BUILD_NUMBER=-1
    LABEL io.astronomer.docker=true
    LABEL io.astronomer.docker.build.number=$BUILD_NUMBER
    LABEL io.astronomer.docker.airflow.onbuild=true
    # Install OS-Level packages
    COPY packages.txt .
    RUN apt-get update && cat packages.txt | xargs apt-get install -y

    FROM stage1 AS stage2
    USER root
    RUN apt-get -y install git python3 openssh-client \
      && mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
    # Install Python packages
    COPY requirements.txt .
    RUN --mount=type=ssh,id=github pip install --no-cache-dir -q -r requirements.txt

    FROM stage1 AS stage3
    # Copy requirements directory
    COPY --from=stage2 /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
    COPY --from=stage2 /usr/local/bin /home/astro/.local/bin
    ENV PATH=“/home/astro/.local/bin:$PATH”

    COPY . .
    ```

    In order, these commands:

    - Install any OS-level packages specified in `packages.txt`.
    - Securely mount your SSH key at build time. This ensures that the key itself is not stored in the resulting Docker image filesystem or metadata.
    - Install Python-level packages from your private repository as specified in your `requirements.txt` file.

  :::tip

  This example `Dockerfile` assumes Python 3.9, but some versions of Astro Runtime may be based on a different version of Python. If your image is based on a version of Python that is not 3.9, replace `python 3.9` in the **COPY** commands listed under the `## Copy requirements directory` section of your `Dockerfile` with the correct Python version.

  To identify the Python version in your Astro Runtime image, run:

     ```
     docker run quay.io/astronomer/astro-runtime:<runtime-version>-base python --version
     ```

  Make sure to replace `<runtime-version>` with your own.

  :::

  :::info

  If your repository is hosted somewhere other than GitHub, replace the domain in the `ssh-keyscan` command with the domain where the package is hosted.

  :::

4. Optional. If you had any other commands in your original `Dockerfile`, add them after the line `FROM stage1 AS stage3`.

#### Step 3: Build a custom Docker image

1. Run the following command to automatically generate a unique image name:

    ```sh
    image_name=astro-$(date +%Y%m%d%H%M%S)
    ```

2. Run the following command to create a new Docker image from your `Dockerfile`. Replace `<ssh-key>` with your SSH private key file name.

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile --progress=plain --ssh=github=“$HOME/.ssh/<ssh-key>” -t $image_name .
    ```

3. Optional. Test your DAGs locally. See [Restart your local environment](develop-project.md#restart-your-local-environment).

4. Deploy the image to Astro using the Astro CLI:

    ```sh
    astro deploy --image-name $image_name
    ```

Your Astro project can now utilize Python packages from your private GitHub repository.

</TabItem>

<TabItem value=“pypi”>

#### Install Python packages from a private PyPI index

Installing Python packages on Astro from a private PyPI index is required for organizations that deploy a [private PyPI server (`private-pypi`)](https://pypi.org/project/private-pypi/) as a secure layer between pip and a Python package storage backend, such as GitHub, AWS, or a local file system or managed service.

To complete this setup, you’ll specify your privately hosted Python packages in `requirements.txt`, create a custom Docker image that changes where pip looks for packages, and then build your Astro project with this Docker image.

#### Prerequisites

- An [Astro project](create-project.md).
- A private PyPI index with a corresponding username and password.

#### Step 1: Add Python packages to your Astro project

To install a Python package from a private PyPI index, add the package name and version to the `requirements.txt` file of your Astro project. If you don’t specify a version, the latest version is installed. Use the same syntax that you used when you added public packages from [PyPI](https://pypi.org). Your `requirements.txt` file can contain both publicly accessible and private packages.

:::caution

Make sure that the name of any privately hosted Python package doesn’t conflict with the name of other Python packages in your Astro project. The order in which pip searches indices might produce unexpected results.

:::

#### Step 2: Update Dockerfile

1. Optional. Copy any build steps you already have in your `Dockerfile` and save them for later.

2. In your `Dockerfile`, add `AS stage` to the `FROM` line which specifies your Runtime image. For example, if you use Runtime 5.0.0, your `FROM` line would be:

   ```text
   quay.io/astronomer/astro-runtime:5.0.0-base AS stage1
   ```

   :::info

   If you use the default distribution of Astro Runtime, replace your existing image with its corresponding `-base` image. The `-base` distribution is built to be customizable and does not include default build logic. For more information on Astro Runtime distributions, see [Distributions](runtime-version-lifecycle-policy.md#distribution).

   :::

3. After the `FROM` line specifying your Runtime image, add the following configuration:

    ```docker
    LABEL maintainer=“Astronomer <humans@astronomer.io>”
    ARG BUILD_NUMBER=-1
    LABEL io.astronomer.docker=true
    LABEL io.astronomer.docker.build.number=$BUILD_NUMBER
    LABEL io.astronomer.docker.airflow.onbuild=true
    # Install OS-Level packages
    COPY packages.txt .
    RUN apt-get update && cat packages.txt | xargs apt-get install -y

    FROM stage1 AS stage2
    # Install Python packages
    ARG PIP_EXTRA_INDEX_URL
    ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}
    COPY requirements.txt .
    RUN pip install --no-cache-dir -q -r requirements.txt

    FROM stage1 AS stage3
    # Copy requirements directory
    COPY --from=stage2 /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
    COPY --from=stage2 /usr/local/bin /home/astro/.local/bin
    ENV PATH=“/home/astro/.local/bin:$PATH”

    COPY . .
    ```

    In order, these commands:

    - Install any OS-level packages specified in `packages.txt`.
    - Add `PIP_EXTRA_INDEX_URL` as an environment variable that contains authentication information for your private PyPI index.
    - Install public and private Python-level packages from your `requirements.txt` file.

4. Optional. If you had any other commands in your original `Dockerfile`, add them after the line `FROM stage1 AS stage3`.

#### Step 3: Build a custom Docker image

1. Run the following command to automatically generate a unique image name:

    ```sh
    image_name=astro-$(date +%Y%m%d%H%M%S)
    ```

2. Run the following command to create a new Docker image from your `Dockerfile`. Replace `<private-pypi-repo-domain-name>`, `<repo-username>` and `<repo-password>` with your own values.

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile --progress=plain --build-arg PIP_EXTRA_INDEX_URL=https://${<repo-username>}:${<repo-password>}@<private-pypi-repo-domain-name> -t $image_name .
    ```

3. Optional. Test your DAGs locally or deploy your image to Astro. See [Build and Run a Project Locally](develop-project.md#build-and-run-a-project-locally) or [Deploy Code to Astro](deploy-code.md).

    ```sh
    astro dev start --image-name $image_name
    ```
  
4. Optional. Deploy the image to a Deployment on Astro using the Astro CLI:

Your Astro project can now utilize Python packages from your private PyPi index.

</TabItem>
</Tabs>
