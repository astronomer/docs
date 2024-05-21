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

