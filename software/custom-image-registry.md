---
title: 'Configure a custom registry for Deployment images'
sidebar_label: 'Configure a custom image registry'
id: custom-image-registry
description: Replace Astronomer's built-in container image registry with your own.
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

Astronomer Software includes access to a Docker image registry that is managed by Astronomer. Every time a user deploys to Astronomer Software, a Docker image is generated and pushed to this registry. Depending on your deploy method, these Docker images can include OS and Python dependencies, DAG code, and the Airflow service.

Using the Astronomer registry is recommended when you're getting started and your team is comfortable deploying code. However, the Astronomer registry might not meet your organization's security requirements.

If your organization can't support the Astronomer default internal registry, you can configure a custom container image registry. This option is best suited for organizations who require additional control for security and governance reasons. Using a custom registry provides your organization with the opportunity to scan images for CVEs, malicious code, and unapproved Python and OS-level packages contained in Docker images.

:::info

A custom registry can still connect to public networks or internet. Therefore, this procedure is different if you're installing Astronomer in an airgapped environment. If you need to create a custom registry for a system that can't connect to the public networks or internet, see [Install Astronomer in an airgapped environment](install-airgapped.md).

:::

## Implementation considerations

Deploying code changes to a custom image registry requires triggering a GraphQL mutation to provide a Deployment release name, image name, and Airflow version to the registry. Because this process is difficult to manually trigger, Astronomer recommends configuring a custom image registry only if your DAG authors can deploy code changes using continuous integration and continuous delivery (CI/CD) pipelines. In this implementation, you use your CI/CD tool to:

- Build your Astro project into a container image.
- Deploy the image to your custom registry.
- Run a query to push the image from your registry to Astronomer Software.

## Prerequisites

- Helm.
- kubectl.
- Astro CLI version 1.3.0+.
- A custom container image registry.
- A process for building and pushing your Astro projects as images to your custom registry.

## Setup

<Tabs
    defaultValue="standard"
    groupId= "setup"
    values={[
        {label: 'Standard', value: 'standard'},
        {label: 'Airgapped', value: 'airgapped'},
    ]}>
<TabItem value="standard">

1. Create a secret for the container repository credentials in your Astronomer namespace:

    ```bash
    kubectl -n <astronomer-platform-namespace> create secret docker-registry <name-of-secret> --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-password> --docker-email=<your-email>
    ```

    To have Astronomer Software sync the registry credentials to all Deployment namespaces, add the following annotation:

    ```bash
    kubectl -n <astronomer-platform-namespace> annotate secret <name-of-secret> "astronomer.io/commander-sync"="platform=astronomer"
    ```

  :::info

  To use different registries for each Deployment, create the same secret in each Deployment namespace instead of your Astronomer namespace. Make sure to specify different custom registries using `--docker-server`. If you don't need to synch your secrets between deployments, you don't need to add the secret annotation.

  :::

2. Open your `config.yaml` file. See [Apply a Config Change](https://docs.astronomer.io/software/apply-platform-config).
3. Add the following to your `config.yaml` file:

    ```yaml
    astronomer:
      houston:
        config:
          deployments:
            enableUpdateDeploymentImageEndpoint: true
          registry:
            protectedCustomRegistry:
              enabled: true
              updateRegistry:
                enabled: true
                host: <your-airflow-image-repo>
                secretName: <name-of-secret>
    ```

  :::info

  To use different registries for each Deployment, do not set `astronomer.houston.config.deployments.registry.protectedCustomRegistry.updateRegistry.host`.

  :::

4. Push the configuration change. See [Apply a config change](https://docs.astronomer.io/software/apply-platform-config).
5. For any existing Deployments, run the following command to sync the registry credentials.

    ```bash
    kubectl create job -n <astronomer-platform-namespace> --from=cronjob/<platform-release-name>-config-syncer upgrade-config-synchronization
    ```

    :::info

    If you're using different registries for each Deployment, skip this step.

    :::

</TabItem>

<TabItem value="airgapped">

### Airgapped

1. Create a secret for the container repository credentials in your Astronomer namespace:

    ```bash
    kubectl -n <your-namespace> create secret docker-registry <name-of-secret> --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-password> --docker-email=<your-email>
    ```

    To have Astronomer Software sync the registry credentials to all Deployment namespaces, add the following annotation:

    ```bash
    kubectl -n <astronomer-platform-namespace> annotate secret <name-of-secret> "astronomer.io/commander-sync"="platform=astronomer"
    ```

  :::info

  To use different registries for each Deployment, create the same secret in each Deployment namespace instead of your Astronomer namespace. Make sure to specify different custom registries using `--docker-server`. You don't need to add the annotation if you're not synccing secrets between Deployments.


  :::

2. Open your `config.yaml` file. See [Apply a Config Change](https://docs.astronomer.io/software/apply-platform-config).

3. Add the following to your `config.yaml` file:

    ```yaml
    astronomer:
      houston:
        config:
          deployments:
            enableUpdateDeploymentImageEndpoint: true
            helm:
              airflow:
                defaultAirflowRepository: <airflow-image-repo>
                images:
                  airflow:
                    repository: <airflow-image-repo>
          registry:
            protectedCustomRegistry:
              enabled: true
              baseRegistry:
                enabled: true
                host: <airflow-image-repo>
                secretName: <name-of-secret-containing-image-repo-creds>
              updateRegistry:
                enabled: true
                host: <airflow-image-repo>
                secretName: <name-of-secret-containing-image-repo-creds>
    ```

  :::info

  To use different registries for each Deployment, do not set `astronomer.registry.protectedCustomRegistry.updateRegistry.host` or `astronomer.registry.protectedCustomRegistry.baseRegistry.host`.

  :::

4. Push the configuration change. See [Apply a config change](https://docs.astronomer.io/software/apply-platform-config).
5. For any existing Deployments, run the following command to sync the registry credentials. If you're using different registries for each Deployment, you can skip this step.

    ```bash
    kubectl create job -n <astronomer-platform-namespace> --from=cronjob/<platform-release-name>-config-syncer upgrade-config-synchronization
    ```


</TabItem>
</Tabs>

## Push code to a custom registry

You can use the Astro CLI to push build and push images from a Kubernetes cluster to your custom registry. Based on the Helm configurations in your Kubernetes cluster, the Astro CLI automatically detects your custom image registry and pushes your image to it. It then calls the Houston API to update your Deployment to pull the new image from the registry.

Within your Kubernetes cluster, open your Astro project and run:

```sh
astro deploy
```

Alternatively, you can run a GraphQL query to update the image in your Deployment after manually pushing the image to the custom registry. This can be useful for automating code deploys using CI/CD.

At a minimum, your query has to include the following:

```graphql
mutation updateDeploymentImage {
        updateDeploymentImage(
                releaseName: "<deployment-release-name>", # for example "analytics-dev"
                image: "<host>/<image-name>:<tag>",  # for example docker.io/cmart123/ap-airflow:test4
                runtimeVersion: "<runtime-version-number>" # for example "5.0.6"
        )
        {
                id
        }
}
```

Alternatively, you can run this same query using curl:

```bash
curl 'https://houston.BASEDOMAIN/v1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://houston.BASEDOMAIN/v1' -H 'Authorization: <your-token>' --data-binary '{"query":"mutation updateDeploymentImage {updateDeploymentImage(releaseName: \"<deployment-release-name>\", image: \"<host>/<image-name>:<tag>\",runtimeVersion: \"<runtime-version-number>\"){id}}"}' --compressed
```
