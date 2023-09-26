---
title: Get started with the Astro API
sidebar_label: Get started
id: get-started
---

In this quick introduction to the Astro API, you'll make some simple requests to retrieve details about your Organization and create a Workspace API token.

## Prerequisites

- An [Astro account](log-in-to-astro.md). 
- An [Organization API token](organization-api-tokens.md) with the Organization Owner role. Astronomer recommends that you create a new API token for this tutorial.
- An Astro Workspace.
- A method for making API requests. This tutorial assumes you're using curl, but you can also use tools such as Postman.

## Step 1: Make your first API request

To access most endpoints, you need to provide an Organization ID to the API as a path parameter. One of the few requests that doesn't require an Organization ID is the [List Organizations](https://docs.astronomer.io/astro/api/platform-api-reference#tag/Organization/operation/ListOrganizations) request, which means that you can programmatically retrieve an Organization ID. 

To retrieve the Organization ID through the API, run the following command:

```bash
curl https://api.astronomer.io/platform/v1beta1/organizations \
--H 'Authorization: Bearer <your-organization-api-token>' \
```

If the command was successful, then you receive a response that begins similarly to the following:

```json {16}
{
  "limit": 10,
  "offset": 0,
  "organizations": [
    {
      "billingEmail": "billing@company.com",
      "createdAt": "2022-11-22T04:37:12T",
      "createdBySubject": {
        "apiTokenName": "my-token",
        "avatarUrl": "https://avatar.url",
        "fullName": "Jane Doe",
        "id": "clm8qv74h000008mlf08scq7k",
        "subjectType": "USER",
        "username": "user1@company.com"
      },
      "id": "clmaxoarx000008l2c5ayb9pt",
      "isScimEnabled": false,
...
      ],
```

Copy the top-level `id` from this response. This is your Organization ID.

While you could have retrieved this value manually from the Cloud UI, using the API lets you script this workflow and execute it on a regular basis.

## Step 2: Request Workspace details from the API

Using the Organization ID you copied, you can now find the ID for the Workspace where you want to create your API token. 

Run the following command to list all Workspaces in your Organization:

```bash
curl https://api.astronomer.io/platform/v1beta1/organizations/<your-organization-id>/workspaces \
--H 'Authorization: Bearer <your-api-token>' \
```

If the command succeeds, the API returns a list of Workspaces similar to the following:

```json{18}
{
  "limit": 0,
  "offset": 0,
  "totalCount": 0,
  "workspaces": [
    {
      "cicdEnforcedDefault": true,
      "createdAt": "2023-09-08T12:00:00Z",
      "createdBy": {
        "apiTokenName": "my-token",
        "avatarUrl": "https://avatar.url",
        "fullName": "Jane Doe",
        "id": "clm8qv74h000008mlf08scq7k",
        "subjectType": "USER",
        "username": "user1@company.com"
      },
      "description": "This is a test workspace",
      "id": "clm8t5u4q000008jq4qoc3036",
      "name": "My Workspace",
      "organizationId": "clm8t5u4q000008jq4qoc3036",
      "organizationName": "My Organization",
      "updatedAt": "2023-09-08T13:30:00Z",
      "updatedBy": {
        "apiTokenName": "my-token",
        "avatarUrl": "https://avatar.url",
        "fullName": "Jane Doe",
        "id": "clm8qv74h000008mlf08scq7k",
        "subjectType": "USER",
        "username": "user1@company.com"
      }
    }
  ]
}
```

In the response for your specific Workspace, the top-level `id`. This is your Workspace ID.

:::tip

If the API returned many Workspaces, try sending the following request instead to limit your search: 

```bash
curl https://api.astronomer.io/platform/v1beta1/organizations/<your-organization-id>/workspaces?search="<your-workspace-name>" \
--H 'Authorization: Bearer <your-organization-api-token>' \
```

Query parameters like `search` are useful for limiting the results that the API returns for `GET` requests.

:::

## Step 3: Update your token description using the API

Now that you have both an Organization ID and a Workspace ID, you can create a Workspace API token using the Astro API.

1. Run the following command to create a new Workspace API token:

    ```bash
    curl -X POST https://api.astronomer-dev.io/iam/v1beta1/organizations/<your-organization-id>/tokens/<your-token-id> \
    --H 'Authorization: Bearer <your-organization-api-token>' \
    -D Copy { "description": "I wrote this description using the Astro API!", "name": "My new API token", "role": "WORKSPACE_MEMBER" }
    ```

    If the request was successful, the API will return a response with all of your new token's details.

2. In the Cloud UI, go to **Workspace Settings** > **Access Management** > **API Tokens** and find your Workspace API token. You should see your updated description under **Description**.

## Next steps

Get familiar with all possible Astro API requests using the API reference guides:

- [Platform API reference](api/platform-api-reference.mdx)
- [IAM API reference](api/iam-api-reference.mdx)