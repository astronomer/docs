---
sidebar_label: 'Deployment logs'
title: 'Deployment logs on Astronomer Software'
id: deployment-logs
description: View and search Airflow webserver, scheduler, and worker logs via the Astronomer Software UI.
---

The Software UI allows you to look up and search Airflow logs emitted by your webserver, scheduler and Worker(s) for any deployment you have access to.

### Interpreting logs

We've designed this view to give you access to deployment level logs that will help you monitor the health of your deployment's Airflow components (webserver, scheduler, Worker).

A few use cases:

- See your scheduler, webserver, and workers all restart after you push `astro dev deploy`
- If your Airflow UI is not loading as expected - is your webserver in a CrashLoop?
- How quickly is your scheduler queuing up tasks?
- Is your Celery worker behaving unexpectedly?

**Note:** These are _not_ task-level logs that you'd find in the Airflow Web UI. Logs on Astronomer are not a replacement for task-level logging in the Airflow UI.

### Prerequisites

To view logs on Astronomer, you'll need:

- Access to an Astronomer Software Installation
- An Airflow deployment on Astronomer

## View logs

To view Airflow logs, log into Astronomer and navigate to: Deployment > Logs.

In the dropdown on the top-right, you'll see a button where you can toggle between logs for your:

- Scheduler
- Webserver
- Workers (*if applicable*)

![Webserver Logs Page](/img/software/logs-webserver.png)

### Filter by time/date

As you manage logs, you can filter by:

- Past 5 minutes
- Past hour
- Today
- All time

To adjust this filter, toggle the top right menu.

### Search logs

On Astronomer, you can search for logs with a text string on the top right.

![Search Logs](/img/software/logs-search.png)
