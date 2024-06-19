---
title: "Astro API best practices"
sidebar_label: "Astro API"
description: "Several best practices to ensure a great experience using the Astro API"
id: astro-api-best-practices
---

The [Astro API](https://www.astronomer.io/docs/api) is Astronomer's REST API for managing resources on Astro, for example to create a deployment. Below are several topics regarding best practices for general REST API development, and specifically the Astro API, to ensure a safe and optimal user experience:

- Considerations for using the Astro API, CLI, and Terraform
- Error handling
- API tokens
- Use a graphical REST API client for development
- Handle rate limiting with exponential backoff retries

## Considerations for using the Astro API, CLI, and Terraform

Astronomer provides several tools to manage Astro resources. Each tool comes with its own use cases:

**Astro API**
- Structured input & output, therefore convenient for automation
- Can be used by any programming language to make HTTP requests
- Have to implement mechanisms such as waiting for deployment creation completed yourself

**Astro CLI**
- Provides a local development environment
- Human-readable output such as text or table format, therefore less suitable for automation
- Convenient for deploying code

**Astro Terraform provider**
- Industry standard tool for managing infrastructure as code
- Requires Terraform knowledge
- Hides complexity of API, generally fewer details to fill out

Which tool suits you best depends on factors such as your technical experience, existing knowledge within your organization, and usage of Astronomer. It's common to use all available tools.

## Error handling

It's a best practice to always expect the unexpected. Meaning, ensure your code handles unexpected situations such as errors properly. We generally make a distinction between client-side and server-side errors. For example, deployment names are unique within a workspace. If you were to create a second deployment with an already-existing name, the Astro API would return an HTTP 400 error. All HTTP 4XX code indicate a client-side error. Server-side errors are indicated by HTTP 5XX status codes, for example HTTP 500 indicates that something failed while handling the client's request. To ensure your code handles errors correctly, wrap requests in a try/except block:

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
            "type": "STANDARD",
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

Additionally, a best security practice is the principle of least privilege, where you grant only the permissions necessary to perform an action and no more. This reduces the attack surface (the number of ways to cause damage) in case of a leaked API token. Astronomer provides three levels of API tokens, from least to most privilege:

- [Deployment API tokens](deployment-api-tokens.md)
- [Workspace API tokens](workspace-api-tokens.md)
- [Organization API tokens](organization-api-tokens.md)

We advise creating API tokens with as little privileges as possible. When using an API token for actions on deployment-level, consider [custom Deployment roles](customize-deployment-roles.md) too.

## Use a graphical REST API client for development

The Astro API documentation already provides a convenient interface to try out the API:

![Astro API documentation](/img/docs/fern.png)

A graphical REST API client can be a helpful addition when developing against any REST API. Popular tools are [Postman](https://www.postman.com) and [Insomnia](https://insomnia.rest/products/insomnia). The Astro API documentation provides downloads to the API specifications which are YAML files that define the API structure, which you can load into your tool of choice: https://www.astronomer.io/docs/api/overview#download-openapi-specifications. Graphical REST API clients often provide convenience features over web-based documentation such as query history, sharing values via variables, ability to define environments with different values, create chained requests (use result from one query in a follow-up query), etc.

## Handle rate limiting with exponential backoff retries

The Astro API limits requests in case the request rate passes certain thresholds, depending on the type of the request: https://www.astronomer.io/docs/api/overview#rate-limiting. When a request is rate limited, the API will return an HTTP 429 status code.

It's a best practice to apply an exponential backoff strategy to not overload the server side for rate-limited requests. An exponential backoff strategy gradually increases the time between requests to allow for the server to recover and respond correctly, e.g. by waiting 1, 2, 4, 8 etc. seconds between consecutive requests. Say we're waiting for a deployment to receive status "HEALTHY" after creation. Creating a deployment can take a moment so repeatedly requesting the status from the Astro API without any pause in between requests will likely result in rate limiting. Here's how you could handle that:

```python {14-19,32-36}
import datetime
import requests
import time

organization_id = "..."
deployment_id = "..."
astro_api_token = "..."

timeout_secs = 600
timeout_attempts = 0
start = datetime.datetime.now()
while True:
    try:
        response = requests.get(
            f"https://api.astronomer.io/platform/v1beta1/organizations/{organization_id}/deployments/{deployment_id}",
            headers={"Authorization": f"Bearer {astro_api_token}"},
        )
        response.raise_for_status()
        timeout_attempts = 0
        
        deployment_status = response.json()["status"]
        if deployment_status == "HEALTHY":
            print("Deployment is healthy")
            break
        if (datetime.datetime.now() - start).total_seconds() > timeout_secs:
            raise Exception("Timeout")
        else:
            print(f"Deployment status is currently {deployment_status}. Waiting...")
            time.sleep(5)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            timeout_attempts += 1
            sleep_duration = 2 ** (timeout_attempts - 1)
            print(f"Request was rate limited. Sleeping {sleep_duration} seconds and trying again.")
            time.sleep(sleep_duration)
        else:
            print("Failed fetching deployment status. Reason: " + e.response.json()["message"])
            raise e
```

We check the HTTP response code and handle HTTP 429 separately from other response codes. While we likely won't hit any rate limit threshold on the Astro API running the script above since we wait 5 seconds between requests, running multiple scripts simultaneously can quickly add up. When receiving an HTTP 429 response we calculate a waiting period of `2 ** (timeout_attempts - 1)` seconds and gradually increase the period depending on the attempt number.

In the example above we defined our own logic for handling rate limits and exponential backoffs. While this works, the code is a bit lengthy and Python's [requests](https://requests.readthedocs.io) library comes with several built-in utilities to simplify the code. For example, you can avoid defining your own exponential backoff logic:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

session = requests.session()
ratelimit_retry = Retry(status_forcelist=[429], backoff_factor=1, total=10)
session.mount(prefix="https://api.astronomer.io", adapter=HTTPAdapter(max_retries=ratelimit_retry))
response = session.get(...)
```

`requests.session()` creates a persistent session between requests and replaces `requests.get(...)` by `session.get(...)` to use the settings configured in the session. This way you don't have to duplicate the same `if e.response.status_code == 429` business logic for every request. The `urllib3.Retry` object applies the same exponential backoff logic for HTTP status 429 up to 10 attempts, meaning it will wait 1, 2, 4, ..., 128, 256, 512 seconds in between the 10 attempts.

One more code simplification using Python's `requests` library is setting a default value for `headers`. While you could write `headers={"Authorization": f"Bearer {astro_api_token}"}` with every request, it's cleaner to define this only once and automatically apply it to every request using the `session` object:

```python
import requests

session = requests.session()
session.headers = {"Authorization": f"Bearer {astro_api_token}"}

# Before
requests.get(
    f"https://api.astronomer.io/platform/v1beta1/organizations/{organization_id}/deployments/{deployment_id}",
    headers={"Authorization": f"Bearer {astro_api_token}"},
)

# After
session.get(f"https://api.astronomer.io/platform/v1beta1/organizations/{organization_id}/deployments/{deployment_id}")
```

## Use `Keep-Alive` for repeated requests

