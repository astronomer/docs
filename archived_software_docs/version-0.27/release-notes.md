---
title: 'Astronomer Software v0.27 Release Notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

## Overview

<!--- Version-specific -->

This document includes all release notes for Astronomer Software v0.27.

Astronomer v0.27 is the latest Stable version of Astronomer Software, while v0.28 remains the latest long-term support (LTS) version. To upgrade to Astronomer v0.27 from v0.26, read [Upgrade to a Stable Version](upgrade-astronomer.md). For more information about Software release channels, read [Release and Lifecycle Policies](release-lifecycle-policy.md). To read release notes specifically for the Astronomer CLI, see [Astronomer CLI Release Notes](cli-release-notes.md).

We're committed to testing all Astronomer Software versions for scale, reliability and security on Amazon EKS, Google GKE and Azure AKS. If you have any questions or an issue to report, don't hesitate to [reach out to us](https://support.astronomer.io).

## 0.27.4

Release date: March 8, 2022

### Bug Fixes

- Fixed an issue where you could not install Astronomer Software 0.27 or 0.28 in an airgapped environment
- Fixed an issue where new users without permissions to create Workspaces would be directed to the **New Workspace** page when they first log in
- Fixed several CVEs

## 0.27.3

Release date: Feb 22, 2022

### Limit Workspace Creation to System Admins

To provide more control over resource usage across your organization, you can now limit the ability to create Workspaces only to users with System Admin permissions.

For more information about each role's permissions, including instructions for how to modify a role's permissions, see [Platform User Management](manage-platform-users.md).

### Additional improvements

- Added the `houston.config.deployments.enableSystemAdminCanCreateDeprecatedAirflows` configuration which enables System Admins to create Deployments with deprecated versions of Astronomer Certified

### Bug Fixes

- Fixed documentation links in the Software UI

## 0.27.1

Release date: January 10, 2022

### Bug Fixes

- Fixed an issue where users could not create Deployments via an IAM role

## 0.27.0

Release date: December 21, 2021

### Custom OAuth Flows

You can now configure a custom OAuth flow as an alternative to Astronomer's default implicit flow. You can customize Astronomer's existing Okta, Google, and GitHub OAuth flows, or you can import an entirely custom OAuth flow. For more information, read [Configure a Custom OAuth Flow](integrate-auth-system.md#configure-a-custom-oauth-flow).

### Deploy DAGs via Git Sync

You can now configure a Git repo to continually push DAGs to an Astronomer Deployment via git-sync. DAGs deployed via git-sync automatically appear in the Airflow UI without requiring additional action or causing downtime. For more information, read [Deploy DAGs via Git Sync](deploy-git-sync.md).

### External ElasticSearch Logging

Custom ElasticSearch logging tools are now supported via new values in your `config.yaml` file:

```yaml
# External ES logging
global:
  customLogging:
    enabled: true
    scheme: https
    host: ""
    port: ""
    secret: ""
    #secretName: ~
    #awsSecretName: ~
    #awsIAMRole: ~
    #awsServiceAccountAnnotation: ~
```

### CLI Support for Podman

By default, the Astronomer CLI uses Docker to execute a few specific commands. As an alternative, you can now configure the Astronomer CLI to use Podman instead. For more information, read [Run the CLI with Podman](https://www.astronomer.io/docs/astro/cli/use-podman).

### Bug Fixes

- Dropped support for Kubernetes 1.17
- Fixed an issue where redeployments could clobber existing annotations for namespaces
- Fixed an issue where new Deployments could potentially generate invalid usernames for Celery and the metadata DB
- Fixed an issue where scheduler, webserver, and worker logs were not accessible via the Astronomer CLI
- Fixed an issue where where setting extra volumes via `config.yaml` did not work when NFS DAG deploys were enabled.
