---
title: 'Deploy to Astro with the API'
sidebar_label: 'Deploy with API'
id: deploy-with-api
---

While you can deploy code to Astro using the GitHub Integration, the Astro CLI, or by configuring a CI/CD pipeline, you might prefer to use the Astro API to automate deploying code. Using the Astro API can solve some of the deploy automation issues that can result because some CI/CD configurations are not compatible with the GitHub Integration and the Astro CLI requires you to install Docker.

Instead of using the other code deploy options, you can instead use the Astro API Deploy endpoints to perform `IMAGE_ONLY`, `DAG_ONLY`, or both `IMAGE_AND_DAG` Deploys.

This guide contains a list of scenarios and the respective scripts that you can use to deploy code with the Astro API using bash scripts. It also includes an example of an entire deploy flow, in case you want to use those steps and integrate into your own CI/CD pipelines.

## Feature overview

This guide highlights the following Astro features to use for automating code deploys:

- The Astro API [`Deploy` endpoint](https://docs.astronomer.io/api/platform-api-reference/deploy/list-deploys) to create and manage code deploys to an Astro Deployment.

## Prerequisites

This use case assumes you have:

- Sufficient permissions to deploy code to your Astro Deployments
- At least one Astro Deployment
- The following values configured:
    - `ORGANIZATION_ID`
    - `DEPLOYMENT_ID`
    - `ASTRO_API_TOKEN` - See [Create an API token](https://docs.astronomer.io/astro/automation-authentication#step-1-create-an-api-token)
    - `AIRFLOW_PROJECT_PATH` - The path where your Airflow project exists.

## Example workflow

## Scripts and scenarios

### With DAG deploy enabled

### With DAG deploy disabled