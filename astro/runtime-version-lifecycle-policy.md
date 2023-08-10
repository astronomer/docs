---
title: "Astro Runtime maintenance and lifecycle policy"
sidebar_label: "Astro Runtime maintenance policy"
id: runtime-version-lifecycle-policy
---

<head>
  <meta name="description" content="Learn how Astronomer releases and maintains Astro Runtime. Astro Runtime is a Docker image built by Astronomer that provides a differentiated Apache Airflow experience and execution framework." />
  <meta name="og:description" content="Learn how Astronomer releases and maintains Astro Runtime. Astro Runtime is a Docker image built by Astronomer that provides a differentiated Apache Airflow experience and execution framework." />
</head>

Astro Runtime is a production ready, data orchestration tool based on Apache Airflow that is distributed as a Docker image and is required by all Astronomer products. It is intended to provide organizations with improved functionality, reliability, efficiency, and performance. Deploying Astro Runtime is a requirement if your organization is using Astro.

Astronomer maintenance and lifecycle policies are part of the distribution and define the period that specific Astro Runtime versions are supported and how frequently updates are provided.

## Release channels

To meet the unique needs of different operating environments, Astro Runtime versions are associated with the following release channels:

- **Stable:** Includes the latest Astronomer and Apache Airflow features, available on release
- **Long-term Support (LTS):** Includes additional testing, stability, and maintenance for a core set of features

Each major Astro Runtime version is associated with an Astro Runtime stable release channel. The LTS release channel is a subset of the stable release channel and includes additional stability, reliability, and support. For more information on how Astro Runtime is versioned, see [Runtime versioning](runtime-image-architecture.md#runtime-versioning).

For users that want to keep up with the latest Astronomer and Airflow features on an incremental basis, we recommend upgrading to new versions of Astro Runtime as soon as they are made generally available. This should be regardless of release channel. New versions of Runtime are issued regularly and include timely support for the latest major, minor, and patch versions of Airflow.

For customers looking for less frequent upgrades and functional changes, we recommend following the LTS release channel exclusively.

## Astro Runtime maintenance policy

The maintenance period for an Astro Runtime version depends on its release channel:

| Release Channel | Maintenance Duration                                                            |
| --------------- | ------------------------------------------------------------------------------- |
| Stable          | 6 months or 3 months after the next major Runtime release (whichever is longer) |
| LTS             | 18 months                                                                       |

For each major Runtime version, only the latest `minor.patch` version is supported at any given time. If you report an issue with an Astro Runtime version that is not latest, the Astronomer Support team will always ask that you upgrade as a first step to resolution. For example, any user who reports an issue with Astro Runtime 4.0.2 will be asked to upgrade to the latest 4.x.y version as soon as it's generally available.

Within the maintenance window of each Astro Runtime version, the following is true:

- A set of Docker images corresponding to that version are available for download on [Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags) and PyPi.
- Astronomer will regularly publish bug or security fixes identified as high priority.
- Support for paying customers running a maintained version of Astro Runtime is provided by [Astronomer Support](https://cloud.astronomer.io/support).
- A user can create a new Deployment with the Cloud UI, API, or Astro CLI with any supported `major.minor` version pair of Runtime. For new Deployments, the Cloud UI assumes the latest patch.

When the maintenance window for a given version of Runtime ends, the following is true:

- Astronomer is not obligated to answer questions regarding a Deployment that is running an unsupported version.
- New Deployments cannot be created on Astro with that version of Runtime. Versions that are no longer maintained will not render as an option in the Deployment creation process from the Cloud UI, API, or Astro CLI.
- The Deployment view of the Cloud UI will show a warning that encourages the user to upgrade if the Deployment is running that version.
- The latest version of the Astro CLI will show a warning if a user pushes an Astro Runtime image to Astronomer that corresponds to that version.

Astronomer will not interrupt service for Deployments running Astro Runtime versions that are no longer in maintenance. Unsupported versions of Astro Runtime are available for local development and testing with the Astro CLI.

### End of maintenance date

Maintenance is discontinued the last day of the month for a given version. For example, if the maintenance window for a version of Astro Runtime is January - June of a given year, that version will be maintained by Astronomer until the last day of June.

## Security

Astronomer continuously checks for available security fixes for software used in Astro Runtime. This process includes scanning language dependencies, container images, and open source threat intelligence sources. When a security fix is available, Astronomer evaluates potential risks for organizations using Astro Runtime and determines deployment priority. Low priority fixes are deployed following the regular maintenance policy as described in [Astro Runtime maintenance policy](runtime-version-lifecycle-policy.md#astro-runtime-maintenance-policy).

If a vulnerability is not yet addressed in a third-party dependency and no official fix is available, Astronomer attempts to address the vulnerability or its impact with environmental mitigations. Whenever possible, Astronomer collaborates with the upstream project to support a timely delivery of the official fix. This process also covers images publicly available on [Quay.io](https://quay.io/repository/astronomer/astro-runtime?tab=tags) and provides context for their vulnerability scanning results.

If you identify a vulnerability that results in relevant risk for your organization, contact [Astronomer security](mailto:security@astronomer.io).

### Backport policy for bug and security fixes

- **Functional bugs:** When Astronomer identifies a significant functional bug in Astro Runtime, a fix is backported to all Long Term Support (LTS) versions and the latest stable version. To avoid the impact of previously identified bugs, Astronomer recommends that you consistently upgrade Astro Runtime to the latest stable version.

- **Security vulnerabilities:** When Astronomer identifies a significant security vulnerability in Astro Runtime, a fix is backported and made available as a patch version for all stable and LTS versions in maintenance. A significant security issue is defined as an issue with significant impact and exploitability.

Occasionally, Astronomer might deviate from the defined response policy and backport a bug or security fix to releases other than the latest stable and LTS versions. To request a fix for a specific bug, contact your customer success manager.

## Astro Runtime lifecycle schedule

<!--- Version-specific -->

The following table contains the exact lifecycle for each published version of Astro Runtime. These timelines are based on the LTS and Stable release channel maintenance policies.

### Stable releases

| Runtime Version                                 | Apache Airflow version | Release Date       | End of Maintenance Date |
| ----------------------------------------------- | ---------------------- | ------------------ | ----------------------- |
| [4](runtime-release-notes.md#astro-runtime-420) | 2.2                    | March 10, 2022     | September 2023          |
| [5](runtime-release-notes.md#astro-runtime-500) | 2.3                    | April 30, 2022     | October 2023            |
| [6](runtime-release-notes.md#astro-runtime-600) | 2.4                    | September 19, 2022 | March 2024              |
| [7](runtime-release-notes.md#astro-runtime-700) | 2.5                    | December 3, 2022   | July 2023               |
| [8](runtime-release-notes.md#astro-runtime-800) | 2.6                    | April 30, 2023     | October 2023            |
| [9](runtime-release-notes.md#astro-runtime-900) | 2.6                    | August 14, 2023    | January 2024            |

### Long-term support (LTS) releases 

| Runtime Version                                 | Apache Airflow version | Release Date       | End of Maintenance Date |
| ----------------------------------------------- | ---------------------- | ------------------ | ----------------------- |
| [4](runtime-release-notes.md#astro-runtime-420) | 2.2                    | March 10, 2022     | September 2023          |
| [5](runtime-release-notes.md#astro-runtime-500) | 2.3                    | April 30, 2022     | October 2023            |
| [6](runtime-release-notes.md#astro-runtime-600) | 2.4                    | September 19, 2022 | March 2024              |

:::info
For version compatibility information, see the [Runtime release notes](runtime-release-notes.md).
:::

If you have any questions or concerns, contact [Astronomer support](https://cloud.astronomer.io/support).

## Related documentation

- [Astro Runtime architecture](runtime-image-architecture.md)
- [Astro Runtime release notes](runtime-release-notes.md)
