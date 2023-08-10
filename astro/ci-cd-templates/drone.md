---
sidebar_label: Drone
title: Astro CI/CD templates for Drone
id: drone
description: Use pre-built Astronomer CI/CD templates to automate deploying Apache Airflow DAGs to Astro using Drone CI.
---

Use the following CI/CD templates to automate deploying Apache Airflow DAGs from a Git repository to Astro with [Drone CI](https://www.drone.io/).

The templates for DroneCI use the [image deploy](template-overview.md#template-types) process with a _single branch implementation_, which requires only one Astro Deployment.

If you use the [DAG-only deploy feature](astro/deploy-code#deploy-dags-only) on Astro or you're interested in a multiple-branch implementation, see [Template overview](template-overview.md) to configure your own. To learn more about CI/CD on Astro, see [Choose a CI/CD strategy](set-up-ci-cd.md).

## Prerequisites

- An [Astro project](develop-project.md#create-an-astro-project) hosted in a Git repository that Drone can access.
- An [Astro Deployment](create-deployment.md).
- Either a [Workspace API token](workspace-api-tokens.md) or an [Organization API token](organization-api-tokens.md).
- A functional Drone [server](https://docs.drone.io/server/overview/).
- A user with admin privileges to your Drone server.
- A [Docker runner](https://docs.drone.io/runner/docker/overview/).

## Single branch implementation

1. Set the following environment variable as a repository-level [secret](https://docs.drone.io/secret/repository/) on Drone:

    - `ASTRO_API_TOKEN`: The value for your Workspace or Organization API token.

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
        - astro deploy <your-deployment-id> -f
        depends on:
        - wait

        environment:
          ASTRO_API_TOKEN:
            from_secret: ASTRO_API_TOKEN

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

