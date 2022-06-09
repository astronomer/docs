---
title: 'Manage Deployment API Keys'
sidebar_label: 'Deployment API Keys'
id: api-keys
description: Create Deployment API keys to make requests to Airflow's REST API and set up a CI/CD pipeline.
---

## Overview

This guide provides instructions for how to create API keys for Deployments on Astro. You can use API keys to programmatically deploy DAGs to a Deployment on Astro.

You can use a Deployment API key to:

- Deploy code to Astro in a [CI/CD pipeline](ci-cd.md).
- Programmatically update [Deployment configurations](configure-deployment-resources.md) and [environment variables](environment-variables.md).
- Fetch a short-lived access token that assumes the permissions of the Deployment API key. This access token can be used to make requests to the [Airflow REST API](airflow-api.md).

When using Deployment API keys, keep in mind the following:

- A Deployment API key ID and secret are valid indefinitely and can be used to access Deployments without manual authentication.
- Deployment API keys are deleted permanently if their corresponding Deployment is deleted.

## Create an API Key

To create an API key for a Deployment:

1. In the Cloud UI, open your Deployment.
2. In the **API Keys** menu, click **Add API Key**:

    <div class="text--center">
      <img src="/img/docs/add-api-key.png" alt="Add API Key button" />
    </div>

3. Give the key a name and description, then click **Create API Key**:

    <div class="text--center">
      <img src="/img/docs/create-api-key.png" alt="Create API Key button" />
    </div>

From here, you can copy the API key ID and secret for use in API calls and CI/CD pipelines. Make sure to save the key secret securely, as this is the only time you will have access to see it in plain text.

:::tip

If you just need to make a single API call, you can use a temporary user authentication token instead of a Deployment API key ID and secret pair. To retrieve a temporary authentication token, go to `cloud.astronomer.io/token` and copy the token that appears. This token is valid only for 24 hours.

:::

## Using Deployment API Keys

Deployment API keys are primarily used to automate actions that otherwise require manual inputs. They allow you to:

- Deploy code to Astro [using CI/CD](ci-cd.md) with tools such as GitHub Actions or Jenkins.
- Deploy code and configuration changes to Astro [using the Astro CLI](deploy-code.md) without user authentication.
- Automate requests to the [Airflow REST API](airflow-api.md).

To use API keys with the Astro CLI, you need to make your Deployment API key ID and secret accessible to the machine running the CLI via the following OS-level environment variables:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

For example, to update a given Deployment using the Astro CLI on a Mac machine, set temporary OS-level environment variables with the following commands:

```sh
export ASTRONOMER_KEY_ID=<your-key-id>
export ASTRONOMER_KEY_SECRET=<your-key-id>
```

After setting the variables, running `astro deployment update` works for the Deployment without you having to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update production-level Deployments.

## Delete an API Key

To delete a Deployment API Key:

1. In the Cloud UI, open your Deployment.
2. In the menu for the API key you want to delete, click **Edit**:

    <div class="text--center">
      <img src="/img/docs/edit-api-key.png" alt="Edit API Key button" />
    </div>

3. Click **Delete API Key**, then follow the onscreen prompt to finalize the deletion:

    <div class="text--center">
      <img src="/img/docs/delete-api-key.png" alt="Delete API Key button" />
    </div>


## Next Steps

For more information about how to use API keys, see:

- [CI/CD](ci-cd.md)
- [Deploy Code](deploy-code.md)
- [Airflow API](airflow-api.md)
