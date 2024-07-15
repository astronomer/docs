---
sidebar_label: 'Overview'
title: 'Use the Houston API on Astronomer Software'
id: houston-api
description: Learn how to make requests to your Astronomer Software installation using the Houston API.
---

The Houston API allows you to build applications that provision and manage resources on Astronomer Software. You can use the Houston API to perform CRUD operations on entities scoped to the Astronomer platform, including Apache Airflow® Deployments, Workspaces, and users.

For example, you can:

- Delete a deployment
- Look up a deployment's resource config
- Add a user to a Workspace
- Make a user a System Administrator

Anything you can do with the Software UI, you can do programmatically with the Houston API.

## Schema overview

The Houston API uses the [GraphQL API](https://graphql.org/learn/) query language. You can make GraphQL requests using standard REST API tools such as [HTTP](https://www.apollographql.com/blog/making-graphql-requests-using-http-methods) and curl. GraphQL APIs support two main request types: _queries_ and _mutations_. You can run these requests against _objects_ which are similar to endpoints in REST APIs.

A _query_ is a request for specific information and is similar to a `GET` request in a REST API. The primary difference between GraphQL queries and Rest API queries is that GraphQL queries only return the fields that you specify within your request. For example, consider the following query to retrieve information about a user:

```graphql
query User {
  users(user: { email: "name@mycompany.com"} )
  {
    id
    roleBindings {role}
  }
}
```

The Houston API would only return the ID and role bindings for the user because those are the only fields specified in the query.

A _mutation_ is a request to update data for a specific object. Different mutations exist for creating, updating, and deleting objects. When you write a mutation request, it's best practice to use [variables](https://graphql.org/learn/queries/#variables) to store the data you want to update. For example, consider the following example mutation:

```graphql
mutation workspaceAddUser(
  $workspaceUuid: Uuid = "<your-workspace-uuid>"
  $email: String! = "<user-email-address>"
  $role: Role! = <user-workspace-role>
  $bypassInvite: Boolean! = true
) {
  workspaceAddUser(
    workspaceUuid: $workspaceUuid
    email: $email
    role: $role
    deploymentRoles: $deploymentRoles
    bypassInvite: $bypassInvite
  ) {
    id
  }
}
```

In this mutation, the values to update are formatted as variables in the first part of the request, then applied in the second half. Variables marked with a `!` are required in order for the query to complete. Lastly, the mutation requests the Houston API to return `id` of the added user to confirm that the mutation was successful. In this way, it's possible to make a mutation and a query in a single request. 

For more basic GraphQL usage rules and examples, see the [GraphQL documentation](https://graphql.org/learn/queries/).

## Prerequisites

There are no general prerequisites using the Houston API. However, the `upsertDeployment` mutation is behind a feature flag. To enable this feature on your Astronomer Software installation, set the following configuration in your `config.yaml` file:

```yaml
astronomer:
  houston:
    config:
      deployments:
        upsertDeploymentEnabled: true
```

Then push the configuration change to your cluster. See [Apply a config change](https://docs.astronomer.io/software/apply-platform-config).

## Authenticate to the Houston API

A Houston API request requires a token so that the request can be authenticated and authorized with a specific level of access on Astronomer Software. 

You can retrieve a token in one of the following ways:

- Create a [service account](ci-cd.md#step-1-create-a-service-account) and note its **API Key**. This is recommended for most production workflows.
- Go to `https://app.<your-base-domain>/token`, log in with your user account, and copy the API token that appears. This is recommended if you want to test API requests with your own user credentials. API tokens retrieved this way expire after 24 hours or when an Admin users changes your level of access.

You then need to add your token as an `Authorization` header to your Houston API requests. For example, the following curl command uses `'Authorization: <my-api-token>'` to authenticate a request to add a new Workspace user:

```sh
curl 'https://houston.mybasedomain.io/v1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://houston.mybasedomain.io' -H 'authorization: <my-api-token>' --data-binary '{"query":"mutation workspaceAddUser(\n    $workspaceUuid: Uuid = \"<your-workspace-uuid>\"\n    $email: String! = \"<user-email-address>\"\n    $role: Role! = <user-workspace-role>\n    $bypassInvite: Boolean! = true\n  ) {\n    workspaceAddUser(\n      workspaceUuid: $workspaceUuid\n      email: $email\n      role: $role\n      deploymentRoles: $deploymentRoles\n      bypassInvite: $bypassInvite\n    ) {\n      id\n    }\n  }"}' --compressed
```

## Develop and test Houston API queries

The Astronomer Houston API is available in a [GraphQL playground](https://www.apollographql.com/docs/apollo-server/v2/testing/graphql-playground/) where you can view the Houston API schema and documentation, as well as model, test, and export requests. To test requests in the playground, you must have a valid [authentication token](#authenticate-to-the-houston-api). 

1. Access the Astronomer Houston API GraphQL playground at `https://houston.<your-base-domain>/v1`.
2. Click **HTTP Headers**.
3. Add your authentication token in the following format:

    ```graphql
    {"authorization": "<your-api-token>"}
    ```

You can now run Houston API queries directly in your browser using the **Play** button in the GraphQL playground. 

## See also

- [Houston API examples](houston-api-examples.md)
