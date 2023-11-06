---
sidebar_label: 'Deploy history and rollbacks'
title: 'Roll back to previous deploys using deploy histories'
id: deploy-history
description: View a historical record of code deploys to an Astro Deployment and roll back to specific deploys when something goes wrong.
---

The **Deploy History** tab in the Cloud UI shows you a record of all code deploys to your Deployment. Use this page to track the development of a Deployment and to pinpoint when your team made key changes to code.

In addition to maintaining a history of all deploys, Astronomer stores the image and DAGs for all deploys made in the last three months. You can trigger a rollback to any of these deploys so that your Deployment starts running a previous version of your code. 

Deploy rollbacks are an emergency option if a Deployment unexpectedly stops working after a recent deploy. For example, if one of your DAGs worked in development but suddenly fails in a mission-critical production Deployment, you can roll back to your previous deploy to quickly get your pipeline running again. You can then troubleshoot the issue more thoroughly in development before redeploying to production. You can roll back to any deploy in the last three months regardless of your Runtime version, DAG code, or Deployment settings.

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

:::tip

If you deploy to Astro through CI/CD, Astronomer recommends adding the Git commit ID as the description for your deploy. This serves as a reference if you roll back your Deployment and also need to roll back your Git repository.

:::

## Roll back to a past deploy

:::warning

Astronomer recommends triggering Deployment rollbacks only as a last result for recent deploys which aren't working as expected. Deployment rollbacks can be destructive, especially if you triggered multiple deploys between your current version and the rollback version. See [What happens during a deploy rollback](#what-happens-during-a-deploy-rollback) before you trigger a rollback to anticipate any unexpected effects.

:::

1. In the Cloud UI, select a Deployment.
2. Click **Deploy History**.
3. Locate the deploy you want to roll back to. In the **Rollback to** column for the deploy, click **Deploy***. 
4. Provide a description for your rollback, then complete the confirmation to trigger the rollback.

After the deploy completes, the **Deploy History** table shows your rollback deploy at the top of the table as the most recent deploy and includes your rollback description and rollback deploy time. Your Docker image tag and DAG bundle names are the same as the previous version you rolled back to. The historic deploy that you rolled back to still appears in chronological order in the table. 

For example, consider a user who, on November 8, 2023 at 13:00, rolled back to a deploy from November 6, 2023 at 14:00:

- At the top of the **Deploy History** table, an entry for the rollback deploy would have the following information:
    - **Time**: **14:00 11/8/2023**
    - **Docker image**: **deploy-2023-11-6T14-00**
    - **DAG bundle version**: **2023-11-16T14:00:00.0000000Z**
    - **Deploy description**: Your rollback description.

## What happens during a deploy rollback

A deploy rollback is technically a new deploy of a previous version of your code. This means that the rollback deploy appears as a new deploy in **Deploy History**, and the records for any deploys between your current version and rollback version are still preserved. In Git terms, this is the equivalent of `git revert`.

When you trigger a roll back, the following information is rolled back:
- All project code, including DAGs.
- Your Astro Runtime version.
- Your Deployment's DAG deploy setting.

The following information isn't rolled back:

- Your Deployment's resource configurations, such as executor and scheduler configurations.
- Your Deployment's environment variable values.
- Any other Deployment settings that you configure through the Cloud UI, such as your Deployment name and description. 
- For Runtime version downgrades, any data related to features which are not available in the rollback version are erased from the metadata database and not recoverable.

After you trigger a rollback, any currently running tasks from before the rollback continue to run your latest code, while new Pods for downstream tasks run the code from the rollback version. This is identical behavior to pushing new code as described in [What happens during a code deploy](deploy-project-image.md#what-happens-during-a-project-deploy).