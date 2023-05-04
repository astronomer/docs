---
title: 'Astronomer Docs'
id: home
slug: /
description: 'Learn everything you need to know about Astro and Apache Airflow™'
hide_table_of_contents: true
---

import LinkCardGrid from '@site/src/components/LinkCardGrid';
import LinkCard from '@site/src/components/LinkCard';
import AstroCard from '@site/src/components/AstroCard';
import NewsletterForm from '@site/src/components/NewsletterForm';

<img src="/img/home-logos@2x.png" width="145" height="48" style={{marginBottom: "0.5rem"}} />

# Astronomer Docs

<p className="DocItem__header-description">Learn everything you need to know about Astro and Apache Airflow™</p>

---

<AstroCard />

## Getting started

<LinkCardGrid>
  <LinkCard topIcon label="Get started with the Astro CLI" description="The Astro CLI is the command line interface for data orchestration. It's the easiest way to get started with Apache Airflow and can be used with all Astronomer products." href="/astro/cli/overview" icon="/img/code-icon.svg" />
  <LinkCard topIcon label="Understand Airflow concepts" description="Learn about the fundamentals of how Airflow works and best practices for running it at scale." href="/learn/category/airflow-concepts" icon="/img/airflow-logo-85x85.png" />
  <LinkCard topIcon label="Explore Airflow tutorials" description="Follow step-by-step instructions to get Airflow up and running for any use case." href="/learn/category/airflow-tutorials" icon="/img/doc-icon.svg" />
</LinkCardGrid>

## What's new?

<LinkCardGrid>
  <LinkCard truncate label="Astro Python SDK" description="Simplify ELT pipeline writing using a new SDK from Astronomer." href="/learn/astro-python-sdk" />
  <LinkCard truncate label="Worker queues" description="Run tasks in worker queues which are optimized for their execution." href="/astro/configure-worker-queues" />
  <LinkCard truncate label="Release notes" description="A complete record of the latest changes to Astro." href="/astro/release-notes" />
</LinkCardGrid>
