---
sidebar_label: 'Example API requests'
title: 'Example Houston API requests'
id: houston-api-examples
description: Examples of some of the most common queries you might make to the Astronomer Software Houston API
---

Use the following example Houston API requests as the basis for your applications developed for Astronomer Software. 

## Example queries

The following sample queries can be used to retrieve common information for specific Astronomer objects.

### Query Deployment details

The `workspaceDeployment` query can be used to retrieve details about a Deployment in a given Workspace. It requires the following inputs:

- **Workspace ID**: To retrieve this value, run `astro workspace list`. Alternatively, open a Workspace in the Software UI and copy the value after `/w/` in your Workspace URL (for example `https://app.basedomain/w/<workspace-id>`).
- **Deployment release name**: To retrieve this value, run `astro deployment list` in your Workspace. Alternatively, you can copy the **Release name** from your Deployment's **Settings** tab in the Software UI.

and can return any of the fields under `Type Details`:

- `config`
- `uuid`
- `status`
- `createdAt`
- `updatedAt`
- `roleBindings`
- etc.

For instance, you can run the following query to retrieve the Deployment's:

- ID
- Health status
- Creation time
- Update time
- Users

```graphql
query workspaceDeployment {
  workspaceDeployment(
    releaseName: "mathematical-probe-2087"
    workspaceUuid: "ck35y9uf44y8l0a19cmwd1x8x"
  )
  {
    id
    status
    createdAt
    updatedAt
    roleBindings {id, role, user{}} 
  }
}
```

### Query user details

A common query is `users`, which lets you retrieve information about multiple users at once. To use this query, you must provide:

- At least one of the following `userSearch` values:

    - `userId` (String): The user's ID
    - `userUuid`(String): The user's unique ID
    - `username` (String): The user's username
    - `email` (String): The user's email
    - `fullName` (String): The user's full name
    - `createdAt`(DateTime): When the user was created
    - `updatedAt`(DateTime): When the user was updated
  
- **Workspace ID**: To retrieve this value, run `astro workspace list`. Alternatively, open a Workspace in the Software UI and copy the value after `/w/` in your Workspace URL (for example `https://app.basedomain/w/<workspace-id>`).

The query returns the requested details for all users who exactly match the values provided for the `userSearch`. For example, the following query would retrieve the requested values for any user accounts with the email `name@mycompany.com`


```graphql
query User {
  users(user: { email: "<name@mycompany.com>"} )
  {
    id
    roleBindings {role}
    status
    createdAt
  }
}
```

## Example mutations

Mutations make a change to your platform's underlying database. For some common examples, read below.

### Create a Deployment

To create a Deployment, you'll need Workspace Admin permissions and a -**Workspace ID**. To retrieve this value, run `astro workspace list`. Alternatively, open a Workspace in the Software UI and copy the value after `/w/` in your Workspace URL (for example `https://app.basedomain/w/<workspace-id>`).

This example mutation creates a Deployment with the Celery executor and the latest Runtime version. It then returns the Deployment's ID and configuration to confirm that it was successfully created. 

```graphql
mutation CreateDeployment {
  createDeployment(
    workspaceUuid: "<workspace-id>",
    type: "airflow",
    label: "<deployment-name>",
    executor:CeleryExecutor,
    runtimeVersion: "{{RUNTIME_VER}}"
    )
    {
      id
      executor
      releaseName
      workspace{label}
      roleBindings{id}
    }
}
```

### Create or update a Deployment with configurations

:::info 

The `upsertDeployment` mutation is behind a feature flag. To enable this feature, set the following configuration in your `config.yaml` file:

```yaml
astronomer:
  houston:
    config:
      deployments:
        upsertDeploymentEnabled: true
```

Then push the configuration change to your cluster. See [Apply a config change](https://docs.astronomer.io/software/apply-platform-config).

:::

The `upsertDeployment` mutation can be used to both create and update Deployments with all possible Deployment configurations. If you query `upsertDeployment` without a `deploymentUuid`, the Houston API creates a new Deployment according to your specifications. If you specify an existing `deploymentUuid`, the Houston API updates the Deployment with that ID. All queries to create a Deployment require specifying a `workspaceUuid`.

The following query creates a new Deployment in a custom namespace `test-new-dep` and configures a Deployment environment variable `AIRFLOW__CORE__COLORED_LOG_FORMAT`.

```graphql
mutation upsertDeployment(
  $workspaceUuid: Uuid,
  $deploymentUuid: Uuid,
  $label: String,
  $description: String,
  $releaseName: String,
  $namespace: String,
  $environmentVariables: [InputEnvironmentVariable],
  $image: String,
  $dockerconfigjson: JSON,
  $version: String,
  $airflowVersion: String,
  $runtimeVersion: String,
  $desiredRuntimeVersion: String,
  $executor: ExecutorType,
  $workers: Workers,
  $webserver: Webserver,
  $scheduler: Scheduler,
  $triggerer: Triggerer,
  $dagDeployment: DagDeployment,
  $properties: JSON,
  $cloudRole: String
) {
  upsertDeployment(
    workspaceUuid: $workspaceUuid,
    deploymentUuid: $deploymentUuid,
    label: $label,
    description: $description,
    releaseName: $releaseName,
    namespace: $namespace,
    environmentVariables: $environmentVariables,
    image: $image,
    dockerconfigjson: $dockerconfigjson,
    version: $version,
    airflowVersion: $airflowVersion,
    runtimeVersion: $runtimeVersion,
    desiredRuntimeVersion: $desiredRuntimeVersion,
    executor: $executor,
    workers: $workers,
    webserver: $webserver,
    scheduler: $scheduler,
    triggerer: $triggerer,
    dagDeployment: $dagDeployment,
    properties: $properties,
    cloudRole: $cloudRole
) {
    id
    config
    urls {
      type
      url
      __typename
    }
    properties
    description
    label
    releaseName
    namespace
    status
    type
    version
    workspace {
      id
      label
      __typename
    }
    airflowVersion
    runtimeVersion
    desiredAirflowVersion
    upsertedEnvironmentVariables {
      key
      value
      isSecret
      __typename
    }
    dagDeployment {
      type
      nfsLocation
      repositoryUrl
      branchName
      syncInterval
      syncTimeout
      ephemeralStorage
      dagDirectoryLocation
      rev
      sshKey
      knownHosts
      __typename
    }
    createdAt
    updatedAt
    __typename
  }
}
{
  "workspaceUuid": "cldemxl9502454yxe6vjlxy23",
	"environmentVariables": [
    {
      "key": "AIRFLOW__CORE__COLORED_LOG_FORMAT",
      "value": "test",
      "isSecret": false
    }
  ],
  "releaseName": "",
  "namespace": "test-new-dep",
  "executor": "CeleryExecutor",
  "workers": {},
  "webserver": {},
  "scheduler": {
    "replicas": 1
  },
  "label": "test-new-dep",
  "description": "",
  "runtimeVersion": "7.2.0",
  "properties": {
    "extra_au": 0
  },
  "dagDeployment": {
    "type": "image",
    "nfsLocation": "",
    "repositoryUrl": "",
    "branchName": "",
    "syncInterval": 1,
    "syncTimeout": 120,
    "ephemeralStorage": 2,
    "dagDirectoryLocation": "",
    "rev": "",
    "sshKey": "",
    "knownHosts": ""
  }
}
```

### Delete a Deployment

To delete a Deployment, you'll need:

- Either System Admin or Workspace Admin permissions
- A Deployment ID. To retrieve this value, run `astro deployment list` or request the `id` value in the `workspaceDeployment` query.

The following example mutation deletes a Deployment, then returns the ID of the Deployment to confirm that it was successfully deleted. 

```graphql
mutation DeleteDeployment {
  deleteDeployment (
    deploymentUuid: "<deployment-id>"
  ) {
    id
  }
}
```

### Create a Deployment user

To add an existing Astronomer Software user to a Deployment, you'll need. 

- Workspace Admin privileges
- A Deployment ID. To retrieve this value, run `astro deployment list` or request the `id` value in the `workspaceDeployment` query.
- The ID of the user to add. To retrieve this, request the `id` value in a `users` query or run `astro workspace user list`.
- The role to add the user as. Can be `DEPLOYMENT_ADMIN`, `DEPLOYMENT_EDITOR`, or `DEPLOYMENT_VIEWER`.

The following query adds a user to a Deployment as a Deployment viewer,. then returns the user and Deployment information back to the requester. 

```graphql
mutation AddDeploymentUser(
		$userId: "f9182b1d-2f7c-4d33-920b-2124b1660d83"
		$email: "usertoadd@mycompany.com"
		$deploymentId: "<deploymentId>"
		$role: DEPLOYMENT_VIEWER
	) {
		deploymentAddUserRole(
			userId: $userId
			email: $email
			deploymentId: $deploymentId
			role: $role
		) {
			id
			user {
				username
			}
			role
			deployment {
				id
				releaseName
			}
		}
	}
```

### Delete a user

To delete a user from Astronomer Software, you'll need:

- System Admin permissions
- The ID of the user to delete. To retrieve this, request the `id` value in a `users` query or run `astro workspace user list`.

The following query removes a user, then returns information about the deleted user. 

```graphql
mutation removeUser {
	removeUser (
    userUuid: "<user-id>"
  ) {
    uuid
    emails {address}
    status
  }
}
```

### Verify user email

If a user on the platform has trouble verifying their email address, you can use the Houston API to manually verify it for them.

To run this mutation, you'll need:

- System Admin Permissions
- The user's email address. Additionally, ensure that the user has already begun creating an account on the platform. They must have signed up for an account, and Astronomer Software must already have generated an invite token for the user. 

The following request verifies the email and returns `true` or `false` based on whether the mutation was successful. 

```graphql
mutation verifyEmail {
	verifyEmail (
    email: "<user-email>"
  )
}
```

### Bypass user email verification

If you don't need certain users to verify their email before they join a Workspace, you can configure a bypass when you add them to a Workspace. This can be useful for minimizing friction when programmatically inviting many users to your platform.

To run this mutation, you'll need:

- Workspace Admin permissions
- A -**Workspace ID**. To retrieve this value, run `astro workspace list`. Alternatively, open a Workspace in the Software UI and copy the value after `/w/` in your Workspace URL (for example `https://app.basedomain/w/<workspace-id>`).
- The user's email address.
- The user's desired role in the Workspace (`WORKSPACE_ADMIN`, `WORKSPACE_EDITOR`, `WORKSPACE_USER`).

The following example mutation can be run to add a user to a Workspace as a `WORKSPACE_USER`.

```graphql
mutation workspaceAddUser(
    $workspaceUuid: Uuid = "<your-workspace-uuid>"
    $email: String! = "<user-email-address>"
    $role: Role! = WORKSPACE_USER
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

### Add a System Admin

To add a user as a System Admin through the Houston API, you'll need the following values: 

- To retrieve this, request the `id` value in a `users` query or run `astro workspace user list`.
- System Admin permissions

You can then run the following query to add the user as a System Admin.

```graphql
mutation createSystemRoleBinding (
    $userId: "<user-id>"
    $role: SYSTEM_ADMIN
) {
  createSystemRoleBinding(
    userId: $userId
    role: $role
  ) {
    id
  }
}
```

### Update environment variables

To programmatically update environment variables, you'll need:

- A Deployment ID. To retrieve this value, run `astro deployment list` or request the `id` value in the `workspaceDeployment` query.
- A Deployment release name: To retrieve this value, run `astro deployment list` in your Workspace. Alternatively, you can copy the **Release name** from your Deployment's **Settings** tab in the Software UI.
  

Then, in your GraphQL Playground, run the following:

```graphql
mutation UpdateDeploymentVariables {
  updateDeploymentVariables(
    deploymentUuid: "<deployment-id>",
  	releaseName: "<deployment-release-name>",
    environmentVariables: [
      {key: "<environment-variable-1>",
      value: "<environment-variable-value-1>",
      isSecret: <true-or-false>},
      {key: "<environment-variable-2>",
      value: "<environment-variable-value-2>",
      isSecret: <true-or-false>}
    ]
  ) {
    key
    value
    isSecret
  }
}
```