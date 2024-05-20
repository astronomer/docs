---
title: "Upgrading Astro Runtime"
sidebar_label: "Upgrading Astro"
description: "How to upgrade your version of Astro Runtime safely and rollback if necessary."
id: upgrading-astro
---

Astro includes features that make upgrading to the latest version of Astro Runtime easy and, more importantly, safe. When taking advantage of these features, you should keep a few best practices in mind to ensure that your Deployments remain stable and current with the latest fixes and improvements.

## Feature overview

In this guide, you'll learn:

- How to use the [Astro CLI](https://docs.astronomer.io/cli/overview.md) to test an Astro project against a higher version of Astro Runtime for dependency conflicts and import errors prior to upgrading. 
- How to use the Astro UI to perform a rollback to an earlier deployment and Runtime version in an emergency.

## Best practice guidance

Keeping the version of Astro Runtime in your projects up-to-date is highly recommended as new versions are released regularly to apply bug fixes, security fixes, and improvements not only to Astro but also the underlying Airflow package.

Upgrades can apply breaking changes, especially in the case of new major versions. The Astro CLI has built-in functionality to identify and help resolve negative impacts of breaking changes. Using this feature prior to upgrades is highly recommended.

In the case of emergencies, the Astro UI supports rollbacks to previous deployments including automatic version downgrading. Astro's rollback functionality is akin to Git's `revert` feature and makes use of the UI's deploy history. Rollbacks revert project code only, keeping environment variables and other configuration unchanged. Also, downgrading erases any data related to newer features. For these reasons, we recommend viewing rollbacks only as a measure of last resort. 

## Assumed knowledge

To get the most out of this guide, you should have a basic understanding of:

- The [Astro CLI](https://docs.astronomer.io/cli/overview.md).
- Creating and managing [Deployment](https://docs.astronomer.io/astro/create-deployment)s on Astro.

### Testing upgrades using the Astro CLI

Before upgrading Astro Runtime, we recommend running the Astro CLI's `upgrade-test` command locally:

```bash
astro dev upgrade-test --runtime-version <upgraded-runtime-version>
```

This command: 

- Compares dependency versions between the current and upgraded environments.
- Checks DAGs in the project against the new Airflow version for errors.
- Runs a DAG parse test with the new Airflow version.
- Produces:
	- an HTML report with environment metadata and a Results table including any errors logged.
	- an upgraded Dockerfile.
	- `pip freeze` output for both versions.
	- a Dependency Compare file with all versioning information organized by Airflow Providers Minor Updates, Airflow Providers Major Updates, Major Updates, Minor Updates, etc. 

![Astro Upgrade Test Report](/img/guides/astro-upgrade_test_report.png)

```text
Apache Airflow Update:
apache-airflow 2.9.0+astro.2 >> 2.9.1+astro.1

Airflow Providers Minor Updates:
apache-airflow-providers-celery 3.6.2 >> 3.7.0
apache-airflow-providers-common-sql 1.12.0 >> 1.13.0
apache-airflow-providers-datadog 3.5.1 >> 3.6.0
apache-airflow-providers-elasticsearch 5.3.4 >> 5.4.0
apache-airflow-providers-fab 1.0.4 >> 1.1.0
apache-airflow-providers-ftp 3.8.0 >> 3.9.0
apache-airflow-providers-http 4.10.1 >> 4.11.0
apache-airflow-providers-imap 3.5.0 >> 3.6.0
apache-airflow-providers-mysql 5.5.4 >> 5.6.0
apache-airflow-providers-postgres 5.10.2 >> 5.11.0
apache-airflow-providers-redis 3.6.1 >> 3.7.0
apache-airflow-providers-smtp 1.6.1 >> 1.7.0
apache-airflow-providers-sqlite 3.7.1 >> 3.8.0

Airflow Providers Patch Updates:
apache-airflow-providers-openlineage 1.7.0 >> 1.7.1

Unknown Updates:
msrestazure 0.6.4 >> 0.6.4.post1

Major Updates:
azure-mgmt-datafactory 6.1.0 >> 7.0.0
google-ads 23.1.0 >> 24.0.0
platformdirs 3.11.0 >> 4.2.1
redis 4.6.0 >> 5.0.4
urllib3 1.26.18 >> 2.2.1
```

### Rolling back deployments

:::danger

Astronomer recommends triggering Deployment rollbacks only as a last resort for recent deploys that aren't working as expected. Deployment rollbacks can be disruptive, especially if you triggered multiple deploys between your current version and the rollback version. See [What happens during a deploy rollback](https://docs.astronomer.io/astro/upgrade-runtime#step-3-optional-run-upgrade-tests-with-the-astro-cli:~:text=What%20happens%20during%20a%20deploy%20rollback).

The only way to downgrade a Deployment's version of Astro Runtime is to trigger a rollback to a previous deploy on Astro.

:::

The Astro UI supports rollbacks including automatic version downgrading. For detailed instructions, see [Deploy history](https://docs.astronomer.io/astro/deploy-history#roll-back-to-a-past-deploy) and [Upgrade Astro Runtime](https://docs.astronomer.io/astro/upgrade-runtime#step-7-deploy-to-astronomer).

:::tip

The `upgrade-test` command can also be used to test the current Runtime version against a _downgraded_ version.

:::

See also [Upgrade Astro Runtime](https://docs.astronomer.io/astro/upgrade-runtime#step-3-optional-run-upgrade-tests-with-the-astro-cli).
