---
sidebar_label: 'Overview'
title: 'Configure a Deployment on Astronomer Software'
id: configure-deployment
description: Learn the ways you can configure individual Airflow Deployments on Astronomer Software
---

An Airflow Deployment on Astronomer is an instance of Apache Airflow that runs in your Astronomer Software cluster. Each Astronomer Software Deployment is hosted on a dedicated Kubernetes namespace, has a dedicated set of resources, and operates with an isolated Postgres metadata database.

A Deployment typically encapsulates a single use case or context. Each Deployment has a number of settings that you can fine-tune so that you're running Airflow optimally for this context. Use the following topics to learn more about each available configuration option on an Astronomer Software Deployment. 

## Deployment creation and deletion

Creating and deleting Deployments can become an operational complexity when you run Airflow across many teams. See the following documentation to learn about all of the options for creating Deployments, deleting Deployments, and ensuring that Deployment resources are returned back to your cluster for future use. 

## Deployment resources

The amount of CPU and memory available to your Deployment defines how many tasks it can run in parallel. See [Deployment resources](deployment-resources.md) to learn how to configure your Deployment's scheduler, executor, and webserver resources. 

## Environment variables

Each Deployment has its own set of environment variables that you can use to define both Airflow-level configurations and DAG objects such as connections. See [Environment variables](environment-variables.md) to learn more about setting these 

## Deploy methods

Astronomer supports several different methods for deploying DAGs and code-based project configurations to Astro. See [Deploy methods overview](deploy-code-overview.md).

When you're ready to automate a deploy mechanism at scale for your team, see [CI/CD](ci-cd.md) to learn how to configure API credentials and examples of CI/CD pipelines in different version management tools.



