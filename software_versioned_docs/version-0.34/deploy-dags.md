---
sidebar_label: 'Deploy DAGs using the CLI'
title: 'Deploy DAGs to Astronomer Software using the Astro CLI'
id: deploy-dags
description: Learn how to enable and trigger DAG-only deploys on Astronomer Software.
---

DAG-only deploys are the fastest way to deploy code to Astronomer Software. They are recommended if you only need to deploy changes made to the `dags` directory of your Astro project.

When this feature is configured for a Deployment, you must still do a full project deploy when you make a change to any file in your Astro project that isn't in the `dags` directory, or when you [upgrade Astro Runtime](manage-airflow-versions.md).

DAG-only deploys have the following benefits:

- DAG-only deploys are faster than project deploys.
- Deployments pick up DAG-only deploys without restarting. This results in a more efficient use of workers and no downtime for your Deployments.
- If you have a CI/CD process that includes both DAG and image-based deploys, you can use your repository's permissions to control which users can perform which kinds of deploys.
- DAG deploys transmit significantly less data in most cases, which makes them quicker than image deploys when upload speeds to the Deployment are slow.

:::danger

When you [update a Deployment](#configure-dag-only-deploys-on-a-deployment) to support DAG-only deploys, all DAGs in your Deployment will be removed. To continue running your DAGs, you must redeploy them using `astro deploy --dags`.

:::

## Prerequisites

- Astro CLI version 1.23 or later

## Enable the feature on an Astronomer cluster

By default, DAG-only deploys are disabled for all Deployments on Astronomer Software. To enable the feature, set both `astronomer.houston.config.deployments.configureDagDeployment` and `global.dagOnlyDeployment.enabled` to `true` in your `values.yaml` file:

```yaml
global:
  dagOnlyDeployment:
    enabled: true
astronomer:
  houston:
    config:
      deployments:
        configureDagDeployment: true
```

:::info

If you need to customize the resources available to the DAG deploy mechanism on your Astronomer Software cluster, update your configuration to include the following values:

```yaml
global:
  dagOnlyDeployment:
    enabled: true
    resources:
      requests:
        # Update values as required for your cluster
        cpu: "100m"
        memory: "256Mi"
      limits:
        # Update values as required for your cluster
        cpu: "500m"
        memory: "1024Mi"
    image: quay.io/astronomer/ap-dag-deploy:0.3.2
    securityContext:
      fsGroup: 50000
```

:::

:::info

When you enable DAG only deploys on a given Deployment, Astronomer Software spins up a component in the Deployment called the DAG deploy server. The default resources for the DAG deploy server are 1 CPU and 1.5 GB of memory, which allows you to push up to 15MB of compressed DAGs per deploy. To deploy more than 15MB of compressed DAGs at a time, increase the CPU and memory in the `resources` configuration by 1 CPU and 1.5MB for each additional 15MB of DAGs you want to upload. For more information, see [How DAG-only deploys work](#trigger-a-dag-only-deploy).

:::

:::warning

If you use a [third-party ingress controller](third-party-ingress-controllers.md), you can't upload more than 8MB of compressed DAGs regardless of your DAG server size.

:::

Then, push the configuration change. See [Apply a config change](https://docs.astronomer.io/software/apply-platform-config).

## Configure DAG-only deploys on a deployment

By default, Deployments are configured only for complete project image deploys. To enable DAG-only deploys:

1. Open your Deployment in the Astronomer Software UI.
2. In the **Settings** tab under the **DAG Deployment** section, change the **Mechanism** to **DAG Only Deployment**.
3. Click **Deploy changes**
4. Redeploy your DAGs using `astro deploy --dags`. See [Trigger a DAG-only deploy](#trigger-a-dag-only-deploy). This step is required because all DAGs in your deployed image will be deleted from your Deployment when you enable the feature.

## Trigger a DAG-only deploy

Run the following command to trigger a DAG-only deploy:

```sh
astro deploy --dags <deployment-id>
```

:::info

You can still run `astro deploy` to trigger a complete project deploy. When you do this, the Astro CLI builds all project files excluding DAGs into a Docker image and deploys the image. It then deploys your DAGs separately using the DAG deploy mechanism.

:::

:::info

If you deploy DAGs to a Deployment that is running a previous version of your code, then tasks that are `running` continue to run on existing workers and are not interrupted unless the task does not complete within 24 hours of the DAG deploy.

These new workers execute downstream tasks of DAG runs that are in progress. For example, if you deploy to Astronomer when `Task A` of your DAG is running, `Task A` continues to run on an old Celery worker. If `Task B` and `Task C` are downstream of `Task A`, they are both scheduled on new Celery workers running your latest code.

This means that DAG runs could fail due to downstream tasks running code from a different source than their upstream tasks. DAG runs that fail this way need to be fully restarted from the Airflow UI so that all tasks are executed based on the same source code.

:::

## Deploy DAG-only deploys programmatically

Astronomer Software Deployment includes a REST API endpoint that you can use to upload DAGs programmatically.

### Prerequisites

Create a service account that has access to your Deployment and copy its associated API key. See [Create a service account using the Software UI](ci-cd.md#create-a-service-account-using-the-software-ui). Alternatively, go to `https://app.BASEDOMAIN/token` and copy the generated token to authenticate with your own user credentials.

### Setup

Your automated workflow must include the following two steps:

1. Create a `.tgz` file that contains only the `dags` folder of your Astro project. This file should be accessible from the rest of your automated process. For example, you can do this using the following command:

    ```sh
    tar -czf dags.tgz dags
    ```

2. Run a `POST` request to the endpoint `https://deployments.basedomain/<deployment-release-name>/dags/upload` to upload your `.tgz` file to your Deployment. For example, making the request using curl would look similar to the following:

    ```sh
    curl --location 'https://deployments.basedomain/<deployment-release-name>/dags/upload' \
    --header 'Authorization: Bearer <your-service-account-token>' \
    --form 'dags.tar.gz=@<your-dags-tgz-location>'
    ```

