---
title: 'Configure a secrets backend'
sidebar_label: 'Overview'
id: secrets-backend
description: "Learn to configure a secrets backend on Astro to store Airflow connections and variables"
---

Apache Airflow [variables](https://docs.astronomer.io/learn/airflow-variables) and [connections](https://docs.astronomer.io/learn/connections) often contain sensitive information about your external systems that you need to keep in a _secrets backend_ tool, which stores secrets in a secure and centralized location. Unlike other management strategies, such as using Environment Variables or working with connections and variables in the Airflow UI, secrets backends require a third-party secrets manager. This means that you can use a secrets manager administered by your organization for existing security protocols, or you need to choose and set up a secrets backend. 

This document explains the available secrets backend integrations supported by Astro and how Airflow finds connections and variables if you use multiple strategies to manage them.

See [Manage connections and variables](manage-connections-variables.md) to learn more about your available options and decide whether using a secrets backend complies with your organization's security requirements.

## Available integrations

Secrets backend integrations can be configured individually with each Astro Deployment by someone with [**Workspace Operator**](user-permissions.md#workspace-roles) permissions. 

Using secrets to set Airflow connections requires knowledge of how to generate Airflow connections in URI or JSON format. See [Import and export Airflow connections and variables](import-export-connections-variables.md) for guidance on how to export your connections and variables based on where they are stored.

Astro integrates with the following secrets backend tools:

- [AWS Secrets Manager](secrets-backend/aws-secretsmanager.md)
- [AWS Systems Manager Parameter Store](secrets-backend/aws-paramstore.md)
- [Azure Key Vault](secrets-backend/azure-key-vault.md)
- [Google Cloud Secret Manager](secrets-backend/gcp-secretsmanager.md)
- [Hashicorp Vault](secrets-backend/hashicorp-vault.md)

## How Airflow finds connections or variables

:::tip

If you need to access your secrets backend from your local Airflow, you can mount your user credentials to a local Airflow environment. While this implementation is not recommended for Astro Deployments, it lets you quickly test pipelines with data hosted in your cloud. See [Authenticate to cloud services](cli/authenticate-to-clouds.md).

:::

If you configure a secrets backend on Astro, you can still continue to define Airflow variables and connections as either [environment variables](environment-variables.md) or in the Airflow UI. Airflow checks for the value of an Airflow variable or connection in the following order:

1. Secrets backend
2. Environment variables
3. The Airflow UI