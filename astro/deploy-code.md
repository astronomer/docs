---
sidebar_label: 'Overview'
title: 'Deploy code to Astro'
id: deploy-code
description: Learn about the different ways you can deploy code to Astro.
---

To run your code on Astro, you need to deploy it to a Deployment. You can deploy part or all of an Astro project to an Astro Deployment.

There are three options for deploying code to a Deployment:

- **Project deploys**: Run `astro deploy` to build every non-DAG file in your Astro project as a Docker image and deploy the image to all Airflow components in a Deployment. This includes your `Dockerfile`, plugins, and all Python and OS-level packages. DAGs are deployed separately to each Airflow component through a sidecar container. See [Deploy a project image](deploy-project-image.md).
- **DAG-only deploys**: Run `astro deploy --dags` to deploy only your DAG files to Astro. If you only need to deploy DAG changes, running this command is faster than running `astro deploy` since it does not require installing dependencies. See [Deploy DAGS](deploy-dags.md).
- **Image-only deploys**: Run `astro deploy --image` to build and deploy your Astro project configurations as a Docker image without deploying your DAGs. This is useful you have a multi-repo CI/CD strategy, and you want to deploy your DAGs and project configurations from different repositories or storage buckets. See [Image-only deploys](deploy-dags.md#trigger-an-image-only-deploy)

For each deploy option, you can either trigger the deploy manually or through CI/CD. CI/CD pipelines can include both image deploys and DAG-only deploys, and they can deploy to multiple different Deployments based on different branches in your git repository. See [CI/CD overview](set-up-ci-cd.md).

If multiple deploys are triggered simultaneously or additional deploys are triggered while a deploy is still processing, whether manually or through CI/CD, the first deploy is processed and then the subsequent deploys are completed. This behavior is different from how Astro processes simultaneous code deploys with the [GitHub integration](deploy-github-integration.md#deploys), which cancels the first deploy, and applies the most recent.

## See also

- [Create an Astro project](cli/develop-project.md#create-an-astro-project)
- [Develop your Astro project](cli/develop-project.md)
