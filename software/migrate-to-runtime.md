---
title: 'Migrate a Deployment from Astronomer Certified to Astro Runtime'
sidebar_label: 'Migrate to Astro Runtime'
id: migrate-to-runtime
description: Run an upgrade progress to migrate your Software Deployment from Astronomer Certified (AC) to Astro Runtime.
---

import {siteVariables} from '@site/src/versions';

Astro Runtime builds on the reliability of Astronomer Certified (AC) with new features that center on usability and performance.

Migrating a Deployment to Astro Runtime is similar to the standard upgrade process. There are no known disruptions when migrating a Deployment from AC to the equivalent version of Astro Runtime.

## Prerequisites

To migrate to Astro Runtime, you must have Astronomer Software 0.29 or later. See [Upgrade Astronomer](upgrade-astronomer.md).

## Differences between Astro Runtime and Astronomer Certified

Functionally, Runtime images are similar to AC images. They both include:

- Timely support for new patch, minor, and major versions of Apache Airflow.
- Support lifecycles that extend beyond those offered by the open source community.
- Regularly backported bug and security fixes.

Astro Runtime includes additional features which are not available in AC images, including:

- Exclusive features for improving task execution, including smart task concurrency defaults and high availability configurations.
- The `astronomer-providers` package, which is an open source collection of Apache Airflow providers and modules maintained by Astronomer.
- Airflow UI improvements, such as showing the Deployment Docker image tag in the footer of all UI pages.

See [Runtime Architecture](runtime-image-architecture.md) for more detailed information about Runtime's distribution and features.

All versions of AC have an equivalent version of Astro Runtime. To see the equivalent version of Astro Runtime for a Deployment running AC, open the Deployment in the Software UI and go to **Settings**. The equivalent version of Astro Runtime is shown in the **Migrate to Runtime-[Version number]** button.

## Astronomer Houston API migration considerations 

If you're using the Astronomer Houston API and you're migrating from AC to Astro Runtime, you'll need to replace `airflowVersion` arguments with `runtimeVersion` arguments in your scripts. You can use the [GraphQL Playground](https://www.apollographql.com/docs/apollo-server/api/plugin/landing-pages/#graphql-playground-landing-page/) to evaluate the API calls in your scripts. To access the Houston GraphQL playground, go to `https://houston.BASEDOMAIN/v1/`.

## Step 1: Start the migration process

1. In the Software UI, open your Deployment.
2. Click the **Settings** tab and then click **Migrate to Runtime-[Version Number]**.

You can't simultaneously migrate to Astro Runtime and upgrade your Deployment. To upgrade to a later version of Runtime than your equivalent AC version, you must first either upgrade Astronomer Certified or migrate to Astro Runtime before upgrading. For example, the upgrade path from AC 2.2.3 (Airflow 2.2.3) to Runtime 5.0.4 (Airflow 2.3.0) would be:

AC 2.2.3 > AC 2.3.0 > Astro Runtime 5.0.4

If you prefer to use the Astro CLI, you can run `astro deployment runtime migrate --deployment-id=<your-deployment-id>` to start the upgrade process.

## Step 2: Migrate your Astro project

1. In your Astro project, open your `Dockerfile`.
2. Update the `FROM` line of your project's `Dockerfile` to reference a new Astro Runtime image. For example, to migrate to Astro Runtime 5.0.4, you would change the `FROM` line to:

    ```sh
    FROM quay.io/astronomer/astro-runtime:5.0.4
    ```

    For a list of currently supported Astronomer images, see:

    - [AC Lifecycle Schedule](ac-support-policy.md#astronomer-certified-lifecycle-schedule)
    - [Astro Runtime Lifecycle Schedule](https://docs.astronomer.io/astro/runtime-version-lifecycle-policy#astro-runtime-lifecycle-schedule)

  :::warning

  Astronomer does not support Airflow downgrades. After you upgrade your Airflow version, you can't revert to an earlier version.

  :::

3. Optional. Test your migration to Astro Runtime locally by running:

    ```sh
    astro dev restart
    ```

    All 4 running Docker containers for each of the Airflow components restart and begin running your new image.

    To confirm that your migration was successful, open the Airflow UI at `localhost:8080` and scroll to the bottom of any page. You should see your new Runtime version in the footer.

## Step 3: Deploy to Astronomer

1. To push your migration from Astronomer Certified to Astro Runtime on Astronomer Software, run:

    ```sh
    astro deploy
    ```

2. In the Software UI, open your Deployment and click **Open Airflow**.
3. Scroll to the bottom of any page. You should see your new Runtime version in the footer.
