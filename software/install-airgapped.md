---
title: "Install Astronomer Software in an airgapped environment"
sidebar_label: "Install in an airgapped environment"
description: "Infrastructure considerations and Helm configuration to install Astronomer in an airgapped environment"
id: install-airgapped
---

By default, the Software installation process requires accessing public repositories to download the following components:

- Docker images from `quay.io/astronomer` or `docker.io`
- Astronomer Helm charts from `helm.astronomer.io`
- Astronomer version information from `updates.astronomer.io`

If you cannot use public repositories and networks for your installation, you can install Astronomer in an airgapped environment. An airgapped environment is a locked-down environment with no access to or from the public internet.

This guide explains how to configure your system to install Astronomer without access to the public internet by moving Astronomer images to an accessible registry in your airgapped environment. After completing this setup, follow Steps 1 to 8 in the [AWS](install-aws-standard.md), [Azure](install-azure-standard.md), or [GCP](install-gcp-standard.md) installation guide to finish your installation.


## Prerequisites

To complete this setup, you need:

- A VPC.
- Private Kubernetes.
- A PostgreSQL instance accessible from that environment.
- PostgreSQL superuser permissions.
- A VPN (or other means) set up to access, at a minimum, Kubernetes and DNS from inside your VPC.
- A Helm configuration file for Astronomer named `values.yaml`. You can find sample `values.yaml` files in the [AWS](install-aws-standard.md#step-8-configure-your-helm-chart), [Azure](install-azure-standard.md#step-8-configure-your-helm-chart), [GCP](install-gcp-standard.md#step-8-configure-your-helm-chart) standard installation guides.

## Step 1: Configure a private Docker registry

Astronomer's Docker images are hosted on a public registry which isn't accessible from an airgapped network. Therefore, these images must be hosted on a Docker registry accessible from within your own network. Every major cloud platform provides its own managed Docker registry service that can be used for this step:

- AWS: [ECR](https://aws.amazon.com/ecr/)
- Azure: [Azure Container Registry](https://azure.microsoft.com/en-us/services/container-registry/)
- GCP: [Container Registry](https://cloud.google.com/container-registry)

You can also set up your own registry using a dedicated registry service such as [JFrog Artifactory](https://jfrog.com/artifactory/). Regardless of which service you use, follow the product documentation to configure a private registry according to your organization's security requirements.

After you create your registry:

1. Log in to the registry and follow the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#log-in-to-docker-hub) to produce a `/.docker/config.json` file.
2. Run the following command to create an image pull secret:

    ```sh
    kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=<path/to/.docker/config.json> \
    --type=kubernetes.io/dockerconfigjson
    ```
3. Copy the generated secret for use in Step 3.

## Step 2: Fetch images from Astronomer's Helm template

The images and tags which are required for your Software installation depend on the version of Astronomer you're installing. To gather a list of exact images and tags required for your Astronomer version:

1. Run the following command to template the Astronomer Helm chart and fetch all of its rendered image tags. Make sure to substitute `<your-basedomain>` and `<your-astronomer-version>` with your information.

    ```bash
    helm template --version <your-astronomer-version> astronomer/astronomer --set global.dagOnlyDeployment.enabled=True --set global.loggingSidecar.enabled=True --set global.postgresqlEnabled=True --set global.authSidecar.enabled=True --set global.baseDomain=<your-basedomain> | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq
    ```

    This command sets all possible Helm values that could impact which images are required for your installation. By fetching all images now, you save time by eliminating the risk of missing an image.
    
2. Run the following command to determine the Astronomer Apache Airflow® Helm chart version:
 
    ```shell
    helm template astronomer/astronomer --version <your-astronomer-version>|grep 'Static helm' -A4| grep "version: " | sed -e 's/"//g' -e 's/version:[ ]//' -e 's/^ */v/g'
    ```

3. Run the following command to template the Astronomer Airflow Helm chart and fetch its rendered image tags:

    ```shell
    helm template --version <your-astronomer-airflow-chart-version> astronomer/airflow --set airflow.postgresql.enabled=false --set airflow.pgbouncer.enabled=true --set airflow.statsd.enabled=true --set airflow.executor=CeleryExecutor | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq
    ```

    **Note:** The Astronomer Airflow Helm Chart version begins with the letter v and is versioned separately from Astronomer Software and Airflow.

These commands generate a list of images required for your version of Astronomer. Add these images to a private image registry hosted within your organization's network. In Step 3, you will specify this private registry in your Astronomer configuration.

> **Note:** If you have already enabled or disabled Astronomer platform components in your `values.yaml`, you can pass `-f/--values values.yaml` to `helm template` to print a list specific to your `values.yaml` configuration.

## Step 3: Add images to your values.yaml file

Regardless of whether you choose to mirror or manually pull/push images to your private registry, the returned images and/or tags must be made accessible within your network.

To make these images accessible to Astronomer, specify your organization's private registry in the `global` section of your `values.yaml` file:

```yaml
global:
  privateRegistry:
    enabled: true
    repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo
    # secretName: ~
```

This configuration automatically pulls most Docker images required in the Astronomer Helm chart. You must also configure the following images individually in a separate section of your `values.yaml` file:

```yaml
astronomer:
  houston:
    config:
      deployments:
        helm:
          runtimeImages:
            airflow:
              repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/astro-runtime
            flower:
              repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/astro-runtime
          airflow:
            defaultAirflowRepository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/ap-airflow
            defaultRuntimeRepository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/astro-runtime
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
              gitSync:
                repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer/ap-git-sync
```

## Step 4: Fetch Apache Airflow® Helm charts

There are two Helm charts required for Astronomer:

- The [Astronomer Helm chart](https://github.com/astronomer/astronomer) for the Astronomer Platform
- The [Astronomer Apache Airflow® Helm chart](https://github.com/astronomer/airflow-chart) for Airflow deployments in Astronomer Platform

The Astronomer Helm chart can be downloaded using `helm pull` and applied locally if desired.

Commander, which is Astronomer's provisioning component, uses the Astronomer Airflow Helm chart to create Airflow deployments. You have two options to make the Helm chart available to Commander:

- Use the built-in Astronomer Airflow Helm chart in the Commander Docker image.
- Host the Astronomer Airflow Helm chart within your network. Not every cloud provider has a managed Helm registry, so you might want to check out [JFrog Artifactory](https://jfrog.com/artifactory) or [ChartMuseum](https://github.com/helm/chartmuseum).

To use the built-in Astronomer Airflow Helm chart in the Commander Docker image, add the following configuration to your `values.yaml` file:

```yaml
astronomer:
  commander:
    airGapped:
      enabled: true
```

To configure a self-hosted Helm chart, add the following configuration to your `values.yaml` file:

```yaml
# Example URL - replace with your own repository destination
global:
  helmRepo: "http://artifactory.example.com:32775/artifactory/astro-helm-chart"
```

:::info

If you configure both options in your `values.yaml` file, then `astronomer.commander.airGapped.enabled` takes precedence over `global.helmRepo`.

:::

## Step 5: Fetch Apache Airflow® updates

By default, Astronomer checks for Airflow updates once a day at midnight by querying `https://updates.astronomer.io/astronomer-runtime`, which returns a JSON file with version details. However, this URL is not accessible in an airgapped environment. There are several options for making these updates accessible in an airgapped environment:

- You can download the JSON and host it in a location that's accessible within your airgapped environment, for example:
    - AWS S3
    - Git
    - Nginx (example below)
- You can disable the update checks (not advised)

This setup assumes that the updates JSON will be manually downloaded and added to your environment. For guidance on how to automate this process, reach out to your Astronomer contact.

### Exposing Apache Airflow® updates using an Nginx endpoint

The following topic provides an example implementation of hosting the Airflow updates JSON files in your airgapped environment and accessing them via an Nginx endpoint. Depending on your organization's platform and use cases, your own installation might vary from this setup.

To complete this setup:

1. Host an updates JSON in a Kubernetes configmap by running the following commands:

    ```bash
    $ curl -L https://updates.astronomer.io/astronomer-certified --output astronomer-certified.json
    $ curl -L https://updates.astronomer.io/astronomer-runtime --output astronomer-runtime.json
    $ kubectl create configmap astronomer-certified --from-file=astronomer-certified.json=./astronomer-certified.json -n astronomer
    $ kubectl create configmap astronomer-runtime --from-file=astronomer-runtime.json=./astronomer-runtime.json -n astronomer
    ```


2. Add an Nginx deployment and service configuration to a new file named `nginx-astronomer-certified.yaml`:

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: astronomer-releases
      namespace: astronomer
    spec:
      strategy:
        type: Recreate
      selector:
        matchLabels:
          app: astronomer-releases
      template:
        metadata:
          labels:
            app: astronomer-releases
        spec:
          containers:
          - name: astronomer-releases
            image: ap-nginx-es
            resources:
              requests:
                memory: "32Mi"
                cpu: "100m"
              limits:
                memory: "128Mi"
                cpu: "500m"
            ports:
            - containerPort: 8080
            volumeMounts:
            - name: astronomer-certified
              mountPath: /usr/share/nginx/html/astronomer-certified
              subPath: astronomer-certified.json
            - name: astronomer-runtime
              mountPath: /usr/share/nginx/html/astronomer-runtime
              subPath: astronomer-runtime.json
          volumes:
          - name: astronomer-certified
            configMap:
              name: astronomer-certified
          - name: astronomer-runtime
            configMap:
              name: astronomer-runtime
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: astronomer-releases
      namespace: astronomer
    spec:
      type: ClusterIP
      selector:
        app: astronomer-releases
      ports:
      - port: 80
        targetPort: 8080
    ---
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: astronomer-astronomer-releases-nginx-policy
    spec:
      ingress:
      - from:
        - namespaceSelector: {}
          podSelector: {}
        ports:
        - port: 8080
          protocol: TCP
      podSelector:
        matchLabels:
          app: astronomer-releases
      policyTypes:
      - Ingress
    ```

    Note the Docker image in the deployment and ensure that this is also accessible from within your environment.

3. Save this file and apply it to your cluster by running the following command:

    ```sh
    kubectl apply -f nginx-astronomer-releases.yaml
    ```

    The updates JSON will be accessible by the service name from pods in the Kubernetes cluster via `http://astronomer-releases.astronomer.svc.cluster.local/astronomer-certified.json`.

To validate if the updates JSON is accessible you have several options:

- If an image with `curl` is available in your network, you can run:

    ```bash
    $ kubectl run --rm -it [container name] --image=[image] --restart=Never -- /bin/sh
    $ curl http://astronomer-releases.astronomer.svc.cluster.local/astronomer-certified
    $ curl http://astronomer-releases.astronomer.svc.cluster.local/astronomer-runtime
    ```

- If you have `curl` installed on your client machine:

    ```bash
    $ kubectl proxy
    # In a separate terminal window:
    $ curl http://localhost:8001/api/v1/namespaces/astronomer/services/astronomer-releases/astronomer-certified
    $ curl http://localhost:8001/api/v1/namespaces/astronomer/services/astronomer-releases/astronomer-runtime
    ```

- Complete the entire Software installation, then use one of the `astro-ui` pods which include `bash` and `curl`:

    ```bash
    $ kubectl exec -it astronomer-astro-ui-7cfbbb97fd-fv8kl -n=astronomer -- /bin/bash
    $ curl http://astronomer-releases.astronomer.svc.cluster.local/astronomer-certified
    $ curl http://astronomer-releases.astronomer.svc.cluster.local/astronomer-runtime
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
      url: http://astronomer-releases.astronomer.svc.cluster.local/astronomer-certified
    updateRuntimeCheck: # Configure URL for Airflow updates check
      url: http://astronomer-releases.astronomer.svc.cluster.local/astronomer-runtime
    config:
      deployments:
        helm:
          airflow:
            extraEnv:
            - name: AIRFLOW__ASTRONOMER__UPDATE_URL
              value: http://astronomer-releases.astronomer.svc.cluster.local/astronomer-runtime
```

## Step 6: Create a Kubernetes TLS Secret

Store the public TLS certificate in a kubernetes secret in the Astronomer platform namespace. If you use a third-party ingress controller, this secret must be named `astronomer-tls`. You must use `astronomer-tls` exactly. There is no substitution for platform release name. Additionally, make sure the value of `global.tlsSecret` in your `values.yaml` is also set to `astronomer-tls`.

To store the secret in the Astronomer platform namespace, run the following command:

```sh
kubectl -n <astronomer platform namespace> create secret tls astronomer-tls --cert <your-certificate-filepath> --key <your-private-key-filepath>
```

Most third-party ingress-controllers require the public certificate to be available in the namespace of the various airflow instances. If using a third-party ingress-controller, run the following command to mark the secret for automatic replication into Astronomer-managed Airflow namespaces. When you run the command, substitute both instances of `<astronomer-platform-namespace>` with the name of the Astronomer Software platform namespace:

```sh
kubectl -n <astronomer-platform-namespace> annotate secret astronomer-tls "astronomer.io/commander-sync"="platform=<astronomer platform namespace>"
```

If you received a certificate from a private CA, you also need to follow these steps:

1. Add the root certificate provided to you by your security team to an [Opaque Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types) in the Astronomer namespace by running the following command:

    ```sh
    kubectl create secret generic private-root-ca --from-file=cert.pem=./<your-certificate-filepath> -n astronomer
    ```

    The root certificate that you specify with this command must be the certificate of the authority that signed the Astronomer certificate, rather than the Astronomer certificate itself. This is the same certificate you need to install with all your clients for them to trust your services.

    :::info
    
    The name of the secret file must be `cert.pem` for Astronomer to properly trust your certificate.
    
    :::
    

2. Note the value of `private-root-ca`. You need this value to configure your Helm chart in Step 7 to specify the `privateCaCerts` key-value pair with this value.

## Step 7: Install Astronomer using Helm

Before completing this step, double-check that the following statements are true:

- You made Astronomer's Docker images, Astronomer Airflow Helm chart, and updates JSON accessible inside your network.
- You completed Steps 1 through 8 in the [AWS](install-aws-standard.md), [Azure](install-azure-standard.md), or [GCP](install-gcp-standard.md) install guide.

After this check, you can install the Astronomer Helm chart by running the following commands, making sure to replace `<your-image-tag>` with the version of Astronomer that you want to install:

```bash
curl -L https://github.com/astronomer/astronomer/archive/v<your-image-tag>.tar.gz -o astronomer.tgz

# Alternatively, use helm pull to pull the latest version of Astronomer
helm pull astronomer/astronomer

# ... If necessary, copy to a place where you can access Kubernetes ...
helm install astronomer -f values.yaml -n astronomer astronomer.tgz
```

After these commands finish, continue your installation with Step 10 (Verify pods are up) in the [AWS](install-aws-standard.md#step-10-verify-pods-are-up), [Azure](install-azure-standard.md#step-10-verify-all-pods-are-up), or [GCP](install-gcp-standard.md#step-10-verify-that-all-pods-are-up) installation guide.
