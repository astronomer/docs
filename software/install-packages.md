---
sidebar_label: 'Install Packages'
title: 'Install Packages on Astronomer Certified Images'
id: install-packages
description: Install OS-level and Python-level packages for Airflow using Astronomer Certified.
---

## Overview

By default, the Astronomer Certified Docker image is distributed with a collection of pre-installed Python and OS-level packages to help users integrate with popular applications. Python-level packages are dependencies that Airflow uses, while OS-level packages are dependencies required for the underlying Debian OS. For the full list of built-in packages, read [Image Architecture](image-architecture.md).

Depending on your use case and distribution of Astronomer Certified, you might want to install additional packages to your environment. This guide provides steps for installing dependencies to both Astronomer's Docker image and Python wheel.

## Install Packages to the Docker Image

If you use the Astronomer Certified Docker image to run Airflow, you can install packages directly onto your image via your `Dockerfile`. To install OS-level packages, you can specify them using a `RUN` directive with `apt-get`. For example, the following `Dockerfile` would install `your-os-package` on the image:

```dockerfile
FROM quay.io/astronomer/ap-airflow:2.2.0-buster-onbuild
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         <your-os-package> \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
```

To install a specific version of an OS-level package, use the following format for your installation command:

```
apt-get install <your-os-package>=<version> -V
```

To install a Python-level package, specify the package using a `RUN` directive with `pip install` instead. For example:

```dockerfile
FROM quay.io/astronomer/ap-airflow:2.2.0-buster-onbuild
RUN pip install --no-cache-dir --user <your-python-package>
```

To install a specific version of a Python-level package, include your package version in a pip [constraints file](https://pip-python3.readthedocs.io/en/latest/user_guide.html#constraints-files) and copy it into your Dockerfile. The base Docker image already has a pip constraints file which can be found [on GitHub](https://github.com/astronomer/ap-airflow/blob/master/2.1.0/buster/build-time-pip-constraints.txt).

> **Note:** Installing dependencies will look different if you are deploying your Docker image to Astronomer via the Astronomer CLI. For an Astronomer platform-based setup, read [Install Packages via the Astronomer CLI](install-packages.md#install-packages-via-the-astronomer-cli).

Once you rebuild your image with `docker-build`, the image will have access to any packages that you specified. To confirm that a package was installed:

1. Run `docker ps` and retrieve the container ID of your Scheduler container.
2. Run the following command:

    ```
    docker exec -it <scheduler-container-id> pip freeze | grep <package-name>
    ```

    If the package was successfully installed, you should see the following output:

    ```
    <package-name>==<version>
    ```


## Install Packages on a Virtual Machine

To build Python and OS-level packages into a machine running the Python wheel distribution of Astronomer Certified, run the following command:

```sh
sudo -u astro ~astro/airflow-venv/bin/pip install --extra-index-url=https://pip.astronomer.io/simple/ 'astronomer-certified[<your-package>]==<airflow-version>.*'
```

You can also create your own Python packages and install them into your Airflow environment via a Python wheel, or you can configure an environment variable to automatically add the packages to your Airflow project directory. For more information on this setup, read the [Apache Airflow documentation on managing modules](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/modules_management.html).

## Install Packages via Astronomer

If you're deploying the Astronomer Certified Docker image via Astronomer CLI, there are alternative workflows for installing packages and other dependencies to your image. For more information, read [Customize Images](customize-image.md).
