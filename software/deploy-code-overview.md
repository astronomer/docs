---
sidebar_label: 'Overview'
title: 'Configure code deploy mechanisms on Astronomer Software'
id: deploy-code-overview
description: Learn about the available options for deploying code to Astronomer Software
---

Deploying code is the process of pushing code to an Astronomer Software Deployment. A code deploy can include an entire Astro project as a Docker image, or just the code in your Astro project `dags` directory. Astronomer Software supports a few different methods for deploying code to a Deployment. You can:

- Deploy [project images](deploy-cli.md) or [DAGs only](deploy-dags.md) using the Astro CLI. Deploying a project image is the only way to deploy Airflow-level configurations and dependencies to a Deployment.
- Deploy DAGs using an [NFS volume](deploy-nfs.md).
- Deploy DAGs using [Git sync](deploy-git-sync.md).

Use this document to learn more about each available method and make a decision about which method is right for your use case. 

## Astro CLI deploys

By default, you can deploy code to an Airflow Deployment by building it into a Docker image and pushing that image to the Astronomer Registry via the CLI or API. This workflow is described in [Deploy code via the CLI](deploy-cli.md). 

This mechanism builds your DAGs into a Docker image alongside all other files in your Astro project directory, including your Python and OS-level packages, your Dockerfile, and your plugins.

The resulting image is then used to generate a set of Docker containers for each of Airflow's core components. Every time you run `astro deploy` in the Astro CLI, your DAGs are rebuilt into a new Docker image and all Docker containers are restarted.

You can also enable [DAG only deploys](deploy-dags.md) to deploy only your `dags` directory without building a Docker image. Note that you will still need access to Docker to authenticate to Astronomer Software before you can deploy DAGs.

## NFS volume-based DAG deploys

For advanced teams who deploy DAG changes more frequently, Astronomer also supports an [NFS volume-based](https://kubernetes.io/docs/concepts/storage/volumes/#nfs) DAG deploy mechanism.

Using this mechanism, you can deploy DAGs to an Airflow Deployment on Astronomer by adding the corresponding Python files to a shared file system on your network. Compared to image-based deploys, NFS volume-based deploys limit downtime and enable continuous deployment.

To deploy DAGs to a Deployment via an NFS volume, you must first enable the feature at the platform level. For more information, read [Deploy DAGs via NFS volume](deploy-nfs.md).

## Git-sync DAG deploys

For teams using a Git-based workflow for DAG development, Astronomer supports a [git-sync](https://github.com/kubernetes/git-sync) deploy mechanism.

To deploy DAGs via git-sync, you add DAGs to a repository that has been configured to sync with your Astronomer Deployment. Once the Deployment detects a change in the repository, your DAG code will automatically sync to your Deployment with no downtime. For more information on configuring this feature, read [Deploy DAGs via git sync](deploy-git-sync.md).