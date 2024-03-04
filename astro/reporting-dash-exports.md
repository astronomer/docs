---
sidebar_label: 'Export reporting data'
title: "Export data reports and set up alerts"
id: reporting-dash-exports
description: "Export data from reporting dashboards or configure conditional exports as alerts."
---

:::warning

This feature is in [Private Preview](https://docs.astronomer.io/astro/feature-previews). Please reach out to your customer success manager to enable this feature.

:::

You can export data from your reporting dashboards, either as a file download, sent to an email address, or sent to an email address on a regular schedule. The reporting dashboard also offers you the ability to set up a *reporting dashboard alert*, or a scheduled data export that occurs when the data set meets certain conditional critera.

:::info

Only users with **Organization Billing Admin** [user permissions](user-permissions.md#organization-roles) can access reporting dashboards.

:::

As an Astro administrator, you might want to export reporting data to share with other team members or to keep a record of key performance indicators. Astro supports several different methods for exporting reporting data based on how and when you want to receive the data. Specifically, you can export data:

- Manually through the Cloud UI.
- On a regular schedule.
- Whenever a certain condition is met, such as a metric reaching a specific threshold.

When you export reporting data, Astro exports the last 1.0M of data from a specific dashboard in the file format of your choice. Use this document to learn about the different ways you can trigger the export process.

![Expand the menu to view all options for downloading data, emailing data, scheduling a data export, and setting up a data alert.](/img/docs/dash-open-menu.png)

## Download reporting data

In the **Export** menu, you can choose to download up to 1.0 M rows of data in a particular file format.

### Export reporting data to email

Instead of downloading your data directly, you can choose to email it to a specified address by choosing **Export** > **Send now**. Enter the recipient's email address and optionally edit the subject line and email body message. Then, in the **Attachments** section, select the report you want to send and file format to include it as. You can choose the from the same file types available for a one-time data download. To send more than one report, click **+ Add**.

:::tip

If you need to send data to a member of your team with fewer permissions on Astro, you can export the report with the recipient's level of user permissions by clicking **Run queries as recipient** in the **More options** section.

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

