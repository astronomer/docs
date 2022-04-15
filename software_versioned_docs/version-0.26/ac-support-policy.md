---
title: 'Astronomer Certified Versioning and Support'
sidebar_label: 'Versioning and Support Policy'
id: ac-support-policy
description: Versioning and lifecycle policy for Astronomer Certified, Astronomer's Apache Airflow offering.
---

## Overview

Astronomer Certified (AC) is a Debian-based, production-ready distribution of Apache Airflow that mirrors the open source project and undergoes additional levels of rigorous testing conducted by our team. New versions of AC are issued regularly based on Apache Airflow's community release schedule.

This Docker image is hosted on [Astronomer's Docker Registry](https://quay.io/repository/astronomer/ap-airflow?tab=tags) and allows you to run Airflow on Astronomer. All projects require that you specify an AC image in your `Dockerfile`.

This document provides information on the following:

- How AC is versioned
- Which versions of AC are currently available
- The maintenance schedule and end-of-maintenance date for all versions

For guidelines on how to upgrade, read [Upgrade Apache Airflow on Astronomer](manage-airflow-versions.md).

## Release Channels

To meet the unique needs of different operating environments, Astronomer Certified (AC) versions are associated with the following release channels:

- **Stable:** Includes the latest Astronomer and Apache Airflow features, available on release
- **Long-term Support (LTS):** Includes additional testing, stability, and maintenance for a core set of features

All releases of AC are considered stable. The LTS release channel is a subset of the stable release channel that promises additional stability, reliability, and support from our team.

For users that want to keep up with the latest Astronomer and Airflow features on an incremental basis, we recommend upgrading to new versions of AC as soon as they are made generally available. This should be regardless of release channel. New versions of AC are issued regularly and depend on the Apache Airflow community release schedule.

For customers looking for less frequent upgrades and functional changes, we recommend following the LTS release channel exclusively.

## Versioning Scheme

Astronomer Certified follows [Semantic Versioning](https://semver.org/). This means that Astronomer ships Major, Minor, and Patch releases of AC in the format of `major.minor.patch-hotfix`.

- **Major** versions are released for significant feature additions, including backward-incompatible changes to an API or DAG specification.
- **Minor** versions are released for functional changes, including backward-compatible changes to an API or DAG specification.
- **Patch** versions are released for bug and security fixes that resolve incorrect behavior.
- **Hotfix** versions may include bug or security fixes not yet available in community releases of Apache Airflow.

For AC `2.1.3-5`, for example:

- Major = `2.`
- Minor = `.1`
- Patch = `.3`
- Hotfix = `-5`

An AC Docker image will be published for every major and minor version of Apache Airflow. For example, AC images that correspond with Apache Airflow 2.0, 2.1, 2.2 etc. will be available on Astronomer as they're released in the open source project.

It is considered safe to upgrade to minor and patch versions within a major version. Upgrade guidance for major and LTS versions is provided with each release. There is no relation between an AC release's version number and its release channel.

### Hotfix Versions

All hotfix releases of AC have a [corresponding changelog](https://github.com/astronomer/ap-airflow/blob/master/2.1.0/CHANGELOG.md) which specifies the date the hotfix was released and all individual changes made to it. Bugs that are reported by the wider Airflow community are often fixed in AC before they are fixed in the subsequent open source release.

For information on how to upgrade to the latest hotfix release, read [Upgrade to an AC Patch Version](manage-airflow-versions.md#patch-versions-of-astronomer-certified).

### Distribution

AC Docker images come in two variants:

- `quay.io/astronomer/ap-airflow:<version>-buster-onbuild`
- `quay.io/astronomer/ap-airflow:<version>-buster`

For example, the images for Astronomer Certified 2.1.0 would be:

- `quay.io/astronomer/ap-airflow:2.1.0-buster`
- `quay.io/astronomer/ap-airflow:2.1.0-buster-onbuild`

For the smoothest, out-of-the-box Airflow experience, we strongly recommend and default to `buster-onbuild` images in your project's `Dockerfile`. These images incorporate Docker ONBUILD commands to copy and scaffold your Airflow project directory so you can more easily pass those files to the containers running each core Airflow component.

For complex use cases that require customizing AC base image, read [Customize your Airflow Image on Astronomer](customize-image.md).

## Backport Policy for Bug and Security Fixes

If a major stability bug in Astronomer Certified  is identified by Astronomer, a fix will be backported to all LTS versions and only the latest stable version. For users on a stable version that is not latest, our team will recommend that you upgrade. Major issues in this category may result in significant delays in task scheduling as well as potential data loss.

If a major security issue is identified, a fix will be backported and made available as a new AC hotfix version for _all_ available stable and LTS releases. Major issues in this category are classified by a combination of impact and exploitability.

In rare instances, the Astronomer team may make an exception and backport a bug or security fix to a release that is beyond the commitment stated above. To submit a request for consideration, please reach out to your customer success manager.

## Astronomer Certified Maintenance Policy

The maintenance period for an Astronomer Certified version depends on its release channel:

| Release Channel | Maintenance Duration |
| --------------- | -------------------- |
| Stable          | 6 Months             |
| LTS             | 18 Months            |

For each `major.minor` pair, only the latest patch and hot-fix combination is supported at any given time. If you report an issue with an Astronomer Certified patch or hot-fix version that is not latest, the Astronomer Support team will always ask that you upgrade as a first step to resolution. For example, the Support team encourages any user who reports an issue with Astronomer Certified 2.2.2 to first upgrade to 2.2.3 as soon as it's generally available.

Within the maintenance window of each Astronomer Certified version, the following is true:

- A Python wheel and set of Docker images corresponding to that version are available for download via [Quay.io](http://quay.io), PyPi and [Downloads](https://www.astronomer.io/downloads).
- Astronomer will regularly publish hotfixes for bug or security issues identified as high priority.
- The Astronomer Support team will offer support for paying customers running a supported version of AC via the [Astronomer Support Portal](https://support.astronomer.io).
- A user can create a new Airflow Deployment via the Software UI, CLI, or API with any supported version of AC.

When the maintenance window for a version of AC ends, the following is true:

- The Astronomer Support team is not obligated to answer questions regarding an Airflow Deployment that is running that version.
- New Airflow Deployments cannot be created with that version of AC. Unsupported versions will _not_ render as an option in the Deployment creation process from the Software UI, API, or CLI.
- The latest version of the Astronomer CLI will show a warning if a user pushes a Docker image to Astronomer that corresponds to that version.

To ensure reliability, service will not be interrupted for Astronomer Deployments running a version of AC that is no longer supported. Unsupported versions will also continue to be available for local development and testing via the Astronomer CLI.

### End of Maintenance Date

Maintenance is discontinued the last day of the month for a given version. For example, if the maintenance window for a version of Astronomer Certified is January - June of a given year, that version will be maintained by Astronomer until the last day of June.

## Astronomer Certified Lifecycle Schedule

The following tables contain the exact lifecycle for each published version of Astronomer Certified. These timelines are based on the LTS and Stable release channel maintenance policies.

### Stable Releases

| AC Version                                                                                 | Release Date   | End of Maintenance Date|
| ------------------------------------------------------------------------------------------ | -------------- | -----------------------|
| [1.10.12](https://github.com/astronomer/ap-airflow/blob/master/1.10.12/CHANGELOG.md)       | Sep 30, 2020   | February 2022*         |
| [1.10.14](https://github.com/astronomer/ap-airflow/blob/master/1.10.14/CHANGELOG.md)       | Dec 10, 2020   | February 2022*         |
| [1.10.15](https://github.com/astronomer/ap-airflow/blob/master/1.10.15/CHANGELOG.md)  | March 19, 2021 | September 2022         |
| [2.0](https://github.com/astronomer/ap-airflow/blob/master/2.0.0/CHANGELOG.md)             | Dec 17, 2020   | February 2022*         |
| [2.1](https://github.com/astronomer/ap-airflow/blob/master/2.1.4/CHANGELOG.md)       | May 21, 2021   | November 2022          |
| [2.2](https://github.com/astronomer/ap-airflow/blob/master/2.2.0/CHANGELOG.md)             | Oct 12, 2021   | April 2022             |
| 2.3                                                                                  | April 2022 (Planned) | October 2022 (Planned)  |

> *Given the wide usage of AC 1.10.12, 1.10.14, and 2.0, Astronomer has extended the maintenance period for those versions through February 2022.

### LTS Releases

| AC Version                                                                                 | Release Date   | End of Maintenance Date |
| ------------------------------------------------------------------------------------------ | -------------- | ----------------------- |
| [1.10.15](https://github.com/astronomer/ap-airflow/blob/master/1.10.15/CHANGELOG.md) | March 19, 2021 | September 2022          |
| [2.1](https://github.com/astronomer/ap-airflow/blob/master/2.1.4/CHANGELOG.md)       | May 21, 2021   | November 2022           |

If you have any questions or concerns, reach out to [Astronomer Support](https://support.astronomer.io).
