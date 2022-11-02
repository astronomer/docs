---
sidebar_label: Overview
title: Astro Cloud IDE
id: overview
description: Learn how to build pipelines with the Cloud IDE.
slug: /cloud-ide
---

import LinkCardGrid from '@site/src/components/LinkCardGrid';
import LinkCard from '@site/src/components/LinkCard';

<p class="DocItem__header-description">
  A cloud-based, notebook-inspired IDE for writing and testing data pipelines. No Airflow knowledge or local setup is required.
</p>

:::caution

<!-- id to make it easier to remove: cloud-ide-preview-banner -->

The Cloud IDE is currently in _Public Preview_ and it is available to all Astro customers. It is still in development and features and functionality are subject to change.

If you have any feedback, please submit it to the [Astro Cloud IDE product portal](https://portal.productboard.com/75k8qmuqjacnrrnef446fggj).

:::

The Astro Cloud IDE is a notebook-inspired development environment for writing and testing data pipelines with Astro. The Cloud IDE lowers the barrier to entry for new Apache Airflow users and improves the development experience for experienced users.

One of the biggest barriers to using Airflow is writing boilerplate code for basic actions such as creating dependencies, passing data between tasks, and connecting to external services. You can configure all of these with the Cloud UI so that you only need to write the Python or SQL code that executes your work.

In the following image, you can see how you can use the Astro Cloud IDE to write a DAG by only writing SQL. The Astro Cloud IDE automatically generates a DAG with dependencies based only on the Jinja templating in each SQL query. All connections, package dependencies, and DAG metadata are configured with the UI.

![Product Screenshot](/img/cloud-ide/pipeline-editor.png)

<!-- insert demo video -->

## Cloud IDE Features

<LinkCardGrid>
  <LinkCard
    label="Focus on task logic"
    description="Turn everyday Python and SQL into Airflow-ready DAG files that follow the latest best practices."
  />
  <LinkCard
    label="Handle data seamlessly"
    description="Pass data directly from one task to another using a notebook-style interface. No configuration required."
  />
  <LinkCard
    label="Move between SQL and Python"
    description="Use SQL tables as dataframes by referencing your upstream query name, and query your dataframes directly from SQL."
  />
  <LinkCard
    label="Auto-generate your DAG"
    description="Your dependency graph and DAG file are auto-generated based on data references in your SQL and Python code."
  />
  <LinkCard
    label="Source control your changes"
    description="Push your pipeline to a Git repository with a built-in Git integration."
  />
  <LinkCard
    label="Deploy directly to Astro"
    description="Use the included CI/CD script to deploy your code to a production Deployment on Astro."
  />
</LinkCardGrid>

## Documentation

<LinkCardGrid>
  <LinkCard truncate label="Quickstart" description="Create data pipelines with the Cloud IDE." href="/astro/cloud-ide/quickstart" />
  <LinkCard truncate label="Deploy a project" description="Push your changes from the Astro Cloud IDE directly to GitHub or a Deployment." href="/astro/cloud-ide/deploy-project" />
  <LinkCard truncate label="Security" description="Learn how the Astro Cloud IDE keeps your code and production Deployments secure." href="/astro/cloud-ide/security" />
</LinkCardGrid>
