---
title: "GCP GKE Installation Guide"
navTitle: "Standard Installation"
description: "How to install Astronomer on Google Cloud Platform (GCP)."
---

This guide describes the steps to install Astronomer on Google Cloud Platform (GCP), which allows you to deploy and scale any number of [Apache Airflow](https://airflow.apache.org/) deployments within an [GCP Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/) cluster.

## Prerequisites

To install Astronomer on GCP, you'll need access to the following tools and permissions:

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Google Cloud SDK](https://cloud.google.com/sdk/install)
* [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* A compatible version of Kubernetes as described in Astronomer's [Version Compatibility Reference](https://www.astronomer.io/docs/enterprise/stable/resources/version-compatibility-reference)
* [Helm v3.2.1](https://github.com/helm/helm/releases/tag/v3.2.1)
* An SMTP Service & Credentials (e.g. Mailgun, Sendgrid, etc.)
* Permission to create and modify resources on Google Cloud Platform
* Permission to generate a certificate (not self-signed) that covers a defined set of subdomains


## Step 1: Choose a Base Domain

All Astronomer services will be tied to a base domain of your choice, under which you will need the ability to add and edit DNS records.

Once created, your Astronomer base domain will be linked to a variety of sub-services that your users will access via the internet to manage, monitor and run Airflow on the platform.

For the base domain `astro.mydomain.com`, for example, here are some corresponding URLs that your users would be able to reach:

* Astronomer UI: `app.astro.mydomain.com`
* Airflow Deployments: `deployments.astro.mydomain.com/uniquely-generated-airflow-name/airflow`
* Grafana Dashboard: `grafana.astro.mydomain.com`
* Kibana Dashboard: `kibana.astro.mydomain.com`

For the full list of subdomains, see Step 4.

## Step 2: Configure GCP for Astronomer Deployment

> Note: You can view Google Cloud Platform's Web Console at https://console.cloud.google.com/

### Create a GCP Project

Login to your Google account with the `gcloud` CLI:
```
$ gcloud auth login
```

Create a project:
```
$ gcloud projects create [PROJECT_ID]
```

Confirm the project was successfully created:
```
$ gcloud projects list
PROJECT_ID             NAME                PROJECT_NUMBER
astronomer-project     astronomer-project  364686176109
```

Configure the `gcloud` CLI for use with your new project:
```
$ gcloud config set project [PROJECT_ID]
```

Set your preferred compute zone, which will have a compute region tied to it.

You'll need this later on:

```
$ gcloud compute zones list
$ gcloud config set compute/zone [COMPUTE_ZONE]
```

### Create a GKE Cluster

Now that you have a GCP project to work with, the next step is to create a GKE (Google Kubernetes Engine) cluster that the Astronomer platform can be deployed into. Learn more about GKE [here](https://cloud.google.com/kubernetes-engine/).

First, enable the [Google Kubernetes Engine API](https://console.cloud.google.com/apis/library/container.googleapis.com?q=kubernetes%20engine).

Then, create a Kubernetes cluster via the `gcloud` CLI:

```
$ gcloud container clusters create [CLUSTER_NAME] --zone [COMPUTE_ZONE] --cluster-version [VERSION] --machine-type n1-standard-8 --enable-autoscaling --max-nodes 10 --min-nodes 3
```

A few important notes:

- Each version of Astronomer Enterprise is compatible with only a particular set of Kubernetes versions. For more information, refer to Astronomer's [Version Compatibility Reference](https://www.astronomer.io/docs/enterprise/stable/resources/version-compatibility-reference).
- We recommend using the [`n1-standard-8` machine type](https://cloud.google.com/compute/docs/machine-types#n1_standard_machine_types) with a minimum of 3 nodes (24 CPUs) as a starting point.
- The Astronomer platform and all components within it will consume ~11 CPUs and ~40GB of memory as the default overhead, so we generally recommend using larger vs smaller nodes.
- For more detailed instructions and a full list of optional flags, refer to GKE's ["Creating a Cluster"](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-cluster).

If you work with multiple Kubernetes environments, `kubectx` is an incredibly useful tool for quickly switching between Kubernetes clusters. Learn more [here](https://github.com/ahmetb/kubectx).


### Create a Static IP Address

Generate a static IP address:
```
$ gcloud compute addresses create astronomer-ip --region [COMPUTE_REGION] --project [PROJECT_ID]
```

View your newly generated IP address and record the output for use later on:
```
$ gcloud compute addresses describe astronomer-ip --region [COMPUTE_REGION] --project [PROJECT_ID] --format 'value(address)'
```

## Step 3: Configure Helm with Your GKE Cluster

Helm is a package manager for Kubernetes. It allows you to easily deploy complex Kubernetes applications. You'll use helm to install and manage the Astronomer platform. Learn more about helm [here](https://helm.sh/).

### Create a Kubernetes Namespace

Create a namespace to host the core Astronomer Platform. If you are running through a standard installation, each Airflow deployment you provision will be created in a separate namespace that our platform will provision for you, this initial namespace will just contain the core Astronomer platform.

```
$ kubectl create namespace <my-namespace>
```

## Step 4: Configure TLS

We recommend running Astronomer Enterprise on a dedicated domain (`BASEDOMAIN`) or subdomain (`astro.BASEDOMAIN`).

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

To obtain a TLS certificate, complete one of the following setups:

* **Option 1:** Obtain a TLS certificate from Let's Encrypt. We recommend this option for smaller organizations where your DNS administrator and Kubernetes cluster administrator are either the same person or on the same team.
* **Option 2:** Request a TLS certificate from your organization's security team. We recommend this option for large organizations with their own  protocols for generating TLS certificates.

### Option 1: Create TLS certificates using Let's Encrypt

[Let's Encrypt](https://letsencrypt.org/) is a free and secure certificate authority (CA) service that provides TLS certificates that renew automatically every 90 days. Use this option if you are configuring Astronomer for a smaller organization without a dedicated security team.

To set up TLS certificates this way, follow the guidelines in [Automatically Renew TLS Certificates Using Let's Encrypt](https://www.astronomer.io/docs/enterprise/stable/manage-astronomer/renew-tls-cert#automatically-renew-tls-certificates-using-lets-encrypt).

### Option 2: Request a TLS certificate from your security team

If you're installing Astronomer for a large organization, you'll need to request a TLS certificate and private key from your enterprise security team. This certificate needs to be valid for the `BASEDOMAIN` your organization uses for Astronomer, as well as the subdomains listed at the beginning of Step 4. You should be given two `.pem` files:

- One for your encrypted certificate
- One for your private key

To confirm that your enterprise security team generated the correct certificate, run the following command using the `openssl` CLI:

```sh
$ openssl x509 -in?? <your-certificate-filepath> -text -noout
```

This command will generate a report. If the `X509v3 Subject Alternative Name` section of this report includes either a single `*.BASEDOMAIN` wildcard domain or the subdomains listed at the beginning of Step 4, then the certificate creation was successful.

Depending on your organization, you may receive either a globally trusted certificate or a certificate from a private CA. The certificate from your private CA may include a domain certificate, a root certificate, and/or intermediate certificates, all of which need to be in proper certificate order. To verify certificate order, follow the guidelines below.

#### Verify certificate order (private CA only)

To confirm that your certificate has the proper certificate order, first run the following command using the `openssl` CLI:

```sh
$ openssl crl2pkcs7 -nocrl -certfile <your-certificate-filepath> | openssl pkcs7 -print_certs -noout
```

This command will generate a report of all certificates included. Verify that the order of these certificates is as follows:

1. Domain
2. Intermediate (optional)
3. Root

If the order of all certificates is correct, read below for instructions on how to create a Kubernetes secret using your new root certificate.

#### Create a Kubernetes secret

If you received a globally trusted certificate, simply run the following command and proceed to Step 5:

```sh
$ kubectl create secret tls astronomer-tls --cert <your-certificate-filepath> --key <your-private-key-filepath>
```

If you received a certificate from a private CA, follow the steps below instead:

1. Add the root certificate provided by your security team to an [Opaque Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types) in the Astronomer namespace by running the following command:

    ```sh
    $ kubectl create secret generic private-root-ca --from-file=cert.pem=./<your-certificate-filepath>
    ```

    > **Note:** The root certificate which you specify here should be the certificate of the authority that signed the Astronomer certificate, rather than the Astronomer certificate itself. This is the same certificate you need to install with all clients to get them to trust your services. 

    > **Note:** The name of the secret file must be `cert.pem` for your certificate to be trusted properly.

2. Note the value of `private-root-ca` for when you configure your Helm chart in Step 6. You'll need to additionally specify the `privateCaCerts` key-value pair with this value for that step.

## Step 5: Configure the Database

Astronomer by default requires a central Postgres database that will act as the backend for Astronomer's Houston API and will host individual Metadata Databases for all Airflow Deployments spun up on the platform.

While you're free to configure any database, most GCP users on Astronomer run [Google Cloud SQL](https://cloud.google.com/sql/). For production environments, we _strongly_ recommend a managed Postgres solution.

> **Note:** If you're setting up a development environment, this step is optional. Astronomer can be configured to deploy the PostgreSQL helm chart as the backend database with the following set in your `config.yaml`:
> ```
> global:
>   postgresqlEnabled: true
> ```

To connect to an external database to your GKE cluster, create a Kubernetes Secret named `astronomer-bootstrap` that points to your database.

```bash
kubectl create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://USERNAME:$PASSWORD@host:5432" \
  --namespace astronomer
```

## Step 6: Configure Your Helm Chart

As a next step, create a file named `config.yaml` in an empty directory.

For context, this `config.yaml` file will assume a set of default values for our platform that specify everything from user role definitions to the Airflow images you want to support. As you grow with Astronomer and want to customize the platform to better suit your team and use case, your `config.yaml` file is the best place to do so.

In the newly created file, copy the example below and replace `baseDomain`, `private-root-ca`, `/etc/docker/certs.d`, `ssl.enabled`, and `smtpUrl` with your own values. For more example configuration files, go [here](https://github.com/astronomer/astronomer/tree/master/configs).


```yaml
#################################
### Astronomer global configuration
#################################
global:
?? # Base domain for all subdomains exposed through ingress
?? baseDomain: astro.mydomain.com

?? # Name of secret containing TLS certificate
?? tlsSecret: astronomer-tls

?? # Enable privateCaCerts only if your enterprise security team
?? # generated a certificate from a private certificate authority.
?? privateCaCerts:
?? - private-root-ca

?? # Enable privateCaCertsAddToHost only when your nodes do not already
?? # include the private CA in their docker trust store.
?? # Most enterprises already have this configured,
?? # and in that case 'enabled' should be false.
?? privateCaCertsAddToHost:
?? ?? enabled: true
?? ?? hostDirectory: /etc/docker/certs.d
  # For development or proof-of-concept, you can use an in-cluster database
?? postgresqlEnabled: false

  # Enables using SSL connections to
  # encrypt client/server communication
  # between databases and the Astronomer platform.
  # If your database enforces SSL for connections,
  # change this value to true
  ssl:
    enabled: false
#################################
### Nginx configuration
#################################
nginx:
?? # IP address the nginx ingress should bind to
?? loadBalancerIP: ~

#################################
### SMTP configuration
#################################

astronomer:
?? houston:
?? ?? config:
?? ?? ?? publicSignups: false # Users need to be invited to have access to Astronomer. Set to true otherwise
?? ?? ?? emailConfirmation: true # Users get an email verification before accessing Astronomer
?? ?? ?? deployments:
?? ?? ?? ?? manualReleaseNames: true # Allows you to set your release names
?? ?? ?? ?? serviceAccountAnnotationKey: iam.gke.io/gcp-service-account  # Flag to enable using IAM roles (don't enter a specific role)
?? ?? ?? email:
?? ?? ?? ?? enabled: true
?? ?? ?? ?? smtpUrl: YOUR_URI_HERE
?? ?? ?? ?? reply: "noreply@astronomer.io" # Emails will be sent from this address
?? ?? ?? auth:
?? ?? ?? ?? github:
?? ?? ?? ?? ?? enabled: true # Lets users authenticate with Github
?? ?? ?? ?? local:
?? ?? ?? ?? ?? enabled: false # Disables logging in with just a username and password
?? ?? ?? ?? openidConnect:
?? ?? ?? ?? ?? google:
?? ?? ?? ?? ?? ?? enabled: true # Lets users authenticate with Google
```

 SMTP is required and will allow users to send and accept email invites to Astronomer. The SMTP URI will take the following form:

```yml
smtpUrl: smtps://USERNAME:PW@HOST/?pool=true
```

These are the minimum values you need to configure for installing Astronomer. For information on additional configuration, read [What's Next](https://www.astronomer.io/docs/enterprise/next/install/gcp/install-gcp-standard#whats-next).

## Step 7: Install Astronomer

Now that you have a GCP cluster set up and your `config.yaml` defined, you're ready to deploy all components of our platform.

First, run:

```
$ helm repo add astronomer https://helm.astronomer.io/
```

Then, run:

```sh
$ helm repo update
```

This will ensure that you pull the latest from our Helm repository. Finally, run:

```sh
$ helm install -f config.yaml --version=0.23 --namespace=<your-platform-namespace> <your-platform-release-name> astronomer/astronomer
```

This command will install the latest available patch version of Astronomer Enterprise v0.23. To override latest and specify a patch, add it to the `--version=` flag in the format of `0.23.x`. To install Astronomer Enterprise v0.23.9, for example, specify `--version=0.23.9`. For information on all available patch versions, refer to [Enterprise Release Notes](/docs/enterprise/stable/resources/release-notes/).

Once you run the commands above, a set of Kubernetes pods will be generated in your namespace. These pods power the individual services required to run our platform, including the Astronomer UI and Houston API.

## Step 8: Verify That All Pods Are Up

To verify all pods are up and running, run:

```
$ kubectl get pods --namespace <my-namespace>
```

You should see something like this:

```
$ kubectl get pods --namespace astronomer
NAME                                                    READY   STATUS      RESTARTS   AGE
newbie-norse-alertmanager-0                            1/1     Running     0          30m
newbie-norse-cli-install-565658b84d-bqkm9              1/1     Running     0          30m
newbie-norse-commander-7d9fd75476-q2vxh                1/1     Running     0          30m
newbie-norse-elasticsearch-client-7cccf77496-ks2s2     1/1     Running     0          30m
newbie-norse-elasticsearch-client-7cccf77496-w5m8p     1/1     Running     0          30m
newbie-norse-elasticsearch-curator-1553734800-hp74h    1/1     Running     0          30m
newbie-norse-elasticsearch-data-0                      1/1     Running     0          30m
newbie-norse-elasticsearch-data-1                      1/1     Running     0          30m
newbie-norse-elasticsearch-exporter-748c7c94d7-j9cvb   1/1     Running     0          30m
newbie-norse-elasticsearch-master-0                    1/1     Running     0          30m
newbie-norse-elasticsearch-master-1                    1/1     Running     0          30m
newbie-norse-elasticsearch-master-2                    1/1     Running     0          30m
newbie-norse-elasticsearch-nginx-5dcb5ffd59-c46gw      1/1     Running     0          30m
newbie-norse-fluentd-gprtb                             1/1     Running     0          30m
newbie-norse-fluentd-qzwwn                             1/1     Running     0          30m
newbie-norse-fluentd-rv696                             1/1     Running     0          30m
newbie-norse-fluentd-t8mqt                             1/1     Running     0          30m
newbie-norse-fluentd-wmjvh                             1/1     Running     0          30m
newbie-norse-grafana-57df948d9-jv2m9                   1/1     Running     0          30m
newbie-norse-houston-dbc647654-tcxbz                   1/1     Running     0          30m
newbie-norse-kibana-58bdf9bdb8-2j67t                   1/1     Running     0          30m
newbie-norse-kube-state-549f45544f-mcv7m               1/1     Running     0          30m
newbie-norse-nginx-7f6b5dfc9c-dm6tj                    1/1     Running     0          30m
newbie-norse-nginx-default-backend-5ccdb9554d-5cm5q    1/1     Running     0          30m
newbie-norse-orbit-d5585ccd8-h8zkr                     1/1     Running     0          30m
newbie-norse-prisma-699bd664bb-vbvlf                   1/1     Running     0          30m
newbie-norse-prometheus-0                              1/1     Running     0          30m
newbie-norse-registry-0                                1/1     Running     0          30m
```

If you are seeing issues here, check out our [guide on debugging your installation](/docs/enterprise/stable/troubleshoot/debug-install/)

## Step 9: Verify You Can Access the Astronomer UI

Go to `app.BASEDOMAIN` to see the Astronomer UI.

Consider this your new Airflow control plane. From the Astronomer UI, you'll be able to both invite and manage users as well as create and monitor Airflow Deployments on the platform.

## Step 10: Verify Your TLS Setup

To check if your TLS certificates were accepted, log in to the Astronomer UI. Then, go to `app.BASEDOMAIN/token` and run:

```
$ curl -v -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"
```

Verify that this output matches with that of the following command, which doesn't look for TLS:

```
$ curl -v -k -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"
```

Next, to make sure the registry is accepted by Astronomer's local docker client, try authenticating to Astronomer with the Astronomer CLI:

```sh
$ astro auth login <your-astronomer-base-domain>
```

If you can log in, then your Docker client trusts the registry. If Docker does not trust the Astronomer registry, run the following and restart Docker:

```
$ mkdir -p /etc/docker/certs.d
$ cp privateCA.pem /etc/docker/certs.d/
```

Finally, try running `$ astro deploy` on a test deployment. Create a deployment in the Astronomer UI, then run:
```sh
$ mkdir demo
$ cd demo
$ astro airflow init
$ astro deploy -f
```
Check the Airflow namespace. If pods are changing at all, then the Houston API trusts the registry.

If you have Airflow pods in the state "ImagePullBackoff", check the pod description. If you see an x509 error, ensure that you added the `privateCaCertsAddToHost` key-value pairs to your Helm chart. If you missed these during installation, follow the steps in [Apply a Platform Configuration Change on Astronomer](https://www.astronomer.io/docs/enterprise/stable/manage-astronomer/apply-platform-config) to add them after installation.

## What's Next

To help you make the most of Astronomer Enterprise, check out the following additional resources:

* [Renew TLS Certificates on Astronomer Enterprise](/docs/enterprise/stable/manage-astronomer/renew-tls-cert/)
* [Integrating an Auth System](/docs/enterprise/stable/manage-astronomer/integrate-auth-system/)
* [Configuring Platform Resources](/docs/enterprise/stable/manage-astronomer/configure-platform-resources/)
* [Managing Users on Astronomer Enterprise](/docs/enterprise/stable/manage-astronomer/manage-platform-users/)

### Astronomer Support Team

If you have any feedback or need help during this process and aren't in touch with our team already, a few resources to keep in mind:

* [Community Forum](https://forum.astronomer.io): General Airflow + Astronomer FAQs
* [Astronomer Support Portal](https://support.astronomer.io/hc/en-us/): Platform or Airflow issues

For detailed guidelines on reaching out to Astronomer Support, reference our guide [here](/docs/enterprise/stable/resources/support/).
