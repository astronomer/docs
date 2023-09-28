---
title: 'Astronomer Software v0.29 release notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---


<!--- Version-specific -->

This document includes all release notes for Astronomer Software version 0.29.

0.30 is the latest long-term support (LTS) version of Astronomer Software. To upgrade to 0.30, see [Upgrade Astronomer](upgrade-astronomer.md). For more information about Astronomer Software release channels, see [Release and lifecycle policies](release-lifecycle-policy.md). For more Astronomer Software release notes, see:

- [Astro CLI release notes](cli-release-notes.md)
- [Astro Runtime release notes](https://docs.astronomer.io/astro/runtime-release-notes)
- [Astronomer Software 0.29 release notes](https://docs.astronomer.io/software/0.29/release-notes)
- [Astronomer Software 0.28 release notes](https://docs.astronomer.io/software/0.28/release-notes)
- [Astronomer Software 0.25 release notes](https://docs.astronomer.io/software/0.25/release-notes)

Astronomer tests all Astronomer Software versions for scale, reliability, and security on Amazon EKS, Google GKE, and Azure AKS. If you have questions or an issue to report, contact [Astronomer support](https://support.astronomer.io).

:::warning Breaking change

There is an [unresolved Kubernetes bug](https://github.com/kubernetes/kubernetes/issues/65106) that occurs when upgrading Helm charts that include duplicate keys in an `env` array. If you have a Helm chart with duplicate keys and upgrade to Astronomer Software 0.29.3+, all key-value pairs with the duplicate key are removed from your environment.

To preserve duplicate keys in your Helm chart, you can either reapply the values after upgrading, or you can use the `--reset-values` flag when running the upgrade script as described in [Upgrade Astronomer](upgrade-astronomer.md).

:::

## v0.29.5

Release date: October 11, 2022

### Additional improvements

- Improved the startup time for the platform NATS server.
- You can now configure a `livenessProbe` and `readinessProbe` specific to Prometheus in the Prometheus Helm chart.
- You can now configure a specific `securityContext` for Fluentd Pods and containers in the Fluentd Helm chart.

### Bug fixes 

- Fixed an issue where upgrading Astronomer Software with a custom `houston.deployments.components` value in Helm could break the Software UI.
- Fixed an issue where upgrading a Deployment from Airflow 1.10.15 to 2.3 can prevent you from configuring the Deployment's resources in the Software UI.
- Fixed the following CVEs:

    - [CVE-2022-40674](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40674)
    - [CVE-2022-3224](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3224)

## v0.29.4

Release date: September 13, 2022

### Additional improvements

- You can now specify `authUrlParams` for your identity provider (IdP) in `config.yaml`
- Added error handling for upgrading a Software installation on an unsupported upgrade path

### Bug fixes

- Fixed an issue where you could not create Deployments with unsupported Airflow versions when `enableSystemAdminCanCreateDeprecatedAirflows: true`
- Fixed the following vulnerabilities:

    - [CVE-2022-1996](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1996)
    - [CVE-2022-21698](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-21698)
    - [CVE-2022-35949](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-35949)
    - [CVE-2022-35948](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-35948)
    - [CVE-2022-37434](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-37434)

## v0.29.3

Release date: August 5, 2022

### Additional improvements

- Resolved several high and critical CVEs.

### Bug fixes

- API requests to query the AUs allocated to **Extra Capacity** are now returning results for all Deployments in a Workspace. Previously, queries were only returning partial results.

## v0.29.2

Release date: July 18, 2022

### Additional improvements

- You can now configure Vector on [logging sidecars](export-task-logs.md#export-logs-using-container-sidecars) to send Airflow task logs to third-party log management systems.
- Resolved several high and critical CVEs.
- You can now assign System Viewer and System Editor permissions to a [Team](import-idp-groups.md).
- You can now assign System Viewer and System Editor permissions to a user from the Software UI.

### Bug fixes

- If you have `customLogging.enabled=true` and `loggingSidecar.customConfig=false` in your Helm configuration, logs now appear in the Software UI as expected.
- System Admins can no longer update their own role.
- The Software UI no longer counts inactive users in its user count figures.
- Fixed an issue where you could still access a Deployment using a URL after logging out of the Software UI.
- Fixed an issue where you could view Deployment information from a Workspace that was deleted with `astro workspace delete`.
- Fixed an issue where you could not open Celery from the Software UI.
- Improved the reliability of upgrading Astronomer Software with 30+ Deployments when `upgradeDeployments=true`.

## v0.29.1

Release date: June 3, 2022

### Bug fixes

- Fixed an issue where you couldn't run Houston API queries for Deployments using `releaseName` and `label`
- Fixed an issue where a user could not log in through Azure AD SSO if the user belonged to a group without a `displayName`

## v0.29.0

Release date: June 1, 2022

### Support for Astro Runtime images

You can now use Astro Runtime images in your Software Deployments. Additionally, you can now select Runtime images when setting **Image Version** for a Deployment in the Software UI.

Functionally, Runtime images are similar to Certified images. They both include:

- Same-day support for Apache Airflow releases
- Extended support lifecycles
- Regularly backported bug and security fixes

Astro Runtime includes additional features which are not available in Astronomer Certified images, including:

- The `astronomer-providers` package, which includes a set of operators that are built and maintained by Astronomer
- Airflow UI improvements, such as showing your Deployment's Docker image tag in the footer
- Features that are exclusive to Astro Runtime and coming soon, such as new Airflow components and improvements to the DAG development experience

To upgrade a Deployment to Runtime, follow the steps in [Upgrade Airflow](manage-airflow-versions.md), making sure to replace the Astronomer Certified image in your Dockerfile with an Astro Runtime version.

### Use a custom container image registry to deploy code

You can now configure a custom container image registry in place of Astronomer's default registry. This option is best suited for mature organizations who require additional control for security and governance reasons. Using a custom registry provides your organization with the opportunity to scan images for CVEs, malicious code, and approved/ unapproved Python and OS-level dependencies prior to deploying code. To configure this feature, see [Configure a custom image registry](custom-image-registry.md).

### Export task logs using logging sidecars

You can now configure logging sidecar containers to collect and export task logs to ElasticSearch. This exporting approach is best suited for organizations that use Astronomer Software in a multi-tenant cluster where security is a concern, as well as for organizations running many small tasks using the Kubernetes executor. To configure this feature, see [Export task logs](export-task-logs.md).

### Simplified configuration for namespace pools

The process for configuring namespace pools has been simplified. As an alternative to manually creating namespaces, you can now delegate the creation of each namespace, including roles and rolebindings, to Astronomer Software. While this feature is suitable for most use cases, you can still manually create namespaces if you want more fine-grained control over the namespace's resources and permissions. For more information, see [Namespace pools](namespace-pools.md).

### Additional improvements

- Added support for [Kubernetes 1.22](https://kubernetes.io/blog/2021/08/04/kubernetes-1-22-release-announcement/)
- Deprecated usage of [kubed](https://appscode.com/products/kubed/) for security and performance improvements
- Redis containers can now run as non-root users
- Added minimum security requirements for user passwords when using local auth
- You can now use Azure DevOps repos in your [Git sync](deploy-git-sync.md) configurations
- You can now disable all network policies for Airflow components using the Astronomer Helm chart
- System Admins can now view all Workspaces on their installation by default
- User auth tokens for the Software UI are now stored in httpOnly cookies
- When importing IdP groups as teams, you can now configure a `teamFilterRegex` in `config.yaml` to filter out IdP groups from being imported using regex
- Added support for audit logging when a user interacts with the Houston API. This includes actions within the Software UI

### Bug fixes

- Fixed an issue in Deployments running Airflow 2.3+ where logs for dynamically mapped tasks did not have a correct `log_id`
- Fixed a typo in the `loadBalancerIP` key in the Nginx Helm chart
- Fixed an issue where Azure AD connect sync did not work with Astronomer's Teams feature
- Fixed an issue where upgrades would fail if you had changed `networkNSLabels` from `true` to `false` in `config.yaml`
