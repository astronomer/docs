---
sidebar_label: 'Architecture'
title: 'Astro architecture'
id: astro-architecture
description: Astro uses a multi-plane structure to help make Airflow more secure and reliable. Learn how the control plane and data plane work together on the cloud.
---

Astro Hosted is a managed service for data orchestration that is built for the cloud and powered by Apache Airflow. Your Airflow environments are hosted and managed entirely by Astronomer, enabling you to shift your focus from infrastructure to data. 

Astro Hosted consists of three core components for managing Airflow, all hosted on Astronomer's cloud:

- The _Astro control plane_ is Astronomer's interface for managing your Airflow environments in the cloud. It includes the Cloud UI, the Astro CLI, and Cloud API.
- _Astro clusters_ are dedicated Kubernetes clusters that can run multiple Airflow environments.
- A _Deployment_ is an Airflow environment running on Astro. Each Deployment includes all of the core Airflow components, plus additional Astronomer tooling that help you optimize resource usage, observability, and security.

Astro Deployments can securely connect to external data services so that you can place Airflow at the heart of your data ecosystem. 

![Astro Hosted overview](/img/docs/architecture-overview.png)



