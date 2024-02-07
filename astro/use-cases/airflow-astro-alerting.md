---
title: 'Set up a multi-channel alerting system for your Airflow pipelines on Astro'
sidebar_label: 'Multi-channel alerting systems'
id: multi-channel-alerting-systems
---

When orchestrating data pipelines, it's key that you know when something goes wrong, whether that's a business critical pipeline failing or a DAG that provides data for another team taking longer than normal to complete. A common consideration when running Airflow at scale is how to alert your team in different scenarios.

Airflow has built-in notification mechanisms for common use cases, but they have some limitations. For the cases where Airflow notifications aren't sufficient, [Astro alerts](https://docs.astronomer.io/astro/alerts) provide an additional level of observability.

When you combine Airflow notifications with Astro alerts, you can:

- Use Astro alerts to configure DAG failure or success alerts for common communication channels like Slack, PagerDuty, or email.
- Use Astro alerts to implement pipeline SLAs based on task duration.
- Use Airflow email notifications and callbacks for custom task-level alerting logic.

This use case shows how to combine Airflow and Astro alerts for a couple of common scenarios. For general guidance on when to use which type of alert, see the [Explanation](#explanation) section.

## Feature overview

This use case depends on the following Astro and Airflow features to create different types of alerts for your pipelines:

- [Astro alerts](https://docs.astronomer.io/astro/alerts) for configuring DAG SLAs and failure notifications.
- [Airflow callbacks](https://docs.astronomer.io/learn/error-notifications-in-airflow#airflow-callbacks) for custom task-level alerts. 

## Prerequisites

This use case assumes you have:

- At least one [Astro Deployment](https://docs.astronomer.io/astro/create-deployment). Your deployment must run Astro Runtime 7.1.0 or later and it must have OpenLineage enabled.
- An [Astro project](https://docs.astronomer.io/astro/cli/develop-project) with at least one DAG. Your DAG should have at least two tasks.

However, you can extend this use case to encompass any number of Astro Deployments and DAGs.

## Implementation

To implement this use case:

1. Open the DAG in your Astro project and configure a pre-built SlackNotifier for one of its tasks as a task-level argument. See [Example pre-built notifier: Slack](https://docs.astronomer.io/learn/error-notifications-in-airflow#example-pre-built-notifier-slack) for sample code.  
2. Deploy your project to your Astro Deployment. See [Deploy code to Astro](https://docs.astronomer.io/astro/deploy-code).
3. Add a connection to Slack in the Astro Cloud UI. See [Create Airflow connections in the Cloud UI](create-and-link-connections.md). This connection will be used by your SlackNotifier, so make sure the connection ID matches what you used in your DAG code in Step 1.
4. In your Astro Deployment, configure an Astro **DAG failure** alert for your DAG using the communication channel of your choice. See [Set up Astro alerts](https://docs.astronomer.io/astro/alerts).
5. Configure an Astro **Absolute time** alert for your DAG based on the amount of time you expect your DAG to complete in. Use the communication channel of your choice. See [Set up Astro alerts](https://docs.astronomer.io/astro/alerts).

## Explanation

Using a combination of Astro alerts and Airflow notifications allows your team to implement alerting logic using the best tool for each scenario. You might need different types of alerts that are better suited towards one option or the other, as shown in the example in this use case:

- **Task-level alerts with custom logic** are recommended if you want be notified of success or failure only for a specific task, or you want to run custom code if a task succeeds or fails. Task-level success or failure alerts or alerts with custom logic are not currently supported with Astro alerts, but they're straightforward to implement in Airflow
- DAG-level success or failure alerts can be created using either Airflow notifications or Astro alerts, but on Astro they are easy to configure and don't require any code changes. To implement these alerts with Airflow, you need to update your DAG code and complete additional configuration for your communication channel (for example, setting up an SMTP server for email alerts).
- Absolute time alerts are recommended when you need your DAG to complete by a certain time of day. These types of alerts are available only on Astro.

In some cases, whether you set up an alert on Astro or in Airflow will depend on how your DAGs were configured before you moved to Astro. For example, if all of your DAGs already have email-on-failure notifications configured, it will likely be easier for you to configure an SMTP server on Astro and rely on the existing notification than implement a new Astro alert for each DAG. On the other hand, if you are developing new DAGs on Astro, it will likely be easier to implement Astro alerts which require less configuration for the communication channels.

:::info

Programmatically creating Astro alerts, which may be helpful if you have a large number of DAGs, is coming soon.

:::

In other cases, Astro alerts are always the better option. If you need to implement SLAs for your pipelines so you immediately know when a DAG task is taking too long to run, you should use the absolute time or task duration Astro alerts. There are a couple of reasons these are preferable to Airflow SLAs:

- The Astro alert for task duration is relevant to the task start time, making it easy to understand and implement for your use case. Airflow SLAs often cause confusion because they are relevant to the DAG execution date, not the task start time.
- The Astro alert for absolute time allows you to implement alerts based on a specific time of day your DAG should complete. This type of SLA is not available in Airflow.
- Astro alerts allow you to easily choose between multiple common communication channels. With Airflow SLAs, if you want your notification sent somewhere other than your email, you have to write your own custom callback logic. Additionally, if you have an SMTP service configured in your Airflow environment you will get email notifications for SLA misses; there is no way to turn this behavior off.

### Recommended alerts

Generally, Astronomer recommends choosing the following alerts for these common scenarios:

| Scenario                                   | Astro alert | Airflow email notification | Airflow callback | Airflow SLA | Airflow timeout |
|--------------------------------------------|-------------|-----------------------------|------------------|--------------|------------------|
| Email on DAG success or retry               | X           | X                           |                  |              |                  |
| Email on specific task success or retry     |             | X                           |                  |              |                  |
| Custom DAG-level alerting logic             |             |                             | X                |              |                  |
| Custom task-level alerting logic            |             |                             | X                |              |                  |
| Absolute time DAG SLA                       | X           |                             |                  |              |                  |
| Task duration SLA                           | X           |                             |                  |              |                  |
| Stop a running task after some amount of time|           |                             |                  |              | X                |
| Trigger another DAG based on an alert       | X           |                             |                  |              |                  |


## See also

- [Set up Astro alerts](https://docs.astronomer.io/astro/alerts)
- [Manage Airflow DAG notifications](https://docs.astronomer.io/learn/error-notifications-in-airflow)
