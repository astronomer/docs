---
title: 'Manage Deployment API keys'
sidebar_label: 'Deployment API keys'
id: api-keys
description: Create Deployment API keys to make requests to Airflow's REST API and set up a CI/CD pipeline.
---

An API key is a unique key ID and secret pair that can be used in place of manual user authentication for certain actions on Astro. You can use API keys to automate common actions on Astro that otherwise require manual inputs.

With Deployment API keys, you can:

- Automate deploying code to Astro [in CI/CD](ci-cd.md) with tools such as GitHub Actions or Circle CI.
- Automate updating [environment variables](environment-variables.md).
- Fetch a short-lived access token that assumes the permissions of the Deployment API key. This access token can be used to make requests to the [Airflow REST API](airflow-api.md).

## Using API keys

When using a Deployment API key, keep in mind:

- A Deployment API key ID and secret are valid indefinitely.
- Deployment API keys are deleted permanently if their corresponding Deployment is deleted.
- A Deployment API key is not tied to the user that creates it. If the user that creates the API key is removed from the Workspace or their permissions change, the API key does not lose access to the Deployment and CI/CD workflows that use it are not affected.
- Any user or service with access to an API key and secret can access the corresponding Deployment. The only way to delete this access is to [delete the API key](api-keys.md#delete-an-api-key) or [delete the Deployment](configure-deployment-resources.md#delete-a-deployment).

:::info

You cannot currently use API keys to automate creating and updating Deployments, creating and updating Workspaces, or inviting and removing users.

A new API key framework is coming soon to Astro to unlock advanced automation workflows. If you're interested in this feature or have questions, contact [Astronomer support](https://cloud.astronomer.io/support).

:::

## Create an API key

1. In the Cloud UI, select a Workspace and then select a Deployment.

2. Click the **API Keys** tab.

3. Click **API Key**:

    ![Add API key button](/img/docs/add-api-key.png)

4. Enter a name and an optional description for the API key and then click **Create API Key**:

    ![Create API key button](/img/docs/create-api-key.png)

5. Optional. Copy the API key ID and secret for use in API calls and CI/CD pipelines and then click **I've saved the Key Secret**. Make sure you save the key secret securely, as this is the only time you will have access to see it in plain text.

:::tip

If you just need to make a single API call, you can use a temporary user authentication token instead of a Deployment API key ID and secret pair. To retrieve a temporary authentication token, go to `cloud.astronomer.io/token` and copy the token that appears. This token is valid only for 24 hours.

:::

## Use an API key with Astro CLI

To use a Deployment API key with the Astro CLI, you must make your API key ID and secret accessible to the CLI by setting the following OS-level environment variables:

- `ASTRONOMER_KEY_ID`
- `ASTRONOMER_KEY_SECRET`

For example, to update a Deployment using the Astro CLI on a Mac machine, set temporary OS-level environment variables with the following commands:

```sh
export ASTRONOMER_KEY_ID=<your-key-id>
export ASTRONOMER_KEY_SECRET=<your-key-secret>
```

After you set the variables, you can run `astro deployment update` for the Deployment and you don't have to manually authenticate to Astronomer. Astronomer recommends storing `ASTRONOMER_KEY_SECRET` as a secret before using it to programmatically update a Deployment.

## Use an API key for CI/CD

If you deploy DAGs regularly to a production environment, Astronomer recommends using Deployment API keys to automate pushing code with a tool like GitHub Actions or Circle CI.

For more information and examples, see [Automate code deploys with CI/CD](ci-cd.md).

## Delete an API key

If you delete an API key, make sure that no existing CI/CD pipelines are using it. Once deleted, an API key and secret cannot be recovered. If you unintentionally delete an API key, create a new one and update any CI/CD workflows that used the deleted API key.

1. In the Cloud UI, select a Workspace and then select a Deployment.

2. Click the **API Keys** tab.

3. Click **Edit** next to your API key.

    ![Edit API key button](/img/docs/edit-api-key.png)

4. Click **Delete API Key**, enter `Delete`, and then click **Yes, Continue**.

## Related documentation

- [CI/CD](ci-cd.md)
- [Deploy code](deploy-code.md)
- [Airflow API](airflow-api.md)
