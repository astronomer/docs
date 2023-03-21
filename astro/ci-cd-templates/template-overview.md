---
sidebar_label: Template overview
title: Astro Cloud IDE
id: template-overview
description: Use pre-built templates to get started with automating code Deploys 
---

Use the Astronomer CI/CD templates to automate code deployment to Astro with popular CI/CD management tools, including GitHub Actions and Circle CI. This document contains information about each general template type, including how each template is implemented.

To decide which template is right for you and to learn more about CI/CD use cases, see [Set up CI/CD](set-up-ci-cd.md).

## Prerequisites

- A deploy strategy for your CI/CD pipeline. See [Set up CI/CD](set-up-ci-cd.md).
- A [Deployment API key ID and secret](api-keys.md).
- A CI/CD management tool, such as [GitHub Actions](https://docs.github.com/en/actions).
- An [Astro project](create-project.md) that is hosted in a place that your CI/CD tool can access.

## Template types

Templates allow you to configure automated workflows using popular CI/CD tools. Each template can be implemented without changes to produce a CI/CD pipeline. However, Astronomer recommends reconfiguring the templates to work with your own directory structures, tools, and processes.

Template types differ based on how they push code to your Deployment when you update specific files in your project. Use

### Image-only templates  

Image-only templates build a Docker image and push it to Astro whenever you update any file in your Astro project. This type of template works well for development workflows that include complex Docker customization or logic.

CI/CD templates that use image-only workflows do the following:

- Access Deployment API key credentials. These credentials must be set as OS-level environment variables named `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET`.
- Install the latest version of the Astro CLI.
- Run `astro deploy`. This creates a Docker image for your Astro project, authenticates to Astro using your Deployment API key, and pushes the image to your Deployment.

This is equivalent to running the following shell script:

```sh
# Set Deployment API key credentials as environment variables
$ export ASTRONOMER_KEY_ID="<your-api-key-id>"
$ export ASTRONOMER_KEY_SECRET="<your-api-key-secret>"
# Install the latest version of Astro CLI
$ curl -sSL install.astronomer.io | sudo bash -s
# Build your Astro project into a Docker image and push the image to your Deployment
$ astro deploy
```

### DAG-based templates

DAG-based templates use the `--dags` flag in the Astro CLI to push DAG changes to Astro. These CI/CD pipelines deploy your DAGs only when files in your `dags` folder are modified, and they deploy the rest of your Astro project as a Docker image when other files or directories are modified. For more information about the benefits of this workflow, see [Deploy DAGs only](deploy-code.md#deploy-dags-only).

CI/CD templates that use the DAG-based workflow do the following:

- Access Deployment API key credentials. These credentials must be set as OS-level environment variables named `ASTRONOMER_KEY_ID` and `ASTRONOMER_KEY_SECRET`.
- Install the latest version of the Astro CLI.
- Determine which files were updated by the commit:
    - If only DAG files in the `dags` folder have changed, run `astro deploy --dags`. This pushes your `dags` folder to your Deployment.
    - If any file not in the `dags` folder has changed, run `astro deploy`. This triggers two subprocesses. One that creates a Docker image for your Astro project, authenticates to Astro using your Deployment API key, and pushes the image to your Deployment. A second that pushes your `dags` folder to your Deployment.

This is equivalent to the following shell script: 

```sh
# Set Deployment API key credentials as environment variables
export ASTRONOMER_KEY_ID="<your-api-key-id>"
export ASTRONOMER_KEY_SECRET="<your-api-key-secret>"
export DAG_FOLDER="<path to dag folder ie. dags/>"
# Install the latest version of Astro CLI
curl -sSL install.astronomer.io | sudo bash -s
# Determine if only DAG files have changes
files=$(git diff --name-only HEAD^..HEAD)
dags_only=1
for file in $files; do
  if [[ $file != "$DAG_FOLDER"* ]]; then
    echo "$file is not a dag, triggering a full image build"
    dags_only=0
    break
  fi
done
# If only DAGs changed deploy only the DAGs in your 'dags' folder to your Deployment
if [ $dags_only == 1 ]
then
    astro deploy --dags
fi
# If any other files changed build your Astro project into a Docker image, push the image to your Deployment, and then push and DAG changes
if [ $dags_only == 0 ]
then
    astro deploy
fi
```

### Template implementations

Each template type supports a variety of implementations, some of which are documented for each tool:

- Single branch: Deploys a single branch from your version control tool to Astro. This is the default template for all CI/CD tools. 
- Multiple branch: Deploys multiple branches to separate Deployments on Astro.
- Custom image: Deploys an Astro project with a customized Runtime image and additional build arguments.

If a CI/CD tool has only one template listed, it is a single branch implementation of an image-only template.
