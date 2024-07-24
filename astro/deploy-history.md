---
sidebar_label: 'Deploy history and rollbacks'
title: 'Roll back to previous deploys using deploy histories'
id: deploy-history
description: View a historical record of code deploys to an Astro Deployment and roll back to specific deploys when something goes wrong.
---

import HostedBadge from '@site/src/components/HostedBadge';

<HostedBadge/>

The **Deploy History** tab in the Astro UI shows you a record of all code deploys to your Deployment. Use this page to track the development of a Deployment and to pinpoint when your team made key changes to code.

Astronomer stores the image and DAGs for all deploys made in the last 90 days. You can trigger a rollback to any of these deploys so that your Deployment starts running a previous version of your code.

Deploy rollbacks are an emergency option if a Deployment unexpectedly stops working after a recent deploy. For example, if one of your DAGs worked in development but suddenly fails in a mission-critical production Deployment, you can roll back to your previous deploy to quickly get your pipeline running again. This allows you to troubleshoot the issue more thoroughly in development before redeploying to production. You can roll back to any deploy in the last three months regardless of your Runtime version, DAG code, or Deployment settings.

![View of the Deploy History tab in the Astro UI, with one deploy entry](/img/docs/deploy-history.png)

## View deploy history

1. In the Astro UI, select a Deployment.
2. Click **Deploy History**

For each deploy, the **Deploy History** table shows the user who made the deploy, when they made the deploy, what image they used, the type of deploy, and any descriptions they added to the deploy.

### Types of deploys

There are different types of deploys, which are shared in the Deploy History table. You can read more about the different deploy options in [Deploy code to Astro](deploy-code.md). These deploy types include:

    - Image-only deploy
    - DAG-only deploy
    - GitHub deploy
    - (*Private Preview*) dbt project deploy

## Add a description to a deploy

Adding a description to a deploy is a helpful way to let other users know why you made a deploy and what the deploy contains. Descriptions appear in your deploy's entry in the **Deploy History** table.

To add a description to a deploy, specify the `--description` flag when you run `astro deploy`. For example:

```bash
astro deploy --description "Added a new 'monitor_weather' DAG"
```

:::tip

If you deploy to Astro through CI/CD, Astronomer recommends adding the Git commit ID or equivalent version ID as the description for your deploy. This serves as a reference if you need to roll back your Git repository when you roll back your Deployment.

:::

## Roll back to a past deploy

:::danger

Astronomer recommends triggering Deployment rollbacks only as a last resort for recent deploys that aren't working as expected. Deployment rollbacks can be disruptive, especially if you triggered multiple deploys between your current version and the rollback version. See [What happens during a deploy rollback](#what-happens-during-a-deploy-rollback) before you trigger a rollback to anticipate any unexpected effects.

:::

1. In the Astro UI, select a Deployment.
2. Click **Deploy History**.
3. Locate the deploy you want to roll back to. In the **Rollback to** column for the deploy, click **Deploy**.
4. Provide a description for your rollback, then complete the confirmation to trigger the rollback.

You can roll back to any deploy within the last three months. If your last deploy was more than three months ago, you can only roll back to that deploy. After the rollback completes, the **Deploy History** table shows your rollback deploy as the most recent deploy and includes both your rollback description and rollback deploy time. Your Docker image tag, DAG bundle name, and dbt bundles are the same as the previous version you rolled back to. The historic deploy that you rolled back to still appears in chronological order in the table.

For example, consider a user who, on November 8, 2023 at 13:00, rolled back to a deploy from November 6, 2023 at 14:00. At the top of the **Deploy History** table, an entry for the rollback deploy would have the following information:

- **Time**: **14:00 11/8/2023**
- **Docker image**: **deploy-2023-11-6T14-00** (Or the custom name of your historical image tag)
- **DAG bundle version**: **2023-11-16T14:00:00.0000000Z**
- **Deploy description**: Your rollback description.

### What happens during a deploy rollback

A deploy rollback is a new deploy of a previous version of your code. This means that the rollback deploy appears as a new deploy in **Deploy History**, and the records for any deploys between your current version and rollback version are still preserved. In Git terms, this is equivalent to `git revert`.

When you trigger a rollback, the following information is rolled back:

- All project code, including DAGs.
- Your Astro Runtime version.
- Your Deployment's DAG deploy setting.

The following information isn't rolled back:

- Your Deployment's resource configurations, such as executor and scheduler configurations.
- Your Deployment's environment variable values.
- Any other Deployment settings that you configure through the Astro UI, such as your Deployment name and description.
- For Runtime version downgrades, any data related to features that are not available in the rollback version are erased from the metadata database and not recoverable.

A rollback's effect on running tasks depends on whether the rollback downgrades your Deployment:

- If a rollback downgrades a Deployment to a previous version of Astro Runtime, all currently running tasks fail immediately. If a task has any remaining retries, those retries will run after the rollback is complete.
- If a rollback doesn't include a downgrade, any currently running tasks from before the rollback continue to run your latest code, while new Pods for downstream tasks run the code from the rollback version. This is identical behavior to pushing new code as described in [What happens during a code deploy](deploy-project-image.md#what-happens-during-a-project-deploy).
