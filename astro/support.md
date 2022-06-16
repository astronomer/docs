---
title: 'Astro Support'
navTitle: 'Astro Support'
id: support
description: Get Astro support when you need it.
---

If you're an Astro user and need answers to common questions, the following resources are available:

- [Astronomer Forum](https://forum.astronomer.io)
- [Airflow Guides](https://www.astronomer.io/guides/airflow-and-hashicorp-vault)

If you're experiencing a more serious issue and need Astronomer expertise, you can use one of the following methods to contact Astronomer Support:

- Submit a support request in the [Cloud UI](#submit-a-support-request-in-the-cloud-ui)
- File a support request on the [Astronomer Support Portal](https://support.astronomer.io/hc/en-us)
- Send an email to [support@astronomer.io](mailto:support@astronomer.io)
- Call +1 (831) 777-2768

## Best Practices for Support Request Submissions

The following are the best practices for submitting support requests on the Astronomer Support Portal:

- Always indicate priority

    To help Astronomer Support respond effectively to your support request, it's important that you correctly identify the severity of your issue. The following are the categories that Astronomer uses to determine the severity of your support request:

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

## Submit a Support Request in the Cloud UI

If you're using Astro version 5.0.4 or later, you can submit your support request in the Cloud UI.

1. In the Cloud UI, click **Help** > **Submit Support Request**.

2. Complete the following fields:

    - **Problem Statement**: Enter a description of the issue you are experiencing. Provide as much detail as possible.
    - **Workspace**: Optional. Select the Workspace where the issue is occurring. This list is auto-populated when you submit a support request from a Workspace or a Deployment.
    - **Deployment**: Optional. Select the Deployment where the issue is occurring. This list is auto-populated when you submit a support request from a Workspace or a Deployment.
    - **Problem Start**: Optional. Select the date and time the issue started.
    - **Description**: Enter a thorough description of the issue. Provide as much detail as possible. 
    - **Priority**: Select the severity of your issue. For severity level explanations, see [Best Practices for Submitting Support Requests](#best-practices-for-submitting-support-requests).
    - **Business Impact**: Optional. Describe how this issue is affecting your organization.
    - **CC Emails**: Optional. Enter the email address of a team member that you want to notify about this issue. Click **Add Additional Email** to add additional email addresses.

3. Click **Submit**.

## Submit a Support Request on the Astronomer Support Portal

If you're new to Astronomer, you'll need to create an account on the [Astronomer Support Portal](https://support.astronomer.io) to submit a support request. If you're working with a team and want to view support tickets created by other team members, use your work email or the domain you share with your team members for your account. If your team uses more than one email domain (for example, @astronomer.io), contact Astronomer and ask to have it added manually to your organization

If you're an existing customer, sign in to the Astronomer Support Portal and create a new support request.

## Monitor Existing Support Requests

After you've submitted your support request, sign in to the [Astronomer Support Portal](https://support.astronomer.io) to:

- Review and comment on requests from your team
- Monitor the status of your requests
- Communicate with Astronomer Support

> **Note:** To add a teammate to an existing ticket, cc them in a followup message within the email thread that was automatically generated when the ticket was created.