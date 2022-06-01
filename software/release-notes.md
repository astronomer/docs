---
title: 'Astronomer Software v0.29 Release Notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

## Overview

<!--- Version-specific -->

This document includes all release notes for Astronomer Software version 0.29.

0.29 is the latest stable version of Astronomer Software, while 0.28 remains  the latest LTS long-term support (LTS) version of Astronomer Software. To upgrade to 0.29, read [Upgrade Astronomer](upgrade-astronomer-stable.md). For more information about Software release channels, read [Release and Lifecycle Policies](release-lifecycle-policy.md). To read release notes specifically for the Astronomer CLI, see [Astronomer CLI Release Notes](cli-release-notes.md).

We're committed to testing all Astronomer Software versions for scale, reliability and security on Amazon EKS, Google GKE and Azure AKS. If you have any questions or an issue to report, don't hesitate to [reach out to us](https://support.astronomer.io).

## v0.29.0

Release date: June 1, 2022

### Support for Astro Runtime Images on Software

You can now use Astro Runtime images in your Software Deployments. Additionally, you can now select Runtime images when setting **Image Version** for a Deployment in the Software UI.

Functionally, Runtime images are similar to Certified images. They both include:

- Same-day support for Apache Airflow releases
- Extended support lifecycles
- Regularly backported bug and security fixes

Astronomer Runtime includes additional features which are not available in Astronomer Certified images, including:

- The `astronomer-providers` package, which includes a set of deferrable operators build and maintained by Astronomer
- Airflow UI improvements, such as the showing your Deployment's Docker image tag in the footer of all UI pages
- Future Runtime-exclusive features, such as new Airflow components and improvements to the DAG development experience

To upgrade a Deployment to Runtime, follow the steps in Upgrade Airflow, making sure to replace the Astronomer Certified image in your Dockerfile with an Astronomer Runtime version.

### Export Task Logs Using Logging Sidecars

You can now configure logging sidecar containers to collect and export task logs to ElasticSearch. This exporting approach is best suited for organizations that use Astronomer Software in a multi-tenant cluster and need to prioritize security.To configure this feature, see [Export Task Logs](export-task-logs.md).

### Simplified Configuration for Namespace Pools

The process for configuring namespace pools has been simplified. As an alternative to manually creating namespaces, you can now delegate the creation of each namespace, including roles and rolebindings, to Astronomer Software. While this feature is suitable for most use cases, you can still manually create namespaces if you want more fine-grained control over the namespace's resources and permissions. For more information, see [Namespace Pools](namespace-pools.md).
