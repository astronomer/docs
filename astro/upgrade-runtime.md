---
sidebar_label: 'Upgrade Runtime'
title: 'Upgrade Astro Runtime'
id: upgrade-runtime
description: Upgrade your Deployment's version of Astro Runtime.
---

## Overview

New versions of Astro Runtime are released regularly to support new features from both Astro and Apache Airflow. To take advantage of new functionality, as well as bug and security fixes, we recommend regularly upgrading your Deployment's Runtime version.

Follow this guide to upgrade a Deployment's Airflow environment using the Astro CLI. You can use these steps to upgrade to any major, minor, or patch version of Runtime.

## Step 1: Update Your Dockerfile

1. In your local Astro project directory, open your `Dockerfile`.
2. Update the [image](runtime-version-lifecycle-policy.md#runtime-images) in the `FROM` statement of your Dockerfile to a new version of Runtime.

    Once you upgrade Runtime versions, you can't downgrade to an earlier version. The Airflow metadata database structurally changes with each release, making for backwards incompatibility across versions.

    For a table reference of available Runtime versions, see [Available Versions](runtime-version-lifecycle-policy.md#available-runtime-versions). For Astronomer's platform's full collection of Docker Images, go to the [Astro Runtime repository on Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags). To see what changes are included in each version, read [Runtime Release Notes](runtime-release-notes.md).

## Step 2: Deploy Your Image

To test your upgrade locally:

1. Save the changes to your Dockerfile.
2. In your project directory, run `astrocloud dev restart`. This restarts the Docker containers for the Airflow Webserver, Scheduler, and Postgres Metadata DB.
3. Access your locally-running Airflow environment at `http://localhost:8080`.

To push your upgrade to Astro, run `astrocloud deploy` and select the Deployment you want to upgrade. This will bundle your updated directory, re-build your image and push it to your hosted Deployment on Astro.

## Step 3: Confirm Your Upgrade

1. In the Cloud UI, go to your upgraded Deployment.
2. Click **Open Airflow**.
3. In the Airflow UI, scroll to the bottom of any page. You should see your new Runtime version in the footer:

    ![Runtime Version banner](/img/docs/image-tag-airflow-ui.png)

## Upgrade Considerations

This topic contains information about upgrading to specific versions of Astro Runtime. This includes notes on breaking changes, database migrations, and other considerations that might depend on your use case.

### Runtime 5.0.x (Airflow 2.3.x)

Astro Runtime 5.0.0 includes changes to the schema of the Airflow metadata database. When you first upgrade to Runtime 5, consider the following:

- Upgrading to Runtime 5.0 can take 10 to 30 minutes or more depending on the number of task instances that have been recorded in the metadata database throughout the lifetime of your Deployment. During the upgrade, scheduled tasks will continue to execute but new tasks will not be scheduled.
- Once you upgrade successfully to Runtime 5.0, you might see errors in the Airflow UI that warn you of incompatible data in certain tables of the database. For example:

    ```
    Airflow found incompatible data in the `dangling_rendered_task_instance_fields` table in your metadata database, and moved...
    ```

    These warnings have no impact on your tasks or DAGs and can be ignored. If you want to remove these warning messages from the Airflow UI, reach out to [Astronomer Support](https://support.astronomer.io). If requested, Astronomer can drop incompatible tables from your metadata database.

For more information on Airflow 2.3, see ["Apache Airflow 2.3.0 is here"](https://airflow.apache.org/blog/airflow-2.3.0/) or the [Airflow 2.3.0 changelog](https://airflow.apache.org/docs/apache-airflow/2.3.0/release_notes.html#airflow-2-3-0-2022-04-30).
