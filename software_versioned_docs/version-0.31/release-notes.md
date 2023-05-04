---
title: 'Astronomer Software v0.31 release notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

<!--- Version-specific -->

0.31 is the latest stable version of Astronomer Software, while 0.30 remains the latest long-term support (LTS) release. To upgrade to 0.31, see [Upgrade Astronomer](upgrade-astronomer.md). For more information about Software release channels, see [Release and lifecycle policies](release-lifecycle-policy.md). To read release notes specifically for the Astro CLI, see [Astro CLI release notes](https://docs.astronomer.io/astro/cli/release-notes).

## 0.31.3

Release date: February 24, 2023

### Additional improvements

- You can now configure `extraVolumes` and `extraVolumeMounts` in the Alertmanager Helm chart, which can be useful for storing secret credentials for services that read your alerts.
- You can now use `astronomer.houston.ingress.annotation` in the Astronomer Helm chart to configure custom ingress annotations for Houston.
- You can now upgrade the Airflow Helm chart for individual Deployments by running `yarn upgrade-deployments <deployment-id>` from within the Houston Pod.

### Bug fixes 

- Fixed an issue where you could not set `AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER` in a Deployment if you were using an Astronomer Certified image.
- Astronomer Software now filters orphaned Deployments and Workspaces owned by users who were removed from an identity provider (IdP) group with SCIM enabled.
- Fixed a security vulnerability where you could query Elasticsearch logs for a Deployment from a different Deployment.
- Fixed an issue where authentication tokens were visible in Nginx logs produced by the Software UI.
- Fixed an issue where deploying an image with the `docker/build-push-action` GitHub action could produce errors in Houston that affected the entire Astronomer Software installation.
- Fixed the following vulnerabilities:
  
    - [CVE-2023-24807](https://nvd.nist.gov/vuln/detail/CVE-2023-24807)
    - [CVE-2022-25881](https://nvd.nist.gov/vuln/detail/CVE-2023-25881)
    - [CVE-2023-8286](https://nvd.nist.gov/vuln/detail/CVE-2023-8286)

## 0.31.2

Release date: February 2, 2023

### Additional improvements

- Support for Kubernetes [1.25](https://kubernetes.io/blog/2022/08/23/kubernetes-v1-25-release/) and [1.26](https://kubernetes.io/blog/2022/12/09/kubernetes-v1-26-release/).
- You can now configure custom annotations for Houston ingress by setting `astronomer.houston.ingress.annotation` in your `config.yaml` file. 
- The System Admin **Deployments** list in the Software UI is now paginated. 
- You can now use the following values in your `config.yaml` file to configure resource allocation for the git-sync relay service:
  
    - `astronomer.gitSyncRelay.gitSyncResources`
    - `astronomer.gitSyncRelay.gitDaemonResources`
    - `astronomer.gitSyncRelay.securityContext`

- You can now set `timeoutSeconds` for `readinessProbe` and `livenessProbe` in the Prometheus Helm chart.
- Fixed an issue where Deployments with many DAGs could not be successfully upgraded due to a short timeout.
- Houston API now logs an installation's deployed image versions whenever a GraphQL mutation is completed.

### Bug fixes 

- To limit Out of Memory (OOM) errors when migrating large DAGs, Deployment database migrations now use the same resources as the Deployment's scheduler.
- Fixed an issue in the Software UI where refreshing pages listing Workspace or Deployment service accounts returned an error.
- Fixed an issue where PgBouncer didn't work if you pulled its image from a private registry.
- When you view a user through a Teams list as a System Admin and return to the list, you now return to the Teams list instead of the System Admin users list. 
- Fixed the following vulnerabilities:
  
    - [CVE-2022-23529](https://nvd.nist.gov/vuln/detail/CVE-2022-23529)
    - [CVE-2021-44906](https://nvd.nist.gov/vuln/detail/CVE-2021-44906)
    - [CVE-2022-23540](https://nvd.nist.gov/vuln/detail/CVE-2022-23540)
    - [CVE-2022-23541](https://nvd.nist.gov/vuln/detail/CVE-2022-23541)
    - [CVE-2022-3996](https://nvd.nist.gov/vuln/detail/CVE-2022-3996)
    - [CVE-2022-43551](https://nvd.nist.gov/vuln/detail/CVE-2022-43551)
    - [CVE-2021-46848](https://nvd.nist.gov/vuln/detail/CVE-2021-46848)
    - [CVE-2022-21698](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-21698)
    - [CVE-2021-44716](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44716)
    - [CVE-2022-27664](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-27664)
    - [CVE-2021-43565](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-43565)
    - [CVE-2021-38561](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-38561)

## 0.31.1

Release date: December 23, 2022

### Additional improvements 

- You can now configure `extraFlags` for the Prometheus startup command in the Prometheus Helm chart.

### Bug fixes 

- Fixed an issue where logging sidecars would occasionally fail to terminate.
- Fixed the following vulnerabilities:
    - [CVE-2021-46848](https://nvd.nist.gov/vuln/detail/CVE-2021-46848)
    - [CVE-2021-44716](https://nvd.nist.gov/vuln/detail/CVE-2021-44716)
    - [CVE-2022-27191](https://nvd.nist.gov/vuln/detail/CVE-2022-27191)
    - [CVE-2022-27664](https://nvd.nist.gov/vuln/detail/CVE-2022-27664)
    - [CVE-2022-32149](https://nvd.nist.gov/vuln/detail/CVE-2022-41717)
    - [CVE-2022-37454](https://nvd.nist.gov/vuln/detail/CVE-2022-37454)
    - [CVE-2022-41717](https://nvd.nist.gov/vuln/detail/CVE-2022-41717)
    - [CVE-2022-42919](https://nvd.nist.gov/vuln/detail/CVE-2022-42919)
    - [CVE-2022-45061](https://nvd.nist.gov/vuln/detail/CVE-2022-45061)
    - [CVE-2022-46146](https://nvd.nist.gov/vuln/detail/CVE-2022-46146)

## 0.31.0

Release date: December 7, 2022

### View and export task usage metrics

You can now view task usage metrics from the Software UI.

Task usage metrics provide an overview of your Airflow task runs and can help you quickly identify Deployments where more tasks are running or failing than expected. 

To configure the feature, see [Set up task usage metrics](task-usage-metrics.md).

### New root user role

Astronomer Software's role-based access control (RBAC) system now supports a single root user for each installation. The root user has a non-configurable username and autogenerated password stored as a Kubernetes secret in your installation. 

See [Manage the root user](https://docs.astronomer.io/software/0.31/manage-root-user#log-in-as-the-root-user).

### Manage Astronomer users through a SCIM integration 

Astronomer Software now supports managing users through System for Cross-domain Identity Management (SCIM), which allows you to automatically provision and deprovision users based on templates for access and permissions. See [Manage users with SCIM](integrate-auth-system.md#manage-users-and-teams-with-scim).

### Invite users only through Teams

Using the new root user feature, you can now configure Astronomer Software so that users are managed exclusively through Teams. This helps you better integrate with your identity provider (IdP) by ensuring that all users on your platform are authenticated and managed through the IdP. See [Disable individual user management](import-idp-groups.md#disable-individual-user-management).

### New default resource limits and requests 

Astronomer Software 0.31 includes new default resource limits and requests on the following resources: 

- Alertmanager
- Elasticsearch
- NATS
- PostrgeSQL
- STAN
- Nginx
- Grafana
- Blackbox exporter

You might experience OOMKill errors or unexpected behavior after upgrading if you use resources beyond the new default limits. To minimize disruption, view resource usage for these components in [Grafana](grafana-metrics.md) prior to upgrade and compare this usage to the default resource limits in the [Astronomer Helm chart](https://github.com/astronomer/astronomer/blob/master/charts/astronomer/values.yaml). 

If your current usage is expected and higher than the default resource limits, update the limits in your `config.yaml` file before upgrading to Astronomer Software 0.31.

### Additional improvements 

- You can now set a custom security context for `es-client` by setting `elasticsearch.client.securityContext.capabilities.add={}` in the ElasticSearch Helm chart.
- The **Deployment users** page is now paginated in the Software UI.
- You can now set `astronomer.registry.logLevel` to filter which types of logs appear in your Docker registry.
- The default Git-sync interval is now 1 instead of 0.
- You can now configure a Deployment to have 0 triggerer components.
- You can now set `astronomer.houston.config.useAutoCompleteForSensativeFields=false` to disable autocomplete on sensitive fields in the Software UI.
- You can now set `astronomer.houston.config.shouldLogUsername=true` to include user email addresses in audit logs for logins through the Houston API.
- [Git sync-based Deployments](deploy-git-sync.md) now have a dedicated git-sync relay pod, service, and network policy.
  
### Bug fixes

- The Software UI now stores user tokens with `httpOnly` and `secure` flags.
- Fixed an issue where the Software UI would occasionally show an incorrect **Extra AU** number for Deployments. 
- Fixed the following vulnerabilities:

    - [CVE-2022-37601](https://security.snyk.io/vuln/SNYK-JS-LOADERUTILS-3043105)
    - [CVE-2022-43680](https://nvd.nist.gov/vuln/detail/CVE-2022-43680)
    - [CVE-2022-40674](https://nvd.nist.gov/vuln/detail/CVE-2022-40674)
  
- Fixed an issue where you could not access Astronomer Software's Docker registry if you had access to more than 100 Deployments. 
- Fixed an issue where the Software UI did not show the correct last used dates for service accounts. 
- Fixed an issue where NATS would send false Deployment alert emails.
- Fixed an issue where the configuration in `astronomer.houston.updateRuntimeCheck.url` was ignored if not all supported Deployment image versions were present in the destination URL. 
