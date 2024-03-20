---
title: "Custom Deployment role permissions references"
sidebar_label: Deployment role permissions
id: deployment-role-reference
description: Learn about each possible permission that you can assign to custom Deployment roles
---

:::publicpreview
:::

:::info

This feature is available only in the Enterprise tier.

:::


This document contains all available permissions that you can assign to a [custom Deployment role](customize-deployment-roles). Permissions are organized by the object that the permissions belong to.

## Deployment

- `deployment.get`: Get information about the Deployment, including its details and resource configurations.
- `deployment.update`: Update information about the Deployment, including its details and resource configurations.
- `deployment.delete`: Delete the Deployment.

## Deployment Airflow AdminMenu

- `deployment.airflow.adminMenu.get`: View the **Admin** menu in the Airflow UI.

## Deployment Airflow Astronomer

- `deployment.airflow.astronomer.get`: View the **Astronomer** menu in the Airflow UI.

## Deployment Airflow AuditLog

- `deployment.airflow.auditLog.get`: View the **Audit Log** menu in the Airflow UI.

## Deployment Airflow BrowseMenu

- `deployment.airflow.browseMenu.get`: View the **Browse** menu in the Airflow UI.

## Deployment Airflow ClusterActivity

- `deployment.airflow.clusterActivity.get`: View the **Cluster Activity** menu in the Airflow UI.

## Deployment Airflow Config

- `deployment.airflow.configMenu.get`: View the **Config** menu in the Airflow UI.

### Deployment Airflow Connection

- `deployment.airflow.connection.get`: View connections in the Airflow UI.
- `deployment.airflow.connection.create`: Create connections in the Airflow UI.
- `deployment.airflow.connection.update`: Update connections in the Airflow UI.
- `deployment.airflow.connection.delete`: Delete connections in the Airflow UI.

### Deployment Airflow DAG

- `deployment.airflow.dag.get`: View DAGs in the Airflow UI or Astro UI **DAGs** page.
- `deployment.airflow.dag.update`: Update DAGs in the Airflow UI or Astro UI **DAGs** page.
- `deployment.airflow.dag.delete`: Delete DAGs in the Airflow UI or Astro UI **DAGs** page.

## Deployment Airflow DagCode

- `deployment.airflow.dagCode.get`: View the source code for DAGs in the Airflow UI or Astro UI **DAGs** page.

## Deployment Airflow DagDependencies

- `deployment.airflow.dagDependencies.get`: View the task dependencies for DAGs in the Airflow UI.

### Deployment Airflow DAGRun

- `deployment.airflow.dagRun.get`: View DAG runs in the Airflow UI or Astro UI **DAGs** page.
- `deployment.airflow.dagRun.create`: Create DAG runs in the Airflow UI or Astro UI **DAGs** page.
- `deployment.airflow.dagRun.update`: Update DAG runs in the Airflow UI or Astro UI **DAGs** page.
- `deployment.airflow.dagRun.delete`: Delete DAG runs in the Airflow UI or Astro UI **DAGs** page.

## Deployment Airflow Datasets

- `deployment.airflow.datasets.get`: View the datasets for DAGs in the Airflow UI.

## Deployment Airflow Docs

- `deployment.airflow.docs.get`: View the documentation for DAGs in the Airflow UI.

## Deployment Airflow ImportError

- `deployment.airflow.importError.get`: View any import errors for DAGs in the Airflow UI.

## Deployment Airflow Job

- `deployment.airflow.job.get`: View scheduler jobs in the Airflow UI.

## Deployment Airflow Plugin

- `deployment.airflow.plugin.get`: View plugins in the Airflow UI.

## Deployment Airflow Pool

- `deployment.airflow.pool.get`: View pools in the Airflow UI.
- `deployment.airflow.pool.create`: Create pools in the Airflow UI.
- `deployment.airflow.pool.update`: Update pools in the Airflow UI.
- `deployment.airflow.pool.delete`: Delete pools in the Airflow UI.

## Deployment Airflow Provider

- `deployment.airflow.provider.get`: View installed provider packages in the Airflow UI.

## Deployment Airflow SlaMiss

- `deployment.airflow.slaMiss.get`: View details about SLA misses in the Airflow UI.

## Deployment Airflow TaskInstance

- `deployment.airflow.taskInstance.get`: View task instances in the Airflow UI or Astro UI **DAGs** page.
- `deployment.airflow.taskInstance.create`: Create task instances in the Airflow UI or Astro UI **DAGs** page.
- `deployment.airflow.taskInstance.update`: Update task instances in the Airflow UI or Astro UI **DAGs** page.
- `deployment.airflow.taskInstance.delete`: Delete task instances in the Airflow UI or Astro UI **DAGs** page.

## Deployment Airflow TaskLog

- `deployment.airflow.taskLog.get`: View task logs in the Airflow UI or Astro UI **DAGs** page.

## Deployment Airflow TaskReschedule

- `deployment.airflow.taskReschedule.get`: View task reschedules in the Airflow UI or Astro UI **DAGs** page.

## Deployment Airflow Trigger

- `deployment.airflow.trigger.get`: View information about triggers in the Airflow UI.

## Deployment Airflow Variable

- `deployment.airflow.variable.get`: View variables in the Airflow UI.
- `deployment.airflow.variable.create`: Create variables in the Airflow UI.
- `deployment.airflow.variable.update`: Update variables in the Airflow UI.
- `deployment.airflow.variable.delete`: Delete variables in the Airflow UI.

## Deployment Airflow Website

- `deployment.airflow.website.get`: Access the Airflow UI homepage.

## Deployment Airflow XCom

- `deployment.airflow.xcom.get`: View XComs data in the Airflow UI.
- `deployment.airflow.xcom.delete`: View XComs data in the Airflow UI.

## Deployment Alerts

- `deployment.alerts.get`: View configured Deployment alerts.
- `deployment.alerts.create`: Create Deployment-level Astro alerts in the Astro UI or through the Astro API.
- `deployment.alerts.update`: Update Deployment-level Astro alerts in the Astro UI or through the Astro API.
- `deployment.alerts.delete`: Delete Deployment-level Astro alerts in the Astro UI or through the Astro API.

## Deployment ApiKeys (Deprecated)

Astro API Keys are deprecated and will no longer be available on June 1, 2024. If you still use API Keys, you can use these permissions. Learn more about using [Deployment API Tokens](deployment-api-tokens.md), which replace Deployment API Key functionality.

- `deployment.apiKeys.get`: View Deployment API keys.
- `deployment.apiKeys.delete`: Delete Deployment API keys.

## Deployment ApiTokens

- `deployment.apiTokens.get`: View Deployment API tokens in the Astro UI or through the Astro API.
- `deployment.apiTokens.create`: Create Deployment API tokens in the Astro UI or through the Astro API.
- `deployment.apiTokens.update`: Update Deployment API tokens in the Astro UI or through the Astro API.
- `deployment.apiTokens.delete`: Delete Deployment API tokens in the Astro UI or through the Astro API.
- `deployment.apiTokens.rotate`: Rotate Deployment API tokens in the Astro UI or through the Astro API.

## Deployment Deploys

- `deployment.deploys.get`: View deploy history for the Deployment in the Astro UI or through the Astro API.
- `deployment.deploys.create`: Make Deploys to the Deployment.
- `deployment.deploys.update`: Roll back deploys to the Deployment.

## Deployment EnvObjects

- `deployment.envObjects.get`: View Airflow objects created in the Astro **Environments** page.
- `deployment.envObjects.create`: Create Airflow objects in the Astro **Environments** page.
- `deployment.envObjects.update`: Update Airflow objects in the Astro **Environments** page.
- `deployment.envObjects.delete`: Delete Airflow objects in the Astro **Environments** page.

## Deployment Logs

- `deployment.logs.get`: View Deployment logs in the Astro UI.

## Deployment Metrics

- `deployment.metrics.get`: View Deployment **Analytics** in the Astro UI.

## Deployment Teams

- `deployment.teams.get`: View Teams belonging to a Deployment.
- `deployment.teams.delete`: Update Team membership to a Deployment.

## Deployment Users

- `deployment.users.get`: View users belonging to a Deployment.
- `deployment.users.delete`: Update user membership to a Deployment.
