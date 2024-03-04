---
sidebar_label: 'Export reporting data'
title: "Export data reports and set up alerts"
id: reporting-dash-exports
description: "Export data from reporting dashboards or configure conditional exports as alerts."
---

:::info Enterprise

Organization reporting dashboards are only available if you have an Enterprise product plan.

:::


You can export data from your reporting dashboards, either as a file download, sent to an email address, or sent to an email address on a regular schedule. The reporting dashboard also offers you the ability to set up a *reporting dashboard alert*, or a scheduled data export that occurs when the data set meets certain conditional critera.

As an Astro administrator, you might want to export reporting data to share with other team members or to keep a record of key performance indicators. Astro supports several different methods for exporting reporting data based on how and when you want to receive the data. Specifically, you can export data:

- Manually through the Astro UI.
- On a regular schedule.
- Whenever a certain condition is met, such as a metric reaching a specific threshold.

When you export reporting data, Astro exports the last [1.0 million rows of data](https://help.sigmacomputing.com/docs/download-export-and-upload-limitations) from a specific dashboard in the file format of your choice. Use this document to learn about the different ways you can trigger the export process.

## Prerequisites

- Only users with **Organization Billing Admin** [user permissions](user-permissions.md#organization-roles) can access Organization dashboards.

## Download reporting data

1. To view Astro reporting dashboards, click your Workspace name in the upper left corner of the Astro UI, click **Organization Settings**, and then click **Dashboards**. You can also access this page directly at [https://cloud.astronomer.io/dashboards](https://cloud.astronomer.io/dashboards).
2. Open the **Export** menu on the chart or table that you want to export.
<img src={require("../static/img/docs/dash-open-menu.png").default} alt="Expand the menu to view all options for downloading data, emailing data, scheduling a data export, and setting up a data alert." style={{ width: "60%", maxWidth: "400px", height: "auto" }} />

3. Choose the file format that you want to use to download your data. Astro generates your data export and saves it to your Downloads folder.

## Export reporting data to email

Instead of downloading your data directly, you can choose to email it to a specified address.

1. To view Astro reporting dashboards, click your Workspace name in the upper left corner of the Astro UI, click **Organization Settings**, and then click **Dashboards**. You can also access this page directly at [https://cloud.astronomer.io/dashboards](https://cloud.astronomer.io/dashboards).
2. Open the **Export** menu and then select **Send now**.

<img src={require("../static/img/docs/dash-open-menu.png").default} alt="Expand the menu to view all options for downloading data, emailing data, scheduling a data export, and setting up a data alert." style={{ width: "60%", maxWidth: "400px", height: "auto" }} />

3. Enter the recipient's email address and optionally edit the subject line and email body message.
    :::tip

    If you need to send data to a member of your team with fewer permissions on Astro, you can export the report with the recipient's level of user permissions by clicking **Run queries as recipient** in the **More options** section.

    :::
4. In the **Attachments** section, select the report you want to send and file format to include it as. You can choose from the same file types available for a one-time data download.
5. (Optional) To send more than one report, click **+ Add**, and then select the report you want to send and its file format.

When you receive a report via email, the sender appears as **Sigma Computing**. The subject line also includes the name of the dashboard element's data you exported.

![Example email alert shows the sender as Sigma with information about the report in the subject line.](/img/docs/dash-email-alert.png)

### Schedule an emailed data report

1. To view Astro reporting dashboards, click your Workspace name in the upper left corner of the Astro UI, click **Organization Settings**, and then click **Dashboards**. You can also access this page directly at [https://cloud.astronomer.io/dashboards](https://cloud.astronomer.io/dashboards).
2. Open the **Export** menu for the reporting element you want to schedule an email export for and select **Schedule**.

<img src={require("../static/img/docs/dash-open-menu.png").default} alt="Expand the menu to view all options for downloading data, emailing data, scheduling a data export, and setting up a data alert." style={{ width: "60%", maxWidth: "400px", height: "auto" }} />

3. Enter the recipient's email address and optionally edit the subject line and email body message.

    :::tip

    If you need to send data to a member of your team with fewer permissions on Astro, you can export the report with the recipient's level of user permissions by clicking **Run queries as recipient** in the **More options** section.

    :::


If you toggle **Condition** when setting up your schedule, it allows you to configure a conditional data export, or *reporting dashboard alert*. Instead of sending a report at a specific time interval, it sends a data report when your data meets criteria that you define.

## Set up a reporting dashboard alert

1. To view Astro reporting dashboards, click your Workspace name in the upper left corner of the Astro UI, click **Organization Settings**, and then click **Dashboards**. You can also access this page directly at [https://cloud.astronomer.io/dashboards](https://cloud.astronomer.io/dashboards).
2. Open the **Export** menu for the reporting element you want to set up an alert for.

<img src={require("../static/img/docs/dash-open-menu.png").default} alt="Expand the menu to view all options for downloading data, emailing data, scheduling a data export, and setting up a data alert." style={{ width: "60%", maxWidth: "400px", height: "auto" }} />

2. Click **Alert when**, or toggle **Condition** when setting up your scheduled email data report, to define when you want the reporting dashboard to send a data report to a defined email address.

<img src={require("../static/img/docs/dash-export-alert.png").default} alt="Configure the conditions that trigger the reporting dashboard to send you a data report for a particular dashboard element." style={{ width: "60%", maxWidth: "400px", height: "auto" }} />

Like with an emailed dashboard report, when you receive a dashboard alert in an email, the sender appears as **Sigma Computing**. The subject line also includes the name of the dashboard element's data you exported.

