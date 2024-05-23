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

<details>
  <summary><strong>Complete deploy script</strong></summary>

    ```bash

    #!/bin/bash

    ORGANIZATION_ID=<set organization id>
    DEPLOYMENT_ID=<set deployment id>
    ASTRO_API_TOKEN=<set api token>
    AIRFLOW_PROJECT_PATH=<set path to your airflow project>

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

    ```

</details>

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

<details>
  <summary><strong>DAG-only deploy script</strong></summary>

  ```bash
  #!/bin/bash

    ORGANIZATION_ID=<set organization id>
    DEPLOYMENT_ID=<set deployment id>
    ASTRO_API_TOKEN=<set api token>
    AIRFLOW_PROJECT_PATH=<set path to your airflow project>

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

  ```

</details>

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

<details>
  <summary><strong>Image-only deploy script</strong></summary>

  ```bash
    #!/bin/bash

    ORGANIZATION_ID=<set organization id>
    DEPLOYMENT_ID=<set deployment id>
    ASTRO_API_TOKEN=<set api token>
    AIRFLOW_PROJECT_PATH=<set path to your airflow project>

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
    echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $AIRFLOW_PROJECT_PATH"
    docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $AIRFLOW_PROJECT_PATH
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

<details>
  <summary><strong>Complete code deploy script</strong></summary>

  ```bash
    #!/bin/bash

    ORGANIZATION_ID=<set organization id>
    DEPLOYMENT_ID=<set deployment id>
    ASTRO_API_TOKEN=<set api token>
    AIRFLOW_PROJECT_PATH=<set path to your airflow project>

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
    echo -e "\nBuilding Docker image $REPOSITORY:$TAG for $DEPLOYMENT_ID from $AIRFLOW_PROJECT_PATH"
    docker build -t $REPOSITORY:$TAG --platform=linux/amd64 $AIRFLOW_PROJECT_PATH
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