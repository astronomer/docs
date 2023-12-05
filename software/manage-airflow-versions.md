---
title: "Upgrade Airflow/ Astro Runtime on Astronomer Software"
sidebar_label: "Upgrade Airflow/ Astro Runtime"
id: manage-airflow-versions
description: Adjust and upgrade Airflow versions on Astronomer Software.
---

import {siteVariables} from '@site/src/versions';

## Overview

Regularly upgrading your Software Deployments ensures that your Deployments continue to be supported and that your Airflow instance has the latest features and functionality.

To upgrade your Airflow Deployment to a later version of Airflow:

- Select a new Airflow version with the Software UI or CLI to start the upgrade.
- Change the FROM statement in your project's `Dockerfile` to reference an Astronomer Certified (AC) or Astro Runtime image that corresponds to your current Airflow version. See [Customize Your Image](customize-image.md).
- Deploy to Astronomer.

## Available Astronomer image versions

A cron job automatically pulls new Astronomer image versions from the Astronomer [update service](http://updates.astronomer.io/) and adds them to the Software UI and CLI within 24 hours of their publication. You don't have to upgrade Astronomer to upgrade Airflow.

If you don't want to wait for new Astronomer image versions, you can manually trigger the cron job with the following Kubernetes command:

```sh
kubectl create job --namespace astronomer --from=cronjob/astronomer-houston-update-airflow-check airflow-update-check-first-run
```

If you get a message indicating that a job already exists, delete the job and rerun the command.

## Step 1: Review upgrade considerations

Astro upgrades can include breaking changes, especially when you're upgrading to a new major version. Check the [upgrade considerations](#upgrade-considerations) for your upgrade version to anticipate any breaking changes or upgrade-specific instructions before you proceed.

## Step 2: Start the upgrade process

Starting the upgrade process doesn't interrupt or otherwise impact your Airflow Deployment. It only signals to Astronomer Software that you intend to upgrade at a later time.

### With the Software UI

1. Go to **Deployment** > **Settings** > **Basics** > **Airflow Version**.
2. Select an Airflow version.
3. Click **Upgrade**.

### With the Astro CLI

1. Run `astro auth login <base-domain>` to confirm you're authenticated.

2. Run the following command to list your current Deployments. 
   
    ```zsh
    astro deployment list
    ```

    Copy the ID of the Deployment you want to upgrade.

3. Run the following command to list the available Airflow versions:

    ```zsh
    astro deployment airflow upgrade --deployment-id=<deployment-id>
    ```

4. Enter the Airflow version you want to upgrade to and press `Enter`.

## Step 3: (Optional) Pin provider package versions

Major Astro Runtime upgrades can include major upgrades to built-in provider packages. These package upgrades can sometimes include breaking changes for your DAGs. See the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html) for a list of all available provider packages and their release notes. 

For the most stable upgrade path, Astronomer recommends pinning all provider package versions from your current Runtime version before upgrading. To check the version of all provider packages installed in your Runtime version, run:

```sh
docker run --rm quay.io/astronomer/astro-runtime:<current-runtime-version> pip freeze | grep apache-airflow-providers
```

After reviewing this list, pin the version for each provider package in your Astro project `requirements.txt` file. For example, Runtime 7.4.1 uses version 4.0.0 of `apache-airflow-providers-databricks`. To pin this version of the Databricks provider package when you upgrade to a later version of Runtime, you add the following line to your `requirements.txt` file:

```text
apache-airflow-providers-databricks==4.0.0
```

## Step 4: (Optional) Run upgrade tests with the Astro CLI

You can use the Astro CLI to anticipate and address problems before upgrading to a newer version of Astro Runtime. Before you upgrade, run the following command to run tests against the version of Astro Runtime you're upgrading to:

```bash 
astro dev upgrade-test --runtime-version <upgraded-runtime-version>
```

The Astro CLI then generates test results in your Astro project that identify dependency conflicts and import errors that you would experience using the new Astro Runtime version. Review these results and make the recommended changes to reduce the risk of your project generating errors after you upgrade. For more information about using this command and the test results, see [Test before upgrade your Astro project](https://docs.astronomer.io/astro/cli/test-your-astro-project-locally#test-before-an-astro-runtime-upgrade).

## Step 5: Update your Astro project

1. In your Astro project, open your `Dockerfile`.
2. Change the Docker image in the `FROM` statement of your `Dockerfile` to a new version of Astro Runtime. For example, to upgrade to the latest version of Runtime, you would change the `FROM` statement in your Dockerfile to:

    <pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}`}</code></pre>

    For a list of supported Astro Runtime versions, see [Astro Runtime maintenance and lifecycle policy](https://docs.astronomer.io/astro/runtime-version-lifecycle-policy#astro-runtime-lifecycle-schedule).

  :::warning

  After you upgrade your Airflow version, you can't revert to an earlier version.

  :::

3. (Optional) Test your upgrade on your local machine by running:

    ```sh
    astro dev restart
    ```

    All 4 Airflow Docker containers restart and begin running your new image.

    To confirm that your migration was successful, open the Airflow UI at `localhost:8080` and scroll to the bottom of any page. You should see your new Runtime version in the footer.

## Step 6: Deploy to Astronomer

1. Run the following command to push your upgraded Astro project to your Deployment:

    ```sh
    astro deploy
    ```

2. In the Software UI, open your Deployment and click **Open Airflow**.
3. In the Airflow UI, scroll to the bottom of any page. You should see your new Runtime version in the footer.

## Cancel Airflow upgrade

As a System Admin, you can cancel an Airflow Deployment upgrade at any time if you haven't yet changed the Astronomer image in your `Dockerfile` and deployed it.

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

:::info

If you can't cancel your upgrade and receive an error message about using an unsupported Airflow version, set the following value in your `config.yaml` file and [apply the change](apply-platform-config.md) to successfully cancel your upgrade. This configuration allows you to roll back to your current version of Airflow, even if it's not supported. 

```yaml
astronomer:
  houston:
    config:
      deployments:
        enableSystemAdminCanCreateDeprecatedAirflows: true
```

:::


## Upgrade considerations

Consider the following when you upgrade Astro Runtime:

- Astronomer does not support downgrading a Deployment on Astronomer Software to a lower version of Astro Runtime.
- All versions of the Astro CLI support all versions of Astro Runtime. There are no dependencies between the two products.
- Upgrading to certain versions of Runtime might result in extended upgrade times or otherwise disruptive changes to your environment. To learn more, see [Version-specific upgrade considerations](upgrade-runtime.md#version-upgrade-considerations).

To stay up to date on the latest versions of Astro Runtime, see [Astro Runtime release notes](runtime-release-notes.md). For more information on Astro Runtime versioning and support, see [Astro Runtime versioning and lifecycle policy](runtime-version-lifecycle-policy.md). For a full collection of Astro Runtime Docker images, go to the [Astro Runtime repository on Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

### Version upgrade considerations

This is where you'll find the upgrade considerations for specific Astro Runtime versions. This includes breaking changes, database migrations, and other considerations.

:::info

If an Astro Runtime version isn't included in this section, then there are no specific upgrade considerations for that version.

:::

#### Runtime 9 (Airflow 2.7)

##### Connection testing in the Airflow UI disabled by default

In Airflow 2.7, connection testing in the Airflow UI is disabled by default. Astronomer does not recommend reenabling the feature unless you fully trust all users with edit/ delete permissions for Airflow connections.

To reenable the feature, set the following environment variable in your Astro project Dockerfile:

```dockerfile
ENV AIRFLOW__CORE__TEST_CONNECTION=Enabled
```

##### Upgrade to Python 3.11

The base distribution of Astro Runtime 9 uses Python 3.11 by default. Some provider packages, such as `apache-airflow-providers-apache-hive`, aren't compatible with Python 3.11.

To continue using these packages with a compatible version of Python, upgrade to the [Astro Runtime Python distribution](runtime-image-architecture.md#python-version-distributions) for your desired Python version.

#### Runtime 8 (Airflow 2.6)

##### Breaking change to `apache-airflow-providers-cncf-kubernetes` in version 8.4.0

Astro Runtime 8.4.0 upgrades `apache-airflow-providers-cncf-kubernetes` to 7.0.0, which includes a breaking change by [removing some deprecated features from KubernetesHook](https://github.com/apache/airflow/commit/a1f5a5425e65c40e9baaf5eb4faeaed01cee3569). If you are using any of these features, either pin your current version of `apache-airflow-providers-cncf-kubernetes` to your `requirements.txt` file or ensure that you don't use any of the deprecated features before upgrading.

##### Package dependency conflicts

Astro Runtime 8 includes fewer default dependencies than previous versions. Specifically, the following provider packages are no longer installed by default:

- `apache-airflow-providers-apache-hive`
- `apache-airflow-providers-apache-livy`
- `apache-airflow-providers-databricks`
- `apache-airflow-providers-dbt-cloud`
- `apache-airflow-providers-microsoft-mssql`
- `apache-airflow-providers-sftp`
- `apache-airflow-providers-snowflake`

If your DAGs depend on any of these provider packages, add the provider packages to your Astro project `requirements.txt` file before upgrading. You can also [pin specific provider package versions](#optional-pin-provider-package-versions) to ensure that none of your provider packages change after upgrading.

##### Upgrade to Python 3.10

Astro Runtime 8 uses Python 3.10. If you use provider packages that don't yet support Python 3.10, use one of the following options to stay on Python 3.9:

- Run your tasks using the KubernetesPodOperator or PythonVirtualenvOperator. You can configure the environment that these tasks run in to use Python 3.9.
- Use the [`astronomer-provider-venv`](https://github.com/astronomer/astro-provider-venv) to configure a custom virtual environment that you can apply to individual tasks.

##### Provider incompatibilities

There is an incompatibility between Astro Runtime 8 and the following provider packages installed together:

- `apache-airflow-providers-cncf-kubernetes==6.1.0`
- `apache-airflow-providers-google==10.0.0`

That can be resolved by pinning `apache-airflow-providers-google==10.9.0` or greater in your `requirements.txt` file.

This incompatibility results in breaking the GKEStartPodOperator. This operator inherits from the KubernetesPodOperator, but then overrides the hook attribute with the GKEPodHook. In the included version of the `cncf-kubernetes` providers package, the KubernetesPodOperator uses a new method, `get_xcom_sidecar_container_resources`. This method is present in the KubernetesHook, but not the GKEPodHook. Therefore, when it is called it causes the task execution to break. 

#### Runtime 6 (Airflow 2.4)

Smart Sensors were deprecated in Airflow 2.2.4 and removed in Airflow 2.4.0. If your organization is still using Smart Sensors, you'll need to start using deferrable operators. See [Deferrable operators](https://docs.astronomer.io/learn/deferrable-operators).

#### Runtime 5 (Airflow 2.3)

Astro Runtime 5.0.0, based on Airflow 2.3, includes changes to the schema of the Airflow metadata database. When you first upgrade to Runtime 5.0.0, consider the following:

- Upgrading to Runtime 5.0.0 can take 10 to 30 minutes or more depending on the number of task instances that have been recorded in the metadata database throughout the lifetime of your Deployment on Astro.
- Once you upgrade successfully to Runtime 5, you might see errors in the Airflow UI that warn you of incompatible data in certain tables of the database. For example:

    ```txt
    Airflow found incompatible data in the `dangling_rendered_task_instance_fields` table in your metadata database, and moved...
    ```

    These warnings have no impact on your tasks or DAGs and can be ignored. If you want to remove these warning messages from the Airflow UI, reach out to [Astronomer support](https://cloud.astronomer.io/open-support-request). If requested, Astronomer can drop incompatible tables from your metadata database.

For more information on Airflow 2.3, see ["Apache Airflow 2.3.0 is here"](https://airflow.apache.org/blog/airflow-2.3.0/) or the [Airflow 2.3.0 changelog](https://airflow.apache.org/docs/apache-airflow/2.3.0/release_notes.html#airflow-2-3-0-2022-04-30).
