---
sidebar_label: Overview
title: Astro Cloud IDE
id: overview
description: Learn how to build pipelines with the Cloud IDE.
---

import LinkCardGrid from '@site/src/components/LinkCardGrid';
import LinkCard from '@site/src/components/LinkCard';

<p class="DocItem__header-description">
  A notebook-style interface for writing and testing pipelines with no Airflow knowledge or local setup required.
</p>

## Cloud IDE Features

<LinkCardGrid>
  <LinkCard
    label="Focus on task logic"
    description="Turn everyday Python and SQL into Airflow-ready DAG files that follow the latest best practices."
  />
  <LinkCard
    label="Handle data seamlessly"
    description="Pass data directly from one task to another via our familiar, notebook-style interface. No configuration required."
  />
  <LinkCard
    label="Standardize on Airflow primitives"
    description="Produce a best-practice Airflow DAG file that leverages the latest-and-greatest APIs from the Airflow & Astronomer communities."
  />
  <LinkCard
    label="Auto-generate your DAG"
    description="Your dependency graph is auto-generated based on data references in your SQL and Python code."
  />
  <LinkCard
    label="Commit your changes to Git"
    description="Check your pipeline into a Git repository with our built-in, easy-to-use Git integration."
  />
  <LinkCard
    label="Deploy with the click of a button"
    description="Using our out-of-the-box CI/CD, you can deploy your DAG to Astro in just a few clicks."
  />
</LinkCardGrid>
