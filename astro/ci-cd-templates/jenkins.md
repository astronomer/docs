---
sidebar_label: Jenkins
title: Astro CI/CD templates for Jenkins
id: jenkins
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using Jenkins. 
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Use the following CI/CD templates to automate deploying Apache Airflow DAGs from a Git repository to Astro with [Jenkins](https://www.jenkins.io/).

The following templates for Jenkins are available:

- [Image-only deploy templates](template-overview.md#image-only-templates)
- [DAG-based deploy templates](template-overview.md#dag-based-templates)

Each template type supports multiple implementations. If you have one Deployment and one environment on Astro, use the _single branch implementation_. If you have multiple Deployments that support development and production environments, use the _multiple branch implementation_. If your team builds custom Docker images, use the _custom image_ implementation.

For more information on each template or to configure your own, see [Template overview](template-overview.md). To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](develop-project.md#create-an-astro-project) hosted in a Git repository that Jenkins can access.
- An [Astro Deployment](create-deployment.md).
- Either a [Workspace API token](workspace-api-tokens.md) or an [Organization API token](organization-api-tokens.md).
- Access to [Jenkins](https://www.jenkins.io/).

Each CI/CD template implementation might have additional requirements.

## Image-only templates
 
<Tabs
    defaultValue="standard"
    groupId= "image-only-templates"
    values={[
        {label: 'Single branch', value: 'standard'},
        {label: 'Multiple branch', value: 'multibranch'},
        {label: 'Custom Image', value: 'custom'},
    ]}>
<TabItem value="standard">

To automate code deploys to a single Deployment using [Jenkins](https://www.jenkins.io/), complete the following setup in a Git-based repository hosting an Astro project:

1. In your Jenkins pipeline configuration, add the following environment variables:

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your production deployment

    To set environment variables in Jenkins, on the Jenkins Dashboard go to **Manage Jenkins** > **Configure System** > **Global Properties** > **Environment Variables** > **Add**. To see Jenkins documentation on environment variables click [here](https://www.jenkins.io/doc/pipeline/tour/environment/)

    Be sure to set the value for your API token as secret.

2. At the root of your Astro Git repository, add a [Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) that includes the following script:

    <pre><code parentName="pre">{`pipeline {
        agent any
        stages {
            stage('Deploy to Astronomer') {
                when {
                    expression {
                        return env.GIT_BRANCH == "origin/main"
                    }
                }
                steps {
                    checkout scm
                    sh '''
                    curl -LJO https://github.com/astronomer/astro-cli/releases/download/v${siteVariables.cliVersion}/astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    tar -zxvf astro_${siteVariables.cliVersion}_linux_amd64.tar.gz astro && rm astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    ./astro deploy
                    '''
                }
            }
        }
        post {
            always {
                cleanWs()
            }
        }
    }`}</code></pre>

    This `Jenkinsfile` triggers a code push to Astro every time a commit or pull request is merged to the `main` branch of your repository.

</TabItem>

<TabItem value="multibranch">

To automate code deploys across multiple Deployments using [Jenkins](https://www.jenkins.io/), complete the following setup in a Git-based repository hosting an Astro project:

1. In Jenkins, add the following environment variables:

    - `PROD_ASTRO_API_TOKEN`: The value for your production Workspace or Organization API token.
    - `PROD_DEPLOYMENT_ID`: The Deployment ID of your production Deployment
    - `DEV_ASTRO_API_TOKEN`: The value for your development Workspace or Organization API token.
    - `DEV_DEPLOYMENT_ID`: The Deployment ID of your development Deployment

    To set environment variables in Jenkins, on the Jenkins Dashboard go to **Manage Jenkins** > **Configure System** > **Global Properties** > **Environment Variables** > **Add**. To see Jenkins documentation on environment variables click [here](https://www.jenkins.io/doc/pipeline/tour/environment/)

    Be sure to set the values for your API credentials as secret.

2. At the root of your Git repository, add a [`Jenkinsfile`](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) that includes the following script:

    <pre><code parentName="pre">{`pipeline {
        agent any
        stages {
            stage('Set Environment Variables') {
                steps {
                    script {
                        if (env.GIT_BRANCH == 'main') {
                            echo "The git branch is ${siteVariables.jenkinsenv}";
                            env.ASTRONOMER_API_TOKEN = env.PROD_ASTRONOMER_API_TOKEN;
                            env.ASTRONOMER_DEPLOYMENT_ID = env.PROD_DEPLOYMENT_ID;
                        } else if (env.GIT_BRANCH == 'dev') {
                            echo "The git branch is ${siteVariables.jenkinsenv}";
                            env.ASTRONOMER_API_TOKEN = env.DEV_ASTRONOMER_API_TOKEN;
                            env.ASTRONOMER_DEPLOYMENT_ID = env.DEV_DEPLOYMENT_ID;
                        } else {
                            echo "This git branch ${siteVariables.jenkinsenv} is not configured in this pipeline."
                        }
                    }
                }
            }
            stage('Deploy to Astronomer') {
                steps {
                    checkout scm
                    sh '''
                    curl -LJO https://github.com/astronomer/astro-cli/releases/download/v${siteVariables.cliVersion}/astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    tar -zxvf astro_${siteVariables.cliVersion}_linux_amd64.tar.gz astro && rm astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    ./astro deploy
                    '''
                }
            }
        }
        post {
            always {
                cleanWs()
            }
        }
    }`}</code></pre>

    This `Jenkinsfile` triggers a code push to an Astro Deployment every time a commit or pull request is merged to the `dev` or `main` branch of your repository.

</TabItem>

<TabItem value="custom">

If your Astro project requires additional build-time arguments to build an image, you need to define these build arguments using Docker's [`build-push-action`](https://github.com/docker/build-push-action).

#### Configuration requirements

- An Astro project that requires additional build-time arguments to build the Runtime image.

1. In your Jenkins pipeline configuration, add the following environment variables:

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your production deployment

    To set environment variables in Jenkins, on the Jenkins Dashboard go to **Manage Jenkins** > **Configure System** > **Global Properties** > **Environment Variables** > **Add**. To see Jenkins documentation on environment variables click [here](https://www.jenkins.io/doc/pipeline/tour/environment/)

    Be sure to set the value for your API token as secret.

2. At the root of your Astro Git repository, add a [Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) that includes the following script:

<pre><code parentName="pre">{`pipeline {
        agent any
        stages {
            stage('Deploy to Astronomer') {
                when {
                    expression {
                        return env.GIT_BRANCH == "origin/main"
                    }
                }
                steps {
                    checkout scm
                    sh '''
                    export astro_id=${siteVariables.jenkinsenv3}
                    docker build -f Dockerfile --progress=plain --build-arg <your-build-arguments> -t ${siteVariables.jenkinsenv4} .
                    curl -LJO https://github.com/astronomer/astro-cli/releases/download/v${siteVariables.cliVersion}/astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    tar -zxvf astro_${siteVariables.cliVersion}_linux_amd64.tar.gz astro && rm astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    ./astro deploy --image-name ${siteVariables.jenkinsenv4}
                    '''
                }
            }
        }
        post {
            always {
                cleanWs()
            }
        }
    }`}</code></pre>

This `Jenkinsfile` triggers a code push to Astro every time a commit or pull request is merged to the `main` branch of your repository.

</TabItem>

</Tabs>

## DAG-based templates

The DAG-based template uses the `--dags` flag in the Astro CLI to push DAG changes to Astro. These CI/CD pipelines deploy your DAGs only when files in your `dags` folder are modified, and they deploy the rest of your Astro project as a Docker image when other files or directories are modified. For more information about the benefits of this workflow, see [Deploy DAGs only](deploy-code.md#deploy-dags-only).

### Single branch implementation

Use the following template to implement DAG-only deploys to a single Deployment using Jenkins.

1. In your Jenkins pipeline configuration, add the following parameters:

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your production deployment

    Be sure to set the values for your API token as secret.

2. At the root of your Git repository, add a [`Jenkinsfile`](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) that includes the following script:

    <pre><code parentName="pre">{`pipeline {
        agent any
        stages {
            stage('Dag Only Deploy to Astronomer') {
                when {
                    expression {
                        return env.GIT_BRANCH == "origin/main"
                    }
                }
                steps {
                    checkout scm
                    sh '''
                    curl -LJO https://github.com/astronomer/astro-cli/releases/download/v${siteVariables.cliVersion}/astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    tar -zxvf astro_${siteVariables.cliVersion}_linux_amd64.tar.gz astro && rm astro_${siteVariables.cliVersion}_linux_amd64.tar.gz
                    files=($(git diff-tree HEAD --name-only --no-commit-id))
                    find="dags"
                    if [[ ${siteVariables.jenkinsenv1} =~ (^|[[:space:]])"$find"($|[[:space:]]) && ${siteVariables.jenkinsenv2} -eq 1 ]]; then
                    ./astro deploy --dags;
                    else
                    ./astro deploy;
                    fi
                    '''
                }
            }
        }
        post {
            always {
                cleanWs()
            }
        }
    }`}</code></pre>

