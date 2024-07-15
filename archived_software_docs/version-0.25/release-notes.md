---
title: 'Astronomer v0.25 Release Notes'
sidebar_label: 'Release Notes'
id: release-notes
---

This document contains all release notes for Astronomer Software 0.25.

0.30 is the latest long-term support (LTS) version of Astronomer Software. To upgrade to 0.30, read [Upgrade Astronomer](upgrade-astronomer.md). For more information about Software release channels, see [Release and lifecycle policies](release-lifecycle-policy.md). 

If you're upgrading to Astronomer v0.30, see [Upgrade to Astronomer v0.25](upgrade-astronomer.md). To upgrade to a patch version within the Astronomer v0.25 series, see [Upgrade to a Patch Version of Astronomer Software](upgrade-astronomer.md).

For more Astronomer Software release notes, see:

- [Astro CLI release notes](cli-release-notes.md)
- [Astro Runtime release notes](runtime-release-notes.md)
- [Astronomer Software 0.29 release notes](https://www.astronomer.io/docs/software/0.29/release-notes)
- [Astronomer Software 0.28 release notes](https://www.astronomer.io/docs/software/0.28/release-notes)
- [Astronomer Software 0.25 release notes](https://www.astronomer.io/docs/software/0.25/release-notes)

All Astronomer Software versions are tested for scale, reliability and security on Amazon EKS, Google GKE, and Azure AKS. If you have questions or an issue to report, contact [Astronomer support](https://support.astronomer.io).

## 0.25.15

Release date: October 18, 2022

### Bug fixes 

- Fixed the following vulnerabilities:
    - [CVE-2022-40674](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40674)
    - [CVE-2022-44906](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-44906)
    - [CVE-2022-32213](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-32213)
    - [CVE-2022-32214](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-32214)
    - [CVE-2022-32215](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-32215)
    - [CVE-2022-31129](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-31129)
    - [CVE-2022-25878](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25878)
    - [CVE-2022-24785](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24785)

## 0.25.14

Release date: September 21, 2022

### Additional improvements

- Improved the startup time for the NATS server
- Upgraded Prometheus to the LTS release of 2.37.0
- Removed all remaining uses of Helm2

### Bug fixes

- Fixed several Common Vulnerabilities and Exposures (CVEs) by upgrading images for system components

## 0.25.13

Release date: February 23, 2022

### Additional improvements

- Fixed several CVEs
- Updated documentation links in the UI to point to Software documentation

## 0.25.12

Release date: December 11, 2021

### Bug Fixes

- Remediated [CVE-2021-44228](https://github.com/advisories/GHSA-jfh8-c2jp-5v3q) related to Log4J by setting `ES_JAVA_OPTS=-Dlog4j2.formatMsgNoLookups=true` at runtime for all ElasticSearch containers

## v0.25.11

Release Date: October 27, 2021

### Bug Fixes

- Fixed a security issue where an internal API endpoint could be accessed by an unauthorized user with a specific event input

## v0.25.8

Release Date: September 17, 2021

### Pre-created Namespaces for Deployments

You can now pre-create Kubernetes namespaces for use across your platform. You might want to configure this feature to limit the number of active Deployments on your platform, or to link ownership of a specific Deployment to a given department in your organization.

This feature must first be enabled and configured on your platform before it can be used. For more information, see [Pre-Create Namespaces](pre-create-namespaces.md).

### Minor Improvements

- You can now use both New Relic and CloudWatch to monitor platform logs. For more information on exporting logs to these 3rd party monitoring resources, reach out to your Astronomer representative.

### Bug Fixes

- Deprecated support for Kubernetes 1.16.
- Fixed an issue where reusing a custom release name after hard deleting a Deployment would occasionally fail
- Fixed an issue where setting a custom release name that began with a number would cause an error in Helm
- Fixed an issue where you couldn't set custom image paths for private certificate authorities (CAs)
- Fixed an issue where setting the `global.storageClass` key in `values.yaml` did not update the storage class for all PVCs on your platform
- Fixed an issue where Houston workers failed to get the issuer certificate for custom CA certs
- Fixed Celery Worker logs not appearing in the Software UI

## v0.25.6

Release Date: August 4, 2021

### Ability to Hard Delete Apache Airflow®® Deployments

Astronomer v0.25.6 introduces a platform-level setting that gives Deployment Admins the ability to hard delete Airflow Deployments. For more information about this feature, read [Delete a Deployment](configure-deployment.md#delete-a-deployment).

### Airgapped Installation

Organizations can now install Astronomer in an airgapped environment with no internet access. To learn more, contact [Astronomer Support](https://support.astronomer.io).

### Bug Fixes

- System Admins now have access to all API endpoints.
- Addressed several security-related issues.

## v0.25.4

Release Date: July 2, 2021

### Minor Improvements

- Added support for installing Astronomer Software via ArgoCD, which facilitates continuous delivery for Kubernetes applications. For more information, read the [Astronomer Forum](https://forum.astronomer.io/t/installing-astronomer-with-argocd/1341).

### Bug fixes

- Fixed an issue where Workspace Service Accounts lost access to Astronomer.

## v0.25.3

Release Date: June 30, 2021

### Support for Third-Party Ingress Controllers

You can now use any Ingress controller for your Astronomer platform. This is particularly useful if you're installing Astronomer onto platforms like OpenShift, which favor a specific type of Ingress controller, or if you want to take advantage of any features not available through the default NGINX Ingress controller.

For more information and setup steps, read [Third-Party Ingress Controllers](third-party-ingress-controllers.md).

### Support for Kubernetes 1.19 and 1.20

The Astronomer platform is now compatible with Kubernetes 1.19 and 1.20. As a Software user, you can now upgrade your clusters to either of these two versions and take advantage of the latest Kubernetes features. For more information, refer to [Kubernetes 1.20 release notes](https://kubernetes.io/blog/2020/12/08/kubernetes-1-20-release-announcement/).

### Bypass Email Verification for Users via Houston API

The Houston API `workspaceAddUser` mutation now includes a `bypassInvite` field. When this field is set to true, users invited to a Workspace no longer need to first verify their email addresses before accessing the Workspace. This type of query can be useful to minimize friction when programmatically inviting many users to your platform. For more information, see [Sample Mutations](houston-api.md#sample-mutations).

### Minor Improvements

- You can now specify values for `global.privateRegistry.user`, `global.privateRegistry.password`, and `global.astronomer.registry.secret` in `config.yaml`. By default, these values are randomly generated.
- Workspace Admins can now perform CRUD operations on any Deployment within their Workspace, even if they don't have Deployment Admin permissions for the given Deployment.
- Prevented `NginxIngressHigh4XXRate` and `NginxIngressHigh5XXRate` alerts from over-firing during periods of low traffic.
- Added the ability to use non-RFC address spaces for Alertmanager.
- Added support for using Workload Identity to configure a GCP registry backend.
- Changed sidecar naming convention from `nginx` to `auth-proxy`.
- Added `fsGroup` to the Webserver `securityContext` to enable [role assumption](https://docs.aws.amazon.com/eks/latest/userguide/security_iam_service-with-iam.html) for EKS 1.17.

### Bugfixes

- Fixed an issue where private root CAs did not work due to an unmounted certificate.
- Fixed broken links to Deployments in alert emails.
- Fixed an issue where historical logs did not appear in the Software UI.
- Fixed an issue where System Admins were unable to create Deployments.
- Fixed a visual bug where some Deployments with only 1 Scheduler were shown as having 2 in the Software UI.
- Fixed a visual bug where users without Workspace Admin permissions had a non-functional **Invite Users** button in the Software UI.

## v0.25.2

Release Date: May 18, 2021

### Bug Fixes

- Fixed an API issue that caused the migration script from Astronomer v0.23 to v0.25 to fail if the NFS volume-based deployment mechanism was not enabled.

## v0.25.1

Release Date: May 11, 2021

### Support for NFS Volume-based DAG Deploys

We are pleased to offer an NFS volume-based DAG deploy mechanism on Astronomer. This new deployment method is an alternative to image-based DAG deploys.

With NFS volume-based DAG deploys, you no longer need to rebuild and restart your environment when deploying changes to your DAGs. When a DAG is added to an external NFS volume, such as Azure File Storage or Google Cloud Filestore, it automatically appears in your Airflow Deployment a short time later. Compared to image-based deploys, this new mechanism limits downtime and better enables continuous development.

This feature must be explicitly enabled on your platform and requires the use of an external NFS volume. For more information, read [Deploy to an NFS Volume](deploy-nfs.md).

> **Note:** To take advantage of this feature, your Apache Airflow® Deployments must be running on Airflow 2.0 or greater. To upgrade your Deployments, read [Manage Airflow Versions](manage-airflow-versions.md).

### Bug Fixes

- Fixed an issue where Grafana pods did not run properly when `global.ssl.mode` was set to `prefer`. ([Source](https://github.com/astronomer/astronomer/pull/1082))
