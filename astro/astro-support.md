---
title: 'Submit a Support Request'
navTitle: 'Astro Support'
id: astro-support
description: Get Astro support when you need it.
---

In addition to product documentation, the following resources are available to help you resolve issues:

- [Astronomer Forum](https://forum.astronomer.io)
- [Airflow Guides](https://www.astronomer.io/guides/)

If you're experiencing a more serious issue and need Astronomer expertise, you can use one of the following methods to contact Astronomer Support:

- Submit a support request in the [Cloud UI](astro-support.md#submit-a-support-request-in-the-cloud-ui)
- File a support request on the [Astronomer Support Portal](https://support.astronomer.io/hc/en-us)
- Send an email to [support@astronomer.io](mailto:support@astronomer.io)
- Call +1 (831) 777-2768

## Best Practices for Support Request Submissions

The following are the best practices for submitting support requests in the Cloud UI or the Astronomer Support Portal:

### Always indicate priority

To help Astronomer Support respond effectively to your support request, it's important that you correctly identify the severity of your issue. The following are the categories that Astronomer uses to determine the severity of your support request:

**P1:** Critical impact, service is unusable in production.

Examples:

- Your tasks are not running and restarting them didn't fix the issue.
- Astronomer is experiencing an incident or downtime that is affecting your data pipelines in production.

**P2:** High impact. Ability to use Astro is severely impaired but does not affect critical pipelines in production.

Examples:

- The Airflow UI is unavailable.
- You are unable to deploy code to your Deployment, but existing DAGs and tasks are running as expected.
- Task logs are missing in the Airflow UI.

**P3:** Medium impact, service is partiallly impaired.

Examples:

- There is a bug in the Software UI.
- Astro CLI usage is impaired (for example, there are incompatibility errors between installed packages).
- There is an Airflow issue that has a code-based solution.
- You received a log alert on Astronomer.

**P4:** Low impact, service fully usable.

Examples:

- You can't find your Workspace.
- There are package incompatibilities caused by a specific, complex use case.
- You have questions about best practices for an action in Airflow or on Astronomer.

### Be as descriptive as possible

The more information you can provide about the issue you're experiencing, the quicker Astronomer Support can start the troubleshooting and resolution process. When submitting a support request, include the following information:

- What project/deployment does this question/issue apply to?
- What did you already try?
- Have you made any recent changes to your Deployment or running DAGs?

### Include logs or code snippets

If you've already copied task logs or Airflow component logs, send them as a part of your request. The more context you can provide, the better.

## Submit a Support Request in the Cloud UI

1. In the Cloud UI, click **Help** > **Submit Support Request**.

    <div class="text--center">
    <img src="/img/docs/support-request-location.png" alt="Submit Support Request menu location" />
    </div>

2. Complete the following fields:

    - **Problem Statement**: Enter a description of the issue you are experiencing. Provide as much detail as possible.
    - **Workspace**: Optional. Select the Workspace where the issue is occurring. This list is auto-populated when you submit a support request from a Workspace or a Deployment.
    - **Deployment**: Optional. Select the Deployment where the issue is occurring. This list is auto-populated when you submit a support request from a Workspace or a Deployment.
    - **Problem Start**: Optional. Select the date and time the issue started.
    - **Description**: Enter a thorough description of the issue. Provide as much detail as possible. 
    - **Priority**: Select the severity of your issue based on how the issue is affecting your organization. For severity level explanations, see [Best Practices for Submitting Support Requests](astro-support.md#best-practices-for-support-request-submissions).
    - **Business Impact**: Optional. Describe how this issue is affecting your organization.
    - **CC Emails**: Optional. Enter the email address of a team member that you want to notify about this issue. Click **Add Additional Email** to add additional email addresses.

3. Click **Submit**.

    You'll receive an email when your ticket is created and follow-up emails as Astronomer Support processes your request. To check the status of a support request, sign in to the [Astronomer Support Portal](https://support.astronomer.io). 

## Submit a Support Request on the Astronomer Support Portal

Astronomer recommends that you submit support requests in the Cloud UI. If you can't access the Cloud UI, you can submit support requests on the [Astronomer Support Portal](https://support.astronomer.io).

If you're new to Astronomer, you'll need to create an account on the Astronomer Support Portal to submit a support request. If you're working with a team and want to view support tickets created by other team members, use your work email or the domain you share with your team members for your account. If your team uses more than one email domain (for example, `@astronomer.io`), contact Astronomer and ask to have the additional domains added to your organization.

If you're an existing customer, sign in to the [Astronomer Support Portal](https://support.astronomer.io) and create a new support request.

## Monitor Existing Support Requests

If you've submitted your support request on the Astronomer Support Portal, sign in to the [Astronomer Support Portal](https://support.astronomer.io) to:

- Review and comment on requests from your team.
- Monitor the status of your requests.
- Communicate with Astronomer Support.

:::tip

To add a teammate to an existing support request, cc them when replying on the support ticket email thread.

:::