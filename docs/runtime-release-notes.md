---
sidebar_label: 'Astronomer Runtime'
title: 'Astronomer Runtime Release Notes'
id: runtime-release-notes
---

## Overview

Astronomer Runtime is a Docker image built and published by Astronomer that extends the Apache Airflow project to provide a differentiated experience. This document provides a summary of all changes made to each available version of Astronomer Runtime.

For instructions on how to upgrade, read [Upgrade Astronomer Runtime](upgrade-runtime.md). For general product release notes, go to [Astronomer Cloud Release Notes](release-notes.md). If you have any questions or a bug to report, don't hesitate to reach out to us via Slack or [support@astronomer.io](mailto:support@astronomer.io).

## Astronomer Runtime 4.0.7

- Release date: December 15, 2021
- Airflow version: 2.2.2

### Heartbeat DAG

Astronomer Runtime 4.0.7 includes a health monitoring DAG installed directly into the image itself. The `astronomer_monitoring_dag` emits a heartbeat every 5 minutes to check that your Deployment's schedulers and workers are healthy. If this heartbeat fails twice in a row, it sends an alert about the Deployment's health to the Astronomer UI.

Because this DAG is an essential component of Astronomer's observability tooling,  your organization will not be charged for its task runs. For the same reasons, this DAG cannot be modified or disabled via the Airflow UI. To change the frequency of the DAG's heartbeat, you can specify a cron job in the `AIRFLOW_MONITORING_DAG_SCHEDULE_INTERVAL` environment variable. 

## Astronomer Runtime 4.0.6

- Release date: December 2, 2021
- Airflow version: 2.2.2

### Additional Improvements

- User-supplied `airflow.cfg` files are no longer valid in Astronomer projects. [Environment variables](environment-variables.md) are now the only valid method for setting Airflow configuration options.

### Bug Fixes

- Fixed an issue where the **Browse** menu of the Airflow UI was hidden in some versions of Astronomer Runtime

## Astronomer Runtime 4.0.5

- Release date: November 29, 2021
- Airflow version: 2.2.2

### Bug Fixes

- Fixed an issue where Astronomer Cloud's S3 logging hook prevented users from setting up S3 as a custom XCom backend

## Astronomer Runtime 4.0.4

- Release date: November 19, 2021
- Airflow version: 2.2.2

### Bug Fixes

- Fixed an issue where DAG run and task instance records didn't show up as expected in the Airflow UI

## Astronomer Runtime 4.0.3

- Release date: November 15, 2021
- Airflow version: 2.2.2

### Additional Improvements

- Added support for [Airflow 2.2.2](https://airflow.apache.org/docs/apache-airflow/stable/changelog.html#airflow-2-2-2-2021-11-15), which includes a series of bug fixes for timetables, DAG scheduling, and database migrations. Most notably, it resolves an issue where some DAG runs would be missing in the Airflow UI if `catchup=True` was set.

### Bug Fixes

- Fixed an issue where the Astronomer-themed Airflow UI was not present in local development

## Astronomer Runtime 4.0.2

- Release date: October 29, 2021
- Airflow version: 2.2.1

### Additional Improvements

- Added support for [Airflow 2.2.1](https://airflow.apache.org/docs/apache-airflow/stable/changelog.html#airflow-2-2-1-2021-10-29), which includes a series of bug fixes that address intermittent problems with database migrations from Airflow 2.1 to Airflow 2.2

## Astronomer Runtime 4.0.1

- Release date: October 26, 2021
- Airflow version: 2.2.0

### Bug Fixes

- Fixed an issue where worker pods were stuck in a terminating state when scaling down
- Fixed an issue where the Airflow UI navbar and footer did not show the correct running version of Astronomer Runtime

## Astronomer Runtime 4.0.0

- Release date: October 12, 2021
- Airflow version: 2.2.0

### Support for Airflow 2.2.0

Astronomer Runtime 4.0.0 is a significant release that supports and enhances [Apache Airflow 2.2.0](https://airflow.apache.org/blog/airflow-2.2.0/), an exciting milestone in the open source project. Most notably, this release introduces custom timetables and deferrable operators.

#### Custom Timetables

Timetables represent a powerful new framework that allows Airflow users to create custom schedules using Python. In an effort to provide more flexibility and address known limitations imposed by cron, timetables use an intuitive `data_interval` that, for example, allows you to schedule a DAG to run daily on Monday through Friday, but not on the weekend. Timetables can be easily plugged into existing DAGs, which means that it's easy to create your own or use community-developed timetables in your project.

In addition to supporting the timetables framework, the team at Astronomer has built a `TradingHoursTimetable` that's ready to use in Runtime 4.0.0. You can use this timetable to run a DAG based on whether or not a particular global market is open for trade.

For more information on using timetables, read the [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/timetable.html).

#### Deferrable Operators

[Deferrable operators](https://airflow.apache.org/docs/apache-airflow/stable/concepts/deferring.html) are a new type of Airflow operator that promises improved performance and lower resource costs. While standard operators and sensors take up a Worker slot even when they are waiting for an external trigger, deferrable operators are designed to suspend themselves and free up that Worker slot while they wait. This is made possible by a new, lightweight Airflow component called the Triggerer.

Existing Airflow operators have to be re-written according to the deferrable operator framework. In addition to supporting those available in the open source project, Astronomer has built an exclusive collection of deferrable operators in Runtime 4.0.0. This collection includes the `DatabricksSubmitRunOperator`, the `DatabricksRunNowOperator`, and the `ExternalTaskSensor`. These are designed to be drop-in replacements for corresponding operators currently in use.

As part of supporting deferrable operators, the Triggerer is now available as a fully managed component on Astronomer Cloud. This means that you can start using deferrable operators in your DAGs as soon as you're ready. For more general information on deferrable operators, as well as how to use Astronomer's exclusive deferrable operators, read [Deferrable Operators](deferrable-operators.md).

## Astronomer Runtime 3.0.4

- Release date: October 26, 2021
- Airflow version: 2.1.1

### Bug Fixes

- Fixed an issue where worker pods were stuck in a terminating state when scaling down (backported from Runtime 4.0.1)

## Astronomer Runtime 3.0.3

- Release date: September 22, 2021
- Airflow version: 2.1.1

### Bug fixes

- Fixed an issue where requests to Airflow's REST API with a temporary authentication token failed
- Fixed an issue introduced in Runtime 3.0.2 where `astro dev` commands in the Astronomer CLI did not execute correctly

## Astronomer Runtime 3.0.2

- Release date: September 17, 2021
- Airflow version: 2.1.1

### Bug fixes

- Fixed a series of issues that prevented task logs from appearing in the Airflow UI by implementing a custom task logging handler that does not interfere with AWS credentials or connections configured by users

## Astronomer Runtime 3.0.1

- Release date: September 1, 2021
- Airflow version: 2.1.1

### Additional improvements

- Upgraded the default Python version to `3.9.6`
- Added a link to Astronomer Cloud documentation in the Airflow UI

### Bug fixes

- Removed nonfunctional security and user profile elements from the Airflow UI
- The Airflow UI now shows the correct version of Astronomer Runtime in the footer

## Astronomer Runtime 3.0.0

- Release date: August 12, 2021
- Airflow version: 2.1.1

### Additional improvements

- The Webserver is now the only Airflow component with access to logs, which reduces the risk of exposing sensitive information in logs ([commit](https://github.com/apache/airflow/pull/16754))
- Added support for Python 3.9 ([commit](https://github.com/apache/airflow/pull/15515))
- `token` keys in connections are now marked as masked by default ([commit](https://github.com/apache/airflow/pull/16474))

### Bug fixes

- Fixed module vulnerabilities exposed by `yarn audit` ([commit](https://github.com/apache/airflow/pull/16440))
- Fixed an issue where tasks would fail when running with `run_as_user` ([commit](https://github.com/astronomer/airflow/commit/075622cbe))
- Fixed an issue where tasks would fail when running with `CeleryKubernetesExecutor` ([commit](https://github.com/astronomer/airflow/commit/90aaf3d48))
