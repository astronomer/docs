---
title: 'Manage Astro connections in branch-based deploy workflows'
sidebar_label: 'Connections + Branch-based deploys'
id: use-case-astro-connections
---

Branch-based development is ubiquitous in all modern software development, including data and machine learning engineering. It allows for multiple developers to work on the same codebase at the same time, without interfering with each other's work and rigorous testing of changes before they are merged into production.

Data and machine learning pipelines often interact with a multitude of external systems, such as data warehouses and APIs. When using Airflow, these systems are accessed via [Airflow connections](https://docs.astronomer.io/learn/connections). In a best practice workflow, different connections are used for different environments, such as development and production.  

Astro offers first-class support for [branch-based development](https://docs.astronomer.io/astro/automation-overview) and central and [secure management of connections](https://docs.astronomer.io/astro/manage-connections-variables). 

This use case walks you through setting up a branch-based development and deployment workflow with GitHubActions and Airflow connections managed in Astro.

## Before you start

Before trying this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- An [Astro account](https://www.astronomer.io/try-astro/) with two [Astro Deployments](https://docs.astronomer.io/astro/create-deployment), one for development (`conn-management-demo-dev`) and one for production (`conn-management-demo-prod`).
- A [GitHub account](https://github.com/).
- An account in a SQL-based data warehouse with two distinct databases: one for development (`CONN_DEMO_DEV`), one for production data (`CONN_DEMO_PROD`), each containing an empty schema called `COOKIES`. This example uses a Snowflake account for which a [30-day free trial](https://trial.snowflake.com/?owner=SPN-PID-365384) is available.
- An [AWS account](https://aws.amazon.com/). A [free tier](https://aws.amazon.com/free/) is available and sufficient for this project.

## Step 1: Create your data warehouse connection in the Astro Environment Manager

First, we will create 2 Airflow connections in the Astro Environment Manager for both deployments to inherit.

1. Log into your Astro account and navigate to the Astro Environment Manager. Click the **+ Connection** button to create a new connection.

    ![Screenshot of the Astro UI showing the Astro Environment Manager and the + Connection button.](/img/docs/use-case-astro-connections_conn_one.png)

2. Create a new connection to your data warehouse. We will use Snowflake for this example but any SQL-based data warehouse will work. If no connection type is available for your data warehouse, you can select the type **Generic**.

3. Give the new connection the name `snowflake_conn_management_demo` and fill the connection form with your connection credentials. Make sure to provide the _development_ database to the `DATABASE` field in the connection form, we will override this field later for the production deployment. To make sure this connection is available to all existing and future Deployments in this workspace, toggle switch at the start of the form to **Linked to all**. 

    ![Screenshot of the Connections Config menu in the Astro Environment Manager](/img/docs/use-case-astro-connections_conn_two.png)

4. Click **Create Connection** to save your connection.

5. View the connection in the Astro Environment Manager. You should see the connection listed with the name `snowflake_conn_management_demo` which is applied to `All Deployments` in your workspace.

    ![Screenshot of the Astro Environment Manager with the `snowflake_conn_management_demo`](/img/docs/use-case-astro-connections_conn_all_deployments.png)

## Step 2: Override a connection field for a specific deployment

Currently the `snowflake_conn_management_demo` connection points to the development database for all Deployments in your workspace. In this step, we will override the `DATABASE` field for the production deployment to point to the production database.

1. In the Astro Environment Manager, click on the `snowflake_conn_management_demo` connection to open the connection details. You will see a list of all Deployments this connection is available to. Since we linked this connection to all Deployments in the workspace, you should see all Deployments of this workspace listed. Click on the **Edit** button for the `prod` deployment to override fields for this deployment.

    ![Screenshot of the connection details view with the **Edit** button for the prod deployment highlighted.](/img/docs/use-case-astro-connections_conn_override_one.png)

2. Change the `DATABASE` field to your production database. The new value will override the default you defined for the connection in Step 1.3.

    ![Screenshot of the connection details view with the DATABASE field highlighted.](/img/docs/use-case-astro-connections_conn_override_two.png)

3. Click **Update Connection Link** to save your changes. The connection details view will now show the number of overrides for this connection when applied to the `prod` deployment.

    ![Screenshot of the connection details view with the overrides highlighted.](/img/docs/use-case-astro-connections_conn_override_three.png)

## Step 3: Create your AWS connection in the Astro Environment Manager

Next, we will create an Airflow connection to AWS in the Astro Environment Manager.

1. Click the **+ Connection** button to create a new connection.

2. Create a new connection to AWS. This time, select the `AWS` connection type.

3. Give the new connection the name `aws_conn_management_demo` and fill the connection form with your connection credentials. We want this connection to only be available to deployments we explicitly link it to, so make sure to leave the switch at the start of the form at **Restricted**.

    ![Screenshot of the Connections Config menu in the Astro Environment Manager](/img/docs/use-case-astro-connections_conn_aws.png)

4. Click **Create Connection** to save your connection.

5. View the connection in the Astro Environment Manager. You should see the connection listed with the name `aws_conn_management_demo` which is currently available to `0 Deployments` in your workspace.

    ![Screenshot of the Astro Environment Manager with the `aws_conn_management_demo`](/img/docs/use-case-astro-connections_conn_zero_deployments.png)

## Step 4: Link the AWS connection to your Deployments

Now that we have created the AWS connection, we will link it to the `Dev` and `Prod` deployments. Remember that we set the connection to **Restricted** in Step 3.3, so it is not available to any deployments by default.

1. In the Astro Environment Manager, click on the `aws_conn_management_demo` connection to open the connection details. You will see a list of all Deployments this connection is available to. Since we set the connection to **Restricted**, you should see no Deployments listed. Click on the **+ Link Deployment** button to link the connection to a Deployment.

    ![Screenshot of the connection details view with the **Link Deployment** button highlighted.](/img/docs/use-case-astro-connections_conn_link_deployment_one.png)

2. Select your `dev` Deployment and link the connection. In this step it would also be possible to override fields, but we will leave the connection as is. Click **Link connection** to save your changes.

    ![Screenshot of the connection link to deployment form.](/img/docs/use-case-astro-connections_conn_link_deployment_two.png)

3. Repeat the previous step for the `prod` Deployment. Now both Deployments should be listed in the connection details view.

    ![Screenshot of the connection details view with the two linked deployments highlighted.](/img/docs/use-case-astro-connections_conn_link_deployment_three.png)

