---
sidebar_label: Overview
title: Astro Cloud IDE
id: overview
description: Learn how to build pipelines with the Cloud IDE.
---

import LinkCardGrid from '@site/src/components/LinkCardGrid';
import LinkCard from '@site/src/components/LinkCard';

<p class="DocItem__header-description">
  A cloud-based, notebook-inspired IDE for writing and testing data pipelines. No Airflow knowledge or local setup required.
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
    label="Move between SQL and Python"
    description="Use SQL tables as dataframes by just referencing your upstream query name, and vice versa."
  />
  <LinkCard
    label="Auto-generate your DAG"
    description="Your dependency graph and DAG file are auto-generated based on data references in your SQL and Python code."
  />
  <LinkCard
    label="Source control your changes"
    description="Check your pipeline into a Git repository with our built-in, easy-to-use Git integration."
  />
  <LinkCard
    label="Deploy with the click of a button"
    description="Using our out-of-the-box CI/CD, you can deploy your DAG to a production runtime on Astro in just a few clicks."
  />
</LinkCardGrid>
