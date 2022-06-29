---
title: "Astro Runtime versioning and lifecycle policy"
sidebar_label: "Versioning and lifecycle policy"
id: runtime-version-lifecycle-policy
description: Learn how Astronomer releases and maintains Astro Runtime, the core component that powers a differentiated Apache Airflow experience on Astro.
---

## Overview

Astro Runtime is a Debian-based, production-ready distribution of Apache Airflow that extends the open source project to provide you with differentiated functionality that centers around reliability, efficiency, and performance.

Astro Runtime Docker images are hosted on [Astronomer's Docker registry](https://quay.io/repository/astronomer/astro-runtime) and enable Airflow on Astro. All Astro projects require that you specify an Astro Runtime image in your `Dockerfile`, and all Deployments on Astro must run only one version of Runtime. Every version of Astro Runtime correlates to one version of Apache Airflow. Depending on the needs of your pipelines, you can run different versions of Astro Runtime on different Deployments within a given Workspace or cluster.

This document provides information on the following:

- How Runtime is versioned
- Which versions of Runtime are currently available
- The maintenance schedule and end-of-maintenance date for all versions

For guidelines on how to upgrade to a new version of Runtime, see [Upgrade Runtime](upgrade-runtime.md). For a summary of each version's changes, see [Runtime Release Notes](runtime-release-notes.md).

## Release channels

To meet the unique needs of different operating environments, Astro Runtime versions are associated with the following release channels:

- **Stable:** Includes the latest Astronomer and Apache Airflow features, available on release
- **Long-term Support (LTS):** Includes additional testing, stability, and maintenance for a core set of features

All releases of Astro Runtime are considered stable. The LTS release channel is a subset of the stable release channel that promises additional stability, reliability, and support from our team.

For users that want to keep up with the latest Astronomer and Airflow features on an incremental basis, we recommend upgrading to new versions of Astro Runtime as soon as they are made generally available. This should be regardless of release channel. New versions of Runtime are issued regularly and include timely support for the latest major, minor, and patch versions of Airflow.

For customers looking for less frequent upgrades and functional changes, we recommend following the LTS release channel exclusively.

## Versioning scheme

Astro Runtime follows [Semantic Versioning](https://semver.org/). This means that Astronomer ships major, minor, and patch releases of Runtime in the format of `major.minor.patch`.

- **Major** versions are released for significant feature additions, including backward-incompatible changes to an API or DAG specification.
- **Minor** versions are released for functional changes, including backward-compatible changes to an API or DAG specification.
- **Patch** versions are released for bug and security fixes that resolve incorrect behavior.

For Runtime `4.0.6`, for example:

- Major = `4.`
- Minor = `.0`
- Patch = `.6`

A Runtime Docker image will be published for most major and minor versions of Apache Airflow. Astronomer is committed to same-day releases of Runtime images for supported community Airflow versions.

It is considered safe to upgrade to minor and patch versions within a major version. Upgrade guidance for major and LTS versions is provided with each release. There is no relation between a Runtime release's version number and its release channel.

### Distribution

Runtime Docker images are formatted as:

- `quay.io/astronomer/astro-runtime:<version>`
- `quay.io/astronomer/astro-runtime:<version>-base`

For example, the images for Astro Runtime 4.0.6 would be:

- `quay.io/astronomer/astro-runtime:4.0.6`
- `quay.io/astronomer/astro-runtime:4.0.6-base`

For the smoothest, out-of-the-box Airflow experience, we strongly recommend and default to non-`base` images in your project's `Dockerfile`. These images incorporate Docker ONBUILD commands to copy and scaffold your Astro project directory so you can more easily pass those files to the containers running each core Airflow component. For complex use cases that require additional customization, a `base` Astro Runtime image might work best.

## Backport policy for bug and security fixes

When Astronomer identifies a significant bug in Astro Runtime, a fix is backported to all Long Term Support (LTS) versions and the latest stable version. To avoid the impact of previously identified bugs, Astronomer recommends that you upgrade Astro Runtime if you are not using the latest stable version.

When Astronomer identifies a significant security vulnerability in Astro Runtime, a fix is backported and made available as a patch version for all stable and LTS versions in maintenance. A significant security issue is defined as an issue with significant impact and exploitability.

Occasionally, Astronomer might deviate from the defined response policy and backport a bug or security fix to releases other than the latest stable and LTS versions. To request a fix for a specific bug, contact your customer success manager.

### Security scan results on Quay.io

Astronomer is aware of the **Security Scan Report** results that are provided by [Project Quay](https://www.projectquay.io/) for each Astro Runtime image and are publicly available on [Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

Astronomer monitors the security scan results regularly to determine if any of the vulnerabilities pose a risk to organizations using Astro Runtime. Typically, vulnerabilities found in Astro Runtime are in third-party packages that are installed in Astro Runtime but are not maintained by Astronomer. When a vulnerability is determined to have a high exploitability risk, Astronomer works with vendors to correct it and incorporate a fix into stable and LTS releases of Astro Runtime.

If there is a critical vulnerability in the Security Scan results that causes concern for your organization, contact [Astronomer Support](https://support.astronomer.io/).

## Astro Runtime maintenance policy

The maintenance period for an Astro Runtime version depends on its release channel:

| Release Channel | Maintenance Duration |
| --------------- | -------------------- |
| Stable          | 6 Months             |
| LTS             | 18 Months            |

For each `major.minor` pair, only the latest patch is supported at any given time. If you report an issue with an Astro Runtime patch version that is not latest, the Astronomer Support team will always ask that you upgrade as a first step to resolution. For example, we encourage any user who reports an issue with Astro Runtime 4.0.2 to first upgrade to the latest 4.0.x version as soon as it's generally available.

Within the maintenance window of each Astro Runtime version, the following is true:

- A set of Docker images corresponding to that version are available for download on [Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags) and PyPi.
- Astronomer will regularly publish bug or security fixes identified as high priority.
- Support for paying customers running a maintained version of Astro Runtime is provided by [Astronomer Support](https://support.astronomer.io).
- A user can create a new Deployment with the Cloud UI, API, or Astro CLI with any supported `major.minor` version pair of Runtime. For new Deployments, the Cloud UI assumes the latest patch.

When the maintenance window for a given version of Runtime ends, the following is true:

- Astronomer is not obligated to answer questions regarding a Deployment that is running an unsupported version.
- New Deployments cannot be created on Astro with that version of Runtime. Versions that are no longer maintained will not render as an option in the Deployment creation process from the Cloud UI, API, or Astro CLI.
- The Deployment view of the Cloud UI will show a warning that encourages the user to upgrade if the Deployment is running that version.
- The latest version of the Astro CLI will show a warning if a user pushes an Astro Runtime image to Astronomer that corresponds to that version.

Astronomer will not interrupt service for Deployments running Astro Runtime versions that are no longer in maintenance. Unsupported versions of Astro Runtime are available for local development and testing with the Astro CLI.

### End of maintenance date

Maintenance is discontinued the last day of the month for a given version. For example, if the maintenance window for a version of Astro Runtime is January - June of a given year, that version will be maintained by Astronomer until the last day of June.

## Astro Runtime lifecycle schedule

<!--- Version-specific -->

The following table contains the exact lifecycle for each published version of Astro Runtime. These timelines are based on the LTS and Stable release channel maintenance policies.

### Stable releases

| Runtime Version                                          | Release Date    | End of Maintenance Date |
| ---------------------------------------------------------| ----------------| ------------------------|
| [3.0.x](runtime-release-notes.md#astro-runtime-300)      | August 12, 2021 | February 2022           |
| [4.0.x](runtime-release-notes.md#astro-runtime-400)      | Oct 12, 2021    |  April 2022             |
| [4.1.x](runtime-release-notes.md#astro-runtime-410)      | Feb 22, 2022    |  August 2022            |
| [4.2.x](runtime-release-notes.md#astro-runtime-420)      | March 10, 2022  |  September 2022         |
| [5.0.x](runtime-release-notes.md#astro-runtime-500)      | April 30, 2022  |  October 2022         |

If you have any questions or concerns, reach out to [Astronomer support](https://support.astronomer.io).
