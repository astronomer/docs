---
sidebar_label: 'Known Limitations'
title: 'Known Limitations'
id: known-limitations
description: Reference a real-time view of known limitations and planned features for Astro.
---

## Overview

As we build and grow Astro, our team is committed to maintaining transparency about the current limitations of the product as well as the roadmap ahead of us.

The list below represents known issues at the time of writing. We're moving fast to address these and are excited to work with you to identify solutions to some of these foundational questions.

If you have questions or feedback about any item below, reach out to your Customer Success Manager.

## Known Limitations

- In order to invite a user to a Workspace, the user must already be a member of the Organization as described in [Add a User](add-user.md). Workspace invites that can add a user to the Organization are not currently supported.
- If a user changes Workspace roles on Astro, it can take a maximum of 10 minutes for corresponding Airflow permission changes to take effect.
- Astro supports only the Celery Executor. If you currently use the Kubernetes Executor, you might have to modify your tasks to run on Astro.
- Clicking on **Refresh DAG** in the Airflow UI will redirect you to `<org-name>.astronomer.run` (Astro Home Page) instead of the task instance URL. We recommend upgrading to [Runtime 4.0](runtime-release-notes.md#astro-runtime-400), as Airflow 2.2 no longer requires this refresh button in the Airflow UI.
- Deployment API keys can be used to automate code deploys to Astro, but they cannot be used to programmatically update other properties of the Deployment via the Astro CLI.

## Coming Soon

- A new tab in the Cloud UI dedicated to [data lineage](https://www.astronomer.io/guides/airflow-openlineage).
- Improved Workspace roles and permissions.
- Workspace API keys that are accepted by the Astro CLI and can be used to automate the creation and deletion of Deployments.
- Worker Queues, which will allow you to configure tasks within a single Deployment to run on various combinations of infrastructure and configuration.
- A new executor built by Astronomer that will offer intelligent worker packing, task-level resource requests, an improved logging system, and Kubernetes-like task isolation.
- The ability for Organization Owners to create a Cluster without Astronomer's assistance.
- Support for Astro Clusters on Google Cloud Platform and Microsoft Azure.
