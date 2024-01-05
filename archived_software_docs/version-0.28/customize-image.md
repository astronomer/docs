---
sidebar_label: 'Customize Image'
title: 'Customize Your Image on Astronomer Software'
id: customize-image
description: Customize your Astronomer image, including adding dependencies and running commands on build.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

## Overview

The Astro CLI is intended to make it easier to develop with Apache Airflow, whether you're developing on your local machine or deploying code to Astronomer. The following guidelines describe a few of the methods you can use to customize the Docker Image that gets pushed to Airflow every time you rebuild your image locally using `$ astro dev start` or deploy to Astronomer using `$ astro deploy`.

More specifically, this doc includes instructions for how to:

- Add Python and OS-level Packages
- Add dependencies
- Run commands on build
- Access the Airflow CLI
- Add Environment Variables Locally
- Build from a Private Repository

> **Note:** The guidelines below assume that you've initialized a project on Astronomer via `$ astro dev init`. If you haven't done so already, refer to our ["CLI Quickstart" doc](install-cli.md).

## Add Python and OS-level Packages

To build Python and OS-level packages into your Airflow Deployment, add them to your `requirements.txt` and `packages.txt` files on Astronomer. Both files were automatically generated when you initialized an Airflow project locally via `$ astro dev init`. Steps below.

### Add your Python or OS-Level Package

Add all Python packages to your `requirements.txt` and any OS-level packages you'd like to include to your `packages.txt` file.

To pin a version of that package, use the following syntax:

```
<package-name>==<version>
```

If you'd like to exclusively use Pymongo 3.7.2, for example, you'd add the following in your `requirements.txt`:

```
pymongo==3.7.2
```

If you do _not_ pin a package to a version, the latest version of the package that's publicly available will be installed by default.

### Rebuild your Image

Once you've saved those packages in your text editor or version control tool, rebuild your image by running:

```
astro dev stop
```

followed by

```
astro dev start
```

This process stops your running Docker containers and restarts them with your updated image.

### Confirm your Package was Installed (_Optional_)

If you added `pymongo` to your `requirements.txt` file, for example, you can confirm that it was properly installed by running a `$ docker exec` command into your Scheduler.

1. Run `$ docker ps` to identify the 3 running docker containers on your machine
2. Grab the container ID of your Scheduler container
3. Run the following:

```
docker exec -it <scheduler-container-id> pip freeze | grep pymongo

pymongo==3.7.2
```

## Add Other Dependencies

In the same way you can build Python and OS-level Packages into your image, you're free to build additional dependencies and files for your DAGs to use.

In the example below, we'll add a folder of `helper_functions` with a file (or set of files) that our Airflow DAGs can then use.

### Add the folder into your project directory

```bash
.
├── airflow_settings.yaml
├── dags
│   └── example-dag.py
├── Dockerfile
├── helper_functions
│   └── helper.py
├── include
├── packages.txt
├── plugins
│   └── example-plugin.py
└── requirements.txt
```

### Rebuild your Image

Follow the instructions in the "Rebuild your Image" section above.

### Confirm your files were added (_Optional_)

Similar to the `pymongo` example above, you can confirm that `helper.py` was properly built into your image by running a `$ docker exec` command into your Scheduler.

1. Run `$ docker ps` to identify the 3 running docker containers on your machine
2. Grab the container ID of your Scheduler container
3. Run the following:

```bash
docker exec -it <scheduler-container-id> /bin/bash
bash-4.4$ ls
Dockerfile  airflow_settings.yaml  helper_functions  logs  plugins  unittests.cfg
airflow.cfg  dags  include  packages.txt  requirements.txt
```

Notice that `helper_functions` folder has been built into your image.

## Configure airflow_settings.yaml

When you first initialize a new Airflow project on Astronomer, a file titled `airflow_settings.yaml` will be automatically generated. With this file you can configure and programmatically generate Airflow Connections, Pools, and Variables when you're developing locally.

For security reasons, the `airflow_settings.yaml` file is currently _only_ for local development and should not be used for pushing up code to Astronomer via `$ astro deploy`. For the same reason, we'd recommend adding this file to your `.gitignore`.

:::tip

If you're interested in programmatically managing Airflow Connections, Variables or Environment Variables on Astronomer Software, we recommend integrating a [Secret Backend](secrets-backend.md).

:::

### Add Airflow Connections, Pools, Variables

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
  pools: ## pool_name, pool_slot, and pool_description are required
    - pool_name: my_new_pool
      pool_slot: 5
      pool_description:
  variables: ## variable_name and variable_value are required
    - variable_name: my_variable
      variable_value: my_value
```

Make sure to specify all required fields that correspond to the objects you create. If you don't specify them, you will see a build error on `$ astro dev start`.

### Additional Entries

If you want to add a second Connection/Pool/Variable, copy the existing fields and make a new entry like so:

```yaml
variables:
  - variable_name: my_first_variable
    variable_value: value123
  - variable_name: my_second_variable
    variable_value: value987
```

## Run Commands on Build

If you're interested in running any extra commands when your Airflow Image builds, it can be added to your `Dockerfile` as a `RUN` command. These will run as the last step in the image build process.

For example, if you wanted to run `ls` when your image builds, your `Dockerfile` would look like this:

```
FROM quay.io/astronomer/ap-airflow:1.10.12-buster-onbuild
RUN ls
```

## Docker Compose Override

The Astro CLI is built on top of [Docker Compose](https://docs.docker.com/compose/), a tool for defining and running multi-container Docker applications. To override the default CLI configurations ([found here](https://github.com/astronomer/astro-cli/blob/main/airflow/include/composeyml.go)), add a `docker-compose.override.yml` file to your Astronomer project directory. The values in this file override the default settings when you run `$ astro dev start`.

To add another volume mount for a directory named `custom_dependencies`, for example, add the following to your `docker-compose.override.yml`:

```
version: "3.1"
services:
  scheduler:
    volumes:
      - /home/astronomer_project/custom_dependencies:/usr/local/airflow/custom_dependencies:ro
```

Make sure to specify `version: "3.1"` and mimic the format of the source code file linked above.

When your image builds on `$ astro dev start`, any changes made within the `custom_dependencies` directory will be picked up automatically the same way they are with files in your `dags` directory:

```
$ docker exec -it astronomer_project239673_scheduler_1 ls -al
total 76
drwxr-xr-x    1 astro    astro         4096 Dec 30 17:21 .
drwxr-xr-x    1 root     root          4096 Dec 14  2018 ..
-rw-rw-r--    1 root     root            38 Oct  8 00:07 .dockerignore
-rw-rw-r--    1 root     root            31 Oct  8 00:07 .gitignore
-rw-rw-r--    1 root     root            50 Oct  8 00:10 Dockerfile
-rw-r--r--    1 astro    astro        20770 Dec 30 17:21 airflow.cfg
drwxrwxr-x    2 1000     1000          4096 Oct  8 00:07 dags
-rw-r--r--    1 root     root           153 Dec 30 17:21 docker-compose.override.yml
drwxrwxr-x    2 1000     1000          4096 Oct  8 00:07 include
drwxr-xr-x    4 astro    astro         4096 Oct  8 00:11 logs
drwxr-xr-x    2 1000     1000          4096 Dec 30 17:15 custom_dependencies
-rw-rw-r--    1 root     root             0 Oct  8 00:07 packages.txt
drwxrwxr-x    2 1000     1000          4096 Oct  8 00:07 plugins
-rw-rw-r--    1 root     root             0 Oct  8 00:07 requirements.txt
-rw-r--r--    1 astro    astro         2338 Dec 30 17:21 unittests.cfg
```

> **Note:** The Astro CLI does _not_ support overrides to Environment Variables. For more information on how to set, configure and customize those values, see ["Environment Variables" doc](environment-variables.md).

## Access to the Airflow CLI

You're free to use native Airflow CLI commands on Astronomer when developing locally by wrapping them around docker commands.

To add a connection, for example, you can run:

```bash
docker exec -it SCHEDULER_CONTAINER bash -c "airflow connections -a --conn_id test_three  --conn_type ' ' --conn_login etl --conn_password pw --conn_extra {"account":"blah"}"
```

Refer to the native [Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/usage-cli.html) for a list of all commands.

## Add Environment Variables Locally

To import Environment Variables from a specific file, run `$ astro dev start` with an `--env` flag:

```
astro dev start --env .env
```

> **Note:** This feature is limited to local development only. Whatever `.env` you use locally will _not_ be bundled up when you deploy to Astronomer.
>
> For more detail on how to add Environment Variables both locally and on Astronomer, refer to our [Environment Variables doc](environment-variables.md).

## Install Python Packages from Private Sources

Python packages can be installed from public and private locations into your image. To install public packages listed on [PyPI](https://pypi.org/search/), follow the steps in [Add Python and OS-level Packages](customize-image.md#add-python-and-os-level-packages). To install packages listed on private PyPI indices or a private git-based repository, you need to complete additional configuration in your project.

Depending on where your private packages are stored, use one of the following setups to install your packages to an Astro project by customizing your Runtime image.

<Tabs
    defaultValue="github"
    values={[
        {label: 'Private GitHub Repo', value: 'github'},
        {label: 'Private PyPi Index', value: 'pypi'},
    ]}>
<TabItem value="github">

## Install Python Packages from a Private GitHub Repository

This topic provides instructions for building your Astro project with Python packages from a private GitHub repository.  At a high level, this setup entails specifying your private packages in `requirements.txt`, creating a custom Docker image that mounts a GitHub SSH key for your private GitHub repositories, and building your project with this Docker image.

Although this setup is based on GitHub, the general steps can be completed with any hosted Git repository.

:::info

The following setup has been validated only with a single SSH key. Due to the nature of `ssh-agent`, you might need to modify this setup when using more than one SSH key per Docker image.

:::

### Prerequisites

To install Python packages from a private GitHub repository on Astronomer Software, you need:

- The [Astro CLI](install-cli.md).
- A [Software project](create-project.md).
- Custom Python packages that are [installable via pip](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
- A private GitHub repository for each of your custom Python packages.
- A [GitHub SSH Private Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) authorized to access your private GitHub repositories.

:::danger

If your organization enforces SAML single sign-on (SSO), you must first authorize your key to be used with that authentication method. For instructions, see [GitHub documentation](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-an-ssh-key-for-use-with-saml-single-sign-on).

:::

This setup assumes that each custom Python package is hosted within its own private GitHub repository. Installing multiple packages from a single private GitHub repository is not supported.


### Step 1: Specify the Private Repository in Your Project

To add a Python package from a private repository to your Software project, specify the repository's SSH URL in your project's `requirements.txt` file. This URL should be formatted as `git+ssh://git@github.com/<your-github-organization-name>/<your-private-repository>.git`.

For example, to install the `mypackage1` & `mypackage2` from `myorganization`, as well as `numpy v 1.22.1`, you would add the following to `requirements.txt`:

```
git+ssh://git@github.com/myorganization/mypackage1.git
git+ssh://git@github.com/myorganization/mypackage2.git
numpy==1.22.1
```

This example assumes that the name of each of your Python packages is identical to the name of its corresponding GitHub repository. In other words,`mypackage1` is both the name of the package and the name of the repository.

### Step 2. Create Dockerfile.build

1. In your Astro project, create a duplicate of your `Dockerfile` and name it `Dockerfile.build`.

2. In `Dockerfile.build`, add `AS stage` to the `FROM` line which specifies your Astronomer image. For example, if you use Astronomer Certified 2.2.5, your `FROM` line would be:

   ```text
   FROM quay.io/astronomer/ap-airflow:2.2.5 AS stage1
   ```

  :::warning

  If you use the default distribution of an Astronomer Certified image, make sure to remove the `-onbuild` part of the image. The Astronomer Certified distribution that does not specify `-onbuild` is built to be customizable and does not include default build logic. For more information, see [Distributions](ac-support-policy.md#distribution).

  Similarly, if you use an Astro Runtime image, ensure that the distribution you're using is the `-base` image.

  :::

3. In `Dockerfile.build` after the `FROM` line specifying your image, add the following configuration:

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
    - Securely mount your GitHub SSH key at build time. This ensures that the key itself is not stored in the resulting Docker image filesystem or metadata.
    - Install all Python-level packages in `requirements.txt` file, including those from a private GitHub repository.

  :::tip

  This example `Dockerfile.build` assumes Python 3.9, but some versions of Astronomer images may be based on a different version of Python. If your image is based on a version of Python that is not 3.9, replace `python 3.9` in the **COPY** commands listed under the `## Copy requirements directory` section of your `Dockerfile.build` with the correct Python version.

  To identify the Python version in your AC image, run:

     ```
     docker run quay.io/astronomer/<astronomer-image>:<astronomer-image-version> python --version
     ```

  Make sure to replace  `<astronomer-image>` `<astronomer-image-version>` with your own.

  :::

  :::info

  If your repository is hosted somewhere other than GitHub, replace the domain in the `ssh-keyscan` command with the domain where the package is hosted.

  :::

### Step 3. Build a Custom Docker Image

1. Run the following command to create a new Docker image from your `Dockerfile.build` file, making sure to replace `<ssh-key>` with your SSH private key file name and `<your-image>` with your Astronomer image:

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --ssh=github="$HOME/.ssh/<ssh-key>" -t custom-<your-image> .
    ```

    For example, if you have `quay.io/astronomer/ap-airflow:2.2.5` in your `Dockerfile.build`, this command would be:

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --ssh=github="$HOME/.ssh/<authorized-key>" -t custom-ap-airflow:2.2.5 .
    ```

  :::info

  If your repository is hosted somewhere other than GitHub, replace the location of your SSH key in the `--ssh` flag.

  :::

2. Replace the contents of your Software project's `Dockerfile` with the following:

   ```
   FROM custom-<your-image>
   ```

   For example, if your base image was `quay.io/astronomer/ap-airflow:2.2.5`, this line would be:

   ```
   FROM custom-ap-airflow:2.2.5
   ```

Your Software project can now utilize Python packages from your private GitHub repository.

</TabItem>

<TabItem value="pypi">

#### Install Python Packages from a Private PyPI Index

This topic provides instructions for building your Astro project using Python packages from a private PyPI index. In some organizations, python packages are prebuilt and pushed to a hosted private pip server (such as pypiserver or Nexus Repository) or managed service (such as PackageCloud or Gitlab). At a high level, this setup requires specifying your private packages in `requirements.txt`, creating a custom Docker image that changes where pip looks for packages, and building your project with this Docker image.

#### Prerequisites

To build from a private repository, you need:

- A [Software project](create-project.md).
- A private PyPI index with username and password authentication.

#### Step 1: Add privately hosted packages to requirements.txt

Privately hosted packages should already be built and pushed to the private repository. Depending on the repository used, it should be possible to browse and find the necessary package and version required. The package name and (optional) version can be added to requirements.txt in the same syntax as for publicly listed packages on [PyPI](https://pypi.org). The requirements.txt can contain a mixture of both publicly accessible and private packages.

:::warning

Ensure that the name of the package on the private repository does not clash with any existing python packages. The order that pip will search indices might produce unexpected results.

:::

#### Step 2: Create Dockerfile.build

1. In your Astro project, create a duplicate of your `Dockerfile` named `Dockerfile.build`.

2. In `Dockerfile.build`, add `AS stage` to the `FROM` line which specifies your Runtime image. For example, if you use Runtime 5.0.0, your `FROM` line would be:

   ```text
   quay.io/astronomer/astro-runtime:5.0.0-base AS stage1
   ```

   :::warning

   If you use the default distribution of Astronomer Certified, make sure to remove the `-onbuild` part of the image. The Astronomer Certified distribution that does not specify `-onbuild` is built to be customizable and does not include default build logic. For more information, see [Distributions](ac-support-policy.md#distribution).

   Similarly, if you use an Astro Runtime image, ensure that the distribution you're using is the `-base` image.

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

#### Step 3: Build a Custom Docker Image

1. Run the following command to create a new Docker image from your `Dockerfile.build` file, making sure to substitute in the pip repository and associated credentials:

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --build-arg PIP_EXTRA_INDEX_URL=https://${<repo-username>}:${<repo-password>}@<private-pypi-repo-domain-name> -t custom-<airflow-image> .
    ```

    For example, if you have `quay.io/astronomer/ap-airflow:2.2.5` in your `Dockerfile.build`, this command would be:

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --progress=plain --build-arg PIP_EXTRA_INDEX_URL=https://${<repo-username>}:${<repo-password>}@<private-pypi-repo-domain-name> -t custom-ap-airflow:2.2.5 .
    ```


2. Replace the contents of your Software project's `Dockerfile` with the following:

   ```
   FROM custom-<astronomer-image>
   ```

   For example, if your base image was `quay.io/astronomer/ap-airflow:2.2.5`, this line would be:

   ```
   FROM custom-ap-airflow:2.2.5
   ```

   Your Software project can now utilize Python packages from your private PyPi index.

</TabItem>
</Tabs>
