---
sidebar_label: 'Upgrade Astro Runtime'
title: 'Upgrade Astro Runtime'
id: upgrade-runtime
---

<head>
  <meta name="description" content="Learn how to upgrade the Astro Runtime version on your Deployments. To take advantage of new features and bug and security fixes, upgrade Astro Runtime when a new version becomes available." />
  <meta name="og:description" content="Learn how to upgrade the Astro Runtime version on your Deployments. To take advantage of new features and bug and security fixes, upgrade Astro Runtime when a new version becomes available." />
</head>

import {siteVariables} from '@site/src/versions';

New versions of Astro Runtime are released regularly to support new Astro and Apache Airflow functionality. To take advantage of new features and bug and security fixes, Astronomer recommends upgrading Astro Runtime as new versions are available.

## Prerequisites

- An [Astro project](develop-project.md#create-an-astro-project).
- An [Astro Deployment](create-deployment.md).
- The [Astro CLI](cli/install-cli.md).

:::info

If you're only upgrading a local Airflow environment, you don't need an Astro Deployment and you can skip steps 7-8.

:::

## Step 1: Review upgrade considerations

Astro upgrades can include breaking changes, especially when you're upgrading to a new major version. Check the [upgrade considerations](#upgrade-considerations) for your upgrade version to anticipate any breaking changes or upgrade-specific instructions.

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

The Astro CLI then generates test results in your Astro project that identify dependency conflicts and import errors that you would experience using the new Astro Runtime version. Review these results and make the recommended changes to reduce the risk of your project generating errors after you upgrade. For more information about using this command and the test results, see [Test before upgrade your Astro project](cli/test-your-astro-project-locally.md#test-before-upgrading-your-astro-project).

## Step 4: Update Your Dockerfile

1. In your Astro project, open your `Dockerfile`.
2. Change the Docker image in the `FROM` statement of your `Dockerfile` to a new version of Astro Runtime.

    To upgrade to the latest version of Runtime, for example, change the `FROM` statement in your Dockerfile to:

    <pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}`}</code></pre>

    You must always specify the major, minor, and patch version of any given Astro Runtime version.

## Step 5: Test Astro Runtime locally

Astronomer recommends testing new versions of Astro Runtime locally before upgrading a Deployment on Astro.

1. Save the changes to your `Dockerfile`.
2. Open your project directory in your terminal and run `astro dev restart`. This restarts the Docker containers for the Airflow webserver, scheduler, triggerer, and Postgres metadata database.
3. Access the Airflow UI of your local environment by navigating to `http://localhost:8080` in your browser.
4. Confirm that your local upgrade was successful by scrolling to the bottom of any page. You should see your new Astro Runtime version in the footer as well as the version of Airflow it is based on.

    ![Runtime Version banner - Local](/img/docs/image-tag-airflow-ui-local.png)

5. (Optional) Run DAGs locally to ensure that all of your code works as expected. If you encounter errors after your upgrade, it's possible that your new Astro Runtime version includes a breaking provider package change. If you encounter one of these breaking changes, follow the steps in [Upgrade or pin provider package versions](#optional-upgrade-or-pin-provider-package-versions) to check your provider package versions and, if required, pin the provider package version from your previous Runtime version in your `requirements.txt` file.

### Step 6: (Optional) Upgrade and test provider packages

If you pinned provider package versions before your upgrade, upgrade your provider packages by changing the pinned version in your `requirements.txt` file. Test east provider package upgrade locally before deploying to Astro. 

## Step 7: Deploy to Astronomer

To push your upgraded project to an Astro Deployment, run:

```sh
astro deploy
```

For more information about deploying to Astro, see [Deploy code](deploy-code.md).

:::caution

Once you upgrade to a Deployment on Astro to a new version of Astro Runtime, you cannot roll back or downgrade to a lower version. If you attempt to do so, you will see an error in the Astro CLI and your request to deploy will not succeed.

:::

## Step 8: Confirm your upgrade on Astro

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click **Open Airflow**.
3. In the Airflow UI, scroll to the bottom of any page. You should see your new Runtime version in the footer:

    ![Runtime Version banner - Astro](/img/docs/image-tag-airflow-ui-astro.png)

    You will also see an **Image tag** for your deploy. This tag is shown only for Deployments on Astro and is not generated for changes in a local environment.

## Upgrade considerations

Consider the following when you upgrade Astro Runtime:

- All versions of the Astro CLI support all versions of Astro Runtime. There are no dependencies between the two products.
- Upgrading to certain versions of Runtime might result in extended upgrade times or otherwise disruptive changes to your environment. To learn more, see [Version-specific upgrade considerations](upgrade-runtime.md#version-upgrade-considerations).
- Astronomer does not support downgrading a Deployment on Astro to a lower version of Astro Runtime.

To stay up to date on the latest versions of Astro Runtime, see [Astro Runtime release notes](runtime-release-notes.md). For more information on Astro Runtime versioning and support, see [Astro Runtime versioning and lifecycle policy](runtime-version-lifecycle-policy.md). For a full collection of Astro Runtime Docker images, go to the [Astro Runtime repository on Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

### Version upgrade considerations

This is where you'll find the upgrade considerations for specific Astro Runtime versions. This includes breaking changes, database migrations, and other considerations.

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

##### Upgrade directly to Astro Runtime 8.1

Astro Runtime 8.0 introduced a number of bugs and dependency conflicts which were subsequently fixed in Runtime 8.1. As a result, Astro Runtime 8.0 is not available in the Cloud UI and no longer supported by Astronomer. To use Airflow 2.6, upgrade directly to Runtime 8.1.

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

There is an incompatibility between Astro Runtime 8 and the following provider packages:

- `apache-airflow-providers-cncf-kubernetes==6.1.0`
- `apache-airflow-providers-google==10.0.0`

That can be resolved by pinning `apache-airflow-providers-cncf-kubernetes==5.2.2` in your `requirements.txt`file.

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

    These warnings have no impact on your tasks or DAGs and can be ignored. If you want to remove these warning messages from the Airflow UI, reach out to [Astronomer support](https://cloud.astronomer.io/support). If requested, Astronomer can drop incompatible tables from your metadata database.

For more information on Airflow 2.3, see ["Apache Airflow 2.3.0 is here"](https://airflow.apache.org/blog/airflow-2.3.0/) or the [Airflow 2.3.0 changelog](https://airflow.apache.org/docs/apache-airflow/2.3.0/release_notes.html#airflow-2-3-0-2022-04-30).