---
title: "Install Astronomer Software"
sidebar_label: "Install Astronomer Software"
description: "Install Astronomer Software in a multi-tenant, airgapped environment with all recommended security and networking configurations"
id: install-airgapped
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This guide describes the steps to install Astronomer Software, which allows you to deploy and scale any number of Apache Airflow deployments.

Astronomer recommends platform administrators perform their first Astronomer Software installation manually using the procedures described in this document.

Astronomer recommends platform administrators adapt the procedures contained in this document to meet organizational best-practices when deploying to change-controlled environments.

# MAJOR REWORK IN PROGRESS DO NOT COPY-EDIT


## Prerequisites

<Tabs
    defaultValue="aws"
    groupId= "prerequisites"
    values={[
        {label: 'EKS on AWS', value: 'aws'},
        {label: 'GKE on GCP', value: 'gcp'},
        {label: 'AKS on Azure', value: 'azure'},
        {label: 'Other', value: 'other'},
    ]}>

<TabItem value="aws">
The following prerequisites apply when running Astronomer Software on Amazon EKS (see the 'Other' tab if running a different version of Kubernetes on AWS).

- An EKS Kubernetes cluster, running a version of Kubernetes certified as compatible on the [Version Compatibility Reference](version-compatibility-reference.md) providing the following components.
  * The [Amazon EBS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html) (or an alternative CSI) must be installed on the Kubernetes Cluster.
  * An AWS Load Balancer Controller for the IP target type is required for all private Network Load Balancers (NLBs). See [Installing the AWS Load Balancer Controller add-on](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html).  
- A PostgreSQL instance, accessible from your Kubernetes cluster, and running a version of Postgres certified as compatible on the [Version Compatibility Reference]
(version-compatibility-reference.md).
- PostgreSQL superuser permissions.
- Permission to create and modify resources on AWS.
- Permission to generate a certificate that covers a defined set of subdomains.
- An SMTP service and credentials. For example, Mailgun or Sendgrid.
- The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).
- (Optional) [`eksctl`](https://eksctl.io/) for creating and managing your Astronomer cluster on EKS.
- A machine with access to the Kubernetes API Server meeting the following criteria:
  * Network access to the Kubernetes API Server - either directly or VPN.
  * Network access to load-balancer resources created when Astronomer Software is installed later in the procedure - either directly or via vpn.
  * Configured to use the DNS servers where Astronomer Software DNS records will be created.
  * [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
  * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) may be required to trouble-shoot certain certificate-related conditions.
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) may be required to trouble-shoot certain certificate-related conditions.

</TabItem>

<TabItem value="gcp">
The following prerequisites apply when running Astronomer Software on Google GKE (see the 'Other' tab if running a different version of Kubernetes on GCP).

- A GKE Kubernetes cluster, running a version of Kubernetes certified as compatible on the [Version Compatibility Reference](version-compatibility-reference.md).
- A PostgreSQL instance, accessible from your Kubernetes cluster, and running a version of Postgres certified as compatible on the [Version Compatibility Reference]
- PostgreSQL superuser permissions.
- Permission to create and modify resources on Google Cloud Platform
- Permission to generate a certificate that covers a defined set of subdomains.
- An SMTP service and credentials. For example, Mailgun or Sendgrid.
- [Google Cloud SDK](https://cloud.google.com/sdk/install)
- A machine with access to the Kubernetes API Server meeting the following criteria:
  * Network access to the Kubernetes API Server - either directly or VPN.
  * Network access to load-balancer resources created when Astronomer Software is installed later in the procedure - either directly or via vpn.
  * Configured to use the DNS servers where Astronomer Software DNS records will be created.
  * [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
  * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
  * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) may be required to trouble-shoot certain certificate-related conditions.


</TabItem>

<TabItem value="azure">
The following prerequisites apply when running Astronomer Software on Azure AKS (see the 'Other' tab if running a different version of Kubernetes on Azure).

- A Kubernetes cluster, running a version of Kubernetes certified as compatible on the [Version Compatibility Reference](version-compatibility-reference.md).
- A PostgreSQL instance, accessible from your Kubernetes cluster, and running a version of Postgres certified as compatible on the [Version Compatibility Reference]
  * If your organization uses Azure Database for PostgreSQL as the database backend, you need to enable the `pg_trgm` extension using the Azure portal or the Azure CLI before you install Astronomer Software. If you don't enable the `pg_trgm` extension, the install will fail. For more information about enabling the `pg_trgm` extension, see [PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions).
- PostgreSQL superuser permissions.
- Permission to create and modify resources on Azure
- Permission to generate a certificate that covers a defined set of subdomains
- An SMTP service and credentials. For example, Mailgun or Sendgrid.
- The [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- A machine with access to the Kubernetes API Server meeting the following criteria:
  * Network access to the Kubernetes API Server - either directly or VPN.
  * Network access to load-balancer resources created when Astronomer Software is installed later in the procedure - either directly or via vpn.
  * Configured to use the DNS servers where Astronomer Software DNS records will be created.
  * [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
  * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
  * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) may be required to trouble-shoot certain certificate-related conditions.


</TabItem>

<TabItem value="other">
The following prerequisites apply when running Astronomer Software on Kubernetes.

- A Kubernetes cluster. For versioning considerations, see [Version Compatibility Reference](version-compatibility-reference.md).
- A PostgreSQL instance accessible from your Kubernetes cluster. For versioning considerations, see [Version Compatibility Reference](version-compatibility-reference.md).
- PostgreSQL superuser permissions.
- An SMTP service and credentials. For example, Mailgun or Sendgrid.
- Permission to generate a certificate that covers a defined set of subdomains.
- PostgreSQL superuser permissions.
- The ability to create DNS records.
- A machine with access to the Kubernetes API Server meeting the following criteria:
  * Network access to the Kubernetes API Server - either directly or VPN.
  * Network access to load-balancer resources created when Astronomer Software is installed later in the procedure - either directly or via vpn.
  * Configured to use the DNS servers where Astronomer Software DNS records will be created.
  * [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
  * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) may be required to trouble-shoot certain certificate-related conditions.
</TabItem>

</Tabs>

## Step 1: Determining how to structure and organize your platform environments {#determining-how-to-structure-and-organize-your-platform-environments}
The procedures detailed in this document create an Astronomer Software platform-instance that will be used used to deploy and manage multiple Airflow installations.

Do not install multiple instances of Astronomer Software onto the same Kubernetes cluster.

Plan a series of environments so that Astronomer Software platform-upgrades and Kubernetes upgrades can be tested in advance, e.g.:
  * sandbox - lowest environment, contains no sensitive-data, used only by system-administrators to experiment, not subject to change-control
  * development - user-accessible, subject to most of the restrictions of higher environments, relaxed change-control
  * staging - all network/security/patch-versions in lock-step with production, no availability guarantees, relaxed change-control
  * production - hosts production Airflow instances (dev airflow instances may live here or in lower environments)

### Create a platform-project directory{#platform-deployment-project-directory}
Create a platform-project directory to store files you will be creating throughout this installation guide.

e.g.
`mkdir ~/astronomer-dev`

:::tip

Certain files in this directory may contain secrets. For your first install, keep these in a secure place on a suitable machine. As you progress to higher environments, vault these files seperately and use the remaining files to serve as the basis for your CI/CD deployment.

:::

## Step 2: Create values.yaml from a template {#create-valuesyaml-from-a-template}

Choose the template below that corresponds to your Kubernetes Platform and save it to a file named `values.yaml` in your platform-project directory.

* Do not make any changes to this file until instructed to do so in later steps.
* Do not apply this file with helm until instructed to do so in later steps.

:::tip

Create a platform-project directory for each platform environment to store values.yaml and other files you will be creating throughout this installation guide. e.g. store as `astronomer-sandbox/values.yaml`.

:::


Subsequent steps of this installation guide will instruct you to review or make changes to the contents of `values.yaml`. As you make changes to this file, do not apply them to the cluster until you reach the step where are you are explicitly instructed to apply the platform configurtation.

This file defines major platform configuration settings for the Astronomer Software Platform and must be present to install, upgrade, or reconfigure Astronomer Software. You'll continually modify this file as you grow with Astronomer Software and want to take advantage of new features.


<Tabs
    defaultValue="aws"
    groupId= "prerequisites"
    values={[
        {label: 'EKS on AWS', value: 'aws'},
        {label: 'GKE on GCP', value: 'gcp'},
        {label: 'AKS on Azure', value: 'azure'},
        {label: 'Other', value: 'other'},
    ]}>

<TabItem value="aws">

```yaml
#################################
### Astronomer global configuration for EKS
#################################
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: sandbox-astro.example.com

  # Name of secret containing TLS certificate
  tlsSecret: astronomer-tls

  # List of secrets containing the cert.pem of trusted private certification authorities
  # Example command: `kubectl create secret generic private-root-ca --from-file=cert.pem=./private-root-ca.pem`
  # privateCaCerts:
  # - private-root-ca

  # For development or proof-of-concept, you can use an in-cluster database
  # postgresqlEnabled: true is NOT supported in production.
  postgresqlEnabled: false

  ssl:
    # if doing a proof-of-concept with in-cluster-db, this must be set to false
    enabled: true
  dagOnlyDeployment:
    enabled: true
#################################
### Nginx configuration
#################################
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: ~
  #  set privateLoadbalancer to 'false' to make nginx request a LoadBalancer on a public vnet
  privateLoadBalancer: true
  # Dict of arbitrary annotations to add to the nginx ingress. For full configuration options, see https://docs.nginx.com/nginx-ingress-controller/configuration/ingress-resources/advanced-configuration-with-annotations/
  ingressAnnotations: {service.beta.kubernetes.io/aws-load-balancer-type: nlb} # Change to 'elb' if your node group is private and doesn't utilize a NAT gateway
  # If all subnets are private, auto-discovery may fail.
  # You must enter the subnet IDs manually in the annotation below. 
  # service.beta.kubernetes.io/aws-load-balancer-subnets: subnet-id-1,subnet-id-2
astronomer:
  houston:
    config:
      publicSignups: false # Users need to be invited to have access to Astronomer. Set to true otherwise
      emailConfirmation: true # Users get an email verification before accessing Astronomer
      upgradeDeployments:
        enabled: false # dont automatically upgrade airflow instances when the platform is upgraded
      deployments:
        hardDeleteDeployment: true # Allow deletions to immediately remove the database and namespace
        manualReleaseNames: true # Allows you to set your release names
        serviceAccountAnnotationKey: eks.amazonaws.com/role-arn # Flag to enable using IAM roles (don't enter a specific role)
        configureDagDeployment: true # Required for dag-only deploys
        enableUpdateDeploymentImageEndpoint: true # Enables apis for deploying images
        upsertDeploymentEnabled: true # Enables additional apis for updating deployments
      email:
        enabled: true
        reply: "noreply@my.email.internal" # Emails will be sent from this address
      auth:
        github:
          enabled: true # Lets users authenticate with Github
        local:
          enabled: false # Disables logging in with just a username and password
        openidConnect:
          google:
            enabled: true # Lets users authenticate with Google
    secret:
    - envName: "EMAIL__SMTP_URL"  # Reference to the Kubernetes secret for SMTP credentials. Can be removed if email is not used.
      secretName: "astronomer-smtp"
      secretKey: "connection"
```


</TabItem>

<TabItem value="gcp">

```yaml
#################################
### Astronomer global configuration for GKE
#################################
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: sandbox-astro.example.com

  # Name of secret containing TLS certificate
  tlsSecret: astronomer-tls

  # List of secrets containing the cert.pem of trusted private certification authorities
  # Example command: `kubectl create secret generic private-root-ca --from-file=cert.pem=./private-root-ca.pem`
  # privateCaCerts:
  # - private-root-ca

  # For development or proof-of-concept, you can use an in-cluster database
  # postgresqlEnabled: true is NOT supported in production.
  postgresqlEnabled: false

  ssl:
    # if doing a proof-of-concept with in-cluster-db, this must be set to false
    enabled: true
  dagOnlyDeployment:
    enabled: true
#################################
### Nginx configuration
#################################
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: ~
  #  set privateLoadbalancer to 'false' to make nginx request a LoadBalancer on a public vnet
  privateLoadBalancer: true
  # Dict of arbitrary annotations to add to the nginx ingress. For full configuration options, see https://docs.nginx.com/nginx-ingress-controller/configuration/ingress-resources/advanced-configuration-with-annotations/
  ingressAnnotations: {}

astronomer:
  houston:
    config:
      publicSignups: false # Users need to be invited to have access to Astronomer. Set to true otherwise
      emailConfirmation: true # Users get an email verification before accessing Astronomer
      upgradeDeployments:
        enabled: false # dont automatically upgrade airflow instances when the platform is upgraded
      deployments:
        hardDeleteDeployment: true # Allow deletions to immediately remove the database and namespace
        manualReleaseNames: true # Allows you to set your release names
        serviceAccountAnnotationKey: iam.gke.io/gcp-service-account  # Flag to enable using IAM roles (don't enter a specific role)
        configureDagDeployment: true # Required for dag-only deploys
        enableUpdateDeploymentImageEndpoint: true # Enables apis for deploying images
        upsertDeploymentEnabled: true # Enables additional apis for updating deployments
      email:
        enabled: true
        reply: "noreply@my.email.internal" # Emails will be sent from this address
      auth:
        github:
          enabled: true # Lets users authenticate with Github
        local:
          enabled: false # Disables logging in with just a username and password
        openidConnect:
          google:
            enabled: true # Lets users authenticate with Google
    secret:
    - envName: "EMAIL__SMTP_URL"  # Reference to the Kubernetes secret for SMTP credentials. Can be removed if email is not used.
      secretName: "astronomer-smtp"
      secretKey: "connection"

```

</TabItem>

<TabItem value="azure">

```yaml
#################################
### Astronomer global configuration for AKS
#################################
global:
  # Enables default values for Azure installations
  azure:
    enabled: true


  # Base domain for all subdomains exposed through ingress
  baseDomain: sandbox-astro.example.com

  # Name of secret containing TLS certificate
  tlsSecret: astronomer-tls

  # List of secrets containing the cert.pem of trusted private certification authorities
  # Example command: `kubectl create secret generic private-root-ca --from-file=cert.pem=./private-root-ca.pem`
  # privateCaCerts:
  # - private-root-ca

  # For development or proof-of-concept, you can use an in-cluster database
  # postgresqlEnabled: true is NOT supported in production.
  postgresqlEnabled: false

  ssl:
    # if doing a proof-of-concept with in-cluster-db, this must be set to false
    enabled: true
    mode: "prefer"
  dagOnlyDeployment:
    enabled: true
#################################
### Nginx configuration
#################################
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: ~
  #  set privateLoadbalancer to 'false' to make nginx request a LoadBalancer on a public vnet
  privateLoadBalancer: true
  # Dict of arbitrary annotations to add to the nginx ingress. For full configuration options, see https://docs.nginx.com/nginx-ingress-controller/configuration/ingress-resources/advanced-configuration-with-annotations/
  ingressAnnotations:
    # required for azure load balancer post Kubernetes 1.24
    service.beta.kubernetes.io/azure-load-balancer-health-probe-request-path: "/healthz"

astronomer:
  houston:
    config:
      publicSignups: false # Users need to be invited to have access to Astronomer. Set to true otherwise
      emailConfirmation: true # Users get an email verification before accessing Astronomer
      upgradeDeployments:
        enabled: false # dont automatically upgrade airflow instances when the platform is upgraded
      deployments:
        hardDeleteDeployment: true # Allow deletions to immediately remove the database and namespace
        manualReleaseNames: true # Allows you to set your release names
        configureDagDeployment: true # Required for dag-only deploys
        enableUpdateDeploymentImageEndpoint: true # Enables apis for deploying images
        upsertDeploymentEnabled: true # Enables additional apis for updating deployments
      email:
        enabled: true
        reply: "noreply@my.email.internal" # Emails will be sent from this address
      auth:
        github:
          enabled: true # Lets users authenticate with Github
        local:
          enabled: false # Disables logging in with just a username and password
        openidConnect:
          google:
            enabled: true # Lets users authenticate with Google
    secret:
    - envName: "EMAIL__SMTP_URL"  # Reference to the Kubernetes secret for SMTP credentials. Can be removed if email is not used.
      secretName: "astronomer-smtp"
      secretKey: "connection"
```

</TabItem>

<TabItem value="other">

```yaml
#################################
### Astronomer global configuration
#################################
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: sandbox-astro.example.com

  # Name of secret containing TLS certificate
  tlsSecret: astronomer-tls

  # List of secrets containing the cert.pem of trusted private certification authorities
  # Example command: `kubectl create secret generic private-root-ca --from-file=cert.pem=./private-root-ca.pem`
  # privateCaCerts:
  # - private-root-ca

  # For development or proof-of-concept, you can use an in-cluster database
  # postgresqlEnabled: true is NOT supported in production.
  postgresqlEnabled: false

  ssl:
    # if doing a proof-of-concept with in-cluster-db, this must be set to false
    enabled: true
  dagOnlyDeployment:
    enabled: true
#################################
### Nginx configuration
#################################
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: ~
  # Dict of arbitrary annotations to add to the nginx ingress. For full configuration options, see https://docs.nginx.com/nginx-ingress-controller/configuration/ingress-resources/advanced-configuration-with-annotations/
  ingressAnnotations: {}

astronomer:
  houston:
    config:
      publicSignups: false # Users need to be invited to have access to Astronomer. Set to true otherwise
      emailConfirmation: true # Users get an email verification before accessing Astronomer
      deployments:
        hardDeleteDeployment: true # Allow deletions to immediately remove the database and namespace
        manualReleaseNames: true # Allows you to set your release names
        configureDagDeployment: true # Required for dag-only deploys
        enableUpdateDeploymentImageEndpoint: true # Enables apis for deploying images
        upsertDeploymentEnabled: true # Enables additional apis for updating deployments
      email:
        enabled: true
        reply: "noreply@my.email.internal" # Emails will be sent from this address
      auth:
        github:
          enabled: true # Lets users authenticate with Github
        local:
          enabled: false # Disables logging in with just a username and password
        openidConnect:
          google:
            enabled: true # Lets users authenticate with Google
    secret:
    - envName: "EMAIL__SMTP_URL"  # Reference to the Kubernetes secret for SMTP credentials. Can be removed if email is not used.
      secretName: "astronomer-smtp"
      secretKey: "connection"
```

</TabItem>


</Tabs>

## Step 3: Decide Whether to Use a Third-Party Ingress Controller
Astronomer Software requires an Kubernetes Ingress Controller to function.

Astronomer generally recommends customers use its integrated ingress-controller but supports certain third-party ingress controllers. Ingress controllers, including Astronomer's ingress controllers, typically need elevated permissions to function - particularly the ability to list all namespaces and view the ingresses in those namespaces and the ability to retrieve secrets in those namespaces to locate and use private TLS certificates used to service those ingresses.

Customers in complex regulatory requirements frequently have ingress-controllers that are already internally-approved to hold those permissions. 

Astronomer supports [third-party ingress-controllers](#third-party-ingress-controllers) in certain configurations.

Customers using third-party ingress-controllers will perfrom certain additional steps later in the procedure to disable the integrated ingress-controller and configure Astronomer for use with their pre-existing ingress-controller.

## Step 4: Choose and configure the base domain {#choose-and-configure-the-base-domain}

### Choosing the base domain {#choosing-the-base-domain}
The installation procedure detailed in this guide will create a variety of services that your users will access to manage, monitor, and run Airflow on the platform.

Choose a base-domain (e.g. `astronomer.example.com`, `astro-sandbox.example.com`, `astro-prod.example.internal`) for which:
* you have the ability to create and edit DNS records
* you have the ability to issue TLS-certificates
* the following addresses are available:
  - `app.<base-domain>`
  - `deployments.<base-domain>`
  - `houston.<base-domain>`
  - `grafana.<base-domain>`
  - `kibana.<base-domain>`
  - `install.<base-domain>`
  - `alertmanager.<base-domain>`
  - `prometheus.<base-domain>`
  - `registry.<base-domain>`

The base-domain itself does not need to be available and may even point to another service not associated with Astronomer or Airflow. If available, later sections of this document will establish a vanity-redirect from `<base-domain>` to `app.<base-domain>`.

When choosing a baseDomain, consider:
* the name you choose must be be resolvable by both your users and Kubernetes itself
* you will need to have or obtain a TLS certificate that is recognized as valid by your users (and if using the Astronomer Software integrated container registry, by Kubernetes itself)
* wildcardcard certificates are only valid one-level deep (e.g. an ingress controller using a certificate of `*.example.com` can provide service for `app.example.com` but not `app.astronomer-dev.example.com`).
* the bottom-level hostnames (e.g. `app`, `registry`, `prometheus`) are fixed and cannot be changed.
* most kubernetes clusters refuse to resolve DNS hostnames with more than 5 segments (seperated by the dot character; e.g. `app.astronomer.sandbox.mygroup.example.com` is 6 segments and might be problematic, so choosing a baseDomain of `astronomer-sandbox.mygroup.example.com` instead of `astronomer.sandbox.mygroup.example.com` would be advisable).
* the base-domain will be visible to end-users
  - when accessing the Astronomer Software UI (e.g. `https://app.sandbox-astro.example.com`)
  - when accessing an Airflow Deployment (e.g. `https://deployments.sandbox-astro.example.com/deployment-release-name/airflow`)
  - when logging into the astro cli (e.g. `astro login sandbox-astro.example.com`)
  
:::tip

OpenShift customers who wish to use OpenShift's integrated ingress controller typically use the hostname of the default OpenShift ingress controller as their base-domain. Doing so results in a slightly-unwieldy user-visible hostname of `app.apps.<OpenShift-domain>` and requires permission to re-configure the route-admission policy for the standard ingress controller to `InterNamespaceAllowed` (covered later in this document). See [Third Party Ingress Controller - Configuration notes for OpenShift](third-party-ingress-controllers#configuration-notes-for-OpenShift) additional infomation and options.

:::

### Configuring the base domain

Locate the `global.baseDomain` key already present in your `values.yaml` file and change it to your base-domain.

e.g.
```yaml
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: sandbox-astro.example.com
```

## Step 5: Create the Astronomer Software platform namespace {#create-the-astronomer-software-platform-namespace}

In your Kubernetes cluster, create a [kubernetes namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) (Astronomer generally recommends this namespace be named `astronomer`) to contain the Astronomer Software platform.

```sh
kubectl create namespace astronomer
```

The contents of this namespace will be used to provision and manage Airflow instances running in other namespaces. Each Airflow will have its own isolated namespace.



## Step 6: Third-Party Ingress-Controller DNS Configuration {#third-party-ingress-controller-dns-configuration}

Skip this step if using Astronomer Software's integrated ingress-controller as equivalent procedures are performed [later in this procedure](#intigrated-ingress-controller-dns-configuration).

Follow the instructions in this section to create DNS entries pointing to the third-party ingress-controller instance that will provide ingress service to Astronomer Software.

:::info

Third-party ingress-controllers are configured [later in this procedure](#configuring-a-third-party-ingress-controller).

:::

### Astronomer Software Third-Party DNS Requirements and Record Guidance {#third-party-dns-guidance}

Astronomer Software requires the following domain-names be registered and resolvable within the Kubernetes Cluster and to users of Astronomer And Airflow.
  - `<base-domain>` (optional but recommended, provides a vanity re-direct to `app.<base-domain>`)
  - `app.<base-domain>` (required)
  - `deployments.<base-domain>` (required)
  - `houston.<base-domain>` (required)
  - `grafana.<base-domain>` (required if using Astronomer Software's integrated grafana)
  - `kibana.<base-domain>` (required if not using external elasticsearch)
  - `install.<base-domain>` (optional)
  - `alertmanager.<base-domain>` (required if using Astronomer Software's integrated Alert Manager)
  - `prometheus.<base-domain>` (required)
  - `registry.<base-domain>` (required if using Astronomer Software's integrated container-registry)

Astronomer generally recommends that:
* the `<base-domain>` record be a zone-apex record (typically expressed by using a hostname of `@`) pointing to the IP(s) of the ingress-controller
* all other records be CNAME records pointing to the `<base-domain>`

For platform administrators unable to register the base-domain, Astronomer recommends that:
* the `app.<baseDomain>` record be an A record pointing to the IP(s) of the ingress-controller
* all other records be CNAME records pointing to `app.<base-domain>`

:::tip

For lower environments, Astronomer recommends a relatively short ttl-value (e.g. 60 seconds) when you first deploy Astronomer so that any errors can be quickly corrected.

:::


### Request Ingress Information from your Ingress-Administrator {#get-ingress-info}

Provide your Ingress Controller Administrator with the [Astronomer Software Third-Party DNS Requirements and Record Guidance](#third-party-dns-guidance) above (replacing`<base-domain>` with the base-domain from [Choosing the Base Domain](#choosing-the-base-domain)) and guidance and request the following information:
* what ingress class name you should use (or whether you should leave blank and use the default)
* what IP address(es) you should use for DNS entries pointing to the ingress controller
* whether DNS-records will be automatically created in reponse to Ingress rources that we will be created later in the install
* if DNS-records need to be manually created, and if so who will coordinate their creation and who will create them
### Create DNS records pointing to your third-party ingress-controller

Create DNS records pointed to your third-party ingress-controller.

### Verify DNS records are pointed to your third-party ingress-controller

Use `dig <hostname>` or `getent hosts <hostname>` to verify each DNS entry is created and pointing to the IP address of the ingress-controller you will be using.

## Step 7: Requesting and Validating an Astronomer TLS Certificate {#requesting-and-validating-an-astronomer-tls-certificate}

In order to install Astronomer Software, you'll need a TLS certificate that is valid for several domains - one of which will be the primary name on the certificate (referred to as the Common name or CN) and the rest will be equally-valid supplementary domains known as Subject Alternative Names (SAN)s.

Astronomer requires a private certificate be present in the Astronomer Platform namespace, even if using a third-party ingress-controller that doesn't otherwise require it.

### Requesting an Ingress-Controller TLS Certificate {#request-a-certificate-bundle}

Request a TLS certificate and associated items (see below) from your enterprise security team.

When requesting a certificate for Astronomer Software, use the [base domain you chose earlier](#choosing-the-base-domain) as the Common Name (CN). If your Certificate Authority will not issue certificates for the bare base domain, use `app.<base-domain>` as the Common Name instead.

Additionally, you must include *either* a wildcard Subject Alternative Name (SAN) entry of `*.<base-domain>` *or* an explicit SAN entry for each of the following items:

```sh
app.<base-domain> (omit if already used as the Common Name)
deployments.<base-domain>
registry.<base-domain>
houston.<base-domain>
grafana.<base-domain>
kibana.<base-domain>
install.<base-domain>
alertmanager.<base-domain>
prometheus.<base-domain>
```

:::warning

If using the Astronomer Software integrated container registry, the encryption-type used on your TLS certificate must be *RSA*. Cerbot users must include `-key-type rsa` when requesting certificates, most other solutions generate RSA-keys by default. If using the registry, we will confirm the received certificate encryption type [in later steps](#docker-registry-cert-encryption-restrictions).

:::

In your request to your Security Team, include:
* the Common Name and Subject Alternative Name(s) as per above
* if using the Astronomer Software integrated container registry, the requirement that the encryption type of the certificate *must* be RSA
* request that the return format be as follows:
  - a key.pem - containing the private key in pem format
  - **either** a full-chain.pem (containing the public certificate additional certificates required to validate it, in pem format) **or** a bare `cert.pem` and explicit affirmation that there are no intermediate certificates and that the public certificate is the full-chain
  - **either** the private-root-ca.pem of the the private Certificate Authority used to create your certificate (in pem format) or a statement that the certificate is signed by public Certificate Authority

### Validating the received certficiate and associated items
Ensure that you have received each of the follownig three items:

* a key.pem - containing the private key in pem format
* **either** a full-chain.pem (containing the public certificate additional certificates required to validate it, in pem format) **or** a bare `cert.pem` and explicit affirmation that there are no intermediate 
* **either** the private-root-ca.pem of the the private Certificate Authority used to create your certificate (in pem format) or a statement that the certificate is signed by public Certificate Authority

Validate that your enterprise security team generated the correct certificate, run the following command using the `openssl` CLI:

```sh
openssl x509 -in  <your-certificate-filepath> -text -noout
```

This command will generate a report. If the `X509v3 Subject Alternative Name` section of this report includes either a single `*.<base-domain>` wildcard domain or all subdomains, then the certificate creation was successful.

Confirm that your full-chain certificate chain is ordered correctly. To determine your certificate chain order, run the following command using the `openssl` CLI:

```sh
openssl crl2pkcs7 -nocrl -certfile <your-full-chain-certificate-filepath> | openssl pkcs7 -print_certs -noout
```

The command generates a report of all certificates. Verify the order of the certificates is as follows:

- Domain
- Intermediate (optional)
- Root

### Additional Validation for the Astronomer Integrated Container Registry{#docker-registry-cert-encryption-restrictions}
If you will not be storing images in Astronomer's integrated container registry and will instead be storing all container images an [external container registry](#configure-a-private-docker-registry-airflow)) skip this sub-step.

The Astronomer Software integrated container-registry requires the key used to sign traffic originating from the Astronomer Software platform do so using the RSA encryption method.

Follow the following procedure to identify the encryption type associated with the certificate you were provided from your certificate authority.

Extract the bare public cert (if it was not already included in the files provided by your certificate-authority) from the full-chain certificate file.

e.g.
```sh
openssl crl2pkcs7 -nocrl -certfile full-chain.pem | openssl pkcs7 -print_certs -noout > cert.pem`
```

Examine the public certificate and ensure all Signature Alogithm's are listed as `sha1WithRSAEncryption`.

```sh
openssl x509 -in cert.pem -text|grep Algorithm 
        Signature Algorithm: sha1WithRSAEncryption
            Public Key Algorithm: rsaEncryption
    Signature Algorithm: sha1WithRSAEncryption
```

If your key is not compatible with the Astronomer Software integrated container registry, request your Certificate Authority [re-issue the credentials](#request-a-certificate-bundle) (re-emphasizing the need for an RSA cert) or [use an external container registry](#configure-a-private-docker-registry-airflow).


## Step 8: Storing and configuring the Ingress Controller Public TLS Full-Chain Certificate {#storing-and-configuring-the-public-tls-full-chain-certificate}

### Storing the full-chain TLS certificate in the Astronomre Platform Namespace
Store the public full-chain certificate in the Astronomer Software Platform Namespace in a `tls`-type Kubernetes secret named `astronomer-tls` using the following command.

If your enterprise-security organization has instructed you that there are no intermediate certifi

```sh
kubectl -n <astronomer platform namespace> create secret tls astronomer-tls --cert <fullchain-pem-filepath> --key <your-private-key-filepath>
```

E.g.
```sh
kubectl -n astronomer create secret tls astronomer-tls --cert full-chain.pem --key server_private_key.pem
```

Naming the secret `astronomer-tls` (no substitutions) is always recommended and is a strict requirement when using a third-party ingress-controller.

## Step 9: Configuring a third-party ingress-controller {#configuring-a-third-party-ingress-controller}

If using Astronomer Software's integrated ingress controller, skip this step.

Follow procedures at [Third-party Ingress-Controllers](#third-party-ingress-controllers), which includes steps to:
* perform the standard configuration required to a third-party ingress-controller
* perform any environment-specific configured required for ingress controllers in certain environments (like OpenShift)
* perform any additional controller-specific required configuration (required for most ingress-controllers)

## Step 10: Configuring a Private Certificate Authority {#configuring-a-private-certificate-authority}

If you received a private certificate for the ingress controller, follow the instructions at [configuring private CAs](#extra-private-cas) to store the Certificate Authority's public root certificate used to create it in a Kubernetes seccret in the astronomer platform namespace and configure Astronomer Software platform components to trust it.

Additionally, repeat the above procedure to configure Astronomer Software platform components to [trust the private CAs](#configuring-private-cas) for each service not already present in `global.privateCaCerts`.
* email server (unless disabled)
* any container registries that Kubernetes will pull from
* if using OAUTH, the OAUTH provider
* if using external elasticsearch, any external elasticsearch instances
* if using external prometheus, any external prometheus instances

Configure Astronomer Software platform components to [trust the private CAs](#configuring-private-cas) for each service not already present in `global.privateCaCerts`.

## Step 11: Ensure your Kubernetes Cluster Trusts Required Certificate Authorities{#private-cas-for-kubernetes}
Kubernetes must be able to pull images from one or more container registries for Astronomer Software to function.

By default, Kubernetes **only** trusts publicly signed certificates.

You may need to add additional trusted certificate-authorities to your Kubernetes Cluster's store of trusted certificates when:
* you have configured Astronomer software to pull platform [platform container images](#use-a-custom-image-repository-for-platform-images) from an external container registry that uses a certificate signed by a private certificate-authority
* users will be deploying airflow images to Astronomer Software's integrated container registry **and** Astronomer is using a TLS certificate issued by a private Certificate Authority 
* users will be deploying images to an external container registry **and** that registry is using a TLS certificate issued by a private Certificate Authority 

If none of the above situations apply, skip this step.

Kubernetes does not honor the list of certificates [trusted by the Astronomer Software platform](#configuring-a-private-certificate-authority).

Many enterprises configure Kubernetes to trust additional certificate-authorities as part of their standard cluter-creation procedure.

Contact your Kubernetes Administrator to find out what, if any, private certificaties are currently trusted by your Kubernetes Cluster.

Consult your Kubernetes administrator and Kubernetes-provider's documentation for instructions on configuring Kubernetes trust additional Certificate Authorities.

Follow procedures for your Kubernetes provider to configure Kubernetes to trust each certificate authority associated with container registries (including the integrated container registry, if applicable) that Kubernetes will be pulling images from.

Certain clusters do not provide a mechanism to configure the list of certificates trusted by Kubernetes.

While configuring Kubernetes list of cluster-certificates is a custeomer-responsibility, Astronomer Software includes an optional component that can, for certiain Kubernetes Cluster configurations, add certificates defined in `astronomer.privateCaCerts` to the list of certificates trusted by Kubernetes. This can be enabled by setting `astronomer.privateCaCertsAddToHost.enabled` and ``astronomer.privateCaCertsAddToHost.addToContainerd` to `true`. E.g.

```yaml
  astronomer:
    privateCaCertsAddToHost:
      enabled: true
      addToContainerd: true
      hostDirectory: /etc/containerd/certs.d
```

The above configuration is valid for most Kubernetes Clusters, including EKS and AKS.

GKE users must additionally add a `containerdConfigToml` containing a pair of lines for each registry hostname (and the associated secret name) in the following format:
```
  astronomer:
    privateCaCertsAddToHost:
      enabled: true
      addToContainerd: true
      hostDirectory: /etc/containerd/certs.d
      containerdConfigToml: |-
        [host."https://<registry hostname>"]
          ca = "/etc/containerd/certs.d/<registry hostname>/<secret name>.pem"
```

## Step 12: Configure Outbound SMTP Email {#configure-outbound-smtp-email}


Astronomer Software requires the ability to send email to:
* notifying users of certain errors (e.g. users that try to deploy mis-matched Airflow image versions)
* sending and accepting email invites from Astronomer
* sending certain platform alerts (in the default configuration, configurable)

Astronomer Software sends all outbound email via SMTP.

:::info

If evaluating Astronomer Software in an environment where outbound SMTP is not available, follow instructions in `Appendix: Configuring Astronomer Software To Not Send Outbound Email` and then skip the rest of this section.

:::

1. Obtain a valid set of SMTP credentials.
2. Ensure that the Kubetes Cluster has access to send outbound email to the SMTP server.
3. Change the reply values already present in `values.yaml` from `noreply@my.email.internal` to an email address that is valid for use with the SMTP credentials.
4. Construct an email connection string (see guidance later in this section) and store it in a secret named `astronomer-tls` in the astronomer platform namespace. Make sure to *url-encode* the username and password if they contain special characters.
  e.g.
  ```sh
  kubectl -n astronomer create secret generic astronomer-smtp --from-literal connection="smtp://my@40user:my%40pass@smtp.email.internal/?requireTLS=true"
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

## Step 13: Configure volume storage classes
Astronomer strongly recommends against backing any volumes used for Astronomer Software with mechanical hard-drives.

If your cluster defines a volume-storage class, and you wish to use it for all volumes associated with Astronomer Software and the Airlfow deployments it you may skip this step.

Replace `<desired-storage-class>` in the following configuration data with the storage class you wish to use for each respective component (removing any entries where you wish to use the default) and merge into `values.yaml` - either manually or by placing [merge_yaml.py](#merge_yaml) in your astro-platform project-directory and running `python merge_yaml.py storage-class-config.yaml values.yaml`.

```yaml
alertmanager:
  persistence:
    storageClassName: "<desired-storage-class>"
stan:
  store:
    volume:
      storageClass: "<desired-storage-class>"
prometheus:
  persistence:
    storageClassName: "<desired-storage-class>"
elasticsearch:
  common:
    persistence:
      storageClassName: "<desired-storage-class>"
astronomer:
  registry:
    persistence:
      storageClassName: "<desired-storage-class>"
  houston:
    config:
      deployments:
        helm:
          dagDeploy:
            persistence:
              storageClass: "<desired-storage-class>"
          airflow:
            redis:
              persistence:
                storageClassName: "<desired-storage-class>"
# this option does not apply when using an external postgres database
# bundled postgresql not a supported option, only for use in proof-of-concepts
postgresql:
  persistence:
    storageClass: "<desired-storage-class>"

```


## Step 14: Configure the database {#configure-the-database}

## Create a database instance

Astronomer requires a central Postgres database that acts as the backend for Astronomer's Houston API and will host individual metadata databases for all Airflow Deployments spun up on the platform.

:::info

If, while evaluating Astronomer Software, you need to create a temporary environment where Postgres is not available, locate the `global.postgresqlEnabled` option already present in your `values.yaml` and set it to `true` then skip the remainder of this step.

Setting `global.postgresqlEnabled` to `true` is an **unsupported** configuration and **must not** be used on any development, staging, or production environment.

:::


:::info

If using Azure Database for PostgreSQL or another Postgres instance that does not enable the `pg_trgm` by default, you **must** enable the `pg_trgm` extension prior to installing Astronomer Software. If `pg_trgm` is not enabled, the install will fail. `pg_tgrm` is enabled by default on Amazon RDS and Google Cooud SQL for PostgresQL. For instructions on enabling the `pg_trgm` extension for Azure Flexible Server, see [PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions).

:::

Additional requirements apply to the following databases:
- AWS RDS:
  * [t2 medium](https://aws.amazon.com/rds/instance-types/) is the minimum RDS instance size.
- Azure Flexible Server:
  * you must enable the `pg_trgm` extension as per the advisory earlier in this section
  * Set `global.ssl.mode`to `prefer` in your `values.yaml`


Create a Kubernetes Secret named `astronomer-bootstrap` that points to your database. You must URL encode any special characters in your Postgres password.

To create this secret, run the following command replacing the astronomer platform namespace, username, password, database hostname, and database port with their respective values (username and password must be url-encoded if they contain special-characters):

```sh
kubectl --namespace <astronomer platform namespace> create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://<url-encoded username>:<url-encoded password>@<database hostname>:<database port>"
```

e.g. For a username named `bob` with password `abc@abc` at hostname `some.host.internal`:
```sh
kubectl --namespace astronomer create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://bob:abc%40abc@some.host.internal:5432"
```


## Step 15: Configure an external docker registry for user-provided Airflow images {#configure-a-private-docker-registry-airflow}
Astronomer Software users create customized Airflow container images. These images frequently contain sensitive information and **must** be stored in a secure location accessible to Kubernetes.

Astronomer software deploys an integrated image-registry that can be used for this purpose.

Users may use images hosted in other container image repositories accessible to the Kubernetes cluster without additional platform-level configuration.

See [Configure a custom registry for Deployment images](#custom-image-registry) for additional configurable options.

## Step 16: Configure the docker registry used for platform images {#configure-a-private-docker-registry-platform}

If you are installing Astronomer Software onto a Kubernetes Cluster that can pull container images from public image repositories and you do not wish to mirror these images locally skip this step.

### Configure values.yaml to to use a custom image repository for platform images {#use-a-custom-image-repository-for-platform-images}

Astronomer expects the images to be present using their normal names but prefixed by a string you define. E.g. if you specify `artifactory.example.com/astronomer`, when you mirror images later in this procedure, you would mirror:
* `quay.io/astronomer/ap-houston-api` to `artifactory.example.com/astronomer/ap-houston-api`
* `quay.io/astronomer/astronomer/ap-commander` to `artifactory.example.com/astronomer/ap-commander`
* etc.

Replace `<custom-platform-repo-prefix>` in the following configuration data with your platform image repository prefix and merge into `values.yaml` - either manually or by placing [merge_yaml.py](#merge_yaml) in your astro-platform project-directory and running `python merge_yaml.py private-platform-registry-snippet.yaml values.yaml`.

```yaml
global:
  privateRegistry:
    enabled: true
    repository: <custom-platform-repo-prefix>
astronomer:
  houston:
    config:
      deployments:
        helm:
          runtimeImages:
            airflow:
              repository: <custom-platform-repo-prefix>/astro-runtime
            flower:
              repository: <custom-platform-repo-prefix>/astro-runtime
          airflow:
            defaultAirflowRepository: <custom-platform-repo-prefix>/ap-airflow
            defaultRuntimeRepository: <custom-platform-repo-prefix>/astro-runtime
            images:
              airflow:
                repository: <custom-platform-repo-prefix>/ap-airflow
              statsd:
                repository: <custom-platform-repo-prefix>/ap-statsd-exporter
              redis:
                repository: <custom-platform-repo-prefix>/ap-redis
              pgbouncer:
                repository: <custom-platform-repo-prefix>/ap-pgbouncer
              pgbouncerExporter:
                repository: <custom-platform-repo-prefix>/ap-pgbouncer-exporter
              gitSync:
                repository: <custom-platform-repo-prefix>/ap-git-sync

```

e.g. for a custom platform image repository prefix of `012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer`:

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

### Configuration authenticating to the platform registry
Astronomer Software platform images are requently hosted internal repositories that do not require configuration. If your repostory requires you pass an image credential:

1. Log in to the registry and follow the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#log-in-to-docker-hub) to produce a `/.docker/config.json` file.
2. Run the following command to create an image pull secret named `platform-regcred` in the Astronomer Software platform namespace:

    ```sh
    kubectl -n <astronomer platform namespace> create secret generic platform-regcred \
    --from-file=.dockerconfigjson=<path/to/.docker/config.json> \
    --type=kubernetes.io/dockerconfigjson
    ```
3. Set `global.privateRegistry.secretName` in `values.yaml` to `platform-regcred`, e.g.:

    ```yaml
    global:
      privateRegistry:
        secretName: platform-regcred
    ```


## Step 17: Determine what version of Astronomer Software to install {#determine-what-version-of-astronomer-software-to-install}

Astronomer recommends new Astronomer Software installations use the most-recently version of either the Stable or LTS (long-term support) release-channel.

Current recommended versions:
  * Stable Channel: v0.34.1 (0.34 is supported until August 2025)
  * Long-term Support Channel: v0.34.1 (0.34 is supported until August 2025)

See Astronomer Software's [lifecycle policy](release-lifecycle-policy) and [release notes](version-compatibility-reference) for more information.


## Step 18: Fetch Airflow Helm charts {#fetch-airflow-helm-charts}

* If you have internet accces to `https://helm.astronomer.io` run the following command on the machine you will be installing Astronomer Software on:
```sh
helm repo add astronomer https://helm.astronomer.io/
helm repo update
```
* If you do not have internet access to `https://helm.astronomer.io` download the Astronomer Software Platform helm chart file corresponding to the version of Astronomer Software they are installing or upgrading to from `https://helm.astronomer.io/astronomer-<version number>.tgz`. 
  * e.g. if installing Astronomer Software v0.34.1 download `https://helm.astronomer.io/astronomer-0.34.1.tgz`.
  * This file does not need to uploaded to an internal chart-repository.


## Step 19: Create and customize upgrade.sh {#create-and-customize-upgradesh}

Create a file named `upgrade.sh` in your [platform-deployment project-directory](#platform-deployment-project-directory) containing the script below, then customize:
* CHART_VERSION - v-prefixed version of the Astronomer Software version, including patch (e.g. v0.34.1)
* RELEASE_NAME - helm release name, strongly recommended `astronomer`
* NAMESPACE - namespace name to install platform components into, strongly recommend `astronomer`
* CHART_NAME - set to `astronomer/astronomer` if fetching from the internet or the filename if installing from a file (e.g. `astronomer-0.34.1.tgz`)

```sh
#!/bin/bash
set -xe

# typically astronomer
RELEASE_NAME=<astronomer-platform-release-name>
# typically astronomer
NAMESPACE=<astronomer-platform-namespace>
# typically astronomer/astronomer
CHART_NAME=<chart name>
# format is v<major>.<minor>.<path> e.g. v0.32.9
CHART_VERSION=<v-prefixed version of the Astronomer Software platform chart>
# ensure all the above environment variables have been set

helm repo add --force-update astronomer https://helm.astronomer.io
helm repo update

# upgradeDeployments false ensures that Airflow charts are not upgraded when this script is ran
# If you deployed a config change that is intended to reconfigure something inside Airflow,
# then you may set this value to "true" instead. When it is "true", then each Airflow chart will
# restart. Note that some stable version upgrades require setting this value to true regardless of your own configuration.
# If you are currently on Astronomer Software 0.25, 0.26, or 0.27, you must upgrade to version 0.28 before upgrading to 0.29. A direct upgrade to 0.29 from a version lower than 0.28 is not possible.
helm upgrade --install --namespace $NAMESPACE \
            -f ./values.yaml \
            --reset-values \
            --version $CHART_VERSION \
            --debug \
            --set astronomer.houston.upgradeDeployments.enabled=false \
            $RELEASE_NAME \
            $CHART_NAME $@
```
## Step 20: Fetch images from Astronomer's Helm template {#fetch-images-from-astronomer's-helm-template}

The images and tags which are required for your Software installation depend on the version of Astronomer you're installing. To gather a list of exact images and tags required for your Astronomer version:

1. Configure your current session by setting:
  * CHART_VERSION - v-prefixed version of the Astronomer Software platform chart, including patch (e.g. v0.34.1)
  * CHART_NAME - set to `astronomer/astronomer` if fetching from the internet or the filename if installing from a file (e.g. `astronomer-0.34.1.tgz`)

    ```bash
    CHART_VERSION=<v-prefixed version of the Astronomer Software platform chart>        
    CHART_NAME=<chart name>
    ```
2. Run the following command to template the Astronomer Helm chart and fetch all of its rendered image tags.
    ```bash
    helm template --version $CHART_VERSION $CHART_NAME --set global.dagOnlyDeployment.enabled=True --set global.loggingSidecar.enabled=True --set global.postgresqlEnabled=True --set global.authSidecar.enabled=True --set global.baseDomain=ignored | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq                           
    ```
    
    This command sets all possible Helm values that could impact which images are required for your installation. By fetching all images now, you save time by eliminating the risk of missing an image. 
3. Run the following command to template the Airflow Helm chart and fetch its rendered image tags:

    ```sh
    helm template --version $CHART_VERSION $CHART_NAME --set airflow.postgresql.enabled=false --set airflow.pgbouncer.enabled=true --set airflow.statsd.enabled=true --set airflow.executor=CeleryExecutor | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq
    ```

The above commands generate a list of images required for your version of Astronomer. 

Copy these images to the container registry using the naming scheme [configured in prior steps](#use-a-custom-image-repository-for-platform-images).

:::tip

You can pass `-f/--values values.yaml` to `helm template` to only show images that apply to your specific configuration.

:::



## Step 21: Fetch Airflow updates {#fetch-airflow-updates}

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

    ```sh
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

## Step 22: Configure namespace pools {#configure-namespace-pools}

Dedicated namespace pools are strongly recommended for the security of any Astronomer Software installation. They allow you to grant Astronomer Software permissions at the namespace level and limit cluster-level permission.

# Step 99: Determine whether to use the Astronomer Software integrated ingress-controller
Astronomer Software 

If using Astronomer Software's integrated ingress controller, skip this step.

Follow procedures at [Third-party Ingress-Controllers](#third-party-ingress-controllers), which includes steps to:
* perform the standard configuration required to a third-party ingress-controller
* perform any environment-specific configured required for ingress controllers in certain environments (like OpenShift)
* perform any additional controller-specific required configuration (required for most ingress-controllers)

See [Configure a Kubernetes namespace pool for Astronomer Software](namespace-pools.md) to learn how to configure pre-created namespaces in your `values.yaml` file. When you decide on a namespace pool implementation, apply the required changes to your cluster and `values.yaml` file. 

Do not apply the configuration to your cluster yet as described in the linked documentation - you'll be applying your complete platform configuration all at once later in this setup.

Most third-party ingress-controllers require the public certificate additionally be available in the namespace of the various airflow instances. If using a third-party ingress-controller, run the following command to mark the secret for automatic-replication into astronomer-managed Airflow namespaces, substituting both instances of `<astronomer platform namespace>` with the name of the Astronomer Software platform namespace:

Do not apply the configuration to your cluster yet as described in the linked documentation - you'll be applying your complete platform configuration all at once later in this setup.

## Step 23: Configure sidecar logging {#configure-sidecar-logging}

Running a logging sidecar to export Airflow task logs is essential for running Astronomer Software in a multi-tenant cluster. See [Export logs using container sidecars](export-task-logs.md#export-logs-using-container-sidecars) to learn how to configure logging sidecars in your `values.yaml` file. 

Do not apply the configuration to your cluster yet as described in the linked documentation - you'll be applying your complete platform configuration all at once later in this setup.


## Step 24: Integrate an external identity provider {#integrate-an-external-identity-provider}

Astronomer Software includes integrations for several of the most popular identity providers (IdPs), such as Okta and Microsoft Entra ID. Configuring an external IdP allows you to automatically provision and manage users in accordance with your organization's security requirements. See [Integrate an auth system](integrate-auth-system.md) to configure the identity provider of your choice in your `config.yaml` file. 

Do not apply the configuration to your cluster yet as described in the linked documentation - you'll be applying your complete platform configuration all at once later in this setup.

## Step 25: OpenShift Configuration {#OpenShift-configuration}
Merge the following configuration options into `values.yaml` - either manually or by placing [merge_yaml.py](#merge_yaml) in your astro-platform project-directory and running `python merge_yaml.py OpenShift-snippet.yaml values.yaml`.

```yaml
astronomer:
  authSidecar:
    enabled: true
  dagOnlyDeployment:
    securityContext:
      fsGroup: ""
  fluentdEnabled: false
  loggingSidecar:
    enabled: true
    name: sidecar-log-consumer
  sccEnabled: false
elasticsearch:
  securityContext:
    fsGroup: ~
  sysctlInitContainer:
    enabled: false
```


## Step 26: Pre-creating the Load-Balancer {#creating-the-load-balancer}

If using a third-party ingress-controller or provisioning domain-names for ingress objects using external-dns, skip this step.

Astronomer Software platform components require DNS entries be pointing to a load-balancer associated with your ingress-controller to install and function.

Perform a preliminary install of Astronomer Software to trigger the load-balancer creation.

:::info

This installation will fail (as intended) and timeout after 30 seconds but will cause the load balancer to be created.

:::

<Tabs
    defaultValue="script"
    groupId= "load-balancer-creation"
    values={[
        {label: 'upgrade.sh', value: 'script'},
        {label: 'helm', value: 'helm'},
    ]}>

<TabItem value="script">

```bash
./upgrade.sh --timeout 30s
```

</TabItem>
<TabItem value="helm">

* CHART_VERSION - v-prefixed version of the Astronomer Software version, including patch (e.g. v0.34.1)
* RELEASE_NAME - helm release name, strongly recommended `astronomer`
* NAMESPACE - namespace name to install platform components into, strongly recommend `astronomer`
* CHART_NAME - set to `astronomer/astronomer` if fetching from the internet or the filename if installing from a file (e.g. `astronomer-0.34.1.tgz`)

```sh
#!/bin/bash
set -xe

# typically astronomer
RELEASE_NAME=<astronomer-platform-release-name>
# typically astronomer
NAMESPACE=<astronomer-platform-namespace>
# typically astronomer/astronomer
CHART_NAME=<chart name>
# format is v<major>.<minor>.<path> e.g. v0.32.9
CHART_VERSION=<v-prefixed version of the Astronomer Software platform chart>
# ensure all the above environment variables have been set

helm upgrade --install --namespace $NAMESPACE \
            -f ./values.yaml \
            --reset-values \
            --version $CHART_VERSION \
            --debug \
            --set astronomer.houston.upgradeDeployments.enabled=false \
            --timeout 30s \
            $RELEASE_NAME \
            $CHART_NAME $@
```

</TabItem>
</Tabs>

Run `kubectl -n <astronomer platformm namespace> get service -l component=ingress-controller` and verify that a service-type LoadBalancer resource has been created and received an External IP in a range that is accessible to your end-users but **not** accessible to the general internet.

E.g.

```shell
$kubectl -n astronomer get service -l component=ingress-controller
NAME                       TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
astronomer-nginx           LoadBalancer   172.30.239.161   10.42.42.17     80:32697/TCP,443:30727/TCP   39m
astronomer-nginx-metrics   ClusterIP      172.30.245.154   <none>          10254/TCP                    39m
```

If the Astronomer Software platfrom chart is uninstalled and re-installed, the ingress controller will virtually always receive a new IP address (requiring DNS entries to be updated).

In lower environments, you may set `nginx.loadBalancerIP` in `values.yaml` to the External-IP address:

e.g.

```
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: "10.42.42.17"
```

This optional allows the cluster to request same Load Balancer IP at creation-time. Practically, re-builds immediately following tear-downs almost always can receive the same IP address but re-issuance is not guaranteed and installations will fail if the IP address has been assigned elsewhere or is otherwise not available.  As such, this option should not be used in higher environments unless you have taken special measures to guarantee re-issuence.


## Step 27: Configure DNS for the integrated ingress-controller {#intigrated-ingress-controller-dns-configuration}

If using a third-party ingress-controller skip this step - you completed corresponding procedures in a [prior section](#third-party-ingress-controller-dns-configuration)).

The Astronomer load balancer routes incoming traffic to your NGINX ingress controller. After you install Astronomer Software, the load balancer will spin up in your cloud provider account.

Run `$ kubectl get svc -n <astronomer platform namespace>`m e.g. `kubectl get svc -n ingress` to view your load balancer's CNAME, located under the `EXTERNAL-IP` column for the `astronomer-nginx` service. It should look similar to the following:

```sh
$ kubectl get svc -n astronomer
NAME                                 TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)                                      AGE
astronomer-alertmanager              ClusterIP      172.20.48.232    <none>                                                                    9093/TCP                                     24d
[...]
astronomer-nginx                     LoadBalancer   172.20.54.142    ELB_ADDRESS.us-east-1.elb.amazonaws.com                                   80:31925/TCP,443:32461/TCP,10254:32424/TCP   24d
astronomer-nginx-default-backend     ClusterIP      172.20.186.254   <none>                                                                    8080/TCP                                     24d
[...]                         
```

You will need to create a new CNAME record through your DNS provider using the external IP listed for for `astronomer-nginx`.

You can create a single wildcard CNAME record such as `*.sandbox-astro.example.com`, or alternatively create individual CNAME records for the following routes:

Astronomer Software requires the following domain-names be registered and resolvable within the Kubernetes Cluster and to users of Astronomer And Airflow.
  - `<base-domain>` (optional but recommended, provides a vanity re-direct to `app.<base-domain>`)
  - `app.<base-domain>` (required)
  - `deployments.<base-domain>` (required)
  - `houston.<base-domain>` (required)
  - `grafana.<base-domain>` (required if using Astronomer Software's integrated grafana)
  - `kibana.<base-domain>` (required if not using external elasticsearch)
  - `install.<base-domain>` (optional)
  - `alertmanager.<base-domain>` (required if using Astronomer Software's integrated Alert Manager)
  - `prometheus.<base-domain>` (required)
  - `registry.<base-domain>` (required if using Astronomer Software's integrated container-registry)

## Step 28: Install Astronomer using Helm {#install-astronomer-using-helm}

Install the Astronomer Software helm chart using `upgrade.sh` (recommended for your first install) or directly from helm.

<Tabs
    defaultValue="script"
    groupId= "load-balancer-creation"
    values={[
        {label: 'upgrade.sh', value: 'script'},
        {label: 'helm', value: 'helm'},
    ]}>

<TabItem value="script">

```sh
./upgrade.sh --timeout 20m
```

</TabItem>
<TabItem value="helm">

```sh
helm upgrade --install --namespace <astronomer-platform-namespace> \
            -f ./values.yaml \
            --reset-values \
            --version <v-prefixed-astronomer-platform-chart-version> \
            --debug \
            --set astronomer.houston.upgradeDeployments.enabled=false \
            --timeout 20m \
            $RELEASE_NAME \
            $CHART_NAME $@
```

</TabItem>
</Tabs>

## Step 29: Verify Pods are up {#verify-pods-are-up}

To verify all pods are up and running, run:

```sh
kubectl get pods --namespace <astronomer-platform-namespace>
```

All pods should be in Running status. E.g.:

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

If all pods are not in running status, check out our [guide on debugging your installation](debug-install.md).


## Step 30: Verify you can access the Software UI {#verify-you-can-access-the-software-ui}

Visit `https://app.<base-domain>` in your web-browser to view Astronomer Software's web interface.

Consider this your new Airflow control plane. From the Astronomer Software UI, you'll be able to both invite and manage users as well as create and monitor Airflow Deployments on the platform.

## Step 31: Verify TLS is Working {#verify-your-tls-setup}

To check if your TLS certificates were accepted, log in to the Software UI. Then, go to `app.BASEDOMAIN/token` and run:

```sh
curl -v -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"
```

Verify that this output matches with that of the following command, which doesn't look for TLS:

```sh
curl -v -k -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"
```

## Step 32: Verify Your Local Machine Trusts the Container Registry

If not using Astronomer
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

If you missed these steps during installation, follow the steps in [Apply a config change](apply-platform-config.md) to add them after installation. If you are using a base image such as CoreOS that does not permit values to be changed, or you otherwise can't modify `values.yaml`, contact [Astronomer support](https://support.astronomer.io) for additional configuration assistance.



## Configuring Astronomer Software To Not Send Outbound Email

Astronomer Software can be configured to not send outbound email.

:::info

Setting `astronomer.houston.config.publicSignups` to `true` in conjunction with `astronomer.houston.config.email.enabled` to `false` is only secure when all non-OIDC authentication backends are explicitly disabled and the OIDC-provider provides sufficient user-validation to prevent untrusted users from accessing Astronomer Software.

:::

To disable email transmission and email verision of users attempting to access the platform:
1. set `astronomer.houston.config.email.enabled` to `false`
2. set `astronomer.houston.config.publicSignups` to `true`
3. remove the `EMAIL__SMTP_URL` list-item from `astronomer.houston.secret`

If the guide has not yet instructed you to install Astronomer software, skip the remainder of this section.

Apply the configuration update to the Astronomer Software helm release using `upgrade.sh` (recommended for your first install) or directly from helm. 

## Configuring Astronomer Software to trust Private Certificate Authorities (Private CA's) {#configuring-private-cas}

1. Store the Certificate Authority's root public certificate to an [Opaque Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types) in the Astronomer namespace with a descriptive name, e.g. `private-root-ca` by running the following command:

    ```sh
    kubectl -n <astronomer platform namespace> create secret generic <secret name> --from-file=cert.pem=./<your-ca-certificate>
    ```

    e.g.

    ```sh
    kubectl -n astronomer create secret generic private-root-ca --from-file=cert.pem=./private-root-ca.pem
    ```

    > **Note:** The root certificate which you specify here should be the certificate of the authority that signed the Astronomer certificate. This is not the certificate associated with Astronomer or any other service.

    > **Note:** The name of the secret file must be `cert.pem` for your certificate to be trusted properly.

    > **Note:** The file must contain only a single certificate, it may not be a certificate bundle.

2. Add `<secret name>` to the list of secret names contained in `global.privateCaCerts` in `values.yaml`. E.g.
    ```yaml
    astronomer:
      privateCaCerts:
      - private-root-ca
    ```

## Addendum
### merge_yaml.py {#merge-yaml}

```python
#!/usr/bin/env python
"""
Backup destination file and merge YAML contents of src into dest.

By default creates backups, overwrites destination, and clobbers lists.

Usage:
    merge_yaml.py src dest [--create-backup=True] [--dry-run] [--show-stacktrace=False] [--merge-lists=True] [--help]
"""


import argparse
import os
import shutil
from datetime import datetime
import sys
from pathlib import Path

# Check Python version
if sys.version_info < (3, 0):
    print("Error: This script requires Python 3.0 or greater.")
    sys.exit(2)

# Try importing ruamel.yaml
try:
    from ruamel.yaml import YAML
except ImportError:
    print(
        "Error: ruamel.yaml is not installed. Please install it using 'pip install ruamel.yaml'"
    )
    sys.exit(2)

yaml = YAML()


def deep_merge(d1, d2, **kwargs):
    """Deep merges dictionary d2 into dictionary d1."""
    merge_lists = kwargs.get("merge_lists")
    for key, value in d2.items():
        if key in d1:
            if isinstance(d1[key], dict) and isinstance(value, dict):
                deep_merge(d1[key], value, **kwargs)
            elif merge_lists and isinstance(d1[key], list) and isinstance(value, list):
                d1[key].extend(value)
            else:
                d1[key] = value
        else:
            d1[key] = value
    return d1


def load_yaml_file(filename):
    """Load YAML data from a file."""
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as file:
        return yaml.load(file)


def save_yaml_file(filename, data):
    """Save YAML data to a file."""
    with open(filename, "w") as file:
        yaml.dump(data, file)


def create_backup(filename):
    """Create a timestamped backup of the file."""
    # create a directory called backups relative to the filename
    backup_dir = filename.parent / "yaml_backups"
    try:
        backup_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(
            f"Error: Could not create backup directory {backup_dir}. Check your file-permissions or use --no-create-backup to skip creating a backup."
        )
        exit(2)

    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    backup_filename = backup_dir / f"{filename.name}.{timestamp}.bak"
    shutil.copyfile(filename, backup_filename)
    print(f"Backup created: {backup_filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Deep merge YAML contents of src into dest."
    )
    parser.add_argument("src", type=Path, help="Source filename")
    parser.add_argument("dest", type=Path, help="Destination filename")
    parser.add_argument(
        "--create-backup",
        type=bool,
        default=True,
        help="Create a backup of the destination file before merging",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print to stdout only, do not write to the destination file",
    )
    # add a argument for showing the stack trace on yaml parse errors
    parser.add_argument(
        "--show-stacktrace",
        action="store_true",
        help="Show stack trace on yaml parse errors",
    )
    # add an argument to clobber lists
    parser.add_argument(
        "--merge-lists",
        action="store_true",
        help="Merge list items instead of clobbering",
        default=False,
    )

    args = parser.parse_args()

    src_filename = args.src.resolve().expanduser()
    dest_filename = args.dest.resolve().expanduser()

    # make sure both files exist
    if not src_filename.exists():
        print(f"Error: {args.src} does not exist")
        exit(2)

    if not dest_filename.exists():
        print(f"Error: {args.dest} does not exist")
        exit(2)

    try:
        src_data = load_yaml_file(src_filename)
    except Exception as e:
        print(
            f"Error: {args.src} is not a valid YAML file. Run with --show-stacktrace to see the error."
        )
        if args.show_stacktrace:
            raise e
        exit(2)
    try:
        dest_data = load_yaml_file(dest_filename)
    except Exception as e:
        print(
            f"Error: {args.dest} is not a valid YAML file. Run with --show-stacktrace to see the error."
        )
        if args.show_stacktrace:
            raise e
        exit(2)

    if args.create_backup and not args.dry_run:
        create_backup(dest_filename)

    src_data = load_yaml_file(args.src)
    dest_data = load_yaml_file(args.dest)

    # if dest_data is empty, just copy src_data to dest_data
    if not dest_data:
        if not args.dry_run:
            save_yaml_file(args.dest, src_data)
    else:
        merged_data = deep_merge(dest_data, src_data, merge_lists=args.merge_lists)
        if not args.dry_run:
            save_yaml_file(args.dest, merged_data)
            print(f"Merged data from {args.src} into {args.dest}")
        else:
            yaml.dump(merged_data, sys.stdout)


if __name__ == "__main__":
    main()

```
                        
                         
