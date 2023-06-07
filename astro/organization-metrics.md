---
sidebar_label: 'Organization'
title: 'View metrics for an Astro Organization'
id: organization-metrics
---

Organization metrics help Organization Owners and Billing Admins track resource usage across all Workspaces in Astro. Use Organization metrics to identify Deployments that could have their resource usage optimized.

## Astro usage

To access the **Usage** page, click the Astronomer logo in the upper left corner of the Cloud UI, then click **Usage**.

Use the **Usage** to review the number of successful task runs across Deployments in your Organization.

![Usage tab in the Cloud UI](/img/docs/usage.png)

The bar chart on the left shows your Organization's total successful task runs per day for the past 31 days, with each day's volume sorted by Deployment. Each color in the bar chart represents a different Deployment. To see each Deployment's number of successful task runs for a given day, you can hover over the bar chart for that day with your mouse.

The legend on the right side of the menu shows the colors used for each Deployment. This legend shows each Deployment's total sum of successful task runs over the last 31 days. The daily numbers on the left bar chart add up to the monthly total per Deployment on the right.

To export this data as a `.csv` file, click the **Export** button above the legend.

## See also

- [DAG metrics](dag-metrics.md)
- [Deployment metrics](deployment-metrics.md)
