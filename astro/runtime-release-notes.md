---
sidebar_label: 'Astro Runtime'
title: 'Astro Runtime release notes'
id: runtime-release-notes
toc_min_heading_level: 2
---

import {siteVariables} from '@site/src/versions';

<head>
  <meta name="description" content="This is where you’ll find information about the latest Astro Runtime features and functionality. Astro Runtime is a Docker image built by Astronomer that provides a differentiated Apache Airflow experience and execution framework." />
  <meta name="og:description" content="This is where you’ll find information about the latest Astro Runtime features and functionality. Astro Runtime is a Docker image built by Astronomer that provides a differentiated Apache Airflow experience and execution framework." />
</head>

<!--version-specific-->

<p>
    <a href="/astro-runtime-release-notes.xml" target="_blank">
        <img src="/img/pic_rss.gif" width="36" height="14" alt="Subscribe to RSS Feed" />
    </a>
</p>

Astro Runtime is a Docker image built and published by Astronomer that extends the Apache Airflow project to provide a differentiated data orchestration experience. This document provides a summary of changes made to each available version of Astro Runtime. 

To upgrade Astro Runtime, see [Upgrade Astro Runtime](upgrade-runtime.md). For general product release notes, see [Astro Release Notes](release-notes.md). If you have any questions or a bug to report, contact [Astronomer support](https://cloud.astronomer.io/support).

## Astro Runtime 9.2.0

- Release date: October 12, 2023
- Airflow version: 2.7.2

### Airflow 2.7.2

Astro Runtime 9.2.0 includes same-day support for Apache Airflow 2.7.2. Airflow 2.7.2 contains a number of bug fixes including:

- Check if the lower of provided values are sensitives in config endpoint ([#34712](https://github.com/apache/airflow/pull/34712))
- Add missing audit logs for Flask actions add, edit and delete ([#34090](https://github.com/apache/airflow/pull/34090))
- Fix the required permissions to clear a TI from the UI ([#34123](https://github.com/apache/airflow/pull/34123))
- Fixed a bug where manually-triggered DAG runs were causing the recalculation of when the scheduler would trigger the next DAG run ([#34027](https://github.com/apache/airflow/pull/34027))

To learn more, see the [Apache Airflow 2.7.2 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-7-2-2023-10-12).

## Astro Runtime 9.1.0

- Release date: September 7, 2023
- Airflow version: 2.7.1

### Airflow 2.7.1

Astro Runtime 9.1.0 includes same-day support for Apache Airflow 2.7.1. Airflow 2.7.1 contains a number of bug fixes including:

- Treat dag-defined access_control as authoritative if defined ([#33632](https://github.com/apache/airflow/pull/33632))
- Add limit 1 if required first value from query result ([#33632](https://github.com/apache/airflow/pull/33632))
- Fix MappedTaskGroup tasks not respecting upstream dependency ([#33732](https://github.com/apache/airflow/pull/33732))

To learn more, see the [Apache Airflow 2.7.1 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-7-1-2023-09-07).

### Additional improvements

- You can now [export task logs to Datadog](view-logs.md#export-task-logs-to-datadog) from Azure and GCP clusters.
- Upgraded `openlineage-airflow` to 1.1.0. See the [OpenLineage release notes](https://openlineage.io/docs/releases/1_1_0/) for a complete list of changes.
- Upgraded `astro-sdk-python` to 1.7.0, which adds support for Excel files. See the [Astro Python SDK changelog](https://astro-sdk-python.readthedocs.io/en/stable/CHANGELOG.html#id1) for a complete list of changes.

## Astro Runtime 9.0.0

- Release date: August 18, 2023
- Airflow version: 2.7.0

### Airflow 2.7

Astro Runtime 9 is based on Airflow 2.7, which includes a number of new features and improvements. Most notably, Airflow 2.7 includes the following changes:

- In the Airflow UI, the **Trigger DAG w/ config** button now appears only when a DAG has configured [params](https://docs.astronomer.io/learn/airflow-params). Because some teams use this workflow without configuring DAG params, this change has been feature flagged. To revert the change, set the following environment variable in your Dockerfile or as an Astro [environment variable](environment-variables.md):

    - **Key**: `AIRFLOW__WEBSERVER__SHOW_TRIGGER_FORM_IF_NO_PARAMS`
    - **Value**: `True`

- Setup and teardown tasks are a new type of task that you can use to prepare resources and configurations for specific tasks, ensuring that they always have resources even when you retry failed tasks. See [Use setup and teardown tasks in Airflow](https://docs.astronomer.io/learn/airflow-setup-teardown) to learn how to use them.
- You can now clear task groups or mark them as successful/failed from the Airflow UI **Grid View** just like individual tasks.
- You can set `operators.default_deferrable` in your Airflow config to always use the deferrable version of an operator if one is available, which means that you no longer have to update import statements in DAGs to replace traditional operators with deferrable ones. 

To learn more, see the [Apache Airflow 2.7.0 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-7-0-2023-08-14).

### New Python version distributions of Astro Runtime

Each new version of Astro Runtime now has separate distributions for Python 3.8, 3.9. 3.10 and 3.11. Using a Python distribution of Astro Runtime is the easiest way to use a specific Python version in Airflow. 

Specify the Python version you want to use in your image tag, formatted as:

```text
quay.io/astronomer/astro-runtime:<runtime-version>-python-<python-version>
```

For example, to use Python 3.8 in Astro Runtime 9.0.0, you would replace the image tag in your Astro project Dockerfile with `quay.io/astronomer/astro-runtime:9.0.0-python-3.8`.

To keep using the same version of Python across multiple Astro Runtime upgrades, Astronomer recommends that you begin to use the Python distribution for your required Python version.

### Upgrade to Python 3.11

The base image for Astro Runtime now uses Python 3.11. If you want to use a different version of Python, replace your image with the appropriate Python distribution of Astro Runtime.

### Additional improvements

- Upgraded `astronomer-providers` to 1.17.3. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1173-2023-08-07) for a complete list of changes.
- Upgraded `astro-sdk-python` to 1.6.2. See the [Astro Python SDK changelog](https://astro-sdk-python.readthedocs.io/en/stable/CHANGELOG.html#id1) for a complete list of changes.
- Upgraded `openlineage-airflow` to 1.0.0. See the [OpenLineage blog](https://openlineage.io/blog/1.0-release/) for a summary of what's arrived in OpenLineage's first 1.x version.

### Bug fixes

- Fixed an issue where you could not set DAG or task notes in the Airflow UI for environments running on Astro.

## Astro Runtime 8.9.0

- Release date: August 28, 2023
- Airflow version: 2.6.3

### Early access Airflow bug fixes

- Fixed an issue where Airflow incorrectly used `urljoin` to generate the string for `log_url`. ([#33063](https://github.com/apache/airflow/pull/33063)) 

### Additional improvements

- Upgraded `astronomer-providers` to 1.17.3. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1173-2023-08-07) for a complete list of changes.
- Upgraded `astro-sdk-python` to 1.6.2. See the [Astro Python SDK changelog](https://astro-sdk-python.readthedocs.io/en/stable/CHANGELOG.html#id1) for a complete list of changes.

### Bug fixes

- Fixed an issue where you could not set DAG or task notes in the Airflow UI for environments running on Astro.
- Fixed an issue with trigger logs for Deployments running on AWS.

## Astro Runtime 8.8.0

- Release date: July 21, 2023
- Airflow version: 2.6.3

### Early access Airflow bug fixes

- Fix bad delete logic for DAG runs ([32684](https://github.com/apache/airflow/pull/32684)).

### Additional improvements

- Upgraded a few built-in providers to new minor versions. 

### Bug fixes

- Upgraded `apache-airflow-providers-microsoft-azure` to 6.2.1. This fixes an issue where Deployments running Astro Runtime 8.7.0 on Azure clusters experienced failures with deferrable operators and task logs.
- Fixed DAG deletion permissions in Astro for non-admin users.

## Astro Runtime 8.7.0

- Release date: July 11, 2023
- Airflow version: 2.6.3

### Airflow 2.6.3

Astro Runtime 8.7.0 includes same-day support for Apache Airflow 2.6.3. Airflow 2.6.3 contains a number of bug fixes including:

- Fix `operator_extra_links` property serialization in mapped tasks ([31904](https://github.com/apache/airflow/pull/31904))
- You can now specify a format for manual `run_id` inputs. Manually entered `run_ids` must conform with the regex specified in the `[scheduler]allowed_run_id_pattern` setting. [32293](https://github.com/apache/airflow/pull/32293))

For a complete list of the changes, see the [Apache Airflow 2.6.3 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html).

### Additional improvements

- Upgraded `openlineage-airflow` to 0.29.2, which includes support for Spark 3.4. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.29.2) for a complete list of changes. 

## Astro Runtime 8.6.0

- Release date: June 27, 2023
- Airflow version: 2.6.2

### Additional improvements 

- Upgraded `astronomer-providers` to 1.17.1, which includes enhancements to the `S3KeySizeSensorAsync` and some bug fixes. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1170-2023-06-21) for a complete list of changes.
- Upgraded `apache-airflow-providers-providers-amazon` to [8.2.0](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/index.html#id1).

## Astro Runtime 8.5.0

- Release date: June 17, 2023
- Airflow version: 2.6.2

### Airflow 2.6.2

Astro Runtime 8.5.0 includes same-day support for Apache Airflow 2.6.2. Airflow 2.6.2 contains a number of bug fixes including:

- Fix Kubernetes executors detection of deleted pods ([31274](https://github.com/apache/airflow/pull/31274))
- Fix crash when clearing run with task from normal to mapped ([31352](https://github.com/apache/airflow/pull/31352))

For a complete list of the changes, see the [Apache Airflow 2.6.2 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html).

### Additional improvements

- Upgraded `openlineage-airflow` to 0.28.0. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.28.0) for a complete list of changes. 

### Bug fixes

- Fixed an issue where Istio versions were being parsed as [Python versions](https://peps.python.org/pep-0440/) instead of [semantic versions](https://semver.org/), resulting in DAG errors.

## Astro Runtime 8.4.0

- Release date: June 2, 2023
- Airflow version: 2.6.1

### Early access Airflow bug fixes

- Fixed the scheduler crashing when you cleared a run of a normal task that is now a mapped task ([31352](https://github.com/apache/airflow/pull/31352)).

### Additional improvements

- Upgraded `astro-sdk-python` to 1.6.1, which includes support for MySQL and loading data from Azure blob storage to Databricks. See the [Astro Python SDK changelog](https://astro-sdk-python.readthedocs.io/en/stable/CHANGELOG.html#id1) for a complete list of changes.
- Upgraded `apache-airflow-providers-cncf-kubernetes` to [7.0.0](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/index.html#id1).

### Bug fixes

- Fixed an issue where you could not use the KubernetesPodOperator without setting `AIRFLOW_CONN_KUBERNETES_DEFAULT="kubernetes://` in your environment.

## Astro Runtime 8.3.0

- Release date: May 26, 2023
- Airflow version: 2.6.1

### Early access Airflow bug fixes

- Fixed a bug to ensure that `min_backoff` in the base sensor is at least `1` ([31412](https://github.com/apache/airflow/pull/31412))
- Updated error messaging ([31502](https://github.com/apache/airflow/pull/31502))

### Additional improvements

- Upgraded `astronomer-providers` to 1.16.0. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1160-2023-05-19) for a complete list of changes. 
- Upgraded `openlineage-airflow` to 0.26.0. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.26.0) for a complete list of changes. 
- Blocked the ability to pause the Monitoring DAG with the Airflow API. The Monitoring DAG is used by Astronomer to operate your Deployments and should not be paused.
- Added the Datadog provider. See the [Astronomer Registry](https://registry.astronomer.io/providers/apache-airflow-providers-datadog/versions/3.3.0) for more information on using the provider.

## Astro Runtime 8.2.0

- Release date: May 16, 2023
- Airflow version: 2.6.1

### Airflow 2.6.1

Astro Runtime 8.2.0 includes same-day support for Apache Airflow 2.6.1. Airflow 2.6.1 contains a number of bug fixes including:

- Fix timestamp parse failure for Kubernetes executor pod tailing ([31175](https://github.com/apache/airflow/pull/31175))
- Fix calculation of health check threshold for SchedulerJob ([31277](https://github.com/apache/airflow/pull/31277))

For a complete list of the changes, see the [Apache Airflow 2.6.1 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html).

### Additional improvements

- Upgraded `astronomer-providers` to 1.15.5, which includes bug fixes. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1154-2023-04-19) for a complete list of changes. 
- Upgraded `openlineage-airflow` to 0.25.0, which adds support for Spark/Delta `merge into` support. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.25.0) for a complete list of changes. 

## Astro Runtime 8.1.0

- Release date: May 9, 2023
- Airflow version: 2.6.0

### Early access Airflow bug fixes

- Ensure the KPO runs pod mutation hooks correctly ([31173](https://github.com/apache/airflow/pull/31173))

### Additional improvements

- Upgraded `astro-sdk` to 1.6, which includes Astro Python SDK support for MySQL. For a complete list of changes, see the [Astro SDK changelog](https://github.com/astronomer/astro-sdk/blob/main/python-sdk/docs/CHANGELOG.md#160).

## Astro Runtime 8.0.0

- Release date: April 30, 2023
- Airflow version: 2.6.0

:::warning Breaking change

Runtime 8 includes changes that can result in DAGs running differently after upgrading. It also includes a major bug that was subsequently fixed in Runtime 8.1. To use Airflow 2.6, Astronomer recommends upgrading directly to Runtime 8.1. See [Runtime upgrade considerations](upgrade-runtime.md#runtime-8-airflow-26) for more information.

:::

### Airflow 2.6

Astro Runtime 8 is based on Airflow 2.6, which includes a number of new features and improvements with an emphasis on observability. Most notably, Airflow 2.6 includes the following changes:

- [Notifiers](https://airflow.apache.org/docs/apache-airflow/stable/howto/notifications.html) are a new class that can be used to send notifications from a DAG to a third party application, such as Slack. This release includes the [SlackNotifier](https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/_api/airflow/providers/slack/notifications/slack_notifier/index.html#airflow.providers.slack.notifications.slack_notifier.SlackNotifier), with more notifiers coming in the future. 
- A major bug related to zombie tasks has been fixed. The logic for handling stalled tasks has been moved to the scheduler, and any tasks that have been queued for more than `scheduler.task_queued_timeout` are now marked as failed. This prevents a type of zombie task where tasks are stuck in an infinite loop of being scheduled and queued. 
- You can now view logs for individual triggers in the Airflow UI. Trigger logs tell you when an individual task is sleeping and when it's triggered.

To learn more, see the [Apache Airflow 2.6.0 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-6-0-2023-04-30).

### Fewer dependencies installed by default

Astro Runtime now includes fewer default dependencies to save on memory usage. The following provider packages are no longer installed by default:

- `apache-airflow-providers-apache-hive`
- `apache-airflow-providers-apache-livy`
- `apache-airflow-providers-databricks`
- `apache-airflow-providers-dbt-cloud`
- `apache-airflow-providers-microsoft-mssql`
- `apache-airflow-providers-sftp`
- `apache-airflow-providers-snowflake`
- `apache-airflow-providers-ssh`

If your DAGs use any of these providers, ensure that the provider packages are listed in your Astro project `requirements.txt` file before upgrading. 

### Upgrade to Python 3.10

Astro Runtime now uses Python 3.10 by default. To continue using Python 3.9, see [Python versioning](runtime-image-architecture.md#python-versioning).

### Additional improvements

- Upgraded `astronomer-providers` to 1.15.4, which includes a bug fix for a backwards compatibility issue. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1154-2023-04-19) for a complete list of changes. 
- Upgraded `openlineage-airflow` to 0.23.0, which includes support for dbt snapshots and support for parsing additional SQL commands. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/blob/main/CHANGELOG.md#0230---2023-4-20) for a complete list of changes.

## Astro Runtime 7.6.0

- Release date: June 13, 2023
- Airflow version: 2.5.3

### Early access Airflow bug fixes

- Mark `[secrets] backend_kwargs` as a sensitive config ([31788](https://github.com/apache/airflow/pull/31788))

### Additional Improvements

- Upgraded `openlineage-airflow` to 0.27.2. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.27.2) for a complete list of changes. 

## Astro Runtime 7.5.0

- Release date: May 29, 2023
- Airflow version: 2.5.3

### Early access Airflow bug fixes

- Fixed a bug to ensure that `min_backoff` in the base sensor is at least `1` ([31412](https://github.com/apache/airflow/pull/31412))
- Updated error messaging ([31502](https://github.com/apache/airflow/pull/31502))

### Additional Improvements

- Upgraded `astronomer-providers` to 1.16.0. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1160-2023-05-19) for a complete list of changes. 
- Upgraded `astro-sdk-python` to 1.6.1, which includes support for MySQL and loading data from Azure blob storage to Databricks. See the [Astro Python SDK changelog](https://astro-sdk-python.readthedocs.io/en/stable/CHANGELOG.html#id1) for a complete list of changes.
- Upgraded `openlineage-airflow` to 0.26.0. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.26.0) for a complete list of changes. 
- Blocked the ability to pause the Monitoring DAG with the Airflow API. The Monitoring DAG is used by Astronomer to operate your Deployments and should not be paused.

## Astro Runtime 7.4.3

- Release date: April 28, 2023
- Airflow version: 2.5.3

### Early access Airflow bug fixes

- Fix KubernetesExecutor sending state to scheduler ([30872](https://github.com/apache/airflow/pull/30872))

### Additional improvements

- Upgraded `astronomer-providers` to 1.15.4, which includes a bug fix for a backwards compatibility issue. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1154-2023-04-19) for a complete list of changes. 

## Astro Runtime 7.4.2

- Release date: April 1, 2023
- Airflow version: 2.5.3

### Airflow 2.5.3

Astro Runtime 7.4.2 includes same-day support for Apache Airflow 2.5.3. Airflow 2.5.3 contains a number of bug fixes including:

- Fix `TriggerRuleDep` when the mapped tasks count is 0 ([30084](https://github.com/apache/airflow/pull/30084))
- Fix some long known Graph View UI problems ([29971](https://github.com/apache/airflow/pull/29971))

For a complete list of the changes, see the [Apache Airflow 2.5.3 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html).

### Additional improvements 

- Upgraded `astronomer-providers` to 1.15.2, which includes several bug fixes. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/releases/tag/1.15.2) for a complete list of changes. 

## Astro Runtime 7.4.1

- Release date: March 17, 2023
- Airflow version: 2.5.2

### Early access Airflow bug fixes

- Ensure that `dag.partial_subset` doesn't mutate task group properties ([30129](https://github.com/apache/airflow/pull/30129))
- Revert fix for on_failure_callback when task receives a SIGTERM ([30165](https://github.com/apache/airflow/pull/30165))

## Astro Runtime 7.4.0

- Release date: March 15, 2023
- Airflow version: 2.5.2

### Airflow 2.5.2

Astro Runtime 7.2.0 includes same-day support for Apache Airflow 2.5.2. Airflow 2.5.2 contains a number of bug fixes including:

- Fix validation of date-time field in API and Parameter schemas ([29395](https://github.com/apache/airflow/pull/29395))
- DAG list sorting lost when switching page ([29756](https://github.com/apache/airflow/pull/29756))

For a complete list of the changes, see the [Apache Airflow 2.5.2 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-5-2-2023-03-15).

### Additional improvements

- Upgraded `astro-sdk-python` to 1.5.3, which includes Openlineage facets for Microsoft SQL server and restores some pandas load option classes. See the [Astro Python SDK changelog](https://astro-sdk-python.readthedocs.io/en/stable/CHANGELOG.html#id1) for a complete list of changes.
- Upgraded `astronomer-providers` to 1.15.1, which includes a new async sensor `SnowflakeSensorAsync` and a number of bug fixes. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1151-2023-03-09) for a complete list of changes. 
- Upgraded `openlineage-airflow` to 0.21.1, which includes support for capturing custom environment variables from Spark and a number of bug fixes. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.21.1) for a complete list of changes. 

## Astro Runtime 7.3.0

- Release date: February 14, 2023
- Airflow version: 2.5.1

### Early access Airflow bug fixes

- Use time not tries for queued & running re-checks ([28586](https://github.com/apache/airflow/pull/28586))

### Additional improvements 

- Installed the following OS-level packages to support the Astro Python SDK MSSQL integration:

    - `postgresql-client`
    - `freetds-dev`
    - `libssl-dev`
    - `libkrb5-dev`
    
- Upgraded `astro-sdk-python` to 1.5.0, which includes support for Microsoft SQL and DuckDB. See the [Astro Python SDK changelog](https://github.com/astronomer/astro-sdk/blob/main/python-sdk/docs/CHANGELOG.md#150) for a complete list of changes.
- Upgraded `openlineage-airflow` to 0.20.4, which includes a new extractor for the GCSToGCSOperator. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.17.0) for a complete list of changes. 

## Astro Runtime 7.2.0

- Release date: January 20, 2023
- Airflow version: 2.5.1

### Airflow 2.5.1

Astro Runtime 7.2.0 includes same-day support for Apache Airflow 2.5.1. Airflow 2.5.1 contains a number of bug fixes including:

- Return list of tasks that will be queued ([28066](https://github.com/apache/airflow/pull/28066))
- Fix masking of non-sensitive environment variables ([28802](https://github.com/apache/airflow/pull/28802))

For a complete list of the changes, see the [Apache Airflow 2.5.1 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-5-1-2023-01-20).

### The Astro Python SDK is now included with Astro Runtime

Astro Runtime now includes the Astro Python SDK, an open source tool and Python package (`astro-sdk-python`) for DAG development that is built and maintained by Astronomer. With Astro Runtime versions 7.2.0 and later, you don't have to add the Astro Python SDK to your Astro project to use it.

To learn more about the Astro Python SDK, see [Astro Python SDK ReadTheDocs](https://astro-sdk-python.readthedocs.io/en/stable/) and [The Astro Python SDK Tutorial for ETL](https://docs.astronomer.io/learn/astro-python-sdk-etl).

### Early access Airflow bug fixes

In anticipation of future support for the Kubernetes executor on Astro, Astro Runtime includes the following bug fixes from Airflow 2.5.2:

- Be more selective when adopting pods with KubernetesExecutor ([28899](https://github.com/apache/airflow/pull/28899))
- KubernetesExecutor sends state even when successful ([28871](https://github.com/apache/airflow/pull/28871))
- Annotate KubeExecutor pods that we don't delete ([28844](https://github.com/apache/airflow/pull/28844))

### Additional improvements

- Upgraded `astronomer-providers` to 1.14.0, which includes support for using a role Amazon Resource Name (ARN) with `AwsBaseHookAsync`. See the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/1.13.0/CHANGELOG.rst) for a complete list of changes.
- Upgraded `openlineage-airflow` to 0.19.2, which includes new support for Airflow operators like the `S3FileTransformOperator` and additional facets for task runs. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.19.2) for a complete list of changes.

## Astro Runtime 7.1.0

- Release date: December 21, 2022
- Airflow version: 2.5.0

### Additional improvements

- Upgraded `astronomer-providers` to 1.13.0, which includes a collection of minor enhancements and bug fixes. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1130-2022-12-16). 
- Upgraded `openlineage-airflow` to 0.18.0, which includes new support for Airflow operators like the `SQLExecuteQueryOperator`. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.18.0) for more information. 
- Upgraded `apache-airflow-providers-microsoft-azure` to 5.0.1, which includes a bug fix to revert `offset` and `length` to be optional arguments.
- Upgraded `certifi` to 2022.12.7.
- Airflow environments hosted on Astro now include a **Back to Astro** button in the Airflow UI. Use this button to return to the Deployment hosting the Airflow environment in the Cloud UI.

## Astro Runtime 7.0.0 

- Release date: December 2, 2022 
- Airflow version: 2.5.0

### Airflow 2.5.0

Astro Runtime 7.0.0 includes same-day support for Airflow 2.5.0, which includes a collection of new features, bug fixes, automatic changes, and deprecations. Features include:

- Add comments to task instances and DAG runs in the Airflow UI ([#26457](https://github.com/apache/airflow/pull/26457))
- Clear all task instances in a task group with one click in the Airflow UI ([#26658](https://github.com/apache/airflow/pull/26658)), [#28003](https://github.com/apache/airflow/pull/28003))
- Trigger a task when at least one upstream tasks is successful with new `one_done` trigger rule [#26146](https://github.com/apache/airflow/pull/26146)
- New **Parsed at** metric in the DAG view of the Airflow UI [#27573](https://github.com/apache/airflow/pull/27573)
- Filter datasets in Airflow UI based on recent update events [#26942](https://github.com/apache/airflow/pull/26942)

To learn more, see [What's New in Apache Airflow 2.5](https://www.astronomer.io/blog/whats-new-in-apache-airflow-2-5/) and the [Apache Airflow 2.5.0 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-5-0-2022-12-02).

### Additional improvements 

- In the Airflow UI for Astro Deployments, the **Audit Logs** page now shows the Astro user who performed a given action in the **Owner** column.
- Upgraded `astronomer-providers` to 1.11.2, which includes a collection of bug fixes. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1112-2022-11-19). 
- Upgraded `openlineage-airflow` to 0.17.0, which includes improvements to the OpenLineage spark integration and additional facets for the OpenLineage Python client. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.17.0) for more information.  

## Astro Runtime 6.6.0

- Release date: June 13, 2023
- Airflow version: 2.4.3

### Early access Airflow bug fixes

- Mark `[secrets] backend_kwargs` as a sensitive config ([31788](https://github.com/apache/airflow/pull/31788))

### Additional Improvements

- Upgraded `openlineage-airflow` to 0.27.2. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.27.2) for a complete list of changes. 

## Astro Runtime 6.5.0

- Release date: May 29, 2023
- Airflow version: 2.4.3

### Early access Airflow bug fixes

- Updated error messaging ([31502](https://github.com/apache/airflow/pull/31502))

### Additional Improvements

- Upgraded `astronomer-providers` to 1.16.0. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1160-2023-05-19) for a complete list of changes. 
- Upgraded `openlineage-airflow` to 0.26.0. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.26.0) for a complete list of changes. 
- Blocked the ability to pause the Monitoring DAG with the Airflow API. The Monitoring DAG is used by Astronomer to operate your Deployments and should not be paused.

## Astro Runtime 6.4.0

- Release date: March 23, 2023
- Airflow version: 2.4.3

### Early access Airflow bug fixes

- Ensure that `dag.partial_subset` doesn't mutate task group properties ([#30129](https://github.com/apache/airflow/pull/30129))
- redirect to the origin page with all the params ([#29212](https://github.com/apache/airflow/pull/29212))
- datasets, next_run_datasets, remove unnecessary timestamp filter ([#29441](https://github.com/apache/airflow/pull/29441))

### Additional improvements

- Upgraded `astronomer-providers` to 1.15.1, which includes a collection of bug fixes and a new async sensor `SnowflakeSensorAsync`. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1151-2023-03-09) for a complete list of changes.. 
- Upgraded `openlineage-airflow` to 0.21.1, which includes a collection of bug fixes. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.21.1) for a complete list of changes. 
- When using Runtime in an Astronomer Software installation, OpenLineage and the Astronomer monitoring DAG are now disabled. OpenLineage can be re-enabled in your Deployment by setting the `OPENLINEAGE_URL` environment variable, or by setting the `OPENLINEAGE_DISABLED=False` environment variable.

## Astro Runtime 6.3.0

- Release date: February 14, 2023
- Airflow version: 2.4.3

### Early access Airflow bug fixes

- Use time not tries for queued & running re-checks ([28586](https://github.com/apache/airflow/pull/28586))

### Additional improvements 

- Upgraded `openlineage-airflow` to 0.20.4, which includes a new extractor for the GCSToGCSOperator. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.17.0) for a complete list of changes. 

## Astro Runtime 6.2.1

- Release date: January 26, 2023
- Airflow version: 2.4.3

### Early access Airflow bug fixes

In anticipation of future support for the Kubernetes executor on Astro, Astro Runtime includes the following bug fixes from Apache Airflow:

- Annotate KubernetesExecutor pods that we don’t delete ([28844](https://github.com/apache/airflow/pull/28844))

## Astro Runtime 6.2.0

- Release date: January 26, 2023
- Airflow version: 2.4.3

### Early access Airflow bug fixes

In anticipation of future support for the Kubernetes executor on Astro, Astro Runtime includes the following bug fixes from Apache Airflow:

- Fix bad pods pickled in executor_config ([28454](https://github.com/apache/airflow/pull/28454))
- Be more selective when adopting pods with KubernetesExecutor ([28899](https://github.com/apache/airflow/pull/28899))
- Only patch single label when adopting pod ([28776](https://github.com/apache/airflow/pull/28776))

### Additional improvements 

- Upgraded `astronomer-providers` to 1.14.0, which includes support for using a role ARN with `AwsBaseHookAsync`. See the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/1.13.0/CHANGELOG.rst) for a complete list of changes.
- Upgraded `openlineage-airflow` to 0.19.2, which includes new support for Airflow operators such as the `S3FileTransformOperator` and additional facets for task runs. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.19.2) for a complete list of changes.

## Astro Runtime 6.1.0

- Release date: December 21, 2022
- Airflow version: 2.4.3

### Early access Airflow bug fixes

- Make DagRun state updates for paused DAGs faster ([#27725](https://github.com/apache/airflow/pull/27725))
- Fix deadlock when chaining multiple empty mapped tasks ([#27964](https://github.com/apache/airflow/pull/27964))

### Additional improvements 

- Upgraded `astronomer-providers` to 1.13.0, which includes a collection of minor enhancements and bug fixes. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1130-2022-12-16). 
- Upgraded `openlineage-airflow` to 0.18.0, which includes new support for Airflow operators like the `SQLExecuteQueryOperator`. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.18.0) for more information.
- Upgraded `apache-airflow-providers-microsoft-azure` to 5.0.1, which includes a bug fix to revert `offset` and `length` to be optional arguments.
- You can now run Astro Runtime images on Red Hat OpenShift.
- In the Airflow UI for Astro Deployments, the **Audit Logs** page now shows the Astro user who performed a given action in the **Owner** column.
- Airflow environments hosted on Astro now include a **Back to Astro** button in the Airflow UI. Use this button to return to the Deployment hosting the Airflow environment in the Cloud UI.
- You can now add comments to the `packages.txt` file of an Astro project.

## Astro Runtime 6.0.4

- Release date: November 14, 2022
- Airflow version: 2.4.3

### ARM64-based images for faster local development with Apple M1

:::caution

To deploy a project using Astro Runtime 6.0.4 or later from an Apple M1 computer to Astro, you must use Astro CLI version 1.4.0 or later or else the deploy will fail. See [Install the Astro CLI](cli/install-cli.md).

:::

Astro Runtime images now support both AMD64 and ARM64 processor architectures for local development. When you install Astro Runtime 6.0.4 or later, Docker automatically runs the correct architecture based on the computer you're using.

If you run the Astro CLI on a Mac computer that uses an ARM-based [Apple M1 Silicon chip](https://www.apple.com/newsroom/2020/11/apple-unleashes-m1/), you will see a significant performance improvement when running Airflow locally. For example, the time it takes to run `astro dev start` on average has decreased from over 5 minutes to less than 2 minutes.

For more information on developing locally with the Astro CLI, see [Develop a Project](cli/develop-project.md).

### Airflow 2.4.3 

Astro Runtime 6.0.4 includes same-day support for Airflow 2.4.3, which includes a collection of bug fixes. Fixes include:

- Make `RotatingFilehandler` used in `DagProcessor` non-caching ([27223](https://github.com/apache/airflow/pull/27223))
- Fix double logging with some task logging handler ([27591](https://github.com/apache/airflow/pull/27591))

For a complete list of the changes, see the [Apache Airflow 2.4.3 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-4-3-2022-11-14).

### Additional improvements 

- Upgraded `openlineage-airflow` to 0.16.1. This release includes the `DefaultExtractor`, which allows you to extract the default available OpenLineage data for external operators without needing to write a custom extractor. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.16.1) for more information. 
- Upgraded `astronomer-providers` to 1.11.1, which includes bug fixes. For a complete list of the changes, see the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1111-2022-10-28).

## Astro Runtime 6.0.3

- Release date: October 24, 2022
- Airflow version: 2.4.2

### Airflow 2.4.2

Astro Runtime 6.0.3 includes same-day support for Airflow 2.4.2. Some changes in Airflow 2.4.2 include:

- Handle mapped tasks in task duration chart ([#26722](https://github.com/apache/airflow/pull/26722))
- Make tracebacks opt-in ([#27059](https://github.com/apache/airflow/pull/27059))

For a complete list of commits, see the [Apache Airflow 2.4.2 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-4-2-2022-10-23).

### Additional improvements  

- Upgraded `openlineage-airflow` to 0.15.1, which includes a dedicated Airflow development environment. You can now create and test changes to custom OpenLineage extractors in an Airflow environment without needing to rebuild your Docker images. For more information, see the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/blob/main/CHANGELOG.md).

## Astro Runtime 6.0.2

- Release date: September 30, 2022
- Airflow version: 2.4.1

### Airflow 2.4.1

Astro Runtime 6.0.2 includes same-day support for Airflow 2.4.1, which includes a collection of bug fixes. Fixes include:

- Fix Deferrable stuck as scheduled during backfill ([#26205](https://github.com/apache/airflow/pull/26205))
- Don't update backfill run from the scheduler ([#26342](https://github.com/apache/airflow/pull/26342))

For a complete list of commits, see the [Apache Airflow 2.4.1 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-4-1-2022-09-30).

### Early access Airflow bug fixes

Astro Runtime 6.0.2 includes the following bug fixes from Apache Airflow 2.4.2:

- Remove DAG parsing from StandardTaskRunner ([#26750](https://github.com/apache/airflow/pull/26750))
- Fix airflow tasks run --local when dags_folder differs from that of processor ([#26509](https://github.com/apache/airflow/pull/26509))
- Add fixture for CLI tests requiring sample dags ([#26536](https://github.com/apache/airflow/pull/26536))

### Additional improvements

- Upgraded `astronomer-providers` to 1.10.0, which includes `SFTPSensorAsync` and `ExternalDeploymentTaskSensorAsync` as new deferrable operators. For a complete list of changes, see the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1100-2022-09-30).

## Astro Runtime 6.0.1

- Release date: September 26, 2022
- Airflow version: 2.4.0

### Bug fixes 

- Fixed an issue where Astro users could not access task logs on Deployments using Runtime 6.0.0
- Backported a fix to correct an issue where logs were not loading from Celery workers ([#26493](https://github.com/apache/airflow/pull/26493))
- Fixed [CVE-2022-40674](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40674)

## Astro Runtime 6.0.0

- Release date: September 19, 2022
- Airflow version: 2.4.0

### Airflow 2.4 and data-aware scheduling

Astro Runtime 6.0.0 provides same-day support for [Airflow 2.4.0](https://airflow.apache.org/blog/airflow-2.4.0/), which delivers significant new features for DAG scheduling. The most notable new features in Airflow 2.4.0 are:

- [Data-aware scheduling](https://airflow.apache.org/docs/apache-airflow/2.4.0/concepts/datasets.html), which is a new method for scheduling a DAG based on when an upstream DAG modifies a specific dataset.
- The [ExternalPythonOperator](https://airflow.apache.org/docs/apache-airflow/2.4.0/howto/operator/python.html#externalpythonoperator), which can execute Python code in a virtual environment with different Python libraries and dependencies than your core Airflow environment.
- Automatic DAG registration. You no longer need to specify `as dag` when defining a DAG object.
- Support for [zipping](https://airflow.apache.org/docs/apache-airflow/2.4.0/concepts/dynamic-task-mapping.html#combining-upstream-data-aka-zipping) dynamically mapped tasks.

For a complete list of commits, see the [Apache Airflow 2.4.0 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-4-0-2022-09-19).

### Additional improvements

- Upgraded `astronomer-providers` to 1.9.0, which includes two new deferrable versions of the operators from the dbt provider package. See the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/1.9.0/CHANGELOG.rst).
- Upgraded `openlineage-airflow` to version `0.14.1`. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/blob/main/CHANGELOG.md).

## Astro Runtime 5.4.0

- Release date: March 23, 2023
- Airflow version: 2.3.4

### Early access Airflow bug fixes

- Ensure that `dag.partial_subset` doesn't mutate task group properties ([#30129](https://github.com/apache/airflow/pull/30129))

### Additional improvements

- Upgraded `astronomer-providers` to 1.15.1, which includes a collection of bug fixes and a new async sensor `SnowflakeSensorAsync`. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1151-2023-03-09) for a complete list of changes.. 
- Upgraded `openlineage-airflow` to 0.21.1, which includes a collection of bug fixes. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.21.1) for a complete list of changes. 
- When using Runtime in an Astronomer Software installation, OpenLineage and the Astronomer monitoring DAG are now disabled. OpenLineage can be re-enabled in your Deployment by setting the `OPENLINEAGE_URL` environment variable, or by setting the `OPENLINEAGE_DISABLE=False` environment variable.

## Astro Runtime 5.3.0

- Release date: February 14, 2023
- Airflow version: 2.3.4

### Early access Airflow bug fixes

- Use time not tries for queued & running re-checks ([28586](https://github.com/apache/airflow/pull/28586))

### Additional improvements 

- Upgraded `openlineage-airflow` to 0.20.4, which includes a new extractor for the GCSToGCSOperator. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.17.0) for a complete list of changes. 

## Astro Runtime 5.2.1

- Release date: January 26, 2023
- Airflow version: 2.3.4

### Early access Airflow bug fixes

In anticipation of future support for the Kubernetes executor on Astro, Astro Runtime includes the following bug fixes from Apache Airflow:

- Annotate KubernetesExecutor pods that we don’t delete ([28844](https://github.com/apache/airflow/pull/28844))

## Astro Runtime 5.2.0

- Release date: January 26, 2023
- Airflow version: 2.3.4

### Early access Airflow bug fixes

In anticipation of future support for the Kubernetes executor on Astro, Astro Runtime includes the following bug fixes from Apache Airflow:

- Fix bad pods pickled in executor_config ([28454](https://github.com/apache/airflow/pull/28454))
- Be more selective when adopting pods with KubernetesExecutor ([28899](https://github.com/apache/airflow/pull/28899))
- Only patch single label when adopting pod ([28776](https://github.com/apache/airflow/pull/28776))
- Don’t re-patch pods that are already controlled by current worker ([26778](https://github.com/apache/airflow/pull/26778))
- Fix backfill queued task getting reset to scheduled state ([23720](https://github.com/apache/airflow/pull/23720))

### Additional improvements 

- Upgraded `astronomer-providers` to 1.14.0, which includes support for using a role ARN with `AwsBaseHookAsync`. See the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/1.13.0/CHANGELOG.rst) for a complete list of changes.
- Upgraded `openlineage-airflow` to 0.19.2, which includes new support for Airflow operators like the `S3FileTransformOperator` and additional facets for task runs. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.19.2) for a complete list of changes.

## Astro Runtime 5.1.0

- Release date: January 4, 2023
- Airflow version: 2.3.4

### Additional improvements

- Upgraded `astronomer-providers` to 1.13.0, which includes a collection of minor enhancements and bug fixes. See the [`astronomer-providers` changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#1130-2022-12-16). 
- Upgraded `openlineage-airflow` to 0.18.0, which includes new support for Airflow operators like the `SQLExecuteQueryOperator`. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/releases/tag/0.18.0) for more information. 
- Airflow environments hosted on Astro now include a **Back to Astro** button in the Airflow UI. Use this button to return to the Deployment hosting the Airflow environment in the Cloud UI.

## Astro Runtime 5.0.13

- Release date: December 12, 2022
- Airflow version: 2.3.4

### Backported Airflow bug fixes

Astro Runtime 5.0.13 includes the following bug fixes from later Apache Airflow releases:

- Change the template to use human readable task_instance description ([#25960](https://github.com/apache/airflow/pull/25960))
- Fix deadlock when chaining multiple empty mapped tasks ([#27964](https://github.com/apache/airflow/pull/27964))

### Additional improvements

- You can now run Astro Runtime images on Red Hat OpenShift.
- You can now add comments to the `packages.txt` file of an Astro project.
- In the Airflow UI for Astro Deployments, the **Audit Logs** page now shows the Astro user who performed a given action in the **Owner** column.

## Astro Runtime 5.0.12

- Release date: November 9, 2022
- Airflow version: 2.3.4

### Backported Airflow bug fixes

Astro Runtime 5.0.12 includes the following bug fixes from Apache Airflow 2.4.2:

- Make tracebacks opt-in ([#27059](https://github.com/apache/airflow/pull/27059))
- Avoid 500 on dag redirect ([#27064](https://github.com/apache/airflow/pull/27064))
- Don’t overwrite connection extra with invalid json ([#27142](https://github.com/apache/airflow/pull/27142))
- Simplify origin string cleaning ([#27143](https://github.com/apache/airflow/pull/27143))

## Astro Runtime 5.0.11

- Release date: November 2, 2022
- Airflow version: 2.3.4

### Backported Airflow bug fixes

Astro Runtime 5.0.11 includes the following bug fix from later Apache Airflow releases:

- Fix warning when using xcomarg dependencies ([#26801](https://github.com/apache/airflow/pull/26801))

### Bug fixes

- Removed the default value for `AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER`, as this value is now set in the Astro data plane. This enables Astronomer Software users to set a value for custom remote logging storage solutions. 

## Astro Runtime 5.0.10

- Release date: October 17, 2022
- Airflow version: 2.3.4

### Additional improvements

- Upgraded `astronomer-providers` to 1.10.0, which includes two new deferrable versions of operators, `SFTPSensorAsync` and `ExternalDeploymentTaskSensorAsync`. See the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/1.10.0/CHANGELOG.rst).
- Upgraded `openlineage-airflow` to version `0.15.1`. See the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/blob/main/CHANGELOG.md).

### Bug fixes

- Revert “Cache the custom secrets backend so the same instance gets re-used” ([#25556](https://github.com/apache/airflow/pull/25556))
- Fixed faulty Kubernetes executor config serialization logic

## Astro Runtime 5.0.9

- Release date: September 20, 2022
- Airflow version: 2.3.4

### Early access Airflow bug fixes

- Fixed an issue where logs were not loading from Celery workers ([#26337](https://github.com/apache/airflow/pull/26337) and [#26493](https://github.com/apache/airflow/pull/26493))
- Fixed CVE-2022-40754 ([#26409](https://github.com/apache/airflow/pull/26409))
- Fixed the Airflow UI not auto-refreshing when scheduled tasks are running. This bug was introduced in Airflow 2.3.4 ([#25950](https://github.com/apache/airflow/pull/25950))
- Fixed an issue where the scheduler could crash when queueing dynamically mapped tasks ([#25788](https://github.com/apache/airflow/pull/25788))

### Additional improvements

- Set `AIRFLOW__CELERY__STALLED_TASK_TIMEOUT=600` by default. This means that tasks that are in `queued` state for more than 600 seconds (10 minutes) will fail. This environment variable can be overridden on Astro but will help prevent tasks from getting stuck in a queued state.
- Upgraded `astronomer-providers` to 1.8.1, which includes various bug fixes. For a complete list of changes, see the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#181-2022-09-01).
- Upgraded `openlineage-airflow` to 0.13.0, which includes fixes for Spark integrations. See the [Astronomer Providers changelog](https://github.com/OpenLineage/OpenLineage/blob/main/CHANGELOG.md#0141---2022-09-07).

## Astro Runtime 5.0.8

- Release date: August 23, 2022
- Airflow version: 2.3.4

### Airflow 2.3.4

Astro Runtime 5.0.8 includes Airflow 2.3.4, which primarily includes bug fixes. For a complete list of commits, see the [Apache Airflow 2.3.4 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-3-4-2022-08-23).

### Additional improvements

- Upgraded `astronomer-providers` to version `1.8.0`, which includes minor bug fixes and performance enhancements. For more information, see the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/1.8.0/CHANGELOG.rst).
- Upgraded `openlineage-airflow` to version `0.13.0`, which includes support for Azure Cosmos DB. For a list of all changes, see the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/blob/main/CHANGELOG.md).

## Astro Runtime 5.0.7

- Release date: August 16, 2022
- Airflow version: 2.3.3

### Early access Airflow bug fixes

Astro Runtime 5.0.7 includes the following bug fixes:

- Fixed an issue where [plugins specified as a python package](https://airflow.apache.org/docs/apache-airflow/stable/plugins.html#plugins-as-python-packages) in an `entry_points` argument were incorrectly loaded twice by Airflow and resulted in an error in the Airflow UI. This bug was introduced in Airflow 2.3.3 ([#25296](https://github.com/apache/airflow/pull/25296))
- Fixed an issue where zombie tasks were not properly cleaned up from DAGs with parse errors [#25550](https://github.com/apache/airflow/pull/25550))
- Fixed an issue where clearing a deferred task instance would not clear its `next_method` field ([#23929](https://github.com/apache/airflow/pull/23929))

These changes were backported from Apache Airflow 2.3.4, which is not yet generally available. The bug fixes were also backported to Astro Runtime 5.0.5.

### Additional improvements

- The Cloud UI no longer shows source code for [supported Airflow operators](https://openlineage.io/docs/integrations/about#capability-matrix) by default. To reenable this feature for a given Deployment, create an [environment variable](environment-variables.md) with a key of `OPENLINEAGE_AIRFLOW_DISABLE_SOURCE_CODE` and a value of `False`.
- Upgraded `openlineage-airflow` to version `0.12.0`, which includes support for Spark 3.3.0 and Apache Flink. For a list of all changes, see the [OpenLineage changelog](https://github.com/OpenLineage/OpenLineage/blob/main/CHANGELOG.md).
- Upgraded `astronomer-providers` to version `1.7.1`, which includes new deferrable operators and improvements to documentation. For more information, see the [Astronomer Providers changelog](https://github.com/astronomer/astronomer-providers/blob/1.7.1/CHANGELOG.rst).
- Upgraded `apache-airflow-providers-amazon` to version `4.1.0`, which includes a bug fix for integrating with AWS Secrets Manager.

## Astro Runtime 5.0.6

- Release date: July 11, 2022
- Airflow version: 2.3.3

### Airflow 2.3.3

Astro Runtime 5.0.6 includes Airflow 2.3.3, which includes bug fixes and UI improvements. For a complete list of commits, see the [Apache Airflow 2.3.3 release notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-3-3-2022-07-05).

### Additional improvements

- Upgraded `astronomer-providers` to 1.6.0, which includes new deferrable operators and support for OpenLineage extractors. For more information, see the [Astronomer Providers changelog](https://astronomer-providers.readthedocs.io/en/stable/changelog.html#id1).

### Bug fixes

- Fixed zombie task handling with multiple schedulers ([#24906](https://github.com/apache/airflow/pull/24906))
- Fixed an issue where `TriggerDagRunOperator.operator_extra_links` could cause a serialization error ([#24676](https://github.com/apache/airflow/pull/24676)

## Astro Runtime 5.0.5

- Release date: July 1, 2022
- Airflow version: 2.3.2

### Early access Airflow bug fixes

Astro Runtime 5.0.5 includes the following bug fixes:

- Fixed an issue where part of the **Grid** view of the Airflow UI would crash or become unavailable if a `GET` request to the Airflow REST API failed ([#24152](https://github.com/apache/airflow/pull/24152))
- Improved the performance of the **Grid** view ([#24083](https://github.com/apache/airflow/pull/24083))
- Fixed an issue where grids for task groups in the **Grid** view always showed data for the latest DAG run instead of the correct DAG run ([#24327](https://github.com/apache/airflow/pull/24327))

These changes were backported from Apache Airflow 2.3.3, which is not yet generally available.

### Additional improvements

- Updated `openlineage-airflow` to v0.10.0. This release includes a built-in `SnowflakeOperatorAsync` extractor for Airflow, an `InMemoryRelationInputDatasetBuilder` for `InMemory` datasets for Spark, and the addition of a copyright statement to all source files

## Astro Runtime 5.0.4

- Release date: June 15, 2022
- Airflow version: 2.3.2

### Additional improvements

- Update `astronomer-providers` to v1.5.0. For more information, see the [Astronomer Providers Changelog](https://astronomer-providers.readthedocs.io/en/stable/changelog.html#id1).
- Add support for Astro clusters with [Istio](https://istio.io/) enabled.

## Astro Runtime 5.0.3

- Release date: June 4, 2022
- Airflow version: 2.3.2

### Airflow 2.3.2

Astro Runtime 5.0.3 includes support for Airflow 2.3.2, which includes:

- Improvements to the Grid view of the Airflow UI, including faster load times for large DAGs and a fix for an issue where some tasks would not render properly ([#23947](https://github.com/apache/airflow/pull/23947))
- Enable clicking on DAG owner in autocomplete dropdown ([#23804](https://github.com/apache/airflow/pull/23804))
- Mask sensitive values for task instances that are not yet running ([#23807](https://github.com/apache/airflow/pull/23807))
- Add cascade to `dag_tag` to `dag` foreign key ([#23444](https://github.com/apache/airflow/pull/23444))

For more information, see the [changelog for Apache Airflow 2.3.2](https://github.com/apache/airflow/releases/tag/2.3.2).

### Additional improvements

- Update `astronomer-providers` to v1.4.0. For more information, see the [Astronomer Providers Changelog](https://astronomer-providers.readthedocs.io/en/stable/changelog.html#id1).
- Update `openlineage-airflow` to v0.9.0. This release includes a fix for an issue present in v0.7.1, v0.8.1, and v0.8.2 where some tasks run with the Snowflake operator would deadlock and not execute. For more information, see the [OpenLineage GitHub repository](https://github.com/OpenLineage/OpenLineage/tree/main/integration/airflow).

## Astro Runtime 5.0.2

- Release date: May 27, 2022
- Airflow version: 2.3.1

### Airflow 2.3.1

Astro Runtime 5.0.2 includes same-day support for Airflow 2.3.1, a release that follows Airflow 2.3.0 with a collection of bug fixes.

Fixes include:

- Automatically reschedule stalled queued tasks in Celery executor ([#23690](https://github.com/apache/airflow/pull/23690))
- Fix secrets rendered in Airflow UI when task is not executed ([#22754](https://github.com/apache/airflow/pull/22754))
- Performance improvements for faster database migrations to Airflow 2.3

For more information, see the [changelog for Apache Airflow 2.3.1](https://github.com/apache/airflow/releases/tag/2.3.1).

### Additional improvements

- Update `astronomer-providers` to v1.3.1. For more information, see the [Astronomer Providers Changelog](https://astronomer-providers.readthedocs.io/en/stable/changelog.html#id5).
- Update `openlineage-airflow` to v0.8.2. For more information, see the [OpenLineage GitHub repository](https://github.com/OpenLineage/OpenLineage/tree/main/integration/airflow).

## Astro Runtime 5.0.1

- Release date: May 9, 2022
- Airflow version: 2.3.0

### Astronomer Providers 1.2.0

Astro Runtime 5.0.1 includes v1.2.0 of the `astronomer-providers` package ([CHANGELOG](https://astronomer-providers.readthedocs.io/en/stable/)). This release includes 5 new [deferrable operators](https://docs.astronomer.io/learn/deferrable-operators):

    - `DataprocSubmitJobOperatorAsync`
    - `EmrContainerSensorAsync`
    - `EmrStepSensorAsync`
    - `EmrJobFlowSensorAsync`
    - `LivyOperatorAsync`

To access the source code of this package, visit the [Astronomer Providers GitHub repository](https://github.com/astronomer/astronomer-providers).

### Additional improvements

- Improved performance when upgrading to Astro Runtime 5.0.x
- Bumped the [`openlineage-airflow` dependency](https://openlineage.io/docs/integrations/airflow/) to `v0.8.1`

## Astro Runtime 5.0.0

- Release date: April 30, 2022
- Airflow version: 2.3.0

### Support for Airflow 2.3 & dynamic task mapping

Astro Runtime 5.0.0 provides support for [Airflow 2.3.0](https://airflow.apache.org/blog/airflow-2.3.0/), which is a significant open source release. The most notable new features in Airflow 2.3.0 are:

- [Dynamic task mapping](https://airflow.apache.org/docs/apache-airflow/2.3.0/concepts/dynamic-task-mapping.html), which allows you to generate task instances at runtime based on changing data and input conditions.
- A new **Grid** view in the Airflow UI that replaces the **Tree** view and provides a more intuitive way to visualize the state of your tasks.
- The ability to [define Airflow connections in JSON](https://airflow.apache.org/docs/apache-airflow/2.3.0/howto/connection.html#json-format-example) instead of as a Connection URI.
- The ability to [reuse a decorated task function](https://airflow.apache.org/docs/apache-airflow/2.3.0/tutorial_taskflow_api.html#reusing-a-decorated-task) between DAGs.

For more information on Airflow 2.3, see ["Apache Airflow 2.3 — Everything You Need to Know"](https://www.astronomer.io/blog/apache-airflow-2-3-everything-you-need-to-know) by Astronomer.

## Astro Runtime 4.2.9

- Release date: December 12, 2022
- Airflow version: 2.2.5

### Backported Airflow bug fixes

Astro Runtime 4.2.9 includes the following bug fixes from later Apache Airflow releases:

- Change the template to use human readable task_instance description ([#25960](https://github.com/apache/airflow/pull/25960))

### Additional improvements

- You can now run Astro Runtime images on Red Hat OpenShift.
- You can now add comments to the `packages.txt` file of an Astro project.
- In the Airflow UI for Astro Deployments, the **Audit Logs** page now shows the Astro user who performed a given action in the **Owner** column.

## Astro Runtime 4.2.8

- Release date: November 9, 2022
- Airflow version: 2.2.5

### Backported Airflow bug fixes

Astro Runtime 4.2.8 includes the following bug fixes from Apache Airflow 2.4.2:

- Make tracebacks opt-in ([#27059](https://github.com/apache/airflow/pull/27059))
- Don’t overwrite connection extra with invalid json ([#27142](https://github.com/apache/airflow/pull/27142))
- Simplify origin string cleaning ([#27143](https://github.com/apache/airflow/pull/27143))

## Astro Runtime 4.2.7

- Release date: October 11, 2022
- Airflow version: 2.2.5

### Backported Airflow bug fixes

Astro Runtime 4.2.7 includes the following bug fixes from later Apache Airflow releases:

- Make sure finalizers are not skipped during exception handling ([#22475](https://github.com/apache/airflow/pull/22475))
- Fix `email_on_failure` with `render_template_as_native_obj` ([#22770](https://github.com/apache/airflow/pull/22770))
- Do not log the hook connection details even at DEBUG level ([#22627](https://github.com/apache/airflow/pull/22627))

### Bug fixes

- Fixed the following vulnerabilities:

    - [CVE-2022-40023](https://avd.aquasec.com/nvd/2022/cve-2022-40023/)
    - [CVE-2022-2309](https://avd.aquasec.com/nvd/2022/cve-2022-2309/)
    - [CVE-2022-40674](https://avd.aquasec.com/nvd/2022/cve-2022-40674/)
    - [CVE-2022-1586](https://avd.aquasec.com/nvd/2022/cve-2022-1586/)
    - [CVE-2022-1587](https://avd.aquasec.com/nvd/2022/cve-2022-1587/)
    - [CVE-2022-3999](https://avd.aquasec.com/nvd/2022/cve-2022-3999/)
    - [CVE-2022-37434](https://avd.aquasec.com/nvd/2022/cve-2022-37434/)
    - [DSA-5197](https://www.debian.org/security/2022/dsa-5197)
    - [CVE-2022-2509](https://avd.aquasec.com/nvd/2022/cve-2022-2509/)
    - [CVE-2022-46828](https://avd.aquasec.com/nvd/2022/cve-2022-46828/)
    - [CVE-2022-1664](https://avd.aquasec.com/nvd/2022/cve-2022-1664/)
    - [CVE-2022-29155](https://avd.aquasec.com/nvd/2022/cve-2022-29155/)
    - [CVE-2022-2068](https://avd.aquasec.com/nvd/2022/cve-2022-2068/)
    - [CVE-2022-1292](https://avd.aquasec.com/nvd/2022/cve-2022-1292/)
    - [CVE-2022-1552](https://avd.aquasec.com/nvd/2022/cve-2022-1552/)

## Astro Runtime 4.2.6

- Release date: April 19, 2022
- Airflow version: 2.2.5

### Additional improvements

- Add initial support for Astro Runtime on Google Cloud Platform (GCP), including logging in Google Cloud Storage (GCS). Support for Astro on GCP is coming soon.

## Astro Runtime 4.2.5
- Release date: April 11, 2022
- Airflow version: 2.2.5

### Bug fixes

- Bug Fix: Apply a [new constraints file](https://raw.githubusercontent.com/apache/airflow/constraints-2.2.5/constraints-3.9.txt) to fix a version incompatibility error with `apache-airflow-providers-elasticsearch` that made task logs inaccessible to users in the Airflow UI. This change was required by Astronomer Software and did not impact users on Astro.

## Astro Runtime 4.2.4

- Release date: April 6, 2022
- Airflow version: 2.2.5

### Support for Airflow 2.2.5

Astro Runtime 4.2.2 includes support for Apache Airflow 2.2.5, which exclusively contains bug fixes and performance improvements. For details on the release, read the [Airflow 2.2.5 changelog](https://airflow.apache.org/docs/apache-airflow/stable/changelog.html#airflow-2-2-5-2022-04-04).

## Astro Runtime 4.2.1

- Release date: March 28, 2022
- Airflow version: 2.2.4

### New deferrable operators

Astro Runtime 4.2.1 upgrades the `astronomer-providers` package to v1.1.0 ([CHANGELOG](https://github.com/astronomer/astronomer-providers/blob/main/CHANGELOG.rst#110-2022-03-23)). In addition to bug fixes and performance improvements, this release includes 7 new deferrable operators:

    - `S3KeySizeSensorAsync`
    - `S3KeysUnchangedSensorAsync`
    - `S3PrefixSensorAsync`
    - `GCSObjectsWithPrefixExistenceSensorAsync`
    - `GCSObjectUpdateSensorAsync`
    - `GCSUploadSessionCompleteSensorAsync`
    - `BigQueryTableExistenceSensorAsync`

For more information about deferrable operators and how to use them, see [Deferrable operators](https://docs.astronomer.io/learn/deferrable-operators). To access the source code of this package, see the [Astronomer Providers GitHub repository](https://github.com/astronomer/astronomer-providers).

### Additional improvements

- Bump the [`openlineage-airflow` provider package](https://openlineage.io/docs/integrations/airflow/) to `v0.6.2`

## Astro Runtime 4.2.0

- Release date: March 10, 2022
- Airflow version: 2.2.4

### New Astronomer Providers package

The `astronomer-providers` package is now installed on Astro Runtime by default. This package is an open source collection of Apache Airflow providers and modules that is maintained by Astronomer. It includes deferrable versions of popular operators such as `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`.

For more information, see [Deferrable operators](https://docs.astronomer.io/learn/deferrable-operators). To access the source code of this package, see the [Astronomer Providers GitHub repository](https://github.com/astronomer/astronomer-providers).

### Additional improvements

- Bump the [`openlineage-airflow` provider package](https://openlineage.io/docs/integrations/airflow/) to `v0.6.1`

## Astro Runtime 4.1.0

- Release date: February 22, 2022
- Airflow version: 2.2.4

### Support for Airflow 2.2.4

Astro Runtime 4.1.0 includes support for Apache Airflow 2.2.4, which exclusively contains bug fixes and performance improvements. For details on the release, read the [Airflow 2.2.4 changelog](https://airflow.apache.org/docs/apache-airflow/stable/changelog.html#airflow-2-2-4-2022-02-22).

## Astro Runtime 4.0.11

- Release date: February 14, 2022
- Airflow version: 2.2.3

### Additional improvements

- Upgraded the `openlineage-airflow` library to `v0.5.2`

## Astro Runtime 4.0.10

- Release date: February 9, 2022
- Airflow version: 2.2.3

### New deferrable operators now available

Astro Runtime now also includes the following operators:

- `KubernetesPodOperatorAsync`
- `HttpSensorAsync`
- `SnowflakeOperatorAsync`
- `FileSensorAsync`

These are all [deferrable operators](https://docs.astronomer.io/learn/deferrable-operators) built by Astronomer and available exclusively on Astro Runtime. They are pre-installed into the Astro Runtime Docker image and ready to use.

### Additional improvements

- The Airflow UI now shows the Deployment's Docker image tag in the footer of all pages. For more information, see [Astro Release Notes for March 10, 2022](release-notes.md#march-10-2022).

### Additional improvements

- To support an enhanced logging experience on Astro, the `apache-airflow-providers-elasticsearch` provider package is now installed by default.

## Astro Runtime 4.0.9

- Release date: January 19, 2022
- Airflow version: 2.2.3

### Additional improvements

- The [`openlineage-airflow` provider package](https://openlineage.io/docs/integrations/airflow/) is now installed in Runtime by default.

## Astro Runtime 4.0.8

- Release date: December 21, 2021
- Airflow version: 2.2.3

### Support for Airflow 2.2.3

Astro Runtime 4.0.8 includes support for [Airflow 2.2.3](https://airflow.apache.org/docs/apache-airflow/stable/changelog.html#airflow-2-2-3-2021-12-20).

Airflow 2.2.3 exclusively contains bug fixes, including:
- Fix for a broken link to task logs in the Gantt view of the Airflow UI ([#20121](https://github.com/apache/airflow/pull/20121))
- Replace references to "Execution Date" in the Task Instance and DAG run tables of the Airflow UI with "Logical Date" ([#19063](https://github.com/apache/airflow/pull/19063))
- Fix problem whereby requests to the `DAGRun` endpoint of Airflow's REST API would return a 500 error if DAG run is in state `skipped` ([#19898](https://github.com/apache/airflow/pull/19898))
- Fix problem where task logs in Airflow UI showed incorrect timezone ([#19401](https://github.com/apache/airflow/pull/19401))
- Fix problem where the **Connections** form in the Airflow UI showed incorrect field names ([#19411](https://github.com/apache/airflow/pull/19411))

### Bug fixes

- Disabled the **Pause** button for `astronomer_monitoring_dag`, which cannot be disabled and helps the Astronomer team monitor the health of your Deployment.

## Astro Runtime 4.0.7

- Release date: December 15, 2021
- Airflow version: 2.2.2

### Astronomer monitoring DAG

Astro Runtime 4.0.7 includes a monitoring DAG that is pre-installed in the Docker image and enabled for all customers. In addition to existing Deployment health and metrics functionality, this DAG allows the Astronomer team to better monitor the health of your data plane by enabling real-time visibility into whether your workers are healthy and tasks are running.

The `astronomer_monitoring_dag` runs a simple bash task every 5 minutes to ensure that your Airflow scheduler and workers are functioning as expected. If the task fails twice in a row or is not scheduled within a 10-minute interval, Astronomer support receives an alert and will work with you to troubleshoot.

Because this DAG is essential to Astro's managed service, your organization will not be charged for its task runs. For the same reasons, this DAG can't be modified or disabled via the Airflow UI. To modify how frequently this DAG runs, you can specify an alternate schedule as a cron expression by setting `AIRFLOW_MONITORING_DAG_SCHEDULE_INTERVAL` as an environment variable.

## Astro Runtime 4.0.6

- Release date: December 2, 2021
- Airflow version: 2.2.2

### Additional improvements

- User-supplied `airflow.cfg` files are no longer valid in Astro projects. [Environment variables](environment-variables.md) are now the only valid method for setting Airflow configuration options.

### Bug fixes

- Fixed an issue where the **Browse** menu of the Airflow UI was hidden in some versions of Astro Runtime

## Astro Runtime 4.0.5

- Release date: November 29, 2021
- Airflow version: 2.2.2

### Bug fixes

- Fixed an issue where Astro's S3 logging hook prevented users from setting up S3 as a custom XCom backend

## Astro Runtime 4.0.4

- Release date: November 19, 2021
- Airflow version: 2.2.2

### Bug fixes

- Fixed an issue where DAG run and task instance records didn't show up as expected in the Airflow UI

## Astro Runtime 4.0.3

- Release date: November 15, 2021
- Airflow version: 2.2.2

### Additional improvements

- Added support for [Airflow 2.2.2](https://airflow.apache.org/docs/apache-airflow/stable/changelog.html#airflow-2-2-2-2021-11-15), which includes a series of bug fixes for timetables, DAG scheduling, and database migrations. Most notably, it resolves an issue where some DAG runs would be missing in the Airflow UI if `catchup=True` was set.

### Bug fixes

- Fixed an issue where the Astro-themed Airflow UI was not present in local development

## Astro Runtime 4.0.2

- Release date: October 29, 2021
- Airflow version: 2.2.1

### Additional improvements

- Added support for [Airflow 2.2.1](https://airflow.apache.org/docs/apache-airflow/stable/changelog.html#airflow-2-2-1-2021-10-29), which includes a series of bug fixes that address intermittent problems with database migrations from Airflow 2.1 to Airflow 2.2

## Astro Runtime 4.0.1

- Release date: October 26, 2021
- Airflow version: 2.2.0

### Bug fixes

- Fixed an issue where worker pods were stuck in a terminating state when scaling down
- Fixed an issue where the Airflow UI navbar and footer did not show the correct running version of Astro Runtime

## Astro Runtime 4.0.0

- Release date: October 12, 2021
- Airflow version: 2.2.0

### Support for Airflow 2.2.0

Astro Runtime 4.0.0 is a significant release that supports and enhances [Apache Airflow 2.2.0](https://airflow.apache.org/blog/airflow-2.2.0/), an exciting milestone in the open source project. Most notably, this release introduces custom timetables and deferrable operators.

#### Custom timetables

Timetables represent a powerful new framework that allows Airflow users to create custom schedules using Python. In an effort to provide more flexibility and address known limitations imposed by cron, timetables use an intuitive `data_interval` that, for example, allows you to schedule a DAG to run daily on Monday through Friday, but not on the weekend. Timetables can be easily plugged into existing DAGs, which means that it's easy to create your own or use community-developed timetables in your project.

In addition to supporting the timetables framework, the team at Astronomer has built a `TradingHoursTimetable` that's ready to use in Runtime 4.0.0. You can use this timetable to run a DAG based on whether or not a particular global market is open for trade.

For more information on using timetables, read the [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/timetable.html).

#### Deferrable operators

[Deferrable operators](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html) are a new type of Airflow operator that promises improved performance and lower resource costs. While standard operators and sensors take up a worker slot even when they are waiting for an external trigger, deferrable operators are designed to suspend themselves and free up that worker slot while they wait. This is made possible by a new, lightweight Airflow component called the triggerer.

Existing Airflow operators have to be re-written according to the deferrable operator framework. In addition to supporting those available in the open source project, Astronomer has built an exclusive collection of deferrable operators in Runtime 4.0.0. This collection includes the `DatabricksSubmitRunOperator`, the `DatabricksRunNowOperator`, and the `ExternalTaskSensor`. These are designed to be drop-in replacements for corresponding operators currently in use.

As part of supporting deferrable operators, the triggerer is now available as a fully managed component on Astro. This means that you can start using deferrable operators in your DAGs as soon as you're ready. For more general information on deferrable operators, as well as how to use Astronomer's exclusive deferrable operators, read [Deferrable operators](https://docs.astronomer.io/learn/deferrable-operators).

## Astro Runtime 3.0.4

- Release date: October 26, 2021
- Airflow version: 2.1.1

### Bug fixes

- Fixed an issue where worker pods were stuck in a terminating state when scaling down (backported from Runtime 4.0.1)

## Astro Runtime 3.0.3

- Release date: September 22, 2021
- Airflow version: 2.1.1

### Bug fixes

- Fixed an issue where requests to Airflow's REST API with a temporary authentication token failed
- Fixed an issue introduced in Runtime 3.0.2 where `astro dev` commands in the Astro CLI did not execute correctly

## Astro Runtime 3.0.2

- Release date: September 17, 2021
- Airflow version: 2.1.1

### Bug fixes

- Fixed a series of issues that prevented task logs from appearing in the Airflow UI by implementing a custom task logging handler that does not interfere with AWS credentials or connections configured by users

## Astro Runtime 3.0.1

- Release date: September 1, 2021
- Airflow version: 2.1.1

### Additional improvements

- Upgraded the default Python version to `3.9.6`
- Added a link to Astro documentation in the Airflow UI

### Bug fixes

- Removed nonfunctional security and user profile elements from the Airflow UI
- The Airflow UI now shows the correct version of Astro Runtime in the footer

## Astro Runtime 3.0.0

- Release date: August 12, 2021
- Airflow version: 2.1.1

### Additional improvements

- The webserver is now the only Airflow component with access to logs, which reduces the risk of exposing sensitive information in logs ([commit](https://github.com/apache/airflow/pull/16754))
- Added support for Python 3.9 ([commit](https://github.com/apache/airflow/pull/15515))
- `token` keys in connections are now marked as masked by default ([commit](https://github.com/apache/airflow/pull/16474))

### Bug fixes

- Fixed module vulnerabilities exposed by `yarn audit` ([commit](https://github.com/apache/airflow/pull/16440))
- Fixed an issue where tasks would fail when running with `run_as_user` ([commit](https://github.com/astronomer/airflow/commit/075622cbe))
- Fixed an issue where tasks would fail when running with `CeleryKubernetesExecutor` ([commit](https://github.com/astronomer/airflow/commit/90aaf3d48))
