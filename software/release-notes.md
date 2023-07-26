---
title: 'Astronomer Software v0.33 release notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

<!--- Version-specific -->

0.33 is the latest stable version of Astronomer Software, while 0.32 remains the latest long-term support (LTS) release. To upgrade to 0.33, see [Upgrade Astronomer](upgrade-astronomer.md). For more information about Software release channels, see [Release and lifecycle policies](release-lifecycle-policy.md). To read release notes specifically for the Astro CLI, see [Astro CLI release notes](https://docs.astronomer.io/astro/cli/release-notes).

## 0.33.0

Release date: July 26, 2023

### Automatic PGBouncer connection scaling

Astronomer Software now automatically scales the size of PGBouncer connection pools based on the connection usage of your current Airflow components. This should result in improved performance, scalability, and utilization of database connections across all Deployments. 

### Additional improvements

- The Workspace **Deployments** page is now paginated in the Astronomer UI.
- You no longer have to set `elasticsearch.curator.age.timestring` when you configure a custom indexing pattern for [Vector logging sidecars](export-task-logs.md#export-logs-using-container-sidecars). The only required value is now `astronomer.houston.config.deployments.helm.loggingSidecar.indexPattern`.
- You can now set `deployments.canCreateDeploymentFromUI` to false to prevent all users from creating new Deployments through the Astronomer UI. 

### Bug fixes

- Fixed an issue where configurations in `astronomer.houston.config.deployments.components` applied only to new Deployments made after the configuration was set. 
- Fixed an issue where a Workspace-level service account would improperly inherit lesser permissions for Deployments it was added to.
- Fixed an issue where the Astronomer UI would still show a **Delete** button for Teams for roles that did not have the `system.teams.remove` permission.
- Fixed an issue where you could get a 500 internal server error from the Airflow UI when switching between pages for a DAG.
- Fixed an issue where you couldn't set `properties.email` using the `upsertDeployment` mutation.
- Fixed an issue where the Astronomer UI would freeze if a System Admin user viewed service accounts without the appropriate permissions. 
- Fixed the following vulnerabilities:

    - [CVE-2023-35945](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-35945)