---
title: 'View logs'
sidebar_label: 'View logs'
id: view-logs
description: View logs for your data pipelines both locally and on Astro.
---

View Airflow task and component logs to troubleshoot your data pipelines and better understand the behavior of your tasks and their execution environment.

## View Airflow task logs

Airflow task logs for both local Airflow environments and Deployments on Astro are available in the Airflow UI. Task logs can help you troubleshoot a specific task instance that failed or retried.

On Astro, Airflow task logs are stored in the data plane on your cloud. On Amazon Web Services (AWS), they are stored in S3. On Google Cloud Platform (GCP), they are stored in Cloud Storage. Task logs are stored indefinitely for existing Astro clusters. The task log retention policy is not currently configurable.

1.  Access the Airflow UI. To access the Airflow UI for a Deployment, open the Deployment in the Cloud UI and click **Open Airflow**. To access the Airflow UI in a local environment, open a browser and go to `http://localhost:8080`.
2. Click a DAG.
3. Click **Graph**.
4. Click a task run.
5. Click **Instance Details**.
6. Click **Log**.

## Access Airflow component logs locally

To show logs for your Airflow scheduler, webserver, or triggerer locally, run the following Astro CLI command:

```sh
astro dev logs
```

Once you run this command, the most recent logs for these components appear in your terminal window.

By default, running `astro dev logs` shows logs for all Airflow components. To see logs only for a specific component, add any of the following flags to your command:

- `--scheduler`
- `--webserver`
- `--triggerer`

To continue monitoring logs, run `astro dev logs --follow`. The `--follow` flag ensures that the latest logs continue to appear in your terminal window. For more information about this command, see [CLI Command Reference](cli/astro-dev-logs.md).

Logs for the Airflow webserver, worker, and triggerer are not available for Deployments on Astro.

## View Airflow scheduler logs

You can access the past 24 hours of scheduler logs for any Deployment on its **Logs** page. Logs are color-coded according to their type. Scheduler logs can help you understand scheduler performance and indicate if a task failed due to an issue with the scheduler. For more information on configuring the scheduler on Astro, see [Scheduler resources](configure-deployment-resources.md#scheduler-resources).

1. In the Cloud UI, select a Workspace and then a Deployment.

2. Click the **Logs** tab.

3. Optional. Select one or more options in the **Log Level** menu and click **Apply**. These are the available options:

    - **Error**: Emitted when a process fails or does not complete. For example, these logs might indicate a missing DAG file, an issue with your scheduler's connection to the Airflow database, or an irregularity with your scheduler's heartbeat.
    - **Warn**: Emitted when Airflow detects an issue that may or may not be of concern but does not require immediate action. This often includes deprecation notices marked as `DeprecationWarning`. For example, Airflow might recommend that you upgrade your Deployment if there was a change to the Airflow database or task execution logic.
    - **Info**: Emitted frequently by Airflow to show that a standard scheduler process, such as DAG parsing, has started. These logs are frequent but can contain useful information. If you run dynamically generated DAGs, for example, these logs will show how many DAGs were created per DAG file and how long it took the scheduler to parse each of them.

When a Deployment generates more than 500 lines of logs in 24 hours, only the most recent 500 lines are shown. If there are no scheduler logs available for a given Deployment, the following message appears:

```  
No matching events have been recorded in the past 24 hours.
```

Typically, this indicates that the Deployment you selected does not currently have any DAGs running.

## Export task logs to Datadog (_AWS only_)

Astro supports forwarding Airflow task logs to [Datadog](https://www.datadoghq.com/). You only need to enable Datadog once for each Astro cluster. After you enable Datadog, task logs from all Deployments in the cluster are exported.

1. Create a new Datadog API key or copy an existing API key. See [API and Application Keys](https://docs.datadoghq.com/account_management/api-app-keys/).
2. Identify the Astro cluster from which you want to forward task logs.
3. Submit a request to [Astronomer support](https://cloud.astronomer.io/support) with your Datadog API key, the name of your Astro cluster, and the [Datadog Site](https://docs.datadoghq.com/getting_started/site/) where you want the logs forwarded.

## Astro audit logs

Astro audit logs record Astro control plane administrative activities and events. You can use the audit logs to determine who did what, where, and when. You can also use audit logs to ensure your organization is meeting its security and regulatory requirements. For example, you can use audit logs to determine when users were added to your organization or to individual Workspaces.

### Available audit log data

The following categories of event data are available in the audit log:

- API events: The data generated by user actions in the Cloud UI, Astro CLI, or from internal processing actions in the Astro control plane.
- Airflow UI access: The data generated when users access the Airflow UI.
- Astronomer container registry access: The data generated when users access the Astronomer container registry with the Astro CLI.

The audit log file is provided as a JSON file. Every entry in the audit log file corresponds to an event, and event attributes provide additional information about the specific event. 

#### Common fields

The following table lists the common fields shared by all three categories of event data.

| Field  | Description                                          |
| ------- | ---------------------------------------------------- |
| `subjectId` | A unique identifier that identifies the initiator of the request. The value can be user ID or an API key. |
| `subjectType` | A unique identifier that identifies the subject of the request. The value can be `USER` or `SERVICEKEY`. |
| `organizationId` | A unique identifier that identifies your organization. This is the value displayed in the Cloud UI **Settings** page. |
| `timestamp` | The date and time the event occurred. |
| `sourceIp` | The IP address of the originating request. |
| `userAgent` | The application used to make the request. |
| `correlationId` | A unique identifier for the request. |

#### API event fields

The following table lists the fields that are unique to API events.

| Field  | Description                                          |
| ------- | ---------------------------------------------------- |
| `operationName` | The name of the API event. For example, `createUserInvite` or `workspaceCreate`. |
| `graphqlClientName` | The type of client making the request. The values are `cloud-ui` or `cli`. |
| `requestInput` | The input for the API request. |
| `requestBody` | Raw graphQL for the event. |

The following table maps some common `operationName` attributes to their corresponding `requestInput` attributes. 

| Event | `operationName` attribute                                          | `requestInput` attributes                   |
| ------- | ---------------------------------------------------- | --------------------------------- |
| A new user is invited to an organization.   | `createUserInvite` | `inviteeEmail`, `role` |
| A user has accepted their invite to an organization. | `updateUserInvite` |
| A user is deleted from an organization.  | `deleteUserInvite` | `inviteId` |
| A user is assigned a new role.  | `assignUserOrganizationRole` | `role`, `userId` |
| A user is removed from an organization.  | `deleteOrganizationUser` | `organizationId`, `userId` |
| A Workspace is created.  | `createWorkspace` | `label`, `organizationId` |
| A Workspace is updated.  | `updateWorkspace` | `label`, `id` |
| A Workspace is deleted.  | `deleteWorkspace` | `id` |
| A user is added to a Workspace, or a user role is updated. | `assignUserWorkspaceRole` | `email`, `role`, `workspaceId` |
| A user is removed from a workspace. | `deleteUserWorkspaceRole` | `userId`, `workspaceId` |
| A new Deployment is created. | `createDeployment` | `label`, `workspaceId` |
| A Deployment is updated. | `updateDeployment` | `deploymentSpec` |
| A Deployment variable is updated. | `updateDeploymentVariables` | `isSecret`, `key` |
| An API key is created for a Deployment. | `createDeploymentApiKey` | `deploymentId`, `role` |
| An API key is deleted for a Deployment. | `deleteDeploymentApiKey` | `id` |
| The code for a Deployment is updated. | `ImageCreate` | `deploymentId` |

Use your analytics or audit tool to view additional attribute mapping information. 

#### Airflow UI access event fields

The following table lists the fields that are unique to Airflow UI access events.

| Field  | Description                                          |
| ------- | ---------------------------------------------------- |
| `targetUrl` | The URL for the canonical name record in the Airflow webserver that runs in the Astro control dataplane. For example, `https://cl8gwrnw601f10tyxhgrhaayw.astronomer.run`.  |
| `path` | The relative path of the page being accessed. For example, `/dzl9chy4/configuration`.  |
| `method` | The HTTP method for the request. |

#### Astronomer container registry access event fields

The following table lists the fields that are unique to Astronomer container registry access events.

| Field  | Description                                          |
| ------- | ---------------------------------------------------- |
| `deploymentId` | A unique identifier that identifies the Deployment on which the event occurred. |
| `path` | The path to the image in the registry. |
| `method` | The HTTP method for the request. |

### Export audit logs

 Audit logs are retained for 90 days. Organization Owner permissions are required to export audit logs. 

 1. In the Cloud UI, click the **Settings** tab.

 2. Select the number days of audit data to export in the **Audit Logs** area and then click **Export**.

    The extracted audit log data is saved as a JSON file in your `downloads` directory with the default filename `<astro-organization-name>-logs-<number-of-days>-days-<date>.json`.

