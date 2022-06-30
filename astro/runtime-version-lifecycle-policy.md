---
title: "Astro Runtime versioning and lifecycle policy"
sidebar_label: "Versioning and lifecycle policy"
id: runtime-version-lifecycle-policy
description: Learn how Astronomer releases and maintains Astro Runtime, the core component that powers a differentiated Apache Airflow experience on Astro.
---

Astro Runtime is a production ready, data orchestration tool based on Apache Airflow that is distributed as a Docker image and is required by all Astronomer products. It is intended to provide organizations with improved functionality, reliability, efficiency, and performance. Deploying Astro Runtime is a requirement if your organization is using Astro.

Policies define the period that specific Astro Runtime versions are supported and the frequency of updates.  

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

If you have any questions or concerns, contact [Astronomer support](https://support.astronomer.io).

## Related documentation

- [Astro Runtime architecture](runtime-image-architecture.md)
- [Astro Runtime release notes](runtime-release-notes.md)
