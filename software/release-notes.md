---
title: 'Astronomer Software v0.32 release notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

<!--- Version-specific -->

0.32 is the latest stable version of Astronomer Software, while 0.30 remains the latest long-term support (LTS) release. To upgrade to 0.32, see [Upgrade Astronomer](upgrade-astronomer.md). For more information about Software release channels, see [Release and lifecycle policies](release-lifecycle-policy.md). To read release notes specifically for the Astro CLI, see [Astro CLI release notes](https://docs.astronomer.io/astro/cli/release-notes).

## 0.32.1

Release date: June 12, 2023

### Additional improvements

- [Underprovisioning](cluster-resource-provisioning.md) now also applies to the following components:

    - PGBouncer
    - Statsd
    - Flower
  
- You can now configure `astronomer.houston.config.deployments.overProvisioningComponents` to limit the scope of [underprovisioning](cluster-resource-provisioning.md) only to specific Airflow components.
- Teams without any users are now automatically deleted.
- You can now authenticate to an external storage service for [archiving task metadata](configure-deployment.md#clean-deployment-task-metadata) using Workload Identity.
- You can now set `prometheus.config.scrape_configs.kubernetes_apiservers.tls_config.insecure_skip_verify` in the Prometheus Helm chart.
- You can now set `astronomer.houston.config.deployments.helm.prometheus.certgenerator.extraAnnotations` in your `config.yaml` file.
- You can now configure credentials for a registry backend as Kubernetes secrets in your `config.yaml` file. See [Configure a registry backend](registry-backend.md).

### Bug fixes

- Fixed an issue where `git-sync-relay` containers wouldn't restart as expected after being terminated.
- Fixed an issue where a service account with the Workspace Editor role could update a Deployment when it didn't have any Deployment-level permissions for the Deployment. 
- Fixed an issue where data for **Disk Usage** and **Platform Overview** did not appear in Grafana.
- System Admins can no longer change a user's system role if the user is imported to Astronomer through an IdP group.
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