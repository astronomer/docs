---
title: 'Astronomer Software v0.33 release notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

<!--- Version-specific -->

0.33 is the latest stable version of Astronomer Software, while 0.32 remains the latest long-term support (LTS) release. To upgrade to 0.33, see [Upgrade Astronomer](upgrade-astronomer.md). For more information about Software release channels, see [Release and lifecycle policies](release-lifecycle-policy.md). To read release notes specifically for the Astro CLI, see [Astro CLI release notes](https://docs.astronomer.io/astro/cli/release-notes).

## 0.33.0

Release date: August 3, 2023

### Automatic PGBouncer connection scaling

Astronomer Software now automatically scales the size of PGBouncer connection pools based on your Airflow component counts and Airflow configuration, instead of solely based on total AU. This improves performance, scalability, and utilization of database connections across all Deployments. 

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