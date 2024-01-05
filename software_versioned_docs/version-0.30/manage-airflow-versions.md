---
title: "Upgrade Airflow on Astronomer Software"
sidebar_label: "Upgrade Airflow"
id: manage-airflow-versions
description: Adjust and upgrade Airflow versions on Astronomer Software.
---

import {siteVariables} from '@site/src/versions';

## Overview

Regularly upgrading your Software Deployments ensures that your Deployments continue to be supported and that your Airflow instance has the latest features and functionality.

To upgrade your Airflow Deployment to a later version of Airflow:

- Select a new Airflow version with the Software UI or CLI to start the upgrade.
- Change the FROM statement in your project's `Dockerfile` to reference an Astro Runtime image that corresponds to your current Airflow version. See [Customize Your Image](customize-image.md).
- Deploy to Astronomer.

## Available Astronomer image versions

A cron job automatically pulls new Astronomer image versions from the Astronomer [update service](http://updates.astronomer.io/) and adds them to the Software UI and CLI within 24 hours of their publication. You don't have to upgrade Astronomer to upgrade Airflow.

If you don't want to wait for new Astronomer image versions, you can manually trigger the cron job with the following Kubernetes command:

> ```sh
> kubectl create job --namespace astronomer --from=cronjob/astronomer-houston-update-airflow-check airflow-update-check-first-run
> ```
>
If you get a message indicating that a job already exists, delete the job and rerun the command.


## Step 1. Start the upgrade process

Starting the upgrade process doesn't interrupt or otherwise impact your Airflow Deployment. It only signals to Astronomer your intent to upgrade at a later time.

The Software UI and CLI only provide Airflow versions that are later than the version currently running in your `Dockerfile`. For example, Airflow `2.1.0` is not available for an Airflow Deployment running `2.2.0`.

### With the Software UI

1. Go to **Deployment** > **Settings** > **Basics** > **Airflow Version**.
2. Select an Airflow version.
3. Click **Upgrade**.

### With the Astro CLI

1. Run `$ astro auth login <base-domain>` to confirm you're authenticated.

2. Run the following command to view your Airflow Deployment `Deployment ID`:

    ```
    astro deployment list
    ```

3. Copy the `DEPLOYMENT ID` value and run the following command to list the available Airflow versions:

    ```
    astro deployment airflow upgrade --deployment-id=<deployment-id>
    ```

4. Enter the Airflow version you want to upgrade to and press `Enter`.

## Step 2: Update your Astro project

1. In your Astro project, open your `Dockerfile`.
2. Update the `FROM` line of your project's `Dockerfile` to reference a new Astronomer image. For example, to upgrade to the latest version of Astro Runtime, you would change the `FROM` line to:

    <pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}`}</code></pre>

    For a list of currently supported versions of Astro Runtime, see [Astro Runtime lifecycle schedule](/astro/runtime-version-lifecycle-policy#astro-runtime-lifecycle-schedule).

  :::danger

  After you upgrade your Airflow version, you can't revert to an earlier version.

  :::

1. Optional. Test your upgrade on your local machine by running:

    ```sh
    astro dev restart
    ```

    All 4 Airflow Docker containers restart and begin running your new image.

    To confirm that your migration was successful, open the Airflow UI at `localhost:8080` and scroll to the bottom of any page. You should see your new Runtime version in the footer.

## Step 3: Deploy to Astronomer

1. To push your upgrade to a Deployment on Astronomer Software, run:

    ```sh
    astro deploy
    ```

  :::warning

  Due to a schema change in the Airflow metadata database, upgrading a Software Deployment to [AC 2.3.0](https://github.com/astronomer/ap-airflow/blob/master/2.3.0/CHANGELOG.md) can take significant time. Depending on the size of your metadata database, upgrades can take 10 minutes to an hour or longer depending on the number of task instances that have been recorded in the Airflow metadata database. During this time, scheduled tasks continue to execute but new tasks are not scheduled.

  To minimize the upgrade time for a Deployment, contact [Astronomer support](https://support.astronomer.io). Minimizing your upgrade time requires removing records from your metadata database.

  :::

2. In the Software UI, open your Deployment and click **Open Airflow**.
3. In the Airflow UI, scroll to the bottom of any page. You should see your new Runtime version in the footer.


## Cancel Airflow upgrade

You can cancel an Airflow Deployment upgrade at any time if you haven't yet changed the Astronomer image in your `Dockerfile` and deployed it.

In the Software UI, select **Cancel** next to **Airflow Version**.

Using the Astro CLI, run:

```
astro deployment airflow upgrade --cancel --deployment-id=<deployment-id>
```

For example, if you cancel an upgrade from Airflow 2.1.0 to Airflow 2.2.0 in the CLI, the following message appears:

```bash
astro deployment airflow upgrade --cancel --deployment-id=ckguogf6x0685ewxtebr4v04x

Airflow upgrade process has been successfully canceled. Your Deployment was not interrupted and you are still running Airflow 2.1.0.
```

Canceling the Airflow upgrade process does not interrupt or otherwise impact your Airflow Deployment or code that's running.
