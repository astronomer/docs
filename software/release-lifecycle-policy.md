---
title: Astronomer release and lifecycle policy
sidebar_label: Release and lifecycle policy
id: release-lifecycle-policy
description: Astronomer's release and lifecycle policy for Astronomer Software.
---

Astronomer supports a variety of policies that drives the naming, release cadence, and maintenance commitments associated with all published software.

This document offers guidelines on the version lifecycle of Astronomer Software. It includes a description of:

- How Astronomer is versioned.
- Which versions of Astronomer Software are currently available.
- Release channels and the maintenance schedule for all versions.

For information on the latest Astronomer Software releases, see [Release notes](release-notes.md). For information on compatibility between all versioned software, see [Software Version compatibility reference](version-compatibility-reference.md).

:::info

These policies apply only to the Astronomer Software platform. For release and lifecycle policies related to Astro Runtime, see [Runtime release and lifecycle Policy](https://docs.astronomer.io/astro/runtime-version-lifecycle-policy).

:::

## Release channels

To meet the unique needs of different operating environments, we offer all Astronomer customers two release channels:

- **Stable:** Includes the latest Astronomer and Airflow features
- **Long-term Support (LTS):** Includes long-term testing, stability, and maintenance for a core set of features

All releases of AC are considered stable. The LTS release channel is a subset of the stable release channel that promises additional stability, reliability, and support from our team.

For customers looking to access Astronomer's newest features on an incremental basis, Astronomer recommends following the stable release channel and upgrading to new versions as soon as they are made available. Stable releases are issued approximately once per quarter for Astronomer Software and the Astro CLI.

For customers looking for less frequent upgrades and functional changes, we recommend following the LTS release channel. Release channels are not binding, so you are free to upgrade to any available version of Astronomer Software at any time.

> **Note:** Release channels apply to Astronomer Software and Astronomer image versions. We do not currently support a long-term release channel for the Astro CLI.

## Astronomer Software versioning

Astronomer follows [Semantic Versioning](https://semver.org/) for all published software. This means that we use Major, Minor, and Patch releases across our product in the format of `major.minor.patch`.

- **Major** versions are released for significant feature additions, including backward-incompatible changes to an API or DAG specification.
- **Minor** versions are released for functional changes, including backward-compatible changes to an API or DAG specification.
- **Patch** versions are released for bug and security fixes that resolve incorrect behavior.

It is considered safe to upgrade to minor and patch versions within a major version. Upgrade guidance for major and LTS versions is provided with each release.

## Version maintenance policy

The maintenance period for an Astronomer Software version depends on its release channel:

| Release Channel | Frequency of Releases | Maintenance Duration |
| --------------- | --------------------- | -------------------- |
| Stable          | Quarterly             | 6 Months             |
| LTS             | Yearly                | 12 Months            |

For each `major.minor` pair, only the latest patch is supported at any given time.

For example, if Astronomer Software v0.26 were a stable version first released in October 2021:

- Support for Astronomer Software v0.26 would end 6 months later in April 2022.
- If a patch version for v0.26 came out in December 2021 (e.g. `v0.26.4`), it would not affect the maintenance duration. Maintenance for v0.26 would still end in April 2022.
- If a major bug was identified in v0.26, a fix would be backported by the Astronomer team and released as a patch to v0.26 as long as it remained the latest stable release.
- If Astronomer Software v0.27 came out as a new stable release, bug fixes would no longer be backported to Astronomer v0.26 and customers would be encouraged to upgrade.
- If a major security issue was identified in v0.26, a fix would be backported and released as a patch at any time during its 6 month maintenance period. Even if v0.27 is the latest stable version of Astronomer Software, a security fix would still be backported to v0.26.

If you contact [Astronomer support](https://support.astronomer.io) about an issue you are experiencing while running an unmaintained version, our team will invite you to upgrade as an initial mitigation step.

### End of maintenance date

Maintenance is discontinued the last day of the month for a given version. For example, if a version of Astronomer Software were supported between January - June of a given year, that version would be maintained by Astronomer until the last day of June.

## Backport policy for bug and security fixes

If a major stability bug is identified by our team, a fix will be backported to all LTS versions and only the latest stable version. For users on a stable version that is not latest, our team will recommend that you upgrade. Major issues in this category may result in significant delays in task scheduling as well as potential data loss.

If a major security issue is identified, a fix will be backported and made available as a new patch version for _all_ supported stable and LTS releases. Major issues in this category are classified by a combination of impact and exploitability.

In rare instances, the Astronomer team may make an exception and backport a bug or security fix to a release that is beyond the commitment stated above. To submit a request for consideration, please reach out to your customer success manager.

## Software lifecycle schedule

<!--- Version-specific -->

The following tables contain the exact lifecycle for each published version of Astronomer Software. These timelines are based on the LTS and stable release channel maintenance policies.

### Stable

| Software Version | Release Date    | End of Maintenance Date |
| ---------------- | --------------- | ----------------------- |
| 0.30             | August 29, 2022 | August 2024             |
| 0.32             | April 28,2023   | October 2023            |
| 0.33             | July 28,2023   | January 2023            |

### LTS

| Software Version | Release Date | End of Maintenance Date |
| ---------------- | ------------ | ----------------------- |
| 0.30             | Aug 29, 2022 | August 2024             |
| 0.32             | April 28,2023   | April 2024            |

