---
title: 'Deploy to Astro with the API'
sidebar_label: 'Deploy with API'
id: deploy-with-api
---

While you can deploy your Apache Airflow code to Astro using the Astro GitHub integration, the Astro CLI, or by configuring a CI/CD pipeline, your organization might prefer to use the Astro API to deploy code. This is because using the Astro API has very few dependencies, making it compatible with almost all CI/CD environments and security requirements.

If the Astro API has access to your Astro project files, you can use the `deploy` endpoints in the Astro API to complete either a complete project deploy, image-only deploy or DAG-only deploy. You can then implement scripts to automate deploys as an alternative to using the Astro CLI or the Astro GitHub integration.

This best practice guide first walks through the steps that are necessary to deploy code to Astro using the Astro API for three different code deploy methods:

- A complete project deploy
- An image-only deploy
- A DAGs-only deploy

Then, the guide shows you the recommended way to combine these three automated processes to create a script with conditional logic that can automatically deploy code to Astro, depending on which types of files change in your Astro project. These examples are bash scripts that use Docker to build the image, but you can use a similar tool like [kaniko](https://github.com/GoogleContainerTools/kaniko). You can also use a different scripting language, like Python, instead of bash.


## Feature overview

This guide highlights the following Astro features:

- The Astro API [`Deploy` endpoint](https://www.astronomer.io/api/platform-api-reference/deploy/list-deploys) to create and manage code deploys to an Astro Deployment.

## Prerequisites

This guide assumes that you have:

- An [API token](deployment-api-tokens.md) with sufficient permissions to deploy code to Astro.
- At least one [Astro Deployment](create-deployment.md).
- An [Astro project](cli/develop-project.md) that's accessible from the machine that is making a request to the Astro API.
- [Docker](https://www.docker.com/), or an alternative container service like Podman.
- The following values:
  - Your Organization ID - See [List Organizations](https://docs.astronomer.io/docs/api/platform-api-reference/organization/list-organizations).
  - The Deployment ID - See [List Deployments](https://docs.astronomer.io/docs/api/platform-api-reference/deployment/list-deployments).
  - Your Astro API token - See [Create an API token](https://www.astronomer.io/docs/astro/automation-authentication#step-1-create-an-api-token).
  - The path where your Astro project exists.

## With DAG-only deploys enabled

If you have DAG-only deploys enabled, you can create scripts for complete project deploys, DAG-only deploys, or image-only deploys. The following sections include a step by step description of the workflow followed by a bash script that executes the workflow.

See [Deploy code to Astro](deploy-code.md) for more information about the different ways to update your DAGs and Airflow images.

### Complete project deploy

The following steps describe the different actions that the script performs to deploy a complete Astro project. Refer to [What happens during a project deploy](deploy-project-image.md#what-happens-during-a-project-deploy) to learn the details about how a project deploy builds and deploys a new Astro image along with deploying DAGs.

1. Make a `POST` request to the `Deploy` endpoint to create a new `deploy` object. In your call, specify `type` as `IMAGE_AND_DAG`. Store the values for `id`, `imageRepository`, `imageTag`, and `dagsUploadURL` that are returned in the response to use in the following steps.

        This action creates an object that represents the intent to deploy code to a Deployment. See the [Astro API documentation](https://www.astronomer.io/docs/api/platform-api-reference/deploy/create-deploy) for request usage and examples.

2. Authenticate to Astronomer's image registry using your Astro API token:

   ```bash

   docker login images.astronomer.cloud -u cli -p <your-api-token>

   ```

3. Build the image using the `imageRepository` and `imageTag` values that you retrieved in Step 1, as well as your Astro project path.

   ```bash

   docker build -t imageRepository:imageTag --platform=linux/amd64 <astro_project_path>

   ```

4. Push the image using the `imageRepository` and `imageTag` values that you retrieved in Step 1.

   ```bash

   docker push imageRepository:imageTag

   ```

5. Create a tar file of your Astro project DAGs folder:

   ```bash

   tar -cvf <path-to-create-tar-file>/dags.tar "dags"

   ```

   :::info

   Make sure to clean up the `dags.tar` file after uploading.

   :::

6. Upload the tar file by making a `PUT` call using the `dagsUploadURL` that you retrieved in Step 1. In this call, it is mandatory to pass the `x-ms-blob-type` as `BlockBlob`. Then, save the `x-ms-version-id` from the response header.

7. Using your deploy `id`, make a request to finalize the deploy. See [Astro API documentation](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/finalize-deploy) for more information about formatting the API request.

   - On `Success`, your DAGs have successfully uploaded and a `x-ms-version-id` of the DAGs tarball is generated in the response headers. Pass this `x-ms-version-id` in the requested body to finish your updates.
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

    # Step 1: Initialize deploy
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

    # Step 2: Log in to Docker
    docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN
    echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $ASTRO_PROJECT_PATH"

    # Step 3: Build image
    docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $ASTRO_PROJECT_PATH

    # Step 4: Push image
    echo -e "\nPushing Docker image $REPOSITORY:$TAG to $DEPLOYMENT_ID"
    docker push $REPOSITORY:$TAG

    # Step 5: Create tar file
    echo -e "\nCreating a dags tar file from $ASTRO_PROJECT_PATH/dags and stored in $ASTRO_PROJECT_PATH/dags.tar\n"
    cd $ASTRO_PROJECT_PATH
    tar -cvf "$ASTRO_PROJECT_PATH/dags.tar" "dags"

    # Step 6: Upload DAGs tar file
    echo -e "\nUploading tar file $ASTRO_PROJECT_PATH/dags.tar\n"
    VERSION_ID=$(curl -i --request PUT $DAGS_UPLOAD_URL \
    --header 'x-ms-blob-type: BlockBlob' \
    --header 'Content-Type: application/x-tar' \
    --upload-file "$ASTRO_PROJECT_PATH/dags.tar" | grep x-ms-version-id | awk -F': ' '{print $2}')

    VERSION_ID=$(echo $VERSION_ID | sed 's/\r//g') # Remove unexpected carriage return characters
    echo -e "\nTar file uploaded with version: $VERSION_ID\n"

    # Step 7: Finalizing Deploy
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

The following script allows you to update only your DAG files. Refer to [Deploy DAGs](deploy-dags.md) to learn the details about how Astro deploys DAGs.

1. Make a `POST` request to the `Deploy` endpoint to create a new `deploy` object. In your request, specify `type` as `DAG_ONLY`. Store the values for `id` and `dagsUploadURL` that are returned in the response to use in the following steps.

        This action creates an object that represents the intent to deploy code to a Deployment. See the [Astro API documentation](https://www.astronomer.io/docs/api/platform-api-reference/deploy/create-deploy) for request usage and examples.

2. Create a tar file of your Astro project DAGs folder:

   ```bash

   tar -cvf <path to create the tar file>/dags.tar "dags"

   ```

   :::note

   Make sure to clean up the `dags.tar` file after uploading.

   :::

3. Upload the tar file by making a `PUT` request using the `dagsUploadURL` that you retrieved in Step 2. In this request, it is mandatory to pass the `x-ms-blob-type` as `BlockBlob`. Then, save the `x-ms-version-id` from the response header.

4. Using your deploy `id`, make a request to finalize the deploy. See [Astro API documentation](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/finalize-deploy) for more information about formatting the API request.

   - On `Success`, your DAGs have successfully uploaded and a `x-ms-version-id` of the DAGs tarball is generated. Pass this `x-ms-version-id` in the requested body to finish your updates.
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

        # Step 1: Initialize deploy
        echo -e "Initiating Deploy Process for deployment $DEPLOYMENT_ID\n"
        CREATE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys" \
        --header "X-Astro-Client-Identifier: script" \
        --header "Content-Type: application/json" \
        --header "Authorization: Bearer $ASTRO_API_TOKEN" \
        --data '{
        "type": "DAG_ONLY"
        }' | jq '.')

        DEPLOY_ID=$(echo $CREATE_DEPLOY | jq -r '.id')
        DAGS_UPLOAD_URL=$(echo $CREATE_DEPLOY | jq -r '.dagsUploadUrl')

        # Step 2: Create a tar file of Astro project DAGs folder

        echo -e "\nCreating a dags tar file from $ASTRO_PROJECT_PATH/dags and stored in $ASTRO_PROJECT_PATH/dags.tar\n"
        cd $ASTRO_PROJECT_PATH
        tar -cvf "$ASTRO_PROJECT_PATH/dags.tar" "dags"

        # Step 3: Upload tar file
        echo -e "\nUploading tar file $ASTRO_PROJECT_PATH/dags.tar\n"
        VERSION_ID=$(curl -i --request PUT $DAGS_UPLOAD_URL \
        --header 'x-ms-blob-type: BlockBlob' \
        --header 'Content-Type: application/x-tar' \
        --upload-file "$ASTRO_PROJECT_PATH/dags.tar" | grep x-ms-version-id | awk -F': ' '{print $2}')

        VERSION_ID=$(echo $VERSION_ID | sed 's/\r//g') # Remove unexpected carriage return characters
        echo -e "\nTar file uploaded with version: $VERSION_ID\n"

        # Step 4: Finalizing Deploy
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

The following script allows you to update only your Astro project by building and deploying a new Docker image. Refer to [What happens during a project deploy](deploy-project-image.md#what-happens-during-a-project-deploy) to learn the details about how Astro deploys image updates.

1.  Make a `POST` request to the `Deploy` endpoint to create a new `deploy` object. In your request, specify `type` as `IMAGE`. Store the value for the `DeployID` that is returned. This action creates an object that represents the intent to deploy code to a Deployment.  See the [Astro API documentation](https://www.astronomer.io/docs/api/platform-api-reference/deploy/create-deploy) for request usage and examples.


2. Log in to Docker with your Astro API token.

   ```bash

   docker login images.astronomer.cloud -u cli -p <your_astro_api_token>

   ```

3. Build the image using the `imageRepository` and `imageTag` values that you retrieved in Step 2, as well as your Astro project path.

   ```bash

   docker build -t imageRepository:imageTag --platform=linux/amd64 <astro_project_path>

   ```

4. Push the image using the `imageRepository` and `imageTag` values that you retrieved earlier.

   ```bash

   docker push imageRepository:imageTag

   ```

5. Using your deploy `id`, make a request to finalize the deploy. See [Astro API documentation](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/finalize-deploy) for more information about formatting the API request.

   - On `Success`, your DAGs have successfully uploaded and a `x-ms-version-id` of the DAGs tarball is generated. Pass this `x-ms-version-id` in the requested body to finish your updates.
   - It might take a few minutes for the changes to update in your Deployment.

<details>
  <summary><strong>Image-only deploy script</strong></summary>

```bash
  # Prerequisites
  #!/bin/bash

  ORGANIZATION_ID=<set organization id>
  DEPLOYMENT_ID=<set deployment id>
  ASTRO_API_TOKEN=<set api token>
  ASTRO_PROJECT_PATH=<set path to your airflow project>

  # Step 1: Initialize Deploy
  echo -e "Initiating Deploy Process for deployment $DEPLOYMENT_ID\n"
  CREATE_DEPLOY=$(curl --location --request POST "https://api.astronomer.io/platform/v1beta1/organizations/$ORGANIZATION_ID/deployments/$DEPLOYMENT_ID/deploys" \
  --header "X-Astro-Client-Identifier: script" \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $ASTRO_API_TOKEN" \
  --data '{
  "type": "IMAGE_ONLY"
  }' | jq '.')

  DEPLOY_ID=$(echo $CREATE_DEPLOY | jq -r '.id')
  REPOSITORY=$(echo $CREATE_DEPLOY | jq -r '.imageRepository')
  TAG=$(echo $CREATE_DEPLOY | jq -r '.imageTag')

  # Step 2 Log in to Docker

  docker login images.astronomer.cloud -u cli -p $ASTRO_API_TOKEN

  # Step 3: Build Docker image
  echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $ASTRO_PROJECT_PATH"
  docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $ASTRO_PROJECT_PATH

  # Step 4: Push image
  echo -e "\nPushing Docker image $REPOSITORY:$TAG to $DEPLOYMENT_ID"
  docker push $REPOSITORY:$TAG

  # Step 5: Finalize Deploy
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

See [Deploy code to Astro](deploy-code.md) for more information about the different ways to update your DAGs and Airflow images.

### Complete project deploy

1. Create the `Deploy` API call using the `IMAGE_AND_DAG` type. This action creates an object that represents the intent to deploy code to a Deployment.

2. After you create the `deploy`, retrieve the `id`, `imageRepository`, and `imageTag` values using the [`GET` deploy API call](https://docs.astronomer.io/docs/api/platform-api-reference/deploy/get-deploy), which you need in the following steps.

3. Log in to Docker with your Astro API token.

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

## (Recommended) Dynamic deploys based on files changed

In addition to manually triggering project, DAG, and image deploys, you can create scripts that trigger specific code deploys depending on whether there have been changes to DAGs or files used to build the project image.

The following code example shows the recommended steps for you to use to create a bash script that triggers different code deploys depending on the files changed in your project. This example demonstrates how to combine all three types of deploys and the conditional logic for when to deploy each.

:::info

This recommended process requires that you enable [DAG-only deploys](deploy-dags.md).

:::

### Dynamic deploys workflow

1. Determine whether DAG files have been changed. If only DAGs have changed, then the script initiates a DAG-only deploy.

2. Make a `POST` request to the `Deploy` endpoint to create a new `deploy` object.

3. If only DAGs have changed, the script initiates a DAGs-only deploy. If you changed more files, the script builds and deploys the project image, and then completes a DAG-only deploy.

4. The script cleans up any tar files created during the build process.

<details>
<summary><strong>Trigger deploys when files change code example</strong></summary>

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
