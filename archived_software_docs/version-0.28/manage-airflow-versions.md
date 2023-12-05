---
title: "Upgrade Apache Airflow on Astronomer Software"
sidebar_label: "Upgrade Airflow"
id: manage-airflow-versions
description: Adjust and upgrade Airflow versions on Astronomer Software.
---

## Overview

On Astronomer, the process of pushing up your code to an individual Airflow Deployment involves customizing a locally built Docker image —— with your DAG code, dependencies, plugins, and so on —— that's then bundled, tagged, and pushed to your Docker Registry.

Included in that build is your `Dockerfile`, a file that is automatically generated when you initialize an Airflow project on Astronomer via our CLI. Every successful build on Astronomer must include a `Dockerfile` that references an Astronomer Certified Docker Image. Astronomer Certified (AC) is a production-ready distribution of Apache Airflow that mirrors the open source project and undergoes additional levels of rigorous testing conducted by our team.

To upgrade your Airflow Deployment to a higher version of Airflow, there are three steps:

1. Initialize the upgrade by selecting a new Airflow version via the Software UI or CLI.
2. Change the FROM statement in your project's `Dockerfile` to reference an AC image that corresponds to the Airflow version indicated in Step 1.
3. Deploy to Astronomer.

This guide provides more specific instructions for each of these steps. For information on Astronomer Certified versioning and support schedules, read [Astronomer Certified Versioning and Support Policy](ac-support-policy.md).

> **Note:** For more thorough guidelines on customizing your image, reference our ["Customize Your Image" doc](customize-image.md).

## Available Astronomer Certified Versions

Starting with Astronomer Software v0.23, new versions of Astronomer Certified are automatically pulled into the Software UI and CLI within 24 hours of their publication via a cron job that pulls from Astronomer's [update service](http://updates.astronomer.io/astronomer-certified). In other words, you don't have to upgrade Astronomer in order to upgrade Airflow.

> **Note:** If you don't want to wait for new versions of Astronomer Certified to appear on their own, you can manually trigger the cron job with the following Kubernetes command:
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

![Airflow Upgrade via Software UI](/img/software/airflow-upgrade-astro-ui.gif)

This action will NOT interrupt or otherwise impact your Airflow Deployment or trigger a code change - it is simply a signal to our platform that you _intend_ to upgrade such that we can guide your experience through the rest of the process.

Once you select a version, you can expect to see a banner next to **Airflow Version** indicating that the upgrade is in progress. For a user upgrading from 1.10.7 to 1.10.12, that banner would read `Upgrade from 1.10.7 to 1.10.12 in progress…`

> **Note:** If you'd like to change the version of Airflow you'd like to upgrade to, you can do so at anytime by clicking **Cancel**, re-selecting a new version and once again clicking **Upgrade**. More on that below.

### with the Astro CLI

To use the Astro CLI to initialize the Airflow upgrade process, run `$ astro login <base-domain>` first to make sure you're authenticated .

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

## Step 2: Deploy a New Astronomer Certified Image

### 1. Locate your Dockerfile in your Project Directory

First, open the `Dockerfile` within your Astronomer directory. When you used the Astro CLI to initialize an Airflow project, the following files should have been automatically generated:

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

Depending on the OS distribution and version of Airflow you want to run, you'll want to reference the corresponding Astronomer Certified image in the FROM statement of your `Dockerfile`.

### 2. Choose your new Astronomer Certified Image

<!--- Version-specific -->

Depending on the Airflow version you'd like to run or upgrade to, copy one of the images in the following table to your `Dockerfile` and proceed to Step 3.

Once you upgrade Airflow versions, you CANNOT downgrade to an earlier version. The Airflow metadata database structurally changes with each release, making for backwards incompatibility across versions.

For our platform's full collection of Docker Images, reference [Astronomer on Quay.io](https://quay.io/repository/astronomer/ap-airflow?tab=tags).

| Airflow Version                                                                      | Debian-based Image                                        |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| [1.10.15](https://github.com/astronomer/ap-airflow/blob/master/1.10.15/CHANGELOG.md) | FROM quay.io/astronomer/ap-airflow:1.10.15-buster-onbuild |
| [2.1.0](https://github.com/astronomer/ap-airflow/blob/master/2.1.0/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.1.0-buster-onbuild   |
| [2.1.1](https://github.com/astronomer/ap-airflow/blob/master/2.1.1/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.1.1-buster-onbuild   |
| [2.1.3](https://github.com/astronomer/ap-airflow/blob/master/2.1.3/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.1.3-buster-onbuild   |
| [2.1.4](https://github.com/astronomer/ap-airflow/blob/master/2.1.4/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.1.4-buster-onbuild   |
| [2.2.0](https://github.com/astronomer/ap-airflow/blob/master/2.2.0/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.2.0-buster-onbuild   |
| [2.2.1](https://github.com/astronomer/ap-airflow/blob/master/2.2.1/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.2.1-onbuild          |
| [2.2.2](https://github.com/astronomer/ap-airflow/blob/master/2.2.2/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.2.2-onbuild          |
| [2.2.4](https://github.com/astronomer/ap-airflow/blob/master/2.2.4/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.2.4-onbuild          |
| [2.2.5](https://github.com/astronomer/ap-airflow/blob/master/2.2.5/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.2.5-onbuild          |
| [2.3.0](https://github.com/astronomer/ap-airflow/blob/master/2.3.0/CHANGELOG.md)     | FROM quay.io/astronomer/ap-airflow:2.3.0-onbuild          |

> **Note:** In November of 2020, Astronomer migrated its Docker Registry from [Docker Hub](https://hub.docker.com/r/astronomerinc/ap-airflow) to [Quay.io](https://quay.io/repository/astronomer/ap-airflow?tab=tags) due to a [change](https://www.docker.com/blog/what-you-need-to-know-about-upcoming-docker-hub-rate-limiting/) in Docker Hub's rate limit policy. If you're using a legacy `astronomerinc/ap-airflow` image, replace it with a corresponding `quay.io/astronomer/ap-airflow` image to avoid rate limiting errors from DockerHub when you deploy to Astronomer (e.g. `toomanyrequests: You have reached your pull rate limit`).

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

:::warning

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

> **Note:** In Airflow 2.0, the **Version** page referenced above will be deprecated. Check the footer of the Airflow UI to validate Airflow version instead.

## Cancel Airflow Upgrade Initialization

If you begin the upgrade process for your Airflow Deployment and would like to cancel it, you can do so at any time either via the Software UI or CLI as long as you have NOT changed the Astronomer Certified Image in your `Dockerfile` and deployed it.

Via the Software UI, select **Cancel** next to **Airflow Version**.

![Cancel Airflow Upgrade via Software UI](/img/software/airflow-upgrade-astro-ui-cancel.gif)

Via the Astro CLI, run:

```
astro deployment airflow upgrade --cancel --deployment-id=<deployment-id>
```

For example, if a user cancels an initialized upgrade from Airflow 1.10.7 to Airflow 1.10.12 via the CLI, they would see the following:

```bash
astro deployment airflow upgrade --cancel --deployment-id=ckguogf6x0685ewxtebr4v04x

Airflow upgrade process has been successfully canceled. Your Deployment was not interrupted and you are still running Airflow 1.10.7.
```

Canceling the Airflow upgrade process will NOT interrupt or otherwise impact your Airflow Deployment or code that's running with it. To re-initialize an upgrade, follow the steps above.

## Upgrade to an AC Hotfix Version

To upgrade to the latest hotfix version of Astronomer Certified, replace the image referenced in your `Dockerfile` with a pinned version that specifies a particular hotfix.

If you're looking for the latest Astronomer Certified 1.10.10, for example, you would:

1. Check the AC [1.10.10 Changelog](https://github.com/astronomer/ap-airflow/blob/master/1.10.10/CHANGELOG.md).
2. Identify the latest patch (e.g. `1.10.10-5`).
3. Pin the Astronomer Certified image in your Dockerfile to that patch version.

In this case, that would be: `FROM quay.io/astronomer/ap-airflow:1.10.10-5-buster-onbuild` (Debian).

> **Note:** If you're pushing code to an Airflow Deployment via the Astro CLI and install a new Astronomer Certified image for the first time _without_ pinning a specific patch, the latest version available will automatically be pulled.
>
> If a patch release becomes available _after_ you've already built an Astronomer Certified image for the first time, subsequent code pushes will _not_ automatically pull the latest corresponding patch. You must follow the process above to pin your image to a particular version.
