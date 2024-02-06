---
sidebar_label: 'Deploy DAGs using the CLI'
title: 'Deploy DAGs to Astronomer Software using the Astro CLI'
id: deploy-dags
description: Learn how to enable and trigger DAG-only deploys on Astronomer Software.
---

DAG-only deploys are the fastest way to deploy code to Astronomer Software. They are recommended if you only need to deploy changes made to the `dags` directory of your Astro project.

When this feature is enabled, you must still do a full project deploy when you make a change to any file in your Astro project that isn't in the `dags` directory, or when you [upgrade Astro Runtime](manage-airflow-versions.md).

DAG-only deploys have the following benefits:

- DAG-only deploys are faster than project deploys.
- Deployments pick up DAG-only deploys without restarting. This results in a more efficient use of workers and no downtime for your Deployments.
- If you have a CI/CD process that includes both DAG and image-based deploys, you can use your repository's permissions to control which users can perform which kinds of deploys.
- DAG deploys transmit significantly less data in most cases, which makes them quicker than image deploys when upload speeds to the Deployment are slow.

## Enable the feature

By default, Deployments are configured only for complete project image deploys. To enable DAG-only deploys:

1. Open your Deployment in the Astronomer Software UI.
2. In the **Settings** tab under the **DAG Deployment** section, change the **Mechanism** to **DAG Only Deployment**. 

## Trigger a DAG-only deploy

Run the following command to trigger a DAG-only deploy:

```sh
astro deploy --dags
```

You can still run `astro deploy` to trigger a complete project deploy. When you do this, the Astro CLI builds all project files including your DAGs into a Docker image as described in [Deploy a project image](deploy-cli.md).

## How DAG-only deploys work

Each Deployment includes a Pod that processes DAG only deploys called the `dag-server`, and each Airflow component has a sidecar container to download new DAGs when they are available. When a user triggers a DAG-only deploy to a Deployment:

- The Astro CLI bundles the DAG code as a .tar.gz file and uploads it to the server.
- The server sends a signal to the Deployment DAG downloader sidecar that there are new DAGs to download.
- The DAG downloader in each Airflow component downloads the new DAGs from the DAG server.
- Airflow scans the dags directory on its configured interval and processes the changed files.

If you deploy DAGs to a Deployment that is running a previous version of your code, then the following happens:

- Tasks that are `running` continue to run on existing workers and are not interrupted unless the task does not complete within 24 hours of the DAG deploy.

    These new workers execute downstream tasks of DAG runs that are in progress. For example, if you deploy to Astronomer when `Task A` of your DAG is running, `Task A` continues to run on an old Celery worker. If `Task B` and `Task C` are downstream of `Task A`, they are both scheduled on new Celery workers running your latest code.

    This means that DAG runs could fail due to downstream tasks running code from a different source than their upstream tasks. DAG runs that fail this way need to be fully restarted from the Airflow UI so that all tasks are executed based on the same source code.

When you run `astro deploy` to deploy a complete project image, the Astro CLI builds all project files including your DAGs into a Docker image as described in [Deploy a project image](deploy-cli.md).