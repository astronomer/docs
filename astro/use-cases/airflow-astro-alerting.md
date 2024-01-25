---
title: 'Set up alerting for your pipelines on Astro'
sidebar_label: 'Airflow and Astro alerting'
id: airflow-astro-alerting
---

When orchestrating data pipelines, it's key that you know when something goes wrong, whether that's a business critical pipeline failing or a DAG that provides data for another team taking longer than normal to complete. A common consideration when running Airflow at scale is how your team will be alerted when different scenarios occur with your DAGs.

Airflow has built-in notification mechanisms that can be leveraged to configure alerts for common use cases. However, there are some key limitations. For the cases where Airflow notifications aren't sufficient, [Astro alerts](alerts.md) provide an additional level of observability.

When you combine Airflow notifications with Astro alerts, you can:

- Easily configure DAG failure or success alerts for common communication channels like Slack, PagerDuty, or email with Astro alerts.
- Leverage Airflow email notifications and callbacks for custom task-level alerting logic.
- Implement pipeline SLAs based on task duration or absolute time with Astro alerts.

## Recommended alerts

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


For more detailed recommendations for when to use which type of alert, see the [Explanation](#explanation) section.


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

Using a combination of Astro alerts and Airflow notifications allows your team to easily implement alerting logic for any scenario. You may need different types of alerts that are better suited towards one option or the other, as shown in the example in this use case:

- Task-level alerts with custom logic, or example if you want to be notified of success or failure only for a specific task, or want to run custom code if a task succeeds or fails, are straightforward to implement in Airflow, but are not currently supported with Astro alerts.
- DAG-level success or failure alerts can be accomplished using either Airflow notifications or Astro alerts, but on Astro they are easy to configure and do not require any code changes. To implement these alerts with Airflow, you would need to update your DAG code and possibly complete more configuration for your communication channel (e.g. setting up an SMTP server for email alerts).
- Absolute time alerts are straightforward to implement with Astro alerts, but are not currently supported in Airflow.

In some cases, whether you set up an alert on Astro or in Airflow will be dependent on how your DAGs were configured before you moved to Astro. For example, if all of your DAGs have email on failure notifications configured already, it will likely be easier for you to configure an SMTP server on Astro and rely on the existing notification rather than implementing a new Astro alert for each DAG. On the other hand, if you are developing new DAGs on Astro, it will likely be easier to implement Astro alerts so you can see everything in one place.

:::note

Programmatically creating Astro alerts, which may be helpful if you have a high number of DAGs, is coming soon.

:::

In other cases, Astro alerts are clearly the better option. If you need to implement SLAs for your pipelines so you know as soon as a task is taking too long or a DAG hasn't completed on time, you should use the absolute time or task duration Astro alerts. There are a couple of reasons these are preferable to Airflow SLAs:

- The Astro alert for task duration is relevant to the task start time, making it easy to understand and implement for your use case. Airflow SLAs often cause confusion because they are relevant to the DAG execution date, not the task start time.
- The Astro alert for absolute time allows you to implement alerts based on a specific time of day your DAG should complete. This type of SLA is not available in Airflow.
- Astro alerts are sent as soon as the task duration is exceeded or absolute time has passed. Missed Airflow SLAs will not be reported until the task has finished running, meaning your notification could be significantly delayed.

## See also

- [Set up Astro alerts](alerts.md)
- [Manage Airflow DAG notifications](error-notifications-in-airflow.md)
