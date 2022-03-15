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
