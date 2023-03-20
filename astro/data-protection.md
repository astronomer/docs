---
sidebar_label: 'Data protection'
title: "Data protection"
id: data-protection
description: Learn how Astronomer uses encryption to protect clusters and data.
---

Astro uses both encryption in transit and encryption at rest to protect data across and within the Data Plane and Control Plane. Additionally, Deployment namespaces are network isolated with restricted communications. This document contains details about each type of encryption and isolation currently in place on Astro.

## Encryption in transit

All communication between control and data planes is encrypted in transit using [TLS](https://www.acunetix.com/blog/articles/tls-security-what-is-tls-ssl-part-1/) 1.2, strong ciphers, and secure transfer (data layer).

All customer data flows within the control plane transit through a mTLS mesh, enforcing TLS 1.2 and secure strong ciphers. Encrypted secret environment variables transit from the Cloud API to a secrets manager in the control plane using TLS 1.2 and strong ciphers. Data planes pull base64 encoded secret environment variables, along with other Airflow configurations over an encrypted TLS connection. As part of the application of configuration manifests in the data plane, all secret and sensitive information is stored in an encrypted etcd cluster at rest.

All internal service communication within the data plane is transmitted using TLS 1.2 and secure ciphers.

Every cluster in your data plane has its own certificates which were generated when the cluster was created and signed by the Let’s Encrypt certificate authority (CA). The certificates are automatically renewed every 90 days. To enhance the security of data plane clusters, Astronomer will soon remove public IPs and the requirement to sign certificates with a public CA.

## Encryption at rest

All data at rest across control and data planes is encrypted with AES-256, one of the strongest block ciphers available. This is done using native cloud provider technologies.

Specifically, control plane data is encrypted on disk with a platform-managed key, including backups and the temporary files created while DB queries are running. Likewise, data plane data is server-side encrypted and volume encrypted, using encryption keys managed by the cloud provider and anchored by hardware security appliances. All resources provisioned across both planes leverage cloud provider envelope encryption wherever possible in accordance with a [defense in depth security strategy](https://en.wikipedia.org/wiki/Defense_in_depth_(computing)).

## Deployment network isolation

All pods and services specific to a single Deployment on Astro are isolated to a corresponding Kubernetes namespace within the Astro cluster in which the Deployment is hosted. All Deployment namespaces on Astro, including those running on the same cluster, are network isolated from each other by default. In addition to the isolation between Deployment namespaces, Astronomer also restricts communication within a namespace to only what is required between components and associated ports.

This level of network isolation is achieved using [network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) enabled by the [Calico](https://kubernetes.io/docs/concepts/cluster-administration/networking/#calico) kubernetes network plugin.

The network isolation between and within Deployment namespaces ensures that communication is restricted to only allow necessary communications within a namespace, and that communication between Deployments is denied. This ensures that unintended communications and attempted data exchanges are blocked.
