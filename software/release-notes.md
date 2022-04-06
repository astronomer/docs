---
title: 'Astronomer Software v0.28 Release Notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

## Overview

<!--- Version-specific -->

This document includes all release notes for Astronomer Software v0.28.

Astronomer v0.28 is the latest Stable version of Astronomer Software, while v0.25 remains the latest long-term support (LTS) version. To upgrade to Astronomer v0.28 from v0.26+, read [Upgrade to a Stable Version](upgrade-astronomer-stable.md). For more information about Software release channels, read [Release and Lifecycle Policies](release-lifecycle-policy.md). To read release notes specifically for the Astronomer CLI, see [Astronomer CLI Release Notes](cli-release-notes.md).

We're committed to testing all Astronomer Software versions for scale, reliability and security on Amazon EKS, Google GKE and Azure AKS. If you have any questions or an issue to report, don't hesitate to [reach out to us](https://support.astronomer.io).

## v0.28.3

Release date: March 17, 2022

### Bug Fixes

- Fixed an issue where airgapped upgrades and installations could fail due to a mismatched Airflow Helm chart between Astronomer components

## v0.28.2

Release date: March 14, 2022

### Additional Improvements

- System Admins can now update the name and description for any Workspace on their installation.
- You can now specify `global.external_labels` and `remote_write` options for Prometheus through the Astronomer Helm chart.
- You can now configure `nodeSelector`, `tolerations`, and `affinity` in the STAN and NATS Helm charts.

### Bug Fixes

- Fixed several CVEs
- Fixed a few issues where some buttons in the Software UI did not link to the appropriate page
- Fixed an issue where you could not install Astronomer Software 0.27 or 0.28 in an [airgapped environment](install-airgapped.md)
- Fixed an issue where System and Workspace Admins were able to delete users that were part of an [IDP team](import-idp-groups.md)

## v0.28.1

Release date: February 22, 2022

### Bug fixes

- Fixed an issue where users could not successfully log in through Azure AD

## v0.28.0

Release date: February 15, 2022

### Import Identity Provider User Groups as Teams

You now can import existing identity provider (IDP) groups into Astronomer Software as Teams, which are groups of Astronomer users that have the same set of permissions to a given Workspace or Deployment. Importing existing IDP groups as Teams enables swift onboarding to Astronomer and better control over multiple user permissions.

For more information about configuring this feature, read [Import IDP Groups](import-idp-groups.md). To learn more about adding and setting permissions for Teams via the Astronomer UI, read [User Permissions](workspace-permissions.md#via-teams).

### Additional Improvements

- Astronomer now supports `prefer` and `require` SSL modes for connecting to PGBouncer. You can set this SSL mode via the `global.ssl.mode` value in your `config.yaml` file. Note that in v0.28.0, this feature works only with AWS and Azure.
- You can now set [Grafana environment variables](https://grafana.com/docs/grafana/latest/administration/configuration/#override-configuration-with-environment-variables) using the `grafana.extraEnvVars` setting in your `config.yaml` file.
- Added a new **Ephemeral Storage Overwrite Gigabytes** slider to the Git Sync configuration screen. You can configure this slider to allocate more memory for syncing larger Git repos.
- Added a new **Sync Timeout** slider to the Git Sync configuration screen. You can configure this slider to set a maximum allowed length of time for syncing a Git repo.

### Bug Fixes

- Removed root user permissions for authSidecar
- Added AWS RDS certificates to list of trusted certificates
- Removed support for Kubernetes 1.18
- Fixed some confusing behavior with the Git-Sync **SSH Key** field in the UI  
- Fixed an issue where the Astronomer platform and Airflow could not communicate in environments where inter-namespace communication is disabled
- Fixed an issue where users would frequently get 502 errors when logging in to the Astronomer UI
- Fixed an issue where users would get timeout issues when attempting to log in to an Astronomer installation on OpenShift
