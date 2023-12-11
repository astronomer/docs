---
sidebar_label: Template overview
title: Template overview
id: template-overview
description: Use pre-built templates to get started with automating code Deploys 
---

Astronomer CI/CD templates are customizable, pre-built code samples that help you configure automated workflows with popular CI/CD tools, such as GitHub Actions or Jenkins. Use the templates to create a workflow that automates deploying code to Astro according to your team's CI/CD requirements and strategy.

Template types differ based on the deploy method they use and how many branches or environments they require. This document contains information about the following template types:

- _DAG deploy templates_ that use the [DAG-only deploy feature](deploy-code.md#deploy-dags-only) in Astro and either deploy DAGs or your entire Astro project depending on the files that you update.
- _Image deploy templates_ that build a Docker image and push it to Astro whenever you update any file in your Astro project, including your DAG directory.
- _Preview Deployment templates_ that automatically create and delete Deployments when you create or delete a feature branch from your main Astro project branch.

Astronomer maintains a dedicated guide with templates for select CI/CD tools. Most guides include image based templates for a single-branch implementation. Astronomer recommends reconfiguring the templates to work with your own directory structures, tools, and processes.

If you're interested in documentation for a CI/CD tool or template type that does not exist, configure your own or [contact Astronomer support](https://cloud.astronomer.io/open-support-request). To learn more about single-branch and multiple-branch implementations and decide which template is right for you, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## DAG deploy templates

_DAG deploy templates_ check the changes in your Astro project and trigger either a dag deploy or image deploy based on the files changed, allowing for faster deploys. This template deploys your DAGs when only the files in your `dags` folder are modified, and it deploys the rest of your Astro project as a Docker image when any other files or directories are modified. To learn more about the benefits of this workflow, see [Deploy DAGs](deploy-dags.md).

CI/CD templates that use the DAG deploy workflow:

- Require that each Deployment have the DAG-only deploy feature enabled. See [Enable/disable DAG-only deploys on a Deployment](deploy-dags.md#enable-disable-dag-only-deploys-on-a-deployment).
- Use a [Deployment API token](deployment-api-tokens.md), [Workspace API token](workspace-api-tokens.md), or [Organization API token](organization-api-tokens.md). This value must be set using the `ASTRO_API_TOKEN` environment variable.
- Install the latest version of the Astro CLI.
- Trigger the following Astro CLI commands depending on which files were updated by the commit:
    - If only DAG files in the `dags` folder have changed, run `astro deploy --dags`. This pushes your `dags` folder to your Deployment.
    - If any file not in the `dags` folder has changed, run `astro deploy`. This triggers two subprocesses. One that creates a Docker image for your Astro project, authenticates to Astro using your Deployment API token, and pushes the image to your Deployment. A second that pushes your `dags` folder to your Deployment.

This process is equivalent to the following shell script: 

```bash
# Set Deployment API token credentials as environment variables
export ASTRO_API_TOKEN="<your-api-token>"
export DAG_FOLDER="<path to dag folder ie. dags/>"
# Install the latest version of Astro CLI
curl -sSL install.astronomer.io | sudo bash -s
# Determine if only DAG files have changes
files=$(git diff --name-only $(git rev-parse HEAD~1) -- .)
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

## Image deploy templates  

_Image based templates_ build a Docker image and push it to Astro whenever you update any file in your Astro project. This type of template works well for development workflows that include complex Docker customization or logic.

CI/CD templates that use image based workflows:

- Use a [Deployment API token](deployment-api-tokens.md), [Workspace API token](workspace-api-tokens.md) or [Organization API token](organization-api-tokens.md). This value must be set using the `ASTRO_API_TOKEN` environment variable.
- Install the latest version of the Astro CLI.
- Run the `astro deploy` command. This creates a Docker image for your Astro project, authenticates to Astro using your Deployment API token, and pushes the image to your Deployment.

This is equivalent to running the following shell script:

```bash
# Set Deployment API token credentials as environment variables
export ASTRO_API_TOKEN="<your-api-token>"
# Install the latest version of Astro CLI
curl -sSL install.astronomer.io | sudo bash -s
# Build your Astro project into a Docker image and push the image to your Deployment
astro deploy <your-deployment-id> -f
```

## Preview Deployment templates

_Preview Deployment_ templates enable a CI/CD workflow that automates creating and deleting Deployments based on feature branches in your Git repository. A preview Deployment is automatically created when the temporary feature branch is created and the Deployment is deleted when the branch is deleted. Astronomer recommends using preview Deployments if you regularly need to test a small set of DAGs on Astro before promoting those DAGs to a base, production Deployment. This helps you lower the infrastructure cost of Deployments that are dedicated to development and testing.

To implement this feature, you need a CI/CD workflow that:

- Creates the preview Deployment when you create a new branch.
- Deploys code changes to Astro when you make updates in the branch.
- Deletes the preview Deployment when you delete the branch. 
- Deploys your changes to your base Deployment after you merge your changes into your main branch.

If you use GitHub Actions as your CI/CD tool, you can find preview Deployment templates as part of the [Astronomer GitHub action in the GitHub Marketplace](https://github.com/astronomer/deploy-action/tree/deployment-preview#deployment-preview-templates). This GitHub action includes sub-actions for each of these four steps. To learn more, see [GitHub Actions](ci-cd-templates/github-actions.md).

To configure your own automated workflow for preview Deployments with another CI/CD tool, use the following scripts. Each of the following four shell scripts is equivalent to the steps required to implement this feature with [GitHub Actions](ci-cd-templates/github-actions.md#deployment-preview-templates).

#### Create a preview Deployment

In a Deployment preview CI/CD pipeline, you run this script when you create a feature branch off of the main branch of your Astro project. 

```bash
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

```bash
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

```bash
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

```bash
# Install the Astro CLI
curl -sSL https://install.astronomer.io | sudo bash -s

# Deploy new code to base Deployment
astro deploy $DEPLOYMENT_ID
```
