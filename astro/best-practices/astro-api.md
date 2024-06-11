---
title: "Astro API best practices"
sidebar_label: "Astro API"
description: "Several best practices to ensure a great experience using the Astro API"
id: astro-api-best-practices
---

The Astro API is Astronomer's REST API for managing resources on Astro, for example to create a deployment. Below are several topics regarding best practices for the Astro API to ensure a safe and optimal user experience:

- Use the latest API version
- Error handling
- API tokens

## Use the latest API version

The version of the Astro API is contained in the URL. Take for example the following URL: `https://api.astronomer.io/platform/v1beta1/organizations/organizationId/deployments`. The value `v1beta1` indicates you're querying version `v1beta1` of the Astro API. It's a best practice to upgrade soon to ensure no last-minute hectic upgrades are needed, and newer versions of the same endpoints are generally more stable. Read more details on the Astro API's versioning and support policy [here](https://www.astronomer.io/docs/astro/api/versioning-and-support).

## Error handling

It's a best practice to always expect the unexpected. Meaning, ensure your code handles unexpected situations such as errors properly. For example, deployment names are unique within a workspace. If you were to create a second deployment with an already-existing name, the Astro API would return an error. To ensure your code handles errors properly, wrap requests in a try/except block:

```python
import requests

organization_id = "..."
workspace_id = "..."
astro_api_token = "..."

try:
    response = requests.post(
        f"https://api.astronomer.io/platform/v1beta1/organizations/{organization_id}/deployments",
        headers={"Authorization": f"Bearer {astro_api_token}"},
        json={
            "astroRuntimeVersion": "{{RUNTIME_VER}}",
            "clusterId": "cabcdefgh12ij34klmn567op8",
            "defaultTaskPodCpu": "0.25",
            "defaultTaskPodMemory": "0.5Gi",
            "executor": "CELERY",
            "isCicdEnforced": False,
            "isDagDeployEnabled": False,
            "isHighAvailability": False,
            "name": "my_deployment",  # <== this will fail if "my_deployment" already exists
            "resourceQuotaCpu": "10",
            "resourceQuotaMemory": "20Gi",
            "schedulerSize": "SMALL",
            "type": "DEDICATED",
            "workspaceId": workspace_id,
        },
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print("Failed creating deployment. Reason: " + e.response.json()["message"])
    raise e
```

The statement `response.raise_for_status()` raises an exception on any HTTP code that's not 2XX, which are HTTP codes for non-successful requests. In the `except` clause you can then handle the exception in any way you wish. In case of an error, the Astro API returns a reason in the response body, key `message`, with HTTP code 400 for this specific request. We print the error reason because without that, we wouldn't know why a request failed. In the case of an already-existing deployment name, the logs will show:

```text
Failed creating deployment. Reason: Invalid request: Deployment name 'my_deployment' already exists in this workspace
```

The complete error response structure is:

```json
{
    "message": "Invalid request: Deployment name 'my_deployment' already exists in this workspace",
    "requestId": "f004d12a-29c8-40d8-b239-2b1b615ea45b",
    "statusCode": 400
}
```

For traceability purposes, you could also include the `requestId` in your logs, which is an internal Astronomer identifier that Astronomer support can use to track down your request.

## API tokens

In automated scripts such as CI/CD pipelines where there's no human in the loop, the Astro API can be queried using an API token. An API token grants access to certain Astronomer resources and it's therefore important to keep the token safe. Do **_not_** hardcode the token in code! Instead, store the token in a secret and expose it as an environment variable `ASTRO_API_TOKEN`:

```shell
export ASTRO_API_TOKEN=...
... run script ...
```

Storing API tokens in a system dedicated for storing secret values, for example [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository), ensures secret values are not visible to humans and only referenced by code when needed. 

Additionally, a best security practice is the principle of least privilege, where you grant only the required permissions to an API token and no more. This reduces the attack surface (the number of ways to cause damage) in case of a leaked API token. Astronomer provides three levels of API tokens, from least to most privilege:

- [Deployment API tokens](deployment-api-tokens.md)
- [Workspace API tokens](workspace-api-tokens.md)
- [Organization API tokens](organization-api-tokens.md)
