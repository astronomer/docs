---
title: 'When to use Airflow or Astro alerts for your pipelines on Astro'
sidebar_label: 'Choosing Airflow or Astro alerts'
id: airflow-vs-astro-alerts
---

When orchestrating data pipelines, it's key that you know when something goes wrong. It could be that a business critical DAG failed or that a DAG that provides data for another team took longer than normal to complete. A common consideration when running [Apache Airflow®](https://airflow.apache.org/) at scale is how to alert your team in different scenarios.

Airflow has built-in notification mechanisms for common use cases, but they have some limitations. For the cases where Airflow notifications aren't sufficient, [Astro alerts](https://www.astronomer.io/docs/astro/alerts) provide an additional level of observability. For many use cases, Astronomer recommends using a combination of Airflow and Astro alerts to best cover all alerting scenarios.

When you combine Airflow notifications with Astro alerts, you can:

- Use Astro alerts to configure DAG failure or success alerts for common communication channels like Slack, PagerDuty, or email.
- Use Astro alerts to implement pipeline SLAs based on task duration or absolute time.
- Use Airflow email notifications and callbacks for custom task-level alerting logic.

This guide provides guidance on when to use Astro or Airflow alerts, as well as an example implementation covering a couple of common alerting scenarios.

## Feature overview

This guide highlights when to use the following Astro and Airflow features to create different types of alerts for your pipelines:

- [Astro alerts](https://www.astronomer.io/docs/astro/alerts) for configuring DAG SLAs and failure notifications.
- [Airflow callbacks](https://www.astronomer.io/docs/learn/error-notifications-in-airflow#airflow-callbacks) for custom task-level alerts. 

## Best practice guidance

Using a combination of Astro alerts and Airflow notifications allows your team to implement alerting logic using the best tool for each scenario. You might need different types of alerts that are better suited towards one option or the other, for example:

- **Task-level alerts with custom logic** are recommended if you want be notified of success or failure only for a specific task, or you want to run custom code if a task succeeds or fails. Task-level success or failure alerts or alerts with custom logic are not currently supported with Astro alerts, but they're straightforward to implement in Airflow.
- **DAG-level success or failure alerts** can be created using either Airflow notifications or Astro alerts, but on Astro they are easy to configure and don't require any code changes. To implement these alerts with Airflow, you need to update your DAG code and complete additional configuration for your communication channel (for example, setting up an SMTP server for email alerts).
- **Absolute time alerts** are recommended when you need your DAG to complete by a certain time of day. These types of alerts are available only on Astro.
- **Task duration alerts** are recommended when you need to know if your task has taken longer than a certain amount of time to complete. These types of alerts are easy to implement with Astro alerts, but are unintuitive in Airflow.

In some cases, whether you set up an alert on Astro or in Airflow will depend on how your DAGs were configured before you moved to Astro. For example, if all of your DAGs already have email-on-failure notifications configured, it will likely be easier for you to configure an SMTP server on Astro and rely on the existing notification than implement a new Astro alert for each DAG. On the other hand, if you are developing new DAGs on Astro, it will likely be easier to implement Astro alerts which require less configuration for the communication channels.

:::info

Programmatically creating Astro alerts is coming soon. This will make it easy to configure alerts for a large number of DAGs without  having to create each alert manually.

:::

In other cases, Astro alerts are always the better option. If you need to implement SLAs for your pipelines so you immediately know when a DAG task is taking too long to run, you should use the absolute time or task duration Astro alerts. There are a couple of reasons these are preferable to Airflow SLAs:

- The Astro alert for task duration is relevant to the task start time, making it easy to understand and implement for your use case. Airflow SLAs often cause confusion because they are relevant to the DAG execution date, not the task start time.
- The Astro alert for absolute time allows you to implement alerts based on a specific time of day your DAG should complete. This type of SLA is not available in Airflow.
- Astro alerts allow you to easily choose between multiple common communication channels. With Airflow SLAs, if you want your notification sent somewhere other than your email, you have to write your own custom callback logic. Additionally, if you have an SMTP service configured in your Airflow environment you will get email notifications for SLA misses; there is no way to turn this behavior off.

### Recommended alerts

Astronomer recommends choosing the following alerts for these common scenarios:

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

For more information on different types of alerts, check out the documentation linked in [See also](#see-also).

## Example

This example shows how to implement a combination of Airflow and Astro alerts to cover notifications for common scenarios including DAG failures, specific task failures, and pipeline SLAs.

### Prerequisites

To implement the alerts shown in this example, you need:

- At least one [Astro Deployment](https://www.astronomer.io/docs/astro/create-deployment). Your Deployment must run Astro Runtime 7.1.0 or later and it must have OpenLineage enabled.
- An [Astro project](https://www.astronomer.io/docs/astro/cli/develop-project) with at least one DAG. Your DAG should have at least two tasks.

However, you can extend this example to encompass any number of Astro Deployments and DAGs.

### Implementation

To implement this use case:

1. Open the DAG in your Astro project and configure a pre-built SlackNotifier for one of its tasks as a task-level argument. See [Example pre-built notifier: Slack](https://www.astronomer.io/docs/learn/error-notifications-in-airflow#example-pre-built-notifier-slack) for sample code.  
2. Deploy your project to your Astro Deployment. See [Deploy code to Astro](https://www.astronomer.io/docs/astro/deploy-code).
3. Add a connection to Slack in the Astro UI. See [Create Airflow connections in the Astro UI](create-and-link-connections.md). This connection will be used by your SlackNotifier, so make sure the connection ID matches what you used in your DAG code in Step 1.
4. In your Astro Deployment, configure an Astro **DAG failure** alert for your DAG using the communication channel of your choice. See [Set up Astro alerts](https://www.astronomer.io/docs/astro/alerts).
5. Configure an Astro **Absolute time** alert for your DAG based on the amount of time you expect your DAG to complete in. Use the communication channel of your choice. See [Set up Astro alerts](https://www.astronomer.io/docs/astro/alerts).

## See also

- [Set up Astro alerts](https://www.astronomer.io/docs/astro/alerts)
- [Manage Airflow DAG notifications](https://www.astronomer.io/docs/learn/error-notifications-in-airflow)
- [Airflow timeouts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#timeouts)
