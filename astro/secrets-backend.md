---
title: 'Configure an external secrets backend on Astro'
sidebar_label: 'Overview'
id: secrets-backend
description: "Learn to configure a secrets backend on Astro to store Airflow connections and variables"
---

Apache Airflow [variables](https://docs.astronomer.io/learn/airflow-variables) and [connections](https://docs.astronomer.io/learn/connections) often contain sensitive information about your external systems that you need to keep secret in a secure and centralized location. You can [choose a management strategy](manage-connections-variables.md) that complies with your organization's security requirements.

Using secrets to set Airflow connections requires knowledge of how to generate Airflow connection in URI or JSON format. See [Import and export Airflow connections and variables](import-export-connections-variables.md) for guidance on how to export your connections and variables based on where they are stored.

:::tip

If you need to access your secrets backend from your local Airflow, you can mount your user credentials to a local Airflow environment. While this implementation is not recommended for Astro Deployments, it lets you quickly test pipelines with data hosted in your cloud. See [Authenticate to cloud services](cli/authenticate-to-clouds.md).

:::

## Available integrations

Secrets backend integrations can be configured individually with each Astro Deployment by someone with [**Workspace Operator**](user-permissions.md#workspace-roles) permissions.

Astro integrates with the following secrets backend tools:

- [Hashicorp Vault](secrets-backend/hashicorp-vault.md)
- [AWS Systems Manager Parameter Store](secrets-backend/aws-paramstore.md)
- [AWS Secrets Manager](secrets-backend/aws-secretsmanager.md)
- [Google Cloud Secret Manager](secrets-backend/gcp-secretsmanager.md)
- [Azure Key Vault](secrets-backend/azure-key-vault.md)

## How Airflow finds an Airflow connection or variable

If you configure a secrets backend on Astro, you can still continue to define Airflow variables and connections either [as environment variables](environment-variables.md) or in the Airflow UI. Airflow checks for the value of an Airflow variable or connection in the following order:

1. Secrets backend
2. Environment variables
3. The Airflow UI
