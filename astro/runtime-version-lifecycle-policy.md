---
title: "Astro Runtime lifecycle policy"
sidebar_label: "Astro Runtime lifecycle policy"
id: runtime-version-lifecycle-policy
description: Learn how Astronomer releases and maintains Astro Runtime, the core component that powers a differentiated Apache Airflow experience on Astro.
---

Astro Runtime is a production ready, data orchestration tool based on Apache Airflow that is distributed as a Docker image and is required by all Astronomer products. It is intended to provide organizations with improved functionality, reliability, efficiency, and performance. Deploying Astro Runtime is a requirement if your organization is using Astro.

Policies define the period that specific Astro Runtime versions are supported and the frequency updates are provided.

## Release channels

To meet the unique needs of different operating environments, Astro Runtime versions are associated with the following release channels:

- **Stable:** Includes the latest Astronomer and Apache Airflow features, available on release
- **Long-term Support (LTS):** Includes additional testing, stability, and maintenance for a core set of features

All releases of Astro Runtime are considered stable. The LTS release channel is a subset of the stable release channel that promises additional stability, reliability, and support from our team.

For users that want to keep up with the latest Astronomer and Airflow features on an incremental basis, we recommend upgrading to new versions of Astro Runtime as soon as they are made generally available. This should be regardless of release channel. New versions of Runtime are issued regularly and include timely support for the latest major, minor, and patch versions of Airflow.

For customers looking for less frequent upgrades and functional changes, we recommend following the LTS release channel exclusively.

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

## Backport policy for bug and security fixes

When Astronomer identifies a significant bug in Astro Runtime, a fix is backported to all Long Term Support (LTS) versions and the latest stable version. To avoid the impact of previously identified bugs, Astronomer recommends that you upgrade Astro Runtime if you are not using the latest stable version.

When Astronomer identifies a significant security vulnerability in Astro Runtime, a fix is backported and made available as a patch version for all stable and LTS versions in maintenance. A significant security issue is defined as an issue with significant impact and exploitability.

Occasionally, Astronomer might deviate from the defined response policy and backport a bug or security fix to releases other than the latest stable and LTS versions. To request a fix for a specific bug, contact your customer success manager.

### Security scan results on Quay.io

Astronomer is aware of the **Security Scan Report** results that are provided by [Project Quay](https://www.projectquay.io/) for each Astro Runtime image and are publicly available on [Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags).

Astronomer monitors the security scan results regularly to determine if any of the vulnerabilities pose a risk to organizations using Astro Runtime. Typically, vulnerabilities found in Astro Runtime are in third-party packages that are installed in Astro Runtime but are not maintained by Astronomer. When a vulnerability is determined to have a high exploitability risk, Astronomer works with vendors to correct it and incorporate a fix into stable and LTS releases of Astro Runtime.

If there is a critical vulnerability in the Security Scan results that causes concern for your organization, contact [Astronomer Support](https://support.astronomer.io/).

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

If you have any questions or concerns, contact [Astronomer support](https://support.astronomer.io).

## Related documentation

- [Astro Runtime architecture](runtime-image-architecture.md)
- [Astro Runtime release notes](runtime-release-notes.md)
