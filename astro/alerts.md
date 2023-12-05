---
sidebar_label: 'Astro alerts'
title: 'Set up Astro alerts'
id: alerts
toc_main_heading_level: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Astro alerts provide an additional level of observability to Airflow's notification systems. You can configure an alert to notify you in Slack, PagerDuty, or through email when a DAG completes, if you have a DAG run failure, or if a task duration exceeds a specified time.

Unlike Airflow callbacks and SLAs, Astro alerts require no changes to DAG code. Follow this guide to set up your Slack, PagerDuty, or email to receive alerts from Astro and then configure your Deployment to send alerts.

:::info

To configure Airflow notifications, see [Airflow email notifications](airflow-email-notifications.md) and [Manage Airflow DAG notifications](https://docs.astronomer.io/learn/error-notifications-in-airflow).

:::

## Prerequisites

- An [Astro project](cli/develop-project.md).
- An [Astro Deployment](create-deployment.md). Your Deployment must run Astro Runtime 7.1.0 or later to configure Astro alerts, and it must also have [OpenLineage enabled](set-up-data-lineage.md#enabledisable-openlineage).
- A Slack workspace, PagerDuty service, or email address.

:::info

Astro alerts requires OpenLineage. By default, every Astro Deployment has OpenLineage enabled. If you disabled OpenLineage in your Deployment, you need to enable it to use Astro alerts. See [Enable/Disable OpenLineage](set-up-data-lineage.md#enabledisable-openlineage).

:::

<!-- Sensitive header used in product - do not change without a redirect-->

## Step 1: Configure your communication channel

<Tabs
    defaultValue="Slack"
    groupId= "step-1-configure-your-communication-channel"
    values={[
        {label: 'Slack', value: 'Slack'},
        {label: 'PagerDuty', value: 'PagerDuty'},
        {label: 'Email', value: 'Email'},
        {label: 'DAG Trigger', value: 'DAG'}
    ]}>
<TabItem value="Slack">

To set up alerts in Slack, you need to create a Slack app in your Slack workspace. After you've created your app, you can generate a webhook URL in Slack where Astro will send Astro alerts.

1. Go to [Slack API: Applications](https://api.slack.com/apps/new) to create a new app in your organization's Slack workspace.

2. Click **From scratch** when prompted to choose how you want to create your app.

3. Enter a name for your app, like `astro-alerts`, choose the Slack workspace where you want Astro to send your alerts, and then click **Create App**.

  :::info
  If you do not have permission to install apps into your Slack workspace, you can still create the app, but you will need to request that an administrator from your team completes the installation.
  :::

4. Select **Incoming webhooks**.

5. On the **Incoming webhooks** page, click the toggle to turn on **Activate Incoming Webhooks**. See [Sending messages using Incoming Webhooks](https://api.slack.com/messaging/webhooks).

6. In the **Webhook URLs for your Workspace** section, click **Add new Webhook to Workspace**.

  :::info

  If you do not have permission to install apps in your Slack workspace, click **Request to Add New Webhook** to send a request to your organization administrator.

  :::

7. Choose the channel where you want to send your Astro alerts and click **Allow**.

8. After your webhook is created, copy the webhook URL from the new entry in the **Webhook URLs for your Workspace** table.

</TabItem>
<TabItem value="PagerDuty">

To set up an alert integration with PagerDuty, you need access to your organization's PagerDuty Service. PagerDuty uses the [Events API v2](https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview#getting-started) to create a new integration that connects your Service with Astro.

1. Open your PagerDuty service and click the **Integrations** tab.

  ![Select PagerDuty integrations](/img/docs/pagerduty_alerts_integrations.png)

2. Click **Add an integration**.

3. Select **Events API v2** as the **Integration Type**.

4. On your **Integrations** page, open your new integration and enter an **Integration Name**.

5. Copy the **Integration Key** for your new Astro alert integration.

</TabItem>
<TabItem value="Email">

No external configuration is required for the email integration. Astronomer recommends allowlisting `astronomer.io` with your email provider to ensure that no alerts go to your spam folder. Alerts are sent from `no-reply@astronomer.io`.

</TabItem>
<TabItem value="DAG">

:::caution

This feature is in [Private Preview](https://docs.astronomer.io/astro/feature-previews). Please reach out to your customer success manager to enable this feature.

:::

The **DAG Trigger** communication channel works differently from other communication channel types. Instead of sending a pre-formatted alert message, Astro makes a generic request through the Airflow REST API to trigger a DAG on Astro. You can configure the triggered DAG to complete any action, such as sending a message to your own incident management system or writing data about an incident to a table.

1. Create a DAG that you want to run when the alert is triggered. For example, you can use the following DAG to run arbitrary Python code when the alert is triggered:

  ```python
  import datetime
  from typing import Any

  from airflow import DAG
  from airflow.operators.python import PythonOperator
  
  with DAG(
      dag_id="register_incident",
      start_date=datetime.datetime(2023, 1, 1),
      schedule=None,
  ):
  
      def _register_incident(params: dict[str, Any]):
          # Here you can run arbitrary Python code. Example DAG run conf payload:
          # {
          #     "dagName": "fail_dag",
          #     "alertType": "PIPELINE_FAILURE",
          #     "alertId": "d75e7517-88cc-4bab-b40f-660dd79df216",
          #     "message": "[Astro Alerts] Pipeline failure detected on DAG fail_dag. \\nStart time: 2023-11-17 17:32:54 UTC. \\nFailed at: 2023-11-17 17:40:10 UTC. \\nAlert notification time: 2023-11-17 17:40:10 UTC. \\nClick link to investigate in Astro UI: https://cloud.astronomer.io/clkya6zgv000401k8zafabcde/dags/clncyz42l6957401bvfuxn8zyxw/fail_dag/c6fbe201-a3f1-39ad-9c5c-817cbf99d123?utm_source=alert\"\\n"
          # }
  
          # Example:
          failed_dag = params["dagName"]
          print(f"Register an incident in my system for DAG {failed_dag}.")
  
      PythonOperator(task_id="register_incident", python_callable=_register_incident)

  ```

2. Deploy the DAG to any Deployment in the Workspace where you want to create the alert. The DAG that triggers the alert and the DAG that the alert runs can be in different Deployments, but they must be deployed in the same Workspace.
3. Create a [Deployment API token](deployment-api-tokens.md) for the Deployment where you deployed the DAG that the alert will run. Copy the token to use in the next step.

</TabItem>
</Tabs>

## Step 2: Create your Workspace alert in the Cloud UI

In the Cloud UI, you can enable alerts from the **Workspace Settings** page.

1. In the Cloud UI, click **Alerts**.

2. Click **Add Alert**.

3. Enter your **Alert Name** and choose the alert type, **DAG Success**, **DAG Failure**, or **Task Duration**.

  :::info

  You can only use Task Duration alerts with individual tasks. Alerting on task group duration is not supported.

  :::

4. Choose the **Communication Channels** where you want to send your alert.

5. Add your communication channel information.

    <Tabs
        defaultValue="Slack"
        groupId= "step-1-configure-your-communication-channel"
        values={[
            {label: 'Slack', value: 'Slack'},
            {label: 'PagerDuty', value: 'PagerDuty'},
            {label: 'Email', value: 'Email'},
            {label: 'DAG Trigger', value: 'DAG'}
        ]}>
    <TabItem value="Slack">

    Paste the Webhook URL from your Slack workspace app. If you need to find a URL for an app you've already created, go to your [Slack Apps](https://api.slack.com/apps) page, select your app, and then choose the **Incoming Webhooks** page.

    ![Add your Slack Webhook URL](/img/docs/astro_alerts_slack.png)

    </TabItem>
    <TabItem value="PagerDuty">

    Paste the Integration Key from your PagerDuty Integration and select the **Severity** of the alert.

    ![Paste the Integration Key](/img/docs/astro_alerts_pagerduty.png)

    </TabItem>
    <TabItem value="Email">

    Enter the email addresses that should receive the alert.

    ![Add an email address](/img/docs/astro_alerts_email.png)

    </TabItem>
    <TabItem value="DAG">

    Select the Deployment where your DAG is deployed, then select the DAG. Enter the Deployment API token that you created in Step 1.

    ![Add an email address](/img/docs/astro_alerts_dag.png)

    </TabItem>
    </Tabs>

6. Add DAGs or tasks that your alert applies to.

    - **DAG failure**: Click **DAG** to choose the Deployment and the DAG that you want to send an alert about if it fails.

    - **DAG success**: Click **DAG** and choose the Deployment and the DAG that you want to send an alert about when it completes.

    - **Task duration**: Click **Task** and choose the Deployment, DAG, and task name. Enter the **Duration** for how long a task should take to run before you send an alert to your communication channels.

     You can add more DAGs or tasks after you create your alert.

7. Click **Create alert**.

## Step 3: (Optional) Test your DAG failure alert

Astro alerts work whether your DAG run is manual or scheduled, so you can test your configured Astro alerts by failing your DAG manually.

1. In the Cloud UI, click **DAGs**.

2. Choose the DAG that has your alert configured.

3. Trigger a DAG run.

4. Select **Mark as** and choose **Failed** to trigger an alert for a DAG failure.

  ![Manually marking a successful DAG run as Failed.](/img/docs/astro_alerts_manual_fail.png)

5. Check your Slack, PagerDuty, or Email alerts for your DAG failure alert. The alert includes information about the DAG, Workspace, Deployment, and data lineage associated with the failure as well as direct links to the Cloud UI.

    ![Example of a Slack test alert.](/img/docs/slack_alerts_example.png)

