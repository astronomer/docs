---
sidebar_label: 'Deploy DAGs'
title: 'Deploy DAGs to Astro'
id: deploy-dags
description: Learn about the different ways you can deploy code to Astro.
---

DAG-only deploys are the fastest way to deploy code to Astro. They are recommended if you only need to deploy changes made to the `dags` directory of your Astro project.

DAG-only deploys are enabled by default on all Deployments on Astro Hosted. When they are enabled, you must still [deploy your project image](deploy-project-image.md) when you make a change to any file in your Astro project that is not in the `dags` directory, or when you [upgrade Astro Runtime](upgrade-runtime.md).

DAG-only deploys have the following benefits:

- DAG-only deploys are significantly faster than project deploys.
- Deployments pick up DAG-only deploys without restarting. This results in a more efficient use of workers and no downtime for your Deployments.
- If you have a CI/CD process that includes both DAG and image-based deploys, you can use your repository's permissions to control which users can perform which kinds of deploys. See [DAG deploy templates](https://docs.astronomer.io/astro/ci-cd-templates/template-overview#dag-deploy-templates) for how you can set this up in your CI/CD pipelines.
- You can use DAG deploys to update your DAGs when you have slow upload speed on your internet connection.

## Trigger a DAG-only deploy

Triggering a DAG-only deploy pushes DAGs to Astro and mounts them to the workers and schedulers in your Deployment. DAG-only deploys do not disrupt running tasks and do not cause any components to restart when you push code. If you deploy changes to a DAG that is currently running, active task runs finish executing according to the code from before you triggered a deploy. New task runs are scheduled using the code from your latest deploy.

Run the following command to deploy only your `dags` directory to a Deployment:

```sh
astro deploy --dags
```

## Trigger an image-only deploy

Even if you primarily use DAG-only deploys, you still need to occasionally make image deploys to update your Astro runtime version or install dependencies. However, depending on your CI/CD strategy, triggering a full project deploy with `astro deploy` might affect your existing DAGs.

When you trigger an image-only deploy, it builds every non-DAG file in your Astro project as a Docker image and deploys the image to all Airflow components in a Deployment. This includes your `Dockerfile`, plugins, and all Python and OS-level packages. DAGs are not deployed, and your Deployment DAG folder and DAG bundle version are not affected. Image-only deploys are only available when you have DAGs-only deploys enabled.

Run the following command to build and deploy only your non-DAG files to a Deployment:

```sh
astro deploy --image
```

:::tip

If you use [prebuilt Docker images](deploy-project-image.md#deploy-a-prebuilt-docker-image) for your image deploys, you can use both the `--image-name` and `--image` flags to update your image without updating your `dags` folder.

:::

## Enable or disable DAG-only deploys on a Deployment

If you have Workspace Owner permissions, you can enable or disable DAG-only deploys for a Deployment at any time. After you disable DAG-only deploys and trigger a code deploy:

- Any changes to your DAG code are deployed as part of your Astro project Docker image.
- Your Deployment no longer includes Azure Blob Storage or DAG downloading sidecars.
- In the Cloud UI, your Deployment **DAG bundle version** will not update when you deploy code.

To determine if turning off DAG-only deploy functionality is the right choice for your organization, contact [Astronomer support](https://cloud.astronomer.io/open-support-request).

Before you enable or disable DAG-only deploys on a Deployment, ensure the following:

- You have access to the latest version of your Deployment's Astro project.
- You can update your Deployment using the Astro CLI.

:::warning

Carefully read and complete all of the following steps to ensure that disabling or enabling DAG-only deploys doesn't disrupt your Deployment. **Immediately after you update the setting, you must trigger an image deploy to your Astro Deployment using `astro deploy`.** If you don't complete this step, you can't access your DAGs in the Airflow UI.

:::

### Prerequisites

Before you enable or disable DAG-only deploys on a Deployment, ensure the following:

- You have Workspace Owner permissions for the Workspace that hosts the Deployment.
- You have access to the latest version of your Deployment's Astro project.
- You can update your Deployment using the Astro CLI.

### Enable DAG-only deploys

DAG-only deploys are enabled by default on Astro Hosted. You have the option to enable DAG-only deploys only if you're on Astro Hybrid or if you've previously disabled them on a Hosted Deployment. After you enable DAG-only deploys:

- You can run `astro deploy --dags` to deploy only DAGs to your Deployment.
- In the Cloud UI, your Deployment **DAG bundle version** updates when you trigger an image deploy or a DAG-only deploy.
- When you only deploy DAGs, it does not automatically upgrade your Runtime version. You must periodically complete a full image deploy to [upgrade the Runtime version](upgrade-runtime.md).
- Your Deployment includes infrastructure for deploying your DAGs separately from your project image. See [What happens during a code deploy](deploy-project-image.md#what-happens-during-a-project-deploy).

1. Run the following command to enable DAG-only deploys:

    ```sh
    astro deployment update --dag-deploy enable
    ```

2. Run the following command to deploy all of the files in your Astro project as a Docker image:

    ```sh
    astro deploy
    ```

### Disable DAG-only deploys

After you disable DAG-only deploys:

- You can't run `astro deploy --dags` to trigger a DAG-only deploy to your Deployment.
- Any changes to your DAG code are deployed as part of your Astro project Docker image.
- In the Cloud UI, your Deployment **DAG bundle version** doesn't update when you deploy code.
- Your Deployment doesn't include infrastructure for deploying your DAGs separately from your project image. See [What happens during a code deploy](deploy-project-image.md#what-happens-during-a-project-deploy).

1. Run the following command to disable DAG-only deploys:

    ```sh
    astro deployment update --dag-deploy disable
    ```

2. Run the following command to deploy all of the files in your Astro project as a Docker image:

    ```sh
    astro deploy
    ```