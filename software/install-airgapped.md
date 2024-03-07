---
title: "Install Astronomer Software in an airgapped environment"
sidebar_label: "Install in an airgapped environment"
description: "Infrastructure considerations and Helm configuration to install Astronomer in an airgapped environment"
id: install-airgapped
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

By default, the Software installation process requires accessing public repositories to download the following components:

- Docker images from `quay.io/astronomer` or `docker.io`
- Astronomer Helm charts from `helm.astronomer.io`
- Astronomer version information from `updates.astronomer.io`

If you cannot use public repositories and networks for your installation, you can install Astronomer in an airgapped environment. An airgapped environment is a locked-down environment with no access to or from the public internet.

This guide explains how to configure your system to install Astronomer without access to the public internet by moving Astronomer images to an accessible registry in your airgapped environment. After completing this setup, follow Steps 1 to 8 in the [AWS](install-aws-standard.md), [Azure](install-azure-standard.md), or [GCP](install-gcp-standard.md) installation guide to finish your installation.

## Prerequisites

<Tabs
    defaultValue="aws"
    groupId= "prerequisites"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
        {label: 'Azure', value: 'azure'},
    ]}>

<TabItem value="aws">

To complete this setup, you need:

- The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).
- A VPC.
- A private Kubernetes environment. For versioning considerations, see [Version Compatibility Reference](version-compatibility-reference.md).
- A VPN (or other means) to access, at a minimum, Kubernetes and DNS from inside your VPC.
- A PostgreSQL instance accessible from your Kubernetes environment. For versioning considerations, see [Version Compatibility Reference](version-compatibility-reference.md).
- The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html)
- [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
- An SMTP service and credentials. For example, Mailgun or Sendgrid.
- Permission to create and modify resources on AWS.
- Permission to generate a certificate (not self-signed) that covers a defined set of subdomains.
- PostgreSQL superuser permissions.
- An AWS Load Balancer Controller for the IP target type is required for all private Network Load Balancers (NLBs). See [Installing the AWS Load Balancer Controller add-on](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html).  
- If you use Kubernetes version 1.23 or later, the [Amazon EBS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html).
- (Optional) [`eksctl`](https://eksctl.io/) for creating and managing your Astronomer cluster on EKS.

</TabItem>

<TabItem value="gcp">

- [Google Cloud SDK](https://cloud.google.com/sdk/install)
- A VPC.
- A private Kubernetes environment. For versioning considerations, see [Version Compatibility Reference](version-compatibility-reference.md).
- A VPN (or other means) to access, at a minimum, Kubernetes and DNS from inside your VPC.
- A PostgreSQL instance accessible from your Kubernetes environment. For versioning considerations, see [Version Compatibility Reference](version-compatibility-reference.md).
- The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html)
- [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
- An SMTP service and credentials. For example, Mailgun or Sendgrid.
- Permission to create and modify resources on Google Cloud Platform
- Permission to generate a certificate (not self-signed) that covers a defined set of subdomains.
- PostgreSQL superuser permissions.
- An AWS Load Balancer Controller for the IP target type is required for all private Network Load Balancers (NLBs). See [Installing the AWS Load Balancer Controller add-on](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html).  
- If you use Kubernetes version 1.23 or later, the [Amazon EBS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html).
- (Optional) [`eksctl`](https://eksctl.io/) for creating and managing your Astronomer cluster on EKS.

:::info

There is a known bug on GCP GKE Dataplane V2 clusters that affects Astronomer Software installations. When Astronomer Software is installed on a GCP GKE Dataplane V2 cluster, the interaction between the Astronomer Nginx ingress controller and Cilium can cause dropped connections, dropped packets, and intermittent 504 timeout errors when accessing the Astronomer UI or Houston API.

To avoid these issues, Astronomer recommends installing Astronomer Software on a GKE Dataplane V1 cluster. 

:::

</TabItem>

<TabItem value="azure">

- A VPC.
- A private Kubernetes environment. For versioning considerations, see [Version Compatibility Reference](version-compatibility-reference.md).
- A VPN (or other means) to access, at a minimum, Kubernetes and DNS from inside your VPC.
- A PostgreSQL instance accessible from your Kubernetes environment. For versioning considerations, see [Version Compatibility Reference](version-compatibility-reference.md).
- The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html)
- [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
- An SMTP service and credentials. For example, Mailgun or Sendgrid.
- The [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- Permission to create and modify resources on Azure
- Permission to generate a certificate (not self-signed) that covers a defined set of subdomains
- PostgreSQL superuser permissions
- If your organization uses Azure Database for PostgreSQL as the database backend, you need to enable the `pg_trgm` extension using the Azure portal or the Azure CLI before you install Astronomer Software. If you don't enable the `pg_trgm` extension, the install will fail. For more information about enabling the `pg_trgm` extension, see [PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions).


</TabItem>


## Step 1: Choose a base domain

All Astronomer services will be tied to a base domain of your choice, under which you will need the ability to add and edit DNS records.

Once created, your Astronomer base domain will be linked to a variety of sub-services that your users will access via the internet to manage, monitor and run Airflow on the platform.

For the base domain `astro.mydomain.com`, for example, here are some corresponding URLs that your users would be able to reach:

- Software UI: `app.astro.mydomain.com`
- Airflow Deployments: `deployments.astro.mydomain.com/deployment-release-name/airflow`
- Grafana Dashboard: `grafana.astro.mydomain.com`
- Kibana Dashboard: `kibana.astro.mydomain.com`

For the full list of subdomains, see Step 3.

## Step 2: Create a namespace

In your Kubernetes cluster, create a [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) called `astronomer` to host the core Astronomer platform:

```sh
kubectl create namespace astronomer
```

After Astronomer is running, each Airflow Deployment that you create will have its own isolated namespace.

## Step 3: Configure TLS

In order for users to access the web applications they need to manage Astronomer, you'll need a TLS certificate that covers the following subdomains:

```sh
BASEDOMAIN
app.BASEDOMAIN
deployments.BASEDOMAIN
registry.BASEDOMAIN
houston.BASEDOMAIN
grafana.BASEDOMAIN
kibana.BASEDOMAIN
install.BASEDOMAIN
alertmanager.BASEDOMAIN
prometheus.BASEDOMAIN
```

:::warning

Astronomer requires you to use RSA to sign TLS certificates. By default, [Certbot](https://certbot.eff.org/) uses Elliptic Curve Digital Signature Algorithm (ECDSA) keys to sign certificates. If you're using Certbot to sign your TLS certificate, you must include `-key-type rsa --rsa-key-size 2048` in your command to sign your certificate with an RSA key. If you don't use RSA keys, deploys fail and error messages appear in the registry and Houston logs. For example, you can run the following command to sign your certificate with an RSA key:

```sh
sudo certbot certonly --manual --preferred-challenges=dns -d -d *. --key-type=rsa
```

:::

Request a TLS certificate and private key from your enterprise security team. This certificate needs to be valid for the `BASEDOMAIN` your organization uses for Astronomer, as well as the subdomains listed at the beginning of Step 4. You should be given two `.pem` files:

* One for your encrypted certificate
* One for your private key

To confirm that your enterprise security team generated the correct certificate, run the following command using the `openssl` CLI:

```sh
openssl x509 -in  <your-certificate-filepath> -text -noout
```

This command will generate a report. If the `X509v3 Subject Alternative Name` section of this report includes either a single `*.BASEDOMAIN` wildcard domain or the subdomains listed at the beginning of Step 4, then the certificate creation was successful.

Depending on your organization, you may receive either a globally trusted certificate or a certificate from a private CA. The certificate from your private CA may include a domain certificate, a root certificate, and/or intermediate certificates, all of which need to be in proper certificate order. To verify certificate order, follow the guidelines below.

### Confirm certificate chain order

If your organization is using a private certificate authority, you'll need to confirm that your certificate chain is ordered correctly. To determine your certificate chain order, run the following command using the `openssl` CLI:

```sh
openssl crl2pkcs7 -nocrl -certfile <your-certificate-filepath> | openssl pkcs7 -print_certs -noout
```

The command generates a report of all certificates. Verify the order of the certificates is as follows:

- Domain
- Intermediate (optional)
- Root

If the certificate order is correct, proceed to step 5.

## Step 4: Create a Kubernetes TLS Secret

If you received a globally trusted certificate or created a self-signed certificate, create a Kubernetes TLS secret using the following command and then proceed to Step 6:

```sh
kubectl create secret tls astronomer-tls --cert <your-certificate-filepath> --key <your-private-key-filepath> -n astronomer
```

If you created a certificate using Let's Encrypt, the `astronomer-tls` secret already exists in your Kubernetes cluster. Run the following command to confirm it exists: 

```bash
kubectl describe secret astronomer-tls --namespace astronomer
```

If you received a certificate from a private CA, follow these steps instead:

1. Add the root certificate provided by your security team to an [Opaque Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types) in the Astronomer namespace by running the following command:

    ```sh
    kubectl create secret generic private-root-ca --from-file=cert.pem=./<your-certificate-filepath> -n astronomer
    ```

    > **Note:** The root certificate which you specify here should be the certificate of the authority that signed the Astronomer certificate, rather than the Astronomer certificate itself. This is the same certificate you need to install with all clients to get them to trust your services.

    > **Note:** The name of the secret file must be `cert.pem` for your certificate to be trusted properly.

2. Note the value of `private-root-ca` for when you configure your Helm chart in Step 8. You'll need to additionally specify the `privateCaCerts` key-value pair with this value for that step.

## Step 5: Configure your SMTP URI

An SMTP service is required for sending and accepting email invites from Astronomer. If you're running Astronomer Software with `publicSignups` disabled (which is the default), you'll need to configure SMTP as a way for your users to receive and accept invites to the platform via email. To integrate your SMTP service with Astronomer, fetch your SMTP service's URI and store it in a Kubernetes secret:

```sh
kubectl create secret generic astronomer-smtp --from-literal connection="smtp://USERNAME:PASSWORD@HOST/?requireTLS=true" -n astronomer
```

In general, an SMTP URI will take the following form:

```text
smtps://USERNAME:PASSWORD@HOST/?pool=true
```

The following table contains examples of what the URI will look like for some of the most popular SMTP services:

| Provider          | Example SMTP URL                                                                                 |
|-------------------|--------------------------------------------------------------------------------------------------|
| AWS SES           | `smtp://AWS_SMTP_Username:AWS_SMTP_Password@email-smtp.us-east-1.amazonaws.com/?requireTLS=true` |
| SendGrid          | `smtps://apikey:SG.sometoken@smtp.sendgrid.net:465/?pool=true`                                   |
| Mailgun           | `smtps://xyz%40example.com:password@smtp.mailgun.org/?pool=true`                                 |
| Office365         | `smtp://xyz%40example.com:password@smtp.office365.com:587/?requireTLS=true`                      |
| Custom SMTP-relay | `smtp://smtp-relay.example.com:25/?ignoreTLS=true`                                               |

If your SMTP provider is not listed, refer to the provider's documentation for information on creating an SMTP URI.


:::info 

If there are `/` or other escape characters in your username or password, you may need to [URL encode](https://www.urlencoder.org/) those characters.

:::

## Step 6: Retrieve the Astronomer platform Helm chart

Starting in the next step, you might need to modify Astronomer's Helm chart to customize your Astronomer installation to your use case. Making changes to the Astronomer Helm chart is the primary method for customizing Astronomer Software. 

To download a templated Helm chart for your installation, run the following command:

```bash
helm template --version <your-astronomer-version> astronomer/astronomer --set global.dagOnlyDeployment.enabled=True --set global.loggingSidecar.enabled=True --set global.postgresqlEnabled=True --set global.authSidecar.enabled=True --set global.baseDomain=<your-basedomain> | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq                           
```

Save the 

## Step 7: Configure the database

By default, Astronomer requires a central Postgres database that acts as the backend for Astronomer's Houston API and will host individual metadata databases for all Airflow Deployments spun up on the platform.

:::info

If you're setting up a development environment, this step is optional. Astronomer can be configured to deploy the PostgreSQL helm chart as the backend database if you add the following to your `config.yaml` file:

```yaml
global:
  postgresqlEnabled: true
```

:::

To connect to an external database to your cluster, create a Kubernetes Secret named `astronomer-bootstrap` that points to your database.

```bash
kubectl create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://USERNAME:$PASSWORD@host:5432" \
  --namespace astronomer
```

:::info

You must URL encode any special characters in your Postgres password.

:::

A few additional configuration notes:

- (AWS Only) Astronomer recommends using a [t2 medium](https://aws.amazon.com/rds/instance-types/) as the minimum RDS instance size.
- If you provision an external database, `postgresqlEnabled` should be set to `false` in Step 8. The in-cluster database should be used only for development or proof-of-concept installations. All production installations should use an external database.
- (Azure only) If your organization uses Azure Database for PostgreSQL as the database backend, you need to enable the `pg_trgm` extension using the Azure portal or the Azure CLI before you install Astronomer Software. If you don't enable the `pg_trgm` extension, the install will fail. For more information about enabling the `pg_trgm` extension, see [PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions).
- (Azure only) If you provision Azure Database for PostgreSQL - Flexible Server, it enforces TLS/SSL and requires that you set `sslmode` to `prefer` in your `config.yaml`.


## Step 8: Configure a private Docker registry

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

## Step 9: Fetch images from Astronomer's Helm template

The images and tags which are required for your Software installation depend on the version of Astronomer you're installing. To gather a list of exact images and tags required for your Astronomer version:

1. Run the following command to template the Astronomer Helm chart and fetch all of its rendered image tags. Make sure to substitute `<your-basedomain>` and `<your-astronomer-version>` with your information.

    ```bash
    helm template --version <your-astronomer-version> astronomer/astronomer --set global.dagOnlyDeployment.enabled=True --set global.loggingSidecar.enabled=True --set global.postgresqlEnabled=True --set global.authSidecar.enabled=True --set global.baseDomain=<your-basedomain> | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq                           
    ```
    
    This command sets all possible Helm values that could impact which images are required for your installation. By fetching all images now, you save time by eliminating the risk of missing an image. 
  
2. Run the following command to template the Airflow Helm chart and fetch its rendered image tags:

    ```shell
    helm template --version <your-airflow-version> astronomer/airflow --set airflow.postgresql.enabled=false --set airflow.pgbouncer.enabled=true --set airflow.statsd.enabled=true --set airflow.executor=CeleryExecutor | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq
    ```

These commands generate a list of images required for your version of Astronomer. Add these images to a private image registry hosted within your organization's network. In Step 3, you will specify this private registry in your Astronomer configuration.

> **Note:** If you have already enabled or disabled Astronomer platform components in your `config.yaml`, you can pass `-f/--values config.yaml` to `helm template` to print a list specific to your `config.yaml` configuration.

## Step 10: Add images to your config.yaml file

Regardless of whether you choose to mirror or manually pull/push images to your private registry, the returned images and/or tags must be made accessible within your network.

To make these images accessible to Astronomer, specify your organization's private registry in the `global` section of your `config.yaml` file:

```yaml
global:
  privateRegistry:
    enabled: true
    repository: 012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo
    # secretName: ~
```

This configuration automatically pulls most Docker images required in the Astronomer Helm chart. You must also configure the following images individually in a separate section of your `config.yaml` file:

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

## Step 11: Fetch Airflow Helm charts

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

## Step 12: Fetch Airflow updates

By default, Astronomer checks for Airflow updates once a day at midnight by querying `https://updates.astronomer.io/astronomer-runtime`, which returns a JSON file with version details. However, this URL is not accessible in an airgapped environment. There are several options for making these updates accessible in an airgapped environment:

- You can download the JSON and host it in a location that's accessible within your airgapped environment, for example:
    - AWS S3
    - Git
    - Nginx (example below)
- You can disable the update checks (not advised)

This setup assumes that the updates JSON will be manually downloaded and added to your environment. For guidance on how to automate this process, reach out to your Astronomer contact.

### Exposing Airflow updates using an Nginx endpoint

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

## Step 13: Install Astronomer using Helm

Before completing this step, double-check that the following statements are true:

- You made Astronomer's Docker images, Airflow Helm chart, and updates JSON accessible inside your network.
- You completed Steps 1 through 8 in the [AWS](install-aws-standard.md), [Azure](install-azure-standard.md), or [GCP](install-gcp-standard.md) install guide.

After this check, you can install the Astronomer Helm chart by running the following commands, making sure to replace `<your-image-tag>` with the version of Astronomer that you want to install:

```bash
curl -L https://github.com/astronomer/astronomer/archive/v<your-image-tag>.tar.gz -o astronomer.tgz

# Alternatively, use helm pull to pull the latest version of Astronomer
helm pull astronomer/astronomer

# ... If necessary, copy to a place where you can access Kubernetes ...
helm install astronomer -f config.yaml -n astronomer astronomer.tgz
```

## Step 14: Verify Pods are up

To verify all pods are up and running, run:

```sh
kubectl get pods --namespace <my-namespace>
```

You should see something like this:

```command
$ kubectl get pods --namespace astronomer

NAME                                                       READY   STATUS              RESTARTS   AGE
astronomer-alertmanager-0                                  1/1     Running             0          24m
astronomer-astro-ui-7f94c9bbcc-7xntd                       1/1     Running             0          24m
astronomer-astro-ui-7f94c9bbcc-lkn5b                       1/1     Running             0          24m
astronomer-cli-install-88df56bbd-t4rj2                     1/1     Running             0          24m
astronomer-commander-84f64d55cf-8rns9                      1/1     Running             0          24m
astronomer-commander-84f64d55cf-j6w4l                      1/1     Running             0          24m
astronomer-elasticsearch-client-7786447c54-9kt4x           1/1     Running             0          24m
astronomer-elasticsearch-client-7786447c54-mdxpn           1/1     Running             0          24m
astronomer-elasticsearch-data-0                            1/1     Running             0          24m
astronomer-elasticsearch-data-1                            1/1     Running             0          24m
astronomer-elasticsearch-exporter-6495597c9f-ks4jz         1/1     Running             0          24m
astronomer-elasticsearch-master-0                          1/1     Running             0          24m
astronomer-elasticsearch-master-1                          1/1     Running             0          23m
astronomer-elasticsearch-master-2                          1/1     Running             0          23m
astronomer-elasticsearch-nginx-b954fd4d4-249sh             1/1     Running             0          24m
astronomer-fluentd-5lv2c                                   1/1     Running             0          24m
astronomer-fluentd-79vv4                                   1/1     Running             0          24m
astronomer-fluentd-hlr6v                                   1/1     Running             0          24m
astronomer-fluentd-l7zj9                                   1/1     Running             0          24m
astronomer-fluentd-m4gh2                                   1/1     Running             0          24m
astronomer-fluentd-q987q                                   1/1     Running             0          24m
astronomer-grafana-c487d5c7b-pjtmc                         1/1     Running             0          24m
astronomer-houston-544c8855b5-bfctd                        1/1     Running             0          24m
astronomer-houston-544c8855b5-gwhll                        1/1     Running             0          24m
astronomer-houston-upgrade-deployments-stphr               1/1     Running             0          24m
astronomer-kibana-596599df6-vh6bp                          1/1     Running             0          24m
astronomer-kube-state-6658d79b4c-hf2hf                     1/1     Running             0          24m
astronomer-kubed-6cc48c5767-btscx                          1/1     Running             0          24m
astronomer-nginx-746589b744-h6r5n                          1/1     Running             0          24m
astronomer-nginx-746589b744-hscb9                          1/1     Running             0          24m
astronomer-nginx-default-backend-8cb66c54-4vjmz            1/1     Running             0          24m
astronomer-nginx-default-backend-8cb66c54-7m86w            1/1     Running             0          24m
astronomer-prometheus-0                                    1/1     Running             0          24m
astronomer-prometheus-blackbox-exporter-65f6c5f456-865h2   1/1     Running             0          24m
astronomer-prometheus-blackbox-exporter-65f6c5f456-szr4s   1/1     Running             0          24m
astronomer-registry-0                                      1/1     Running             0          24m
```

If you are seeing issues here, check out our [guide on debugging your installation](debug-install.md).

## Step 11: Configure DNS

Now that you've successfully installed Astronomer, a new load balancer will have spun up in your AWS account. This load balancer routes incoming traffic to our NGINX ingress controller.

Run `$ kubectl get svc -n astronomer` to view your load balancer's CNAME, located under the `EXTERNAL-IP` column for the `astronomer-nginx` service.

```sh
$ kubectl get svc -n astronomer
NAME                                 TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)                                      AGE
astronomer-alertmanager              ClusterIP      172.20.48.232    <none>                                                                    9093/TCP                                     24d
astronomer-cli-install               ClusterIP      172.20.95.132    <none>                                                                    80/TCP                                       24d
astronomer-commander                 ClusterIP      172.20.167.227   <none>                                                                    8880/TCP,50051/TCP                           24d
astronomer-elasticsearch             ClusterIP      172.20.161.0     <none>                                                                    9200/TCP,9300/TCP                            24d
astronomer-elasticsearch-discovery   ClusterIP      172.20.225.200   <none>                                                                    9300/TCP                                     24d
astronomer-elasticsearch-exporter    ClusterIP      172.20.2.113     <none>                                                                    9108/TCP                                     24d
astronomer-elasticsearch-nginx       ClusterIP      172.20.154.232   <none>                                                                    9200/TCP                                     24d
astronomer-grafana                   ClusterIP      172.20.120.247   <none>                                                                    3000/TCP                                     24d
astronomer-houston                   ClusterIP      172.20.25.26     <none>                                                                    8871/TCP                                     24d
astronomer-kibana                    ClusterIP      172.20.134.149   <none>                                                                    5601/TCP                                     24d
astronomer-kube-state                ClusterIP      172.20.123.56    <none>                                                                    8080/TCP,8081/TCP                            24d
astronomer-kubed                     ClusterIP      172.20.4.200     <none>                                                                    443/TCP                                      24d
astronomer-nginx                     LoadBalancer   172.20.54.142    ELB_ADDRESS.us-east-1.elb.amazonaws.com                                   80:31925/TCP,443:32461/TCP,10254:32424/TCP   24d
astronomer-nginx-default-backend     ClusterIP      172.20.186.254   <none>                                                                    8080/TCP                                     24d
astronomer-astro-ui                  ClusterIP      172.20.186.166   <none>                                                                    8080/TCP                                     24d
astronomer-prometheus                ClusterIP      172.20.72.196    <none>                                                                    9090/TCP                                     24d
astronomer-registry                  ClusterIP      172.20.100.102   <none>                                                                    5000/TCP                                     24d
```

You will need to create a new CNAME record through your DNS provider using the ELB CNAME listed above. If you're using Amazon Route 53, see [Creating records by using the Amazon Route 53 console](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html).

You can create a single wildcard CNAME record such as `*.astro.mydomain.com`, or alternatively create individual CNAME records for the following routes:

```sh
app.astro.mydomain.com
deployments.astro.mydomain.com
registry.astro.mydomain.com
houston.astro.mydomain.com
grafana.astro.mydomain.com
kibana.astro.mydomain.com
install.astro.mydomain.com
alertmanager.astro.mydomain.com
prometheus.astro.mydomain.com
```

Example wildcard CNAME record:
![aws-elb](/img/software/route53.png)

## Step 15: Verify you can access the Software UI

Go to `app.BASEDOMAIN` to see the Software UI.

Consider this your new Airflow control plane. From the Software UI, you'll be able to both invite and manage users as well as create and monitor Airflow Deployments on the platform.

## Step 16: Verify your TLS setup

To check if your TLS certificates were accepted, log in to the Software UI. Then, go to `app.BASEDOMAIN/token` and run:

```sh
curl -v -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"
```

Verify that this output matches with that of the following command, which doesn't look for TLS:

```sh
curl -v -k -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"
```

Next, to make sure the registry is accepted by Astronomer's local docker client, try authenticating to Astronomer with the Astro CLI:

```sh
astro auth login <your-astronomer-base-domain>
```

If you can log in, then your Docker client trusts the registry. If Docker does not trust the Astronomer registry, run the following and restart Docker:

```sh
mkdir -p /etc/docker/certs.d
cp privateCA.pem /etc/docker/certs.d/
```

Finally, try running `$ astro deploy` on a test deployment. Create a deployment in the Software UI, then run:

```sh
mkdir demo
cd demo
astro dev init --use-astronomer-certified
astro deploy -f
```

Check the Airflow namespace. If pods are changing at all, then the Houston API trusts the registry.

If you have Airflow pods in the state `ImagePullBackoff`, check the pod description. If you see an x509 error, ensure that you have:

- Configured containerd’s `config_path` to point to `/etc/containerd/certs.d`.
- Added the `privateCaCertsAddToHost` key-value pairs to your Helm chart. 

If you missed these steps during installation, follow the steps in [Apply a config change](apply-platform-config.md) to add them after installation. If you are using a base image such as CoreOS that does not permit values to be changed, or you otherwise can't modify `config.yaml`, contact [Astronomer support](https://support.astronomer.io) for additional configuration assistance.

## What's next

To help you make the most of Astronomer Software, check out the following additional resources:
* [Renew TLS Certificates on Astronomer Software](renew-tls-cert.md)
* [Integrating an Auth System](integrate-auth-system.md)
* [Configuring Platform Resources](configure-platform-resources.md)
* [Managing Users on Astronomer Software](manage-platform-users.md)

### Astronomer support team

If you have any feedback or need help during this process and aren't in touch with our team already, a few resources to keep in mind:

* [Community Forum](https://forum.astronomer.io): General Airflow + Astronomer FAQs
* [Astronomer Support Portal](https://support.astronomer.io/hc/en-us/): Platform or Airflow issues

For detailed guidelines on reaching out to Astronomer Support, reference our guide [here](support.md).
