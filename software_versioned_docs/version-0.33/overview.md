---
title: 'Astronomer Software documentation'
sidebar_label: 'Overview'
id: overview
slug: /
description: 'Documentation for how to run Airflow at enterprise scale with Astronomer Software.'
hide_table_of_contents: true
---

import LinkCardGrid from '@site/src/components/LinkCardGrid';
import LinkCard from '@site/src/components/LinkCard';

<p class="DocItem__header-description">Astronomer Software is the best way to run Apache Airflow in your private cloud. Using Astronomer's tooling, you can have fine-tuned control over every aspect of your Airflow experience.</p>

import AstroCard from '@site/src/components/AstroCard';

<AstroCard title="Need a managed Airflow solution?" />

## Run Airflow in your private cloud using Astronomer Software

The following diagram shows how you can run Airflow in your private cloud using Astronomer Software:

![Astronomer Software Overview](/img/software/enterpriseArchitecture.svg)

## Get Started
<LinkCardGrid>
  <LinkCard truncate label="Installation guides" description="Install Astronomer Software on your cloud." href="/software/category/install" />
  <LinkCard truncate label="Integrate an auth system" description="Set up enterprise-grade user authentication on Astronomer Software." href="/software/integrate-auth-system" />
  <LinkCard truncate label="CI/CD and automation" description="Use the Houston API and CI/CD tools to automate code deploys and changes to your platform." href="/software/ci-cd" />
</LinkCardGrid>

## Astronomer Software features
<LinkCardGrid>
  <LinkCard label="Push-button Deployments" description="Deploy an Airflow instance with the push of a button." />
  <LinkCard label="Role-based access control" description="Use an extensive RBAC system for configurable and secure user management." />
  <LinkCard label="Configurations via Helm" description="Manage cloud, network, third party provider, and system component configurations using Helm." />
  <LinkCard label="Grafana & Kibana integrations" description="System logging, monitoring, and alerts are available through Grafana and Kibana." />
  <LinkCard label="Astronomer Docker images" description="Run versions of Airflow with extended support lifecycles and additional bug testing." />
</LinkCardGrid>

## Most popular software docs
<LinkCardGrid>
  <LinkCard truncate label="Release notes" description="A list of all changes in the latest version of Astronomer Software." href="/software/release-notes" />
  <LinkCard truncate label="Customize image" description="Guides and considerations for customizing your Astro project and fine-tuning Airflow." href="/software/customize-image" />
  <LinkCard truncate label="Create a project" description="Create all of the necessary files to run Airflow locally or on Astronomer Software." href="/software/create-project" />
</LinkCardGrid>
