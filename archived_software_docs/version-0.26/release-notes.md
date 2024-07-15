---
title: 'Astronomer v0.26 Release Notes'
sidebar_label: 'Release Notes'
id: release-notes
description: Astronomer Software release notes.
---

## Overview

This document includes all release notes for Astronomer Software v0.26.

Astronomer v0.27 is the latest Stable version of Astronomer Software, while v0.28 remains the latest long-term support (LTS) version. To upgrade to Astronomer v0.26 from v0.25, read [Upgrade to v0.26](upgrade-astronomer.md). For more information about Software release channels, read [Release and Lifecycle Policies](release-lifecycle-policy.md).

We're committed to testing all Astronomer Software versions for scale, reliability and security on Amazon EKS, Google GKE and Azure AKS. If you have any questions or an issue to report, don't hesitate to [reach out to us](https://support.astronomer.io).

## 0.26.7

Release date: March 1, 2022

### Additional improvements

- Fixed several CVEs
- Updated documentation links in the UI to point to Software documentation

## 0.26.6

Release date: January 10, 2022

### Bug Fixes

- Fixed an issue where users could not create Deployments via an IAM role

## 0.26.5

Release date: December 11, 2021

### Bug Fixes

- Remediated [CVE-2021-44228](https://github.com/advisories/GHSA-jfh8-c2jp-5v3q) related to Log4J by setting ES_JAVA_OPTS=-Dlog4j2.formatMsgNoLookups=true at runtime for all ElasticSearch containers

## 0.26.4

Release date: November 22, 2021

### Support for Apache Airflow®® 2.2.0

[Apache Airflow® 2.2.0](https://airflow.apache.org/blog/airflow-2.2.0/) is an exciting milestone in the open source project. Most notably, this release introduces custom timetables and deferrable operators.

#### Custom Timetables

Timetables are a powerful new framework that you can use to create custom schedules using Python. In an effort to provide more flexibility and address known limitations imposed by cron, timetables use an intuitive `data_interval` that, for example, allows you to schedule a DAG to run daily on Monday through Friday, but not on the weekend. Timetables can be easily plugged into existing DAGs, which means that it's easy to create your own or use community-developed timetables in your project.

For more information on using timetables, read the [Apache Airflow® Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/timetable.html).

#### Deferrable Operators

Deferrable operators are a new type of Airflow operator that promises improved performance and lower resource costs. While standard operators and sensors take up a Worker or Scheduler slot even when they are waiting for an external trigger, deferrable operators are designed to suspend themselves and free up that Worker or Scheduler slot while they wait. This is made possible by a new, lightweight Airflow component called the Triggerer.

As part of supporting deferrable operators, you can provision multiple Triggerers on your Astronomer Deployments. By provisioning multiple Triggerers, you can ensure that tasks using Deferrable Operators are run even when one Triggerer goes down. For more information about configuring Triggerers and other resources, see [Configure a Deployment](configure-deployment.md).

### CLI Verbosity Flag

You can now specify a `--verbosity` flag for all Astronomer CLI commands. When you specify this flag with a CLI command, the CLI prints out [Logrus](https://github.com/sirupsen/logrus) logs as the command runs. This is useful for debugging any errors that might result from a CLI command.

The flag prints out different levels of logs depending on the value that you pass it. Each possible value (`debug`, `info`, `warn`, `error`, `fatal`, and `panic`) maps to a different Logrus logging level. For more information about these logging levels, read the [Logrus documentation](https://github.com/sirupsen/logrus#level-logging).

### Minor Improvements

- You can now create a custom set of cluster-level permissions for the Astronomer Commander service by setting `astronomer.global.clusterRoles: false` in your `config.yaml` file and pushing a new [RoleBinding](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) to a [pre-created Kubernetes namespace](pre-create-namespaces.md).
- In the `astronomer.houston.config` section of your `config.yaml` file, you can now configure a list of `allowedSystemLevelDomains []`. If you configure this list, only users with emails from domains specified in the list (for example, `<company>.com`) can be granted System Admin privileges.
- Greatly improved load times for the **System Admin** page in the UI.
- You can now specify a node port for 3rd party ingress controllers with a service type of `nodePort`.
- The naming format of service account pods has been changed from `<release-name>-dags-prod-worker-serviceaccount` to `release_name-dags-prod-airflow-worker`.

### Bug Fixes

- Fixed an issue where you could not update an existing Deployment's IAM role via the Astronomer CLI
- Fixed an issue where Deployments would not work on clusters with custom domains
- Fixed error handling when interacting with a Deployment that wasn't fully spun up
- Added a new validation step for Airflow Helm chart values configured in the `astronomer.houston.config.deployments.helm.airflow` section of `config.yaml`
