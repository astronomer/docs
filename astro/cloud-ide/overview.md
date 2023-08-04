---
sidebar_label: Overview
title: Astro Cloud IDE
id: overview
description: Learn how to build pipelines with the Cloud IDE.
slug: /cloud-ide
pagination_next: cloud-ide/quickstart
---

import LinkCardGrid from '@site/src/components/LinkCardGrid';
import LinkCard from '@site/src/components/LinkCard';

<p class="DocItem__header-description">
  A cloud-based, notebook-inspired IDE for writing and testing data pipelines. No Airflow knowledge or local setup is required.
</p>

The Astro Cloud IDE is a notebook-inspired development environment for writing and testing data pipelines with Astro. The Cloud IDE lowers the barrier to entry for new Apache Airflow users and improves the development experience for experienced users.

One of the biggest barriers to using Airflow is writing boilerplate code for basic actions such as creating dependencies, passing data between tasks, and connecting to external services. You can configure all of these with the Cloud UI so that you only need to write the Python or SQL code that executes your work.

In the following image, you can see how you can use the Astro Cloud IDE to write a DAG by only writing SQL. The Astro Cloud IDE automatically generates a DAG with dependencies based only on the Jinja templating in each SQL query. All connections, package dependencies, and DAG metadata are configured with the UI.

![Product Screenshot](/img/cloud-ide/pipeline-editor.png)

## Documentation

<LinkCardGrid>
  <LinkCard truncate label="Quickstart" description="Create data pipelines with the Cloud IDE." href="/astro/cloud-ide/quickstart" />
  <LinkCard truncate label="Deploy a project" description="Push your changes from the Astro Cloud IDE directly to GitHub or a Deployment." href="/astro/cloud-ide/deploy-project" />
  <LinkCard truncate label="Security" description="Learn how the Astro Cloud IDE keeps your code and production Deployments secure." href="/astro/cloud-ide/security" />
</LinkCardGrid>
