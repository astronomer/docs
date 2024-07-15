---
sidebar_label: 'Roll back a deploy'
title: 'Roll back an image deploy on Astronomer Software'
id: deploy-rollbacks
description: Learn how to roll back to a deploy, which lets you run earlier version of your project code.
---

Deploy rollbacks are an emergency option if a Deployment unexpectedly stops working after a recent deploy. For example, if one of your DAGs worked in development but suddenly fails in a mission-critical production Deployment, you can roll back to your previous deploy to quickly get your pipeline running again. This allows you to revert your deployment to a known good state while you investigate the cause of the failure. You can roll back to any deploy in the last three months regardless of your DAG code or Deployment settings. However, rollbacks are only supported for Runtime 5.0.0 and above or its equivalent Apache Airflow® version, 2.3.0 and above.

## Prerequisites

- You must be at least a Deployment Editor or otherwise have the permission `deployment.images.push` or `system.deployments.images.push` to roll back a Deployment.
- Your Deployment must be on Astro Runtime 5 (Airflow 2.3) or later. Rolling back to any version before Astro Runtime 5 is not supported. 
- Your Deployment must be configured to use image or DAG-only deploys. Rollbacks are not supported for NFS deploys and Git sync deploys.
- Your Software installation must have `global.dagOnlyDeployment.enabled=True`
  
## Configure deploy rollbacks

To use deploy rollbacks, you must have them enabled for your entire installation. This configuration allows individual Deployment users with sufficient permissions to optionally enable them in specific Deployments.

Configure the following values in your `values.yaml` file:
  ```yaml
  # Enable APIs to modify deploys
  astronomer:
    houston:
      config:
        deployments:
          enableUpdateDeploymentImageEndpoint: true
  # Enable rollback feature flag
  global:
      deployRollbackEnabled: true
  # Enable cleanup feature flag
  houston:
      cleanupDeployRevisions:
          enabled:  true
  # Configure which data to clean up
  houston:
      cleanupDeployRevisions:
          olderThan:  90
  ```

After you set this configuration, you can enable deploy rollbacks for individual Deployments. This configuration also enables cleanup of any deploy information that are older than 90 days. See [Apply a Config Change](software/apply-platform-config.md) for more information on how to modify these values.

## Enable deploy rollbacks

If deploy rollbacks are configured for your installtion, you can enable them in individual Deployments through the Deployment Settings page.

1. In the Software UI, open your Deployment.
2. On the **Settings** page, toggle **Rollback Deploy** to **Enable**.

## Roll back to a deploy

:::danger

Astronomer recommends triggering Deployment rollbacks only as a last resort for recent deploys that aren't working as expected. Deployment rollbacks can be disruptive, especially if you triggered multiple deploys between your current version and the rollback version. See [What happens during a deploy rollback](#what-happens-during-a-deploy-rollback) before you trigger a rollback to anticipate any unexpected effects.

:::

1. In the Software UI, open your Deployment, then go to **Deploy History**.
2. Find the deploy you want to roll back to in the **Deploys** table, then click **Deploy**.
3. Write a description for why you're triggering the rollback, then confirm the rollback.

### What happens during a deploy rollback

A deploy rollback is a new deploy of a previous version of your code. This means that the rollback deploy appears as a new deploy in **Deploy History**, and the records for any deploys between your current version and rollback version are still preserved. In Git terms, this is equivalent to `git revert`.

When you trigger a rollback, the following information is rolled back:

- All project code, including DAGs.
- Your Astro Runtime version. Note that if you roll back to a restricted Runtime version they can include major bugs and performance issues.
- Your Deployment's DAG deploy setting.

The following information isn't rolled back:

- Your Deployment's resource configurations, such as executor and scheduler configurations.
- Your Deployment's environment variable values.
- Any other Deployment settings that you configure through the Astro UI, such as your Deployment name and description. 
- For Runtime version downgrades, any data related to features that are not available in the rollback version are erased from the metadata database and not recoverable.

Logs related to the rollback are exported to Elasticsearch.
