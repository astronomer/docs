---
sidebar_label: 'Resilience'
title: "Resilience"
id: resilience
description: Learn how Astronomer leverages Availability Zones to make the Control Plane and Data Plane resilient.
---

## Overview

The Astronomer Cloud Control and Data Planes are architected and deployed on major public clouds to take advantage of their resilient and highly available regions. Regions provide multiple physically separated and isolated Availability Zones (AZs) which are connected through low-latency, high-throughput, and highly redundant networking within a geographic region. Additionally, each AZ has independent power, cooling, and physical security.

Astronomer Cloud leverages AZs for both the Control and Data Planes. The Control Plane leverages 3 AZs per region, while the Data Plane leverages 2 AZs per region. Control Planes and Data Planes are also segregated by Cloud providers, with plans to support more public clouds for the Data Plane. As a result, both planes are expected to survive and recover from an AZ outage, though they may experience some degradation until the impacted resources are re-provisioned/promoted to a non-impacted AZ.

In the case of a full region failure of the Control Plane, the services and data would be recovered in an alternate region by Astronomer. In the case of a full region failure of the Data Plane, Clusters impacted by a full regional outage will be restored to an alternate region (see [Disaster Recovery](disaster-recovery.md) for details).

Astronomer Cloud also provides DDoS protection with always-on traffic monitoring, detection, and automatic attack mitigations.
