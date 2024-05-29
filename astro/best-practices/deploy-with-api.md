---
title: 'Deploy to Astro with the API'
sidebar_label: 'Deploy with API'
id: deploy-with-api
---

While you can deploy code using the Astro GitHub Integration, the Astro CLI, or by configuring a CI/CD pipeline, you might prefer to use the Astro API to automate deploying code. Using the Astro API is the most straightforward way to deploy code and requires very few additional dependencies, meaning it is compatible with most CI/CD configurations.

If the Astro API has access to your Astro project files, you can use the Astro API `deploy` endpoints to complete an image deploy or DAG deploy. You can then implement scripts to automate deploys as a workaround to not using the Astro CLI or Astro GitHub integration.

This best practice guide walks through the steps that are necessary to deploy code to Astro using the Astro API. It also provides example bash scripts that implement these steps for different types of deploy workflows in your own CI/CD pipelines. This example uses Docker to build the image, but you can use a similar tool like Kaniko.

## Feature overview

This guide highlights the following Astro features:

- The Astro API [`Deploy` endpoint](https://www.astronomer.io/api/platform-api-reference/deploy/list-deploys) to create and manage code deploys to an Astro Deployment.

## Prerequisites

These use cases assume you have:

- Sufficient permissions to deploy code to your Astro Deployments
- At least one [Astro Deployment](create-deployment.md)
- A container management tool. The following examples show commands using [Docker](https://www.docker.com/).
- The following values:
    - Your Organization ID - See [List Organizations](https://docs.astronomer.io/docs/api/platform-api-reference/organization/list-organizations)
    - The Deployment ID - See [List Deployments](https://docs.astronomer.io/docs/api/platform-api-reference/deployment/list-deployments)
    - Your Astro API token - See [Create an API token](https://www.astronomer.io/docs/astro/automation-authentication#step-1-create-an-api-token)
    - The path where your Astro project exists.

## With DAG-only deploy enabled

If you have DAG-only deploys enabled, you can create scripts for complete project deploys, DAG-only deploys, or image-only deploys. The following sections include a step by step description of the workflow followed by a bash script that executes the workflow.

### Project deploy

The following steps describe the different actions that the script performs to deploy a complete Astro project.

1. Create the `Deploy` API call. This action creates an object that represents the intent to deploy code to a Deployment.
    - Use the `IMAGE_AND_DAG` type.

2. After you create the `deploy`, retrieve the `id`, `imageRepository`, `imageTag`, and `dagsUploadURL` values, using the [`GET` deploy API call](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/get-deploy), which you need in the following steps.

3. Log in to Docker or your container management platform, using the Astro API token that you created.

    ```bash

    docker login images.astronomer.cloud -u cli -p $<your-api-token>

    ```

4. Build the image using the `imageRepository`, `imageTag`, and Astro project path values that you retrieved earlier.

    ```bash

   docker build -t imageRepository:imageTag --platform=linux/amd64 $ASTRO_PROJECT_PATH

    ```

5. Push the image using the `imageRepository` and `imageTag` values that you retrieved in Step 2.

    ```bash

    docker push imageRepository:imageTag

    ```

6. Create a tar file of the DAGs folder, where you specify the path where you want to create the tar file.

    ```bash

    tar -cvf <path to create the tar file>/dags.tar "dags"

    ```

    :::note

    Make sure to clean up the `dags.tar` file after uploading.

    :::

7. Upload the tar file by making a `PUT` call using the `dagsUploadURL` that you retrieved in Step 2. In this call, it is mandatory to pass the following. Then, save the `versionID` from the response header.

    ```bash

    --header 'x-ms-blob-type: BlockBlob'

    ```

8. Finalize the deploy. See [Finalize the deploy](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/finalize-deploy) for more information about the API request.

    - On `Success`, the deploy process has completed. Pass `versionID` in the requested body.
    - It might take a few minutes for the changes to update in your Deployment.

<details>
  <summary><strong>Complete deploy script</strong></summary>

    ```bash

    #!/bin/bash

    ORGANIZATION_ID=<set organization id>
    DEPLOYMENT_ID=<set deployment id>
    ASTRO_API_TOKEN=<set api token>
    ASTRO_PROJECT_PATH=<set path to your Astro project>

    # Initializing Deploy
    echo -e "Initiating Deploy Process for deployment $DEPLOYMENT_ID\n"
    CREATE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys" \
    --header "X-Astro-Client-Identifier: script" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $ASTRO_API_TOKEN" \
    --data '{
    "type": "IMAGE_AND_DAG"
    }' | jq '.')

    DEPLOY_ID=$(echo $CREATE_DEPLOY | jq -r '.id')

    # Build and Push Docker Image
    REPOSITORY=$(echo $CREATE_DEPLOY | jq -r '.imageRepository')
    TAG=$(echo $CREATE_DEPLOY | jq -r '.imageTag')
    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN
    echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $ASTRO_PROJECT_PATH"
    docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $ASTRO_PROJECT_PATH
    echo -e "\nPushing Docker image $REPOSITORY:$TAG to $DEPLOYMENT_ID"
    docker push $REPOSITORY:$TAG

    # Upload dags tar file
    DAGS_UPLOAD_URL=$(echo $CREATE_DEPLOY | jq -r '.dagsUploadUrl')
    echo -e "\nCreating a dags tar file from $ASTRO_PROJECT_PATH/dags and stored in $ASTRO_PROJECT_PATH/dags.tar\n"
    cd $AIRFLOW_PROJECT_PATH
    tar -cvf "$ASTRO_PROJECT_PATH/dags.tar" "dags"
    echo -e "\nUploading tar file $ASTRO_PROJECT_PATH/dags.tar\n"
    VERSION_ID=$(curl -i --request PUT $DAGS_UPLOAD_URL \
    --header 'x-ms-blob-type: BlockBlob' \
    --header 'Content-Type: application/x-tar' \
    --upload-file "$ASTRO_PROJECT_PATH/dags.tar" | grep x-ms-version-id | awk -F': ' '{print $2}')

    VERSION_ID=$(echo $VERSION_ID | sed 's/\r//g') # Remove unexpected carriage return characters
    echo -e "\nTar file uploaded with version: $VERSION_ID\n"

    # Finalizing Deploy
    FINALIZE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys/$DEPLOY_ID/finalize" \
    --header "X-Astro-Client-Identifier: script" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $ASTRO_API_TOKEN" \
    --data '{"dagTarballVersion": "'$VERSION_ID'"}')

    ID=$(echo $FINALIZE_DEPLOY | jq -r '.id')
    if [[ "$ID" != null ]]; then
            echo -e "\nDeploy is Finalized. Image and DAG changes for deployment $DEPLOYMENT_ID should be live in a few minutes"
            echo "Deployed Image tag: $TAG"
            echo "Deployed DAG Tarball Version: $VERSION_ID"
    else
            MESSAGE=$(echo $FINALIZE_DEPLOY | jq -r '.message')
            if  [[ "$MESSAGE" != null ]]; then
                    echo $MESSAGE
            else
                    echo "Something went wrong. Reach out to astronomer support for assistance"
            fi
    fi

    # Cleanup
    echo -e "\nCleaning up the created tar file from $ASTRO_PROJECT_PATH/dags.tar"
    rm -rf "$ASTRO_PROJECT_PATH/dags.tar"

    ```

</details>

### DAG-only deploy

1. Create the `Deploy` API call. This action creates an object that represents the intent to deploy code to a Deployment.
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

<details>
  <summary><strong>DAG-only deploy script</strong></summary>

  ```bash
  #!/bin/bash

    ORGANIZATION_ID=<set organization id>
    DEPLOYMENT_ID=<set deployment id>
    ASTRO_API_TOKEN=<set api token>
    ASTRO_PROJECT_PATH=<set path to your airflow project>

    # Initializing Deploy
    echo -e "Initiating Deploy Process for deployment $DEPLOYMENT_ID\n"
    CREATE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys" \
    --header "X-Astro-Client-Identifier: script" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $ASTRO_API_TOKEN" \
    --data '{
    "type": "DAG_ONLY"
    }' | jq '.')

    DEPLOY_ID=$(echo $CREATE_DEPLOY | jq -r '.id')

    # Upload dags tar file
    DAGS_UPLOAD_URL=$(echo $CREATE_DEPLOY | jq -r '.dagsUploadUrl')
    echo -e "\nCreating a dags tar file from $ASTRO_PROJECT_PATH/dags and stored in $ASTRO_PROJECT_PATH/dags.tar\n"
    cd $AIRFLOW_PROJECT_PATH
    tar -cvf "$ASTRO_PROJECT_PATH/dags.tar" "dags"
    echo -e "\nUploading tar file $ASTRO_PROJECT_PATH/dags.tar\n"
    VERSION_ID=$(curl -i --request PUT $DAGS_UPLOAD_URL \
    --header 'x-ms-blob-type: BlockBlob' \
    --header 'Content-Type: application/x-tar' \
    --upload-file "$ASTRO_PROJECT_PATH/dags.tar" | grep x-ms-version-id | awk -F': ' '{print $2}')

    VERSION_ID=$(echo $VERSION_ID | sed 's/\r//g') # Remove unexpected carriage return characters
    echo -e "\nTar file uploaded with version: $VERSION_ID\n"

    # Finalizing Deploy
    FINALIZE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys/$DEPLOY_ID/finalize" \
    --header "X-Astro-Client-Identifier: script" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $ASTRO_API_TOKEN" \
    --data '{"dagTarballVersion": "'$VERSION_ID'"}')

    ID=$(echo $FINALIZE_DEPLOY | jq -r '.id')
    if [[ "$ID" != null ]]; then
            echo -e "\nDeploy is Finalized. DAG changes for deployment $DEPLOYMENT_ID should be live in a few minutes"
            echo "Deployed DAG Tarball Version: $VERSION_ID"
    else
            MESSAGE=$(echo $FINALIZE_DEPLOY | jq -r '.message')
            if  [[ "$MESSAGE" != null ]]; then
                    echo $MESSAGE
            else
                    echo "Something went wrong. Reach out to astronomer support for assistance"
            fi
    fi

    # Cleanup
    echo -e "\nCleaning up the created tar file from $ASTRO_PROJECT_PATH/dags.tar"
    rm -rf "$ASTRO_PROJECT_PATH/dags.tar"

  ```

</details>

### Image-only deploy

1. Create the `Deploy` API call. This action creates an object that represents the intent to deploy code to a Deployment.
    - Use the `IMAGE` type
    - Retrieve the `id`, `imageRepository`, and `imageTag`, which you need in the following steps.

2. Log in to Docker with the `ASTRO_API_TOKEN` that you created.

    ```bash

    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN

    ```

3. Build the Docker image using the `imageRepository`, `imageTag`, and `ASTRO_PROJECT_PATH` values that you retrieved earlier.

    ```bash

   docker build -t imageRepository:imageTag --platform=linux/amd64 $ASTRO_PROJECT_PATH

    ```

4. Push the Docker image using the `imageRepository` and `imageTag` values that you retrieved earlier.

    ```bash

    docker push imageRepository:imageTag

    ```

5. Finalize the deploy

    - On `Success`, the deploy process has completed. Pass the requested body as empty, `({})`.
    - It might take a few minutes for the changes to update in your Deployment.

<details>
  <summary><strong>Image-only deploy script</strong></summary>

  ```bash
    #!/bin/bash

    ORGANIZATION_ID=<set organization id>
    DEPLOYMENT_ID=<set deployment id>
    ASTRO_API_TOKEN=<set api token>
    ASTRO_PROJECT_PATH=<set path to your airflow project>

    # Initializing Deploy
    echo -e "Initiating Deploy Process for deployment $DEPLOYMENT_ID\n"
    CREATE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys" \
    --header "X-Astro-Client-Identifier: script" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $ASTRO_API_TOKEN" \
    --data '{
    "type": "IMAGE_ONLY"
    }' | jq '.')

    DEPLOY_ID=$(echo $CREATE_DEPLOY | jq -r '.id')

    # Build and Push Docker Image
    REPOSITORY=$(echo $CREATE_DEPLOY | jq -r '.imageRepository')
    TAG=$(echo $CREATE_DEPLOY | jq -r '.imageTag')
    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN
    echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $ASTRO_PROJECT_PATH"
    docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $ASTRO_PROJECT_PATH
    echo -e "\nPushing Docker image $REPOSITORY:$TAG to $DEPLOYMENT_ID"
    docker push $REPOSITORY:$TAG

    # Finalizing Deploy
    FINALIZE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys/$DEPLOY_ID/finalize" \
    --header "X-Astro-Client-Identifier: script" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $ASTRO_API_TOKEN" \
    --data '{}')

    ID=$(echo $FINALIZE_DEPLOY | jq -r '.id')
    if [[ "$ID" != null ]]; then
            echo -e "\nDeploy is Finalized. Image changes for deployment $DEPLOYMENT_ID should be live in a few minutes"
            echo "Deployed Image tag: $TAG"
    else
            MESSAGE=$(echo $FINALIZE_DEPLOY | jq -r '.message')
            if  [[ "$MESSAGE" != null ]]; then
                    echo $MESSAGE
            else
                    echo "Something went wrong. Reach out to astronomer support for assistance"
            fi
    fi
  ```
</details>

## With DAG-only deploy disabled

You can only use complete project deploys if you have DAG-only deploys disabled. Image-only and DAG-only deploys do not work.

### Project deploy

1. Create the `Deploy` API call. This action creates an object that represents the intent to deploy code to a Deployment.
    - Use the `IMAGE_AND_DAG` type
    - Retrieve the `id`, `imageRepository`, and `imageTag`, which you need in the following steps.

2. Log in to Docker

    ```bash

    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN

    ```

3. Build the Docker image using the `imageRepository`, `imageTag`, and `ASTRO_PROJECT_PATH` values that you retrieved earlier.

    ```bash

    docker build -t imageRepository:imageTag --platform=linux/amd64 $ASTRO_PROJECT_PATH

    ```
4. Push the Docker image using the `imageRepository` and `imageTag` values that you retrieved earlier.

    ```bash

    docker push imageRepository:imageTag

    ```

5. Finalize the deploy

    - On `Success`, the deploy process has completed. Pass the requested body as empty, `({})`.
    - It might take a few minutes for the changes to update in your Deployment.

<details>
  <summary><strong>Complete code deploy script</strong></summary>

  ```bash
    #!/bin/bash

    ORGANIZATION_ID=<set organization id>
    DEPLOYMENT_ID=<set deployment id>
    ASTRO_API_TOKEN=<set api token>
    ASTRO_PROJECT_PATH=<set path to your airflow project>

    # Initializing Deploy
    echo -e "Initiating Deploy Process for deployment $DEPLOYMENT_ID\n"
    CREATE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys" \
    --header "X-Astro-Client-Identifier: script" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $ASTRO_API_TOKEN" \
    --data '{
    "type": "IMAGE_AND_DAG"
    }' | jq '.')

    DEPLOY_ID=$(echo $CREATE_DEPLOY | jq -r '.id')

    # Build and Push Docker Image
    REPOSITORY=$(echo $CREATE_DEPLOY | jq -r '.imageRepository')
    TAG=$(echo $CREATE_DEPLOY | jq -r '.imageTag')
    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN
    echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $ASTRO_PROJECT_PATH"
    docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $ASTRO_PROJECT_PATH
    echo -e "\nPushing Docker image $REPOSITORY:$TAG to $DEPLOYMENT_ID"
    docker push $REPOSITORY:$TAG

    # Finalizing Deploy
    FINALIZE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys/$DEPLOY_ID/finalize" \
    --header "X-Astro-Client-Identifier: script" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $ASTRO_API_TOKEN" \
    --data '{}')

    ID=$(echo $FINALIZE_DEPLOY | jq -r '.id')
    if [[ "$ID" != null ]]; then
            echo -e "\nDeploy is Finalized. Image and DAG changes for deployment $DEPLOYMENT_ID should be live in a few minutes"
            echo "Deployed Image tag: $TAG"
    else
            MESSAGE=$(echo $FINALIZE_DEPLOY | jq -r '.message')
            if  [[ "$MESSAGE" != null ]]; then
                    echo $MESSAGE
            else
                    echo "Something went wrong. Reach out to astronomer support for assistance"
            fi
    fi
  ```
</details>

## Trigger deploys when files change

In addition to manually triggering project, DAG, and image deploys, you can create scripts that trigger specific code deploys depending on whether there have been changes to DAGs or files used to build the project image.

The following code example shows the steps you can use to create a bash script that triggers different code deploys depending on the files changed in your project.

### Workflow example steps

1. Determine whether DAG files have been changed. If only DAGs have changed, then the script initiates a DAG-only deploy.

2. Create a`Deploy` with the `CREATE` call.

3. If only DAGs have changed, the script initiates a DAGs-only deploy. If more files have been changed, the script builds and deploys the project image, and then completes a DAG-only deploy.

4. The script cleans up any tar files created during the build process.

<details>
<summary><strong>Trigger deploys code example</strong></summary>

```bash
#!/bin/bash

ORGANIZATION_ID=<set organization id>
DEPLOYMENT_ID=<set deployment id>
ASTRO_API_TOKEN=<set api token>
AIRFLOW_PROJECT_PATH=<set path to your airflow project>

# Determine if only DAG files have changes
files=$(git diff --name-only $(git rev-parse HEAD~1) -- .)
dags_only=1
for file in $files;do
if [[ $file != "$AIRFLOW_PROJECT_PATH/dags"* ]];then
    echo "$file is not a dag, triggering a full image build"
    dags_only=0
    break
fi
done

# Initializing Deploy
echo -e "Initiating Deploy Process for deployment $DEPLOYMENT_ID\n"
CREATE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys" \
--header "X-Astro-Client-Identifier: script" \
--header "Content-Type: application/json" \
--header "Authorization: Bearer $ASTRO_API_TOKEN" \
--data '{
   "type": "IMAGE_AND_DAG"
}' | jq '.')

DEPLOY_ID=$(echo $CREATE_DEPLOY | jq -r '.id')

# If only DAGs changed deploy only the DAGs in your 'dags' folder to your Deployment
if [ $dags_only == 1 ]
then
	# Upload dags tar file
	DAGS_UPLOAD_URL=$(echo $CREATE_DEPLOY | jq -r '.dagsUploadUrl')
	echo -e "\nCreating a dags tar file from $AIRFLOW_PROJECT_PATH/dags and stored in $AIRFLOW_PROJECT_PATH/dags.tar\n"
	cd $AIRFLOW_PROJECT_PATH
	tar -cvf "$AIRFLOW_PROJECT_PATH/dags.tar" "dags"
	echo -e "\nUploading tar file $AIRFLOW_PROJECT_PATH/dags.tar\n"
	VERSION_ID=$(curl -i --request PUT $DAGS_UPLOAD_URL \
	--header 'x-ms-blob-type: BlockBlob' \
	--header 'Content-Type: application/x-tar' \
	--upload-file "$AIRFLOW_PROJECT_PATH/dags.tar" | grep x-ms-version-id | awk -F': ' '{print $2}')

	VERSION_ID=$(echo $VERSION_ID | sed 's/\r//g') # Remove unexpected carriage return characters
	echo -e "\nTar file uploaded with version: $VERSION_ID\n"

	# Finalizing Deploy
	FINALIZE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys/$DEPLOY_ID/finalize" \
	--header "X-Astro-Client-Identifier: script" \
	--header "Content-Type: application/json" \
	--header "Authorization: Bearer $ASTRO_API_TOKEN" \
	--data '{"dagTarballVersion": "'$VERSION_ID'"}')

	ID=$(echo $FINALIZE_DEPLOY | jq -r '.id')
	if [[ "$ID" != null ]]; then
	        echo -e "\nDeploy is Finalized. DAG changes for deployment $DEPLOYMENT_ID should be live in a few minutes"
	        echo "Deployed DAG Tarball Version: $VERSION_ID"
	else
	        MESSAGE=$(echo $FINALIZE_DEPLOY | jq -r '.message')
	        if  [[ "$MESSAGE" != null ]]; then
	                echo $MESSAGE
	        else
	                echo "Something went wrong. Reach out to astronomer support for assistance"
	        fi
	fi

	# Cleanup
	echo -e "\nCleaning up the created tar file from $AIRFLOW_PROJECT_PATH/dags.tar"
	rm -rf "$AIRFLOW_PROJECT_PATH/dags.tar"
fi
# If any other files changed build your Astro project into a Docker image, push the image to your Deployment, and then push and DAG changes
if [ $dags_only == 0 ]
then
   # Build and Push Docker Image
	REPOSITORY=$(echo $CREATE_DEPLOY | jq -r '.imageRepository')
	TAG=$(echo $CREATE_DEPLOY | jq -r '.imageTag')
	docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN
	echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $AIRFLOW_PROJECT_PATH"
	docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $AIRFLOW_PROJECT_PATH
	echo -e "\nPushing Docker image $REPOSITORY:$TAG to $DEPLOYMENT_ID"
	docker push $REPOSITORY:$TAG

	# Upload dags tar file
	DAGS_UPLOAD_URL=$(echo $CREATE_DEPLOY | jq -r '.dagsUploadUrl')
	echo -e "\nCreating a dags tar file from $AIRFLOW_PROJECT_PATH/dags and stored in $AIRFLOW_PROJECT_PATH/dags.tar\n"
	cd $AIRFLOW_PROJECT_PATH
	tar -cvf "$AIRFLOW_PROJECT_PATH/dags.tar" "dags"
	echo -e "\nUploading tar file $AIRFLOW_PROJECT_PATH/dags.tar\n"
	VERSION_ID=$(curl -i --request PUT $DAGS_UPLOAD_URL \
	--header 'x-ms-blob-type: BlockBlob' \
	--header 'Content-Type: application/x-tar' \
	--upload-file "$AIRFLOW_PROJECT_PATH/dags.tar" | grep x-ms-version-id | awk -F': ' '{print $2}')

	VERSION_ID=$(echo $VERSION_ID | sed 's/\r//g') # Remove unexpected carriage return characters
	echo -e "\nTar file uploaded with version: $VERSION_ID\n"

	# Finalizing Deploy
	FINALIZE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys/$DEPLOY_ID/finalize" \
	--header "X-Astro-Client-Identifier: script" \
	--header "Content-Type: application/json" \
	--header "Authorization: Bearer $ASTRO_API_TOKEN" \
	--data '{"dagTarballVersion": "'$VERSION_ID'"}')

	ID=$(echo $FINALIZE_DEPLOY | jq -r '.id')
	if [[ "$ID" != null ]]; then
	        echo -e "\nDeploy is Finalized. Image and DAG changes for deployment $DEPLOYMENT_ID should be live in a few minutes"
	        echo "Deployed Image tag: $TAG"
	        echo "Deployed DAG Tarball Version: $VERSION_ID"
	else
	        MESSAGE=$(echo $FINALIZE_DEPLOY | jq -r '.message')
	        if  [[ "$MESSAGE" != null ]]; then
	                echo $MESSAGE
	        else
	                echo "Something went wrong. Reach out to astronomer support for assistance"
	        fi
	fi

	# Cleanup
	echo -e "\nCleaning up the created tar file from $AIRFLOW_PROJECT_PATH/dags.tar"
	rm -rf "$AIRFLOW_PROJECT_PATH/dags.tar"
fi
```
</details>