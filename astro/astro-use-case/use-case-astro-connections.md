---
title: 'Manage Astro connections in branch-based deploy workflows'
sidebar_label: 'Connections + Branch-based deploys'
id: use-case-astro-connections
---

Branch-based development is ubiquitous in all modern software development, including data engineering and machine learning operations. It allows for multiple developers to work on the same codebase at the same time without interfering with each other's work, and for applying rigorous testing of changes before they are merged into production.

Data pipelines often interact with a multitude of external systems, such as data warehouses and APIs. When using Airflow, these systems are accessed via [Airflow connections](https://docs.astronomer.io/learn/connections). In a best practice workflow, different connections are used for different environments, such as development and production.  

Astro offers first-class support for [branch-based development](https://docs.astronomer.io/astro/automation-overview) and central and [secure management of connections](https://docs.astronomer.io/astro/manage-connections-variables). 

This use case walks you through setting up a branch-based deployment workflow with [GitHub Actions](https://docs.github.com/en/actions) and Airflow connections managed in Astro for a small example project that ingests cookie recipes from S3 into Snowflake. 

## Before you start

Before trying this example, make sure you have:

- The [Astro CLI](https://docs.astronomer.io/astro/cli/overview).
- An [Astro account](https://www.astronomer.io/try-astro/) with two [Astro Deployments](https://docs.astronomer.io/astro/create-deployment). 
- A [GitHub account](https://github.com/).
- An account in a SQL-based data warehouse. This example uses a Snowflake account for which a [30-day free trial](https://trial.snowflake.com/?owner=SPN-PID-365384) is available. 
- An account in an object storage solution. This example uses an [AWS account](https://aws.amazon.com/). A [free tier](https://aws.amazon.com/free/) is available and sufficient for this project.

If you want to use other data warehouse or object storage solutions than Snowflake and AWS, you will need to adapt the example code accordingly and add the relevant [Airflow provider](https://registry.astronomer.io/providers) packages to the `requirements.txt` file of the Astro project.

:::info

In this example we used the following names for the Deployments and databases. You can use different names, but make sure to update the example code accordingly.

- `conn-management-demo-dev`: The development Astro Deployment.
- `conn-management-demo-prod`: The production Astro Deployment.
- `CONN_DEMO_DEV`: The development Snowflake database.
- `CONN_DEMO_PROD`: The production Snowflake database.
- `COOKIES`: An empty schema present in the both Snowflake databases.

:::

## Part 1: Set up Airflow connections on Astro

The first part of this example shows how to set up Airflow connections on Astro and make them available to multiple Deployments.

### Step 1: Create your data warehouse connection in the Astro Environment Manager

First, we create 2 Airflow connections in the Astro Environment Manager for both deployments to inherit.

1. Log into your Astro account and navigate to the Astro Environment Manager. Click the **+ Connection** button to create a new connection.

    ![Screenshot of the Astro UI showing the Astro Environment Manager and the + Connection button.](/img/docs/use-case-astro-connections_conn_one.png)

2. Create a new connection to your data warehouse. We use Snowflake for this example, but you can use any SQL-based data warehouse. If no connection type is available for your data warehouse, you can select the type **Generic**.

3. Give the new connection the name `snowflake_conn_management_demo` and fill the connection form with your connection credentials. Make sure to provide the _development_ database to the `DATABASE` field in the connection form, we override this field later for the production deployment. To make sure this connection is available to all existing and future Deployments in this workspace, toggle switch at the start of the form to **Linked to all**. 

    ![Screenshot of the Connections Config menu in the Astro Environment Manager](/img/docs/use-case-astro-connections_conn_two.png)

4. Click **Create Connection** to save your connection.

5. View the connection in the Astro Environment Manager. You should see the connection listed with the name `snowflake_conn_management_demo` which is applied to `All Deployments` in your workspace.

    ![Screenshot of the Astro Environment Manager with the `snowflake_conn_management_demo`](/img/docs/use-case-astro-connections_conn_all_deployments.png)

:::info

Note that to be able to use a connection defined in the Astro Environment manager in a Deployment, the relevant [Airflow provider](https://registry.astronomer.io/providers) package needs to be installed in that deployment.

:::

### Step 2: Override a connection field for a specific deployment

Currently the `snowflake_conn_management_demo` connection points to the development database for all Deployments in your workspace. In this step, we override the `DATABASE` field for the production deployment to point to the production database. This feature allow you to define a single connection with one connection ID that is available to multiple Deployments, but optionally with different connection fields. Enabling you to use the same connection ID in your DAGs without having to change the code when deploying to different environments.

1. In the Astro Environment Manager, click on the `snowflake_conn_management_demo` connection to open the connection details. You see a list of all Deployments this connection is available to. Since we linked this connection to all Deployments in the workspace, you should see all Deployments of this workspace listed. Click on the **Edit** button for the `conn-management-demo-prod` deployment to override fields for this deployment.

    ![Screenshot of the connection details view with the **Edit** button for the conn-management-demo-prod deployment highlighted.](/img/docs/use-case-astro-connections_conn_override_one.png)

2. Change the `DATABASE` field to your production database. The new value overrides the default you defined for the connection in [Step 1](#step-1-create-your-data-warehouse-connection-in-the-astro-environment-manager).

    ![Screenshot of the connection details view with the DATABASE field highlighted.](/img/docs/use-case-astro-connections_conn_override_two.png)

3. Click **Update Connection Link** to save your changes. The connection details view now shows the number of overrides for this connection when applied to the `conn-management-demo-prod` deployment.

    ![Screenshot of the connection details view with the overrides highlighted.](/img/docs/use-case-astro-connections_conn_override_three.png)

### Step 3: Create your AWS connection in the Astro Environment Manager

Next, we create an Airflow connection to AWS in the Astro Environment Manager.

1. Click the **+ Connection** button to create a new connection.

2. Create a new connection to AWS. This time, select the `AWS` connection type.

3. Give the new connection the name `aws_conn_management_demo` and fill the connection form with your connection credentials. We want this connection to only be available to deployments we explicitly link it to, so make sure to leave the switch at the start of the form at **Restricted**.

    ![Screenshot of the Connections Config menu in the Astro Environment Manager](/img/docs/use-case-astro-connections_conn_aws.png)

4. Click **Create Connection** to save your connection.

5. View the connection in the Astro Environment Manager. You should see the connection listed with the name `aws_conn_management_demo` which is currently available to `0 Deployments` in your workspace.

    ![Screenshot of the Astro Environment Manager with the `aws_conn_management_demo`](/img/docs/use-case-astro-connections_conn_zero_deployments.png)

### Step 4: Link the AWS connection to your Deployments

Now that we have created the AWS connection, we link it to the `conn-management-demo-dev` and `conn-management-demo-prod` deployments. Remember that we set the connection to **Restricted** in [Step 3](#step-3-create-your-aws-connection-in-the-astro-environment-manager), so it is not available to any deployments by default.

1. In the Astro Environment Manager, click on the `aws_conn_management_demo` connection to open the connection details. You see a list of all Deployments this connection is available to. Since we set the connection to **Restricted**, you should see no Deployments listed. Click on the **+ Link Deployment** button to link the connection to a Deployment.

    ![Screenshot of the connection details view with the **Link Deployment** button highlighted.](/img/docs/use-case-astro-connections_conn_link_deployment_one.png)

2. Select your `conn-management-demo-dev` Deployment and link the connection. In this step it would also be possible to override fields, but we leave the connection as is. Click **Link connection** to save your changes.

    ![Screenshot of the connection link to deployment form.](/img/docs/use-case-astro-connections_conn_link_deployment_two.png)

3. Repeat the previous step for the `conn-management-demo-prod` Deployment. Now both Deployments should be listed in the connection details view.

    ![Screenshot of the connection details view with the two linked deployments highlighted.](/img/docs/use-case-astro-connections_conn_link_deployment_three.png)

## Part 2: Set up branch-based deploys with GitHub Actions

After setting up the connections, we create an automated two branch CI/CD workflow for a small sample project that uses both connections defined in [Part 1](#part-1-set-up-airflow-connections-on-astro).

### Step 5: Create your GitHub repository

1. Go to the [Astronomer GitHub](https://github.com/astronomer/ce-conn-management-demo) and [fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo) to your own GitHub account. This repository contains a small sample project ingesting data from S3 into Snowflake, using the connections defined in [Part 1](#part-1-set-up-airflow-connections-on-astro).

2. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the forked repository to your local machine.

3. On your local machine, navigate to the cloned repository directory and create a new branch called `dev`:

    ```sh
    git checkout -B dev
    ```

4. Push the new branch to your GitHub repository:

    ```sh
    git push origin dev
    ```

You should now have a GitHub repository with two branches: `main` and `dev` that contain the same code.

### Step 6: Configure GitHub Actions workflow

The repository already has [a GitHub Actions script](https://github.com/astronomer/ce-conn-management-demo/blob/main/.github/workflows/deploy_to_astro.yaml) defined to run the CI/CD workflow to deploy changes to Astro. Any push to the `dev` branch triggers the workflow to deploy the code to the `conn-management-demo-dev` Deployment. Any merged PR to the `main` branch triggers the workflow to deploy the code to the `conn-management-demo-prod` Deployment.

To configure the workflow for your own Astro account, you need to set two [GitHub Action Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository) and two [GitHub Action variables](https://docs.github.com/en/actions/learn-github-actions/variables#creating-configuration-variables-for-a-repository) in your repository.

1. Configure the following GitHub Action Secrets in your repository:

    - `DEV_ASTRO_API_TOKEN`: The API token of your development Deployment (`conn-management-demo-dev`). You can create Deployment API tokens in the Astro UI, see [Create and manage Deployment API tokens](https://docs.astronomer.io/astro/deployment-api-tokens).
    - `PROD_ASTRO_API_TOKEN`: The API token of your production Deployment (`conn-management-demo-prod`).

    ![Screenshot of the GitHub Actions secrets menu.](/img/docs/use-case-astro-connections_gh_secrets.png)

2. Configure the following GitHub Action variables in your repository:

    - `DEV_ASTRO_DEPLOYMENT_ID`: The id of your development Deployment (`conn-management-demo-dev`). The deployment id can be found in the Astro UI and is in the form of `cabcdef123456789abcdefghi1ab`.
    - `PROD_ASTRO_DEPLOYMENT_ID`: The id of your production Deployment (`conn-management-demo-prod`).

    ![Screenshot of the GitHub Action variables menu.](/img/docs/use-case-astro-connections_gh_variables.png)

### Step 7: Trigger the branch-based deploy workflow

Now that the workflow is configured, you can trigger it by pushing changes to the `dev` branch.

1. Make a small change to the [`collect_cookie_recipes` DAG](https://github.com/astronomer/ce-conn-management-demo/blob/main/dags/collect_cookie_recipes.py), for example by adding a comment.

2. Commit and push the changes to the `dev` branch:

    ```sh
    git add dags/collect_cookie_recipes.py
    git commit -m "Add comment to DAG"
    git push origin dev
    ```

3. Navigate to the **Actions** tab in your GitHub repository. You should see a new workflow run triggered by the push to the `dev` branch.

    ![Screenshot of the GitHub Actions workflow run.](/img/docs/use-case-astro-connections_gh_workflow_dev.png)


4. Create a [pull request](https://docs.github.com/en/pull-requests) from your `dev` to your `main` branch and merge it. This triggers the workflow to deploy the code to the `conn-management-demo-prod` Deployment.

## Part 3: Run the DAGs

Lastly we run the DAGs without needing to change any code or set up any connections in the Airflow UI.

### Step 8: Run the DAGs on Astro

The GitHub Actions workflow triggered in [Step 7](#step-7-trigger-the-branch-based-deploy-workflow) deploys the Astro project to the `conn-management-demo-dev` and `conn-management-demo-prod` Deployments. Now you can run the DAGs on Astro.

1. Navigate to the Astro UI and open the `conn-management-demo-dev` Deployment. Run the `upload_cookie_recipes` helper DAG to upload the sample data from [`include/recipes.json`](https://github.com/astronomer/ce-conn-management-demo/blob/main/include/recipes.json) to S3. The DAG uses the `aws_conn_management_demo` connection defined in [Step 1](#step-1-create-your-data-warehouse-connection-in-the-astro-environment-manager) to access S3.

    ![Screenshot of the Astro UI showing the DAG run for the upload_cookie_recipes DAG.](/img/docs/use-case-astro-connections_upload_dag.png)

2. Run the `collect_cookie_recipes` DAG to ingest the data from S3 into Snowflake. The `conn-management-demo-dev` Deployment uses the `snowflake_conn_management_demo` connection defined in [Step 1](#step-1-create-your-data-warehouse-connection-in-the-astro-environment-manager) to access Snowflake. Without any overrides this connection points to the `CONN_DEMO_DEV` database in Snowflake.

    ![Screenshot of the Astro UI showing the DAG run for the collect_cookie_recipes DAG.](/img/docs/use-case-astro-connections_collect_dag.png)

3. View the data in Snowflake. The `collect_cookie_recipes` DAG ingested the cookie recipes into the `COOKIES` schema in the `CONN_DEMO_DEV` database.

    ![Screenshot of the Snowflake UI showing the COOKIES_RECIPE table in the CONN_DEMO_DEV database.](/img/docs/use-case-astro-connections_snowflake.png)

4. Repeat the steps above for the `conn-management-demo-prod` deployment. Due to the override defined in [Step 2](#step-2-override-a-connection-field-for-a-specific-deployment), the `snowflake_conn_management_demo` connection points to the `CONN_DEMO_PROD` database in Snowflake, where you can view the `COOKIES_RECIPES` table with the ingested data.

### Step 9: (Optional) Run the DAGs locally

You can use the connections defined in the Astro Environment Manager when running the DAGs locally with the Astro CLI. This feature allows you to enable data professionals in your organization to use default connections without having to share connection configuration details or secrets. See also [Import and export Airflow connections and variables](https://docs.astronomer.io/astro/import-export-connections-variables).

1. In the Astro UI navigate to the `ORGANIZATION SETTINGS` of your organization and click **Edit Details**. Click the toggle to enable `ENVIRONMENT SECRETS FETCHING` and **Update Organization** so save your changes.

    ![Screenshot of the Astro UI showing the organization settings Edit Details button.](/img/docs/use-case-astro-connections_organization_edit_2.png)

2. Make sure you are logged into your Astro account with the Astro CLI by running the following command and authenticating with your Astro credentials:

    ```sh
    astro login
    ```

3. Enable local development access to connections created in the Astro Environment Manager by running the following command:

    ```sh
    astro config set -g disable_env_objects false
    ```

4. Find your workspace id by running:

    ```sh 
    astro workspace list
    ```

5. Start a local Airflow instance with the set of the connections defined for your workspace by running the following command:

    ```sh
    astro dev start --workspace-id [workspace-id]
    ```

    You can view which connections were fetched from the Cloud in the console logs.

    ```text
    Airflow is starting up!
    Added Connection: snowflake_conn_management_demo
    Added Connection: aws_conn_management_demo

    Project is running! All components are now available.

    Airflow Webserver: http://localhost:8080
    Postgres Database: localhost:5432/postgres
    The default Airflow UI credentials are: admin:admin
    The default Postgres DB credentials are: postgres:postgres
    ```

5. Run the `collect_cookie_recipes` DAG locally to confirm the connections were imported correctly.

Congratulations! You have successfully set up Airflow connections on Astro and created a branch-based CI/CD workflow with GitHub Actions. You can now use this workflow as a template for your own projects.

## See also

- Documentation: [Manage Airflow connections and variables](https://docs.astronomer.io/astro/manage-connections-variables) on Astro.
- Documentations: [Automate actions on Astro](https://docs.astronomer.io/astro/automation-overview)
- Guide: [Manage Airflow connections](https://docs.astronomer.io/learn/connections).