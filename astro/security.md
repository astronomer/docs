---
sidebar_label: 'Security'
title: "Security in Astro"
id: security
description: Learn how Astro responds to and implements a variety of security concepts
---

## Overview

Astro is a fully managed data orchestration service that allows you to run your data pipelines in your public cloud account on Amazon Web Services (AWS) or Google Cloud Platform (GCP), respecting the need to keep your data private, secure, and within corporate boundaries.

The Astro architecture is secure by default, using encryption in transit, encryption at rest, strong cryptographic protocols, authentication, and role-based access control for authorization to your data pipelines, with a host of flexible and secure connectivity options to your critical data sources. This page serves as a summary of all Astro features that ensure the security and reliability of your systems.


## Shared Responsibility Model

Astro operates on a model of shared responsibility, which means that both the Astronomer team and Astronomer customers are responsible for the security of the platform. For more information, see [Shared Responsibility Model](shared-responsibility-model.md).

## Architecture

Astro boasts a hybrid deployment model founded on a Control Plane hosted by Astronomer and a Data Plane that is hosted in your cloud environment. It optimizes for security whilst relieving your team of operational overhead. For more information, see [Architecture](overview.md#architecture).

## Resilience

The Astro Control and Data Planes are architected and deployed on major public clouds to take advantage of their resilient, secure and highly available regions. Additionally, both planes are designed and architected to take advantage of best-in-class security products offered by the public clouds. For more information, see [Resilience](resilience.md).

## Disaster Recovery

While Astro Data Plane is designed to withstand and survive in-region Availability Zone (AZ) degradations and outages, rest assured Astronomer can also help you recover from major region failures by restoring configuration and secrets from a secure and highly available data store. For more information, read [Disaster Recovery](disaster-recovery.md).

## Physical and Environment Security

Astro leverages all three major public cloud providers (Azure, Google Cloud Platform, Amazon Web Services), thus physical and environmental security is handled entirely by those providers. Each cloud service provider provides an extensive list of compliance and regulatory assurances that they are rigorously tested against, including SOC 1/2-3, PCI-DSS, and ISO27001. For more information, read [Cloud Provider Security Responsibilities](shared-responsibility-model.md#cloud-provider-security-responsibilities).

Astronomer is a global remote company first. We have some small offices in the United States, but they are treated as trustless. Employees need to authenticate to all applications and systems using our IdP (Okta) with MFA even if using office WiFi.

## Data Privacy and Compliance

Astro is AICPA SOC 2 Type I certified with respect to the security, availability, and confidentiality Trust Service Categories. If you are interested in obtaining (NDA required) our SOC 2 Report and Penetration Test report, contact [sales@astronomer.io](mailto:sales@astronomer.io)

Astronomer is also [GDPR-compliant](gdpr-compliance.md) as an organization, and the Astro platform is GDPR-ready. Astronomer offers a Data Processing Agreement (DPA), which satisfies the requirements the GDPR imposes on data controllers with respect to data processors.

Astronomer is committed to pursuing HIPAA, and AICPA SOC 2 Type II compliance in 2022.

## Data Protection

Astro uses both encryption in transit and encryption at rest to protect data across and within the Data and Control Planes, using strong and secure protocols and ciphers, and built-in public cloud features. For more information, see [Data Protection](data-protection.md).

## Secrets Management

Astro is designed to secure sensitive information about your external systems. Sensitive information shared with Astronomer is securely stored and transmitted for consumption by your data pipelines. For more information, see [Secrets Management](secrets-management.md).
