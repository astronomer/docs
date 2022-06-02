---
title: 'Configure a Custom Registry for Deployment Images'
sidebar_label: 'Configure a Custom Image Registry'
id: custom-image-registry
description: Replace Astronomer's built-in container image registry with your own.
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

## Overview

Astronomer Software includes access to a Docker image registry that is managed by Astronomer. Every time a user deploys to Astronomer Software, a Docker image is generated and pushed to this registry. Depending on your deploy method, these Docker images can include OS and Python dependencies, DAG code, and the Airflow service itself.

Using Astronomer's registry is easiest if you're just getting started and your team is comfortable deploying code as described in [Deploy DAGs via CLI](deploy-cli.md), but it might not comply with the security requirements of your organization.

If your organization cannot support Astronomer's default internal registry, you can configure a custom container image registry instead. This option is best suited for mature organizations who require additional control for security and governance reasons. Using a custom registry provides your organization with the opportunity to scan images for CVEs, malicious code, and unapproved Python and OS-level packages contained in the Docker images that are generated during the code deploy process.

## Implementation Considerations

Deploying code changes to a custom image registry requires triggering a GraphQL mutation to provide a Deployment release name, image name, and Airflow version to the registry. Because this process is difficult to manually trigger, Astronomer recommends configuring a custom image registry only if your DAG authors can deploy code changes via CI/CD pipelines. In this implementation, you would use your CI/CD tool to:

1. Build your Astro project into a container image.
2. Deploy the image to your custom registry.
3. Run a query to push the image from your registry to Astronomer Software.

## Prerequisites

To configure this feature, you need:

- Helm.
- kubectl.
- A custom container image registry.
- A process for building and pushing your Astro projects as images to your custom registry.

## Setup

<Tabs
    defaultValue="standard"
    values={[
        {label: 'Standard', value: 'standard'},
        {label: 'Airgapped', value: 'airgapped'},
    ]}>
<TabItem value="standard">

1. Create a secret for the container repository credentials in your Astronomer namespace:

    ```bash
    kubectl -n <your-namespace> create secret docker-registry <name-of-secret> --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-password> --docker-email=<your-email>
    ```

    To have Astronomer Software sync the registry credentials to all Deployment namespaces, add the following annotation:

    ```bash
    kubectl -n <release-namespace> annotate secret <name-of-secret> "astronomer.io/commander-sync"="platform=astronomer"
    ```

  :::info

  To use different registries for each Deployment, create the same secret in each Deployment namespace instead of your Astronomer namespace, making sure to specify different custom registries using `--docker-server`. Because you don’t need to sync secrets between Deployments, you should not add the annotation as described in this step.

  :::

2. Locate your `config.yaml` file. To retrieve it programmatically, run:

    ```bash
    # platform-release-name is usually "astronomer"
    helm get values <your-platform-release-name> astronomer/astronomer -n astronomer
    ```

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
        	        enabled: false
        	        host: <your-airflow-image-repo>
        	        secretName: <name-of-secret>
    ```

  :::info

  To use different registries for each Deployment, do not set `astronomer.houston.config.deployments.registry.protectedCustomRegistry.updateRegistry.host`.

  :::

4. Push the configuration change as described in [Apply a Config Change](https://docs.astronomer.io/software/apply-platform-config)
5. For any existing Deployments, run the following command to sync registry credentials.

    ```bash
    kubectl create job -n <release-namespace> --from=cronjob/astronomer-config-syncer upgrade-config-synchronization
    ```

    :::info

    If you're using different registries for each Deployment, skip this step.

    :::

</TabItem>

<TabItem value="airgapped">

### Air-Gapped

1. Create a secret for the container repository credentials in your Astronomer namespace:

    ```bash
    kubectl -n <your-namespace> create secret docker-registry <name-of-secret> --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-password> --docker-email=<your-email>
    ```

    To have Astronomer Software sync the registry credentials to all Deployment namespaces, add the following annotation:

    ```bash
    kubectl -n <release-namespace> annotate secret <name-of-secret> "astronomer.io/commander-sync"="platform=astronomer"
    ```

  :::info

  To use different registries for each Deployment, create the same secret in each Deployment namespace instead of your Astronomer namespace, making sure to specify different custom registries using `--docker-server`. Because you don’t need to sync secrets between Deployments, you should not add the annotation as described in this step.

  :::

2. Locate your `config.yaml` file. To retrieve it programmatically, run:

    ```bash
    # platform-release-name is usually "astronomer"
    helm get values <your-platform-release-name> astronomer/astronomer -n astronomer
    ```

3. Add the following to your `config.yaml` file:

    ```yaml
    astronomer:
      houston:
        config:
          deployments:
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

4. Push the configuration change as described in [Apply a Config Change](https://docs.astronomer.io/software/apply-platform-config)
5. For any existing Deployments, run the following command to sync registry credentials.

    ```bash
    kubectl create job -n <release-namespace> --from=cronjob/astronomer-config-syncer upgrade-config-synchronization
    ```

  :::info

  If you're using different registries for each Deployment, skip this step.

  :::

</TabItem>
</Tabs>

## Push Code to a Custom Registry

After pushing images for your Astro project to your private registry, you can run a GraphQL query to push these images from your registry to Astronomer Software. At a minimum, your query has to include the following:

```graphql
mutation updateDeploymentImage {
	updateDeploymentImage(
		releaseName: "<deployment-release-name>", # for example "analytics-dev"
		image: "<host>/<image-name>:<tag>",  # for example docker.io/cmart123/ap-airflow:test4
		airflowVersion: "<airflow-version-number>" # for example "2.2.5"
	)
	{
		id
	}
}
```

Alternatively, you can run this same query using curl:

```bash
curl 'https://houston.BASEDOMAIN/v1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://houston.BASEDOMAIN/v1' -H 'Authorization: <your-token>' --data-binary '{"query":"mutation updateDeploymentImage {updateDeploymentImage(releaseName: \"<deployment-release-name>\", image: \"<host>/<image-name>:<tag>\",airflowVersion: \"<airflow-version-number>\"){id}}"}' --compressed
```
