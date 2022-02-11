---
title: 'Manage Deployment API Keys'
sidebar_label: 'Deployment API Keys'
id: api-keys
description: Create Deployment API keys to make requests to Airflow's REST API and set up a CI/CD pipeline.
---

## Overview

This guide provides instructions for how to create API keys for Deployments on Astronomer. You can use API keys to programmatically deploy DAGs to a Deployment on Astronomer.

A Deployment API key has the following properties:

- It can deploy code to Astronomer (customizable permissions coming soon).
- Its key ID and secret are valid indefinitely and can be used to fetch a short-lived access token that assumes the permissions of the Deployment API key. This access token is required by the Astronomer API to complete the deploy code process. For more information on using this token, read [Refresh Access Token](api-keys#refresh-access-token).
- It is deleted permanently if its corresponding Deployment is deleted.

This guide provides steps for creating and deleting Deployment API keys.

## Create an API Key

To create an API key for a Deployment:

1. In the Astronomer UI, open your Deployment.
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

## Request Access Token

In order to deploy code on Astronomer with a Deployment API key, you need to use the API key ID and secret to request an access token. This access token is required by the Astronomer API to trigger the deploy code process. It is valid only for 24 hours. To fetch a token with an existing API key ID and secret, run the following API request:

```curl
curl --location --request POST "https://auth.astronomer.io/oauth/token" \
        --header "content-type: application/json" \
        --data-raw "{
            \"client_id\": \"<api-key-id>\",
            \"client_secret\": \"<api-key-secret>\",
            \"audience\": \"astronomer-ee\",
            \"grant_type\": \"client_credentials\"}" | jq -r '.access_token'
```

Make sure to replace `api-key-id` and `api-key-secret` in this request with values that correspond to your own API key.

To avoid manually fetching this token, we strongly recommend adding this API request to any CI/CD pipeline that uses Deployment API keys. That way, your access token is automatically refreshed every time your CI/CD pipeline needs it to complete the deploy code process. For examples of this implementation, see [CI/CD Templates](ci-cd.md#cicd-templates).

## Delete an API Key

To delete a Deployment API Key:

1. In the Astronomer UI, open your Deployment.
2. In the menu for the API key you want to delete, click **Edit**:

    <div class="text--center">
      <img src="/img/docs/edit-api-key.png" alt="Edit API Key button" />
    </div>

3. Click **Delete API Key**, then follow the onscreen prompt to finalize the deletion:

    <div class="text--center">
      <img src="/img/docs/delete-api-key.png" alt="Delete API Key button" />
    </div>
