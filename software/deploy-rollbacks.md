---
sidebar_label: 'Roll back a deploy'
title: 'Roll back an image deploy on Astronomer Software'
id: deploy-rollbacks
description: Learn how to roll back to a deploy, which lets you run earlier version of your project code.
---

Deploy rollbacks are an emergency option if a Deployment unexpectedly stops working after a recent deploy. For example, if one of your DAGs worked in development but suddenly fails in a mission-critical production Deployment, you can roll back to your previous deploy to quickly get your pipeline running again. This allows you to troubleshoot the issue more thoroughly in development before redeploying to production. You can roll back to any deploy in the last three months regardless of your Runtime version, DAG code, or Deployment settings.

## Prerequisites

- Your Deployment must be on Astro Runtime 5 (Airflow 2.3) or later. Rolling back to any version before Astro Runtime 5 is not supported. 
- Your Deployment must be configured to use standard image and DAG-only deploys. Rollbacks are not supported for NFS deploys and Git sync deploys.
  
## Enable deploy rollbacks

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
- Your Astro Runtime version.
- Your Deployment's DAG deploy setting.