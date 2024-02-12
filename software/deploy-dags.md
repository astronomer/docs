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

## Enable the feature on an Astronomer cluster

By default, DAG-only deploys are disabled for all Deployments on Astronomer Software. To enable the feature, add the following configuration to your `config.yaml` file:

```yaml
dagOnlyDeployment:
    enabled: true
    image: quay.io/astronomer/ap-dag-deploy:0.3.2
    securityContext:
      fsGroup: 50000
    resources: {
      requests:
        cpu: "100m"
        memory: "256Mi"
      limits:
        cpu: "500m"
        memory: "1024Mi" 
    }
```

:::info

When you enable DAG only deploys on a given Deployment, Astronomer Software spins up a component in the Deployment called the DAG deploy server. The default resources for the DAG deploy server are 1 CPU and 1.5 GB of memory, which allows you to push up to 15MB of compressed DAGs per deploy. To deploy more than 15MB of compressed DAGs at a time, increase the CPU and memory in the `resources` configuration by 1 CPU and 1.5MB for each additional 15MB of DAGs you want to upload. For more information, see [How DAG-only deploys work](#how-dag-only-deploys-work).

:::

:::warning

If you use a [third-party ingress controller](third-party-ingress-controllers.md), you can't upload more than 8MB of compressed DAGs regardless of your DAG server size. 

:::

Then, push the configuration change. See [Apply a config change](https://docs.astronomer.io/software/apply-platform-config).

## Configure DAG-only deploys on a deployment

:::danger

When you update a Deployment to support DAG-only deploys, all DAGs in your Deployment will be removed. To continue running your DAGs, you must redeploy them using `astro deploy --dags`. 

:::

By default, Deployments are configured only for complete project image deploys. To enable DAG-only deploys:

1. Open your Deployment in the Astronomer Software UI.
2. In the **Settings** tab under the **DAG Deployment** section, change the **Mechanism** to **DAG Only Deployment**. 
3. Click **Deploy changes**
4. Redeploy your DAGs using `astro deploy --dags`. See [Trigger a DAG-only deploy](#trigger-a-dag-only-deploy). This step is required due to all DAGs in your deployed image being erased when you enable the feature. 

## Trigger a DAG-only deploy

Run the following command to trigger a DAG-only deploy:

```sh
astro deploy --dags <deployment-id>
```

:::info

You can still run `astro deploy` to trigger a complete project deploy. When you do this, the Astro CLI builds all project files excluding DAGs into a Docker image and deploys the image. It then deploys your DAGs separately using the DAG deploy mechanism.

:::

## How DAG-only deploys work


If you deploy DAGs to a Deployment that is running a previous version of your code, then the following happens:

- Tasks that are `running` continue to run on existing workers and are not interrupted unless the task does not complete within 24 hours of the DAG deploy.

    These new workers execute downstream tasks of DAG runs that are in progress. For example, if you deploy to Astronomer when `Task A` of your DAG is running, `Task A` continues to run on an old Celery worker. If `Task B` and `Task C` are downstream of `Task A`, they are both scheduled on new Celery workers running your latest code.

    This means that DAG runs could fail due to downstream tasks running code from a different source than their upstream tasks. DAG runs that fail this way need to be fully restarted from the Airflow UI so that all tasks are executed based on the same source code.
