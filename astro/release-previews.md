---
sidebar_label: 'Astro release previews'
title: 'Release previews'
id: release-previews
description: Learn about Astronomer release previews. 
---

Astronomer shares release previews to give customers a chance to evaluate and provide feedback on features before they are generally available (GA). Release previews have a different degree of feature maturity. This document defines those release preview stages, and the levels of availability, support, and customer access granted at each stage.

To view the support commitment for GA releases of Astro Runtime, see [Astro Runtime maintenance and lifecycle policy](runtime-version-lifecycle-policy.md). To submit feedback or a support request for a Public or Private Preview feature, see [Submit a support request](astro-support.md).

## Astro release previews

Astro features can be shared as Private Preview or Public Preview. The following table describes the differences between the different release preview types.

| Release Preview Type | Customer Access | Availability                                    | Support Commitment                                                                                                                                                                                                                                                         |
| -------------------- | --------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Private Preview      | Invite only    | No SLA or SLO                                  | Product and Research and Development actively communicate with customers who are using a Private Preview feature to receive feedback, bug reports, and more. Customer Reliability Engineering (CRE) doesn't support Private Preview features. |
| Public Preview       | Everyone        | No SLA. Internal SLOs supported by R&D and CRE | CRE treats all issues related to the feature at a P3 or P4 priority level. See [Submit a support request](https://docs.astronomer.io/astro/astro-support#best-practices-for-support-request-submissions). CRE continues to support remediation for all other issues at defined priority levels, including if a platform issue is caused by a feature in Public Preview.       |

## Private Preview

Private Preview provides a limited group of customers with early access to a feature. Customers can test and provide feature feedback before it becomes more widely available.

### Customer access 

Your organization is invited to participate in a Private Preview by your Customer Success Manager or a member of the Astronomer Product team.

### Availability 

SLAs are not available for Private Preview features. Other agreements such as an internal SLO might be provided at the discretion of Astronomer.

### Support

Product and Research and Development actively communicate with customers who are using a feature in Private Preview to solicit feedback and provide support. This includes observations on their experience, triaging bugs, and answering questions.

The CRE team doesn't support Private Preview features.

## Public Preview

All customers can access Public Preview features before they become GA. The primary difference between Public Preview and GA is the availability of the feature and the support provided by Astronomer. 

### Customer access 

All Astro customers can access Public Preview features. Some feature access might be restricted by role-based access control (RBAC).

### Availability 

Public Preview features don't have the same SLA commitment as GA features. Astronomer sets Internal SLOs to monitor and support Public Preview features.

### Support

CRE assigns a P3 or P4 severity level to all Public Preview issues. The following are the definitions for each severity level:

- P3: Loss of use of a feature, or a feature not working as expected. Service is not affected..
- P4: Feature inquiries, or bugs limited to a small number users. Inquiries can include questions about feature capabilities, navigation, installation, or configuration.

If a feature in Public Preview causes an issue with the data plane, CRE treats that issue with the priority of a generally available feature. 