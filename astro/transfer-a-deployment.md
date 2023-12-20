---
sidebar_label: 'Transfer a Deployment'
title: 'Transfer a Deployment to a different Workspace'
id: transfer-a-deployment
description: "Transfer a Deployment to another Workspace in the same cluster."
---

Transferring a Deployment can be helpful when your team needs to change user access to a Deployment. Transferring a Deployment moves all DAGs, task history, connections, and other Astro configurations to another Workspace. This process does not affect your task scheduling or any currently running tasks.

## Prerequisites

- You must be a Workspace Owner or Operator in both the original Workspace and the target Workspace.
- The Workspaces must be in the same Organization. 
- Deployments cannot be transferred to a different cluster from the one in which they were created.
- Only the users who are members of the target Workspace can access the Deployment after it is transferred. 

## Transfer a Deployment to another Workspace 

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.
2. Click the **Options** menu and select **Transfer Deployment**. 

    ![Transfer Deployment in options menu](/img/docs/transfer-deployment.png)

3. Select the target Workspace where you want to transfer the Deployment. 
4. Click **Transfer Deployment**.