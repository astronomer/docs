---
sidebar_label: 'Set up reporting data exports'
title: "Export data reports and set up alerts"
id: reporting-dashboard-exports
description: "Export data from reporting dashboards or configure conditional exports as alerts."
---

:::warning

This feature is in [Private Preview](https://docs.astronomer.io/astro/feature-previews). Please reach out to your customer success manager to enable this feature.

:::

You can export data from your reporting dashboards, either as a file download, sent to an email address, or sent to an email address on a regular schedule. The reporting dashboard also offers you the ability to set up a *reporting dashboard alert*, or a scheduled data export that occurs when the data set meets certain conditional critera.

:::info

Only users with **Organization Billing Admin** [user permissions](user-permissions.md#organization-roles) can access reporting dashboards.

:::

Hover over the dashboard element whose data you want to export, and then expand the additional options menu to choose to either **Export** your data or **Alert when** to email your data to you when it meets your specified criteria.

![Expand the menu to view all options for downloading data, emailing data, scheduling a data export, and setting up a data alert.](/img/docs/dash-email-alert.png)

## Download data

In the **Export** menu, you can choose to download up to 1.0 M rows of data in a particular file format.

## Email a data export

Instead of downloading your data directly, you can choose to email it to a specified address by choosing **Export** > **Send now**. Enter the recipient's email address and optionally edit the subject line and email body message. Then, in the **Attachments** section, select the report you want to send and file format to include it as. You can choose the from the same file types available for a one-time data download. To send more than one report, click **+ Add**.

:::tip

When you configure a data export or alert that is sent to an email address, you can choose to run the report with their level of user permissions by clicking **Run queries as recipient** in the **More options** section.

:::

When you receive a report via email, the sender appears as **Sigma Computing**. The subject line also includes the name of the dashboard element's data you exported.

![Example email alert shows the sender as Sigma with information about the report in the subject line.](/img/docs/dash-email-alert.png)

### Schedule an emailed data report

In addition to emailing a data report once, you can set up a schedule to routinely receive data reports from Astronomer. Select **Export** > **Schedule** to set up your scheduled data export.

If you toggle **Condition** when setting up your schedule, it allows you to configure a conditional data export, or *reporting dashboard alert*. Instead of sending a report at a specific time interval, it sends a data report when your data meets criteria that you define.

## Set up a reporting dashboard alert

Click **Alert when**, or toggle **Condition** when setting up your scheduled email data report, to define when you want the reporting dashboard to send a data report to a defined email address.

![Configure the conditions that trigger the reporting dashboard to send you a data report for a particular dashboard element.](/img/docs/dash-export-alert.png)

Like with an emailed dashboard report, when you receive a dashboard alert, the sender appears as **Sigma Computing**. The subject line also includes the name of the dashboard element's data you exported.

