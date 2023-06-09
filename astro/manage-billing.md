---
sidebar_label: 'Manage billing'
title: 'Manage Astro billing'
id: manage-billing
description: "Change your billing details and view your current spend from the Cloud UI."
---

On Astro Hosted, you're billed based on how many hours you run your Deployment, as well as how many resources your Deployment components use. See [Pricing](https://www.astronomer.io/pricing/) for more a complete breakdown of possible costs.

You can configure payment information and check your total Astro spend from the Cloud UI so that you don't go over your budget for running Airflow.

## Update billing details

In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Billing**. The **Billing** menu includes the following tabs for tracking your payments:

- **Overview** shows your current payment information and your total spend for the current billing cycle.
- **Invoices** shows a breakdown of charges for current and previous billing cycles.
- **Usage** shows your spend over time for each billable Airflow component.

## Update billing details

1. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Billing**. 
2. If you have no payment method on file, click **Add Payment Method** and enter your payment details. To edit an existing payment method, click **Edit** next to the payment method.

## View total spend

In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Billing**. 

The **Overview** page contains high level information about your total Astro spend. 

- **Accrued charges** is the total amount you've spent on Astro resources for the current billing cycle before trial credits and discounts are applied.
- **Balance due** is the total amount you owe for the current billing cycle after trial credits and discounts are applied. If you're on a trial, this is also where you can view how many credits you have left.

## View invoices

1. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Billing**. 
2. Click **Invoices**. 

By default, the Cloud UI shows a draft invoice for your current billing cycle. 

- Each **Charge** is an Astro component that you used at some point in the billing cycle. Note that your worker resources are charged separately from the Deployments they run on and each other. For example, a Deployment with two worker queues will appear as three separate charges in your invoice. 
- **Quantity** represents the number of hours you ran a given Astro component.

:::info

The **Billing** page updates every hour with your total spend in the previous complete hour. For example, at 10:00 AM, the page updates with your spend from 8:00 AM - 9:00 AM on that same day. If your spending metrics don't look accurate based on recent usage, wait until the next complete hour for the page to update.

:::

## View component usage by date

1. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **Billing**. 
2. Click **Usage**. 

Each chart on this page shows your usage over the last 30, 60, or 90 days for each billable component type. Hover over nodes on the chart to see your total hour spend for a component on a given day. Use the dropdown menu in the upper right corner to change the timeframe for each chart.

The charts are organized by component type. For a given component type, the chart shows usage for all instances of a given component type across your Organization. Therefore, it's possible to have more than 24 hours of usage for a given day. For example, if you have two **Deployment with Medium Schedulers** running for 24 hours in a day, the usage chart will show that your total usage for the day was 48 hours.
