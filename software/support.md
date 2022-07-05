---
title: 'Support for Astronomer Software'
navTitle: 'Support'
id: support
description: Get the most from Astronomer Support.
---

The primary objective of Astronomer is helping your organization adopt [Apache Airflow](https://airflow.apache.org/).

Since our inception, Astronomer has garnered a group of Airflow aficionados and experts who are dedicated to doing what they can to help your organization succeed.

In an effort to democratize all-things Airflow, Astronomer makes these resources available to all Airflow users:

- [Astronomer Forum](https://forum.astronomer.io)
- [Airflow Guides](https://www.astronomer.io/guides/airflow-and-hashicorp-vault)

If you're an existing Astronomer customer and you need support, the following options are available:

- Submit a request on the [Astronomer Support Portal](https://support.astronomer.io/hc/en-us)
- Send an email to [support@astronomer.io](mailto:support@astronomer.io)
- Call +1 (831) 777-2768 and leave a voicemail

## Astronomer's support portal

On Astronomer's support portal, you can do two things:

- Submit a Request (Ticket)
- Check the status of your existing requests

### Create an account

To submit a request to Astronomer Support, first create an account on our [Support Portal](https://support.astronomer.io).

If you're working with a team, make sure to create an account with your work email or a domain that the rest of your team shares. This will allow you to have visibility into support tickets across your team.

> **Note:** If your team uses more than one email domain (e.g. @astronomer.io), reach out to us so we can manually add it to your organization.

### Submit a support request

When you submit a ticket to Astronomer's Support Portal, keep the following best practices in mind.

#### 1. Always indicate priority

In order for our team to serve you most effectively, it's critical that we understand the impact of all reported issues. Generally speaking, here are the guidelines we operate under:

- **P1:** Mission critical systems are down, no workaround is immediately available

    Examples:

    - The scheduler is not heartbeating, and restarting didn't fix the issue.
    - All Celery workers are offline.
    - Kubernetes pod executors are not starting.
    - There are extended periods of `503` errors that are not solved by allocating more resources to the webserver.
    - There is an Astronomer outage, such as downtime in the Astronomer Docker Registry.

- **P2:** Some major functionality of Astronomer/Astronomer-owned Airflow is severely impaired, but you are still able to run essential DAGs.

    Examples:

    - The Airflow webserver is unavailable.
    - You are unable to deploy code to your Deployment, but existing DAGs and tasks are running as expected.
    - Task logs are missing in the Airflow UI.

- **P3:** Partial, non-critical loss of functionality of Astronomer/Astronomer-owned Airflow.

    Examples:

    - There is a bug in the Software UI.
    - Astro CLI usage is impaired (for example, there are incompatibility errors between installed packages).
    - There is an Airflow issue that has a code-based solution.
    - You received a log alert on Astronomer.

- **P4:** Questions, issues with code inside specific DAGs, and issues with Airflow that are not primarily owned by Astronomer.

    Examples:

    - You can't find your Workspace.
    - There are package incompatibilities caused by a specific, complex use case.
    - You have questions about best practices for an action in Airflow or on Astronomer.

#### 2. Be as descriptive as possible

The more you can tell us about the issue you're facing, the more quickly we can jump in. Consider including the following:

- What project/deployment does this question/issue apply to?
- What did you already try?
- Have you made any recent changes to your Airflow deployment, code, or image?

#### 3. Attach logs or code snippets if available

If you've already taken note of any task-level Airflow logs or Astronomer platform logs, don't hesitate to send them as a part of your original ticket.

The more context you can give, the better we can help you.

#### 4. Track existing support requests

Once you've submitted a support request to our team, track our response via our Support Portal.

1. See and comment on requests from your team
2. Check the status of your requests
3. Get responses from us via email

> **Note:** To add a teammate to an existing ticket, cc them in a followup message within the email thread automatically generated when the ticket was created.
