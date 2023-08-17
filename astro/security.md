---
sidebar_label: 'Security'
title: "Security in Astro"
id: security
description: Learn how Astro responds to and implements a variety of security concepts
---

Astro is a fully managed data orchestration service that allows you to run your data pipelines in your public cloud account on Amazon Web Services (AWS) or Google Cloud Platform (GCP), respecting the need to keep your data private, secure, and within corporate boundaries.

The Astro architecture is secure by default, using encryption in transit, encryption at rest, strong cryptographic protocols, authentication, and role-based access control for authorization to your data pipelines, with a host of flexible and secure connectivity options to your critical data sources. This page serves as a summary of all Astro features that ensure the security and reliability of your systems.

## Shared responsibility model

Astro operates on a model of shared responsibility, which means that both the Astronomer team and Astronomer customers are responsible for the security of the platform. For more information, see [Shared responsibility model](shared-responsibility-model.md).

## Architecture

Astro provides a deployment model where the core components for managing Airflow are hosted in Astronomer's cloud, allowing you to run Airflow with as little friction as possible and securely connect to your data infrastructure. For more information, see [Architecture](astro-architecture.md).

## Resilience

The Astro control and data planes are architected and deployed on major public clouds to take advantage of their resilient, secure and highly available regions. Additionally, both planes are designed and architected to take advantage of best-in-class security products offered by the public clouds. For more information, see [Resilience](resilience.md).

## Disaster recovery

While Astro data plane is designed to withstand and survive in-region Availability Zone (AZ) degradations and outages, rest assured Astronomer can also help you recover from major region failures by restoring configuration and secrets from a secure and highly available data store. For more information, see [Disaster Recovery](disaster-recovery.md).

## Physical and environment security

Astro leverages all three major public cloud providers (Azure, Google Cloud Platform, Amazon Web Services), thus physical and environmental security is handled entirely by those providers. Each cloud service provider provides an extensive list of compliance and regulatory assurances that they are rigorously tested against, including SOC 1/2-3, PCI-DSS, and ISO27001. For more information, see [Cloud provider security responsibilities](shared-responsibility-model.md#cloud-provider-security-responsibilities).

Astronomer is a global remote company first. The Astronomer offices in the United States are treated as trustless. Employees need to authenticate to all applications and systems using Okta with multi-factor authentication (MFA) when using the office WiFi.

## Data privacy and compliance

Astro is compliant with AICPA SOC 2 controls with respect to the security, availability, and confidentiality Trust Service Categories. To obtain reports related to Astronomer's compliance, such as a SOC 2 Type 2 Report or a Penetration Test Report, visit the [Astronomer Trust Center](https://trust.astronomer.io/).

Astronomer is also [GDPR-compliant](gdpr-compliance.md) as an organization, and the Astro platform is GDPR-ready. Astronomer offers a Data Processing Agreement (DPA), which satisfies the requirements the GDPR imposes on data controllers with respect to data processors.

For organizations operating with protected health information, Astronomer is [HIPAA-compliant](hipaa-compliance.md) as an organization, and the Astro platform is HIPAA-ready.

Additionally, for organizations processing payment card information, Astro is certified as compliant with PCI DSS security standards.

## Data protection

Astro uses both encryption in transit and encryption at rest to protect data across and within the Data and control planes, using strong and secure protocols and ciphers, and built-in public cloud features. For more information, see [Data protection](data-protection.md).

## Secrets management

Astro is designed to secure sensitive information about your external systems. Sensitive information shared with Astronomer is securely stored and transmitted for consumption by your data pipelines. For more information, see [Secrets management](secrets-management.md).

## Patch management in Astro Runtime

Astronomer continuously checks for available security fixes for all software used in Astro Runtime and is committed to delivering these fixes in a timely manner. For more information, see [Security fixes](runtime-version-lifecycle-policy.md#security-fixes).
