---
title: 'Astronomer Software release notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

This document contains release notes for each version of Astronomer Software.

This page contains release notes for all recent Astronomer Software versions. 

0.33 is the latest stable version of Astronomer Software, while 0.32 remains the latest long-term support (LTS) release. To upgrade to 0.33, see [Upgrade Astronomer](upgrade-astronomer.md). For more information about Software release channels, see [Release and lifecycle policies](release-lifecycle-policy.md). To read release notes specifically for the Astro CLI, see [Astro CLI release notes](https://docs.astronomer.io/astro/cli/release-notes).

:::info 

Because Astronomer has separate [maintenance life cycles](release-lifecycle-policy.md) for each minor version of Astronomer Software, a later patch version of Astronomer Software is not guaranteed to have all changes included in previous minor versions. When a release note appears more than once on this page, the related change was introduced to multiple minor versions of Astronomer Software at different times. 

If you're upgrading to receive a specific change, ensure the release note for the change appears either:

- Within your target minor version.
- In a patch version that was released before the first release of your target minor version. For example, a change in 0.32.5, which released 12/8/2023, is not guaranteed to appear in the 0.33 series, which released 9/8/2023, unless there is a release note for it in an 0.33 patch.

:::

## 0.33.2 

Release date: November 20, 2023

### Change to behavior for interacting with deprecated Runtime versions

In 0.33.2, non-System Admin users can now update Deployments using deprecated versions of Astro Runtime. By default, non-System Admin users can now interact with Deployments using deprecated Runtime versions, but only System Admins can create new Deployments with deprecated Runtime versions. As a result of this change, the `enableSystemAdminCanUseNonSupportedRuntime` key has been replaced with `enableSystemAdminCanUseAllRuntimes`. To set the new flag, add the following configuration to your `config.yaml` file:

```yaml
astronomer:
   houston:
      config:
         deployments:
            enableSystemAdminCanUseAllRuntimes: true   
```

### Additional improvements

- You can now configure a global index name prefix to use for both Fluentd and sidecar-based logging, which allows Astronomer Software to retain logs when you migrate between logging solutions. To enable this feature, add the following lines to your `config.yaml` file:

    ```yaml
    global:
       logging:
          indexNamePrefix: <your-index-prefix>
    ```
- Deprecated Kubernetes 1.23

### Bug fixes

- Fixed an issue where deploys were failing for Deployments that used older versions of the Airflow Helm chart.
- Fixed an issue where some dashboards in Grafana were not visible if you didn't manually log in to Grafana as an admin.
- Fixed an issue where the Software UI showed Deployments as healthy even if the triggerer Pod was down.
- Fixed an issue where you couldn't search for a user in the Software UI by their user ID.
- Fixed an issue where the `invites` query returned an error instead of an empty array when no users invites were found.
- Fixed the following vulnerabilities:

    - [CVE-2023-43787](https://nvd.nist.gov/vuln/detail/CVE-2023-43787)
    - [GHSA-m425-mq94-257g](https://github.com/advisories/GHSA-m425-mq94-257g)
    - [CVE-2023-32002](https://nvd.nist.gov/vuln/detail/CVE-2023-32002)
    - [CVE-2023-32006](https://nvd.nist.gov/vuln/detail/CVE-2023-32006)
    - [CVE-2023-32559](https://nvd.nist.gov/vuln/detail/CVE-2023-32559)
    - [CVE-2023-36665](https://nvd.nist.gov/vuln/detail/CVE-2023-36665)
    - [CVE-2023-24540](https://nvd.nist.gov/vuln/detail/CVE-2023-24540)
    - [CVE-2023-24538](https://nvd.nist.gov/vuln/detail/CVE-2023-24538)
    - [CVE-2023-45133](https://nvd.nist.gov/vuln/detail/CVE-2023-45133)
    - [CVE-2022-48174](https://nvd.nist.gov/vuln/detail/CVE-2023-48174)
    - [CVE-2023-39320](https://nvd.nist.gov/vuln/detail/CVE-2023-39320)
    - [CVE-2023-29402](https://nvd.nist.gov/vuln/detail/CVE-2023-29402)
    - [CVE-2023-29404](https://nvd.nist.gov/vuln/detail/CVE-2023-29404)
    - [CVE-2023-29405](https://nvd.nist.gov/vuln/detail/CVE-2023-29405)

## 0.33.1

Release date: October 13, 2023

### Additional improvements

- You can now set `astronomer.auth.microsoft.useExternalProxy: false` in your `config.yaml` file to bypass proxy support for Azure logins.
- You can now list System-level Service Accounts using the Houston API.
- You can now configure a service account specifically for your image registry using by setting `astronomer.registry.serviceaccount` in your `config.yaml` file.
- The Kibana logging dashboard now includes a default index. 

### Bug fixes

- Fixed an issue where if you queried a Deployment name that belonged to two different Deployments in two different Workspaces, the Houston API might retrieve the unintended Deployment. 
- Fixed an issue where you could create users with the Houston API when SCIM was enabled and `userManagement.enable` was `false`.
- Fixed an issue where some dashboards on Grafana didn't load properly.
- Fixed an issue where the Houston API `CreateDeployment` request would return a successful response even though no Deployment was created due to no specified Airflow version.
- Fixed an issue where a System Admin user that did not belong to a Team could delete the Team from the Software UI.
- Fixed an issue where syncing an IdP group from Okta failed when SCIM was enabled and a user account was removed only from Astronomer Software.
- Fixed an issue where adding a user through SCIM provisioning that already exists on an Astronomer Software Azure cluster would throw an error instead of updating the existing user.
- Fixed an issue where the user login process would be unresponsive if the Houston API failed to retrieve IdP group information from Azure.
- Fixed an issue where the Software UI would show Deployments as healthy even when triggerer Pods were failing.
- Fixed an issue where a user who was deleted from Astronomer Software would not appear when they were reinvited through a Team.
- Fixed an issue where the System Admin page in the Software UI had entries that didn't fit the page.
- Astronomer Software now throws an error if you attempt to install it with an unsupported version of Kubernetes.
- Fixed an issue where using the Houston API to query for a Deployment that didn't exist returned a non-descriptive error.
- Fixed an issue where `ap-blackbox-exporter` did not respect global network policies.
- Fixed the following vulnerabilities:

    - [CVE-2023-38325](https://nvd.nist.gov/vuln/detail/CVE-2023-38325)
    - [CVE-2023-4863](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-4863)
    - [CVE-2023-37788](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37788)
    - [CVE-2023-37920](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37920)
    - [CVE-2023-36665](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-36665)
    - [CVE-2023-26115](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-26115)
    - [CVE-2023-29526](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-29526)
    - [CVE-2022-48174](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-48174)
    - [CVE-2022-2253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2253)
    - [CVE-2017-11468](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-11468)
    - [CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840)
    - [CVE-2023-2976](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2976)
    - [CVE-2023-1370](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1370)
    - [CVE-2021-40690](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-40690)
    - [CVE-2023-40577](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-40577)
    - [CVE-2022-41721](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41721)
    - [CVE-2023-25653](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-25653)
    - [CVE-2022-21698](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-21698)
    - [CVE-2021-33194](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-33194)
    - [CVE-2021-38561](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-38561)
    - [CVE-2023-25653](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-25653)
    - [CVE-2023-25653](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-25653)
    - [CVE-2023-25653](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-25653)
    - [CVE-2023-25653](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-25653)
    - [CVE-2023-25653](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-25653)


## 0.33.0

Release date: September 8, 2023

### Automatic PGBouncer connection scaling

Astronomer Software can now automatically scale the size of PGBouncer connection pools based on your Airflow component counts and Airflow configuration, instead of solely based on total AU. This improves performance, scalability, and utilization of database connections across all Deployments. 

This feature is off by default. You can enable it by setting  `deployments.pgBouncerResourceCalculationStrategy: airflowStratV2` in your `config.yaml` file. To revert back to previous behavior, set this key to `auStratV1` instead.

### Additional improvements

- You can now disable Airflow and platform alerts on the Prometheus alerts dashboard by setting `prometheus.defaultAlerts.airflow.enabled` and `prometheus.defaultAlerts.airflow.enabled` to `false` in your Prometheus Helm chart. If you disable these alerts, you can still add back specific alerts or configure custom alerts using `prometheus.defaultAlerts.additionalAlerts`. See [Create custom alerts](platform-alerts.md#create-custom-alerts).
- Added support for [Kubernetes 1.27](https://kubernetes.io/blog/2023/04/11/kubernetes-v1-27-release/).
- The Workspace **Deployments** page is now paginated in the Astronomer UI.
- The **Extra Capacity** field in the Astronomer UI now shows up to 6 digits of AU.
- You no longer have to set `elasticsearch.curator.age.timestring` when you configure a custom indexing pattern for [Vector logging sidecars](export-task-logs.md#export-logs-using-container-sidecars). The only required value is now `astronomer.houston.config.deployments.helm.loggingSidecar.indexPattern`.
- When you create or update a Deployment and select a Runtime version, the Astronomer UI now shows only the latest supported Astro Runtime patch for each supported Astro Runtime major version.
- You can now set `deployments.canUpsertDeploymentFromUI: false` to prevent all users besides System Admins from updating Deployments and environment variables through the Astronomer UI.
- You can now [overprovision](cluster-resource-provisioning.md) the `triggerer-log-groomer` component.

### Bug fixes

- Fixed an issue where a Deployment using Runtime 8 or earlier with the Celery executor would show as healthy in the Software UI even when workers were unavailable.
- Fixed an issue where Grafana could not start up on an OpenShift cluster.
- Fixed an issue where configurations in `astronomer.houston.config.deployments.components` applied only to Deployments that were created after the configuration was set. 
- Fixed an issue where a Workspace-level service account would improperly inherit lesser permissions for Deployments it was added to.
- The Astronomer UI now shows an error if you click the **Delete** button for Teams and you don't have the `system.teams.remove` permission.
- Fixed an issue where you couldn't upgrade a Deployment's Airflow version if the Deployment used git-sync deploys and had default resources.
- Fixed an issue where you could get a 500 internal server error from the Airflow UI when switching between pages for a DAG.
- Fixed an issue where you couldn't set `properties.email` using the `upsertDeployment` mutation.
- Fixed an issue where the Astronomer UI would not show the right error screen when a user without the appropriate permissions viewed service accounts. 
- Fixed the following vulnerabilities:

    - [CVE-2023-35945](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-35945)
    - [CVE-2023-37920](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37920)
    - [CVE-2023-2253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2253)
    - [CVE-2023-39417](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-39417)
    - [CVE-2023-37920](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37920)
    - [CVE-2023-35945](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-35945)

## 0.32.5

Release date: December 8, 2023

### Additional improvements

- You can now configure a global index name prefix to use for both [Fluentd and sidecar-based logging](export-task-logs.md), which allows Astronomer Software to retain logs when you migrate between logging solutions. To enable this feature, add the following lines to your `config.yaml` file:

    ```yaml
    global:
      logging:
        indexNamePrefix: <your-index-prefix>
    ```
    
- Deprecated Kubernetes 1.23.
- Astronomer Software now throws an error if you attempt to install it with an unsupported version of Kubernetes.
- You can now set the following configuration to bypass proxy support when Astronomer Software redirects to Azure login. This might be required in some circumstances when importing identity provider groups as Teams: <!-- https://github.com/astronomer/issues/issues/5844 -->

    ```yaml
    astronomer:
      houston:
        config:
          auth:
            microsoft:
              useExternalProxy: false
    ```

### Bug fixes

- Fixed an issue where using the Houston API to query for a Deployment that didn't exist returned a non-descriptive error.
- Fixed an issue where you couldn't update the value for an existing secret environment variable.
- Fixed an issue where you couldn't search for a user in the Software UI by their user ID.
- Fixed an issue where you couldn't access Grafana or Kibana on GKE V2 clusters <!-- https://github.com/astronomer/issues/issues/5963-- >
- Fixed an issue where the `invites` query returned an error instead of an empty array when no users invites were found.
- Fixed the following vulnerabilities:
    - [CVE-2023-39325](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-39325)
    - [CVE-2023-5363](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-5363)
    - [CVE-2023-43787](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-43787)
    - [CVE-2023-4911](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-4911)
    - [CVE-2023-5678](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-5678)
    - [CVE-2023-37788](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37788)
    - [CVE-2023-32002](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-32002)
    - [CVE-2023-32006](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-32006)
    - [CVE-2023-32559](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-32559)
    - [CVE-2022-37434](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-37434)
    - [CVE-2022-48174](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-48174)
    - [CVE-2023-39320](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-39320)
    - [CVE-2023-29402](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-29402)
    - [CVE-2023-29404](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-29404)
    - [CVE-2023-29405](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-29405)
    - [CVE-2023-37788](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37788)
    - [CVE-2023-40577](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-40577)
    - [CVE-2023-2253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2253)
    - [CVE-2022-41721](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41721)

## 0.32.4

Release date: October 19, 2023

### Additional improvements

You can now create a default Kibana index when installing Software. 

### Bug fixes

- Fixed an issue where `ap-blackbox-exporter` did not respect global network policies.

- Fixed the following vulnerabilities:
    - [CVE-2023-4863](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-4863)
    - [CVE-2023-4911](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-4911)
    - [CVE-2023-11468](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-11468)
    - [CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840)
    - [CVE-2023-29491](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-29491)
    - [CVE-2023-37788](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37788)
    - [CVE-2023-37920](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37920)
    - [CVE-2023-38039](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-38039)
    - [CVE-2023-38325](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-38325)
    - [CVE-2023-38545](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-38545)
    - [CVE-2023-39417](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-39417)
    - [CVE-2023-41721](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-41721)
    - [CVE-2023-44487](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-44487)
    - [CVE-2023-45133](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-45133)
    - [CVE-2023-48174](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-48174)
    - [CVE-2021-33194](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-33194)
    - [CVE-2021-38561](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-38561)
    - [CVE-2023-40577](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-40577)

## 0.32.3

Release date: August 31, 2023

### Additional improvements

- You can now disable Airflow and platform alerts on the Prometheus alerts dashboard by setting `Values.defaultAlerts.airflow.enabled` and `prometheus.defaultAlerts.platform.enabled` to `false` in your Prometheus Helm chart. If you disable these alerts, you can still add back specific alerts or configure custom alerts using `prometheus.defaultAlerts.additionalAlerts`. See [Create custom alerts](platform-alerts.md#create-custom-alerts).
- You no longer have to set `elasticsearch.curator.age.timestring` when you configure a custom indexing pattern for [Vector logging sidecars](export-task-logs.md#export-logs-using-container-sidecars). The only required value is now `global.loggingSidecar.indexPattern`.
- You can now configure a service account specifically for your image registry using by setting `astronomer.registry.serviceaccount` in your `config.yaml` file.
- You can now [overprovision](cluster-resource-provisioning.md) the `triggerer-log-groomer` component.
- You can now set `astronomer.houston.enableHoustonInternalAuthorization` in your `config.yaml` file to redirect all authorization requests from the ingress controller to the Houston API internal service endpoint. This can increase performance and decrease network latency.
- Upgraded ElasticSearch to 8.x.
- Added support for [Kubernetes 1.27](https://kubernetes.io/blog/2023/04/11/kubernetes-v1-27-release/).

### Bug fixes

- Fixed an issue where Helm changes to statsd Pod resources would apply only to new Deployments.
- Fixed an issue where Grafana could not start up on an OpenShift cluster.
- Fixed an issue where a Deployment using Runtime 8 or earlier with the Celery executor would show as healthy in the Software UI even when workers were unavailable.
- Fixed an issue where a System Admin user that did not belong to a Team could delete the Team from the Software UI.
- Fixed an issue where syncing an IdP group from Okta failed when SCIM was enabled and a user account was removed only from Astronomer Software.
- Fixed an issue where you couldn't upgrade a Deployment's Airflow version if the Deployment used git-sync deploys and had default resources.
- Fixed an issue where the user login process would be unresponsive if the Houston API failed to retrieve IdP group information from Azure.
- Fixed the following vulnerabilities:

    - [CVE-2023-37920](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37920)
    - [CVE-2023-35945](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-35945)
    - [CVE-2023-36665](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-36665)
    - [CVE-2023-2650](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2650)

## 0.32.2

Release date: June 23, 2023

### Bug fixes

- Reverted a change which prevented Workspace-level service accounts from accessing a Deployment when the service account didn't have specific permissions for that Deployment.
- Fixed an issue where some screens of the Airflow UI would produce an HTTP 500 internal server error.

## 0.32.1

Release date: June 12, 2023

### Additional improvements

- [Overprovisioning](cluster-resource-provisioning.md) now also applies to the following components:

    - PGBouncer
    - Statsd
    - Flower
  
- You can now configure `astronomer.houston.config.deployments.overProvisioningComponents` to limit the scope of [overprovisioning](cluster-resource-provisioning.md) only to specific Airflow components.
- Teams without any users are now automatically deleted when SCIM is disabled.
- You can now authenticate to an external storage service for [archiving task metadata](configure-deployment.md#clean-deployment-task-metadata) using Workload Identity.
- You can now set `prometheus.config.scrape_configs.kubernetes_apiservers.tls_config.insecure_skip_verify` in the Prometheus Helm chart.
- You can now set `astronomer.houston.config.deployments.helm.prometheus.certgenerator.extraAnnotations` in your `config.yaml` file.
- You can now configure credentials for a registry backend as Kubernetes secrets in your `config.yaml` file. See [Configure a registry backend](registry-backend.md).

### Bug fixes

- Fixed an issue where `git-sync-relay` containers wouldn't restart as expected after being terminated.
- Fixed an issue where a service account with the Workspace Editor role could update a Deployment when it didn't have any Deployment-level permissions for the Deployment. 
- Fixed an issue where data for **Disk Usage** and **Platform Overview** did not appear in Grafana.
- System Admins can no longer change a user's system role if the user is imported to Astronomer through an IdP group and `manageSystemPermissionsViaIdpGroups` is set to `true`.
- Fixed an issue where you could not create a new Deployment from the Cloud UI if you updated its scheduler count using the text-based input field. 
- Fixed an issue where container status and usage did not appear in the **Metrics** tab for Deployments with pre-created namespaces.
- Fixed an issue where resource requests configured from the Software UI could get out of sync with the Houston database.
- Fixed an issue where where updating a Deployment's resource configuration did not persist in the Houston database when that Deployment had overprovisioning enabled.
- Reduced the number of redundant calls that Astronomer Software makes to your identity provider (IdP) when a user logs in.
- Fixed a security vulnerability in logging.
- Fixed the following vulnerabilities:

    - [CVE-2023-29491](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-29491)
    - [CVE-2023-1999](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1999)
    - [CVE-2023-27561](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-27561)
    - [CVE-2022-41727](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-41727)
    - [CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840)
    - [CVE-2023-2650](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2650)

## 0.32.0

Release date: April 28, 2023

### Clean Deployment task metadata

You can now clean task data from your Deployments by exporting it to an external storage service. This workflow reduces the amount of data Airflow stores in your Deployment metadata database by archiving data that you don't need to access on a regular basis. To configure this job, see [Clean Deployment task metadata](configure-deployment.md#clean-deployment-task-metadata).

### Programmatically create and update Deployments with the Houston API

You can now programmatically create or update Deployments using the Houston API `upsertDeployment` mutation. Unlike `createDeployment`, the `upsertDeployment` mutation includes keys for configuring Deployment resources such as environment variables. See [Create or update a Deployment with configurations](houston-api.md#create-or-update-a-deployment-with-configurations).

### Reduce resource requests for Airflow components in development environments

You can reduce the amount of CPU and memory that an Airflow component requests in development environments, allowing you to more efficiently provision resources based on the requirements for your development Deployments. See [Underprovision Airflow resources](cluster-resource-provisioning) for configuration steps.

### New cron job to clean Deployment task data

You can now clean task data from your Deployments by exporting it to an external storage service. This workflow reduces the amount of storage Astronomer Software uses by archiving data that you don't need to access on a regular basis. See [Configure a Deployment](configure-deployment.md#clean-deployment-task-metadata) for configuration steps.

### Assign System-level permissions to Teams

You can assign the System Admin, System Editor, and System Viewer permissions to teams by setting the following values in your `config.yaml` file:

```sh
# Auth configuration.
auth:
  openidConnect:
    idpGroupsImportEnabled: true
    # Optional configuration. Set to assign System-level permissions using Teams.
    manageSystemPermissionsViaIdpGroups:
      enabled: true
      systemAdmin: ["<your-system-admin-groups>"] // Only these groups will be treated as SysAdmin Groups
      systemEditor: ["<your-system-editor-groups>"]
      systemViewer: ["<your-system-viewer-groups>"]
```

When coupled with [disabling individual user management](import-idp-groups.md#disable-individual-user-management), this feature allows you to control all user permissions on Astronomer Software exclusively through your identity provider. For more information, see [Import IdP groups](import-idp-groups.md).

### PostgreSQL 15

Astronomer Software version 0.32 upgrades PostgreSQL from 11.18.0-1 to 15. If you use in-cluster PostgreSQL for your workflows, upgrading to Software 0.32 without pinning your PostgreSQL version can impact your workflows. See the [Upgrade to Postgres 15](upgrade-astronomer.md#upgrade-to-postgres-15) for upgrade considerations and steps.

### Additional improvements

- Added support for using git-sync with a private image registry.
- The root user feature introduced in Astronomer Software version 0.31 has been deprecated. System Admins now have the highest level of permissions on the platform.
- Workspaces are now required to have unique names. If you have existing Workspaces with identical names, upon upgrade the duplicate names will be appended with an underscore and a number.
- If you configured [git-sync deploys](deploy-git-sync.md) for a Deployment, you can now [view error logs](deployment-logs.md) emitted from the git-sync Kubernetes Pod in the Software UI.
- You can now configure a custom indexing pattern for [Vector logging sidecars](export-task-logs.md#export-logs-using-container-sidecars) by setting both `elasticsearch.curator.age.timestring` and `astronomer.houston.config.deployments.helm.loggingSidecar.indexPattern` in your `config.yaml` file.
- You can now configure custom environment variables for ElasticSearch-based custom logging using the `astronomer.customLogging.extraEnv` value in your `config.yaml` file.
- The `astronomer.houston.config.deployments.sysAdminScalabilityImprovementsEnabled` key has been replaced with `astronomer.houston.config.deployments.performanceOptimizationModeEnabled`  for improved performance across additional Software UI views.

### Bug fixes

- Fixed an issue where ElasticSearch Curator version 7 and later did not work as expected.
- Fixed an issue where sidecar containers would sometimes not terminate properly after their primary container was terminated.
- Fixed an issue in the Software UI where you could not view Deployment details for a Deployment that included "team" in its name.
- Fixed an issue where a service account with Workspace Editor permissions could update Deployments. 
- Fixed an issue where Prometheus was using more memory than expected due to a misconfiguration of statsd.
Fixed an issue in the Software UI where a text search returned duplicate entries for a single Deployment name.
- Fixed an issue where authentication tokens were visible in Nginx logs produced by the Software UI.
- Fixed the following vulnerabilities:

    - [CVE-2022-46146](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-46146)
    - [CVE-2022-27664](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-27664)
    - [CVE-2021-32149](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-32149)
    - [CVE-2021-2625](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-2625)
    - [CVE-2023-0286](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0286)
    - [CVE-2023-25881](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-25881)
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
    - [CVE-2022-3970](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3970)  

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

## 0.30.8

Release date: September 15, 2023

### Additional improvements

- You can now configure credentials for a registry backend as Kubernetes secrets in your `config.yaml` file. See [Configure a registry backend](registry-backend.md).
- You can now disable Airflow and platform alerts on the Prometheus alerts dashboard by setting `prometheus.defaultAlerts.airflow.enabled` and `prometheus.defaultAlerts.airflow.enabled` to `false` in your Prometheus Helm chart. If you disable these alerts, you can still add back specific alerts or configure custom alerts using `prometheus.defaultAlerts.additionalAlerts`. See [Create custom alerts](platform-alerts.md#create-custom-alerts).
- You no longer have to set `elasticsearch.curator.age.timestring` when you configure a custom indexing pattern for [Vector logging sidecars](export-task-logs.md#export-logs-using-container-sidecars). The only required value is now `astronomer.houston.config.deployments.helm.loggingSidecar.indexPattern`. 
- You can now configure a service account specifically for your image registry using by setting `astronomer.registry.serviceaccount` in your `config.yaml` file. 
- The Kibana logging dashboard now includes a default index. 
- Added support for [Kubernetes 1.27](https://kubernetes.io/blog/2023/04/11/kubernetes-v1-27-release/).

### Bug fixes

- Fixed an issue where if you queried a Deployment name that belonged to two different Deployments in two different Workspaces, the Houston API might retrieve the unintended Deployment. 
- Fixed an issue where Helm changes to statsd Pod resources would apply only to new Deployments. 
- Fixed an issue where data for **Disk Usage** and **Platform Overview** did not appear in Grafana. 
- Fixed an issue where you could get a 500 internal server error from the Airflow UI when switching between pages for a DAG. 
- Astronomer Software now throws an error if you attempt to install it with an unsupported version of Kubernetes.
- Removed support for Kubernetes 1.22.
- Fixed an issue where using the Houston API to query for a Deployment that didn't exist returned a non-descriptive error.
- Fixed an issue where you couldn't create registry service accounts on Openshift clusters. 
- Fixed the following vulnerabilities:

    - [CVE-2022-48174](https://nvd.nist.gov/vuln/detail/CVE-2022-48174)
    - [CVE-2023-38325](https://nvd.nist.gov/vuln/detail/CVE-2023-38325)
    - [CVE-2023-36665](https://nvd.nist.gov/vuln/detail/CVE-2023-36665)
    - [CVE-2022-48174](https://nvd.nist.gov/vuln/detail/CVE-2022-48174)
    - [CVE-2022-41723](https://nvd.nist.gov/vuln/detail/CVE-2022-41723)
    - [CVE-2022-29458](https://nvd.nist.gov/vuln/detail/CVE-2022-29458)
    - [CVE-2023-0464](https://nvd.nist.gov/vuln/detail/CVE-2023-0464)
    - [CVE-2023-2650](https://nvd.nist.gov/vuln/detail/CVE-2023-2650)
    - [CVE-2022-29458](https://nvd.nist.gov/vuln/detail/CVE-2022-29458)
    - [CVE-2023-27561](https://nvd.nist.gov/vuln/detail/CVE-2023-27561)
    - [CVE-2017-11468](https://nvd.nist.gov/vuln/detail/CVE-2017-11468)
    - [CVE-2023-2253](https://nvd.nist.gov/vuln/detail/CVE-2023-2253)
    - [CVE-2023-28840](https://nvd.nist.gov/vuln/detail/CVE-2023-28840)
    - [CVE-2022-21698](https://nvd.nist.gov/vuln/detail/CVE-2022-21698)
    - [CVE-2023-28319](https://nvd.nist.gov/vuln/detail/CVE-2023-28319)
    - [CVE-2023-29491](https://nvd.nist.gov/vuln/detail/CVE-2023-29491)
    - [CVE-2023-35945](https://nvd.nist.gov/vuln/detail/CVE-2023-35945)
    - [CVE-2023-37920](https://nvd.nist.gov/vuln/detail/CVE-2023-37920)
    - [CVE-2022-41721](https://nvd.nist.gov/vuln/detail/CVE-2022-41721)
    - [CVE-2023-39417](https://nvd.nist.gov/vuln/detail/CVE-2023-39417)
    - [CVE-2023-37788](https://nvd.nist.gov/vuln/detail/CVE-2023-37788)
    - [CVE-2023-40577](https://nvd.nist.gov/vuln/detail/CVE-2023-40577)
    - [CVE-2021-33194](https://nvd.nist.gov/vuln/detail/CVE-2021-33194)
    - [CVE-2021-38561](https://nvd.nist.gov/vuln/detail/CVE-2021-38561)

## 0.30.7

Release date: May 26, 2023

### Additional improvements

- You can now configure custom environment variables for ElasticSearch-based custom logging using the `astronomer.customLogging.extraEnv` value in your `config.yaml` file.
- You can now configure `prometheus.config.scrape_configs.kubernetes_apiservers.tls_config.insecure_skip_verify` in the Prometheus Helm chart.
- You can now set `astronomer.houston.config.deployments.helm.prometheus.certgenerator.extraAnnotations` in your `config.yaml` file.
- You can now configure a custom indexing pattern for [Vector logging sidecars](export-task-logs.md#export-logs-using-container-sidecars) by setting both `elasticsearch.curator.age.timestring` and `astronomer.houston.config.deployments.helm.loggingSidecar.indexPattern` in your `config.yaml` file.
- The Software UI now shows a warning message for Deployments currently running an Astronomer Certified image. Only System Admins can create Deployments with deprecated Astronomer Certified images by setting `deployments.enableSystemAdminCanCreateDeprecatedAirflows` to `true`.
- Grafana now includes an **Astronomer Houston Dashboard** that you can use to view Houston metrics. 
- Improved signalling between primary Kubernetes containers and the logging sidecar so that you no longer have to set `global.loggingSidecar.terminationEndpoint` in your `config.yaml` file.

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

:::warning Breaking Change for Azure Database for PostgreSQL

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

## 0.29.5

Release date: October 11, 2022

:::warning Breaking change

(https://github.com/kubernetes/kubernetes/issues/65106) that occurs when you upgrade Helm charts that include duplicate keys in an `env` array. If you have a Helm chart with duplicate keys and upgrade to Astronomer Software 0.29.3+, all key-value pairs with the duplicate key are removed from your environment.

To preserve duplicate keys in your Helm chart, you can either reapply the values after upgrading, or you can use the `--reset-values` flag when you run the upgrade script as described in [Upgrade Astronomer](upgrade-astronomer.md).

:::

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

## 0.29.4

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

## 0.29.3

Release date: August 5, 2022

### Additional improvements

- Resolved several high and critical CVEs.

### Bug fixes

- API requests to query the AUs allocated to **Extra Capacity** are now returning results for all Deployments in a Workspace. Previously, queries were only returning partial results.

## 0.29.2

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

## 0.29.1

Release date: June 3, 2022

### Bug fixes

- Fixed an issue where you couldn't run Houston API queries for Deployments using `releaseName` and `label`
- Fixed an issue where a user could not log in through Azure AD SSO if the user belonged to a group without a `displayName`

## 0.29.0

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

## v0.28.8

Release date: January 26, 2023

### Bug fixes

- Fixed the following vulnerabilities: 

    - [CVE-2021-44716](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44716)
    - [CVE-2022-27664](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-27664)
    - [CVE-2022-2625](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2625)
    - [CVE-2022-37454](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-37454)
    - [CVE-2022-42919](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42919)
    - [CVE-2022-45061](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-45061)
    - [CVE-2022-46146](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-46146)
    - [CVE-2022-27191](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-46146)
    - [CVE-2022-32149](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-32149)
    - [CVE-2022-37601](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-37601)
    - [CVE-2022-43680](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-43680)

- Fixed an issue where service accounts with System Admin permissions couldn't create Deployments on deprecated Airflow versions.
- Fixed an issue where you could not upgrade a Deployment from an unsupported version of Astronomer Certified (AC) to another unsupported version of AC.
- Fixed an issue where Deployments with many DAGs could not be successfully upgraded due to a short timeout.
- Fixed an issue in the Software UI where an error message appeared after refreshing pages listing Workspace or Deployment service accounts.
- Fixed an issue where you could not view Deployment-level service accounts in the Software UI.

## v0.28.7

Release date: October 14, 2022

### Bug fixes 

- Fixed the following vulnerabilities:
    - [CVE-2022-40674](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40674)
    - [CVE-2022-3224](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3224)

## v0.28.6

Release date: September 21, 2022

### Additional improvements

- You can now specify `authUrlParams` for your identity provider (IdP) in `config.yaml`
- Added support for Kubernetes 1.21, 1.22, and 1.23
- Upgraded Prometheus to the LTS release of 2.37.0

### Bug fixes

- Fixed the following Common Vulnerabilities and Exposures (CVEs):
    - [CVE-2022-1996](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1996)
    - [CVE-2022-21698](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-21698)
    - [CVE-2022-0624](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0624)
    - [CVE-2022-31129](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-31129)

- Fixed several additional CVEs by upgrading images for system components
- Fixed an issue where custom authentication methods did not appear in the Software UI

## v0.28.5

Release date: June 23, 2022

### Bug fixes

- Fixed several high level CVEs
- User auth tokens for the Software UI are now stored in httpOnly cookies
- Fixed an issue where Grafana dashboards were not accessible
- Fixed an issue where a user could not log in through Azure AD SSO if the user belonged to a group without a `displayName`

## v0.28.4

Release date: April 8, 2022

### Additional Improvements

- Users added to Astronomer Software via an [IDP group](import-idp-groups.md) no longer need to be invited by email in order to join Astronomer.
- Teams now support [Azure AD Connect sync](https://docs.microsoft.com/en-us/azure/active-directory/hybrid/concept-azure-ad-connect-sync-user-and-contacts) for user groups.
- System admins can no longer remove the last user from an active Workspace or Deployment. This ensures that a given Workspace or Deployment can always be deleted by an existing member. Similarly, Workspace Admins can no longer remove a Team if doing so results in a Workspace having zero Admins.
- You can now map your IDP's groups claim to Astronomer's expected claim of `groups` via the `astronomer.houston.config.auth.openidConnect.<idp>.claimsMapping` setting in `config.yaml`.
### Bug Fixes

- Fixed an issue where deleted Teams did not disappear from the Software UI until you refreshed the page
- Fixed an issue where Teams were still available in the Software UI even when their underlying IDP group had been deleted from the IDP
- Fixed an issue where creating a Deployment with the default resource configuration would result in a Deployment having a **Scheduler Count** of 1 instead of the stated default of 2
- Fixed an issue where you could not deploy code to a Deployment that shared the release name of a previous Deployment which was hard deleted
- Fixed an issue where you could not create a Deployment with a numeric-only name in a pre-created namespace

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

By default, the Astronomer CLI uses Docker to execute a few specific commands. As an alternative, you can now configure the Astronomer CLI to use Podman instead. For more information, read [Run the CLI with Podman](https://docs.astronomer.io/astro/cli/configure-cli#run-the-astro-cli-using-podman).

### Bug Fixes

- Dropped support for Kubernetes 1.17
- Fixed an issue where redeployments could clobber existing annotations for namespaces
- Fixed an issue where new Deployments could potentially generate invalid usernames for Celery and the metadata DB
- Fixed an issue where scheduler, webserver, and worker logs were not accessible via the Astronomer CLI
- Fixed an issue where where setting extra volumes via `config.yaml` did not work when NFS DAG deploys were enabled.

## 0.26.7

Release date: March 1, 2022

### Additional improvements

- Fixed several CVEs
- Updated documentation links in the UI to point to Software documentation

## 0.26.6

Release date: January 10, 2022

### Bug Fixes

- Fixed an issue where users could not create Deployments via an IAM role

## 0.26.5

Release date: December 11, 2021

### Bug Fixes

- Remediated [CVE-2021-44228](https://github.com/advisories/GHSA-jfh8-c2jp-5v3q) related to Log4J by setting ES_JAVA_OPTS=-Dlog4j2.formatMsgNoLookups=true at runtime for all ElasticSearch containers

## 0.26.4

Release date: November 22, 2021

### Support for Airflow 2.2.0

[Apache Airflow 2.2.0](https://airflow.apache.org/blog/airflow-2.2.0/) is an exciting milestone in the open source project. Most notably, this release introduces custom timetables and deferrable operators.

#### Custom Timetables

Timetables are a powerful new framework that you can use to create custom schedules using Python. In an effort to provide more flexibility and address known limitations imposed by cron, timetables use an intuitive `data_interval` that, for example, allows you to schedule a DAG to run daily on Monday through Friday, but not on the weekend. Timetables can be easily plugged into existing DAGs, which means that it's easy to create your own or use community-developed timetables in your project.

For more information on using timetables, read the [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/timetable.html).

#### Deferrable Operators

Deferrable operators are a new type of Airflow operator that promises improved performance and lower resource costs. While standard operators and sensors take up a Worker or Scheduler slot even when they are waiting for an external trigger, deferrable operators are designed to suspend themselves and free up that Worker or Scheduler slot while they wait. This is made possible by a new, lightweight Airflow component called the Triggerer.

As part of supporting deferrable operators, you can provision multiple Triggerers on your Astronomer Deployments. By provisioning multiple Triggerers, you can ensure that tasks using Deferrable Operators are run even when one Triggerer goes down. For more information about configuring Triggerers and other resources, see [Configure a Deployment](configure-deployment.md).

### CLI Verbosity Flag

You can now specify a `--verbosity` flag for all Astronomer CLI commands. When you specify this flag with a CLI command, the CLI prints out [Logrus](https://github.com/sirupsen/logrus) logs as the command runs. This is useful for debugging any errors that might result from a CLI command.

The flag prints out different levels of logs depending on the value that you pass it. Each possible value (`debug`, `info`, `warn`, `error`, `fatal`, and `panic`) maps to a different Logrus logging level. For more information about these logging levels, read the [Logrus documentation](https://github.com/sirupsen/logrus#level-logging).

### Minor Improvements

- You can now create a custom set of cluster-level permissions for the Astronomer Commander service by setting `astronomer.global.clusterRoles: false` in your `config.yaml` file and pushing a new [RoleBinding](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) to a pre-created Kubernetes namespace.
- In the `astronomer.houston.config` section of your `config.yaml` file, you can now configure a list of `allowedSystemLevelDomains []`. If you configure this list, only users with emails from domains specified in the list (for example, `<company>.com`) can be granted System Admin privileges.
- Greatly improved load times for the **System Admin** page in the UI.
- You can now specify a node port for 3rd party ingress controllers with a service type of `nodePort`.
- The naming format of service account pods has been changed from `<release-name>-dags-prod-worker-serviceaccount` to `release_name-dags-prod-airflow-worker`.

### Bug Fixes

- Fixed an issue where you could not update an existing Deployment's IAM role via the Astronomer CLI
- Fixed an issue where Deployments would not work on clusters with custom domains
- Fixed error handling when interacting with a Deployment that wasn't fully spun up
- Added a new validation step for Airflow Helm chart values configured in the `astronomer.houston.config.deployments.helm.airflow` section of `config.yaml`
