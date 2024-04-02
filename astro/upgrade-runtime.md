---
sidebar_label: 'Upgrade Astro Runtime'
title: 'Upgrade Astro Runtime'
id: upgrade-runtime
description: "Learn how to upgrade the Astro Runtime version on your Deployments. To take advantage of new features and bug and security fixes, upgrade Astro Runtime when a new version becomes available."
---

import HostedBadge from '@site/src/components/HostedBadge';

New versions of Astro Runtime are released regularly to support new Astro and Apache Airflow functionality. To take advantage of new features and bug and security fixes, Astronomer recommends upgrading Astro Runtime as new versions are available.

## Prerequisites

- The [Astro CLI](cli/install-cli.md).
- An [Astro project](cli/get-started-cli.md).
- An [Astro Deployment](create-deployment.md).

:::info

If you're only upgrading a local Airflow environment, you don't need an Astro Deployment and you can skip steps 7-8.

:::

## Step 1: Review upgrade considerations

Astro upgrades can include breaking changes, especially when you're upgrading to a new major version. Check the [upgrade considerations](#upgrade-considerations) for your upgrade version to anticipate any breaking changes or upgrade-specific instructions before you proceed.

## Step 2: (Optional) Pin provider package versions

Major Astro Runtime upgrades can include major upgrades to built-in provider packages. These package upgrades can sometimes include breaking changes for your DAGs. See the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html) for a list of all available provider packages and their release notes.

For the most stable upgrade path, Astronomer recommends pinning all provider package versions from your current Runtime version before upgrading. To check the version of all provider packages installed in your Runtime version, run:

```sh
docker run --rm quay.io/astronomer/astro-runtime:<current-runtime-version> pip freeze | grep apache-airflow-providers
```

After reviewing this list, pin the version for each provider package in your Astro project `requirements.txt` file. For example, Runtime 7.4.1 uses version 4.0.0 of `apache-airflow-providers-databricks`. To pin this version of the Databricks provider package when you upgrade to a later version of Runtime, you add the following line to your `requirements.txt` file:

```text
apache-airflow-providers-databricks==4.0.0
```

## Step 3: (Optional) Run upgrade tests with the Astro CLI

You can use the Astro CLI to anticipate and address problems before upgrading to a newer version of Astro Runtime. Before you upgrade, run the following command to run tests against the version of Astro Runtime you're upgrading to:

```bash
astro dev upgrade-test --runtime-version <upgraded-runtime-version>
```

The Astro CLI then generates test results in your Astro project that identify dependency conflicts and import errors that you would experience using the new Astro Runtime version. Review these results and make the recommended changes to reduce the risk of your project generating errors after you upgrade. For more information about using this command and the test results, see [Test before upgrade your Astro project](cli/test-your-astro-project-locally.md#test-before-an-astro-runtime-upgrade).

## Step 4: Update Your Dockerfile

1. In your Astro project, open your `Dockerfile`.
2. Change the Docker image in the `FROM` statement of your `Dockerfile` to a new version of Astro Runtime.

    To upgrade to the latest version of Runtime, for example, change the `FROM` statement in your Dockerfile to:

    ```
    FROM quay.io/astronomer/astro-runtime:{{RUNTIME_VER}}
    ```

    You must always specify the major, minor, and patch version of any given Astro Runtime version.

3. Save the changes to your `Dockerfile`.

## Step 5: Test Astro Runtime locally

Astronomer recommends testing new versions of Astro Runtime locally before upgrading a Deployment on Astro.

1. Open your project directory in your terminal and run `astro dev restart`. This restarts the Docker containers for the Airflow webserver, scheduler, triggerer, and Postgres metadata database.
2. Access the Airflow UI of your local environment by navigating to `http://localhost:8080` in your browser.
3. Confirm that your local upgrade was successful by scrolling to the end of any page. The new Astro Runtime version is listed in the footer as well as the version of Airflow it is based on.

    ![Runtime Version banner - Local](/img/docs/image-tag-airflow-ui-local.png)

4. (Optional) Run DAGs locally to ensure that all of your code works as expected. If you encounter errors after your upgrade, it's possible that your new Astro Runtime version includes a breaking provider package change. If you encounter one of these breaking changes, follow the steps in [Upgrade or pin provider package versions](#optional-upgrade-or-pin-provider-package-versions) to check your provider package versions and, if required, pin the provider package version from your previous Runtime version in your `requirements.txt` file.

### Step 6: (Optional) Upgrade and test provider packages

If you pinned provider package versions before your upgrade, upgrade your provider packages by changing the pinned version in your `requirements.txt` file. Test east provider package upgrade locally before deploying to Astro.

## Step 7: Deploy to Astronomer

To push your upgraded project to an Astro Deployment, run:

```sh
astro deploy
```

For more information about deploying to Astro, see [Deploy code](deploy-code.md).

:::warning

After you upgrade a Deployment on Astro to a new version of Astro Runtime, the only way to downgrade is to [roll back to a previous deploy](deploy-history.md). If you attempt to downgrade a Deployment by updating your Dockerfile, the Astro CLI produces an error and your request to deploy does not succeed.

Generally speaking, Deployment rollbacks to lower Runtime versions are recommended only when your current code isn't working as expected. This is because rollbacks to lower Runtime versions can result in your Deployment losing data from the metadata database. For more information, see [What happens during a deploy rollback](deploy-history.md#what-happens-during-a-deploy-rollback).

:::

## Step 8: Confirm your upgrade on Astro

1. In the Astro UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click **Open Airflow**.
3. In the Airflow UI, scroll to the bottom of any page. You should see your new Runtime version in the footer:

    ![Runtime Version banner - Astro](/img/docs/image-tag-airflow-ui-astro.png)

    You will also see an **Image tag** for your deploy. This tag is shown only for Deployments on Astro and is not generated for changes in a local environment.

## Upgrade considerations

Consider the following when you upgrade Astro Runtime:

- All versions of the Astro CLI support all versions of Astro Runtime. There are no dependencies between the two products.
- Upgrading to certain versions of Runtime might result in extended upgrade times or otherwise disruptive changes to your environment. To learn more, see [Version-specific upgrade considerations](upgrade-runtime.md#version-upgrade-considerations).
- You can't downgrade a Deployment on Astro to a lower version of Astro Runtime unless you [roll back to a previous deploy](deploy-history.md).

To stay up to date on the latest versions of Astro Runtime, see [Astro Runtime release notes](runtime-release-notes.md). For more information on Astro Runtime versioning and support, see [Astro Runtime versioning and lifecycle policy](runtime-version-lifecycle-policy.mdx). For a full collection of Astro Runtime Docker images, go to the [Astro Runtime repository on Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

### Run a deprecated Astro Runtime version

<HostedBadge/>

If you're migrating to Astro from OSS Airflow or Astro Hybrid, where your Deployments run using an older version of Airflow or a deprecated version of the Astro Runtime, you can now use stepwise migration to complete your migration in stages. First, you can create Deployments with a deprecated version of the Astro Runtime using the Astro API to move to an Astro Hosted environment. Then, you can upgrade your code to the most up-to-date version of the Astro Runtime.

Deployments that run deprecated Astro Runtime versions will only receive support as [Astro Runtime maintenance policy](runtime-version-lifecycle-policy.mdx#astro-runtime-maintenance-policy), and Astronomer might advise you to upgrade your runtime to the latest version of Astro to resolve performance issues or bugs.

:::info

When you choose a deprecated version of Astro Runtime, Astronomer recommends always choosing the latest patch version that includes your desired Airflow version. Some earlier patch versions of Astro Runtime include unexpected behavior and can't be used even as a deprecated version. For more information about which versions are affected, see the [Version upgrade considerations](#version-upgrade-considerations).

:::

1. Contact your Astronomer account team and request the ability to run deprecated versions of Astro Runtime.
2. Create a [Personal Access Token](https://cloud.astronomer.io/token) to use for authentication to Astro.
    :::note

    You only need a PAT for the first Deployment in your Organization running a deprecated version of the Runtime.

    :::
3. Create a Deployment using the [Astro API](https://docs.astronomer.io/api/platform-api-reference/deployment/create-deployment). In your request, specify your deprecated Astro Runtime version using the `astroRuntimeVersions` property.

After you create the Deployment, you can manage the Deployment using any interface, including the Astro CLI and [Astro UI](deployment-settings.md). You can also create additional Deployments with deprecated Runtimes using a [Deployment API Token](deployment-api-tokens.md).

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

To continue using these packages with a compatible version of Python, upgrade to the [Astro Runtime Python distribution](runtime-image-architecture.mdx#python-version-distributions) for your desired Python version.

#### Runtime 8 (Airflow 2.6)

##### Breaking change to `apache-airflow-providers-cncf-kubernetes` in version 8.4.0

Astro Runtime 8.4.0 upgrades `apache-airflow-providers-cncf-kubernetes` to 7.0.0, which includes a breaking change by [removing some deprecated features from KubernetesHook](https://github.com/apache/airflow/commit/a1f5a5425e65c40e9baaf5eb4faeaed01cee3569). If you are using any of these features, either pin your current version of `apache-airflow-providers-cncf-kubernetes` to your `requirements.txt` file or ensure that you don't use any of the deprecated features before upgrading.

##### Upgrade directly to Astro Runtime 8.1

Astro Runtime 8.0 introduced a number of bugs and dependency conflicts which were subsequently fixed in Runtime 8.1. As a result, Astro Runtime 8.0 is not available in the Astro UI and no longer supported by Astronomer. To use Airflow 2.6, upgrade directly to Runtime 8.1.

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
