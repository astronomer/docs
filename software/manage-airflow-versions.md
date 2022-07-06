---
title: "Upgrade Apache Airflow on Astronomer Software"
sidebar_label: "Upgrade Airflow"
id: manage-airflow-versions
description: Adjust and upgrade Airflow versions on Astronomer Software.
---

import {siteVariables} from '@site/src/versions';

Regularly upgrading your Software Deployments ensures that your Deployments continue to be supported and that your Airflow instance has the latest features and functionality.

To upgrade your Airflow Deployment to a later version of Airflow:

- Select a new Airflow version with the Software UI or CLI to initialize the upgrade.
- Change the FROM statement in your project's `Dockerfile` to reference an Astronomer Certified (AC) or Astro Runtime image that corresponds to your current Airflow version. See [Customize Your Image](customize-image.md).
- Deploy to Astronomer.

## Available Astronomer image versions

A cron job automatically pulls new Astronomer image versions from the Astronomer [update service](http://updates.astronomer.io/) and adds them to the Software UI and CLI within 24 hours of their publication. You don't have to upgrade Astronomer to upgrade Airflow.

If you don't want to wait for new Astronomer image versions, you can manually trigger the cron job with the following Kubernetes command:

> ```sh
> kubectl create job --namespace astronomer --from=cronjob/astronomer-houston-update-airflow-check airflow-update-check-first-run
> ```
>
If you get a message indicating that a job already exists, delete the job and rerun the command.


## Step 1. Initialize the upgrade process

An upgrade doesn't interrupt or otherwise impact your Airflow Deployment. It only signals to Astronomer your intent to upgrade.

The Software UI and CLI only provide Airflow versions that are later than the version currently running in your `Dockerfile`. For example, Airflow `1.10.7` is not available for an Airflow Deployment running `1.10.10`.

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
    You can expect the following output:

    ```
    astro deployment list
    NAME                                            DEPLOYMENT NAME                 DEPLOYMENT ID                 AIRFLOW VERSION
    new-deployment-1-10-10-airflow-k8s-2            elementary-rotation-5522        ckgwdq8cs037169xtbt2rtu15     1.10.12
    ```

3. Copy the `DEPLOYMENT ID` value and run the following command to list the available Airflow versions:

    ```
    astro deployment airflow upgrade --deployment-id=<deployment-id>
    ```

4. Enter the Airflow version you want to upgrade to and press `Enter`.

## Step 2: Deploy a new Astronomer image

### 1. Locate your Dockerfile in your project directory

Open the `Dockerfile` in your Astronomer directory. When you initialized an Astro project with the Astro CLI, the following files were automatically generated:

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

### 2. Choose your new Astronomer image

<!--- Version-specific -->

Update the `FROM` line of your project's `Dockerfile` to reference a new Astronomer image. For example, to upgrade to the latest version of Astro Runtime, you would change the `FROM` line to:

<pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}`}</code></pre>

For a list of current Astronomer images, see:

- [Astronomer Certified Lifecycle Schedule](ac-support-policy.md#astronomer-certified-lifecycle-schedule)
- [Astro Runtime Lifecycle Schedule](https://docs.astronomer.io/astro/runtime-version-lifecycle-policy#astro-runtime-lifecycle-schedule)

:::warning

After you upgrade your Airflow version, you can't revert to an earlier version.

:::

For Astronomer's full list of Docker images, see [Astronomer Certified on Quay.io](https://quay.io/repository/astronomer/ap-airflow?tab=tags) and [Astro Runtime on Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

### 3. Test your upgrade locally (_Optional_)

To test a new version of Astronomer Certified on your local machine, save all of your changes to your `Dockerfile` and run:

```sh
$ astro dev stop
```

All 4 running Docker containers for each of the Airflow components (webserver, scheduler, Postgres, triggerer) stop.

Run the following command to apply your changes:

```sh
$ astro dev start
```

### 4. Deploy to Astronomer

To push your upgrade to a Deployment on Astronomer Software, run:

```sh
astro deploy
```

:::caution

Due to a schema change in the Airflow metadata database, upgrading a Software Deployment to [AC 2.3.0](https://github.com/astronomer/ap-airflow/blob/master/2.3.0/CHANGELOG.md) can take significant time. Depending on the size of your metadata database, upgrades can take 10 minutes to an hour or longer depending on the number of task instances that have been recorded in the Airflow metadata database. During this time, scheduled tasks continue to execute but new tasks are not scheduled.

To minimize the upgrade time for a Deployment, contact [Astronomer support](https://support.astronomer.io). Minimizing your upgrade time requires removing records from your metadata database.

:::

### 5. Confirm your version in the Airflow UI

Open the Airflow UI and confirm that you're running the correct Airflow version.

#### Local development

1. Open a browser and go to http://localhost:8080/.

    Port 8080 is the default. To change this settiong, see [this forum post](https://forum.astronomer.io/t/i-already-have-the-ports-that-the-cli-is-trying-to-use-8080-5432-occupied-can-i-change-the-ports-when-starting-a-project/48).

2. Go to **About** > **Version**.

#### On Astronomer

In the Software UI, go to the Airflow Deployment page.

> **Note:** In Airflow versions 2.0 and later, the **Version** page is deprecated. Airflow version information is provided in footer of the Airflow UI.

## Cancel Airflow upgrade initialization

You can cancel an Airflow Deployment upgrade at any time if you haven't yet changed the Astronomer image in your `Dockerfile` and deployed it.

In the Software UI, select **Cancel** next to **Airflow Version**.

Using the Astro CLI, run:

```
astro deployment airflow upgrade --cancel --deployment-id=<deployment-id>
```

For example, if you cancel an initialized upgrade from Airflow 1.10.7 to Airflow 1.10.12 in the CLI, the following message appears:

```bash
astro deployment airflow upgrade --cancel --deployment-id=ckguogf6x0685ewxtebr4v04x

Airflow upgrade process has been successfully canceled. Your Deployment was not interrupted and you are still running Airflow 1.10.7.
```

Canceling the Airflow upgrade process does not interrupt or otherwise impact your Airflow Deployment or code that's running.

## Upgrade to a hotfix version of Astronomer Certified

To upgrade to the latest hotfix version of Astronomer Certified, replace the image referenced in your `Dockerfile` with a pinned version that specifies a particular hotfix. Astro Runtime does not support hotfix versions.

To upgrade to the latest Astronomer Certified 2.3.0 patch fix, for example, you would:

1. Check the AC [2.3.0 Changelog](https://github.com/astronomer/ap-airflow/blob/master/2.3.0/CHANGELOG.md).
2. Identify the latest patch (e.g. `2.3.0-5`).
3. Pin the image in your Dockerfile to that patch version. For example,  `FROM quay.io/astronomer/ap-airflow:2.3.0-5-onbuild` (Debian).

> **Note:** If you're pushing code to an Airflow Deployment using the Astro CLI and install a new Astronomer Certified image for the first time _without_ pinning a specific hotfix version, the latest available version is automatically pulled.
>
> If a hotfix release becomes available _after_ you've already built an Astronomer Certified image for the first time, subsequent code pushes do _not_ automatically pull the latest corresponding hotfix. Follow the hotfix upgrade process to pin your image to a particular version.
