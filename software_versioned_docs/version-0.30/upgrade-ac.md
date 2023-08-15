---
title: 'Upgrade an Astronomer Certified Airflow Environment'
sidebar_label: 'Upgrade Astronomer Certified'
id: upgrade-ac
description: Upgrade your Apache Airflow environment by installing the latest version of Astronomer Certified.
---

> **Warning**
> No versions of Astronomer Certified (AC) are currently supported by Astronomer. Astronomer stopped releasing new versions of AC with the release of Apache Airflow 2.4. Astronomer recommends creating all new Deployments with Astro Runtime, as well as migrating existing Deployments from AC to Astro Runtime as soon as your organization is ready. See [Migrate to Runtime](migrate-to-runtime.md) and [Runtime image architecture](runtime-image-architecture.md).

## Overview

New versions of Astronomer Certified (AC) are released regularly to support new major, minor, or patch versions of Apache Airflow. To take advantage of both features as well as bug and security fixes, we recommend regularly upgrading to the latest version of AC.

Follow this guide to upgrade your Airflow environment either on a virtual machine with the AC Python Wheel or on Docker with the AC Docker image.

>**Note:** Upgrading to Airflow 2.0 requires additional steps and precautions. If you're upgrading from Airflow 1.10 to Airflow 2.0+, we recommend following Apache Airflow's [Upgrading to Airflow 2.0 guide](https://airflow.apache.org/docs/apache-airflow/stable/upgrading-to-2.html).

> **Note:** Once you upgrade Airflow versions, you cannot downgrade to an earlier version. The Airflow metadata database structurally changes with each release, which results in backwards incompatibility across versions.

## Upgrade Astronomer Certified on Docker

If you're upgrading an Astronomer Certified environment running on Docker, all you need to do is update your Dockerfile to reference a new Astronomer Certified Docker image.

1. Choose a new Astronomer Certified image based on the Airflow version you want to upgrade to. For a list of supported Astronomer Certified images, see [Astronomer Certified Lifecycle Schedule](ac-support-policy.md#astronomer-certified-lifecycle-schedule) or our [Quay.io repository](https://quay.io/repository/astronomer/ap-airflow?tab=tags).

2. Open the `Dockerfile` in your Airflow project directory.

    In your `Dockerfile`, replace the value in the existing `FROM` statement with the new Astronomer Certified Docker image you're upgrading to. For example, to upgrade to Airflow 2.1, your Dockerfile would include the following line:

    ```
    FROM quay.io/astronomer/ap-airflow:2.1.0-buster-onbuild
    ```

    If you're developing locally, make sure to save your changes before proceeding.

4. If you are using the Astronomer CLI, run `astro dev stop` followed by `astro dev start` to restart your 3 Airflow components (Scheduler, Webserver, and Database).

    If you aren't using the Astronomer CLI, you can manually stop all Airflow containers using `docker compose down --volumes --rmi all`.

5. Open the Airflow UI and click **About** > **Version** to confirm that the upgrade was successful. If you're developing locally with the Astronomer CLI, the Airflow UI is available at `http://localhost:8080/`.

## Upgrade the Astronomer Certified Python Wheel

Before upgrading, make sure both of the following are true:

* Your Airflow metadata DB is backed up.
* All DAGs have been paused and no tasks are running.

Then, for each machine running Airflow:

1. Upgrade Astronomer Certified using the following command, making sure to replace the dependencies and version number as needed:

    ```sh
    pip install --extra-index-url=https://pip.astronomer.io/simple/ 'astronomer-certified[<dependencies>]==<version-number>' --upgrade
    ```

    For example, if you wanted to upgrade to the latest patch version of Airflow 2.1 while using a Postgres database, your command would look something like this:

    ```sh
    pip install --extra-index-url=https://pip.astronomer.io/simple/ 'astronomer-certified[postgres]==2.1.0.*' --upgrade
    ```

2. Upgrade your metadata DB using the following command:

    ```sh
    airflow upgradedb
    ```

    > **Note:** This command changes to `airflow db upgrade` in Airflow 2.0+. For more information on major changes in 2.0, read [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/upgrading-to-2.html#airflow-cli-changes-in-2-0).

3. In a web browser, access the Airflow UI at http://localhost:8080 and click **About** > **Version**. Once there, you should see the correct Airflow version listed.

    > **Note:** The URL listed above assumes your Webserver is at port 8080 (default). To change that default, read [this forum post](https://forum.astronomer.io/t/i-already-have-the-ports-that-the-cli-is-trying-to-use-8080-5432-occupied-can-i-change-the-ports-when-starting-a-project/48).
