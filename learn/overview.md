---
title: 'Learn'
sidebar_label: 'Overview'
id: overview
slug: /
description: 'Use tutorials and concepts to learn everything you need to know about Apache Airflow and Astro'
hide_table_of_contents: true
---

import LinkCardGrid from '@site/src/components/LinkCardGrid';
import LinkCard from '@site/src/components/LinkCard';
import AstroCard from '@site/src/components/AstroCard';

<p class="DocItem__header-description">Use tutorials and concepts to learn everything you need to know about Apache Airflow and Astro.</p>

## New to Airflow?

<LinkCardGrid>
  <LinkCard label="Get started with Apache Airflow" description="Set up Airflow and run your first DAG in under an hour." href="/learn/get-started-with-airflow" icon="/img/airflow-logo.png" />
  <LinkCard label="Write a DAG with the Astro Python SDK" description="Build a production-ready ETL pipeline with the Astro Python SDK." href="/learn/astro-python-sdk" icon="/img/astro-monogram.svg" />
</LinkCardGrid>

## Featured tutorials

<LinkCardGrid>
  <LinkCard label="Get started with Apache Airflow, Part 2" description="Use providers and connect your Airflow instance to external tools." href="/learn/get-started-with-airflow-part-2" truncate />
  <LinkCard label="Orchestrate Snowflake with Airflow" description="Get enhanced observability and compute savings while orchestrating your Snowflake jobs." href="/learn/airflow-snowflake" truncate />
  <LinkCard label="Integrate OpenLineage and Airflow" description="Get lineage metadata from your DAGs using OpenLineage and Marquez." href="/learn/airflow-openlineage" truncate />
</LinkCardGrid>

## Featured Airflow concepts

<LinkCardGrid>
  <LinkCard label="Datasets and Data-Aware Scheduling in Airflow" description="Master the datasets feature in Airflow 2.4." href="/learn/airflow-datasets" truncate />
  <LinkCard label="Data quality and Airflow" description="Learn data quality best practices and compare data quality tools." href="/learn/data-quality" truncate />
  <LinkCard label="Dynamic Tasks in Airflow" description="Generate tasks dynamically at runtime." href="/learn/dynamic-tasks" truncate />
</LinkCardGrid>

<AstroCard />

