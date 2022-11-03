---
sidebar_label: 'Architecture'
title: 'Astro architecture'
id: astro-architecture
description: Astro uses a multi-plane structure to help make Airflow more secure and reliable. Learn how the control plane and data plane work together on the cloud.
---

Astro is a managed service for data orchestration that is built for the cloud and powered by Apache Airflow. Astro is built with a multi-plane architecture which consists of:

- A control plane that is hosted by Astronomer.
- A data plane that can run either in your cloud or in a single-tenant account hosted by Astronomer.

Astro can be activated on Amazon Web Services (AWS), Google Cloud Platform (GCP), or Microsoft Azure. Astronomer runs Astro on managed Kubernetes services for each cloud provider, including AWS Elastic Kubernetes Service (EKS), Google Kubernetes Engine (GKE), and Azure Kubernetes Service (AKS).

The control plane and data plane are managed by Astronomer and require no operational oversight by your organization. The Astro architecture ensures that tasks are executed securely within your corporate network.

![Astro architecture overview](/img/docs/architecture-overview.png)

For more information about Astro architecture, contact [Astronomer support](https://cloud.astronomer.io/support).

## Related documentation

- [Shared responsibility model](shared-responsibility-model.md)
- [Install Astro on AWS](install-aws.md)
- [Install Astro on GCP](install-gcp.md)
- [Install Astro on Azure](install-azure.md)