---
sidebar_label: 'Deploy DAGs'
title: 'Deploy DAGs to Astro'
id: deploy-dags
description: Learn about the different ways you can deploy code to Astro.
---

DAG-only deploys are the fastest way to deploy code to Astro. They are recommended if you only need to deploy changes made to the `dags` directory of your Astro project.

To push only DAGs to Astro, you must enable the feature for each Deployment. You only need to enable the feature once. After it is enabled, you must still [deploy your project image](deploy-project-image.md) when you make a change to any file in your Astro project that is not in the `dags` directory.

Enabling DAG-only deploys on Astro has a few benefits:

- DAG-only deploys are significantly faster than project deploys.
- Deployments pick up DAG-only deploys without restarting. This results in a more efficient use of workers and no downtime for your Deployments.
- If you have a CI/CD process that includes both DAG and image-based deploys, you can use your repository's permissions to control which users can perform which kinds of deploys. See [DAG-based templates](https://docs.astronomer.io/astro/ci-cd-templates/template-overview#dag-based-templates) for how you can set this up in your CI/CD pipelines.
- You can use DAG deploys to update your DAGs when you have slow upload speed on your internet connection.

## Enable DAG-only deploys on a Deployment

Before you enable DAG-only deploys on a Deployment, ensure that you have access to the Deployment's Astro project and can trigger deploys from your current machine with the Astro CLI. You cannot enable the DAG-only deploy feature in the Cloud UI.

1. Open your Deployment's Astro project.
2. Run the following command to enable the feature on your Deployment:

    ```sh
    astro deployment update --dag-deploy enable
    ```

3. When the prompt appears in the Astro CLI, select the Deployment where you want to enable the feature. Running tasks will not be interrupted, but new tasks will not be scheduled until you trigger your first DAG-only deploy.
4. Run the following command to finalize the setup and trigger a DAG-only deploy to your Deployment:  

    ```sh
    astro deploy --dags
    ```

    If you don't trigger a deploy after enabling the feature, your Deployment cannot schedule new tasks.

5. (Optional) Open your Deployment in the Cloud UI. Confirm your deploy was successful by checking the Deployment's **DAG Bundle Version**. The version name should include the date and time that you triggered the deploy.

## Trigger a DAG-only deploy

Triggering a DAG-only deploy pushes DAGs to Astro and mounts them to the workers and schedulers in your Deployment. DAG-only deploys do not disrupt running tasks and do not cause any components to restart when you push code. If you deploy changes to a DAG that is currently running, active task runs finish executing according to the code from before you triggered a deploy. New task runs are scheduled using the code from your latest deploy.

Run the following command to deploy only your `dags` directory to a Deployment:

```sh
astro deploy --dags
```

## Disable DAG-only deploys on a Deployment

If you have Workspace Admin permissions, you can turn off DAG-only deploys for a Deployment at any time if your organization doesn't benefit from faster deploys or prefers a deployment method that is exclusively based on building and deploying your Astro project as a Docker image. To determine if turning off DAG-only deploy functionality is the right choice for your organization, contact [Astronomer support](https://cloud.astronomer.io/support). 

When you turn off DAG-only deploys, your DAGs might not reappear in the Airflow UI until you trigger a deploy. To make sure you can continue to access to your data, trigger an image deploy to Astro immediately after you turn off the DAG-only deploy feature. 

1. Run the following command to turn off DAG-only deploys:

    ```sh
    astro deployment update --dag-deploy disable
    ```

2. Run the following command to deploy all of the files in your Astro project as a Docker image:

    ```sh
    astro deploy
    ```