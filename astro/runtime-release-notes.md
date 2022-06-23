---
sidebar_label: 'Astro Runtime'
title: 'Astro Runtime release notes'
id: runtime-release-notes
description: Release notes for Astro Runtime, the differentiated Apache Airflow experience and execution framework.
---

## Overview

Astro Runtime is a Docker image built and published by Astronomer that extends the Apache Astro project to provide a differentiated data orchestration experience. This document provides a summary of all changes made to each available version of Astro Runtime.

For instructions on how to upgrade, read [Upgrade Astro Runtime](upgrade-runtime.md). For general product release notes, go to [Astro Release Notes](release-notes.md). If you have any questions or a bug to report, reach out to [Astronomer support](https://support.astronomer.io).

## Astro Runtime 5.0.4

- Release date: June 15, 2022
- Airflow version: 2.3.2

### Additional improvements

- Update `astronomer-providers` to v1.5.0. For more information, see the [Astronomer Providers Changelog](https://astronomer-providers.readthedocs.io/en/stable/changelog.html#id1).
- Add support for Astro clusters with [Istio](https://istio.io/) enabled.

## Astro Runtime 5.0.3

- Release date: June 4, 2022
- Airflow version: 2.3.2

### Support for Airflow 2.3.2

Astro Runtime 5.0.3 includes same-day support for Airflow 2.3.2, a release that follows Airflow 2.3.1 with a collection of bug fixes.

Fixes include:

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

### Support for Airflow 2.3.1

Astro Runtime 5.0.2 includes same-day support for Airflow 2.3.1, a release that follows Airflow 2.3.0 with a collection of bug fixes.

Fixes include:

- Automatically reschedule stalled queued tasks in Celery executor ([#23690](https://github.com/apache/airflow/pull/23690))
- Fix secrets rendered in Airflow UI when task is not executed ([#22754](https://github.com/apache/airflow/pull/22754))
- Performance improvements for faster database migrations to Airflow 2.3

For more information, see the [Apache Airflow changelog](https://github.com/apache/airflow/releases/tag/2.3.1).

### Additional improvements

- Update `astronomer-providers` to v1.3.1. For more information, see the [Astronomer Providers Changelog](https://astronomer-providers.readthedocs.io/en/stable/changelog.html#id5).
- Update `openlineage-airflow` to v0.8.2. For more information, see the [OpenLineage GitHub repository](https://github.com/OpenLineage/OpenLineage/tree/main/integration/airflow).

## Astro Runtime 5.0.1

- Rlease date: May 9, 2022
- Airflow version: 2.3.0

### Astronomer Providers 1.2.0

Astro Runtime 5.0.1 includes v1.2.0 of the `astronomer-providers` package ([CHANGELOG](https://astronomer-providers.readthedocs.io/en/stable/)). This release includes 5 new [deferrable operators](deferrable-operators.md):

    - `DataprocSubmitJobOperatorAsync`
    - `EmrContainerSensorAsync`
    - `EmrStepSensorAsync`
    - `EmrJobFlowSensorAsync`
    - `LivyOperatorAsync`

To access the source code of this package, visit the [Astronomer Providers GitHub repository](https://github.com/astronomer/astronomer-providers).

### Additional improvements

- Improved performance when upgrading to Astro Runtime 5.0.x
- Bumped the [`openlineage-airflow` dependency](https://openlineage.io/integration/apache-airflow/) to `v0.8.1`

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

For more information about deferrable operators and how to use them, see [deferrable operators](deferrable-operators.md). To access the source code of this package, see the [Astronomer Providers GitHub repository](https://github.com/astronomer/astronomer-providers).

### Additional improvements

- Bump the [`openlineage-airflow` provider package](https://openlineage.io/integration/apache-airflow/) to `v0.6.2`

## Astro Runtime 4.2.0

- Release date: March 10, 2022
- Airflow version: 2.2.4

### New Astronomer Providers package

The `astronomer-providers` package is now installed on Astro Runtime by default. This package is an open source collection of Apache Airflow providers and modules that is maintained by Astronomer. It includes deferrable versions of popular operators such as `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`.

For more information, see [deferrable operators](deferrable-operators.md). To access the source code of this package, see the [Astronomer Providers GitHub repository](https://github.com/astronomer/astronomer-providers).

### Additional improvements

- Bump the [`openlineage-airflow` provider package](https://openlineage.io/integration/apache-airflow/) to `v0.6.1`

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

These are all [deferrable operators](deferrable-operators.md) built by Astronomer and available exclusively on Astro Runtime. They are pre-installed into the Astro Runtime Docker image and ready to use.

### Additional improvements

- The Airflow UI now shows the Deployment's Docker image tag in the footer of all pages. For more information, see [Astro Release Notes for March 10, 2022](release-notes.md#march-10-2022).

### Additional improvements

- To support an enhanced logging experience on Astro, the `apache-airflow-providers-elasticsearch` provider package is now installed by default.

## Astro Runtime 4.0.9

- Release date: January 19, 2022
- Airflow version: 2.2.3

### Additional improvements

- The [`openlineage-airflow` provider package](https://openlineage.io/integration/apache-airflow/) is now installed in Runtime by default.

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

[Deferrable operators](https://airflow.apache.org/docs/apache-airflow/stable/concepts/deferring.html) are a new type of Airflow operator that promises improved performance and lower resource costs. While standard operators and sensors take up a worker slot even when they are waiting for an external trigger, deferrable operators are designed to suspend themselves and free up that worker slot while they wait. This is made possible by a new, lightweight Airflow component called the triggerer.

Existing Airflow operators have to be re-written according to the deferrable operator framework. In addition to supporting those available in the open source project, Astronomer has built an exclusive collection of deferrable operators in Runtime 4.0.0. This collection includes the `DatabricksSubmitRunOperator`, the `DatabricksRunNowOperator`, and the `ExternalTaskSensor`. These are designed to be drop-in replacements for corresponding operators currently in use.

As part of supporting deferrable operators, the triggerer is now available as a fully managed component on Astro. This means that you can start using deferrable operators in your DAGs as soon as you're ready. For more general information on deferrable operators, as well as how to use Astronomer's exclusive deferrable operators, read [deferrable operators](deferrable-operators.md).

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
