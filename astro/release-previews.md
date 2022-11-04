---
sidebar_label: 'Astro release previews'
title: 'Release previews'
id: release-previews
description: Learn about Astronomer release previews. 
---

Astronomer shares release previews to give customers a chance to evaluate and provide feedback on features before they are generally available (GA). Release previews have a different degree of feature maturity. This document defines those release preview stages, and the levels of availability, support, and customer access granted at each stage.

To view support promises for GA releases of Runtime, see [Astro Runtime maintenance and lifecycle policy](runtime-version-lifecycle-policy.md). To submit feedback or a support request for a Public or Private Preview feature, see [Submit a support request](astro-support.md).

## Astro release previews

Astro features can be shared as Private Preview or Public Preview. The table below offers a snapshot on how the release previews differ:

| Release Preview Type | Customer Access | Availability                  | Support                                                                                                                                                                                                                                                   |
| -------------------- | --------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Private Preview      | Invite only.    | No SLA or SLO.                | Product and R&D will be in active communication with customers who are in a Private Preview of a feature to receive feedback, bug reports, questions, and more. Customer Reliability Engineering (CRE) does not provide support for features in Private Preview.                                                                                             |
| Public Preview       | Everyone       | No SLA. Internal SLOs supported by R&D and CRE. | CRE treats all issues within the feature as P3 or P4, depending on the nature of the issue. CRE continues to support remediation for all other issues at defined priority levels, including if a platform issue is caused by a feature in Public Preview. |

## Private Preview

Private Preview offers a select group of customers early access to a feature— to test, offer feedback, and preview a feature before it becomes more widely available.

### Customer access 

An invite to a Private Preview will come from your Customer Success Manager or a member of the Astronomer Product team.

### Availability 

No SLA is set for a feature in Private Preview. Other availability metrics may be set, such as an internal SLO.

### Support

Product and R&D will be in active communication with customers who are in Private Preview of a feature to hear feedback and provide support, including observations on the experience, triaging bugs, and answering questions.

Astronomer's Customer Reliability Engineering (CRE) team does not provide support for features in Private Preview.

## Public Preview

Public Preview offers all customers access to a feature before it is released for GA. The key difference between Public Preview and General Availability is in availability and support for the feature. 

### Customer access 

All Astro customer orgs have access to the feature. Note: some features may have access gated by Role-Based Access Control.

### Availability 

A feature in Public Preview does not have the same SLA commitment as a GA feature. Internal service level objectives (SLO’s) will be set to monitor and support the feature’s availability.

### Support

CRE will treat all issues within a Public Preview feature as P3 or P4, depending on the nature of the issue:

- P3: Loss of use of the feature (not affecting service in general). Feature not working as expected.
- P4: Inquiry about the feature. Information requested on capabilities, navigation, installation, or configuration. Bug affecting a small number of users.

CRE continues to support issue remediation for all other issues at defined priority levels, including if a platform issue is caused by a feature in Public Preview.