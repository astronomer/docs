---
sidebar_label: 'Astronomer Certified Architecture'
title: 'Astronomer Certified Image Architecture'
id: image-architecture
description: Reference documentation for Astronomer Certified, Astronomer Software's Docker image for Apache Airflow.
---

## Overview

The Astronomer Certified Docker image for Apache Airflow extends the community-developed Airflow image in a way that makes running Airflow more secure, reliable, and extensible. It is the default image for Airflow Deployments on Astronomer.

This guide provides reference information for the building blocks of Astronomer Certified, as well as information on its release and distribution.

## Distribution

Astronomer Certified is distributed both as a Python wheel and a Debian-based Docker image. These distributions vary slightly in scope and dependencies.

The Python wheel and Docker image are functionally identical to open source Apache Airflow. Additionally, they both include performance and stability improvements, including critical bug fixes and security patches.

The Astronomer Certified Docker image is built from the Python wheel and incorporates additional logic that makes it easier for users to both get started and run Airflow at scale. This includes:

- A robust testing suite that covers performance benchmarking and end-to-end functionality and upgrade testing for certified environments.
- A built-in directory of example DAGs that leverage Airflow's most powerful features.
- A collection of pre-installed Airflow provider packages.
- Full compatibility with the Astronomer Platform.

![Diagram of AC distribution scheme](/img/software/ac-diagram.png)

Every supported version of the Astronomer Certified Python wheel is available at [pip.astronomer.io](https://pip.astronomer.io/simple/astronomer-certified/). The Dockerfiles for all supported Astronomer Certified images can be found in [Astronomer's `ap-airflow` GitHub repository](https://github.com/astronomer/ap-airflow):

- [Airflow 2.2.4](https://github.com/astronomer/ap-airflow/blob/master/2.2.4/bullseye/Dockerfile)
- [Airflow 2.2.3](https://github.com/astronomer/ap-airflow/blob/master/2.2.3/bullseye/Dockerfile)
- [Airflow 2.2.2](https://github.com/astronomer/ap-airflow/blob/master/2.2.2/bullseye/Dockerfile)
- [Airflow 2.2.1](https://github.com/astronomer/ap-airflow/blob/master/2.2.1/bullseye/Dockerfile)
- [Airflow 2.2.0](https://github.com/astronomer/ap-airflow/blob/master/2.2.0/bullseye/Dockerfile)
- [Airflow 2.1.0](https://github.com/astronomer/ap-airflow/blob/master/2.1.0/buster/Dockerfile)
- [Airflow 2.0.2](https://github.com/astronomer/ap-airflow/blob/master/2.0.2/buster/Dockerfile)
- [Airflow 2.0.0](https://github.com/astronomer/ap-airflow/blob/master/2.0.0/buster/Dockerfile)
- [Airflow 1.10.15](https://github.com/astronomer/ap-airflow/blob/master/1.10.15/buster/Dockerfile)
- [Airflow 1.10.14](https://github.com/astronomer/ap-airflow/blob/master/1.10.14/buster/Dockerfile)
- [Airflow 1.10.12](https://github.com/astronomer/ap-airflow/blob/master/1.10.12/buster/Dockerfile)
- [Airflow 1.10.10](https://github.com/astronomer/ap-airflow/blob/master/1.10.10/buster/Dockerfile)

## Image Requirements

Running Airflow with the Astronomer Certified Docker image requires specific versions for key system components.  

- Python: 3.6, 3.7, 3.8, 3.9
- Database: PostgreSQL (11, 12), MySQL (5.7, 8.0+)
- System Distribution: Debian 10 (Buster)

> **Note:** While the Astronomer Certified Python Wheel supports Python versions 3.6, 3.7, and 3.8, Astronomer Certified Docker images have been tested and built only with Python 3.7. To run Astronomer Certified on Docker with Python 3.6 or 3.8, you can create a custom image with a different Python version specified. For more information, read [Change Python Versions](https://www.astronomer.iocustomize-image#build-with-a-different-python-version).

These requirements are slightly different for running only the Python wheel. For the Python wheel, you can use:

- Python: 3.6, 3.7, 3.8, 3.9
- Database: PostgreSQL (9.6, 10, 11, 12, 13), MySQL (5.7, 8+), SQLite (3.15.0+)
- System Distribution: Debian 10 (Buster)

 For more information on running a Python wheel installation of Astronomer Certified, read [Install on a Virtual Machine](single-node-install.md).

## Environment Variables

When an Airflow service is started, it checks a file for runtime environment variables. These are equivalent to values defined in Airflow's `airflow.cfg` file.

If you run the Astronomer Certified Docker image without the Astronomer platform, environment variables are defined in your Dockerfile. They can be overwritten with a runtime command, such as `docker run`.

If you're running the Astronomer Certified Docker image with the Astronomer platform, there are a few ways you can configure environment variables. For more information, read [Environment Variables](environment-variables.md).

Astronomer Certified supports the same environment variables as Apache Airflow. For a list of all configurable environment variables, read the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html).

The following table lists the essential environment variables used when running Airflow with Astronomer Certified. Only environment variables explicitly defined in the Dockerfile are listed here; all other environment variables have the same default value as they have in OSS Airflow.

| Variable                                        | Description                                                                   | Default Value                                     |
| ----------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------- |
| `AIRFLOW_PIP_VERSION`                             | The version of pip that is used to install Python packages and Airflow itself.            | 19.3.1                                            |
| `AIRFLOW_HOME`                                    | Filepath for your Airflow project directory.                                  | usr/local/airflow                                 |
| `AIRFLOW__WEBSERVER__BASE_URL`                    | The URL used to access the Airflow UI.                                        | http://localhost:8080                             |
| `ASTRONOMER_USER`                                 | The username for your Airflow user.                                           | astro                                             |
| `ASTRONOMER_UID `                                 | The ID for your Airflow user.                                                 | 5000                                              |
| `PIP_NO_CACHE_DIR`                                | Specifies whether to maintain copies of source files when installing via pip. | True                                              |
| `PYTHON_MAJOR_MINOR_VERSION`                      | The version of Python to use for Airflow.                                     | 3.9                                               |

## Provider Packages

Starting in version 2.0.0, the Astronomer Certified image includes provider packages that are utilized in some background processes, as well as packages which are commonly used by the Airflow community. The following table contains version information for each provider package installed as part of Astronomer Certified:

| Astronomer Certified | [amazon](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/index.html) |[azure](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/index.html) | [celery](https://airflow.apache.org/docs/apache-airflow-providers-celery/stable/index.html) | [cncf.kubernetes](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/index.html) | [elasticsearch](https://airflow.apache.org/docs/apache-airflow-providers-elasticsearch/stable/index.html) | [ftp](https://airflow.apache.org/docs/apache-airflow-providers-ftp/stable/index.html) | [google](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/index.html) |   [http](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/index.html) |[imap](https://airflow.apache.org/docs/apache-airflow-providers-imap/stable/index.html) | [mysql](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/index.html) | [postgres](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/index.html) | [redis](https://airflow.apache.org/docs/apache-airflow-providers-redis/stable/index.html) | [slack](https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/index.html) | [sqlite](https://airflow.apache.org/docs/apache-airflow-providers-sqlite/stable/index.html) | [ssh](https://airflow.apache.org/docs/apache-airflow-providers-ssh/stable/index.html) |
| -------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
|**2.0.0**|1.0.0|1.1.0|1.0.0|1.0.1|1.0.4|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|1.0.0|
|**2.0.2**|1.3.0|1.3.0|1.0.1|1.2.0|1.0.4|1.0.1|2.2.0|1.1.1|1.0.1|1.1.0|1.0.1|1.0.1|3.0.0|1.0.2|1.3.0|
|**2.1.0**|1.4.0|2.0.0|1.0.1|1!1.2.1|1.0.4|1.1.0|3.0.0|2.0.0|1.0.1|1.1.0|1.0.2|1.0.1|3.0.0|1.0.2|1.3.0|
|**2.1.1**|1!2.0.0|1!3.0.0|1!2.0.0|1!2.0.0|1!2.0.1|1!2.0.0|1!4.0.0|1!2.0.0|1!2.0.0|1!2.0.0|1!2.0.0|1!2.0.0|1!4.0.0|1!2.0.0|1!2.0.0|
|**2.1.3**|1!2.1.0|1!3.1.0|1!2.0.0|1!2.0.2|1!2.0.2|1!2.0.0|1!5.0.0|1!2.0.0|1!2.0.0|1!2.1.0|1!2.0.0|1!2.0.0|1!4.0.0|1!2.0.0|1!2.1.0|
|**2.1.4**|1!2.2.0|1!3.1.1|1!2.1.0|1!2.0.2|1!2.0.3|1!2.0.1|1!5.1.0|1!2.0.1|1!2.0.1|1!2.1.1|1!2.2.0|1!2.0.1|1!4.0.1|1!2.0.1|1!2.1.1|
|**2.2.0**|1!2.2.0|1!3.2.0|1!2.1.0|1!2.0.3|1!2.0.3|1!2.0.1|1!6.0.0|1!2.0.1|1!2.0.1|1!2.1.1|1!2.3.0|1!2.0.1|1!4.1.0|1!2.0.1|1!2.2.0|
|**2.2.1**|1!2.2.0|1!3.2.0|1!2.1.0|1!2.0.3|1!2.0.3|1!2.0.1|1!6.0.0|1!2.0.1|1!2.0.1|1!2.1.1|1!2.3.0|1!2.0.1|1!4.1.0|1!2.0.1|1!2.2.0|
|**2.2.2**|1!2.3.0|1!3.3.0|1!2.1.0|1!2.1.0|1!2.1.0|1!2.0.1|1!6.1.0|1!2.0.1|1!2.0.1|1!2.1.1|1!2.3.0|1!2.0.1|1!4.1.0|1!2.0.1|1!2.3.0|
|**2.2.3**|1!2.3.0|1!3.3.0|1!2.1.0|1!2.1.0|1!2.1.0|1!2.0.1|1!6.1.0|1!2.0.1|1!2.0.1|1!2.1.1|1!2.3.0|1!2.0.1|1!4.1.0|1!2.0.1|1!2.3.0|
|**2.2.4**|1!3.0.0|1!3.6.0|1!2.1.0|1!3.0.2|1!2.2.0|1!2.0.1|1!6.4.0|1!2.0.3|1!2.2.0|1!2.2.0|1!3.0.0|1!2.0.1|1!4.2.0|1!2.1.0|1!2.4.0|

## System Dependencies

The Astronomer Certified Docker image includes a number of OS-level dependencies for running basic system processes. These dependencies can be installed in the Python Wheel as described in [Install Packages](install-packages.md).

- [apt-utils](https://packages.debian.org/buster/apt-utils)
- [build-essential](https://packages.debian.org/buster/build-essential)
- [curl](https://packages.debian.org/buster/curl)
- [build-essential](https://packages.debian.org/buster/build-essential)
- [default-libmysqlclient-dev](https://packages.debian.org/buster/default-libmysqlclient-dev)
- [libmariadb3](https://packages.debian.org/buster/libmariadb3)
- [freetds-bin](https://packages.debian.org/buster/freetds-bin)
- [gosu](https://packages.debian.org/buster/gosu)
- [libffi6](https://packages.debian.org/buster/libffi6)
- [libffi-dev](https://packages.debian.org/buster/libffi-dev)
- [libkrb5-3](https://packages.debian.org/buster/libkrb5-3)
- [libkrb5-dev](https://packages.debian.org/buster/libkrb5-dev)
- [libpq5](https://packages.debian.org/buster/libpq5)
- [libpq-dev](https://packages.debian.org/buster/libpq-dev)
- [libsasl2-2](https://packages.debian.org/buster/libsasl2-2)
- [libsasl2-dev](https://packages.debian.org/buster/libsasl2-dev)
- [libsasl2-modules](https://packages.debian.org/buster/libsasl2-modules)
- [libssl1.1](https://packages.debian.org/buster/libssl1.1)
- [libssl-dev](https://packages.debian.org/buster/libssl-dev)
- [locales](https://packages.debian.org/buster/locales)
- [netcat](https://packages.debian.org/buster/netcat)
- [rsync](https://packages.debian.org/buster/rsync)
- [sasl2-bin](https://packages.debian.org/buster/sasl2-bin)
- [sudo](https://packages.debian.org/buster/sudo)
- [tini](https://packages.debian.org/buster/tini)

## Extras

Astronomer Certified includes a few packages that don't have a corresponding provider. These packages are used for basic system functions or optional Airflow functionality. The following list contains all extra packages built into Astronomer Certified by default:

- `async`: Provides asynchronous workers for Gunicorn
- `password`: Adds support for user password hashing
- `statsd`: Adds support for sending metrics to StatsD
- `virtualenv`: Adds support for running Python tasks in local virtual environments
