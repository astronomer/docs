---
sidebar_label: 'DAG alerts'
title: 'Set up Astro DAG alerts'
id: dag-alerts
toc_main_heading_level: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Astro DAG alerts provide an additional level of observability to Airflow's notification systems. You can configure a DAG alert to notify you in Slack or PagerDuty if you have a DAG run failure or if a task duration exceeds a specified time. 

Unlike Airflow callbacks and SLAs, Astro DAG alerts require no changes to DAG code and are designed to integrate with Slack and PagerDuty. Follow this guide to set up your Slack or PagerDuty to receive alerts from Astro and then configure your Deployment to send alerts.

To configure Airflow notifications, see [Airflow email notifications](airflow-email-notifications.md) and [Manage Airflow DAG notifications](error-notifications-in-airflow.md)

## Prerequisites

- An [Astro project](develop-project.md).
- An [Astro Deployment](create-deployment.md). Your Deployment must run Astro Runtime 7.1.0 or later to configure DAG alerts.
- A Slack workspace and/or PagerDuty service.

## Step 1: Configure your communication channel

<Tabs
    defaultValue="Slack"
    groupId= "step-1-configure-your-communication-channel"
    values={[
        {label: 'Slack', value: 'Slack'},
        {label: 'PagerDuty', value: 'PagerDuty'}
    ]}>
<TabItem value="Slack">

To set up alerts in Slack, you need to create a Slack app in your Slack workspace. After you've created your app, you can generate a webhook URL in Slack where Astro will send DAG alerts. 

1. Go to [Slack API: Applications](https://api.slack.com/apps/new) to create a new app in your organization's Slack workspace.

2. Click **From scratch** when prompted to choose how you want to create your app.

3. Enter a name for your app, like `astro-alerts`, choose the Slack workspace where you want Astro to send your alerts, and then click **Create App**.

  :::info
  If you do not have permission to install apps into your Slack workspace, you can still create the app, but you will need to request that an administrator from your team completes the installation.
  :::

4. Select **Incoming webhooks**.

5. On the **Incoming webhooks** page, click to turn on **Activate Incoming Webhooks**.

6. In the **Webhook URLs for your Workspace** section, click **Add new Webhook to Workspace**. 

  :::info

  If you do not have permission to install apps in your Slack workspace, click **Request to Add New Webhook** to send a request to your organization administrator.
  
  :::

7. Choose the channel where you want to send your Astro alerts and click **Allow**.

8. After your webhook is created, copy the webhook URL from the new entry in the **Webhook URLs for your Workspace** table.

</TabItem>
<TabItem value="PagerDuty">

To set up an alert integration with PagerDuty, you need access to your organization's PagerDuty Service. PagerDuty uses the [Events API v2](https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview#getting-started) to create a new integration that connects your Service with Astro.

1. Open your PagerDuty service.

2. On the **Integrations** tab, click **Add an integration**.

3. Select **Events API v2** as the **Integration Type**.

4. On your **Integrations** page, open your new integration and enter an **Integration Name**.

5. Copy the **Integration Key** for your new Astro alert integration.

</TabItem>
</Tabs>

## Step 2: Create your workspace alert in the Cloud UI

In the Cloud UI, you can enable alerts from the **Workspace Settings** page. 


1. In the Cloud UI, select the Astro workspace you want to create an alert for.

2. Click **Workspace Settings**, then click **Alerts**.

3. Click **Add Alert**. 

4. Enter your **Alert Name** and choose the alert type, either **Pipeline Failure** or **Task Duration**. 

5. Choose the **Communication Channel** where you want to send your alert. You can choose to send alerts to both Slack and PagerDuty.

6. Add your communication channel information.

    <Tabs>
    <TabItem value="Slack">
    
    Paste the Webhook URL from your Slack workspace app. If you need to find a URL for an app you've already created, go to your [Slack Apps](https://api.slack.com/apps) page, select your app, and then choose the **Incoming Webhooks** page. 
    
    </TabItem>
    <TabItem value="PagerDuty">

    Paste the Integration Key from your PagerDuty Integration and select the **Severity** of the alert.
    
    </TabItem>
    </Tabs>

7. Add DAG or Tasks to your alert.

     - **Pipeline failure**: Click **Pipeline** to choose the DAG that you want to send an alert about if it fails.
    
    - **Task duration**: Click **Task** and choose the Deployment, DAG, and task name. Enter the **Duration** for how long a task should take to run before you send an alert to your communication channels.

     You can add more DAGs or tasks after you create your alert. 

8. Click **Create alert**.