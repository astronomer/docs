---
title: 'Submit a support request'
navTitle: 'Astro support'
id: astro-support
description: Get Astro support when you need it.
---

import BusinessBadge from '@site/src/components/BusinessBadge';

In addition to product documentation, the following resources are available to help you resolve issues:

- [Astronomer knowledge base](https://support.astronomer.io/hc/en-us)
- [Airflow guides](https://www.astronomer.io/docs/learn/)
If you're experiencing an issue or have a question that requires Astronomer expertise, use one of the following methods to contact Astronomer support:

- Submit a support request in the [Astro UI](https://cloud.astronomer.io/open-support-request).
- Submit a support request on the [Astronomer support portal](https://support.astronomer.io/hc/en-us).
- Send an email to [support@astronomer.io](mailto:support@astronomer.io).

## Best practices for support request submissions

The following are the best practices for submitting support requests in the Astro UI or the Astronomer support portal:

### Check the Astro status page

Before you open a ticket for unexpected or disruptive behavior on Astro, check the [Astro status page](https://status.astronomer.io/) to see if the problem you're experiencing has already been reported.

### Be as descriptive as possible

The more information you can provide about the issue you're experiencing, the quicker Astronomer support can start the troubleshooting and resolution process. When submitting a support request, include the following information:

- Have you made any recent changes to your Deployment or running DAGs?
- What solutions have you already tried?
- Is this a problem in more than one Deployment?

### Include logs or code snippets

If you've already copied task logs or Airflow component logs, send them as a part of your request. The more context you can provide, the better.

### Check recommended support articles

If you draft your support ticket on the [Astronomer support portal](https://support.astronomer.io), the portal automatically recommends support articles to you based on the content in your ticket. Astronomer recommends looking through these recommendations to see if your issue has a documented solution before submitting your ticket.

You can also proactively search support articles without submitting a support ticket on the [Astronomer knowledge base](https://support.astronomer.io/hc/en-us).

## Submit a support request in the Astro UI

1. In the Astro UI, click **Help** > **Submit Support Request**.

    ![Submit Support Request menu location](/img/docs/support-request-location.png)

    Alternatively, you can directly access the support form by going to `https://cloud.astronomer.io/open-support-request`.

2. Select a **Request Type**. Your request type determines which other fields appear in the support request.
3. Complete the rest of the support request.
4. Click **Submit**.

    You'll receive an email when your ticket is created and follow-up emails as Astronomer support replies to your request. To check the status of a support request, you can also sign in to the [Astronomer support portal](https://support.astronomer.io).

## Submit a support request on the Astronomer support portal

Astronomer recommends that you submit support requests in the Astro UI. If you can't access the Astro UI, sign in to the [Astronomer support portal](https://support.astronomer.io) and create a new support request.

If you're new to Astronomer, you'll need to create an account on the Astronomer support portal to submit a support request. Astronomer recommends that you create an account with the same email address that you use to access Astro. This allows you to view support tickets from other team members that have email addresses with the same domain.

If your team uses more than one email domain, add all domains to your Organization so that team members with different email domains can view each others' support requests. See [Create and manage domains for your Organization](manage-domains.md).

## Monitor existing support requests

If you've submitted your support request on the Astronomer support portal, sign in to the [Astronomer support portal](https://support.astronomer.io) to:

- Review and comment on requests from your team.
- Monitor the status of all requests in your organization.

:::tip

To add a teammate to an existing support request, cc them when replying on the support ticket email thread.

:::

## Ticket Priorities

To help Astronomer Support respond effectively to your support request, priorities are determined automatically by Astronomer. Refer to the [Astronomer Technical Support and Success Packages](https://www.astronomer.io/legal/technical-support-success-packages/) to read more about ticket priorities and their SLAs.

The following sections show the four ticket priorities with examples and descriptions for each:

### P1: Critical impact

A Deployment is completely unavailable, or a DAG that was previously working in production is no longer working.

Astronomer handles P1 tickets with the highest levels of urgency. If Astronomer Support responds to a P1 ticket, and subsequently does not hear back from you for 2 hours, the ticket priority is automatically changed to P2.

Additionally, if the immediate problem is solved, but follow-up investigations continue, those investigations are conducted in a separate ticket at a lower priority.

### P2: High impact

Your ability to use Astro is severely impaired, but does not affect any critical, previously working pipelines in production.

Examples:

- A newly deployed production DAG is not working, even though it worked successfully in a development or test environment.
- The Airflow UI is unavailable.
- You can't deploy code to your Deployment, but existing DAGs and tasks run as expected.
- You need to [modify a Hybrid cluster setting](manage-hybrid-clusters.md) that is required for running tasks, such as adding a new worker instance type.
- Task logs are missing in the Airflow UI.

### P3: Medium impact

Service is partially impaired.

Examples:

- A newly deployed DAG is not working in a development Deployment, even though it worked successfully in a local environment using the Astro CLI.
- You need to [modify a Hybrid cluster setting](manage-hybrid-clusters.md) that affects your cluster's performance, but isn't required to run tasks, such as changing the size of your cluster's database or adding a new VPC peering connection.
- Astro CLI usage is impaired. For example, there are incompatibility errors between installed packages.
- There is an Airflow issue that has a code-based solution.
- You received a log alert on Astronomer.
- You lost the ability to use a [Public Preview](https://docs.astronomer.io/astro/feature-previews) feature that does not affect general services.

### P4: Low impact

Astro is fully usable, but you have a question for the Support team.

Examples:

- There are package incompatibilities caused by a specific, complex use case.
- You have an inquiry or a small bug report for a Public Preview feature.

## Request an escalation for an existing support ticket
<BusinessBadge/>

Business and Enterprise customers can request escalated support for an existing ticket. To request a support escalation, email escalations@astronomer.io with the following information:

* Ticket number
* Issue summary
* Reason for escalation

Reasons for escalation include:

* The ticket is taking much longer than expected to resolve.
* Multiple attempts to solve the issue have failed.
* The urgency of the ticket has increased substantially.
## Book office hours

If you don't require break-fix support, Astronomer recommends scheduling a meeting with the Astronomer Data Engineering team during office hours. In an office hours meeting, you can ask questions, make feature requests, or get expert advice for your data pipelines.

For more information about booking an office hour meeting, see [Book an office hours appointment](office-hours.md#book-an-office-hours-appointment).
