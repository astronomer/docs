---
title: "Install Astronomer Software in an Airgapped Environment"
sidebar_label: "Install in an Airgapped Environment"
description: "Infrastructure considerations and Helm configuration to install Astronomer in an airgapped environment"
id: install-airgapped
---

## Overview

By default, the Software installation process requires accessing public repositories to download various components:

- Docker images from `quay.io/astronomer` or `docker.io`
- Astronomer Helm charts from `helm.astronomer.io`
- Astronomer version information from `updates.astronomer.io`

If you cannot rely on public repositories and networks for your installation, you can install Astronomer in an airgapped environment. An airgapped environment is a locked-down environment with no access to or from the public internet.

This guide explains how to configure your system to install Astronomer without access to the public internet. The steps in this guide should be followed in addition to Steps 1 to 8 in the [AWS](install-aws-standard.md), [Azure](install-azure-standard.md), or [GCP](install-gcp-standard.md) installation guide.

> **Note:** If you have some means to allow traffic to the public internet, e.g. a proxy that allows a list of accepted destinations/sources, that will make the airgapped installation much easier. This page assumes an environment without any possibility of accessing the public internet.

## Prerequisites

To complete this setup, you need:

- A VPC.
- Private Kubernetes.
- A Postgres instance accessible from that environment.
- A VPN (or other means) set up to access, at a minimum, Kubernetes and DNS from inside your VPC.

## Step 1: Configure a Private Docker Registry

Astronomer's Docker images are hosted on a public registry which isn't accessible from an airgapped network. Therefore, these images must be hosted on a Docker registry accessible from within your own network. Every major cloud platform provides its own managed Docker registry service that can be used for this step:

- AWS: [ECR](https://aws.amazon.com/ecr/)
- Azure: [Azure Container Registry](https://azure.microsoft.com/en-us/services/container-registry/)
- GCP: [Container Registry](https://cloud.google.com/container-registry)

You can also set up your own registry using a dedicated registry service such as [JFrog Artifactory](https://jfrog.com/artifactory/). Regardless of which service you use, follow the product documentation to configure a private registry according to your organization's security requirements.

## Step 2: Fetch Images from Astronomer's Helm Template

The images and tags which are required for your Software installation depend on the version of Astronomer you're installing. Image tags are subject to change, even within existing versions, for example to resolve critical security issues, and therefore not listed here. To gather a list of exact images and tags required for your Astronomer Helm chart version, you can template the Helm chart and fetch the rendered image tags:

```bash
$ helm template astronomer/astronomer --version 0.27 | grep "image: " | sed 's/^ *//g' | sort | uniq

image: "quay.io/prometheus/node-exporter:v1.3.0"
image: quay.io/astronomer/ap-alertmanager:0.23.0
image: quay.io/astronomer/ap-astro-ui:0.27.5
image: quay.io/astronomer/ap-base:3.15.0
image: quay.io/astronomer/ap-cli-install:0.26.1
...
```

Once you have this list of images, add them to a private image registry hosted within your organization's network. In Step 3, you will specify this private registry in your Astronomer configuration.

> **Note:** If you have already enabled/disabled Astronomer platform components in your `config.yaml`, you can pass `-f/--values config.yaml` to `helm template` to print a list specific to your `config.yaml` configuration.

## Step 3: Add Images to Your config.yaml File

Regardless of whether you choose to mirror or manually pull/push images to your private registry, the returned images and/or tags must be made accessible within your network.

To make these images accessible to Astronomer, specify your organization's private registry in the `global` section of your `config.yaml` file:

```yaml
global:
  privateRegistry:
    enabled: true
    repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo
    # user: ~
    # password: ~
```

This configuration automatically pulls most Docker images required in the Astronomer Helm chart. You must configure the following additional images individually in a separate section of your `config.yaml` file:

```yaml
astronomer:
    houston:
        deployments:
          helm:
            airflow:
              defaultAirflowRepository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/ap-airflow
              images:
                airflow:
                  repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/ap-airflow
                statsd:
                  repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/ap-statsd-exporter
                redis:
                  repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/ap-redis
                pgbouncer:
                  repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/ap-pgbouncer
                pgbouncerExporter:
                  repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/ap-pgbouncer-exporter
```
​
## Step 4: Fetch Airflow Helm Charts

There are two Helm charts required for Astronomer:

- The [Astronomer Helm chart](https://github.com/astronomer/astronomer) for the Astronomer Platform
- The [Airflow Helm chart](https://github.com/astronomer/airflow-chart) for Airflow deployments in Astronomer Platform

The Astronomer Helm chart can be downloaded using `helm pull` and applied locally if desired.

Commander, which is Astronomer's provisioning component, uses the Airflow Helm chart to create Airflow deployments. You have two options to make the Helm chart available to Commander:

- Use the built-in Airflow Helm chart in the Commander Docker image.
- Host the Airflow Helm chart within your network. Not every cloud provider has a managed Helm registry, so you might want to check out [JFrog Artifactory](https://jfrog.com/artifactory) or [ChartMuseum](https://github.com/helm/chartmuseum).

To use the built-in Airflow Helm chart in the Commander Docker image, add the following configuration to your `config.yaml` file:

```yaml
astronomer:
  commander:
    airGapped:
      enabled: true
```

To configure a self-hosted Helm chart, add the following configuration to your `config.yaml` file:

```yaml
# Example URL - replace with your own repository destination
global:
  helmRepo: "http://artifactory.company.com:32775/artifactory/astro-helm-chart"
```

:::info

If you configure both options in your `config.yaml` file, then `astronomer.commander.airGapped.enabled` takes precedence over `global.helmRepo`.

:::

## Step 5: Fetch Airflow Updates

By default, Astronomer checks for Airflow updates once a day at midnight by querying `https://updates.astronomer.io/astronomer-runtime`, which returns a JSON file with version details. However, this URL is not accessible in an airgapped environment. There are several options for making these updates accessible in an airgapped environment:

- You can download the JSON and host it in a location that's accessible within your airgapped environment, for example:
    - AWS S3
    - Git
    - Nginx (example below)
- You can disable the update checks (not advised)

This setup assumes that the updates JSON will be manually downloaded and added to your environment. For guidance on how to automate this process, reach out to your Astronomer contact.

### Exposing Airflow updates via an Nginx endpoint

The following topic provides an example implementation of hosting the Airflow updates JSON in your airgapped environment and accessing it via an Nginx endpoint. Depending on your organization's platform and use cases, your own installation might vary from this setup.

To complete this setup:

1. Host an updates JSON in a Kubernetes configmap by running the following commands:

    ```bash
    $ curl -L https://updates.astronomer.io/astronomer-runtime --output astronomer-certified.json
    $ kubectl create configmap astronomer-certified --from-file=astronomer-certified.json=./astronomer-certified.json -n astronomer
    ```

2. Add an Nginx deployment and service to a new file named `nginx-astronomer-certified.yaml`:

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: astronomer-certified
      namespace: astronomer
    spec:
      strategy:
        type: Recreate
      selector:
        matchLabels:
          app: astronomer-certified
      template:
        metadata:
          labels:
            app: astronomer-certified
        spec:
          containers:
          - name: astronomer-certified
            image: 012345678910.dkr.ecr.us-east-1.amazonaws.com/nginx:stable # Replace with own image
            resources:
              requests:
                memory: "32Mi"
                cpu: "100m"
              limits:
                memory: "128Mi"
                cpu: "500m"
            ports:
            - containerPort: 80
            volumeMounts:
            - name: astronomer-certified
              mountPath: /usr/share/nginx/html
          volumes:
          - name: astronomer-certified
            configMap:
              name: astronomer-certified
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: astronomer-certified
      namespace: astronomer
    spec:
      type: ClusterIP
      selector:
        app: astronomer-certified
      ports:
      - port: 80
        targetPort: 80
    ```

    Note the Docker image in the deployment and ensure that this is also accessible from within your environment.

3. Save this file and apply it to your cluster by running the following command:

    ```sh
    kubectl apply -f nginx-astronomer-certified.yaml
    ```

    The updates JSON will be accessible by the service name from pods in the Kubernetes cluster via `http://astronomer-certified.astronomer.svc.cluster.local/astronomer-certified.json`.

To validate if the updates JSON is accessible you have several options:

- If an image with `curl` is available in your network, you can run:

    ```bash
    $ kubectl run --rm -it [container name] --image=[image] --restart=Never -- /bin/sh
    $ curl http://astronomer-certified.astronomer.svc.cluster.local/astronomer-certified.json
    ```

- If you have `curl` installed on your client machine:

    ```bash
    $ kubectl proxy
    # In a separate terminal window:
    $ curl http://localhost:8001/api/v1/namespaces/astronomer/services/astronomer-certified/astronomer-certified.json
    ```

- Complete the entire Software installation, then use one of the `astro-ui` pods which include `bash` and `curl`:

    ```bash
    $ kubectl exec -it astronomer-astro-ui-7cfbbb97fd-fv8kl -n=astronomer -- /bin/bash
    $ curl http://astronomer-certified.astronomer.svc.cluster.local/astronomer-certified.json
    ```

No matter what option you choose, the commands that you run should return the updates JSON if the service was configured correctly.

### Configuring a custom updates JSON URL

After you have made the updates JSON accessible within your premises, you must configure the Helm chart to fetch updates from the custom URL:  

```yaml
astronomer:
  houston:
    updateCheck: # There is a 2nd check for Astronomer platform updates but this is deprecated and not actively used. Therefore disable
      enabled: false
    updateAirflowCheck: # Configure URL for Airflow updates check
      url: http://astronomer-certified.astronomer.svc.cluster.local
```

## Step 6: Install Astronomer via Helm

Before completing this step, double-check that the following statements are true:

- You made Astronomer's Docker images, Airflow Helm chart, and updates JSON accessible inside your network.
- You completed Steps 1 through 8 in the [AWS](install-aws-standard.md), [Azure](install-azure-standard.md), or [GCP](install-gcp-standard.md) install guide.

After this check, you can install the Astronomer Helm chart by running the following commands:

```bash
curl -L https://github.com/astronomer/astronomer/archive/v0.27.1.tar.gz -o astronomer-0.27.1.tgz
# Alternatively, use helm pull
helm pull astronomer/astronomer --version 0.27.1

# ... If necessary, copy to a place where you can access Kubernetes ...

helm install astronomer -f config.yaml -n astronomer astronomer-0.27.1.tgz
```

After these commands are finished running, continue your installation with Step 10 (Verify pods are up) in the [AWS](install-aws-standard.md#step-10-verify-pods-are-up), [Azure](install-azure-standard.md#step-10-verify-all-pods-are-up), or [GCP](install-gcp-standard.md#step-10-verify-that-all-pods-are-up) installation guide.
