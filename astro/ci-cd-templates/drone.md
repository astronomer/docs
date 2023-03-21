---
sidebar_label: Drone
title: Drone CI/CD templates
id: drone
description: Use pre-built templates to get started with automating code deploys from drone to Astro 
---

Use the following template to automate [single branch deploys](template-overview.md#template-types) to Astro using [Drone CI](https://www.drone.io/).

## Prerequisites

This pipeline configuration requires:

- A functional Drone [server](https://docs.drone.io/server/overview/) and [Docker runner](https://docs.drone.io/runner/docker/overview/).
- A user with admin privileges to your Drone server.

## Setup

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

