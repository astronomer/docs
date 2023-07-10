---
title: 'Submit a support request'
navTitle: 'Astro support'
id: astro-support
description: Get Astro support when you need it.
---

In addition to product documentation, the following resources are available to help you resolve issues:

- [Astronomer Forum](https://forum.astronomer.io)
- [Airflow Guides](https://docs.astronomer.io/learn/)

If you're experiencing an issue or have a question that requires Astronomer expertise, use one of the following methods to contact Astronomer support:

- Submit a support request in the [Cloud UI](https://cloud.astronomer.io/support).
- Submit a support request on the [Astronomer support portal](https://support.astronomer.io/hc/en-us).
- Send an email to [support@astronomer.io](mailto:support@astronomer.io).
- Call +1 (831) 777-2768.

## Best practices for support request submissions

The following are the best practices for submitting support requests in the Cloud UI or the Astronomer support portal:

### Always indicate priority

To help Astronomer support respond effectively to your support request, it's important that you correctly identify the severity of your issue. The following are the categories that Astronomer uses to determine the severity of your support request:

**P1:** Critical impact, service is unusable in production.

Examples:

- Your tasks are not running and restarting them didn't fix the issue.
- Astronomer is experiencing an incident or downtime that is affecting your data pipelines in production.

**P2:** High impact. Ability to use Astro is severely impaired but does not affect critical pipelines in production.

Examples:

- The Airflow UI is unavailable.
- You are unable to deploy code to your Deployment, but existing DAGs and tasks are running as expected.
- You need to [modify a Hybrid cluster setting](manage-hybrid-clusters.md) that is required for running tasks, such as adding a new worker instance type.
- Task logs are missing in the Airflow UI.

**P3:** Medium impact. Service is partially impaired.

Examples:

- There is a bug in the Software UI.
- You need to [modify a Hybrid cluster setting](manage-hybrid-clusters.md) that affects your cluster's performance but isn't required to run task, such as changing the size of your cluster's database or adding a new VPC peering connection.
- Astro CLI usage is impaired (for example, there are incompatibility errors between installed packages).
- There is an Airflow issue that has a code-based solution.
- You received a log alert on Astronomer.
- You have lost use of a Public Preview feature that does not affect general services. 

**P4:** Low impact. Astro is fully usable but you have a question for our team.

Examples:

- There are package incompatibilities caused by a specific, complex use case.
- You have an inquiry or a small bug report for a Public Preview feature.

### Be as descriptive as possible

The more information you can provide about the issue you're experiencing, the quicker Astronomer support can start the troubleshooting and resolution process. When submitting a support request, include the following information:

- Have you made any recent changes to your Deployment or running DAGs?
- What solutions have you already tried?
- Is this a problem in more than one Deployment?

### Include logs or code snippets

If you've already copied task logs or Airflow component logs, send them as a part of your request. The more context you can provide, the better.

## Submit a support request in the Cloud UI

1. In the Cloud UI, click **Help** > **Submit Support Request**.

    ![Submit Support Request menu location](/img/docs/support-request-location.png)

    Alternatively, you can directly access the support form by going to `https://cloud.astronomer.io/support`.

2. Select a **Request Type**. Your request type determines which other fields appear in the support request.
3. Complete the rest of the support request. 
4. Click **Submit**.

    You'll receive an email when your ticket is created and follow-up emails as Astronomer support replies to your request. To check the status of a support request, you can also sign in to the [Astronomer support portal](https://support.astronomer.io).

## Submit a support request on the Astronomer support portal

Astronomer recommends that you submit support requests in the Cloud UI. If you can't access the Cloud UI, you can submit support requests on the [Astronomer support portal](https://support.astronomer.io).

- If you're an existing customer, sign in to the [Astronomer support portal](https://support.astronomer.io) and create a new support request.
- If you're new to Astronomer, you'll need to create an account on the Astronomer support portal to submit a support request. Astronomer recommends that you use the same email address that you use to access Astro for your account. 
- If you're working with a team and want to view support tickets created by other team members, use your work email or the domain you share with other team members for your account (for example, `@astronomer.io`).
- If your team uses more than one email domain, contact Astronomer and ask to have the additional domains added to your organization.

## Monitor existing support requests

If you've submitted your support request on the Astronomer support portal, sign in to the [Astronomer support portal](https://support.astronomer.io) to:

- Review and comment on requests from your team.
- Monitor the status of all requests in your organization.

:::tip

To add a teammate to an existing support request, cc them when replying on the support ticket email thread.

:::

## Book office hours in the Cloud UI

If you don't require break-fix support, Astronomer recommends scheduling a meeting with the Astronomer Data Engineering team during office hours. In an office hour meeting, you can ask questions, make feature requests, or get expert advice for your data pipelines. Office hours are recommended if:

- You have questions about best practices for an action in Airflow or on Astro.
- You have a feature request related to Astro or Airflow.

To book an office hour meeting, open the Cloud UI and click **Help** > **Book Office Hours**. Use the provided Calendly form to schedule a 30-minute office hour meeting. In the form, provide details about the new issues and questions that you want to discuss during the meeting.
