---
sidebar_label: Drone
title: Drone CI/CD templates
id: drone
description: Use pre-built templates for Drone to automate your Apache Airflow code deploys to Astro  
---

Templates are customizable, pre-built code samples that allow you to configure automated workflows using popular CI/CD tools. You can use this template for [Drone CI](https://www.drone.io/) to automate code deploys to Astro with Image-only deploy templates. 

[Image-only deploy templates](template-overview.md#template-types) create an automated workflow that builds a Docker image and then pushes it to Astro whenever you update any file in your Astro project. You can choose whether to deploy to a single Deployment, called _Single branch implementation_, or multiple Deployments, called _Multiple branch implementation_. 

See [Template overview](template-overview.md) to decide which template is right for you and to learn more about CI/CD use cases, see [Set up CI/CD](set-up-ci-cd.md).

## Prerequisites

This pipeline configuration requires:

- A deploy strategy for your CI/CD pipeline. See [Set up CI/CD](set-up-ci-cd.md).
- A [Deployment API key ID and secret](api-keys.md).
- A functional Drone [server](https://docs.drone.io/server/overview/).
- A [Docker runner](https://docs.drone.io/runner/docker/overview/).
- A user with admin privileges to your Drone server.
- An [Astro project](create-project.md) hosted in a Git repository that your CI/CD tool can access.

## Single branch implementation

1. Set the following environment variables as repository-level [secrets](https://docs.drone.io/secret/repository/) on Drone:

    - `ASTRONOMER_KEY_ID` = `<your-key-id>`
    - `ASTRONOMER_KEY_SECRET` = `<your-key-secret>`

2. In your Drone server, open your Astro project repository and go to **Settings** > **General**. Under **Project Settings**, turn on the **Trusted** setting.

3. In the top level of your Git repository, create a file called `.drone.yml` that includes the following configuration:

    ```yaml
    ---
    kind: pipeline
    type: docker
    name: deploy

    steps:
      - name: install
        image: debian
        commands:
        - apt-get update
        - apt-get -y install curl
        - curl -sSL install.astronomer.io | sudo bash -s
      - name: wait
        image: docker:dind
        volumes:
        - name: dockersock
          path: /var/run
        commands:
        - sleep 5
      - name: deploy
        image: docker:dind
        volumes:
        - name: dockersock
          path: /var/run
        commands:
        - astro deploy -f
        depends on:
        - wait

        environment:
          ASTRONOMER_KEY_ID:
            from_secret: ASTRONOMER_KEY_ID
          ASTRONOMER_KEY_SECRET:
            from_secret: ASTRONOMER_KEY_SECRET

    services:
    - name: docker
      image: docker:dind
      privileged: true
      volumes:
      - name: dockersock
        path: /var/run

    volumes:
    - name: dockersock
      temp: {}

    trigger:
      branch:
      - main
      event:
      - push
    ```

