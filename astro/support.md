---
title: 'Astro Support'
navTitle: 'Astro Support'
id: support
description: Get Astro support when you need it.
---

If you're an Astro user and need answers to common questions, the following resources are available:

- [Astronomer Forum](https://forum.astronomer.io)
- [Airflow Guides](https://www.astronomer.io/guides/airflow-and-hashicorp-vault)

If you've encountered a more serious issue and need Astronomer expertise,  you can use one of the following methods to contact Astronomer Support:

- Submit a support request in the Cloud UI
- File a support request on the [Astronomer Support Portal](https://support.astronomer.io/hc/en-us)
- Send an email to [support@astronomer.io](mailto:support@astronomer.io)
- Call +1 (831) 777-2768

## Submit a Support Request on the Astronomer Support Portal

To submit a support request to Astronomer Support, you need to create an account on the [Astronomer Support Portal](https://support.astronomer.io).

If you're working with a team, create an account with your work email or the domain you share with your team members. This lets you view support tickets created by other team members.

> **Note:** If your team uses more than one email domain (e.g. @astronomer.io), contact Astronomer to have it added manually to your organization.

The following are the best practices for submitting support requests on the Astronomer Support Portal:

- Always indicate priority

    To help Astronomer Support respond effectively to your support request, it's important that you correctly identify the severity of your issue. The following are the catergories that Astronomer uses to determine the severity of your support request:

    - **P1:** Critical systems are unavailable, no workaround is immediately available

        Examples:

        - The Scheduler is not heartbeating, and restarting didn't fix the issue.
        - All Celery workers are offline.
        - Kubernetes pod executors are not starting.
        - There are extended periods of `503` errors that are not solved by allocating more resources to the Webserver.
        - There is an Astronomer outage, such as downtime in the Astronomer Docker Registry.

    - **P2:** Significant Astronomer/Astronomer-owned Airflow functionality is impaired, but your organization is still able to run essential DAGs.

        Examples:

        - The Airflow Webserver is unavailable.
        - You are unable to deploy code to your Deployment, but existing DAGs and tasks are running as expected.
        - Task logs are missing in the Airflow UI.

    - **P3:** Partial, non-critical loss of Astronomer/Astronomer-owned Airflow functionality.

        Examples:

        - There is a bug in the Software UI.
        - Astro CLI usage is impaired (for example, there are incompatibility errors between installed packages).
        - There is an Airflow issue that has a code-based solution.
        - You received a log alert on Astronomer.

    - **P4:** General questions, issues with code inside specific DAGs, and issues with Airflow that are not primarily owned by Astronomer.

        Examples:

        - You can't find your Workspace.
        - There are package incompatibilities caused by a specific, complex use case.
        - You have questions about best practices for an action in Airflow or on Astronomer.

- Be as descriptive as possible

    The more information you can provide about the issue you're experiencing, the quicker Astronomer Support can start the troubleshooting and resolution process. When submitting a support request, include the following information:

    - What project/deployment does this question/issue apply to?
    - What did you already try?
    - Have you made any recent changes to your Airflow deployment, code, or image?

- Include logs or code snippets

    If you've already taken note of any task-level Airflow logs or Astronomer platform logs, don't hesitate to send them as a part of your original ticket.

    The more context you can give, the better we can help you.

## Track existing support requests

Once you've submitted your support request to Astronomer Support, you can monitor progress on the Astronomer Support Portal.

- See and comment on requests from your team
- Check the status of your requests
- Get responses from us by email

> **Note:** To add a teammate to an existing ticket, cc them in a followup message within the email thread automatically generated when the ticket was created.