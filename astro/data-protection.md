---
sidebar_label: 'Data Protection'
title: "Data Protection"
id: data-protection
description: Learn how Astronomer uses encryption to protect Clusters and data.
---

## Overview

Astro uses both encryption in transit and encryption at rest to protect data across and within the Data and Control Planes. This document contains details about each type of encryption used in Astro processes.

## Encryption in Transit

All communication between Control and Data Planes is encrypted in transit using [TLS](https://www.acunetix.com/blog/articles/tls-security-what-is-tls-ssl-part-1/) 1.2, strong ciphers, and secure transfer (data layer).

All customer data flows within the Control Plane transit through a mTLS mesh, enforcing TLS 1.2 and secure strong ciphers. Encrypted secret environment variables transit from the Cloud API to a managed secrets backend using TLS 1.2 and strong ciphers. Data Planes pull base64 encoded secret environment variables, along with other Airflow configurations over an encrypted TLS connection. As part of the application of configuration manifests in the Data Plane, all secret and sensitive information is stored in an encrypted etcd cluster at rest.

All internal service communication within the Data Plane is transmitted using TLS 1.2 and secure ciphers. Astronomer plans to enforce an mTLS mesh to all Airflow Deployment namespaces in early 2022.

Each Cluster in your Data Plane has its own certificates which were generated when the Cluster was created and signed by the Let’s Encrypt Certificate Authority (CA). In 2022, Astronomer will enhance the security posture of Clusters in the Data Plane by removing public IPs and the need to sign certificates with a public CA.

## Encryption at Rest

All data at rest across Control and Data Planes is encrypted with AES-256, one of the strongest block ciphers available. This is done using native cloud provider technologies.

Specifically, Control Plane data is encrypted on disk with a platform-managed key, including backups and the temporary files created while DB queries are running. Likewise, Data Plane data is server-side encrypted and volume encrypted, using encryption keys managed by the cloud provider and anchored by hardware security appliances. By early 2022, all resources provisioned across both planes will leverage cloud provider envelope encryption wherever possible in accordance with a [defense in depth security strategy](https://www.us-cert.gov/bsi/articles/knowledge/principles/defense-in-depth).
