---
title: 'Astronomer Software Documentation'
sidebar_label: 'Overview'
id: overview
slug: /
description: 'Documentation for how to run Airflow at enterprise scale with Astronomer Software.'
---

## Overview

Astronomer Software is the best way to run Apache Airflow in your private cloud. Using Astronomer's tooling, you can have fine-tuned control over every aspect of your Airflow experience.

## Features

Astronomer Software's key features ensure that enterprise organizations can run Apache Airflow securely and reliably:

- Push-button Deployments of Apache Airflow
- Role-based access control (RBAC) for configurable and secure user management
- Extensive cloud, network, third party provider, and system component configurations via Helm
- System logging, monitoring, and alerts via Grafana and Kibana
- Astronomer Certified, a collection of Docker images that provides a differentiated data orchestration experience. Astronomer Certified includes timely support for the latest major, minor, and patch versions of Airflow

## Architecture

The following diagram shows how you can run Airflow in your private cloud using Astronomer Software:

![Astronomer Software Overview](https://assets2.astronomer.io/main/enterpriseArchitecture.svg)

## Installation Guides

If you are new to Astronomer Software, use the following guides to install the system on your cloud service:

* [Amazon Web Services EKS](install-aws-standard.md)
* [Google Cloud Platform GKE](install-gcp-standard.md)
* [Microsoft Azure AKS](install-azure-standard.md)

## Customizing Your Installation

Because the platform uses Helm, it's easy to customize your Software installation. Below are some guides for most common customizations:

* [Integrating Auth Systems](integrate-auth-system.md)
* [Configuring Resources with Helm](manage-platform-users.md)
* [Configuring a Registry Back End](registry-backend.md)
* [Built-in Alerts](platform-alerts.md)

## Administration

There are many tools at your disposal for administering Astronomer:

* [The Houston API Playground](houston-api.md)
* [Metrics](grafana-metrics.md)
* [Using Kibana](kibana-logging.md)
* [Using kubectl](kubectl.md)
* [Pulling Postgres Credentials](access-airflow-database.md)
* [Upgrade to a Patch Version of Astronomer Software](upgrade-astronomer-stable.md/)

## License

Usage of Astronomer requires an [Astronomer Platform Software Edition license](https://github.com/astronomer/astronomer/blob/master/LICENSE).
