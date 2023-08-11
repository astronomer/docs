---
sidebar_label: 'Overview'
title: 'Astro Documentation'
id: overview
slug: /
description: Everything you need to know about Astronomer’s modern data orchestration tool for the cloud, powered by Apache Airflow.
hide_table_of_contents: true
---

import LinkCardGrid from '@site/src/components/LinkCardGrid';
import LinkCard from '@site/src/components/LinkCard';
import AstroCard from '@site/src/components/AstroCard';

<p class="DocItem__header-description">Everything you need to know about Astronomer’s modern data orchestration tool for the cloud, powered by Apache Airflow.</p>

<AstroCard />

## Run on the cloud

<LinkCardGrid>
  <LinkCard topIcon label="Create a Deployment" description="A Deployment is an instance of Apache Airflow hosted on Astro." href="/astro/create-deployment" icon="/img/deployment.svg" />
  <LinkCard topIcon label="Deploy code" description="Get your DAGs up and running on Astro." href="/astro/deploy-code" icon="/img/code.svg" />
  <LinkCard topIcon label="Automate with CI/CD" description="Push code to Astro using templates for popular CI/CD tools." href="/astro/ci-cd-templates/template-overview" icon="/img/automation.svg" />
</LinkCardGrid>

## Get started

<LinkCardGrid>
  <LinkCard label="I'm unfamiliar with Apache Airflow" description="Use tutorials and concepts to learn everything you need to know about running Airflow." href="/learn/" icon="/img/airflow-logo.png" />
  <LinkCard label="I'm ready to create my first project" description="Learn how to create an Astro project and run it locally with the Astro command-line interface (CLI)." href="/astro/create-first-dag" icon="/img/astro-monogram.svg" />
</LinkCardGrid>

## Featured Astro docs

<LinkCardGrid>
  <LinkCard truncate label="Get started with the Astro CLI" description="Create an Astro project and run it locally to start developing your DAGs." href="/astro/cli/get-started-cli" />
  <LinkCard truncate label="Automate code deploys with CI/CD" description="Configure your Airflow environments to run faster and cost less." href="/astro/set-up-ci-cd" />
  <LinkCard truncate label="Deploy code to Astro" description="Use the Astro CLI to push your Astro project to a Deployment" href="/astro/deploy-code" />
</LinkCardGrid>
