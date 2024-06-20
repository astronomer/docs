---
title: 'Deploy to Astro with the API'
sidebar_label: 'Deploy with API'
id: deploy-with-api
---

While you can deploy code using the Astro GitHub integration, the Astro CLI, or by configuring a CI/CD pipeline, there are some environments where you can only use the Astro API to deploy code. This is because using the Astro API has very few dependencies, making it compatible with almost all CI/CD environments and security requirements.

If the Astro API has access to your Astro project files, you can use the Astro API `deploy` endpoints to complete an image deploy or DAG deploy. You can then implement scripts to automate deploys as an alternative to using the Astro CLI or Astro GitHub integration.

This best practice guide walks through the steps that are necessary to deploy code to Astro using the Astro API. It also provides example bash scripts that implement these steps for different types of deploy workflows in your own CI/CD pipelines. This example uses Docker to build the image, but you can use a similar tool like Kaniko. You can also use a different scripting language, like Python, instead of bash.

## Feature overview

This guide highlights the following Astro features:

- The Astro API [`Deploy` endpoint](https://www.astronomer.io/api/platform-api-reference/deploy/list-deploys) to create and manage code deploys to an Astro Deployment.

## Prerequisites

These use cases assume you have:

- An [API token](deployment-api-tokens.md) with sufficient permissions to deploy code to Astro.
- At least one [Astro Deployment](create-deployment.md).
- An [Astro project](cli/develop-project.md) that's accessible from the machine where you're using the Astro API.
- A container management tool. The following examples use [Docker](https://www.docker.com/).
- The following values:
  - Your Organization ID - See [List Organizations](https://docs.astronomer.io/docs/api/platform-api-reference/organization/list-organizations).
  - The Deployment ID - See [List Deployments](https://docs.astronomer.io/docs/api/platform-api-reference/deployment/list-deployments).
  - Your Astro API token - See [Create an API token](https://www.astronomer.io/docs/astro/automation-authentication#step-1-create-an-api-token).
  - The path where your Astro project exists.

## With DAG-only deploys enabled

If you have DAG-only deploys enabled, you can create scripts for complete project deploys, DAG-only deploys, or image-only deploys. The following sections include a step by step description of the workflow followed by a bash script that executes the workflow.

### Project deploy

The following steps describe the different actions that the script performs to deploy a complete Astro project.

1. Make a `POST` request to the `Deploy` endpoint to create a new `deploy` object. In your call, specify `type` as `IMAGE_AND_DAG`. Store the value for the `DeployID` that is returned. This action creates an object that represents the intent to deploy code to a Deployment. See the [Astro API documentation](https://www.astronomer.io/docs/api/platform-api-reference/deploy/create-deploy) for request usage and examples.

2. Make a `GET` request to the `Deploy` endpoint. Copy the values for `id`, `imageRepository`, `imageTag`, and `dagsUploadURL` to use in the following steps. See the [Astro API documentation](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/get-deploy) for request usage and examples.

3. Authenticate to Astronomer's image registry using your Astro API token:

   ```bash

   docker login images.astronomer.cloud -u cli -p <your-api-token>

   ```

4. Build the image using the `imageRepository` and `imageTag` values that you retrieved in Step 2, as well as your Astro project path.

   ```bash

   docker build -t imageRepository:imageTag --platform=linux/amd64 <astro_project_path>

   ```

5. Push the image using the `imageRepository` and `imageTag` values that you retrieved in Step 2.

   ```bash

   docker push imageRepository:imageTag

   ```

6. Create a tar file of your Astro project DAGs folder:

   ```bash

   tar -cvf <path-to-create-tar-file>/dags.tar "dags"

   ```

   :::info

   Make sure to clean up the `dags.tar` file after uploading.

   :::

7. Upload the tar file by making a `PUT` call using the `dagsUploadURL` that you retrieved in Step 2. In this call, it is mandatory to pass the `x-ms-blob-type` as `BlockBlob`. Then, save the `versionID` from the response header.

8. Using your `DeployId`, make a request to finalize the deploy. See [Astro API documentation](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/finalize-deploy) for more information about formatting the API request.

   - On `Success`, your DAGs have successfully uploaded and a `versionID` of the DAGs tarball is generated. Pass this `versionID` in the requested body to finish your updates.
   - It might take a few minutes for the changes to update in your Deployment.

<details>
  <summary><strong>Complete project deploy script</strong></summary>

    ```bash

    # Prerequisites
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
    REPOSITORY=$(echo $CREATE_DEPLOY | jq -r '.imageRepository')
    TAG=$(echo $CREATE_DEPLOY | jq -r '.imageTag')
    DAGS_UPLOAD_URL=$(echo $CREATE_DEPLOY | jq -r '.dagsUploadUrl')

    # Log in to docker and build docker image
    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN
    echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $ASTRO_PROJECT_PATH"
    docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $ASTRO_PROJECT_PATH
    echo -e "\nPushing Docker image $REPOSITORY:$TAG to $DEPLOYMENT_ID"
    docker push $REPOSITORY:$TAG

    # Step 7: Upload dags tar file
    echo -e "\nCreating a dags tar file from $ASTRO_PROJECT_PATH/dags and stored in $ASTRO_PROJECT_PATH/dags.tar\n"
    cd $ASTRO_PROJECT_PATH
    tar -cvf "$ASTRO_PROJECT_PATH/dags.tar" "dags"
    echo -e "\nUploading tar file $ASTRO_PROJECT_PATH/dags.tar\n"
    VERSION_ID=$(curl -i --request PUT $DAGS_UPLOAD_URL \
    --header 'x-ms-blob-type: BlockBlob' \
    --header 'Content-Type: application/x-tar' \
    --upload-file "$ASTRO_PROJECT_PATH/dags.tar" | grep x-ms-version-id | awk -F': ' '{print $2}')

    VERSION_ID=$(echo $VERSION_ID | sed 's/\r//g') # Remove unexpected carriage return characters
    echo -e "\nTar file uploaded with version: $VERSION_ID\n"

    # Step 8: Finalizing Deploy
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

1. Make a `POST` request to the `Deploy` endpoint to create a new `deploy` object. In your call, specify `type` as `DAG_ONLY`. Store the value for the `DeployID` that is returned. This action creates an object that represents the intent to deploy code to a Deployment. See the [Astro API documentation](https://www.astronomer.io/docs/api/platform-api-reference/deploy/create-deploy) for request usage and examples.

2. Make a `GET` request to the `Deploy` endpoint. Copy the values for `id` and `dagsUploadURL` to use in the following steps. See the [Astro API documentation](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/get-deploy) for request usage and examples.

3. Create a tar file of your Astro project DAGs folder:

   ```bash

   tar -cvf <path to create the tar file>/dags.tar "dags"

   ```

   :::note

   Make sure to clean up the `dags.tar` file after uploading.

   :::

4. Upload the tar file by making a `PUT` call using the `dagsUploadURL` that you retrieved in Step 2. In this call, it is mandatory to pass the `x-ms-blob-type` as `BlockBlob`. Then, save the `versionID` from the response header.

5. Using your `DeployId`, make a request to finalize the deploy. See [Astro API documentation](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/finalize-deploy) for more information about formatting the API request.

   - On `Success`, your DAGs have successfully uploaded and a `versionID` of the DAGs tarball is generated. Pass this `versionID` in the requested body to finish your updates.
   - It might take a few minutes for the changes to update in your Deployment.

<details>
  <summary><strong>DAG-only deploy script</strong></summary>

        ```bash

        # Prerequisites
        #!/bin/bash

        ORGANIZATION_ID=<set organization id>
        DEPLOYMENT_ID=<set deployment id>
        ASTRO_API_TOKEN=<set api token>
        ASTRO_PROJECT_PATH=<set path to your airflow project>

        # Step 1: Initializing deploy
        echo -e "Initiating Deploy Process for deployment $DEPLOYMENT_ID\n"
        CREATE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys" \
        --header "X-Astro-Client-Identifier: script" \
        --header "Content-Type: application/json" \
        --header "Authorization: Bearer $ASTRO_API_TOKEN" \
        --data '{
        "type": "DAG_ONLY"
        }' | jq '.')

        DEPLOY_ID=$(echo $CREATE_DEPLOY | jq -r '.id')

        # Step 2-4: Copy Deploy ID and Upload URL, create tar file, and upload DAGs tar file
        DAGS_UPLOAD_URL=$(echo $CREATE_DEPLOY | jq -r '.dagsUploadUrl')
        echo -e "\nCreating a dags tar file from $ASTRO_PROJECT_PATH/dags and stored in $ASTRO_PROJECT_PATH/dags.tar\n"
        cd $ASTRO_PROJECT_PATH
        tar -cvf "$ASTRO_PROJECT_PATH/dags.tar" "dags"
        echo -e "\nUploading tar file $ASTRO_PROJECT_PATH/dags.tar\n"
        VERSION_ID=$(curl -i --request PUT $DAGS_UPLOAD_URL \
        --header 'x-ms-blob-type: BlockBlob' \
        --header 'Content-Type: application/x-tar' \
        --upload-file "$ASTRO_PROJECT_PATH/dags.tar" | grep x-ms-version-id | awk -F': ' '{print $2}')

        VERSION_ID=$(echo $VERSION_ID | sed 's/\r//g') # Remove unexpected carriage return characters
        echo -e "\nTar file uploaded with version: $VERSION_ID\n"

        # Step 5: Finalizing Deploy
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

1.  Make a `POST` request to the `Deploy` endpoint to create a new `deploy` object. In your call, specify `type` as `IMAGE`. Store the value for the `DeployID` that is returned. This action creates an object that represents the intent to deploy code to a Deployment.  See the [Astro API documentation](https://www.astronomer.io/docs/api/platform-api-reference/deploy/create-deploy) for request usage and examples.

2. Make a `GET` request to the `Deploy` endpoint. Copy the values for `id`, `imageRepository`, and `imageTag` to use in the following steps. See the [Astro API documentation](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/get-deploy) for request usage and examples.

3. Log in to Docker with your Astro API token.

   ```bash

   docker login images.astronomer.cloud -u cli -p <your_astro_api_token>

   ```

4. Build the image using the `imageRepository` and `imageTag` values that you retrieved in Step 2, as well as your Astro project path.

   ```bash

   docker build -t imageRepository:imageTag --platform=linux/amd64 <astro_project_path>

   ```

5. Push the image using the `imageRepository` and `imageTag` values that you retrieved earlier.

   ```bash

   docker push imageRepository:imageTag

   ```

6. Using your `DeployId`, make a request to finalize the deploy. See [Astro API documentation](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/finalize-deploy) for more information about formatting the API request.

   - On `Success`, your DAGs have successfully uploaded and a `versionID` of the DAGs tarball is generated. Pass this `versionID` in the requested body to finish your updates.
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

1. Create the `Deploy` API call using the `IMAGE_AND_DAG` type. This action creates an object that represents the intent to deploy code to a Deployment.

2. After you create the `deploy`, retrieve the `id`, `imageRepository`, and `imageTag` values using the [`GET` deploy API call](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/get-deploy), which you need in the following steps.

3. Log in to Docker

   ```bash

   docker login images.astronomer.cloud -u cli -p <your_astro_api_token>

   ```

4. Build the Docker image using the `imageRepository`, `imageTag`, and Astro project path values that you retrieved earlier.

   ```bash

   docker build -t imageRepository:imageTag --platform=linux/amd64 <astro_project_path>

   ```

5. Push the Docker image using the `imageRepository` and `imageTag` values that you retrieved earlier.

   ```bash

   docker push imageRepository:imageTag

   ```

6. Finalize the deploy. See [Finalize the deploy](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/finalize-deploy) for more information about the API request.

   - On `Success`, the new image has successfully uploaded. Since you didn't update any DAGs in this deploy, pass the requested body as empty, `({})`.
   - It might take a few minutes for the changes to update in your Deployment.

<details>
  <summary><strong>Complete project deploy script</strong></summary>

        ```bash

        #Prerequisites
        #!/bin/bash

        ORGANIZATION_ID=<set organization id>
        DEPLOYMENT_ID=<set deployment id>
        ASTRO_API_TOKEN=<set api token>
        ASTRO_PROJECT_PATH=<set path to your airflow project>

        # Step 1: Initializing Deploy
        echo -e "Initiating Deploy Process for deployment $DEPLOYMENT_ID\n"
        CREATE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys" \
        --header "X-Astro-Client-Identifier: script" \
        --header "Content-Type: application/json" \
        --header "Authorization: Bearer $ASTRO_API_TOKEN" \
        --data '{
        "type": "IMAGE_AND_DAG"
        }' | jq '.')

        DEPLOY_ID=$(echo $CREATE_DEPLOY | jq -r '.id')

        # Step 2-5: Build and Push Docker Image
        REPOSITORY=$(echo $CREATE_DEPLOY | jq -r '.imageRepository')
        TAG=$(echo $CREATE_DEPLOY | jq -r '.imageTag')
        docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN
        echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $ASTRO_PROJECT_PATH"
        docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $ASTRO_PROJECT_PATH
        echo -e "\nPushing Docker image $REPOSITORY:$TAG to $DEPLOYMENT_ID"
        docker push $REPOSITORY:$TAG

        # Step 6: Finalizing Deploy
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

The following code example shows the steps you can use to create a bash script that triggers different code deploys depending on the files changed in your project. This example demonstrates a recommended way for combining all three types of deploys and the conditional logic for when to deploy each.

### Workflow example steps

1. Determine whether DAG files have been changed. If only DAGs have changed, then the script initiates a DAG-only deploy.

2. Make a `POST` request to the `Deploy` endpoint to create a new `deploy` object.

3. If only DAGs have changed, the script initiates a DAGs-only deploy. If you changed more files, the script builds and deploys the project image, and then completes a DAG-only deploy.

4. The script cleans up any tar files created during the build process.

<details>
<summary><strong>Trigger deploys code example</strong></summary>

```bash
#!/bin/bash

ORGANIZATION_ID=<set organization id>
DEPLOYMENT_ID=<set deployment id>
ASTRO_API_TOKEN=<set api token>
ASTRO_PROJECT_PATH=<set path to your airflow project>

# Determine if only DAG files have changes
files=$(git diff --name-only $(git rev-parse HEAD~1) -- .)
dags_only=1
for file in $files;do
if [[ $file != "$ASTRO_PROJECT_PATH/dags"* ]];then
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
	echo -e "\nCreating a dags tar file from $ASTRO_PROJECT_PATH/dags and stored in $ASTRO_PROJECT_PATH/dags.tar\n"
	cd $ASTRO_PROJECT_PATH
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
fi
# If any other files changed build your Astro project into a Docker image, push the image to your Deployment, and then push and DAG changes
if [ $dags_only == 0 ]
then
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
	cd $ASTRO_PROJECT_PATH
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
fi
```

</details>
