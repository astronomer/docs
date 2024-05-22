---
title: "Upgrading Astro Runtime"
sidebar_label: "Upgrading Astro Runtime"
description: "How to upgrade your version of Astro Runtime safely and rollback if necessary."
id: upgrading-astro
---

Astro includes features that make upgrading to the latest version of Astro Runtime easy and, more importantly, safe. When taking advantage of these features, you should keep a few best practices in mind to ensure that your Deployments remain stable and have all the latest fixes and improvements.

## Overview

In this guide, you'll learn about best practices to follow when:

- Upgrading Astro Runtime. 
- Performing a rollback to an earlier deployment and Runtime version in an emergency.

## General best practices

Keeping the version of Astro Runtime in your projects up-to-date is highly recommended as new versions are released regularly to apply bug fixes, security fixes, and improvements.

Upgrades can include breaking changes, particularly in the case of new major versions. Provider package upgrades in new minor versions of the underlying Airflow package can also cause issues. The Astro CLI has [built-in functionality](https://docs.astronomer.io/astro/cli/test-your-astro-project-locally#test-before-an-astro-runtime-upgrade) to keep such changes from breaking your DAGs. We recommend making use of this feature prior to every upgrade.

We also recommend reviewing the [Astro Runtime maintenance and lifecycle policy](https://docs.astronomer.io/astro/runtime-version-lifecycle-policy#astro-runtime-maintenance-policy) for maintenance duration information so you have plenty of time to upgrade before the maintenance window for your current version closes.

In the case of emergencies, a rollback to a previous deploy can be used to downgrade the Astro Runtime version. Astro's rollback functionality, akin to Git's `revert` feature, makes use of Astro's deploy history. Rollbacks revert project code only, keeping environment variables and other configuration unchanged. Also, downgrading erases any data related to newer features. For these reasons, we recommend viewing rollbacks only as a measure of last resort.

:::note

Enterprise users can use organization dashboards to check whether a Deployment's Astro Runtime version is currently supported. See [Organization dashboard](https://docs.astronomer.io/astro/organization-dashboard#deployment-detail) for details.

Upgrading to certain versions of Runtime can result in extended upgrade times or otherwise disruptive changes to your environment. To learn more, see [Version-specific upgrade considerations](https://docs.astronomer.io/astro/upgrade-runtime#version-upgrade-considerations).

::: 

## Upgrading Astro Runtime

For a smooth upgrade path, we recommend following the guidance in [Upgrade Astro Runtime](https://docs.astronomer.io/astro/upgrade-runtime) with special attention to these optional steps: 
- Pinning the provider package versions in your current version of Runtime to ensure a stable upgrade path. This is a simple process involving a single command and, if necessary, modification of `requirements.txt` based on the output.
- Running upgrade tests to anticipate and address problems. This involves a single command that:

	- Compares dependency versions between the current and upgraded environments.
	- Checks DAGs in the project against the new Airflow version for errors.
	- Runs a DAG parse test with the new Airflow version.
	- Produces in new project directory `upgrade-test-<current_version>--<upgraded_version>`:
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

For more details about the `upgrade-test` command, see [Testing your Astro project locally](https://docs.astronomer.io/astro/cli/test-your-astro-project-locally#test-before-an-astro-runtime-upgrade).

## Rolling back deployments

:::danger

Astronomer recommends triggering Deployment rollbacks only as a last resort for recent deploys that aren't working as expected. Deployment rollbacks can be disruptive, especially if you triggered multiple deploys between your current version and the rollback version. See [What happens during a deploy rollback](https://docs.astronomer.io/astro/upgrade-runtime#step-3-optional-run-upgrade-tests-with-the-astro-cli:~:text=What%20happens%20during%20a%20deploy%20rollback).

:::

:::tip

The `upgrade-test` command can also be used to test the current Runtime version against a _downgraded_ version.

:::

The only way to downgrade the version of Astro Runtime in a Deployment is to trigger a rollback to a previous deploy on Astro. To do so, follow the guidance in [Roll back to previous deploys using deploy histories](https://docs.astronomer.io/astro/deploy-history).

## See also 

- [Upgrade Astro Runtime](https://docs.astronomer.io/astro/upgrade-runtime#step-3-optional-run-upgrade-tests-with-the-astro-cli).
