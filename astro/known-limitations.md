---
sidebar_label: 'Known Limitations'
title: 'Known Limitations'
id: known-limitations
description: Reference a real-time view of known limitations and planned features for Astro.
---

## Overview

As we build and grow Astro, our team is committed to maintaining transparency about the current limitations of the product as well as the roadmap ahead of us.

The list below represents known issues at the time of writing. We're moving fast to address these and are excited to work with customers as we identify solutions to some of these foundational questions.

If you have questions or thoughts about any item below, don't hesitate to reach out to us.

## Known Limitations

- Assistance from our team is required to give the first user in your Organization access to Astro.
- Users cannot be directly invited to an Organization. To add a user to an Organization, you must invite them to a Workspace as described in [Add a User](add-user.md).
- When a user first creates an account, they will be asked to validate their email address. Email validation is not currently required to access Astro, but we encourage users to follow the process anyway as we will enforce it in the future.
- If you're running Astro Runtime `2.1.1`, `3.0.0`, or `3.0.1`, the Astro Runtime field in the Cloud UI shows `Unknown`. Once you upgrade to Runtime 3.0.2+, your Deployment's version of Runtime is correctly listed.
- If a user changes Workspace roles on Astro, it can take a maximum of 10 minutes for corresponding Airflow permission changes to take effect.
- Clicking on **Refresh DAG** in the Airflow UI will redirect you to `<org-name>.astronomer.run` (Astro Home Page) instead of the task instance URL. We recommend upgrading to [Runtime 4.0](runtime-release-notes.md#astro-runtime-400), as Airflow 2.2 no longer supports this refresh button in the Airflow UI.

## Coming Soon

- Long-lasting Deployment API Keys
- Full CLI functionality
- Self-service Cluster
- Analytics
