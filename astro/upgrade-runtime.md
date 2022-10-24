---
sidebar_label: 'Upgrade Runtime'
title: 'Upgrade Astro Runtime'
id: upgrade-runtime
description: Upgrade your Deployment's version of Astro Runtime.
---

import {siteVariables} from '@site/src/versions';


New versions of Astro Runtime are released regularly to support new Astro and Apache Airflow functionality. To take advantage of new features and bug and security fixes, Astronomer recommends upgrading Astro Runtime as new versions are available.

## Upgrade Considerations

Consider the following when you upgrade Astro Runtime:

- All versions of the Astro CLI support all versions of Astro Runtime. There are no dependencies between the two products.
- Upgrading to certain versions of Runtime might result in extended upgrade times or otherwise disruptive changes to your environment. To learn more, see [Version-specific upgrade considerations](upgrade-runtime.md#version-specific-upgrade-considerations).
- Astronomer does not support downgrading a Deployment on Astro to a lower version of Astro Runtime.

To stay up to date on the latest versions of Astro Runtime, see [Astro Runtime release notes](runtime-release-notes.md). For more information on Astro Runtime versioning and support, see [Astro Runtime versioning and lifecycle policy](runtime-version-lifecycle-policy.md). For a full collection of Astro Runtime Docker images, go to the [Astro Runtime repository on Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

## Prerequisites

- An [Astro project](create-project.md).
- An [Astro Deployment](create-deployment.md).
- The [Astro CLI](cli/install-cli.md).

:::info

If you're upgrading a local Airflow environment, you don't need an Astro Deployment and you can skip steps 3-4.

:::

## Step 1: Update Your Dockerfile

1. In your Astro project, open your `Dockerfile`.
2. Change the Docker image in the `FROM` statement of your `Dockerfile` to a new version of Astro Runtime.

    To upgrade to the latest version of Runtime, for example, change the `FROM` statement in your Dockerfile to:

    <pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}`}</code></pre>

    You must always specify the major, minor, and patch version of any given Astro Runtime version.

## Step 2: Test Astro Runtime locally

Astronomer recommends testing new versions of Astro Runtime locally before upgrading a Deployment on Astro.

1. Save the changes to your `Dockerfile`.
2. Open your project directory in your terminal and run `astro dev restart`. This restarts the Docker containers for the Airflow webserver, scheduler, triggerer, and Postgres metadata database.
3. Access the Airflow UI of your local environment by navigating to `http://localhost:8080` in your browser.
4. Confirm that your local upgrade was successful by scrolling to the bottom of any page. You should see your new Astro Runtime version in the footer as well as the version of Airflow it is based on.

    ![Runtime Version banner - Local](/img/docs/image-tag-airflow-ui-local.png)

## Step 3: Deploy to Astronomer

To push your upgraded project to an Astro Deployment, run:

```sh
astro deploy
```

For more information about deploying to Astro, see [Deploy code](deploy-code.md).

:::caution

Once you upgrade to a Deployment on Astro to a new version of Astro Runtime, you cannot roll back or downgrade to a lower version. If you attempt to do so, you will see an error in the Astro CLI and your request to deploy will not succeed.

:::

## Step 4: Confirm your upgrade on Astro

1. In the Cloud UI, select a Workspace and then select a Deployment.
2. Click **Open Airflow**.
3. In the Airflow UI, scroll to the bottom of any page. You should see your new Runtime version in the footer:

    ![Runtime Version banner - Astro](/img/docs/image-tag-airflow-ui-astro.png)

    You will also see an **Image tag** for your deploy. This tag is shown only for Deployments on Astro and is not generated for changes in a local environment.

## Version upgrade considerations

This topic contains information about upgrading to specific versions of Astro Runtime. This includes breaking changes, database migrations, and other considerations.

### Runtime 5 (Airflow 2.3)

#### Changes to the Airflow metadata database 

Astro Runtime 5.0.0, based on Airflow 2.3, includes changes to the schema of the Airflow metadata database. When you first upgrade to Runtime 5.0.0, consider the following:

- Upgrading to Runtime 5.0.0 can take 10 to 30 minutes or more depending on the number of task instances that have been recorded in the metadata database throughout the lifetime of your Deployment on Astro.
- Once you upgrade successfully to Runtime 5, you might see errors in the Airflow UI that warn you of incompatible data in certain tables of the database. For example:

    ```txt
    Airflow found incompatible data in the `dangling_rendered_task_instance_fields` table in your metadata database, and moved...
    ```

    These warnings have no impact on your tasks or DAGs and can be ignored. If you want to remove these warning messages from the Airflow UI, reach out to [Astronomer support](https://cloud.astronomer.io/support). If requested, Astronomer can drop incompatible tables from your metadata database.

For more information on Airflow 2.3, see ["Apache Airflow 2.3.0 is here"](https://airflow.apache.org/blog/airflow-2.3.0/) or the [Airflow 2.3.0 changelog](https://airflow.apache.org/docs/apache-airflow/2.3.0/release_notes.html#airflow-2-3-0-2022-04-30).
