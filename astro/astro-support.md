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

- Submit a support request in the [Cloud UI](https://cloud.astronomer.io/open-support-request).
- Submit a support request on the [Astronomer support portal](https://support.astronomer.io/hc/en-us).
- Send an email to [support@astronomer.io](mailto:support@astronomer.io).
- Call +1 (831) 777-2768.

## Best practices for support request submissions

The following are the best practices for submitting support requests in the Cloud UI or the Astronomer support portal:

### Always indicate priority

To help Astronomer support respond effectively to your support request, it's important that you correctly identify the severity of your issue. The following are the categories that Astronomer uses to determine the severity of your support request:

**P1:** Critical impact. A Deployment is completely unavailable, or a DAG that was previously working in production is no longer working.

P1 tickets are handled with the highest levels of urgency, if Astronomer Support responds on a P1 ticket and subsequently does not hear back for 2 hours, the ticket priority will be automatically changed to P2.

Additionally, if the immediate problem is solved but there are follow up investigations ongoing, those follow ups will be conducted in a separate ticket at a lower priority.

**P2:** High impact. Ability to use Astro is severely impaired but does not affect critical, previously working pipelines in production.

Examples:

- A newly deployed production DAG is not working, even though it ran successfully in a development or test environment.
- The Airflow UI is unavailable.
- You are unable to deploy code to your Deployment, but existing DAGs and tasks are running as expected.
- You need to [modify a Hybrid cluster setting](manage-hybrid-clusters.md) that is required for running tasks, such as adding a new worker instance type.
- Task logs are missing in the Airflow UI.

**P3:** Medium impact. Service is partially impaired.

Examples:

- A newly deployed DAG is not working in a development Deployment, even though it ran successfully in a local environment using the Astro CLI.
- You need to [modify a Hybrid cluster setting](manage-hybrid-clusters.md) that affects your cluster's performance but isn't required to run tasks, such as changing the size of your cluster's database or adding a new VPC peering connection.
- Astro CLI usage is impaired (for example, there are incompatibility errors between installed packages).
- There is an Airflow issue that has a code-based solution.
- You received a log alert on Astronomer.
- You have lost the ability to use a [Public Preview](https://docs.astronomer.io/astro/feature-previews) feature that does not affect general services.

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

    Alternatively, you can directly access the support form by going to `https://cloud.astronomer.io/open-support-request`.

2. Select a **Request Type**. Your request type determines which other fields appear in the support request.
3. Complete the rest of the support request. 
4. Click **Submit**.

    You'll receive an email when your ticket is created and follow-up emails as Astronomer support replies to your request. To check the status of a support request, you can also sign in to the [Astronomer support portal](https://support.astronomer.io).

## Submit a support request on the Astronomer support portal

Astronomer recommends that you submit support requests in the Cloud UI. If you can't access the Cloud UI, sign in to the [Astronomer support portal](https://support.astronomer.io) and create a new support request. 

If you're new to Astronomer, you'll need to create an account on the Astronomer support portal to submit a support request. Astronomer recommends that you create an account with the same email address that you use to access Astro. This allows you to view support tickets from other team members that have email addresses with the same domain.

If your team uses more than one email domain, add all domains to your Organization so that team members with different email domains can view each others' support requests. See [Create and manage domains for your Organization](manage-domains.md).

## Monitor existing support requests

If you've submitted your support request on the Astronomer support portal, sign in to the [Astronomer support portal](https://support.astronomer.io) to:

- Review and comment on requests from your team.
- Monitor the status of all requests in your organization.

:::tip

To add a teammate to an existing support request, cc them when replying on the support ticket email thread.

:::

## Book office hours

If you don't require break-fix support, Astronomer recommends scheduling a meeting with the Astronomer Data Engineering team during office hours. In an office hours meeting, you can ask questions, make feature requests, or get expert advice for your data pipelines. 

For more information about booking an office hour meeting, see [Book an office hours appointment](office-hours.md#book-an-office-hours-appointment).
