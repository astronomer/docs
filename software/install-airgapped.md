---
title: "Install Astronomer Software"
sidebar_label: "Install Astronomer Software"
description: "Install Astronomer Software in a multi-tenant, airgapped environment with all recommended security and networking configurations"
id: install-airgapped
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This guide describes the steps to install Astronomer Software, which allows you to deploy and scale any number of Apache Airflow deployments.

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
The following prerequisites apply to customers running Astronomer Software on Amazon EKS (see the 'Other' tab if running a different version of Kubernetes on AWS).

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
The following prerequisites apply to customers running Astronomer Software on Google GKE (see the 'Other' tab if running a different version of Kubernetes on GCP).

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
The following prerequisites apply to customers running Astronomer Software on Azure AKS (see the 'Other' tab if running a different version of Kubernetes on Azure).

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
The following prerequisites apply to customers running Astronomer Software on Kubernetes.

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

### Create a platform-project directory
Create a platform-project directory to store files you will be creating throughout this installation guide.

e.g.
`mkdir ~/astronomer-dev`

:::tip

Certain files in this directory may contain secrets. For your first install, keep these in a secure place on a suitable machine. See TODO - guidance on vauliting prior to continuing to higher environments

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

  # Enable privateCaCerts only if your enterprise security team
  # generated a certificate from a private certificate authority.
  # Create a generic secret for each cert, and add it to the list below.
  # Each secret must have a data entry for 'cert.pem'
  # Example command: `kubectl create secret generic private-root-ca --from-file=cert.pem=./<your-certificate-filepath>`
  # privateCaCerts:
  # - private-root-ca

  # Enable privateCaCertsAddToHost only when your nodes do not already
  # include the private CA in their containerd trust store.
  # Most enterprises already have this configured,
  # and in that case 'enabled' should be false.
  privateCaCertsAddToHost:
    enabled: true
    hostDirectory: /etc/containerd/certs.d
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

  # Enable privateCaCerts only if your enterprise security team
  # generated a certificate from a private certificate authority.
  # Create a generic secret for each cert, and add it to the list below.
  # Each secret must have a data entry for 'cert.pem'
  # Example command: `kubectl create secret generic private-root-ca --from-file=cert.pem=./<your-certificate-filepath>`
  # privateCaCerts:
  # - private-root-ca

  # Enable privateCaCertsAddToHost only when your nodes do not already
  # include the private CA in their containerd trust store.
  # Most enterprises already have this configured,
  # and in that case 'enabled' should be false.
  privateCaCertsAddToHost:
    enabled: true
    hostDirectory: /etc/containerd/certs.d
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

  # Enable privateCaCerts only if your enterprise security team
  # generated a certificate from a private certificate authority.
  # Create a generic secret for each cert, and add it to the list below.
  # Each secret must have a data entry for 'cert.pem'
  # Example command: `kubectl create secret generic private-root-ca --from-file=cert.pem=./<your-certificate-filepath>`
  # privateCaCerts:
  # - private-root-ca

  # Enable privateCaCertsAddToHost only when your nodes do not already
  # include the private CA in their containerd trust store.
  # Most enterprises already have this configured,
  # and in that case 'enabled' should be false.
  # privateCaCertsAddToHost:
  #   enabled: true
  #   hostDirectory: /etc/containerd/certs.d

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

  # Enable privateCaCerts only if your enterprise security team
  # generated a certificate from a private certificate authority.
  # Create a generic secret for each cert, and add it to the list below.
  # Each secret must have a data entry for 'cert.pem'
  # Example command: `kubectl create secret generic private-root-ca --from-file=cert.pem=./<your-certificate-filepath>`
  # privateCaCerts:
  # - private-root-ca

  # Enable privateCaCertsAddToHost only when your nodes do not already
  # include the private CA in their containerd trust store.
  # Most enterprises already have this configured,
  # and in that case 'enabled' should be false.
  privateCaCertsAddToHost:
    enabled: true
    hostDirectory: /etc/containerd/certs.d
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


## Step 3: Choose and configure the base domain {#choose-and-configure-the-base-domain}

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
* you will need to have or obtain a TLS certificate that is recognized as valid by your users (and if using the bundled container-registry, by Kubernetes itself)
* wildcardcard certificates are only valid one-level deep (e.g. an ingress controller using a certificate of `*.example.com` can provide service for `app.example.com` but not `app.astronomer-dev.example.com`).
* the bottom-level hostnames (e.g. `app`, `registry`, `prometheus`) are fixed and cannot be changed.
* most kubernetes clusters refuse to resolve DNS hostnames with more than 5 segments (seperated by the dot character; e.g. `app.astronomer.sandbox.mygroup.example.com` is 6 segments and might be problematic, so choosing a baseDomain of `astronomer-sandbox.mygroup.example.com` instead of `astronomer.sandbox.mygroup.example.com` would be advisable).
* the base-domain will be visible to end-users
  - when accessing the Astronomer Software UI (e.g. `https://app.sandbox-astro.example.com`)
  - when accessing an Airflow Deployment (e.g. `https://deployments.sandbox-astro.example.com/deployment-release-name/airflow`)
  - when logging into the astro cli (e.g. `astro login sandbox-astro.example.com`)
  
:::tip

Openshift customers who wish to use OpenShift's integrated ingress controller typically use the hostname of the default OpenShift ingress controller as their base-domain. Doing so results in a slightly-unwieldy user-visible hostname of `app.apps.<openshift-domain>` and requires permission to re-configure the route-admission policy for the standard ingress controller to `InterNamespaceAllowed` (covered later in this document). See [Third Party Ingress Controller - Configuration notes for Openshift](third-party-ingress-controllers#configuration-notes-for-openshift) additional infomation and options.

:::

### Configuring the base domain

Locate the `global.baseDomain` key already present in your `values.yaml` file and change it to your base-domain.

e.g.
```
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: sandbox-astro.example.com
```

## Step 4: Create the Astronomer Software platform namespace {#create-the-astronomer-software-platform-namespace}

In your Kubernetes cluster, create a [kubernetes namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) (Astronomer generally recommends this namespace be named `astronomer`) to contain the Astronomer Software platform.

```sh
kubectl create namespace astronomer
```

The contents of this namespace will be used to provision and manage Airflow instances running in other namespaces. Each Airflow will have its own isolated namespace.

## Step 5: Third-Party Igress-Controller DNS Configuration {#third-party-igress-controller-dns-configuration}

If using Astronomer's bundled ingress-controller - skip this step.

### Astronomer Software Third-Party DNS Requirements and Record Guidance {#third-party-dns-guidance}

Astronomer Software requires the following domain-names be registered and resolvable within the Kubernetes Cluster and to users of Astronomer And Airflow.
  - `<base-domain>` (optional but recommended, provides a vanity re-direct to `app.<base-domain>`)
  - `app.<base-domain>` (required)
  - `deployments.<base-domain>` (required)
  - `houston.<base-domain>` (required)
  - `grafana.<base-domain>` (required if using bundled grafana)
  - `kibana.<base-domain>` (required if not using external elasticsearch)
  - `install.<base-domain>` (optional)
  - `alertmanager.<base-domain>` (required if using bundled alert manager)
  - `prometheus.<base-domain>` (required)
  - `registry.<base-domain>` (required if using bundled container-registry)

Astronomer generally recommends that:
* the `<base-domain>` record be a zone-apex record (typically expressed by using a hostname of `@`) pointing to the IP(s) of the ingress-controller
* all other records be CNAME records pointing to the `<base-domain>`

For customers unable to register the base-domain, Astronomer recommends that:
* the `app.<baseDomain>` record be an A record pointing to the IP(s) of the ingress-controller
* all other records be CNAME records pointing to `app.<base-domain>`

:::tip

For lower environments, Astronomer recommends a relatively short ttl-value (e.g. 60 seconds) when you first deploy Astronomer so that any errors can be quickly corrected.

:::


### Request Ingress Information from your Ingress-Administrator {get-ingress-info}

Provide your Ingress Controller Administrator with the [Astronomer Software Third-Party DNS Requirements and Record Guidance](#third-party-dns-guidance) above (replacing`<base-domain>` with the base-domain from [Choosing the Base Domain](#choosing-the-base-domain)) and guidance and request the following information:
* what ingress class name you should use (or whether you should leave blank and use the default)
* what IP address(es) you should use for DNS entries pointing to the ingress controller
* whether DNS-records will be automatically created in reponse to Ingress rources that we will be created later in the install
* if DNS-records need to be manually created, and if so who will coordinate their creation and who will create them
### Create DNS records pointing to your third-party ingress-controller

Create DNS records pointed to your third-party ingress. controller.

### Verify DNS records are pointed to your third-party ingress-controller

Use `dig <hostname>` or `getent hosts <hostname>` to verify each DNS entry is created and pointing to the IP address of the ingress-controller you will be using.


## Step 6: Requesting and Validating an Astronomer TLS Certificate {#requesting-and-validating-an-astronomer-tls-certificate}

In order to install Astronomer Software, you'll need a TLS certificate that is valid for several domains - one of which will be the primary name on the certificate (referred to as the Common name or CN) and the rest will be equally-valid supplementary domains known as Subject Alternative Names (SAN)s.

Astronomer requires a private certificate be present in the Astronomer Platform namespace, even if using a third-party ingress-controller that doesn't otherwise require it.

### Requesting an Astronomer TLS Certificate

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

If using Astronomer's bundled container image registry, the encryption-type used on your TLS certificate must be *RSA*. Cerbot users must include `-key-type rsa` when requesting certificates, most other solutions generate RSA-keys by default.

:::

In your request to your Security Team, include:
* the Common Name and Subject Alternative Name(s) as per above
* if using the bundled Astronomer container-registry, the requirement that the encryption type of the certificate *must* be RSA
* request that the return format be as follows:
  - a key.pem - containing the private key
  - **either** a full-chain.pem (containing the public certificate additional certificates required to validate it) **or** a bare `cert.pem` and explicit affirmation that there are no intermediate certificates an that the public certificate is the full-chain
  - **either** a statement that the certificate is signed by public and generally recognized Certificate Authority **or** the public certificate of the Certificate Authority used to create your certificate

### Validating the received certficiate and associated items
Ensure that you have received each of the follownig three items:

* a key.pem - containing the private key
* **either** a full-chain.pem (containing the public certificate additional certificates required to validate it) **or** a bare `cert.pem` and explicit affirmation that it the full-chain
* **either** a statement that the certificate is signed by public and generally recognized Certificate Authority **or** the public certificate of the Certificate Authority used to create your certificate


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

## Step 7: Storing and configuring the Public TLS Full-Chain Certificate {#storing-and-configuring-the-public-tls-full-chain-certificate}

### Storing the full-chain TLS certificate in the Astronomre Platform Namespace
Store the public full-chain certificate in the Astronomer Software Platform Namespace in a `tls`-type Kubernetes secret named `astronomer-tls` using the following command.

If your enterprise-security organization has instructed you that there are no intermediate certifi

```sh
kubectl -n <astronomer platform namespace> create secret tls astronomer-tls --cert <fullchain-pem-filepath> --key <your-private-key-filepath>
```

E.g.
```
kubectl -n astronomer create secret tls astronomer-tls --cert fullchain.pem --key server_private_key.pem
```

Naming the secret `astronomer-tls` (no substitutions) is always recommended and is a strict requirement when using a third-party ingress-controller.

## Step 8: Configuring a third-party ingress-controller {#configuring-a-third-party-ingress-controller}
### Check your ingress-controller
### Set the full-chain TLS certificate Kubernetes Secret for replication
Most third-party ingress-controllers require the `astronomer-tls` secret be replicated into each Airflow namespace.

Annotate the secret and set `"astronomer.io/commander-sync` to `platform=<astronomer platform release name>`, e.g.:
```
kubectl -n <astronomer platform namespace> annotate secret astronomer-tls "astronomer.io/commander-sync"="platform=astronomer"
```

Astronomer will automatically replicate the secret into the namespace used by each newly deployed Airflow instance.
