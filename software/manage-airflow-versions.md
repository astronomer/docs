---
title: "Upgrade Apache Airflow on Astronomer Software"
sidebar_label: "Upgrade Airflow"
id: manage-airflow-versions
description: Adjust and upgrade Airflow versions on Astronomer Software.
---

import {siteVariables} from '@site/src/versions';

## Overview

On Astronomer, the process of pushing up your code to an individual Airflow Deployment involves customizing a locally built Docker image —— with your DAG code, dependencies, plugins, and so on —— that's then bundled, tagged, and pushed to your Docker Registry.

Included in that build is your `Dockerfile`, a file that is automatically generated when you initialize an Astro project on Astronomer with the Astro CLI. Every successful build on Astronomer must include a `Dockerfile` that references an Astronomer Certified or Astro Runtime Docker image. Astronomer Certified (AC) and Astro Runtime are production-ready distributions of Apache Airflow that mirror the open source project and undergo additional levels of testing and development. Astro Runtime provides an additional layer of differentiation and was introduced to Astronomer Software in v0.29.

To upgrade your Airflow Deployment to a higher version of Airflow, there are three steps:

1. Initialize the upgrade by selecting a new Airflow version via the Software UI or CLI.
2. Change the FROM statement in your project's `Dockerfile` to reference an AC image that corresponds to the Airflow version indicated in Step 1.
3. Deploy to Astronomer.

> **Note:** For more thorough guidelines on customizing your image, see [Customize Your Image](customize-image.md).

## Available Astronomer Image Versions

New versions of Astronomer images are automatically pulled into the Software UI and CLI within 24 hours of their publication via a cron job that pulls from Astronomer's [update service](http://updates.astronomer.io/). In other words, you don't have to upgrade Astronomer in order to upgrade Airflow.

> **Note:** If you don't want to wait for new versions of Astronomer images to appear on their own, you can manually trigger the cron job with the following Kubernetes command:
>
> ```sh
> kubectl create job --namespace astronomer --from=cronjob/astronomer-houston-update-airflow-check airflow-update-check-first-run
> ```
>
> If you get a message indicating that a job already exists, delete the job and rerun the command.

## Step 1. Initialize the Upgrade Process

The first step to upgrading your Deployment to a higher version of Apache Airflow is to indicate your intent to do so via the Software UI or CLI.

> **Note:** The Software UI and CLI will only make available versions of Airflow that are _higher_ than the version you're currently running in your `Dockerfile`. For example, Airflow `1.10.7` would not be available for an Airflow Deployment running `1.10.10`.

### via the Software UI

To initialize the Airflow upgrade process via the Software UI, navigate to **Deployment** > **Settings** > **Basics** > **Airflow Version**. Next to **Airflow Version**,

1. Select your desired version of Airflow
2. Click **Upgrade**

![Airflow Upgrade via Software UI](https://assets2.astronomer.io/main/docs/manage-airflow-versions/airflow-upgrade-astro-ui.gif)

This action will NOT interrupt or otherwise impact your Airflow Deployment or trigger a code change - it is simply a signal to our platform that you _intend_ to upgrade such that we can guide your experience through the rest of the process.

Once you select a version, you can expect to see a banner next to **Airflow Version** indicating that the upgrade is in progress. For a user upgrading from 1.10.7 to 1.10.12, that banner would read `Upgrade from 1.10.7 to 1.10.12 initiated…`

> **Note:** If you'd like to change the version of Airflow you'd like to upgrade to, you can do so at anytime by clicking **Cancel**, re-selecting a new version and once again clicking **Upgrade**. More on that below.

### with the Astro CLI

To use the Astro CLI to initialize the Airflow upgrade process, run `$ astro auth login <base-domain>` first to make sure you're authenticated .

Once authenticated, grab the `Deployment ID` of the Airflow Deployment you'd like to upgrade by running:

```
astro deployment list
```

You can expect the following output:

```
astro deployment list
 NAME                                            DEPLOYMENT NAME                 DEPLOYMENT ID                 AIRFLOW VERSION
 new-deployment-1-10-10-airflow-k8s-2            elementary-rotation-5522        ckgwdq8cs037169xtbt2rtu15     1.10.12
```

With that `Deployment ID`, run:

```
astro deployment airflow upgrade --deployment-id=<deployment-id>
```

This command will output a list of available versions of Airflow you can choose from and prompt you to pick one. For example, a user upgrading from Airflow 1.10.5 to Airflow 1.10.12 should see the following:

```
astro deployment airflow upgrade --deployment-id=ckguogf6x0685ewxtebr4v04x
#     AIRFLOW VERSION
1     1.10.7
2     1.10.10
3     1.10.12

> 3
 NAME                  DEPLOYMENT NAME       ASTRO       DEPLOYMENT ID                 AIRFLOW VERSION
 Astronomer Stagings   new-velocity-8501     v0.17.0     ckguogf6x0685ewxtebr4v04x     1.10.12

The upgrade from Airflow 1.10.5 to 1.10.12 has been started. To complete this process, add an Airflow 1.10.12 image to your Dockerfile and deploy to Astronomer.
```

As noted above, this action will NOT interrupt or otherwise impact your Airflow Deployment or trigger a code change - it is simply a signal to our platform that you _intend_ to upgrade such that we can guide your experience through the rest of the process.

To complete the upgrade, all you have to do is add a corresponding AC image to your `Dockerfile`.

## Step 2: Deploy a New Astronomer Image

### 1. Locate your Dockerfile in your Project Directory

First, open the `Dockerfile` within your Astronomer directory. When you initialized an Airflow project via the Astro CLI, the following files should have been automatically generated:

```
.
├── dags # Where your DAGs go
│   └── example-dag.py # An example DAG that comes with the initialized project
├── Dockerfile # For Astronomer's Docker image and runtime overrides
├── include # For any other files you'd like to include
├── packages.txt # For OS-level packages
├── plugins # For any custom or community Airflow plugins
└── requirements.txt # For any Python packages
```

Depending on the OS distribution and version of Airflow you want to run, you'll want to reference the corresponding Astronomer image in the FROM statement of your `Dockerfile`.

### 2. Choose your new Astronomer Image

<!--- Version-specific -->

Depending on the Airflow version you'd like to upgrade to, update the `FROM` line of your project's `Dockerfile` to reference a new Astronomer image. For example, to upgrade to the latest version of Astro Runtime, you would change the `FROM` line to:

<pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}`}</code></pre>

For a list of currently maintained Astronomer images, see:

- [Astronomer Certified Lifecycle Schedule](ac-support-policy.md#astronomer-certified-lifecycle-schedule)
- [Astro Runtime Lifecycle Schedule](https://docs.astronomer.io/astro/runtime-version-lifecycle-policy#astro-runtime-lifecycle-schedule)

:::warning

Once you upgrade Airflow versions, you cannot downgrade to an earlier version. The Airflow metadata database structurally changes with each release, making for backwards incompatibility across versions.

:::

For Astronomer's full collection of Docker images, see [Astronomer Certified on Quay.io](https://quay.io/repository/astronomer/ap-airflow?tab=tags) and [Astro Runtime on Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

### 3. Test Your Upgrade Locally (_Optional_)

To test a new version of Astronomer Certified on your local machine, save all changes to your `Dockerfile` and run:

```sh
$ astro dev stop
```

This will stop all 3 running Docker containers for each of the necessary Airflow components (Webserver, Scheduler, Postgres). Then, apply your changes locally by running:

```sh
$ astro dev start
```

### 4. Deploy to Astronomer

To push your upgrade to a Deployment on Astronomer Software, run:

```sh
astro deploy
```

:::caution

Due to a schema change in the Airflow metadata database, upgrading a Software Deployment to [AC 2.3.0](https://github.com/astronomer/ap-airflow/blob/master/2.3.0/CHANGELOG.md) can take significantly longer than usual. Depending on the size of your metadata database, upgrades can take anywhere from 10 minutes to an hour or longer depending on the number of task instances that have been recorded in the Airflow metadata database. During this time, scheduled tasks will continue to execute but new tasks will not be scheduled.

If you need to minimize the upgrade time for a given Deployment, reach out to [Astronomer Support](https://support.astronomer.io). Note that minimizing your upgrade time requires removing records from your metadata database.

:::

### 5. Confirm your version in the Airflow UI

Once you've issued that command, navigate to your Airflow UI to confirm that you're now running the correct Airflow version.

#### Local Development

If you're developing locally, you can:

1. Head to http://localhost:8080/
2. Navigate to `About` > `Version`

Once there, you should see your correct Airflow version listed.

> **Note:** The URL listed above assumes your Webserver is at Port 8080 (default). To change that default, read [this forum post](https://forum.astronomer.io/t/i-already-have-the-ports-that-the-cli-is-trying-to-use-8080-5432-occupied-can-i-change-the-ports-when-starting-a-project/48).

#### On Astronomer

If you're on Astronomer Software, navigate to your Airflow Deployment page on the Software UI.

> **Note:** In Airflow 2.0, the **Version** page referenced above will be deprecated. Check the footer of the Airflow UI to validate your Airflow version instead.

## Cancel Airflow Upgrade Initialization

If you begin the upgrade process for your Airflow Deployment and would like to cancel it, you can do so at any time either via the Software UI or CLI as long as you have NOT changed the Astronomer image in your `Dockerfile` and deployed it.

In the Software UI, select **Cancel** next to **Airflow Version**.

![Cancel Airflow Upgrade via Software UI](https://assets2.astronomer.io/main/docs/manage-airflow-versions/airflow-upgrade-astro-ui-cancel.gif)

Using the Astro CLI, run:

```
astro deployment airflow upgrade --cancel --deployment-id=<deployment-id>
```

For example, if a user cancels an initialized upgrade from Airflow 1.10.7 to Airflow 1.10.12 via the CLI, they would see the following:

```bash
astro deployment airflow upgrade --cancel --deployment-id=ckguogf6x0685ewxtebr4v04x

Airflow upgrade process has been successfully canceled. Your Deployment was not interrupted and you are still running Airflow 1.10.7.
```

Canceling the Airflow upgrade process will NOT interrupt or otherwise impact your Airflow Deployment or code that's running with it. To re-initialize an upgrade, follow the steps above.

## Upgrade to a Hotfix Version of Astronomer Certified

To upgrade to the latest hotfix version of Astronomer Certified, replace the image referenced in your `Dockerfile` with a pinned version that specifies a particular hotfix. This is applicable only for Astronomer Certified, as Astro Runtime does not support hotfix versions.

To upgrade to the latest Astronomer Certified 2.3.0 patch fix, for example, you would:

1. Check the AC [2.3.0 Changelog](https://github.com/astronomer/ap-airflow/blob/master/2.3.0/CHANGELOG.md).
2. Identify the latest patch (e.g. `2.3.0-5`).
3. Pin the image in your Dockerfile to that patch version.

In this case, that would be: `FROM quay.io/astronomer/ap-airflow:2.3.0-5-onbuild` (Debian).

> **Note:** If you're pushing code to an Airflow Deployment via the Astro CLI and install a new Astronomer Certified image for the first time _without_ pinning a specific hotfix version, the latest version available will automatically be pulled.
>
> If a hotfix release becomes available _after_ you've already built an Astronomer Certified image for the first time, subsequent code pushes will _not_ automatically pull the latest corresponding hotfix. You must follow the process above to pin your image to a particular version.
