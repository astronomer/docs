---
sidebar_label: 'Customize Image'
title: 'Customize Your Image on Astronomer Software'
description: Customize your Astronomer Certified image, including adding dependencies and running commands on build.
---

## Overview

The Astronomer CLI was built to be the easiest way to develop with Apache Airflow, whether you're developing on your local machine or deploying code to Astronomer. The guidelines below will cover a few ways you can customize the Docker Image that gets pushed up to Airflow every time you rebuild your image locally via `$ astro dev start` or deploy to Astronomer via `$ astro deploy`.

More specifically, this doc includes instructions for how to:

- Add Python and OS-level Packages
- Add dependencies
- Run commands on build
- Access the Airflow CLI
- Add Environment Variables Locally
- Build from a Private Repository

> **Note:** The guidelines below assume that you've initialized a project on Astronomer via `$ astro dev init`. If you haven't done so already, refer to our ["CLI Quickstart" doc](cli-quickstart.md).

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

> **Note:** Astronomer Certified, Astronomer's distribution of Apache Airflow, is available both as a Debian and Alpine base. We strongly recommend using Debian, as it's much easier to install dependencies and often presents less incompatibility issues than an Alpine Linux image. For details on both, refer to our [Airflow Versioning Doc](manage-airflow-versions.md).

## Add Other Dependencies

In the same way you can build Python and OS-level Packages into your image, you're free to build additional dependencies and files for your DAGs to use.

In the example below, we'll add a folder of `helper_functions` with a file (or set of files) that our Airflow DAGs can then use.

### Add the folder into your project directory

```bash
virajparekh@orbiter:~/cli_tutorial$ tree
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

> **Note:** If you're interested in programmatically managing Airflow Connections, Variables or Environment Variables, we'd recommend integrating a ["Secret Backend"](secrets-backend.md) to help you do so.

### Add Airflow Connections, Pools, Variables

By default, the `airflow_settings.yaml` file will be structured as following:

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

The Astronomer CLI is built on top of [Docker Compose](https://docs.docker.com/compose/), a tool for defining and running multi-container Docker applications. If you're interested in overriding any of our CLI's default configurations ([found here](https://github.com/astronomer/astro-cli/blob/v0.16.5/airflow/include/composeyml.go)), you're free to do so by adding a `docker-compose.override.yml` file to your Astronomer project directory. Any values in this file will override default settings run upon every `$ astro dev start`.

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

> **Note:** The Astronomer CLI does _not_ currently support overrides to Environment Variables. For more information on how to set, configure and customize those values, refer to our ["Environment Variables" doc](environment-variables.md).

## Access to the Airflow CLI

You're free to use native Airflow CLI commands on Astronomer when developing locally by wrapping them around docker commands.

To add a connection, for example, you can run:

```bash
docker exec -it SCHEDULER_CONTAINER bash -c "airflow connections -a --conn_id test_three  --conn_type ' ' --conn_login etl --conn_password pw --conn_extra {"account":"blah"}"
```

Refer to the native [Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/usage-cli.html) for a list of all commands.

## Add Environment Variables Locally

The Astronomer CLI comes with the ability to  bring in Environment Variables from a specified file by running `$ astro dev start` with an `--env` flag as seen below:

```
astro dev start --env .env
```

> **Note:** This feature is limited to local development only. Whatever `.env` you use locally will _not_ be bundled up when you deploy to Astronomer.
>
> For more detail on how to add Environment Variables both locally and on Astronomer, refer to our [Environment Variables doc](environment-variables.md).

## Build from a Private Repository

If you're interested in bringing in custom Python Packages stored in a Private GitHub repo, you're free to do that on Astronomer.

Read below for guidelines.

### Prerequisites

- The Astronomer CLI
- An intialized Astronomer Airflow project and corresponding directory
- An [SSH Key](https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to your Private GitHub repo

If you haven't initialized an Airflow Project on Astronomer (by running `$ astro dev init`), reference our [CLI Quickstart Guide](cli-quickstart.md).

### Step 1. Create a file called Dockerfile.build

1. In your directory, create a file called `Dockerfile.build` that's parallel to your `Dockerfile`.

2. To the first line of that file, add a "FROM" statement that specifies the Airflow Image you want to run on Astronomer and ends with `AS stage`.

If you're running the Debian-based Astronomer Certified image for Airflow 1.10.12, this would be:

```
FROM quay.io/astronomer/ap-airflow:1.10.12-buster AS stage1
```

For a list of all Airflow Images supported on Astronomer, refer to [Upgrade Apache Airflow on Astronomer](manage-airflow-versions.md).

> **Note:** Do NOT include `-onbuild` at the end of your Airflow Image as you typically would in your `Dockerfile`.

3. Immediately below the `FROM...` line specified above, add the folllowing:

```
LABEL maintainer="Astronomer <humans@astronomer.io>"
ARG BUILD_NUMBER=-1
LABEL io.astronomer.docker=true
LABEL io.astronomer.docker.build.number=$BUILD_NUMBER
LABEL io.astronomer.docker.airflow.onbuild=true
# Install Python and OS-Level Packages
COPY packages.txt .
RUN cat packages.txt | xargs apk add --no-cache

FROM stage1 AS stage2
RUN mkdir -p /root/.ssh
ARG PRIVATE_RSA_KEY=""
ENV PRIVATE_RSA_KEY=${PRIVATE_RSA_KEY}
RUN echo "${PRIVATE_RSA_KEY}" >> /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN apk update && apk add openssh-client
RUN ssh-keyscan -H github.com >> /root/.ssh/known_hosts
# Install Python Packages
COPY requirements.txt .
RUN pip install --no-cache-dir -q -r requirements.txt

FROM stage1 AS stage3
# Copy requirements directory
COPY --from=stage2 /usr/lib/python3.6/site-packages/ /usr/lib/python3.6/site-packages/
COPY . .
```

In 3 stages, this file is bundling up your SSH keys, OS-Level packages in `packages.txt` and Python Packages in `requirements.txt` from your private directory into a Docker image.

A few notes:
- The `Private RSA Key` = [SSH Key generated via GitHub](https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- Make sure to replace the first line of this file (`FROM`..) with your Airflow Image (Step 2 above)
- If you don't want keys in this file to be pushed back up to your GitHub repo, consider adding this file to `.gitignore`
- Make sure your custom OS-Level packages are in `packages.txt` and your Python packages in `requirements.txt` within your repo
- If you're running Python 3.7 on your machine, replace the reference to Python 3.6 under `# Copy requirements directory` with `/usr/lib/python3.7/site-packages/` above

### Step 2. Build your Image

Now, let's build a Docker image based on the requirements above that we'll then reference in your Dockerfile, tag, and push to Astronomer.

Run the following in your terminal:

```
docker build -f Dockerfile.build --build-arg PRIVATE_RSA_KEY="$(cat ~/.ssh/id_rsa)" -t custom-<airflow-image> .
```

If you have `quay.io/astronomer/ap-airflow:1.10.12-buster` in your `Dockerfile.build`, for example, this command would be:

```
docker build -f Dockerfile.build --build-arg PRIVATE_RSA_KEY="$(cat ~/.ssh/id_rsa)" -t custom-ap-airflow:1.10.12-buster .
```

### Step 3. Replace your Dockerfile

Now that we've built your custom image, let's reference that custom image in your `Dockerfile`. Replace the current contents of your `Dockerfile` with the following:

```
FROM custom-<airflow-image>
```

If you're running `quay.io/astronomer/ap-airflow:1.10.10-alpine3.10` as specified above, this line would read:

```
FROM custom-ap-airflow:1.10.12-buster
```

### Step 4. Push your Custom Image to Astronomer

Now, let's push your new image to Astronomer.

- If you're developing locally, run `$ astro dev stop` > `$ astro dev start`
- If you're pushing up to Astronomer, you're free to deploy by running `$ astro deploy` or by triggering your CI/CD pipeline

For more detail on the Astronomer deployment process, refer to [Deploy to Astronomer via the CLI](deploy-cli.md).

## Build with a Different Python Version

While the Astronomer Certified (AC) Python Wheel supports Python versions 3.6, 3.7, and 3.8, AC Docker images have been tested and built only for Python 3.7.

To run Astronomer Certified on Docker with Python versions 3.6 or 3.8, you need to create a custom version of the image, specify the `PYTHON_MAJOR_MINOR_VERSION` build argument, and push the custom image to an existing Docker registry. To do so:

1. Using `docker build`, build a custom [Astronomer Certified Docker image](https://github.com/astronomer/ap-airflow) and specify `PYTHON_MAJOR_MINOR_VERSION` for the version of Python you'd like to support. For example, the command for building a custom Astronomer Certified image for Airflow 2.0.0 with Python 3.8 would look something like this:

    ```sh
    docker build --build-arg PYTHON_MAJOR_MINOR_VERSION=3.8 -t <your-registry>/ap-airflow:<image-tag> https://github.com/astronomer/ap-airflow.git#master:2.0.0/buster
    ```

    We recommend using an image tag that indicates the image is using a different Python version, such as `2.0.0-buster-python3.8`.

    > **Note:** To use a different version of Airflow, update the URL to point towards the desired Airflow version. For instance, if you're running Airflow 1.10.14, the GitHub URL here would be: `https://github.com/astronomer/ap-airflow.git#master:1.10.14/buster`

2. Push the custom image to your Docker registry. Based on the example in the previous step, the command to do so would look something like this:

    ```sh
    docker push <your-registry>/ap-airflow:<image-tag>
    ```

3. Update the `FROM` line of your `Dockerfile` to reference the custom image. Based on the previous example, the line would read:

    ```
    FROM <your-registry>/ap-airflow:<image-tag>
    ```

> **Note:** Astronomer Certified Docker images for Apache Airflow 1.10.14+ are Debian-based only. To run Docker images based on Alpine-Linux for Airflow versions 1.10.7, 1.10.10, or 1.10.12, specify `alpine3.10` instead of `buster` in the GitHub URL.
