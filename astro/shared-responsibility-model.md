---
sidebar_label: 'Shared responsibility model'
title: "Shared responsibility model"
id: shared-responsibility-model
description: Astronomer's policy on shared responsibilities between our team and our customers.
---

Astronomer's highest priority is the security and reliability of your tasks. As an Astro customer, you benefit from a fully-managed data orchestration platform that meets the requirements of the most security-sensitive organizations.

Astro operates on a model of shared responsibility, which means that both the Astronomer team and Astronomer customers are responsible for the security of the platform. This document specifies areas of security ownership for both Astronomer customers and the Astronomer team.

## Astronomer's responsibilities

Astronomer is responsible for providing a secure and reliable managed service offering, including:

- Managing the control plane and core services (Cloud UI, Cloud API, Deployment Access, and Cloud image Repository).
- Securing authentication and authorization to all interfaces (UI, API, and CLI).
- Automating provisioning, scaling, and configuration management of Astro resources in the data plane.
- Completing ongoing maintenance (currency, hardening, patching) and uptime monitoring of Astro resources in the data plane. For example, Kubernetes cluster upgrades.
- Maintaining data encryption (at rest/in flight) of Astro managed components (control and data planes).
- Consistently releasing production-ready and supported distributions of [Astro Runtime](upgrade-runtime.md) for net-new and to-be-upgraded Deployments.
- Upon customer request, execute [Disaster Recovery](disaster-recovery.md) procedure for dedicated Hybrid or Hosted clusters.

## Customer's responsibilities  

The customer is responsible for managing certain security aspects of their Astro Organization and Deployments, including:

- Managing roles and permissions of users and API tokens within their organization and Workspace(s).
- Storing and retrieving [authentication tokens](automation-authentication.md), connections, and [environment variables](environment-variables.md) for data pipelines.
- Integrating with their federated identity management platform for secure single sign-on (SSO) authentication with multi-factor authentication (MFA) and customer managed credentials.
- Developing and maintaining data pipelines with security and quality coding best practices, inclusive of vulnerability management of plugins and dependencies.
- Regularly [upgrading their Deployment(s)](upgrade-runtime.md) to the latest Astro Runtime version to take advantage of new functionality, as well as bug and security fixes.
- [Configuring and managing Deployment resource settings](deployment-settings.md) for data pipeline workloads.
- [Securing the network communications](https://docs.astronomer.io/astro/category/connect-to-external-resources) between their data plane and sensitive data resources.

## Cloud provider security responsibilities

Physical and environmental security is handled entirely by our cloud service providers. Each of our cloud service providers provides an extensive list of compliance and regulatory assurances that they are rigorously tested against, including SOC 1/2-3, PCI-DSS, and ISO27001.

### Azure

See the Azure [compliance](https://azure.microsoft.com/en-ca/overview/trusted-cloud/compliance/), [security](https://azure.microsoft.com/en-ca/overview/security/), and [data center security](https://azure.microsoft.com/en-ca/global-infrastructure/) documentation for more detailed information.

### Amazon

See the AWS [compliance](https://aws.amazon.com/compliance/), [security](https://aws.amazon.com/security/), and [data center security](https://aws.amazon.com/compliance/data-center/controls/) documentation for more detailed information.

### Google

See the GCP [compliance](https://cloud.google.com/security/compliance), [security](https://cloud.google.com/security), and [data center security](https://cloud.google.com/security/infrastructure) documentation for more detailed information.
