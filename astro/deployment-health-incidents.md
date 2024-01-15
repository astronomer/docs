---
sidebar_label: 'Deployment health and incidents'
title: 'View and address Deployment incidents'
id: deployment-health-incidents
description: A list of all possible Deployment incident types and steps for resolving each one.
---

:::caution

This feature is in [Private preview](feature-previews.md).

:::

Astro monitors your Deployment and notifies you when specific conditions or metrics are met to ensure that you're up to date on your Deployment's performance. Use your Deployment health status to quickly check if your Deployment has any issues that need immediate attention.

## Deployment health

After you create a Deployment, its real-time health status appears at the top of the Deployment information page. Deployment health indicates if the components within your Deployment are running as expected.

![Deployment Health status](/img/docs/deployment-health.png)

The following are the possible health statuses your Deployments can have:

- **Creating** (Grey): Astro is still provisioning Deployment resources. It is not yet available to run DAGs. See [Create a Deployment](create-deployment.md).
- **Deploying** (Grey): A code deploy is in progress. Hover over the status indicator to view specific information about the deploy, including whether it was an image deploy or a DAG-only deploy.
- **Healthy** (Green): The Airflow webserver and scheduler are both healthy and running as expected.
- **Unhealthy** (Red): Your Deployment webserver or scheduler are restarting or otherwise not in a healthy, running state.
- **Unknown** (Grey): The Deployment status can't be determined.

Your Deployment health status will show a number next to the status if a [Deployment incident](#deployment-incidents) occurred since you last viewed it.

If your Deployment is unhealthy or the status can't be determined, check the status of your tasks and wait for a few minutes. If your Deployment is unhealthy for more than five minutes, review the logs in the [Airflow component logs](view-logs.md#view-airflow-component-logs-in-the-cloud-ui) in the Cloud UI or contact [Astronomer support](https://cloud.astronomer.io/open-support-request).

## Deployment incidents

Astro automatically monitors your Deployments and sends messages when your Deployment isn't running optimally or as expected. These messages are known as _Deployment incidents_.

The following table contains all types of Deployment incidents. Use each of the linked topics to resolve any incidents that occur in your own Deployments. 

| Incident name                           | Description                                                                                        |
| --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Tasks Stuck in Queued                   | There are tasks that have been in a queued state for over 20 minutes.                              |
| Scheduler Heartbeat Not Found           | The Airflow scheduler has not sent a heartbeat for longer than expected.                           |
| Airflow Database Storage Unusually High | The metadata database has tables that are larger than expected.                                    |
| Worker Queue at Capacity                | At least one worker queue in this Deployment is running the maximum number of tasks and workers.   |
| Monitoring Failure                      | Astro failed to monitor the Deployment.                                                            |
| Job Scheduling Disabled                 | The Airflow scheduler is currently disabled and will not automatically schedule new tasks.         |
| Airflow Component Unhealthy             | At least one Airflow component has been unable to start successfully.                              |
| Worker Queue Does Not Exist             | There is at least 1 task instance that is configured to run on a worker queue that does not exist. |

Use the following topics to address each of these incidents.

### Tasks Stuck in Queued

There are tasks stuck in queued which are waiting to be assigned to a worker. This can happen when workers aren't properly scaling or are experiencing issues. 

This type of incident requires no initial user action. Instead, Astronomer Support receives a notification, and you will receive an email from Astronomer Support if this issue can't be resolved. Ensure that you [configured a Deployment contact email](deployment-settings.md#configure-deployment-contact-emails) so that you can be notified if this issue requires additional follow-ups.

### Scheduler Heartbeat Not Found 

This could be a sign that the scheduler is down. Tasks will keep running, but new tasks will not be scheduled. 

If you receive this incident notification, Astronomer Support has already been notified and no action is required from you. Ensure that you [configured a Deployment contact email](deployment-settings.md#configure-deployment-contact-emails) so that you can be notified if this issue requires additional follow-ups.

### Airflow Database Storage Unusually High

Your Deployment metadata database is currently storing tables that are larger than the recommended size for tables. This is typically caused due to XCom data and can result in your metadata database running out of storage.

The following are a few ways to reduce the amount of XCom data in the metadata database:

- Configure an external backend for XCom data, such as AWS S3. See the [Astronomer XCom Backend Tutorial](https://docs.astronomer.io/learn/xcom-backend-tutorial).
- Implement intermediary data storage for tasks so that Airflow doesn't store large amounts of data when passing data between tasks. See [Astronomer documentation].

If you receive this incident notification and don't utilize XComs, submit a request to [Astronomer Support](https://cloud.astronomer.io/open-support-request).

### Worker Queue at Capacity

At least one worker queue in your Deployment is running the maximum possible number of tasks and workers. Tasks will continue to run but new tasks will not be scheduled until worker resources become available.

To limit this notification for a worker queue, increase its **Max # Workers** setting or choose a larger **Worker Type**. See [Configure worker queues](https://docs.astronomer.io/astro/configure-worker-queues).

### Monitoring Failure

Astro has failed to monitor your Deployment.

If you receive this incident notification, Astronomer Support has already been notified and no action is required from you. Ensure that you [configured a Deployment contact email](deployment-settings.md#configure-deployment-contact-emails) so that you can be notified if this issue requires additional follow-ups.

### Job Scheduling Disabled

The Airflow scheduler is currently disabled and will not automatically schedule new tasks. To trigger a task run in this state, you must manually trigger a DAG run.

To resume all scheduling, remove any overrides to the `AIRFLOW__SCHEDULER__USE_JOB_SCHEDULE` environment variable. This variable can be set either in the Cloud UI or in your Astro project Dockerfile.

### Airflow Component Unhealthy

At least one Airflow component has been unable to start successfully. This could be due to a misconfiguration or resource constraints. For more information, see **Details** for this alert or submit a request to [Astronomer Support](https://cloud.astronomer.io/open-support-request).

### Worker Queue Does Not Exist

There is at least 1 task that is configured to run on a worker queue that does not exist. Instances of this task will remain in the queued state until the worker queue is created.

To run these task instances, ensure that you have properly specified an existing worker queue's name in your task definition. See [Configure worker queues](configure-worker-queues.md#assign-tasks-to-a-worker-queue).