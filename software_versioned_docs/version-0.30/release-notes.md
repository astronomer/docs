---
title: 'Astronomer Software v0.30 release notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

<!--- Version-specific -->

0.30 is the latest stable and long-term support (LTS) version of Astronomer Software. To upgrade to 0.30, see [Upgrade Astronomer](upgrade-astronomer.md). For more information about Software release channels, see [Release and lifecycle policies](release-lifecycle-policy.md). To read release notes specifically for the Astro CLI, see [Astro CLI release notes](cli-release-notes.md). For more Astronomer Software release notes, see:

- [Astro CLI release notes](https://docs.astronomer.io/astro/cli/release-notes)
- [Astro Runtime release notes](https://docs.astronomer.io/astro/runtime-release-notes)
- [Astronomer Software 0.31 release notes](https://docs.astronomer.io/software/release-notes)
- [Astronomer Software documentation archive](documentation-archive.md)

## 0.30.7

Release date: May 25, 2023

### Additional improvements

- You can now configure custom environment variables for ElasticSearch-based custom logging using the `astronomer.customLogging.extraEnv` value in your `config.yaml` file.
- You can now configure `prometheus.config.scrape_configs.kubernetes_apiservers.tls_config.insecure_skip_verify` in the Prometheus Helm chart.
- You can now set `astronomer.houston.config.deployments.helm.prometheus.certgenerator.extraAnnotations` in your `config.yaml` file.
- You can now configure a custom indexing pattern for [Vector logging sidecars](export-task-logs.md#export-logs-using-container-sidecars) by setting both `elasticsearch.curator.age.timestring` and `astronomer.houston.config.deployments.helm.loggingSidecar.indexPattern` in your `config.yaml` file.
- All users other than System Admins can no longer create Deployments with Astronomer Certified images. The Software UI will show a warning message for Deployments currently running an Astronomer Certified image.
- Grafana now includes an **Astronomer Houston Dashboard** that you can use to view Houston metrics. 

### Bug fixes

- Fixed an issue where container status and usage did not appear in the **Metrics** tab for Deployments with pre-created namespaces.
- Fixed a security vulnerability in logging.
- Fixed an issue where sidecar containers would sometimes not terminate properly after their primary container was terminated.
- Fixed an issue where Prometheus was using more memory than expected due to a misconfiguration of statsd.
- Fixed an issue where a service account with the Workspace Editor role could update a Deployment when it didn't have any Deployment-level permissions for the Deployment. 
- Fixed an issue in the Software UI where you could not view Deployment details for a Deployment that included "team" in its name.
- Fixed the following vulnerabilities: 
  
    - [CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840)
    - [CVE-2023-27536](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-27536)
    - [CVE-2023-27533](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-27533)
    - [CVE-2023-27534](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-27534)
    - [CVE-2023-27535](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-27535)
    - [CVE-2023-0464](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0464)
    - [CVE-2023-27561](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-27561)
    - [CVE-2022-27664](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-27664)
    - [CVE-2022-41721](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-41721)
    - [CVE-2022-41723](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-41723)
    - [CVE-2022-32149](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-32149)
    - [CVE-2020-25649](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-25649)
    - [CVE-2020-36518](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-36518)
    - [CVE-2022-42003](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42003)
    - [CVE-2022-42004](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-022-42004)
    - [CVE-2022-3171](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3171)
    - [CVE-2022-3509](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3509)
    - [CVE-2022-3510](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3510)
    - [CVE-2022-25857](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25857)
    - [CVE-2022-42898](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42898)

## 0.30.6

Release date: March 2, 2023

### Additional improvements

- Support for Kubernetes [1.25](https://kubernetes.io/blog/2022/08/23/kubernetes-v1-25-release/) and [1.26](https://kubernetes.io/blog/2022/12/09/kubernetes-v1-26-release/).
- You can now configure `extraVolumes` and `extraVolumeMounts` in the Alertmanager Helm chart, which can be useful for storing secret credentials for services that read your alerts.

### Bug fixes 

- Fixed a security vulnerability where you could query Elasticsearch logs for a Deployment from a different Deployment.
- Fixed an issue where deploying an image with the `docker/build-push-action` GitHub action could produce errors in Houston that affected the entire Astronomer Software installation.
- Fixed an issue where authentication tokens were visible in Nginx logs produced by the Software UI.
- Fixed the following vulnerabilities: 
  
    - [CVE-2023-24807](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-24807)
    - [CVE-2023-0286](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0286)
    - [CVE-2023-25881](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-25881)
    - [CVE-2022-27664](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-27664)
    - [CVE-2022-41721](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41721)
    - [CVE-2022-32149](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-32149)
    - [CVE-2022-23529](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23529)
    - [CVE-2021-44906](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44906)
    - [CVE-2022-23540](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23540)
    - [CVE-2022-23541](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23541)

## 0.30.5

Release date: January 11, 2023

### Additional improvements 

- You can now set `timeoutSeconds` for both `readinessProbe` and `livenessProbe` in the Prometheus Helm chart.
- You can now roll back from Software version 0.30 to 0.28.

### Bug fixes 

- Fixed the following vulnerabilities: 
  
    - [CVE-2022-3996](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3996)
    - [CVE-2022-43551](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-43551)
    - [CVE-2021-44716](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44716)
    - [CVE-2022-2625](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2625)
    - [CVE-2022-37454](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-37454)
    - [CVE-2022-42919](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42919)
    - [CVE-2022-45061](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-45061)
    - [CVE-2022-43680](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-43680)
    - [CVE-2017-11468](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-11468)
    - [CVE-2022-21698](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-21698)
    - [CVE-2022-27664](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-27664)
    - [CVE-2022-46146](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-46146)
    - [CVE-2022-32149](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-27664)
    - [CVE-2022-27191](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-27191)
    - [CVE-2022-37601](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-37601)
    - [CVE-2021-43565](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-43565)
    - [CVE-2021-38561](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-38561)

- Fixed an issue where PgBouncer didn't work if you pulled its image from a private registry.
- Fixed an issue where the Software UI would occasionally show an incorrect **Extra AU** number for Deployments. 
- Fixed an issue where users who had access to more than 100 Deployments could not access the Astronomer Software Docker registry.
- Fixed an issue where Deployments with many DAGs could not be successfully upgraded due to a short timeout.
- Fixed an issue where users couldn't log in through Azure Active Directory (AD) if they belonged to more than 100 teams.
- Fixed an issue where service accounts with System Admin permissions could not create Deployments for deprecated Airflow versions. 
- Fixed an issue where you could not set `AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER` in a Deployment if you were using an Astronomer Certified image.
- Fixed an issue in the Software UI where refreshing pages listing Workspace or Deployment service accounts resulted in an error.
- Fixed an issue where logging sidecars would occasionally fail to terminate.
- Fixed an issue where NATS would send false Deployment alert emails.

## 0.30.4 

Release date: November 3, 2022 

### Bug fixes 

- Fixed the following vulnerabilities: 
  
    - [CVE-2022-42915](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42915)
    - [CVE-2022-32190](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-32190)
    - [CVE-2022-14809](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-14809)
    - [CVE-2022-14271](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-14271)
    - [CVE-2022-1996](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1996)
  
- Fixed an issue where `astronomer.houston.updateRuntimeCheck.url: true` was ignored when searching for new Astronomer Certified and Astro Runtime images. 

## 0.30.3

Release date: October 26, 2022

### Additional improvements

- You can now configure custom Alertmanager receivers with their own rules and topics using `customReceiver` in the Alertmanager Helm chart.
- You can now limit which Runtime versions are available for new Deployments using `astronomer.minAstroRuntimeVersion` and `astronomer.airflowMinimumAstroRuntimeVersion` in your `config.yaml` file.
- You can now configure a `livenessProbe` and `readinessProbe` specific to Prometheus in the Prometheus Helm chart.
- You can now pass extra environment variables to [logging sidecars](export-task-logs.md#configure-logging-sidecars) using `global.loggingSidecar.extraEnv` in your `config.yaml` file.  
- You can now define resource requests for [logging sidecars](export-task-logs.md#configure-logging-sidecars) using `global.loggingSidecar.resources` in your `config.yaml` file. 
- You can now configure whether introspection APIs are available in GraphQL using `astronomer.apollo.introspection` in your `config.yaml` file.

### Bug fixes

- Fixed an issue where upgrading Astronomer Software with a custom `houston.deployments.components` value in Helm could make the Software UI unavailable.
- Fixed an issue where the Software UI didn't show the correct value for **Extra Capacity**.
- Fixed an issue where upgrading a Deployment from Airflow 1.10.15 to 2.3 prevented you from configuring Deployment resources in the Software UI.
- Added protections for using Arm-based Runtime images in Software Deployments.
- Fixed an issue where some Deployments failed when pulling secrets from a private Docker registry.
- Fixed an issue where some email alerts for unhealthy Deployments would not send if `namespaceFreeFormEntry: true` was set in `config.yaml`.
- Fixed an issue where you could not view Deployment-level service accounts in the Software UI.
- Fixed an issue where token refreshing could break when the token didn't have a properly formatted date.
- Suppressed some extraneous ElasticSearch logs that made parsing logs for relevant information difficult.
- Fixed the following vulnerabilities:
    - [CVE-2022-40674](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40674)
    - [CVE-2022-41816](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41816)
    - [CVE-2022-2900](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2900)
    - [CVE-2022-3224](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3224)

## 0.30.2

Release date: September 22, 2022

### Additional improvements

- You can now use the [Fluentd Helm chart](https://github.com/astronomer/astronomer/blob/master/charts/fluentd/values.yaml) to set a `securityContext` for Fluentd Pods and containers.
- Improved the startup time for the platform NATS server.
- You can now configure external containers in the `astronomer.houston.config` section of the Astronomer Helm chart.

### Bug fixes

- Fixed several CVEs as a result of updating images for system components. 

## 0.30.1

Release date: September 12, 2022

### Bug fixes

- Fixed the following vulnerabilities:
    - [CVE-2022-1996](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1996)
    - [CVE-2022-21698](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-21698)
    - [CVE-2022-35949](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-35949)
    - [CVE-2022-35948](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-35948)
    - [CVE-2022-37434](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-37434)

## 0.30.0

Release date: August 29, 2022

:::danger Breaking Change for Azure Database for PostgreSQL

A change in 0.30 enabled the `trgm` extension for PostgreSQL. If you use Azure Database for PostgreSQL as your database backend, you need to enable the `pg_trgm` extension before upgrading to Software 0.30 using either Azure portal or the Azure CLI. See [Azure documentation](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions) for configuration steps.

If you don't complete this setup before your upgrade, the upgrade will fail.

:::

### Improved token refreshing for IdP integrations

The Software UI now refreshes your JSON web token (JWT) based on the validity of your authentication token from your IdP. This means that as long as you stay logged in to your IdP, you no longer have to refresh the Software UI to continue accessing the Software UI, Astro CLI, and Houston API.

Additionally, if you change a user's access to Astronomer from your IdP, their permissions will be automatically updated in Astronomer after their current IdP token expires. If you remove a user completely from Astronomer, they are automatically logged out of the Software UI and CLI after their current IdP token expires.

As part of this change, you can now configure `jwt.authDuration` in your [Houston Helm configuration](https://github.com/astronomer/docs/blob/main/software_configs/0.30/default.yaml). If a user is logged on longer than `authDuration`, they will be immediately logged out regardless of the status of their JWT or authentication token.

### Additional improvements

- Workspace users are now paginated in the Software UI.
- You can now configure credentials for a private image registry by specifying a secret you create instead of a username and password. The secret is attached to any Pods that need to access the registry.
- You can now specify `authUrlParams` for your identity provider (IdP) in `config.yaml`.
- System Editors can no longer manage Teams or users in a Workspace. These permissions are now available only at the System Admin level.

### Bug fixes

- Fixed an issue where `updateRuntimeCheck.enabled:false` did not properly stop an Astronomer Software installation from checking for Runtime updates. 
- Fixed an issue where applying an IAM role to a Deployment would reset the Deployment's **Extra Capacity** setting back to the default of 0 AU.
- Fixed an issue where System Admins could receive an error when trying to view a Team imported from a different IdP than their current one.
- When a System Admin makes a change to a Team, that change now appears in the UI without needing to refresh the page.
- Configurations for disabling a specific executor type in `config.yaml` are now reflected in the Software UI.
- Fixed an issue where Workspace-level service accounts could view Deployment information from Deployments outside of their Workspace.
- Fixed an issue where updating the role of a user in a Team using the Astro CLI would not throw an error as expected.
- Fixed an issue where JSON web tokens persisted after a user logged out if `idpGroupsRefreshEnabled` was set to `false`.
- Users authenticating with Google Direct are no longer automatically logged out of Astronomer Software after 1 hour.
