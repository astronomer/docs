---
sidebar_label: 'CI/CD'
title: 'Automate Code Deploys with CI/CD'
id: ci-cd
description: Create a CI/CD pipeline that triggers a deploy to Astro based on changes to your Airflow DAGs.
---

## Overview

There are many benefits to deploying DAGs and other changes to Airflow via a CI/CD workflow. Specifically, you can:

- Deploy new and updated DAGs in a way that streamlines the development process amongst team members.
- Decrease the maintenance cost of integrating changes, allowing your team to quickly respond in case of an error or failure.
- Enforce continuous, automating testing, which increases code quality and protects your DAGs in production.

This guide provides setup steps for configuring a CI/CD pipeline to deploy DAGs on Astro.

## Prerequisites

To set up CI/CD for a given Deployment, you need:

- A [Deployment API key ID and secret](api-keys.md)
- An Organization ID. To find this, go to [**Organization Settings** in the Cloud UI](https://cloud.astronomer.io/settings) and copy the Organization ID displayed there.
- A Deployment ID. To find this, open your Deployment in the Cloud UI and copy the unique string at the end of the URL (e.g. `cktogz2eg847343yzo9pru1b0d` is the ID in `https://cloud.astronomer.io/<workspaceId>/deployments/cktogz2eg847343yzo9pru1b0d`)
- A CI/CD management tool, such as [GitHub Actions](https://docs.github.com/en/actions)
- An Astro project directory that was [initialized via the Astro CLI](deploy-code.md) and is hosted in a place that your CI/CD tool can access
- [Docker](https://docs.docker.com/get-docker/)
- curl

## Workflow Overview

This section provides a high-level overview of how a CI/CD script can use Deployment API keys to push DAGs to Astro. Regardless of what CI/CD tool you use, your pipeline needs to complete these key steps. You can also use this information to manually test the API calls that complete these steps in your pipeline.

At a high level, your CI/CD pipeline will:

1. Access your Deployment using the `Key ID` and `Key secret` of an existing Deployment API key.
2. Build your Astro project into a Docker image.
3. Deploy the image to your Deployment.

This workflow is equivalent to the following bash script:

```bash title="astronomer-ci.sh"
ASTRONOMER_KEY_ID=$1
ASTRONOMER_KEY_SECRET=$2
ORGANIZATION_ID=$3
DEPLOYMENT_ID=$4

# install jq
# brew install jq

# Create time stamp

TAG=deploy-`date "+%Y-%m-%d-%HT%M-%S"`

# Step 1. Authenticate to Astro's Docker registry with your Deployment API key ID and secret. This is equivalent to running `$ astrocloud auth login` via the Astro CLI.

docker login images.astronomer.cloud -u $ASTRONOMER_KEY_ID -p $ASTRONOMER_KEY_SECRET

# Step 2. Build your Astro project into a tagged Docker image.

docker build . -t images.astronomer.cloud/$ORGANIZATION_ID/$DEPLOYMENT_ID:$TAG

# Step 3. Push that Docker image to Astro's Docker registry.

docker push images.astronomer.cloud/$ORGANIZATION_ID/$DEPLOYMENT_ID:$TAG

# Step 4. With your Deployment API key ID and secret, fetch a Deployment API access token. For security reasons, this access token is what ultimately makes your API key valid.

echo "get token"
TOKEN=$( curl --location --request POST "https://auth.astronomer.io/oauth/token" \
        --header "content-type: application/json" \
        --data-raw "{
            \"client_id\": \"$ASTRONOMER_KEY_ID\",
            \"client_secret\": \"$ASTRONOMER_KEY_SECRET\",
            \"audience\": \"astronomer-ee\",
            \"grant_type\": \"client_credentials\"}" | jq -r '.access_token' )

# Step 5. Make a request to the Astro API that passes metadata from your new Docker image and creates a record for it.

echo "get image id"
IMAGE=$( curl --location --request POST "https://api.astronomer.io/hub/v1" \
        --header "Authorization: Bearer $TOKEN" \
        --header "Content-Type: application/json" \
        --data-raw "{
            \"query\" : \"mutation imageCreate(\n    \$input: ImageCreateInput!\n) {\n    imageCreate (\n    input: \$input\n) {\n    id\n    tag\n    repository\n    digest\n    env\n    labels\n    deploymentId\n  }\n}\",
            \"variables\" : {
                \"input\" : {
                    \"deploymentId\" : \"$DEPLOYMENT_ID\",
                    \"tag\" : \"$TAG\"
                    }
                }
            }" | jq -r '.data.imageCreate.id')

# Step 6. Pass the repository URL for the Docker image to your Astro Deployment. This completes the deploy process and triggers your Scheduler, Webserver, and Workers to restart.

echo "deploy image"
curl --location --request POST "https://api.astronomer.io/hub/v1" \
        --header "Authorization: Bearer $TOKEN" \
        --header "Content-Type: application/json" \
        --data-raw "{
            \"query\" : \"mutation imageDeploy(\n    \$input: ImageDeployInput!\n  ) {\n    imageDeploy(\n      input: \$input\n    ) {\n      id\n      deploymentId\n      digest\n      env\n      labels\n      name\n      tag\n      repository\n    }\n}\",
            \"variables\" : {
                \"input\" : {
                    \"id\" : \"$IMAGE\",
                    \"tag\" : \"$TAG\",
                    \"repository\" : \"images.astronomer.cloud/$ORGANIZATION_ID/$DEPLOYMENT_ID\"
                    }
                }
            }"
```

To run this script without a CI/CD tool,

1. Make `ci-cd.sh` executable by running `chmod +x ci-cd.sh`.
2. Run the following command:

    ```sh
    bash ci-cd.sh <your-key-id> <your-key-secret> <your-organization-id> <your-deployment-id>
    ```

## CI/CD Templates

The following section provides basic templates for configuring individual CI pipelines using popular CI/CD tools. Each template can be implemented as-is to produce a simple CI/CD pipeline, but we recommend reconfiguring the templates to work with your own directory structures, workflows, and best practices. More templates are coming soon.

### GitHub Actions

To automate code deploys to a Deployment using [GitHub Actions](https://github.com/features/actions), complete the following setup in a Git-based repository that hosts an Astro project:

1. Set the following as [GitHub secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository):

   - `ASTRONOMER_KEY_ID` = `<your-key-id>`
   - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. Add the following to a new file in `.github/workflows`, making sure to replace `<organization-id>` and `<deployment-id>` with the values for your Deployment:

    ```yaml
    name: Astronomer CI - Deploy Code

    on:
      push:
        branches:
          - main
    jobs:
      build:
        runs-on: ubuntu-latest
        env:
          ORGANIZATION_ID: <organization-id> # Found in `Organization Settings` in the Cloud UI
          DEPLOYMENT_ID: <deployment-id> # Found at the end of your Deployment's URL from the Cloud UI
        steps:
        - name: Check out the repo
          uses: actions/checkout@v2
        - name: Get current date
          id: date
          run: echo "::set-output name=date::$(date +'%Y-%m-%d-%HT%M-%S')"
        - name: Log in to registry
          uses: docker/login-action@v1
          with:
            registry: images.astronomer.cloud
            username: ${{ secrets.ASTRONOMER_KEY_ID }}
            password: ${{ secrets.ASTRONOMER_KEY_SECRET }}
        - name: Build and push images
          uses: docker/build-push-action@v2
          if: github.ref == 'refs/heads/master'
          with:
            push: true
            tags: images.astronomer.cloud/${{ env.ORGANIZATION_ID }}/${{ env.DEPLOYMENT_ID }}:deploy-${{ steps.date.outputs.date }}
        - name: Get access token
          id: token
          run: |
            token=$( curl --location --request POST 'https://auth.astronomer.io/oauth/token' \
            --header 'content-type: application/json' \
            --data-raw '{ "client_id": "${{ secrets.ASTRONOMER_KEY_ID }}","client_secret": "${{ secrets.ASTRONOMER_KEY_SECRET }}","audience": "astronomer-ee","grant_type":"client_credentials"}' | jq -r '.access_token' )
            echo "::set-output name=auth_token::$token"

        - name: Create image
          id: image
          run: |
            image=$( curl --location --request POST 'https://api.astronomer.io/hub/v1' \
            --header 'Authorization: Bearer ${{ steps.token.outputs.auth_token }}' \
            --header 'Content-Type: application/json' \
            --data-raw '{"query":"mutation imageCreate(\n    $input: ImageCreateInput!\n) {\n    imageCreate (\n    input: $input\n) {\n    id\n    tag\n    repository\n    digest\n    env\n    labels\n    deploymentId\n  }\n}","variables":{"input":{"deploymentId":"${{ env.DEPLOYMENT_ID }}","tag":"deploy-${{ steps.date.outputs.date }}"}}}' | jq -r '.data.imageCreate.id')
            echo "::set-output name=image_id::$image"

        - name: Deploy image
          run: |
            curl --location --request POST 'https://api.astronomer.io/hub/v1' \
            --header 'Authorization: Bearer ${{ steps.token.outputs.auth_token }}' \
            --header 'Content-Type: application/json' \
            --data-raw '{"query":"mutation imageDeploy(\n    $input: ImageDeployInput!\n  ) {\n    imageDeploy(\n      input: $input\n    ) {\n      id\n      deploymentId\n      digest\n      env\n      labels\n      name\n      tag\n      repository\n    }\n}","variables":{"input":{"id":"${{ steps.image.outputs.image_id }}","tag":"deploy-${{ steps.date.outputs.date }}","repository":"images.astronomer.cloud/${{ env.ORGANIZATION_ID }}/${{ env.DEPLOYMENT_ID }}"}}}'
    ```


### Jenkins

To automate code deploys to a single Deployment using [Jenkins](https://www.jenkins.io/), complete the following setup in a Git-based repository hosting an Astronomer project:

1. At the root of your Git repository, add a [Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) that includes the following script:

    ```jenkins
    pipeline {
     agent any
       stages {
         stage('Deploy to Astronomer') {
           when {
            expression {
              return env.GIT_BRANCH == "origin/main"
            }
           }
           steps {
             script {
               sh "chmod +x -R ${env.WORKSPACE}"
               sh('./build.sh')
             }
           }
         }
       }
     post {
       always {
         cleanWs()
       }
     }
    }
    ```

    This Jenkinsfile triggers a code push to Astro every time a commit or pull request is merged to the `main` branch of your repository.

2. In your Git repository, configure the following environment variables:

    - `ASTRONOMER_KEY_ID`: Your Deployment API key ID
    - `ASTRONOMER_KEY_SECRET`: Your Deployment API key secret
    - `ORGANIZATION_ID`: Your Organization ID
    - `DEPLOYMENT_ID`: Your Deployment ID

    Be sure to set the values for your API credentials as secret.

3. At the root of your Git repository, create a file called `build.sh` and add the following to it:

    ```sh
    # Create time stamp
    TAG=deploy-`date "+%Y-%m-%d-%HT%M-%S"`

    # Step 1. Authenticate to Astronomer's Docker registry with your Deployment API key ID and secret. This is equivalent to running `$ astrocloud auth login` via the Astro CLI.
    docker login images.astronomer.cloud -u $ASTRONOMER_KEY_ID -p $ASTRONOMER_KEY_SECRET

    # Step 2. Build your Astronomer project into a tagged Docker image.
    docker build . -t images.astronomer.cloud/$ORGANIZATION_ID/$DEPLOYMENT_ID:$TAG

    # Step 3. Push that Docker image to Astronomer's Docker registry.
    docker push images.astronomer.cloud/$ORGANIZATION_ID/$DEPLOYMENT_ID:$TAG

    # Step 4. Fetch an API access token with your Deployment API key ID and secret.
    echo "get token"
    TOKEN=$( curl --location --request POST "https://auth.astronomer.io/oauth/token" \
            --header "content-type: application/json" \
            --data-raw "{
                \"client_id\": \"$ASTRONOMER_KEY_ID\",
                \"client_secret\": \"$ASTRONOMER_KEY_SECRET\",
                \"audience\": \"astronomer-ee\",
                \"grant_type\": \"client_credentials\"}" | jq -r '.access_token' )
    # Step 5. Make a request to the Astronomer API that passes metadata from your new Docker image and creates a record for it.
    echo "get image id"
    IMAGE=$( curl --location --request POST "https://api.astronomer.io/hub/v1" \
            --header "Authorization: Bearer $TOKEN" \
            --header "Content-Type: application/json" \
            --data-raw "{
                \"query\" : \"mutation imageCreate(\n    \$input: ImageCreateInput!\n) {\n    imageCreate (\n    input: \$input\n) {\n    id\n    tag\n    repository\n    digest\n    env\n    labels\n    deploymentId\n  }\n}\",
                \"variables\" : {
                    \"input\" : {
                        \"deploymentId\" : \"$DEPLOYMENT_ID\",
                        \"tag\" : \"$TAG\"
                        }
                    }
                }" | jq -r '.data.imageCreate.id')

    # Step 6. Pass the repository URL for the Docker image to your Astronomer Deployment. This completes the deploy process and triggers your Scheduler and Workers to restart.
    echo "deploy image"
    curl --location --request POST "https://api.astronomer.io/hub/v1" \
            --header "Authorization: Bearer $TOKEN" \
            --header "Content-Type: application/json" \
            --data-raw "{
                \"query\" : \"mutation imageDeploy(\n    \$input: ImageDeployInput!\n  ) {\n    imageDeploy(\n      input: \$input\n    ) {\n      id\n      deploymentId\n      digest\n      env\n      labels\n      name\n      tag\n      repository\n    }\n}\",
                \"variables\" : {
                    \"input\" : {
                        \"id\" : \"$IMAGE\",
                        \"tag\" : \"$TAG\",
                        \"repository\" : \"images.astronomer.cloud/$ORGANIZATION_ID/$DEPLOYMENT_ID\"
                        }
                    }
                }"
    ```
