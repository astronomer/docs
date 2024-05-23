---
title: 'Deploy to Astro with the API'
sidebar_label: 'Deploy with API'
id: deploy-with-api
---

While you can deploy code to Astro using the GitHub Integration, the Astro CLI, or by configuring a CI/CD pipeline, you might prefer to use the Astro API to automate deploying code. Using the Astro API can solve some of the deploy automation issues that can result because some CI/CD configurations are not compatible with the GitHub Integration and the Astro CLI requires you to install Docker.

Instead of using the other code deploy options, you can instead use the Astro API Deploy endpoints to perform `IMAGE_ONLY`, `DAG_ONLY`, or both `IMAGE_AND_DAG` Deploys.

This guide contains a list of scenarios and the respective scripts that you can use to deploy code with the Astro API using bash scripts. It also includes an example of an entire deploy flow, in case you want to use those steps and integrate into your own CI/CD pipelines.

## Feature overview

This guide highlights the following Astro features to use for automating code deploys:

- The Astro API [`Deploy` endpoint](https://docs.astronomer.io/api/platform-api-reference/deploy/list-deploys) to create and manage code deploys to an Astro Deployment.

## Prerequisites

This use case assumes you have:

- Sufficient permissions to deploy code to your Astro Deployments
- At least one Astro Deployment
- The following values configured:
    - `ORGANIZATION_ID`
    - `DEPLOYMENT_ID`
    - `ASTRO_API_TOKEN` - See [Create an API token](https://docs.astronomer.io/astro/automation-authentication#step-1-create-an-api-token)
    - `AIRFLOW_PROJECT_PATH` - The path where your Airflow project exists.

## With DAG-only deploy enabled

### Complete deploy

1. Create the `Deploy`
    - Use the `IMAGE_AND_DAG` type
    - Retrieve the `id`, `imageRepository`, `imageTag`, and `dagsUploadURL`, which you need in the following steps.

2. Log in to Docker with the `ASTRO_API_TOKEN` that you created.

    ```bash

    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN

    ```

3. Build the Docker image using the `imageRepository`, `imageTag`, and `AIRFLOW_PROJECT_PATH` values that you retrieved earlier.

    ```bash

   docker build -t imageRepository:imageTag --platform=linux/amd64 $AIRFLOW_PROJECT_PATH

    ```

4. Push the Docker image using the `imageRepository` and `imageTag` values that you retrieved earlier.

    ```bash

    docker push imageRepository:imageTag

    ```

5. Create a tar file of the DAGs folder, where you specify the path where you want to create the tar file.

    ```bash

    tar -cvf <path to create the tar file>/dags.tar "dags"

    ```

    :::note

    Make sure to clean up the `dags.tar` file after uploading.

    :::

6. Upload the tar file by making a `PUT` call using the `dagsUploadURL` that you retrieved in Step 1. In this call, it is mandatory to pass the following. Then, save the `versionID` from the response header.

    ```bash

    --header 'x-ms-blob-type: BlockBlob'

    ```

7. Finalize the deploy

    - On `Success`, the deploy process has completed. Pass `versionID` in the requested body.
    - It might take a few minutes for the changes to update in your Deployment.

### DAG-only deploy

1. Create a`Deploy` with the `CREATE` call.
    - Use the `DAG_ONLY` type
    - Retrieve the `id` and `dagsUploadURL`, which you need in the following steps.

2. Create a tar file of the DAGs folder, where you specify the path where you want to create the tar file.

    ```bash

    tar -cvf <path to create the tar file>/dags.tar "dags"

    ```

    :::note

    Make sure to clean up the `dags.tar` file after uploading.

    :::

3. Upload the tar file by making a `PUT` call using the `dagsUploadURL` that you retrieved in Step 1. In this call, it is mandatory to pass the following. Then, save the `versionID` from the response header.

    ```bash

    --header 'x-ms-blob-type: BlockBlob'

    ```

4. Finalize the deploy

    - On `Success`, the deploy process has completed. Pass `versionID` in the requested body.
    - It might take a few minutes for the changes to update in your Deployment.

### Image-only deploy

1. Create the `Deploy`
    - Use the `IMAGE` type
    - Retrieve the `id`, `imageRepository`, and `imageTag`, which you need in the following steps.

2. Log in to Docker with the `ASTRO_API_TOKEN` that you created.

    ```bash

    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN

    ```

3. Build the Docker image using the `imageRepository`, `imageTag`, and `AIRFLOW_PROJECT_PATH` values that you retrieved earlier.

    ```bash

   docker build -t imageRepository:imageTag --platform=linux/amd64 $AIRFLOW_PROJECT_PATH

    ```

4. Push the Docker image using the `imageRepository` and `imageTag` values that you retrieved earlier.

    ```bash

    docker push imageRepository:imageTag

    ```

5. Finalize the deploy

    - On `Success`, the deploy process has completed. Pass the requested body as empty, `({})`.
    - It might take a few minutes for the changes to update in your Deployment.

## With DAG-only deploy disabled

:::info

You can only use complete deploys if you have DAG-only deploys disabled. Image-only and DAG-only deploys do not work.

:::

1. Create the `Deploy`
    - Use the `IMAGE_AND_DAG` type
    - Retrieve the `id`, `imageRepository`, and `imageTag`, which you need in the following steps.

2. Log in to Docker

    ```bash

    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN

    ```

3. Build the Docker image using the `imageRepository`, `imageTag`, and `AIRFLOW_PROJECT_PATH` values that you retrieved earlier.

    ```bash

    docker build -t imageRepository:imageTag --platform=linux/amd64 $AIRFLOW_PROJECT_PATH

    ```
4. Push the Docker image using the `imageRepository` and `imageTag` values that you retrieved earlier.

    ```bash

    docker push imageRepository:imageTag

    ```

5. Finalize the deploy

    - On `Success`, the deploy process has completed. Pass the requested body as empty, `({})`.
    - It might take a few minutes for the changes to update in your Deployment.
