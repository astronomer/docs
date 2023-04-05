---
sidebar_label: 'Install packages'
title: 'Install packages on Astronomer Certified images'
id: install-packages
description: Install OS-level and Python-level packages for Airflow using Astronomer Certified.
---

> **Warning**
> No versions of Astronomer Certified (AC) are currently supported by Astronomer. Astronomer stopped releasing new versions of AC with the release of Apache Airflow 2.4. Astronomer recommends creating all new Deployments with Astro Runtime, as well as migrating existing Deployments from AC to Astro Runtime as soon as your organization is ready. See [Migrate to Runtime](migrate-to-runtime.md) and [Runtime image architecture](runtime-image-architecture.md).

By default, the Astronomer Certified Docker image is distributed with a collection of pre-installed Python and OS-level packages to help users integrate with popular applications. Python-level packages are dependencies that Airflow uses, while OS-level packages are dependencies required for the underlying Debian OS. For the full list of built-in packages, read [Image Architecture](image-architecture.md).

Depending on your use case and distribution of Astronomer Certified, you might want to install additional packages to your environment. This guide provides steps for installing dependencies to both Astronomer's Docker image and Python wheel.

## Install packages to the Docker image

If you use the Astronomer Certified Docker image to run Airflow, you can install packages directly onto your image via your `Dockerfile`. To install OS-level packages, you can specify them using a `RUN` directive with `apt-get`. For example, the following `Dockerfile` would install `your-os-package` on the image:

```docker
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

```docker
FROM quay.io/astronomer/ap-airflow:2.2.0-buster-onbuild
RUN pip install --no-cache-dir --user <your-python-package>
```

To install a specific version of a Python-level package, include your package version in a pip [constraints file](https://pip-python3.readthedocs.io/en/latest/user_guide.html#constraints-files) and copy it into your Dockerfile. 

> **Note:** The process for installing dependencies is different if you are using the Astro CLI to deploy your Docker image to Astronomer. For an Astronomer platform-based setup, see [Install packages via the Astro CLI](install-packages.md#install-packages-via-the-astronomer-cli).

Once you rebuild your image with `docker-build`, the image will have access to any packages that you specified. To confirm that a package was installed:

1. Run `docker ps` and retrieve the container ID of your scheduler container.
2. Run the following command:

    ```
    docker exec -it <scheduler-container-id> pip freeze | grep <package-name>
    ```

    If the package was successfully installed, you should see the following output:

    ```
    <package-name>==<version>
    ```


## Install packages on a virtual machine

To build Python and OS-level packages into a machine running the Python wheel distribution of Astronomer Certified, run the following command:

```sh
sudo -u astro ~astro/airflow-venv/bin/pip install --extra-index-url=https://pip.astronomer.io/simple/ 'astronomer-certified[<your-package>]==<airflow-version>.*'
```

You can also create your own Python packages and install them into your Airflow environment via a Python wheel, or you can configure an environment variable to automatically add the packages to your Astro project directory. For more information on this setup, read the [Apache Airflow documentation on managing modules](http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/modules_management.html).

## Install packages using Astronomer

If you're using the Astro CLI to deploy the Astronomer Certified Docker image, there are alternative workflows for installing packages and other dependencies to your image. For more information, see [Customize images](customize-image.md).
