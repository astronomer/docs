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

### Support for Astro Runtime Images

You can now use Astro Runtime images in your Software Deployments. Additionally, you can now select Runtime images when setting **Image Version** for a Deployment in the Software UI.

Functionally, Runtime images are similar to Certified images. They both include:

- Same-day support for Apache Airflow releases
- Extended support lifecycles
- Regularly backported bug and security fixes

Astronomer Runtime includes additional features which are not available in Astronomer Certified images, including:

- The `astronomer-providers` package, which includes a set of operators that are built and maintained by Astronomer
- Airflow UI improvements, such as showing your Deployment's Docker image tag in the footer
- Features that are exclusive to Astro Runtime and coming soon, such as new Airflow components and improvements to the DAG development experience

To upgrade a Deployment to Runtime, follow the steps in [Upgrade Airflow](manage-airflow-versions.md), making sure to replace the Astronomer Certified image in your Dockerfile with an Astro Runtime version.

### Use a Custom Container Image Registry To Deploy Code

You can now configure a custom container image registry in place of Astronomer's default registry. This option is best suited for mature organizations who require additional control for security and governance reasons. Using a custom registry provides your organization with the opportunity to scan images for CVEs, malicious code, and approved/ unapproved Python and OS-level dependencies prior to deploying code. To configure this feature, see [Configure a Custom Image Registry](custom-image-registry.md).

### Export Task Logs Using Logging Sidecars

You can now configure logging sidecar containers to collect and export task logs to ElasticSearch. This exporting approach is best suited for organizations that use Astronomer Software in a multi-tenant cluster where security is a concern, as well as for organizations running many small tasks using the Kubernetes Executor. To configure this feature, see [Export Task Logs](export-task-logs.md).

### Simplified Configuration for Namespace Pools

The process for configuring namespace pools has been simplified. As an alternative to manually creating namespaces, you can now delegate the creation of each namespace, including roles and rolebindings, to Astronomer Software. While this feature is suitable for most use cases, you can still manually create namespaces if you want more fine-grained control over the namespace's resources and permissions. For more information, see [Namespace Pools](namespace-pools.md).

### Additional Improvements

- Added support for [Kubernetes 1.22](https://kubernetes.io/blog/2021/08/04/kubernetes-1-22-release-announcement/)
- Deprecated usage of [kubed](https://appscode.com/products/kubed/) for security and performance improvements
- Redis containers can now run as non-root users
- Added minimum security requirements for user passwords when using local auth
- You can now use Azure DevOps repos in your [Git Sync](deploy-git-sync.md) configurations
- You can now disable all network policies for Airflow components using the Astronomer Helm chart
- System Admins can now view all Workspaces on their installation by default
- User auth tokens for the Software UI are now stored in httpOnly cookies
- When importing IDP groups as teams, you can now configure a `teamFilterRegex` in `config.yaml` to filter out IDP groups from being imported using regex
- Added support for audit logging when a user interacts with the Houston API. This includes actions within the Software UI

### Bug fixes

- Fixed a typo in the `loadBalancerIP` key in the Nginx Helm chart
- Fixed an issue where Azure AD connect sync did not work with Astronomer's Teams feature
- Fixed an issue where upgrades would fail if you had changed `networkNSLabels` from `true` to `false` in `config.yaml`
