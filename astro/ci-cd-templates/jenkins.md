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

- An [Astro project](create-first-dag.md#step-1-create-an-astro-project) hosted in a Git repository that Jenkins can access.
- An [Astro Deployment](create-deployment.md).
- A [Deployment API key ID and secret](api-keys.md).
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

1. In your Jenkins pipeline configuration, add the following parameters:

    - `ASTRONOMER_KEY_ID`: Your Deployment API key ID
    - `ASTRONOMER_KEY_SECRET`: Your Deployment API key secret
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your production deployment

    Be sure to set the values for your API credentials as secret.

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

    - `PROD_ASTRONOMER_KEY_ID`: Your Production Deployment API key ID
    - `PROD_ASTRONOMER_KEY_SECRET`: Your Production Deployment API key secret
    - `PROD_DEPLOYMENT_ID`: The Deployment ID of your Production Deployment
    - `DEV_ASTRONOMER_KEY_ID`: Your Development Deployment API key ID
    - `DEV_ASTRONOMER_KEY_SECRET`: Your Development Deployment API key secret
    - `DEV_DEPLOYMENT_ID`: The Deployment ID of your Development Deployment

    To set environment variables in Jenkins, on the Jenkins Dashboard go to **Manage Jenkins** > **Configure System** > **Global Properties** > **Environment Variables** > **Add**.

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
                            env.ASTRONOMER_KEY_ID = env.PROD_ASTRONOMER_KEY_ID;
                            env.ASTRONOMER_KEY_SECRET = env.PROD_ASTRONOMER_KEY_SECRET;
                            env.ASTRONOMER_DEPLOYMENT_ID = env.PROD_DEPLOYMENT_ID;
                        } else if (env.GIT_BRANCH == 'dev') {
                            echo "The git branch is ${siteVariables.jenkinsenv}";
                            env.ASTRONOMER_KEY_ID = env.DEV_ASTRONOMER_KEY_ID;
                            env.ASTRONOMER_KEY_SECRET = env.DEV_ASTRONOMER_KEY_SECRET;
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
</Tabs>

## DAG-based templates

The DAG-based template uses the `--dags` flag in the Astro CLI to push DAG changes to Astro. These CI/CD pipelines deploy your DAGs only when files in your `dags` folder are modified, and they deploy the rest of your Astro project as a Docker image when other files or directories are modified. For more information about the benefits of this workflow, see [Deploy DAGs only](deploy-code.md#deploy-dags-only).

### Single branch implementation

Use the following template to implement DAG-only deploys to a single Deployment using Jenkins.

1. In your Jenkins pipeline configuration, add the following parameters:

    - `ASTRONOMER_KEY_ID`: Your Deployment API key ID
    - `ASTRONOMER_KEY_SECRET`: Your Deployment API key secret
    - `ASTRONOMER_DEPLOYMENT_ID`: The Deployment ID of your production deployment

    Be sure to set the values for your API credentials as secret.

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

