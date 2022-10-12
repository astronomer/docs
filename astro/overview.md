---
sidebar_label: 'Overview'
title: 'Astro Documentation'
id: overview
slug: /
description: Everything you need to know about Astronomer’s modern data orchestration tool for the cloud, powered by Apache Airflow.
---

Astro is a managed software service that offers a next-generation experience for modern data teams running Apache Airflow, the open source industry standard for data orchestration.

Astro boasts a hybrid deployment model founded on a control plane hosted by Astronomer and a data plane that is hosted in your cloud environment. Both are fully managed by Astronomer. This model offers the self-service convenience of a fully managed service while respecting the need to keep data private, secure, and within corporate boundaries. This solution optimizes security and reduces operational overhead.

Beyond architecture, Astro offers a suite of first-class features that make it easy to author, run, and monitor data pipelines.

## Features

The key features of the Astro architecture include:

- Worker auto-scaling, powered by the Airflow Celery executor + KEDA.
- The ability to run multiple clusters in your organization's network on AWS, GCP, or Azure.
- Astro Runtime, a collection of Docker images that provides a differentiated data orchestration experience.
- Timely support for the latest major, minor, and patch versions of the Apache Airflow open source project.
- Support for role-based access control (RBAC) and single sign-on (SSO) for secure user management and authentication.
- An observability experience that gives you insight into the health and resource consumption of your tasks and pipelines in real time.

## Architecture

The following diagram outlines how the control plane, data plane, and users are connected to enable these features:

![High level overview of Astro's architecture](/img/docs/architecture-overview.png)

## Get started

Astronomer support will schedule an onboarding session for your initial install. Astronomer recommends that you review the following topics after your installation is complete:

- [Install the Astro CLI](cli/install-cli.md)
- [Develop your Astro project](develop-project.md)
- [Configure your Deployment](configure-deployment-resources.md)

If you have a feature request or a bug to report, contact [Astronomer support](https://cloud.astronomer.io/support). We're here to help.

To check the operational status of Astro, visit the [status page](https://status.astronomer.io). Click **Subscribe to Updates**  and then enter your email address to receive a notification when an incident is created, updated, or resolved.
