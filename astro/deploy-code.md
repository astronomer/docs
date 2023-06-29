---
sidebar_label: 'Overview'
title: 'Deploy code to Astro'
id: deploy-code
description: Learn about the different ways you can deploy code to Astro.
---

To run your code on Astro, you need to deploy it to a Deployment. You can deploy part or all of an Astro project to an Astro Deployment.

There are three common patterns for deploying code to a Deployment:

- **Project deploys**: Run `astro deploy` to build every file in your Astro project as a Docker image and deploys the image to all Airflow components in a Deployment. This includes your `Dockerfile`, DAGs, plugins, and all Python and OS-level packages. See [Deploy a project](deploy-project.md).
- **DAG-only deploys**: Run `astro deploy --dags` to deploy only your DAG files to Astro. If you only need to deploy DAG changes, running this command is faster than running `astro deploy` since it does not require installing dependencies. See [Deploy DAGS](deploy-dags.md).
- **CI/CD deploys**: Depending on the use case, CI/CD deploys combine project deploys and DAG-only deploys as an automated process. CI/CD pipelines can deploy to multiple different Deployments based on different branches in your git repository. See [CI/CD overview](set-up-ci-cd.md).


## See also

- [Create an Astro project](create-project.md)
- [Develop your Astro project](develop-project.md)
