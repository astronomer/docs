---
sidebar_label: 'Architecture'
title: 'Astro architecture'
id: astro-architecture
description: Astro uses a multi-plane structure to help make Airflow more secure and reliable. Learn how the control plane and data plane work together on the cloud.
---


Astro is a managed service for data orchestration that is built for the cloud and powered by Apache Airflow. Astro is built with a multi-plane architecture which consists of a control plane that is hosted by Astronomer, and a data plane that can run either in your cloud or in a single-tenant account hosted by Astronomer. In all cases, both the control plane and data plane are managed by Astronomer and require no operational oversight by your team.

Astro's architecture ensures that tasks are executed securely within your network and corporate boundaries, while enabling Astronomer to deliver the full promises of a managed service. The following diagram outlines how the control plane, data plane, and users are connected to enable the Astro feature set. This architecture applies to Astro on Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure.

For more information on Astro's architecture, contact [Astronomer support](https://cloud.astronomer.io/support).

![Astro architecture overview](/img/docs/architecture-overview.png)

