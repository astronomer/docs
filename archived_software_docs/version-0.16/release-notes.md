---
title: 'Astronomer v0.16 Release Notes'
sidebar_label: 'Release Notes'
id: release-notes
description: Astronomer Software release notes.
---

## Notice on Astronomer Software Releases

This document includes all release notes for Astronomer Software v0.16.

For instructions on how to upgrade to the latest v0.16 patch version of Astronomer, read [Upgrade to a Stable Version of Astronomer](upgrade-astronomer-stable.md). If you're interested in upgrading from Astronomer v0.16.x to the latest LTS version of the platform, read [Upgrade to Astronomer Software v0.23](upgrade-to-0-23.md).

We're committed to testing all quarterly Astronomer Software versions for scale, reliability and security on EKS, GKE and AKS. If you have any questions or an issue to report, don't hesitate to [reach out to us]((https://support.astronomer.io).

## Astronomer v0.16

Latest Patch Release: **v0.16.15**

## 0.16.19

Release date: December 11, 2021

### Bug Fixes

- Remediated [CVE-2021-44228](https://github.com/advisories/GHSA-jfh8-c2jp-5v3q) related to Log4J by setting `ES_JAVA_OPTS=-Dlog4j2.formatMsgNoLookups=true` at runtime for all ElasticSearch containers

## v0.16.18

Release Date: November 3, 2021

### Bug Fixes

- Fixed a security issue where an internal API endpoint could be accessed by an unauthorized user with a specific event input

### v0.16.15

Release Date: January 5, 2021

#### Support for Apache Airflow®® 1.10.14

Airflow 1.10.14 was built to make testing and migration to [Airflow 2.0](https://www.astronomer.io/blog/introducing-airflow-2-0) as easy as possible. Highlights include:

- "Warning" to users with duplicate Airflow Connections ([commit](https://github.com/apache/airflow/commit/0e40ddd8e))
- Enable [DAG Serialization](https://airflow.apache.org/docs/apache-airflow/stable/dag-serialization.html) by default ([commit](https://github.com/apache/airflow/commit/8a265067e))
- Support for Airflow 2.0 CLI commands ([commit](https://github.com/apache/airflow/pull/12725))
- Bugfix: Unable to import Airflow plugins on Python 3.8 ([commit](https://github.com/apache/airflow/pull/12859))
- BugFix: Tasks with depends_on_past or task_concurrency are stuck ([commit](https://github.com/apache/airflow/pull/12663))
- Security Fix: Incorrect Session Validation in Airflow Webserver with default config allows a an authorized Airflow user on site A access an unauthorized Airflow Webserver on Site B through the session from Site A. ([Details](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-17526))

To upgrade to AC 1.10.14, add our new Debian image to your Dockerfile:

```
FROM quay.io/astronomer/ap-airflow:1.10.14-buster-onbuild
```

For detailed guidelines on how to upgrade Airflow on Astronomer, read [Upgrade Airflow](manage-airflow-versions.md). For more information on 1.10.14, check out the [Airflow Release](https://github.com/apache/airflow/releases/tag/1.10.14) or the corresponding [AC 1.10.14 changelog](https://github.com/astronomer/ap-airflow/blob/master/1.10.14/CHANGELOG.md).

> **Note:** In an effort to standardize our offering and optimize for reliability, we will only support a Debian-based image for AC 1.10.14. Alpine-based images for AC 1.10.5 - 1.10.12 will continue to be supported. For guidelines on how to migrate from Alpine, go to [Upgrade Apache Airflow®](manage-airflow-versions.md).

#### Support for latest Astronomer Certified Patch Releases

In addition to support for Airflow 1.10.14, Astronomer v0.16.15 also includes support for the latest patch versions of existing Astronomer Certified images:

- [1.10.12-2](https://github.com/astronomer/ap-airflow/blob/master/1.10.12/CHANGELOG.md)
- [1.10.10-6](https://github.com/astronomer/ap-airflow/blob/master/1.10.10/CHANGELOG.md)

For instructions on how to upgrade to the latest patch version of a release, refer to [Upgrade Airflow](manage-airflow-versions.md).

#### Support for Docker Images on Quay.io + DockerHub

Astronomer recently migrated from [Docker Hub](https://hub.docker.com/r/astronomerinc/ap-airflow/tags) to [Quay.io](https://quay.io/repository/astronomer/ap-airflow?tab=tags) as our platform’s primary Docker Registry in light of Docker Hub’s [new rate-limit policy](https://www.docker.com/blog/what-you-need-to-know-about-upcoming-docker-hub-rate-limiting/), effective Nov 2nd, 2020.

Astronomer v0.16.15 supports Docker images that are pulled from _either_ Docker registry, though we strongly encourage users to switch to Quay.io images to avoid rate limiting errors from Docker Hub. This change affects both Airflow images (`ap-airflow`) as well as all Docker images required to run the Astronomer platform, including `ap-grafana`, `ap-registry`, `ap-pgbouncer`, etc. If you're running a legacy Airflow image that pulls from `astronomerinc/ap-airflow`, for example, all it takes is modifying that image in your Dockerfile to read `quay.io/astronomer/ap-airflow`. Both have the exact same functionality.

For more information, refer to [Upgrade Apache Airflow on Astronomer](manage-airflow-versions.md) or [this forum post](https://forum.astronomer.io/t/docker-hub-rate-limit-error-toomanyrequests-you-have-reached-your-pull-rate-limit/887).

#### Bug Fixes & Improvements

- Improvement: Support Airflow's ["upgrade check"](https://airflow.apache.org/docs/apache-airflow/stable/upgrade-check.html) in the Astronomer CLI (`$ astro dev upgrade-check`) (_v0.16.5_)
- Improvement: Support for [Airflow 2.0 in the Astronomer CLI](https://www.astronomer.io/guides/get-started-airflow-2) (_v0.16.5_)

### v0.16.12

Release Date: November 16, 2020

#### Bug Fixes & Improvements

- BugFix: Typo in Pod Security Policy (PSP) for Private CA

### v0.16.11

Release Date: November 2, 2020

##### Bug Fixes & Improvements

- BugFix: Fix conditionally disabling subcharts

### v0.16.10

Release Date: October 30, 2020

#### Support for Custom CA Certificates

For users who rely on an internal Certificate Authority (CA), Astronomer now supports mounting custom CA certificates.

For guidelines, refer to our forum post on ["Using Private CAs on Astronomer"](https://forum.astronomer.io/t/using-private-cas-in-astronomer/753).

#### Bug Fixes & Improvements

- Improvement: New Houston API mutation that allows users to enable or disable KEDA (`updateDeploymentKedaConfig`)
- BugFix: Alerts from Astronomer not sent when an Airflow component breaches the resource threshold level defined in Prometheus

### v0.16.9

Release Date: October 8, 2020

#### Support for Apache Airflow® 1.10.12

Astronomer v0.16.9 comes with support for [Airflow 1.10.12](https://airflow.apache.org/blog/airflow-1.10.12/) in addition to 3 patch versions of previously released images.

Airflow 1.10.12 notably includes:

- The ability to configure and launch pods via YAML files with the Kubernetes Executor and KubernetesPodOperator ([commit](https://github.com/apache/airflow/pull/6230))
- A new `on_kill` method that ensures a KubernetesPodOperator task is killed when it's cleared in the Airflow UI ([commit](https://github.com/apache/airflow/commit/ce94497cc))
- Ability to define a custom XCom class ([commit](https://github.com/apache/airflow/pull/8560))
- Support for grabbing Airflow configs with sensitive data from Secret Backends ([commit](https://github.com/apache/airflow/pull/9645))
- Support for AirfowClusterPolicyViolation support in Airflow local settings ([commit](https://github.com/apache/airflow/pull/10282)).

For a detailed breakdown of all changes, refer to the [AC 1.10.12 Changelog](https://github.com/astronomer/ap-airflow/blob/master/1.10.12/CHANGELOG.md). For instructions on how to upgrade to 1.10.12 on Astronomer, refer to ["Airflow Versioning"](manage-airflow-versions.md).

> **Note:** AC 1.10.12 will be the _last_ version to support an Alpine-based image. In an effort to standardize our offering and optimize for reliability, we'll exclusively build, test and support Debian-based images starting with AC 1.10.13. A guide for how to migrate from Alpine to Debian coming soon.

#### Support for Latest Builds of Astronomer Certified

Astronomer v0.16.9 also includes support for:

- AC 1.10.10-5 ([Changelog](https://github.com/astronomer/ap-airflow/blob/master/1.10.10/CHANGELOG.md))

These patch releases include a fix to an identified security issue listed [here](https://www.astronomer.io/docs/ac/v1.10.10/get-started/security/).

#### Bug Fixes and Improvements

Two additional bugs were addressed in Astronomer v0.16.9:

- BugFix: IAM role integration fails with Debian Airflow Image on DAG run (`[Errno 13] Permission denied`)
- BugFix: Calling the `createWorkspace` Houston API mutation with a system Service Account returns an error (`No Node for the model User`)

### v0.16.8

Release Date: September 25, 2020

#### Export Logs from Fluentd to Amazon S3

Astronomer leverages [Fluentd](https://www.fluentd.org/) as a data collector that is responsible for scraping and cleaning Airflow task logs to then send to [Elasticsearch](https://www.elastic.co/elasticsearch/), a search engine used to centralize and index logs from Airflow. As of v0.16, Astronomer now supports a Fluentd to S3 plugin that allows users to forward Airflow logs to Amazon S3 while ensuring they're also sent to Elasticsearch and otherwise supported by the platform.

For step-by-step guidelines, refer to ["Forward Logs to S3"](logs-to-s3.md).

### v0.16.7

Release Date: September 9, 2020

#### Bug Fixes and Improvements

- BugFix: Adding a non-Airflow config Environment Variable on Software UI with KubernetesExecutor does not get passed successfully

### v0.16.6

Release Date: September 4, 2020

#### Allow Users to Define Custom Platform and Apache Airflow® Deployment-level Alerts in `config.yaml`

Astronomer v0.16.6 allows users to define custom alerts via the `config.yaml` file and successfully pass those to Prometheus, a monitoring tool that Astronomer uses to collect metrics from a variety of endpoints and push them to Grafana for visualization.

For example, you might want to add an Airflow alert to fire if a Deployment has been using over 50% of its pod quota for over 10 minutes or a Platform alert if more than 2 Airflow Schedulers don't heartbeat for more than 5 minutes. Here's what your `config.yaml` might look like:

```yaml
prometheus:
  additionalAlerts:
    airflow: |
      - alert: ExampleAirflowAlert
        expr: (sum by (release) (kube_resourcequota{resource="pods", type="used"}) / sum by (release) (kube_resourcequota{resource="pods", type="hard"})*100) > 50
        for: 10m
        labels:
          tier: airflow
          component: deployment
          workspace: {{ printf "%q" "{{ $labels.workspace }}" }}
          deployment: {{ printf "%q" "{{ $labels.deployment }}" }}
        annotations:
          summary: {{ printf "%q" "{{ $labels.deployment }} is near its pod quota" }}
          description: {{ printf "%q" "{{ $labels.deployment }} has been using over 50% of its pod quota for over 10 minutes." }}
    platform: |
      - alert: ExamplePlatformAlert
        expr: count(rate(airflow_scheduler_heartbeat{}[1m]) <= 0) > 2
        for: 5m
        labels:
          tier: platform
          severity: critical
        annotations:
          summary: {{ printf "%q" "{{ $value }} airflow schedulers are not heartbeating" }}
          description: "If more than 2 Airflow Schedulers are not heartbeating for more than 5 minutes, this alarm fires."
```

For more information on alerts that are generated by default, refer to our ["Alerts" doc](platform-alerts.md).

> **Note:** These alerts are NOT Airflow task-level alerts that require definition at the Airflow code level. For more information on how to set up `email_on_failure` within Airflow, for example, refer to our ["Airflow Alerts" doc](airflow-alerts.md).

#### Bug Fixes and Improvements

- Improvement: Collect kube-dns metrics and add corresponding dashboard in Grafana
- Improvement: Optimize DNS queries to reduce traffic by providing a pgbouncer FQDN suffixed by a period
- BugFix: Error on `$ astro dev init` if not authenticated to Astronomer: "Failed to get list of supported tags from Astronomer" (CLI v0.16.4)
- BugFix: `$ astro upgrade` incorrectly indicates that the user is running the latest version of the CLI if running < v0.10.0 of the CLI (CLI v0.16.4)
- BugFix: Environment Variable changes via the Software UI not consistently reflected in Workers and in underlying Kubernetes secrets
- BugFix: Incorrect Extra Capacity AU detected from Houston API
- BugFix: Port `prometheus-postgres-exporter` and `prometheus-node-exporter` pod security policy (PSP) logic under global `pspEnabled:` flag

### v0.16.5

Release Date: August 19, 2020

#### Support for Latest Builds of Astronomer Certified

Astronomer Software v0.16.5 includes support for the following patch releases of Astronomer Certified (AC), our distribution of Apache Airflow:

- [1.10.10-4](https://github.com/astronomer/ap-airflow/blob/master/1.10.10/CHANGELOG.md)

These patch releases most notably include:

- BugFix: Broken `/landing_times` view in the Airflow UI rendering with plain HTML ([commit](https://github.com/astronomer/airflow/commit/6567df3))
- BugFix: Tighten restriction for `apache-airflow` in requirements.txt to allow users to install other packages with that prefix ([commit](https://github.com/astronomer/ap-airflow/commit/c2536db))
- BugFix: Broken PapermillOperator (1.10.10 only).

For information on how to upgrade Astronomer Certified versions, refer to our ["Manage Airflow Versions" doc](manage-airflow-versions.md).

#### Airflow Chart: Improved Upgrade Process

Historically, upgrades to Astronomer (major, minor or patch) that have included a change to the Airflow Chart forcibly restart all Airflow Deployments running on the platform at the time of the upgrade, often causing task interruption.

This change allows for Airflow Deployments to remain unaffected through the upgrade and for Airflow Chart changes to take effect _only_ when another restart event is triggered by a user (e.g. a code push, Environment Variable change, resource or executor adjustment, etc).

More specifically, this changes the behavior of our API's `updateDeployment` mutation to perform the Airflow Helm Chart version upgrade only if/when a Houston config is updated.

#### Bug Fixes and Improvements

- BugFix: 400 Error on ` $ astro workspace user add` in Astronomer CLI (CLI v0.16.3)
- BugFix: 400 Error on ` $ astro workspace user remove` in Astronomer CLI (CLI v0.16.3)
- BugFix: Users able to create 2+ Service Accounts with the same label
- BugFix: Link to Workspace broken in 'SysAdmin' > 'Users' View
- BugFix: Navigating directly to the 'Metrics' Tab of the Software UI renders error
- BugFix: Adjust commander role to include KEDA CRD (fixes `could not get information about the resource: scaledobjects.keda.k8s.io` on Airflow Deployment creation)

### v0.16.4

Release Date: July 22, 2020

- BugFix: Restore ability to dynamically pull namespace with `namespace=default` in [KubernetesPodOperator] and KubernetesExecutor Config
- BugFix: Error on `$ astro dev init` and `$ astro version` if not authenticated to Astronomer (CLI v0.16.2)

### v0.16.3

Release Date: July 22, 2020

- Improvement: Allow SysAdmins to Access Workspaces in the Astro UI
- Improvement: Create new critical severity alerts for platform system components
- BugFix: Emails caps-sensitive in error for ADFS
- BugFix: Mismatched rendering when switching between Deployments in the Astro UI

### v0.16.1

Release Date: July 9, 2020

- BugFix: 'Metrics' Tab in the Astro UI unresponsive with large task payload
- BugFix: Error when deleting a 'Pending' Workspace invite in Astro UI
- BugFix: "Deployment Status" bubble in the Astro UI persistently blue/pulsating
- BugFix: Issue with Extra Capacity resetting every time you change an Env Var

### v0.16.0

Release Date: June 29, 2020

#### New "Environment Variables" Tab in the Software UI

Astronomer v0.16 comes with significant improvements to the experience of setting Environment Variables on Astronomer. Namely, we've introduced a dedicated 'Variables' tab, lessening the density of the "Settings" page and making these configurations accessible to "Trial" users on Astro.

With the new tab comes the ability for Workspace Admins and Editors to create and mark a value as 'secret', permanently hiding the value from the Software UI (and from the client). From the same tab, users can now export Environment Variables as 'JSON' as well.

For more details on this new feature, reference our ["Environment Variables" doc](environment-variables.md).

#### Support for AD FS

Astronomer v0.16 for Astronomer Software users comes with support for Microsoft's [Active Directory Federation services (AD FS)](https://docs.microsoft.com/en-us/windows-server/identity/active-directory-federation-services), as an alternative authentication system.

To learn more, reference ["Auth Systems on Astronomer"](integrate-auth-system.md).

#### Bug Fixes and Improvements

- BugFix: Add Alphanumeric characters (e.g. S3)to Environment Variable validation in the Astro UI
- BugFix: ExtraCapacity values (over minimum) are overridden in Deployment Update
- Improvement: Simplify `updateUser` Mutation in Houston API (remove `uuid`)
- Security: Implement platform-wide Pod Security Policies
- Security: Clear Javascript CVEs
- BugFix: "Airflow State" dashboard in Grafana broken
- BugFix: CLI Install command should point to BASEDOMAIN (not `install.astronomer.io`) for Software users
- BugFix: SysAdmin can't revoke SysAdmin permissions from another user

## Astronomer v0.15

Release Date: June 8, 2020

### v0.15.0

#### Support for Airflow 1.10.10

As of v0.15, Astronomer users can run the Astronomer Certified (AC) 1.10.10 image, which is based on the [Airflow 1.10.10](https://airflow.apache.org/blog/airflow-1.10.10/) open source version released in early April.

Airflow 1.10.10 notably includes the ability to choose a timezone in the Airflow UI, DAG Serialization functionality for improved Webserver performance, and the [ability to sync Airflow Connections and Variables](https://forum.astronomer.io/t/aws-parameter-store-as-secrets-backend-airflow-1-10-10/606) with a Secret Backend tool (e.g. AWS Secret Manager, Hashicorp Vault, etc.)

For more detail on what's included in AC 1.10.10, reference the [changelog](https://github.com/astronomer/ap-airflow/blob/master/1.10.10/CHANGELOG.md).

#### Ability to Set Custom Release Names

As of Astronomer v0.15, Software customers can now customize the release name of any Airflow Deployment instead of relying on the default naming scheme (e.g. `solar-galaxy-1234`). Release names within a single cluster must be unique and will continue to be immutable following creation.

To activate this feature on the platform, refer to the `manualReleaseNames` value in your `config.yaml`.

#### Ability to Annotate Pods to integrate with IAM Roles

As of Astronomer v0.15, IAM roles can now be appended to all pods within any individual Airflow Deployment on the platform. Users who integrate Airflow with some resource or set of resources (e.g. an AWS S3 bucket or Secret Backend) can now configure them to be accessible only to a subset of Kubernetes pods within your wider Astronomer cluster.

Leverage this feature by specifying an existing IAM role `arn` when you create or update an Airflow Deployment via the Astronomer CLI. For guidelines, go [here](integrate-iam.md).

#### Bug Fixes & Improvements

A few notable bug fixes and improvements:

* Ability to add multiple email addresses to receive deployment-level alerts
* Security improvements to the Software UI
* Reframe "Extra Capacity" in the 'Deployment Configuration' tab of the Software UI
* Improved error handling for users who sign up with an email different than their input in our trial form
* Bug Fix: Warning via the CLI on Debian images
* Bug Fix: "Failed to authenticate to the registry..." error on v0.13 of the CLI
* Added support for AWS S3 Registry Backend
* New UI warning when SMTP credentials are not configured and email invites cannot be sent
* Improved UX of Failed Network Connections
* Bug Fix: Missing "Deployment" label in Airflow Alerts
