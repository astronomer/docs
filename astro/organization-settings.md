---
title: 'Update settings for your Astro Organization'
sidebar_label: 'Update Organization settings'
id: organization-settings
description: Update high-level settings for an Astro Organization that apply to all Workspaces, Deployments, and users.
---

An Organization is the highest management level on Astro. In addition to configuring infrastructure for your Organization, you can update Organization settings that apply to all clusters, Workspaces, Deployments, and users within the Workspace.

This document includes instructions to configure high-level Organization settings from the Cloud UI. To configure more specific Organization-level infrastructure, see:

- [Manage users in an Astro Organization](manage-organization-users.md)
- [Set up authentication and single sign-on for Astro](configure-idp.md)
- [Create a dedicated Astro cluster](create-dedicated-cluster.md)
- [Create and manage Organization API tokens](organization-api-tokens.md)

## Prerequisites

- Organization Owner permissions

## Update your Organization name

Your Organization name is human-readable name that appears in the Cloud UI and in the Astro CLI. Updating your Organization name is a cosmetic change that has no affect on any technical Organization data, such as your Organization ID or short name, which don't change for lifetime of the Organization. 

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. This opens the **General** Organization page.
2. In the **Organization Detail** section, click **Edit Details**.
3. Give your Organization a new **Organization Name**, then click **Update Organization**.

## Configure environment secrets fetching for the Astro Environment Manager

When members of your Organization test an Astro project using the Astro CLI, they can pull connections configured in the [Astro Environment Manager](#create-and-link-connections) to their local Airflow environment based on their Workspace credentials. See [Import and export Airflow connections and variables](import-export-connections-variables.md#from-the-cloud-ui) for more details. 

You can enable or disable this feature based on whether you want Organization members to access Astro-configured connection details from their local machines.

1. In the Cloud UI, click your Workspace name in the upper left corner, then click **Organization Settings**. This opens the **General** Organization page.
2. In the **Organization Detail** section, click **Edit Details**.
3. Click the **Environment Secrets Fetching** toggle to **Enabled** or **Disabled**, then click **Update Organization**.
