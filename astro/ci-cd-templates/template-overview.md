---
sidebar_label: Template overview
title: Template overview
id: template-overview
description: Use pre-built templates to get started with automating code Deploys 
---

Templates are customizable, pre-built code samples that allow you to configure automated workflows using popular CI/CD tools, such as GitHub Actions or Jenkins. Use the Astronomer CI/CD templates to create a workflow that automates deploying code to Astro according to your team's CI/CD strategy and requirements. Template types differ based on which deploy method they use and how many environments they support.

There are a few different types of templates that Astro supports:

- _Image-only templates_ that build a Docker image and push it to Astro whenever you update any file in your Astro project.
- _DAG-based templates_ that use the [DAG-only deploy feature](/deploy-code#deploy-dags-only) in Astro.
- _Preview Deployment templates_ that automatically create and delete Deployments when you create a feature branch from your main Astro project branch.

This document contains information about each general template type, including how each template is implemented. Astronomer recommends reconfiguring the templates to work with your own directory structures, tools, and processes. To decide which template is right for you and to learn more about CI/CD use cases, see [Set up CI/CD](set-up-ci-cd.md).

## Prerequisites

- A deploy strategy for your CI/CD pipeline. See [Set up CI/CD](set-up-ci-cd.md).
- A [Deployment API key ID and secret](api-keys.md).
- A CI/CD management tool, such as [GitHub Actions](https://docs.github.com/en/actions).
- An [Astro project](create-project.md) hosted in a Git repository that your CI/CD tool can access.

## Template types

Templates allow you to configure automated workflows using popular CI/CD tools. Each template can be implemented without changes to produce a CI/CD pipeline, or you can customize them to your use case. Astronomer recommends reconfiguring the templates to work with your own directory structures, tools, and processes.

Template types differ based on how they push code to your Deployment when you update specific files in your project.

### Image-only templates  

_Image-only templates_ build a Docker image and push it to Astro whenever you update any file in your Astro project. This type of template works well for development workflows that include complex Docker customization or logic.

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

_DAG-based templates_ use the `--dags` flag in the Astro CLI to push DAG changes to Astro. These CI/CD pipelines deploy your DAGs only when files in your `dags` folder are modified, and they deploy the rest of your Astro project as a Docker image when other files or directories are modified. For more information about the benefits of this workflow, see [Deploy DAGs only](deploy-code.md#deploy-dags-only).

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

### Preview Deployment templates

_Preview Deployments_ are Deployments that correspond to a temporary feature branch in your Git repository. They are automatically created when the branch is created and deleted when the branch is deleted. You can use Preview Deployments to quickly test a particular set of DAGs and avoid paying for the infrastructure cost of the Deployment when you promote your DAG code to a permanent base Deployment. The Preview Deployment has the same configuration as the base Deployment.

To implement this feature, you need four separate CI/CD actions to complete the following actions:

- Create the preview Deployment when you create a new branch.
- Deploy code changes to Astro when you make updates in the branch.
- Delete the preview Deployment when you delete the branch. 
- Deploy your changes to your base Deployment after you merge your changes into your main branch. 

If you use GitHub Actions, Astronomer maintains a [GitHub action for Deployment previews](https://github.com/astronomer/deploy-action/tree/deployment-preview#deployment-preview-templates) in the GitHub Marketplace that includes sub-actions for each of these steps.

These sub-actions are equivalent to the four shell scripts in the topics below.

#### Create a preview Deployment

In a Deployment preview CI/CD pipeline, you run this script when you create a feature branch off of the main branch of your Astro project. 

```sh
# Install the Astro CLI
curl -sSL https://install.astronomer.io | sudo bash -s

# Get preview Deployment name
DEPLOYMENT_NAME="$(astro deployment inspect $DEPLOYMENT_ID --key configuration.name)"
BRANCH_DEPLOYMENT_NAME=$BRANCH_NAME_$DEPLOYMENT_NAME
BRANCH_DEPLOYMENT_NAME="$BRANCH_DEPLOYMENT_NAME// /_"

# Create template of Deployment to be copied
astro deployment inspect $DEPLOYMENT_ID --template > deployment-preview-template.yaml # automatically creates deployment-preview-template.yaml file

# Add name to Deployment template file
sed -i "s|  name:.*|  name: $BRANCH_DEPLOYMENT_NAME}|g"  deployment-preview-template.yaml

# Create new preview Deployment based on the Deployment template file
astro deployment create --deployment-file deployment-preview-template.yaml

# Deploy new code to the deployment preview 
astro deploy -n $BRANCH_DEPLOYMENT_NAME
```

#### Update a preview Deployment

In a Deployment preview CI/CD pipeline, you run this script whenever you make changes in your feature branch.

```sh
# Install the Astro CLI
curl -sSL https://install.astronomer.io | sudo bash -s

# Get preview Deployment name
DEPLOYMENT_NAME="$(astro deployment inspect $DEPLOYMENT_ID --key configuration.name)"
BRANCH_DEPLOYMENT_NAME=$BRANCH_NAME_$DEPLOYMENT_NAME
BRANCH_DEPLOYMENT_NAME="$BRANCH_DEPLOYMENT_NAME// /_"

# Deploy new code to the preview Deployment
astro deploy -n $BRANCH_DEPLOYMENT_NAME
```

#### Delete a preview Deployment

In a Deployment preview CI/CD pipeline, you run this script when you delete your feature branch.

```sh
# Install the Astro CLI
curl -sSL https://install.astronomer.io | sudo bash -s

DEPLOYMENT_NAME="$(astro deployment inspect $DEPLOYMENT_ID --key configuration.name)"
BRANCH_DEPLOYMENT_NAME=$BRANCH_NAME_$DEPLOYMENT_NAME
BRANCH_DEPLOYMENT_NAME="$BRANCH_DEPLOYMENT_NAME// /_"

# Delete preview Deployment
astro deployment delete -n $BRANCH_DEPLOYMENT_NAME -f
```

#### Deploy changes from a preview Deployment to a base Deployment

In a Deployment preview CI/CD pipeline, you run this script when you merge your feature branch into your main branch.

```sh
# Install the Astro CLI
curl -sSL https://install.astronomer.io | sudo bash -s

# Deploy new code to base Deployment
astro deploy $DEPLOYMENT_ID
```

### Template implementations

Each template type supports a variety of implementations, some of which are documented for each tool:

- _Single branch_: Deploys a single branch from your version control tool to Astro. This is the default template for all CI/CD tools. 
- _Multiple branch_: Deploys multiple branches to separate Deployments on Astro.
- _Custom image_: Deploys an Astro project with a customized Runtime image and additional build arguments.

If a CI/CD tool has only one template listed, it is a single branch implementation of an image-only template.
