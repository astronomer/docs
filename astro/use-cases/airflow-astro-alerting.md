---
title: 'Set up alerting for your pipelines on Astro'
sidebar_label: 'Airflow and Astro alerting'
id: airflow-astro-alerting
---

When orchestrating data pipelines, it's key that you know when something goes wrong, whether that's a business critical pipeline failing or a DAG that provides data for another team team taking longer than normal to complete. A common consideration when running Airflow at scale is how your team will be alerted when different scenarios with your DAGs occur.

Airflow has built-in notification mechanisms that can be leveraged to configure alerts for common use cases. However, there are some key limitations. For the cases where Airflow notifications aren't sufficient, [Astro alerts](alerts.md) provide an additional level of observability.

When you combine Airflow notifications with Astro alerts, you can:

- Easily configure DAG failure or success alerts for common systems like Slack, PagerDuty, or email with Astro alerts.
- Leverage Airflow email notifications and callbacks for custom task-level alerting logic.
- Implement pipeline SLAs based on task duration or absolute time with Astro alerts.

For general recommendations on when to use which type of alert, see the [Explanation](#explanation) section.


## Feature overview

This use case depends on the following Astro and Airflow features to create different types of alerts for your pipelines:

- Configuring DAG SLAs and failure notifications using [Astro alerts](alerts.md).
- Implementing [Airflow callbacks](error-notifications-in-airflow.md) for custom task-level alerts. 

## Prerequisites

This use case assumes you have:

- At least one [Astro Deployment](create-deployment). Your deployment must run Astro Runtime 7.1.0 or later.
- An [Astro project](develop-project.md) with at least one DAG. Your DAG should have at least two tasks.

However, you can extend this use case to encompass any number of Astro Deployments and DAGs.

## Implementation

To implement this use case:

1. In the DAG in your Astro project, add an `on_success_callback` that uses the pre-built SlackNotifier to one task (not the DAG's `default_args`). See [Example pre-built notifier: Slack](error-notifications-in-airflow.md#example-pre-built-notifier-slack).  
2. Deploy your project to your Astro Airflow deployment. See [Deploy code to Astro](deploy-code.md).
3. Add a connection to Slack in the Astro Cloud UI. See [Create Airflow connections in the Cloud UI](create-and-link-connections.md). This connection will be used by your SlackNotifier. Make sure the connection ID matches what you used in your DAG code in Step 1.
4. Configure an Astro DAG failure alert for your DAG using the communication channel of your choice. See [Set up Astro alerts](alerts.md).
5. Configure an Astro absolute time alert for your DAG based on the amount of time you expect your DAG to complete in. Use the communication channel of your choice. See [Set up Astro alerts](alerts.md).

## Explanation

Using a combination of Astro alerts and Airflow notifications allows your team to easily implement alerting logic for any scenario. 

Generally, Astronomer recommends choosing the following alerts for these common scenarios:

table

## See also

- [Set up Astro alerts](alerts.md)
- [Manage Airflow DAG notifications](error-notifications-in-airflow.md)
