---
sidebar_label: 'Known Limitations'
title: 'Known Limitations'
id: known-limitations
description: Reference a real-time view of known limitations and planned features for Astronomer Cloud.
---

## Overview

As we build and grow Astronomer Cloud, our team is committed to maintaining transparency about the current limitations of the product as well as the roadmap ahead of us.

The list below represents known issues at the time of writing. We're moving fast to address these and are excited to work with customers as we identify solutions to some of these foundational questions.

If you have questions or thoughts about any item below, don't hesitate to reach out to us.

## Known Limitations

- Assistance from our team is required to give the first user in your Organization access to Astronomer Cloud.
- When a user first creates an account, they will be asked to validate their email address. Email validation is not currently required to access Astronomer Cloud, but we encourage users to follow the process anyway as we will enforce it in the future.
- During the install process, your team will be added to 1 Astronomer Workspace that supports multiple users and Deployments. To create additional Workspaces in your Organization, assistance from our team is required.
- If you're running Astronomer Runtime `2.1.1`, `3.0.0`, or `3.0.1`, the Astronomer Runtime field in the Astronomer UI shows `Unknown`. Once you upgrade to Runtime 3.0.2+, your Deployment's version of Runtime is correctly listed.
- We do not currently support PgBouncer, but the RDS instance provisioned in your Cluster will support around 1000 connections to your database, enough to support 10-12 Deployments.
- If a user changes Workspace roles on Astronomer, it can take a maximum of 10 minutes for corresponding Airflow permission changes to take effect.
- The usage of [Deployment API Keys](api-keys.md) in [CI/CD processes](ci-cd.md) currently requires fetching a short-lived authentication token and making requests directly to our Docker registry and the Astronomer API. Native support for Deployment API Keys in the Astronomer Cloud CLI is coming soon.
- The Astronomer Cloud CLI is generally limited to `astrocloud dev` commands, in addition to `astrocloud deploy` and `astrocloud auth`.
- Clicking on **Refresh DAG** in the Airflow UI will redirect you to `<org-name>.astronomer.run` (Astronomer Home Page) instead of the task instance URL. We recommend upgrading to [Runtime 4.0](runtime-release-notes.md#astronomer-runtime-400), as Airflow 2.2 no longer supports this refresh button in the Airflow UI.
- [Deferrable operators](deferrable-operators.md) cannot be tested in local Airflow environments running via the Astronomer Cloud CLI. To use deferrable operators, you must have a Deployment running [Runtime 4.0+](runtime-release-notes.md#astronomer-runtime-400).

## Coming Soon

- Long-lasting Deployment API Keys
- Support for CLI Install via Homebrew
- Single Sign-On
- Full CLI functionality
- Self-service Cluster and Workspace creation
- Analytics
