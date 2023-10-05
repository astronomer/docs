---
title: 'Manage Deployment API keys'
sidebar_label: 'Deployment API keys'
id: api-keys
description: Create Deployment API keys to make requests to Airflow's REST API and set up a CI/CD pipeline.
---

:::warning

Deployment API keys will soon be deprecated in favor of [Deployment API tokens](deployment-api-tokens.md). You can continue to use existing Deployment API keys for now, but you will have to complete a one-time migration to Deployment API tokens in the future.

After API tokens are generally available, Deployments with zero API keys will not show the **API Keys** tab and you will no longer be able to create Deployment API keys. If you want to continue using API keys, ensure that you always have at least one API key configured for the Deployment. 

:::

An API key is a unique key ID and secret pair that you can use as an alternative to manual user authentication for some Astro actions. You can also use API keys to automate common actions on Astro that require manual inputs.

You can use Deployment API keys to complete the following actions without authenticating as a user:

- Deploy code to Astro [through CI/CD](set-up-ci-cd.md) with tools such as GitHub Actions or Circle CI.
- Update Deployment [environment variables](env-vars-overview.md).
- Update Deployment resources. See [Manage Deployments as code](manage-deployments-as-code.md).
- Fetch a short-lived access token that assumes the permissions of the Deployment API key. This access token can be used to make requests to the [Airflow REST API](airflow-api.md).

You can't use a Deployment API key to [create Deployments](create-deployment.md) or manage users within a Deployment's Workspace.

## Use API keys

When using a Deployment API key, keep the following in mind:

- A Deployment API key ID and secret are permanently valid.
- Deployment API keys are deleted permanently if their corresponding Deployment is deleted.
- A Deployment API key is not bound to the user who creates it. When a user who created the API key is removed from the Workspace, or their permissions change, the Deployment and CI/CD workflows that use the API key are not affected.
- Any user or service with access to an API key and secret can access the corresponding Deployment. The only way to delete this access is to [delete the API key](api-keys.md#delete-an-api-key) or [delete the Deployment](deployment-settings.md#delete-a-deployment).

## Create an API key

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **API Keys** tab.

3. Click **API Key**:

    ![Add API key button](/img/docs/add-api-key.png)

4. Enter a name and an optional description for the API key and then click **Create API Key**:

    ![Create API key button](/img/docs/create-api-key.png)

5. Optional. Copy the API key ID and secret for use in API calls and CI/CD pipelines and then click **I've saved the Key Secret**. Make sure you save the key secret securely, as this is the only time you will have access to see it in plain text.

:::tip

If you just need to make a single API call, you can use a temporary user authentication token instead of a Deployment API key ID and secret pair. To retrieve a temporary authentication token, go to `cloud.astronomer.io/token` and copy the token that appears. This token is valid only for 1 hour.

:::

## Use an API key with the Astro CLI

To use a Deployment API key with the Astro CLI, you must make your API key ID and secret accessible to the Astro CLI by setting the following OS-level environment variables:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

For example, to update a Deployment using the Astro CLI on a Mac machine, set temporary OS-level environment variables with the following commands:

```sh
export ASTRONOMER_KEY_ID=<your-key-id>
export ASTRONOMER_KEY_SECRET=<your-key-secret>
```

After you set the variables, you can run `astro deployment update` for the Deployment and you don't have to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update a Deployment.

## Use an API key for CI/CD

If you deploy DAGs regularly to a production environment, Astronomer recommends using Deployment API keys to automate pushing code with a tool such as GitHub Actions or Circle CI.

For more information and examples, see [Automate code deploys with CI/CD](set-up-ci-cd.md).

## Delete an API key

If you delete an API key, make sure that no existing CI/CD pipelines are using it. Once deleted, an API key and secret cannot be recovered. If you unintentionally delete an API key, create a new one and update any CI/CD workflows that used the deleted API key.

1. In the Cloud UI, select a Workspace, click **Deployments**, and then select a Deployment.

2. Click the **API Keys** tab.

3. Click **Edit** next to your API key.

    ![Edit API key button](/img/docs/edit-api-key.png)

4. Click **Delete API Key**, enter `Delete`, and then click **Yes, Continue**.

## Related documentation

- [Choose a CI/CD Strategy for deploying code to Astro](set-up-ci-cd.md)
- [Deploy code](deploy-code.md)
- [Airflow API](airflow-api.md)
