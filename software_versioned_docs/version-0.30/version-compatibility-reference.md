---
title: "Version compatibility reference for Astronomer Software"
sidebar_label: "Version compatibility reference"
id: version-compatibility-reference
description: A reference of all adjacent tooling required to run Astronomer Software and corresponding version compatibility.
---

Astronomer Software ships with and requires a number of adjacent technologies that support it, including Kubernetes, Helm, and Apache Airflow itself. This guide provides a reference of all required tools and versions for running Astronomer Software.

While the tables below reference the minimum compatible versions, we typically recommend running the latest versions of all tooling if and when possible.

## Astronomer Software

<!--- Version-specific -->

| Astronomer Platform | Kubernetes                                         | Postgres | Python                                         | Astro Runtime        | Helm |
| ------------------- | -------------------------------------------------- | -------- | ---------------------------------------------- | -------------------- | ---- |
| v0.30               | 1.19¹, 1.20¹, 1.21, 1.22¹, 1.23, 1.24, 1.25¹, 1.26¹, 1.27¹ | 11+      | 3.6, 3.7, 3.8, 3.9 (_requires Airflow 2.2.0+_) | All Runtime versions | 3.6  |
| v0.32               | 1.21, 1.22¹, 1.23, 1.24 , 1.25, 1.26, 1.27¹        | 11+      | 3.6, 3.7, 3.8, 3.9 (_requires Airflow 2.2.0+_) | All Runtime versions | 3.6  |
| v0.33               | 1.21, 1.22, 1.23, 1.24 , 1.25, 1.26                | 11+      | 3.6, 3.7, 3.8, 3.9 (_requires Airflow 2.2.0+_) | All Runtime versions | 3.6  |

:::info

¹: Support for some Kubernetes versions is limited to specific Astronomer Software patch versions.

- Support for Kubernetes 1.19 and 1.20 ends with Astronomer Software version 0.30.4.
- Support for Kubernetes 1.22 ends with Astronomer Software version 0.30.8 and 0.32.3.
- Support for Kubernetes 1.25 and 1.26 starts in Astronomer Software version 0.30.6.
- Support for Kubernetes 1.27 starts in Astronomer Software version 0.30.8 and 0.32.3.

:::

For more detail about the changes in each Astronomer Software release, see the [Astronomer Software Release Notes](release-notes.md).

All currently supported versions of Astronomer-distributed images are compatible with all versions of Astronomer Software. Astro Runtime maintenance is independent of Software maintenance. For more information, see [Astro Runtime maintenance and lifecycle policy](runtime-version-lifecycle-policy.md).

:::info

Due to the [deprecation of Dockershim](https://kubernetes.io/blog/2020/12/02/dockershim-faq/), Azure does not support private Certificate Authorities (CAs) starting with Kubernetes 1.19. If your organization is using a private CA, contact [Astronomer support](https://support.astronomer.io) before upgrading to Kubernetes 1.19 on Azure Kubernetes Service (AKS).

:::

### Kubernetes version support policy

In general, Astronomer Software will support a given version of Kubernetes through its End of Life. This includes Kubernetes upstream and cloud-managed variants like GKE, AKS, and EKS. When a version of Kubernetes reaches End of Life, support will be removed in the next major or minor release of Astronomer Software. For more information on Kubernetes versioning and release policies, refer to [Kubernetes Release History](https://kubernetes.io/releases/) or your cloud provider.

For more information on upgrading Kubernetes versions, follow the guidelines offered by your cloud provider.

- [Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)
- [Azure AKS](https://docs.microsoft.com/en-us/azure/aks/upgrade-cluster)
- [Google GKE](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-upgrades)
- [RedHat OpenShift](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.11/html/updating_clusters/index)
