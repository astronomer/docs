---
sidebar_label: 'View deploy history'
title: 'View the deploy history for an Astro Deployment'
id: deploy-history
description: See a historical record of code deploys to an Astro Deployment.
---

The **Deploy History** tab in the Cloud UI shows you a record of all code deploys to your Deployment. Use this page to track deploys across multiple contributors and pinpoint when a specific change was made.

![View of the Deploy History tab in the Cloud UI, with one deploy entry](/img/docs/deploy-history.png)

## View deploy history

1. In the Cloud UI, select a Deployment.
2. Click **Deploy History**

For each deploy, the **Deploy History** table shows the user that made the deploy, when they made the deploy, what image they used, and any descriptions they added to the deploy. 

## Add a description to a deploy

Adding a description to a deploy is a helpful way to let other users know why you made a deploy and what the deploy contains. Descriptions appear in your deploy's entry in the **Deploy History** table.

To add a description to a deploy, specify the `--description` flag when you run `astro deploy`. For example:

```bash
astro deploy --description "Added a new 'monitor_weather' DAG"
```
