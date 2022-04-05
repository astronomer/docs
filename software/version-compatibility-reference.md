---
title: "Version Compatibility Reference for Astronomer Software"
sidebar_label: "Version Compatibility Reference"
id: version-compatibility-reference
description: A reference of all adjacent tooling required to run Astronomer Software and corresponding version compatibility.
---

## Overview

Astronomer Software ships with and requires a number of adjacent technologies that support it, including Kubernetes, Helm, and Apache Airflow itself. This guide provides a reference of all required tools and versions for running Astronomer Software. This guide also includes a version compatibility reference table for running [Astronomer Certified](image-architecture.md) outside of the context of the Astronomer platform.

While the tables below reference the minimum compatible versions, we typically recommend running the latest versions of all tooling if and when possible.

## Astronomer Software

<!--- Version-specific -->

| Astronomer Platform | Kubernetes                   | Helm | Terraform | Postgres | Python                                    | Astronomer CLI | Astronomer Certified |
| ------------------- | ---------------------------- | ---- | --------- | -------- | ----------------------------------------- | -------------- | -------------------- |
| v0.23               | 1.16, 1.17, 1.18             | 3    | 0.13.5    | 9.6+     | 3.6, 3.7, 3.8                             | 0.23.x         | All                  |
| v0.25               | 1.17, 1.18, 1.19, 1.20, 1.21 | 3.6  | 0.13.5    | 9.6+     | 3.6, 3.7, 3.8, 3.9 (_requires AC 2.2.0+_) | 0.25.x         | All                  |
| v0.26               | 1.17, 1.18, 1.19, 1.20, 1.21 | 3.6  | 0.13.5    | 9.6+     | 3.6, 3.7, 3.8, 3.9 (_requires AC 2.2.0+_) | 0.26.x         | All                  |
| v0.27               | 1.18, 1.19, 1.20, 1.21       | 3.6  | 0.13.5    | 9.6+     | 3.6, 3.7, 3.8, 3.9 (_requires AC 2.2.0+_) | 0.27.x         | All                  |
| v0.28               | 1.19, 1.20, 1.21             | 3.6  | 0.13.5    | 9.6+     | 3.6, 3.7, 3.8, 3.9 (_requires AC 2.2.0+_) | 0.28.x         | All                  |

For more detail on changes between Software versions, refer to [Astronomer Software Release Notes](release-notes.md).

> **Note:** On Astronomer v0.23+, new versions of Apache Airflow on Astronomer Certified are automatically made available in the Software UI and CLI within 24 hours of their publication. For more information, refer to [Available Astronomer Certified Versions](ac-support-policy.md#astronomer-certified-lifecycle-schedule).

> **Note:** Due to the [deprecation of Dockershim](https://kubernetes.io/blog/2020/12/02/dockershim-faq/), Azure does not support private CAs starting with Kubernetes 1.19. If you use a private CA, contact [Astronomer Support](https://support.astronomer.io) before upgrading to Kubernetes 1.19 on AKS.

> **Note:** While Astronomer v0.25 is compatible with Astronomer Certified 2.2.0, support for the Airflow Triggerer is available only in Astronomer v0.26+. To use [Deferrable Operators](https://airflow.apache.org/docs/apache-airflow/stable/concepts/deferring.html), which require the Airflow Triggerer, you must upgrade.

### Kubernetes Version Support Policy

In general, Astronomer Software will support a given version of Kubernetes through its End of Life. This includes Kubernetes upstream and cloud-managed variants like GKE, AKS, and EKS. When a version of Kubernetes reaches End of Life, support will be removed in the next major or minor release of Astronomer Software. For more information on Kubernetes versioning and release policies, refer to [Kubernetes Release History](https://kubernetes.io/releases/) or your cloud provider.

For more information on upgrading Kubernetes versions, follow the guidelines offered by your cloud provider.

- [Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)
- [Azure AKS](https://docs.microsoft.com/en-us/azure/aks/upgrade-cluster)
- [Google GKE](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-upgrades)
- [RedHat OpenShift](https://docs.openshift.com/container-platform/4.6/updating/updating-cluster-between-minor.html)

## Astronomer Certified

| Astronomer Certified | Postgres | MySQL     | Python                         | System Distribution  | Airflow Helm Chart |
| -------------------- | -------- | --------- | ------------------------------ | -------------------- | ------------------ |
| 1.10.15              | 9.6+     | 5.7, 8.0+ | 3.6, 3.7, 3.8                  | Debian 10 (Buster)   | Any                |
| 2.0.0                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8                  | Debian 10 (Buster)   | 0.18.6+            |
| 2.0.2                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8                  | Debian 10 (Buster)   | 0.18.6+            |
| 2.1.0                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8                  | Debian 10 (Buster)   | 0.18.6+            |
| 2.1.1                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8, 3.9             | Debian 10 (Buster)   | 0.18.6+            |
| 2.1.3                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8, 3.9             | Debian 10 (Buster)   | 0.18.6+            |
| 2.1.4                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8, 3.9             | Debian 10 (Buster)   | 0.18.6+            |
| 2.2.0                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8, 3.9             | Debian 11 (Bullseye) | 0.18.6+            |
| 2.2.1                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8, 3.9 (_Default_) | Debian 11 (Bullseye) | 0.18.6+            |
| 2.2.2                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8, 3.9 (_Default_) | Debian 11 (Bullseye) | 0.18.6+            |
| 2.2.3                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8, 3.9 (_Default_) | Debian 11 (Bullseye) | 0.18.6+            |
| 2.2.4                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8, 3.9 (_Default_) | Debian 11 (Bullseye) | 0.18.6+            |
| 2.2.5                | 9.6+     | 8.0+      | 3.6, 3.7, 3.8, 3.9 (_Default_) | Debian 11 (Bullseye) | 0.18.6+            |

For more detail on each version of Astronomer Certified and instructions on how to upgrade, refer to [Upgrade Apache Airflow](manage-airflow-versions.md).

> **Note:** While the Astronomer Certified Python Wheel supports Python versions 3.6, 3.7, and 3.8, Astronomer Certified Docker images have been tested and built only with Python 3.7. To run Astronomer Certified on Docker with Python versions 3.6 or 3.8, you can create a custom image with a different Python version specified. For more information, read [Change Python Versions](customize-image.md#build-with-a-different-python-version).

> **Note:** MySQL 5.7 is compatible with Airflow and Astronomer Certified 2.0 but it does NOT support the ability to run more than 1 Scheduler and is not recommended. If you'd like to leverage Airflow's new Highly-Available Scheduler, make sure you're running MySQL 8.0+.
