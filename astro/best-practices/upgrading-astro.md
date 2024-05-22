---
title: "Upgrading Astro Runtime"
sidebar_label: "Upgrading Astro Runtime"
description: "How to upgrade your version of Astro Runtime safely and rollback if necessary."
id: upgrading-astro
---

Astro includes features that make upgrading to the latest version of Astro Runtime easy and, more importantly, safe. When taking advantage of these features, you should keep a few best practices in mind to ensure that your Deployments remain stable and current with the latest fixes and improvements.

## Feature overview

In this guide, you'll learn:

- How to use the [Astro CLI](https://docs.astronomer.io/cli/overview.md) to test an Astro project against a higher version of Astro Runtime for dependency conflicts and import errors prior to upgrading. 
- How to use the Astro UI to perform a rollback to an earlier deployment and Runtime version in an emergency.

## Best practice guidance

Keeping the version of Astro Runtime in your projects up-to-date is highly recommended as new versions are released regularly to apply bug fixes, security fixes, and improvements to Airflow.

Upgrades can apply breaking changes, particularly in the case of new major versions. With new minor versions of Airflow, it is typically provider package upgrades that cause issues. The Astro CLI has built-in functionality to identify and help resolve problems. We recommend making use of these features prior to upgrades.

In the case of emergencies, a rollback to a previous deploy can be used to downgrade the Astro Runtime version. Astro's rollback functionality, akin to Git's `revert` feature, makes use of Astro's deploy history. Rollbacks revert project code only, keeping environment variables and other configuration unchanged. Also, downgrading erases any data related to newer features. For these reasons, we recommend viewing rollbacks only as a measure of last resort.

:::note

Upgrading to certain versions of Runtime might result in extended upgrade times or otherwise disruptive changes to your environment. To learn more, see [Version-specific upgrade considerations](https://docs.astronomer.io/astro/upgrade-runtime#version-upgrade-considerations).

::: 

## Assumed knowledge

To get the most out of this guide, you should have a basic understanding of:

- The [Astro CLI](https://docs.astronomer.io/cli/overview.md).
- Creating and managing [Deployments](https://docs.astronomer.io/astro/create-deployment).

## Prepare for upgrades

Before upgrading Astro Runtime, we recommend: 
- Pinning the provider package versions in your current version of Runtime to ensure a stable upgrade path.
- Running upgrade tests to anticipate and address problems.

### Pin provider versions

New major versions of Astro Runtime (which correspond to minor versions of Airflow) can include major upgrades to built-in provider packages that can sometimes include breaking changes.

Check the version of all provider packages installed in your Runtime version by running:

```bash
docker run --rm quay.io/astronomer/astro-runtime:<current-runtime-version> pip freeze | grep apache-airflow-providers
```

Then, pin the package versions in `requirements.txt`:

```text
apache-airflow-providers-amazon==8.20.0
```

For more details, see [Upgrading Astro Runtime](https://docs.astronomer.io/astro/upgrade-runtime#step-2-optional-pin-provider-package-versions).

### Run upgrade tests

Run the following command to run tests against the version of Astro Runtime you're upgrading to:

```bash
astro dev upgrade-test --runtime-version <upgraded-runtime-version>
```

This command: 

- Compares dependency versions between the current and upgraded environments.
- Checks DAGs in the project against the new Airflow version for errors.
- Runs a DAG parse test with the new Airflow version.
- Produces in new project directory `upgrade-test-<current_version>--<upgraded_version>` containing:
	- A report with environment metadata and a Results table including any errors logged.
	- An upgraded `Dockerfile`.
	- `pip freeze` output for both versions.
	- A Dependency Compare report with comprehensive information about updates and removals. 

<p align="center">
	![Astro Upgrade Test Report](/img/guides/astro-upgrade_test_report.png)
</p>

```text
Apache Airflow Update:
apache-airflow 2.9.0+astro.2 >> 2.9.1+astro.1

Airflow Providers Minor Updates:
apache-airflow-providers-celery 3.6.2 >> 3.7.0

Airflow Providers Patch Updates:
apache-airflow-providers-openlineage 1.7.0 >> 1.7.1

Unknown Updates:
msrestazure 0.6.4 >> 0.6.4.post1

Major Updates:
azure-mgmt-datafactory 6.1.0 >> 7.0.0

Minor Updates:
Flask-Caching 2.1.0 >> 2.2.0

Patch Updates:
Mako 1.3.2 >> 1.3.3

Added Packages:
methodtools==0.4.7

```

For more details about this command, see [Testing your Astro project locally](https://docs.astronomer.io/astro/cli/test-your-astro-project-locally#test-before-an-astro-runtime-upgrade).

## Upgrade the Astro Runtime version and deploy to Astro

Follow the steps in [Upgrade Astro Runtime](https://docs.astronomer.io/astro/upgrade-runtime) to:

1. Change the version of Runtime in your `Dockerfile`.
2. Test Runtime locally.
3. Upgrade and test provider packages.
4. Deploy to Astronomer.
5. Confirm your upgrade on Astro.

## Rolling back deployments

The only way to downgrade the version of Astro Runtime in a Deployment is to trigger a rollback to a previous deploy on Astro.

:::danger

Astronomer recommends triggering Deployment rollbacks only as a last resort for recent deploys that aren't working as expected. Deployment rollbacks can be disruptive, especially if you triggered multiple deploys between your current version and the rollback version. See [What happens during a deploy rollback](https://docs.astronomer.io/astro/upgrade-runtime#step-3-optional-run-upgrade-tests-with-the-astro-cli:~:text=What%20happens%20during%20a%20deploy%20rollback).

:::

:::tip

The `upgrade-test` command can also be used to test the current Runtime version against a _downgraded_ version.

:::

1. In the Astro UI, select a Deployment.
2. Click **Deploy History**.
3. Locate the deploy you want to roll back to. In the **Rollback to** column for the deploy, click **Deploy**.
4. Provide a description for your rollback, then complete the confirmation to trigger the rollback.

For more details, see [Deploy history](https://docs.astronomer.io/astro/deploy-history#roll-back-to-a-past-deploy) and [Upgrade Astro Runtime](https://docs.astronomer.io/astro/upgrade-runtime#step-7-deploy-to-astronomer).

## See also 

- [Upgrade Astro Runtime](https://docs.astronomer.io/astro/upgrade-runtime#step-3-optional-run-upgrade-tests-with-the-astro-cli).
