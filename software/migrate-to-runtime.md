---
title: 'Migrate a Deployment from Astronomer Certified to Astro Runtime'
sidebar_label: 'Migrate to Astro Runtime'
id: migrate-to-runtime
description: Run an upgrade progress to migrate your Software Deployment from Astronomer Certified to Astro Runtime.
---

Astro Runtime builds on the reliability of Astronomer Certified with new features and provider packages. Astronomer plans to no longer release new versions of Astronomer Certified starting with a minor release of Airflow to be determined. To avoid disruption in the future, Astronomer recommends migrating Deployments from Certified to Runtime now.

Migrating a Deployment from Astronomer Certified is similar to the standard upgrade process. There are no known disruptions when migrating a Deployment from Astronomer Certified to the equivalent version of Astro Runtime.

## Differences between Astro Runtime and Astronomer Certified

Functionally, Runtime images are similar to Certified images. They both include:

- Same-day support for Apache Airflow releases.
- Extended support lifecycles.
- Regularly backported bug and security fixes.

Astro Runtime includes additional features which are not available in Astronomer Certified images, including:

- The `astronomer-providers` package, which includes a set of deferrable operators build and maintained by Astronomer.
- Airflow UI improvements, such as the showing your Deployment's Docker image tag in the footer of all UI pages.
- Future Runtime-exclusive features, such as new Airflow components and improvements to the DAG development experience.

See [Runtime Architecture](runtime-architecture.md) for more detailed information about Runtime's distribution and features.

All versions of Astronomer Certified have an equivalent version of Astro Runtime. To see the equivalent version of Astro Runtime for a Deployment running Astronomer Certified, open the Deployment in the Software UI and go to **Settings**. The equivalent version of Astro Runtime is shown in the **Migrate to Runtime-[Version number]** button.

## Step 1: Start the migration process

1. In the Software UI, open your Deployment.
2. In the **Settings** tab, click **Migrate to Runtime-[Version Number]**.

You can't simultaneously migrate to Astro Runtime and upgrade your Deployment. To upgrade to a later version of Runtime than your equivalent Astronomer Certified version, you must first upgrade Astronomer Certified before migrating to Runtime. For example, the upgrade path from Astronomer Certified 2.2.3 (Airflow 2.2.3) to Runtime 5.0.4 (Airflow 2.3.0) would be:

Astronomer Certified 2.2.3 > Astronomer Certified 2.3.0 > Astro Runtime 5.0.4

If you prefer to use the Astro CLI, you can run `astro deployment runtime migrate --deployment-id=<your-deployment-id>` to start the upgrade process.

## Step 2: Migrate your Astro project

1. In your Astro project, open your `Dockerfile`.
2. Update the `FROM` line of your project's `Dockerfile` to reference a new Astronomer image. For example, to upgrade to the latest version of Astro Runtime, you would change the `FROM` line to:

    <pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}`}</code></pre>

    For a list of currently supported Astronomer images, see:

    - [Astronomer Certified Lifecycle Schedule](ac-support-policy.md#astronomer-certified-lifecycle-schedule)
    - [Astro Runtime Lifecycle Schedule](https://docs.astronomer.io/astro/runtime-version-lifecycle-policy#astro-runtime-lifecycle-schedule)

  :::warning

  After you upgrade your Airflow version, you can't revert to an earlier version.

  :::

3. Optional. Test your upgrade on your local machine by running:

    ```sh
    astro dev restart
    ```

    All 4 running Docker containers for each of the Airflow components (webserver, scheduler, Postgres, triggerer) restart and begin running your new image.

    Open the Airflow UI at `localhost:8080` and go to **About** > **Version**. Confirm that you're running the correct Airflow version.

## Step 3: Deploy to Astronomer

1. To push your upgrade to a Deployment on Astronomer Software, run:

    ```sh
    astro deploy
    ```

2. In the Software UI, open your Deployment and click **Open Airflow**.
3. Go to **About** > **Version**. Confirm that you're running the correct version of Astro Runtime.
