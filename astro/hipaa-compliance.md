---
sidebar_label: 'HIPAA compliance'
title: "HIPAA compliance"
id: hipaa-compliance
description: Learn how to achieve HIPAA compliance on Astro.
---

The Health Insurance Portability and Accountability Act of 1996 (HIPAA) is United States legislation that provides data privacy and security provisions for safeguarding protected health information (PHI).

HIPAA applies to organizations that are classified as [covered entities](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html), as well as other persons or businesses, known as [business associates](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html), that provide services with the handling, transmission, storage, or processing of PHI data. By providing the managed service Astro for data orchestration of PHI data for a HIPAA covered entity or business associate, Astronomer becomes a business associate under HIPAA.

HIPAA requires covered entities or business associates that work with other business associates to produce a contract that imposes specific safeguards on the PHI that the business associate uses or discloses to provide services to a covered entity. The contract is known as a Business Associate Agreement (BAA).

## PHI data processing on the Astro data plane

Upon signing of a HIPAA [Business Associate Agreement (BAA)](https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/index.html), Astronomer permits the processing of PHI data in the Astro data plane. A signed BAA between Astronomer and you, the customer, helps support your HIPAA compliance program, but it is your responsibility to have required internal processes and a security program in place that align with HIPAA requirements. Compliance with HIPAA on Astro is a shared responsibility as outlined in the BAA and the model documented below.

## Shared Responsibility Model for HIPAA compliance

Astro operates on a model of shared responsibility, which means that Astronomer employees and Astronomer customers are equally responsible for ensuring platform security and compliance. This document expands on the general [shared responsibility model](shared-responsibility-model.md) to include specific responsibilities for HIPAA compliance. Maintaining HIPAA compliance is a joint effort that is shared by the public cloud providers, Astronomer, and the customer. Each party must fulfill their individual obligations to ensure HIPAA compliance.

This document references the Astro control and data planes, which are core parts of the Astronomer hybrid deployment model:

- The control plane provides end-to-end visibility, control, and management of users, workspaces, deployments, metrics, and logs.
- The data plane is the single tenant foundation in your cloud and orchestrates your data pipelines on Astro Runtime deployments.

### Astronomer obligations

- Provide a single-tenant data plane to ensure that PHI data processed in the customer's data plane is not shared or accessible by other customers.
- Provide data plane cloud infrastructure options and configuration that enforce encryption in-transit and at rest.
- Encrypt data in transit between control and data plane.
- Encrypt data at rest in control and data plane.
- Monitor control and data planes for but not limited to unauthorized access, malicious activity, intrusions and threats at runtime, and unauthorized configuration changes.
- Deprovision compute and data resources when they are no longer required for task execution, so that the cloud provider can permanently remove the compute and data resources.
- Execute data plane cluster deletion when instructed by the customer, so that the cloud provider can permanently remove the compute and data resources.

### Customer obligations

- Execute a Business Associate Agreement (BAA) with your public cloud provider to process PHI on cloud infrastructure.
- [Configure an identity provider](configure-idp.md) (IdP) for single sign-on to your Astro Organization.
- Use a [supported](runtime-version-lifecycle-policy.md#astro-runtime-lifecycle-schedule) (preferably latest patch) version of [Astro Runtime](runtime-image-architecture.md), to take advantage of the most recent security features and fixes.
- Use [supported and compatible versions](https://github.com/apache/airflow/blob/main/README.md#release-process-for-providers) of [Airflow providers](https://registry.astronomer.io/providers/?page=1), to take advantage of the most recent security features and fixes.
- Create a [secrets backend](https://docs.astronomer.io/astro/secrets-backend) to access sensitive information and secrets from your data pipelines that will be used to access PHI. If you do not have a secrets backend, you must [store your environment variables as secrets](environment-variables.md).
- Ensure all PHI data that is orchestrated or processed by the data plane is encrypted at rest and in transit at all times using modern cryptographic protocols and ciphers, and at no point can be read in clear text. For example, when reading data from an RDS instance, transforming it in the data plane, and writing it out to an S3 bucket.
- Do not output PHI to scheduler and/or task logs, especially in clear text. See [View Logs](view-logs.md) for more information.
- Do not store PHI as part of your DAG image or code.
- Do not store unencrypted PHI in [XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html). Ensure encrypted PHI stored in XComs for task execution is purged following task execution.
- Ensure your [lineage metadata](set-up-data-lineage.md) does not contain any PHI.
- Do not add, delete or modify data plane infrastructure that is provisioned and managed by Astronomer as that may be a violation of HIPAA. For example, disabling encryption of the S3 bucket (AWS), Cloud Storage (GCP), or Storage Account (Azure).

### Cloud provider responsibilities:

- Comply with the business associate obligations outlined in the BAA between Astronomer and cloud provider, and between the customer and cloud provider.
- Provide cloud infrastructure, specifically virtual machines, that support HIPAA compliance:
    - AWS: hardware-enabled encryption at rest and in transit with [EC2 Nitro instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances)
    - GCP: [Shielded GKE nodes](https://cloud.google.com/kubernetes-engine/docs/how-to/shielded-gke-nodes) leveraging built in encryption [at rest](https://cloud.google.com/docs/security/encryption/default-encryption) and [in transit](https://cloud.google.com/docs/security/encryption-in-transit) cluster features
    - Azure: AKS managed [Virtual Machine Scale Sets](https://docs.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview) (VMSS) leveraging built in encryption [at rest](https://docs.microsoft.com/en-us/azure/security/fundamentals/encryption-overview#encryption-of-data-at-rest) and [in transit](https://docs.microsoft.com/en-us/azure/security/fundamentals/encryption-overview#encryption-of-data-in-transit) cluster features
- Permanently delete and remove data disks, databases, object storage, and encryption keys when released or deleted by Astro.

:::info

This page is for informational purposes only. Customers should not consider the information or recommendations presented here to constitute legal advice. Customers should engage their own legal and privacy counsel to properly evaluate their use of Astronomer services, with respect to their legal and compliance requirements and objectives.

:::
