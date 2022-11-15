---
sidebar_label: 'Astro Runtime'
title: 'Astro Runtime release notes'
id: runtime-release-notes
toc_min_heading_level: 2
---

<head>
  <meta name="description" content="This is where you’ll find information about the latest Astro Runtime features and functionality. Astro Runtime is a Docker image built by Astronomer that provides a differentiated Apache Airflow experience and execution framework." />
  <meta name="og:description" content="This is where you’ll find information about the latest Astro Runtime features and functionality. Astro Runtime is a Docker image built by Astronomer that provides a differentiated Apache Airflow experience and execution framework." />
</head>

<!--version-specific-->

Astro Runtime is a Docker image built and published by Astronomer that extends the Apache Airflow project to provide a differentiated data orchestration experience. This document provides a summary of changes made to each available version of Astro Runtime. Note that some changes to Runtime might be omitted based on their availability in Astro.

To upgrade Astro Runtime, see [Upgrade Astro Runtime](upgrade-runtime.md). For general product release notes, see [Astro Release Notes](release-notes.md). If you have any questions or a bug to report, contact [Astronomer support](https://cloud.astronomer.io/support).

## Astro Runtime 6.0.4

- Release date: November 14, 2022
- Airflow version: 2.4.3

### ARM64-based images for faster local development with Apple M1

:::caution

To deploy a project using Astro Runtime 6.0.4 from an Apple M1 computer to Astro, you must use Astro CLI version 1.4.0 or later or else the deploy will fail. See [Install the CLI](install-cli.md).

:::

Astro Runtime images now support both AMD64 and ARM64 processor architectures for local development. When you install Astro Runtime 6.0.4 or later, Docker automatically runs the correct architecture based on the computer you're using.

If you run the Astro CLI on a Mac computer that uses an ARM-based [Apple M1 Silicon chip](https://www.apple.com/newsroom/2020/11/apple-unleashes-m1/), you will see a significant performance improvement when running Airflow locally. For example, the time it takes to run `astro dev start` on average has decreased from over 5 minutes to less than 2 minutes.

For more information on developing locally with the Astro CLI, see [Develop a Project](develop-project.md)

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

Astro Runtime 6.0.2 includes the following bug fixes:

- Remove DAG parsing from StandardTaskRunner ([#26750](https://github.com/apache/airflow/pull/26750))
- Fix airflow tasks run --local when dags_folder differs from that of processor ([#26509](https://github.com/apache/airflow/pull/26509))
- Add fixture for CLI tests requiring sample dags ([#26536](https://github.com/apache/airflow/pull/26536))

These changes were backported from Apache Airflow 2.4.2, which is not yet generally available.

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

- The Cloud UI no longer shows source code for [supported Airflow operators](data-lineage-support-and-compatibility.md#supported-airflow-operators) by default. To reenable this feature for a given Deployment, create an [environment variable](environment-variables.md) with a key of `OPENLINEAGE_AIRFLOW_DISABLE_SOURCE_CODE` and a value of `False`.
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

- Rlease date: May 9, 2022
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
    - [CVE-2022-5197](https://avd.aquasec.com/nvd/2022/cve-2022-5197/)
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

- Bump the [`openlineage-airflow` provider package](https://openlineage.io/integration/apache-airflow/) to `v0.6.2`

## Astro Runtime 4.2.0

- Release date: March 10, 2022
- Airflow version: 2.2.4

### New Astronomer Providers package

The `astronomer-providers` package is now installed on Astro Runtime by default. This package is an open source collection of Apache Airflow providers and modules that is maintained by Astronomer. It includes deferrable versions of popular operators such as `ExternalTaskSensor`, `DatabricksRunNowOperator`, and `SnowflakeOperator`.

For more information, see [Deferrable operators](https://docs.astronomer.io/learn/deferrable-operators). To access the source code of this package, see the [Astronomer Providers GitHub repository](https://github.com/astronomer/astronomer-providers).

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

These are all [deferrable operators](https://docs.astronomer.io/learn/deferrable-operators) built by Astronomer and available exclusively on Astro Runtime. They are pre-installed into the Astro Runtime Docker image and ready to use.

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
