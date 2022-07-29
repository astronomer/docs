---
sidebar_label: 'Upgrade Runtime'
title: 'Upgrade Astro Runtime'
id: upgrade-runtime
description: Upgrade your Deployment's version of Astro Runtime.
---

## Overview

New versions of Astro Runtime are released regularly to support new functionality from both Astro and the Apache Airflow open source project. To take advantage of new features as well as bug and security fixes, we recommend regularly upgrading Astro Runtime as new versions are released.

Follow this guide to upgrade Astro Runtime locally or for a Deployment on Astro. You can use these steps to upgrade to any major, minor, or patch version of Astro Runtime.

As you plan to upgrade, keep in mind that:

- All versions of the Astro CLI support all versions of Astro Runtime. There are no dependencies between the two products.
- Upgrading to certain versions of Runtime might result in extended upgrade times or otherwise disruptive changes to your environment. To learn more, see [Upgrade Considerations](upgrade-runtime.md#upgrade-considerations).
- Astronomer does not support downgrading a Deployment on Astro to a lower version of Astro Runtime.

To stay up to date on the latest versions of Astro Runtime, see [Astro Runtime Release Notes](runtime-release-notes.md). For more information on Astro Runtime versioning and support, see [Astro Runtime Versioning and Lifecycle Policy](runtime-version-lifecycle-policy.md). For a full collection of Astro Runtime Docker images, go to the [Astro Runtime repository on Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

## Prerequisites

To upgrade to a new version of Astro Runtime, you must have:

- An [Astro project](create-project.md).
- An [Astro Deployment](configure-deployment.md).
- The [Astro CLI](install-cli.md).

:::info

If you're only upgrading a local Airflow environment, you do not need an Astro Deployment and can skip steps 3-4 of this guide. 

:::

## Step 1: Update Your Dockerfile

1. In your Astro project, open your `Dockerfile`.
2. Change the Docker image in the `FROM` statement of your `Dockerfile` to a new version of Astro Runtime.

    To upgrade to Astro Runtime 5.0.1, for example, change the `FROM` statement in your Dockerfile to:

    ```
    FROM quay.io/astronomer/astro-runtime:5.0.1
    ```

    You must always specify the major, minor, and patch version of any given Astro Runtime version.

## Step 2: Test Astro Runtime Locally

We strongly recommend testing new versions of Astro Runtime locally before upgrading a Deployment on Astro.  To test your upgrade locally:

1. Save the changes to your `Dockerfile`.
2. Open your project directory in your terminal and run `astrocloud dev restart`. This restarts the Docker containers for the Airflow Webserver, Scheduler, Triggerer, and Postgres metadata database.
3. Access the Airflow UI of your local environment by navigating to `http://localhost:8080` in your browser.
4. Confirm that your local upgrade was successful by scrolling to the bottom of any page. You should see your new Astro Runtime version in the footer as well as the version of Airflow it is based on.

    ![Runtime Version banner - Local](/img/docs/image-tag-airflow-ui-local.png)

## Step 3: Deploy to Astronomer

To push your upgraded project to an Astro Deployment, run:

```sh
astrocloud deploy
```

For more information about deploying to Astro, see [Deploy Code](deploy-code.md).

:::caution

Once you upgrade to a Deployment on Astro to a new version of Astro Runtime, you cannot roll back or downgrade to a lower version. If you attempt to do so, you will see an error in the Astro CLI and your request to deploy will not succeed.

:::

## Step 4: Confirm Your Upgrade on Astro

1. In the Cloud UI, go to **Your Workspaces** > **Deployments** and select your Deployment.
2. Click **Open Airflow**.
3. In the Airflow UI, scroll to the bottom of any page. You should see your new Runtime version in the footer:

    ![Runtime Version banner - Astro](/img/docs/image-tag-airflow-ui-astro.png)

    You will also see an **Image tag** for your deploy. This tag is shown only for Deployments on Astro and is not generated for changes in a local environment.

## Upgrade Considerations

This topic contains information about upgrading to specific versions of Astro Runtime. This includes notes on breaking changes, database migrations, and other considerations that might depend on your use case.

### Runtime 5 (Airflow 2.3)

Astro Runtime 5, based on Airflow 2.3, includes changes to the schema of the Airflow metadata database. When you first upgrade to Runtime 5, consider the following:

- Upgrading to Runtime 5 can take 10 to 30 minutes or more depending on the number of task instances that have been recorded in the metadata database throughout the lifetime of your Deployment on Astro.
- Once you upgrade successfully to Runtime 5, you might see errors in the Airflow UI that warn you of incompatible data in certain tables of the database. For example:

    ```txt
    Airflow found incompatible data in the `dangling_rendered_task_instance_fields` table in your metadata database, and moved...
    ```

    These warnings have no impact on your tasks or DAGs and can be ignored. If you want to remove these warning messages from the Airflow UI, reach out to [Astronomer Support](https://support.astronomer.io). If requested, Astronomer can drop incompatible tables from your metadata database.

For more information on Airflow 2.3, see ["Apache Airflow 2.3.0 is here"](https://airflow.apache.org/blog/airflow-2.3.0/) or the [Airflow 2.3.0 changelog](https://airflow.apache.org/docs/apache-airflow/2.3.0/release_notes.html#airflow-2-3-0-2022-04-30).
