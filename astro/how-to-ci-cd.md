---
sidebar_label: 'How to Setup CI/CD'
title: 'How to Setup CI/CD to Manage your Astronomer Deployments'
id: how-to-ci-cd
---

<head>
  <meta name="description" content="This document will guide ypu through the various options for seting up a CI/CD pipeline with Astronomer tooling and give recommendations along the way." />
  <meta name="og:description" content="This document will guide ypu through the various options for seting up a CI/CD pipeline with Astronomer tooling and give recommendations along the way." />
</head>

# How to Setup CI/CD to Manage your Astronomer Deployments

You can deploy improvements to data pipelines running on Astronomer with CI/CD Pipelines. The following document will walk you through how to set up a CI/CD pipeline with Astronomer tooling and give recommendations along the way.

# Prerequisites

The first step to managing your code deploys with CI/CD is to [set up an Astro project](https://docs.astronomer.io/astro/create-project) with the [Astro CLI](https://docs.astronomer.io/astro/cli/overview). Once you have your project set up, push it to a Github repository or equivalent. We recommend that users manage one Astro Project with one repository. However, it is common for organizations to use multiple repositories and to deploy code from one Astro project to multiple Astronomer Deployments. For example, you may have separate deployments based on the same project for development, staging, production, and new features. We recommend that you manage these deployments by creating a [Git branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches) for each one.

# Settings up an Astro Project Repository

You may want to set up your Astro Project Repository and CI/CD pipelines in different ways based on your organization's goals and requirements. We will cover the three most popular project structures:

- Traditional Astro Project
- Multi Repository Project
- S3 Bucket + Repository Project(for users coming from MWAA)

## Traditional Astro Project

In the traditional Astro project, you manage the files making up a project in one repository. To create this project, you need to push up a project made with the Astro CLI command `[astro dev init](https://docs.astronomer.io/astro/cli/astro-dev-init)` to a Github repository or equivalent git-based management system. This structure is easy to understand and set up. You can go to a single repository for a quick overview of the current state of your Astro project and manage your DAG folder and image in one place. We recommend that our users use this project structure, but we recognize that it does not fit every organization’s needs.

```bash
Tradtional Astro Project Repository structure:
├── dags # Where your DAGs go
│   └── example-dag-basic.py # Example DAG that showcases a simple ETL data pipeline
|   └── example-dag-advanced.py # Example DAG that showcases more advanced Airflow features, such as the TaskFlow API
├── Dockerfile # For the Astro Runtime Docker image, environment variables, and overrides
├── include # For any other files you'd like to include
├── plugins # For any custom or community Airflow plugins
|   └── example-plugin.py
├── tests # For any DAG unit test files to be run with pytest
|   └── test_dag_integrity.py # Test that checks for basic errors in your DAGs
├── airflow_settings.yaml # For your Airflow connections, variables and pools (local only)
├── packages.txt # For OS-level packages
└── requirements.txt # For Python packages
```

## Multi-Repository Project

In a multi-repository project, an organization can manage the DAG folder in one repository and the image in another. This project structure allows admins to separate the management of these aspects so that only users that need access to these repositories can access them. One drawback to this structure is that you must keep your local projects in sync with both repositories to simulate your deployments. Your team members may end up with inconsistencies in their local deployments. Setting up a development deployment can help your team work out these inconsistencies.

To set up a CI/CD pipeline with a multi-repository project, you need to have [dag-deploy enabled](https://docs.astronomer.io/astro/deploy-code#enable-dag-only-deploys-on-a-deployment) on your deployments and setup [dag-deploy CI/CD pipeline](https://docs.astronomer.io/astro/ci-cd#dag-based-workflows) setup on both repositories. Our dag-deploy templates will push DAG code and image code separately by default.

## S3 Bucket + Repository Project

Similar to the multi-repository project, the S3 bucket + repository project separates the management of the DAGs folder and image files. You can manage the DAGs folder within an [S3 bucket](https://aws.amazon.com/s3/) and the image files within Github(or equivalent) repository. 

MWAA users drop DAG files into an S3 bucket to update deployments. For this reason, organizations moving DAGs from MWAA may prefer this structure. We can set up a lambda function for your organization that will send your dags to an Astronomer deployment whenever DAG files are updated or added to a specific S3 bucket.

# CI/CD Tooling & Pipeline Basics

Once you set up your Astro project in a repository, you can create a CI/CD pipeline. An Astro Project’s CI/CD pipeline will push code changes to a specific deployment. These include changes to your DAGs, python requirements, Airflow settings, and Dockerfile. We recommend you use CI/CD to push code changes to your deployments to ensure that you deploy your code from one source(Astro Project Repository). This way, you can ensure that code running in your deployments is version controlled through git.

Astronomer provides tools to do this in two different ways. You can use our custom [Github Actions(deploy-action)](https://github.com/astronomer/deploy-action) or use the [Astro CLI](https://docs.astronomer.io/astro/cli/overview) to create a deploy script with any CI/CD tool of your choice. The basis of these options is the Astro CLI command `[astro deploy](https://docs.astronomer.io/astro/cli/astro-deploy)`.

If you are storing your Astro project in a Github project, the easiest way to set up a pipeline is to add our custom Github Action script to your repository. Create a custom script with the Astro CLI if your pipeline needs functionality our custom action does not provide or if you’d like to use a different CI/CD tool. We have plenty of [example scripts and pipelines](https://docs.astronomer.io/astro/ci-cd) for you to follow.

# Dag Deploys vs Image Deploys

Traditionally deploying code to Astronomer involves using Docker(or equivalent) to perform an [image deploy](https://docs.astronomer.io/astro/ci-cd#image-only-workflows). An image deploy will build your Astro project into a docker image, optionally test the DAGs/python code, push it to Astronomer’s image registry, and deploy it to your deployment. Running the CLI command `[astro deploy](https://docs.astronomer.io/astro/cli/astro-deploy)` in the root of your project directory will trigger an image deploy.

Recently we have introduced the ability to deploy DAG code without creating a docker image with `astro deploy --dags`. We recommend that you configure your CI/CD pipelines to use this feature. This makes your pipelines faster and more efficient. Read our [Deploy DAGs only documentation](https://docs.astronomer.io/astro/deploy-code#deploy-dags-only) to learn more about enabling DAG-only Deploys for your deployments and using it in your CI/CD pipelines.

# Picking a CI/CD Template

Once you have picked a CI/CD tool to run your pipeline, you are ready to choose from one of our CI/CD templates. We have examples of our basic [one-branch deploy template](https://docs.astronomer.io/astro/ci-cd?tab=standard#github-actions-dag-based-deploy) for a variety of CI/CD tooling. This template will push code to a deployment when you merge it into a specific branch. For our [Github Actions](https://docs.github.com/en/actions) templates, we also give two other Github Actions templates multi-branch deploy and [custom image deploy](https://docs.astronomer.io/astro/ci-cd?tab=custom#github-actions-dag-based-deploy). These templates can be used as examples to build CI/CD pipelines in other tools.

You will likely want to set up your CI/CD pipeline as multi-branch deploy. This template deploys your code to a specific deployment based on what branch you push changes. For example, code pushed to a development branch will be pushed to a development Deployment, and so on. This way you can test DAG changes and new DAGs in a development deployment rather than a production one.

The [custom image deploy templates](https://docs.astronomer.io/astro/ci-cd?tab=custom#github-actions-dag-based-deploy) shows how to create a CI/CD pipeline that deploys a custom image during image deploys. If you’d like to use [docker build](https://docs.docker.com/engine/reference/commandline/build/) features such as SSH and build args to build your image, you will need to create your image with a custom docker build command and then deploy it to your deployment. See custom image templates for information.

# Testing and Validating DAGs During CI/CD

You may consider validating and testing your DAG code before deploying it to your Deployment.

Astronomer provides [tooling](https://docs.astronomer.io/astro/test-and-troubleshoot-locally#test-dags-with-the-astro-cli) to validate that your DAGs do not have import or syntax errors. You can implement this parse test with the [Astro CLI](https://docs.astronomer.io/astro/cli/astro-dev-parse) or the [Deploy-Action](https://github.com/astronomer/deploy-action). The default test may not work on all DAGs, especially if they access the meta-database at runtime (a common anti-pattern). In this case, you can write your own parse test using our example pytests.

Astronomer also provides tooling to run [custom Pytests](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#unit-tests) on your DAG code, python methods, and custom operators. The [Astro CLI](https://docs.astronomer.io/astro/cli/astro-dev-pytest) and [Deploy-Action](https://github.com/astronomer/deploy-action#example-using-pytests) will use docker to spin up a docker container that has a similar environment to your deployment and executes your Pytests. We recommend that you pytest any custom python code you use in your DAGs.

# Conclusion

Now you should know the basics of creating a CI/CD pipeline for an Astronomer Deployment. If you’d like help customizing your CI/CD pipelines for your specific use case, feel free to reach out to Astronomer support