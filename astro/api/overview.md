---
title: Astro API overview
sidebar_label: Overview
id: overview
---

The Astro API is a standard REST API that you can use to develop applications for interacting with Astro components.

The API contains multiple schemas, with each schema representing a different part of Astro:

- **Platform API schema**: Includes endpoints for updating your Astro infrastructure and resources, such as clusters, Deployments, and Workspaces.
- **Identity and access management (IAM) API schema**: Includes endpoints for managing role-based access control (RBAC) components, such as users and Teams.

To make your first request using the Astro API, see [Get started with the Astro API](api/get-started.md).

:::info

The Astro API is currently in beta. See [Support](versioning-and-support.md) for all policies related to using beta releases of the API.

:::

## Authentication

All requests to the API must be authenticated. You can use [bearer authentication](https://swagger.io/docs/specification/authentication/bearer-authentication/) to authenticate with a [Workspace API token](workspace-api-tokens.md) or [Organization API token](organization-api-tokens.md). The following example shows how you can add a token to a curl request:

```curl
curl https://api.astronomer-dev.io/platform/v1beta1/organizations/{organizationId}/clusters \
--header 'Authorization: Bearer <your-api-token>'
```

Endpoints can return subsets of specific attributes based on the permissions of your API token. If your API token's role allows you to access something in the Cloud UI or Astro CLI, it also allows you to access the same thing or action using the API. See [User permissions](user-permissions.md) for a list of all possible permissions.

## Rate limiting

The maximum number of API requests you can make with the same API token depends on the type of request you're making:

- **`POST` requests**: You can make a make a maximum of 5 requests per second using the same API token.
- **`DELETE` requests**: You can make a make a maximum of 5 requests per second using the same API token.
- **`GET` requests**: You can make a make a maximum of 10 requests per second using the same API token.

## Idempotent requests

Astro supports different levels of [idempotency](https://en.wikipedia.org/wiki/Idempotence) for different request types.

- **`POST` requests (Create)**: Identical `POST` requests to create a new object will result in the creation of multiple objects. For example, if you make identical requests to create an Organization, Astro creates multiple Organizations with identical settings and unique IDs.
- **`POST` requests (Update)**: Idempotency is guaranteed for all `POST` requests to update an existing object.
- **`DELETE` requests**: Idempotency is guaranteed for all `DELETE` requests. Any successive identical `DELETE` requests return a 404 error.

## API status codes

If the API returns a `200` code, your API request was a success. If the API returns a `40x` or `500` code, your request resulted in one of the following errors:

- `400`: **Bad Request** - Your request was not successful because it was not formatted properly, possibly due to missing required parameters. 
- `401`: **Unauthorized** - Your request did not include an API token. 
- `403`: **Forbidden** - The API token you included did not have sufficient permissions to complete the request.
- `500`: **Internal sever error** - The request could not be completed because of an error caused by Astro.

All error responses include a `requestId` that you can share with Astronomer support if you want to learn more about the error. 