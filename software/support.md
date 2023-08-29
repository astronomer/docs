---
title: 'Submit a support request'
navTitle: 'Astronomer Software support'
id: support
description: Get Astronomer Software support when you need it.
---

In addition to product documentation, the following resources are available to help you resolve issues:

- [Astronomer Forum](https://forum.astronomer.io)
- [Airflow guides](https://docs.astronomer.io/learn/)

If you're experiencing an issue or have a question that requires Astronomer expertise, you can use one of the following methods to contact Astronomer support:

- Submit a support request on the [Astronomer support portal](https://support.astronomer.io/hc/en-us)
- Send an email to [support@astronomer.io](mailto:support@astronomer.io)
- Call +1 (831) 777-2768

## Best practices for support request submissions

The following are the best practices for submitting support requests in the Astronomer support portal:

### Always indicate priority

To help Astronomer support respond effectively to your support request, it's important that you correctly identify the severity of your issue. The following are the categories that Astronomer uses to determine the severity of your support request:

**P1:** Critical impact, a deployment is completely unavailable or a DAG that was previously working in production is no longer working.

Because P1 tickets are handled with the highest levels of urgency, if Astronomer Support responds on a P1 ticket and subsequently does not hear back for 2 hours, the ticket priority will be changed to P2.

**P2:** High impact. Ability to use Astronomer Software is severely impaired but does not affect critical, previously working pipelines in production.

Examples:

- A newly deployed production DAG is not working, even though it was tested in a lower environment.
- The Airflow UI is unavailable.
- You are unable to deploy code to your Deployment, but existing DAGs and tasks are running as expected.
- Task logs are missing in the Airflow UI.

**P3:** Medium impact. Service is partially impaired.

Examples:

- A DAG that has been deployed for the first time, or is on a local development environment, is unexpectedly not working.
- There is a bug in the Software UI.
- Astro CLI usage is impaired (for example, there are incompatibility errors between installed packages).
- There is an Airflow issue that has a code-based solution.
- An error message appeared in the Astronomer Software logs.

**P4:** Low impact. Astronomer Software is fully usable but you have a question for our team.

Examples:

- There are package incompatibilities caused by a specific, complex use case.
- You have questions about best practices for an action in Airflow or on Astronomer Software.
- You have a feature request related to Astronomer Software or Airflow.

### Be as descriptive as possible

The more information you can provide about the issue you're experiencing, the quicker Astronomer support can start the troubleshooting and resolution process. When submitting a support request, include the following information:

- Have you made any recent changes to your Deployment or running DAGs?
- What solutions have you already tried?
- Is this a problem in more than one Deployment?

### Include logs or code snippets

If you've already copied task logs or Airflow component logs, send them as a part of your request. The more context you can provide, the better.

## Submit a support request on the Astronomer support portal

If you're new to Astronomer, you'll need to create an account on the Astronomer support portal to submit a support request. Astronomer recommends that you use the same email address that you use to access Astronomer Software. If you're working with a team and want to view support tickets created by other team members, use your work email or the domain you share with other team members for your account (for example, `@astronomer.io`). If your team uses more than one email domain (for example, `@astronomer.io`), contact Astronomer and ask to have the additional domains added to your organization.

If you're an existing customer, sign in to the [Astronomer support portal](https://support.astronomer.io) and create a new support request.

## Monitor existing support requests

If you've submitted your support request on the Astronomer support portal, sign in to the [Astronomer support portal](https://support.astronomer.io) to:

- Review and comment on requests from your team.
- Monitor the status of all requests in your organization.

:::tip

To add a teammate to an existing support request, cc them when replying on the support ticket email thread.

:::
