---
sidebar_label: 'Features'
title: 'Astro features'
id: features
description: Set environment variables on Astro to specify Airflow configurations and custom logic.
---

Astro is a managed software service that offers a next-generation experience for modern data teams running Apache Airflow, the open source industry standard for data orchestration.

Astro boasts a hybrid deployment model founded on a control plane hosted by Astronomer and a data plane that is hosted in your cloud environment. Both are fully managed by Astronomer. This model offers the self-service convenience of a fully managed service while respecting the need to keep data private, secure, and within corporate boundaries. This solution optimizes security and reduces operational overhead.

Beyond architecture, Astro offers a suite of first-class features that make it easy to author, run, and monitor data pipelines.

## Feature list


- Worker auto-scaling, powered by the Airflow Celery executor and KEDA. See [Worker queues](configure-worker-queues.md).
- The ability to run multiple clusters in your organization's network on AWS, GCP, or Azure.
- Astro Runtime, a collection of Docker images that provides a differentiated data orchestration experience. See [Runtime image architecture](runtime-image-architecture.md).
- Timely support for the latest major, minor, and patch versions of the Apache Airflow open source project.
- Support for role-based access control (RBAC) and single sign-on (SSO) for secure user management and authentication. See [Configure an identity provider (IdP)](configure-idp.md) and [User permissions](user-permissions.md).
- An observability experience that gives you data lineage across your ecosystem as well as real-time insight into the health and resource consumption of your data pipelines on Astro. See  [Data lineage](data-lineage.md] and [Deployment metrics](deployment-metrics.md).