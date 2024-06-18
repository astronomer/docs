---
title: "Install Astronomer Software"
sidebar_label: "Install Astronomer Software"
description: "Install Astronomer Software in a multi-tenant, airgapped environment with all recommended security and networking configurations"
id: install-airgapped
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This guide describes the steps to install Astronomer Software, which allows you to deploy and scale any number of Apache Airflow deployments.

Astronomer recommends platform administrators perform their first Astronomer Software installation manually using the procedures described in this document. You can adapt the procedure to meet organizational best practices when deploying to change-controlled environments.

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

:::info

The following prerequisites apply when running Astronomer Software on Amazon EKS. See the **Other** tab if you run a different version of Kubernetes on AWS.

:::

- An EKS Kubernetes cluster, running a version of Kubernetes certified as compatible on the [Version Compatibility Reference](version-compatibility-reference.md) that provides the following components:
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
- A machine meeting the following criteria with access to the Kubernetes API Server:
    * Network access to the Kubernetes API Server - either direct access or VPN.
    * Network access to load-balancer resources that are created when Astronomer Software is installed later in the procedure - either direct access or VPN.
    * Configured to use the DNS servers where Astronomer Software DNS records can be created.
    * [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
    * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) might be required to troubleshoot certain certificate-related conditions.
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) might be required to troubleshoot certain certificate-related conditions.

</TabItem>

<TabItem value="gcp">
:::info 

The following prerequisites apply when running Astronomer Software on Google GKE. See the **Other** tab if you run a different version of Kubernetes on GCP.

:::

- A GKE Kubernetes cluster, running a version of Kubernetes listed as compatible on the [Version Compatibility Reference](version-compatibility-reference.md).
- A PostgreSQL instance, accessible from your Kubernetes cluster, and running a version of Postgres certified as compatible on the [Version Compatibility Reference](version-compatibility-reference.md).
- PostgreSQL superuser permissions.
- Permission to create and modify resources on Google Cloud Platform.
- Permission to generate a certificate that covers a defined set of subdomains.
- An SMTP service and credentials. For example, Mailgun or Sendgrid.
- [Google Cloud SDK](https://cloud.google.com/sdk/install).
- A machine that meets the following criteria with access to the Kubernetes API Server:
    * Network access to the Kubernetes API Server - either direct access or VPN.
    * Network access to load-balancer resources that are created when Astronomer Software is installed later in the procedure - either direct access or VPN.
    * Configured to use the DNS servers where Astronomer Software DNS records can be created.
    * [Helm with minimum version 3.6](https://helm.sh/docs/intro/install).
    * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
    * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) might be required to troubleshoot certain certificate-related conditions.


</TabItem>

<TabItem value="azure">
:::info

The following prerequisites apply when running Astronomer Software on Azure AKS. See the **Other** tab if you run a different version of Kubernetes on Azure.

:::

- A Kubernetes cluster, running a version of Kubernetes listed as compatible on the [Version Compatibility Reference](version-compatibility-reference.md).
- A PostgreSQL instance, accessible from your Kubernetes cluster, and running a version of Postgres certified as compatible on the [Version Compatibility Reference](version-compatibility-reference.md).
  * If your organization uses Azure Database for PostgreSQL as the database backend, you need to enable the `pg_trgm` extension using the Azure portal or the Azure CLI before you install Astronomer Software. If you don't enable the `pg_trgm` extension, the install fails. For more information about enabling the `pg_trgm` extension, see [PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions).
- PostgreSQL superuser permissions.
- Permission to create and modify resources on Azure.
- Permission to generate a certificate that covers a defined set of subdomains.
- An SMTP service and credentials. For example, Mailgun or Sendgrid.
- The [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- A machine meeting the following criteria with access to the Kubernetes API Server:
    * Network access to the Kubernetes API Server - either direct access or VPN.
    * Network access to load-balancer resources created when Astronomer Software is installed later in the procedure - either direct access or VPN.
    * Configured to use the DNS servers where Astronomer Software DNS records will be created.
    * [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
    * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
    * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) might be required to trouble-shoot certain certificate-related conditions.

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
  * Network access to the Kubernetes API Server - either direct access or VPN.
  * Network access to load-balancer resources created when Astronomer Software is installed later in the procedure - either direct access or VPN.
  * Configured to use the DNS servers where Astronomer Software DNS records will be created.
  * [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
  * The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- (Situational) The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html) might be required to trouble-shoot certain certificate-related conditions.
</TabItem>

</Tabs>

## Step 1: Plan the structure of your Astronomer Software environments {#structure-platform-environments}

Before installing Astronomer Software, consider how many instances of the platform you want to host because you install each of these instances on separate Kubernetes clusters following the instructions in this document.

Each instance of Astronomer Software can host multiple Airflow environments, or Deployments. Some common types of Astronomer Software instances you might consider hosting are:

- Sandbox: The lowest environment that contains no sensitive data, used only by system-administrators to experiment, and not subject to change control.
- Development: User-accessible environment that is subject to most of the same restrictions of higher environments, with relaxed change control rules.
- Staging: All network, security, and patch versions are maintained at the same level as in the production environment. However, it provides no availability guarantees and includes relaxed change control rules.
- Production: The production instance hosts your production Airflow environments. You can choose to host development Airflow environments can be here or in environments with lower levels of support and restrictions.

For each instance of the platform that you plan to host, create a project folder to contain the platform instance's configurations. For example, if you want to install a development environment, create a folder named `~/astronomer-dev`.


:::info

Certain files in the project directory might contain secrets when you set up your sandbox or development environments. For your first install, keep these secrets in a secure place on a suitable machine. As you progress to higher environments, such as staging or production, secure these files separately in a vault and use the remaining project files in your directory to serve as the basis for your CI/CD deployment.

:::

## Step 2: Create `values.yaml` from a template {#create-valuesyaml}

Astronomer Software uses Helm to apply platform-level configurations. Use one of the following templates as the basis for your Astronomer Software platform configuration by copying the template into a local file named `values.yaml` in your platform project directory. As you continue to extend the functionality of your Astronomer Software instances, you can continually modify this file to take advantage of new features.

:::warning

As you copy the template configuration, keep the following in mind.

- Do not make any changes to this file until instructed to do so in later steps.
- Do not run `helm upgrade` or `upgrade.sh` until instructed to do so in later steps. 
- Ignore any instructions to run `helm upgrade` from other Astronomer documentation until you've completed this installation.

:::

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
  # Dictionary of arbitrary annotations to add to the nginx ingress. For full configuration options, see https://docs.nginx.com/nginx-ingress-controller/configuration/ingress-resources/advanced-configuration-with-annotations/
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

## Step 3: Decide whether to use a third-party Ingress controller {#decide-ingress-controller}

Astronomer Software requires a Kubernetes Ingress controller to function and provides an integrated Ingress controller by default.

Astronomer generally recommends you use the integrated Ingress controller, but Astronomer Software also supports certain third-party [ingress-controllers](#third-party-ingress-controllers).

Ingress controllers typically need elevated permissions (including a ClusterRole) to function. Specifically, the Astronomer Software Ingress controller requires the ability to: 

- List all namespaces in the cluster. 
- View ingresses in the namespaces.
- Retrieve secrets in the namespaces to locate and use private TLS certificates that service the ingresses.

If you have complex regulatory requirements, you might need to use an Ingress controller that's approved by your organization and disable Astronomer's integrated controller. You configure this detail later in the installation.

## Step 4: Choose and configure a base domain {#choose-base-domain}

When you install Astronomer Software, it creates a variety of services that your users access to manage, monitor, and run Airflow.

Choose a base domain such as `astronomer.example.com`, `astro-sandbox.example.com`, `astro-prod.example.internal` for which:

- You have the ability to create and edit DNS records
- You have the ability to issue TLS certificates
- The following addresses are available:
  - `app.<base-domain>`
  - `deployments.<base-domain>`
  - `houston.<base-domain>`
  - `grafana.<base-domain>`
  - `kibana.<base-domain>`
  - `install.<base-domain>`
  - `alertmanager.<base-domain>`
  - `prometheus.<base-domain>`
  - `registry.<base-domain>`

The base domain itself does not need to be available and can point to another service not associated with Astronomer or Airflow. If the base domain is available, you can choose to establish a vanity redirect from `<base-domain>` to `app.<base-domain>` later in the installation process.

When choosing a base domain, consider the following:

- The name you choose must be be resolvable by both your users and Kubernetes itself.
- You need to have or obtain a TLS certificate that is recognized as valid by your users. If you use the Astronomer Software integrated container registry, the TLS certification must also be recognized as valid by Kubernetes itself.
- Wildcard certificates are only valid one level deep. For example, an ingress controller that uses a certificate called `*.example.com` can provide service for `app.example.com` but not `app.astronomer-dev.example.com`.
- The bottom-level hostnames, such as `app`, `registry`, `prometheus`, are fixed and cannot be changed.
- Most Kubernetes clusters don't resolve DNS hostnames with more than five segments, each separated by the dot character, `.`. For example, `app.astronomer.sandbox.mygroup.example.com` is six segments and might cause problems. Astronomer recommends choosing a base domain of `astronomer-sandbox.mygroup.example.com` instead of `astronomer.sandbox.mygroup.example.com`.

The base domain is visible to end users. They can view the base domain in the following scenarios:

  - When users access the Astronomer Software UI. For example, `https://app.sandbox-astro.example.com`.
  - When users access an Airflow Deployment. For example, `https://deployments.sandbox-astro.example.com/deployment-release-name/airflow`.
  - When users authenticate to the Astro CLI. For example, `astro login sandbox-astro.example.com`.
  
:::info

If you install Astronomer Software on OpenShift and also want to use OpenShift's integrated ingress controller, you can use the the hostname of the default OpenShift ingress controller as your base domain, such as `app.apps.<OpenShift-domain>`. Doing this requires permission to reconfigure the route admission policy for the standard ingress controller to `InterNamespaceAllowed`. See [Third Party Ingress Controller - Configuration notes for OpenShift](third-party-ingress-controllers.md#configuration-notes-for-OpenShift) for additional information and options.

:::

### Configure the base domain

Locate the `global.baseDomain` in your `values.yaml` file and change it to your base domain as shown in the following example:

```yaml
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: sandbox-astro.example.com
```

## Step 5: Create the Astronomer Software platform namespace {#create-astronomer-namespace}

In your Kubernetes cluster, create a [Kubernetes namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) to contain the Astronomer Software platform. Astronomer recommends naming this namespace `astronomer`. 

```sh
kubectl create namespace astronomer
```

Astronomer Software uses the contents of this namespace to provision and manage Airflow instances running in other namespaces. Each Airflow instance has its own isolated namespace.

## Step 6: (Optional) Configure third-party Ingress controller DNS {#ingress-controller-dns-configuration}

Skip this step if you use Astronomer Software's integrated ingress controller.

Follow the instructions in this section to create DNS entries pointing to the third-party ingress controller instance that provides ingress service to Astronomer Software.

### Astronomer Software Third-Party DNS Requirements and Record Guidance {#third-party-dns-guidance}

Astronomer Software requires the following domain names be registered and resolvable within the Kubernetes cluster and to Astronomer Software users:

  - `app.<base-domain>` (required)
  - `deployments.<base-domain>` (required)
  - `houston.<base-domain>` (required)
  - `prometheus.<base-domain>` (required)
  - `grafana.<base-domain>` (required if using Astronomer Software's integrated grafana)
  - `kibana.<base-domain>` (required if not using external elasticsearch)
  - `registry.<base-domain>` (required if using Astronomer Software's integrated container-registry)
  - `alertmanager.<base-domain>` (required if using Astronomer Software's integrated Alert Manager)
  - `<base-domain>` (optional but recommended, provides a vanity re-direct to `app.<base-domain>`)
  - `install.<base-domain>` (optional)

Astronomer generally recommends that:

- The `<base-domain>` record is a zone apex record, that is typically expressed by using a hostname of `@`, and points to the IP(s) of the ingress controller.
- All other records are CNAME records that point to the `<base-domain>`.

For platform administrators unable to register the base domain, Astronomer recommends that:

- The `app.<baseDomain>` record is a record pointing to the IPs of the ingress controller.
- All other records are CNAME records pointing to `app.<base-domain>`.

:::tip

For lower environments like sandboxes or development environments, Astronomer recommends a relatively short ttl value, such as 60 seconds, when you first deploy Astronomer so that any errors can be quickly corrected.

:::

### Request ingress information from your ingress administrator {#get-ingress-info}

Provide the details you gathered in [Astronomer Software Third-Party DNS Requirements and Record Guidance](#third-party-dns-guidance) to your ingress controller administrator, making sure to replace `<base-domain>` with your chosen base domain. Then, request the following information from the administrator:

- The ingress class name to use, or whether you should leave the class name blank and use the default.
- The IP addresses to use for DNS entries pointing to the ingress controller.
- Whether DNS records are automatically created in response to ingress sources that you create later in the install.
- Whether DNS records need to be manually created, and if so, who coordinates their creation and who creates them.

Save this information for later in this setup.

### Create DNS records pointing to your third-party Ingress controller

Create DNS records that point to your third-party ingress controller, based. on your organization's standard workflows.

Use `dig <hostname>` or `getent hosts <hostname>` to verify that each DNS entry is created and points to the IP address of the ingress controller you use.

## Step 7: Request and validate an Astronomer TLS certificate {#astronomer-tls-certificate}

To install Astronomer Software, you need a TLS certificate that is valid for several domains. One of the domains is the primary name on the certificate, also known as the common name (CN). The additional domains are equally valid, supplementary domains known as Subject Alternative Names (SANs).

Astronomer requires a private certificate to be present in the Astronomer Software platform namespace, even if you use a third-party ingress controller that doesn't otherwise require it.

### Request an ingress controller TLS certificate {#request-a-certificate-bundle}

Request a TLS certificate from your security team for Astronomer Software. In your request, include the following:

- Your chosen base domain as the Common Name (CN). If your certificate authority will not issue certificates for the bare base domain, use `app.<base-domain>` as the CN instead.
- *Either* a wildcard Subject Alternative Name (SAN) entry of `*.<base-domain>` *or* an explicit SAN entry for each of the following items:
    - `app.<base-domain>` (omit if already used as the Common Name)
    - `deployments.<base-domain>`
    - `registry.<base-domain>`
    - `houston.<base-domain>`
    - `grafana.<base-domain>`
    - `kibana.<base-domain>`
    - `install.<base-domain>`
    - `alertmanager.<base-domain>`
    - `prometheus.<base-domain>`
* If you use the Astronomer Software integrated container registry, specify that that the encryption type of the certificate must be RSA.
* Request the following return format:
  - A `key.pem` containing the private key in pem format
  - **Either** a `full-chain.pem` (containing the public certificate additional certificates required to validate it, in pem format) **or** a bare `cert.pem` and explicit affirmation that there are no intermediate certificates and that the public certificate is the full chain.
  - **Either** the `private-root-ca.pem` in pem format of the private Certificate Authority used to create your certificate or a statement that the certificate is signed by a public Certificate Authority.

:::warning

If you're using the Astronomer Software integrated container registry, the encryption type used on your TLS certificate must be **RSA**. Cerbot users must include `-key-type rsa` when requesting certificates. Most other solutions generate RSA keys by default. 

:::

### Validate the received certificate and associated items

Ensure that you received each of the following three items:

- A `key.pem` containing the private key in pem format.
- **Either** a `full-chain.pem`, in pem format, that contains the public certificate additional certificates required to validate it **or** a bare `cert.pem` and explicit affirmation that there are no intermediate certificates and that the public certificate is the full chain.
- **Either** the `private-root-ca.pem` in pem format of the the private Certificate Authority used to create your certificate **or** a statement that the certificate is signed by public Certificate Authority.

To validate that your security team generated the correct certificate, run the following command using the `openssl` CLI:

```sh
openssl x509 -in  <your-certificate-filepath> -text -noout
```

This command will generate a report. If the `X509v3 Subject Alternative Name` section of this report includes either a single `*.<base-domain>` wildcard domain or all subdomains, then the certificate creation was successful.

Confirm that your full-chain certificate chain is ordered correctly. To determine your certificate chain order, run the following command using the `openssl` CLI:

```sh
openssl crl2pkcs7 -nocrl -certfile <your-full-chain-certificate-filepath> | openssl pkcs7 -print_certs -noout
```

The command generates a report of all certificates. Verify that the certificates are in the following order:

- Domain
- Intermediate (optional)
- Root

### (Optional) Additional validation for the Astronomer integrated container registry {#docker-registry-cert-encryption-restrictions}


:::info

If you don't plan to store images in Astronomer's integrated container registry and instead plan to store all container images using an [external container registry](#configure-a-private-docker-registry-airflow), you can skip this step.

:::

The Astronomer Software integrated container registry requires that your private key signs traffic originating from the Astronomer Software platform using the RSA encryption method. Confirm that the key is signing traffic correctly before proceeding.

Run the following command to extract the bare public cert, if it was not already included in the files provided by your certificate authority, from the full-chain certificate file:

```sh
openssl crl2pkcs7 -nocrl -certfile full-chain.pem | openssl pkcs7 -print_certs -noout > cert.pem
```

Examine the public certificate and ensure all Signature Algorithms are listed as `sha1WithRSAEncryption`.

```sh
openssl x509 -in cert.pem -text|grep Algorithm 
        Signature Algorithm: sha1WithRSAEncryption
            Public Key Algorithm: rsaEncryption
    Signature Algorithm: sha1WithRSAEncryption
```

If your key is not compatible with the Astronomer Software integrated container registry, ask your Certificate Authority to [re-issue the credentials](#request-a-certificate-bundle) and emphasize the need for an RSA cert, or [use an external container registry](#configure-a-private-docker-registry-airflow).

## Step 8: Store and configure the ingress controller public TLS full-chain certificate {#public-tls-full-chain-certificate}

Run the following command to store the public full-chain certificate in the Astronomer Software Platform Namespace in a `tls`-type Kubernetes secret named `astronomer-tls`. 

```sh
kubectl -n <astronomer platform namespace> create secret tls astronomer-tls --cert <fullchain-pem-filepath> --key <your-private-key-filepath>
```

However, if your security team has instructed you that there are no intermediate certificates, run the following code example.
```sh
kubectl -n astronomer create secret tls astronomer-tls --cert full-chain.pem --key server_private_key.pem
```

Naming the secret `astronomer-tls` with no substitutions is always recommended and a strict requirement when using a third-party ingress controller.

## Step 9: (Optional) Configure a third-party ingress controller {#configure-third-party-ingress-controller}

If you use Astronomer Software's integrated ingress controller, you can skip this step.

Complete the full setup as described in [Third-party Ingress-Controllers](third-party-ingress-controllers.md), which includes steps to configure ingress controllers in specific environment types. When you're done, return to this page and continue to the next step.

## Step 10: Configure a private certificate authority {#configure-private-certificate-authority}

Skip this step if you don't use a private Certificate Authority (private CA) to sign the certificate used by your ingress-controller. Or, if you don't use a private CA for any of the following services that the Astronomer Software platform interacts with.

Astronomer Software trusts public Certificate Authorities automatically.

Astronomer Software must be configured to trust any private Certificate Authorities issuing certificates for systems Astronomer Software interacts with, including but not limited-to:
* ingress controller
* email server, unless disabled
* any container registries that Kubernetes pulls from
* if using OAUTH, the OAUTH provider
* if using external elasticsearch, any external elasticsearch instances
* if using external prometheus, any external prometheus instances

Perform the procedure described in [Configuring private CAs](#configuring-private-cas) for each certificate authority used to sign TLS certificates.

:::info

Astro CLI users must also configure both their operating system and container solution, [Docker Desktop or Podman]((#configure-desktop-container-solution-extra-cas), to trust the private certificate Authority that was used to create the certificate used by the Astronomer Software ingress controller and any third-party container registries.

:::

## Step 11: Confirm your Kubernetes cluster trusts required CAs {#private-cas-for-kubernetes}

If at least one of the following circumstances apply to your installation, complete this step:

- You configured Astronomer Software to pull [platform container images](#use-a-custom-image-repository-for-platform-images) from an external container registry that uses a certificate signed by a private CA.
- You plan for your users to deploy Airflow images to Astronomer Software's integrated container registry *and* Astronomer is using a TLS certificate issued by a private CA.
- Users will deploy images to an external container registry *and* that registry is using a TLS certificate issued by a private CA. 

Kubernetes must be able to pull images from one or more container registries for Astronomer Software to function. By default, Kubernetes only trusts publicly signed certificates.  This means that by default, Kubernetes does not honor the list of certificates [trusted by the Astronomer Software platform](#configuring-a-private-certificate-authority).

Many enterprises configure Kubernetes to trust additional certificate authorities as part of their standard cluster creation procedure. Contact your Kubernetes Administrator to find out what, if any, private certificates are currently trusted by your Kubernetes Cluster. Then, consult your Kubernetes administrator and Kubernetes provider's documentation for instructions on configuring Kubernetes to trust additional CAs.

Follow procedures for your Kubernetes provider to configure Kubernetes to trust each CA associated with your container registries, including the integrated container registry, if applicable.

Certain clusters do not provide a mechanism to configure the list of certificates trusted by Kubernetes.

While configuring the Kubernetes list of cluster certificates is a customer responsibility, Astronomer Software includes an optional component that can, for certain Kubernetes cluster configurations, add certificates defined in `global.privateCaCerts` to the list of certificates trusted by Kubernetes. This can be enabled by setting `global.privateCaCertsAddToHost.enabled` and ``global.privateCaCertsAddToHost.addToContainerd` to `true` in your `values.yaml` file and setting `global.privateCaCertsAddToHost.containerdConfigToml` to:

```
[host."https://registry.<baseApp>"]
  ca = "/etc/containerd/certs.d/<registry hostname>/<secret name>.pem"
```

For example, if your base domain is astro-sandbox.example.com and the CA public-certifice certificate is stored in the platform namespace in a secret named `my-private-ca`, the `global.privateCaCertsAddToHost` section would be:

```yaml
  global:
    privateCaCertsAddToHost:
      enabled: true
      addToContainerd: true
      hostDirectory: /etc/containerd/certs.d
      containerdConfigToml: |-
        [host."https://registry.astro-sandbox.example.com"]
          ca = "/etc/containerd/certs.d/registry.astro-sandbox.example.com/my-private-ca.pem"      
```

## Step 12: Configure outbound SMTP email {#configure-outbound-smtp-email}

Astronomer Software requires the ability to send email to:

- Notify users of errors with their Airflow Deployments.
- Send emails to invite new users to Astronomer.
- Send certain platform alerts, enabled by default but can be configured.

Astronomer Software sends all outbound email using SMTP.

:::info

If SMTP is not available in the environment where you're installing Astronomer Software, follow instructions in [configure Astronomer Software to not send outbound email](#configure-astronomer-software-to-not-send-outbound-email), and then skip the rest of this section.

:::

1. Obtain a set of SMTP credentials from your email administrator for you to use to send email from Astronomer Software. When you request an email address and display name, remember that these emails are not designed for users to reply directly to them. Request all the following information:
     * Email address
     * Email display name requirements. Some email servers require a **From** line of: `Do Not Reply <donotreply@example.com>`. 
     * SMTP username. This is usually the same as the email address.
     * SMTP password
     * SMTP hostname
     * SMTP port
     * Whether or not the connection supports TLS
     
     :::info 

    If there is a `/` or any other escape character in your username or password, you may need to [URL encode](https://www.urlencoder.org/) those characters.

    :::
    
2. Ensure that your Kubernetes cluster has access to send outbound email to the SMTP server.
3. Change the configuration in `values.yaml` from `noreply@my.email.internal` to an email address that is valid to use with your SMTP credentials.
4. Construct an email connection string and store it in a secret named `astronomer-tls` in the Astronomer platform namespace. Make sure to *url-encode* the username and password if they contain special characters.

    ```sh
    kubectl -n astronomer create secret generic astronomer-smtp --from-literal connection="smtp://my@40user:my%40pass@smtp.email.internal/?requireTLS=true"
    ```

    In general, an SMTP URI is formatted as `smtps://USERNAME:PASSWORD@HOST/?pool=true`. The following table contains examples of the URI for some of the most popular SMTP services:

    | Provider          | Example SMTP URL                                                                                 |
    |-------------------|--------------------------------------------------------------------------------------------------|
    | AWS SES           | `smtp://AWS_SMTP_Username:AWS_SMTP_Password@email-smtp.us-east-1.amazonaws.com/?requireTLS=true` |
    | SendGrid          | `smtps://apikey:SG.sometoken@smtp.sendgrid.net:465/?pool=true`                                   |
    | Mailgun           | `smtps://xyz%40example.com:password@smtp.mailgun.org/?pool=true`                                 |
    | Office365         | `smtp://xyz%40example.com:password@smtp.office365.com:587/?requireTLS=true`                      |
    | Custom SMTP-relay | `smtp://smtp-relay.example.com:25/?ignoreTLS=true`                                               |

    If your SMTP provider is not listed, refer to the provider's documentation for information on creating an SMTP URI.

:::info 

If there is a `/` or any other escape character in your username or password, you may need to [URL encode](https://www.urlencoder.org/) those characters.

:::

## Step 13: Configure volume storage classes

Skip this step if your cluster defines a volume storage class, and you want to use it for all volumes associated with Astronomer Software and its Airflow Deployments.

Astronomer strongly recommends that you do not back any volumes used for Astronomer Software with mechanical hard drives.

Replace `<desired-storage-class>` in the following configuration with the storage class you want to use for each respective component. You can remove the configuration for any component where using the default storage is acceptable. 

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

Merge these values into `values.yaml`. You can do this manually or by placing [merge_yaml.py](#merge-yaml) and the configuration as a new file in your project directory and running `python merge_yaml.py storage-class-config.yaml values.yaml`.

## Step 14: Configure the database {#configure-the-database}

Astronomer requires a central Postgres database that acts as the backend for Astronomer's Houston API and hosts individual metadata databases for all Deployments created on the platform.

:::info

If, while evaluating Astronomer Software, you need to create a temporary environment where Postgres is not available, locate the `global.postgresqlEnabled` option already present in your `values.yaml` and set it to `true`, then skip the remainder of this step.

Note that `global.postgresqlEnabled` to `true` is an unsupported configuration, and should never be used on any development, staging, or production environment.

:::

:::info

If you use Azure Database for either PostgreSQL or another Postgres instance that does not enable the `pg_trgm` by default, you must enable the `pg_trgm` extension prior to installing Astronomer Software. If `pg_trgm` is not enabled, the install will fail. `pg_tgrm` is enabled by default on Amazon RDS and Google Cooud SQL for PostgresQL. 

For instructions on enabling the `pg_trgm` extension for Azure Flexible Server, see [PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions).

:::

Additional requirements apply to the following databases:

- AWS RDS:
  - [t2 medium](https://aws.amazon.com/rds/instance-types/) is the minimum RDS instance size you can use.
- Azure Flexible Server:
  - You must enable the `pg_trgm` extension as per the advisory earlier in this section.
  - Set `global.ssl.mode`to `prefer` in your `values.yaml` file.

Create a Kubernetes Secret named `astronomer-bootstrap` that points to your database. You must URL encode any special characters in your Postgres password.

To create this secret, run the following command replacing the astronomer platform namespace, username, password, database hostname, and database port with their respective values. Remember that username and password must be url-encoded if they contain special-characters:

```sh
kubectl --namespace <astronomer platform namespace> create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://<url-encoded username>:<url-encoded password>@<database hostname>:<database port>"
```

For example, for a username named `bob` with password `abc@abc` at hostname `some.host.internal`, you would run:

```sh
kubectl --namespace astronomer create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://bob:abc%40abc@some.host.internal:5432"
```

## Step 15: Configure an external Docker registry for Airflow images {#configure-a-private-docker-registry-airflow}

By default, Astronomer Software users create customized Airflow container images when they deploy project code to the platform. These images frequently contain sensitive information and must be stored in a secure location accessible to Kubernetes.

Astronomer Software includes an integrated image registry for this purpose.

Users can use images hosted in other container image repositories accessible to the Kubernetes cluster without additional platform-level configuration.

See [Configure a custom registry for Deployment images](#custom-image-registry) for additional configurable options.

## Step 16: Configure the Docker registry used for platform images {#configure-a-private-docker-registry-platform}

Skip this step if you are installing Astronomer Software onto a Kubernetes cluster that can pull container images from public image repositories and you don't want to mirror these images locally.

### Configure your install use a custom image repository for platform images {#use-custom-image-repository-for-platform-images}

Astronomer expects the images to use their normal names, but prefixed by a string you define. For example, if you specify `artifactory.example.com/astronomer`, when you mirror images later in this procedure, you mirror `quay.io/astronomer/<image>` as `<custom-platform-repo-prefix>/astronomer/<image>`. The following show additional examples:

- `quay.io/astronomer/ap-houston-api` to `artifactory.example.com/astronomer/ap-houston-api`
- `quay.io/astronomer/astronomer/ap-commander` to `artifactory.example.com/astronomer/ap-commander`

Replace `<custom-platform-repo-prefix>` in the following configuration data with your platform image repository prefix and merge into `values.yaml` either manually or by placing [merge_yaml.py](#merge_yaml) in your astro-platform project-directory and running `python merge_yaml.py private-platform-registry-snippet.yaml values.yaml`.

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

For example, if your custom platform image registry prefix was `012345678910.dkr.ecr.us-east-1.amazonaws.com/myrepo/astronomer`, your configuration would look like the following:

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

### Configure authentication to a custom platform registry

Astronomer Software platform images are usually hosted in internal repositories that do not require configuration. If your repository requires you pass an image credential:

1. Log in to the registry and follow the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#log-in-to-docker-hub) to produce a `/.docker/config.json` file.
   
2. Run the following command to create an image pull secret named `platform-regcred` in the Astronomer Software platform namespace:

    ```sh
    kubectl -n <astronomer platform namespace> create secret generic platform-regcred \
    --from-file=.dockerconfigjson=<path/to/.docker/config.json> \
    --type=kubernetes.io/dockerconfigjson
    ```

3. Set `global.privateRegistry.secretName` in `values.yaml` to `platform-regcred`. For example:

    ```yaml
    global:
      privateRegistry:
        secretName: platform-regcred
    ```

## Step 17: Determine which version of Astronomer Software to install {#determine-version-of-astronomer-software}

Astronomer recommends new Astronomer Software installations use the most recent version available in either the Stable or Long Term Support (LTS) release-channel. Keep this version number available for the following steps.

See Astronomer Software's [lifecycle policy](release-lifecycle-policy) and [release notes](version-compatibility-reference) for more information.

## Step 18: Fetch Airflow Helm charts {#fetch-airflow-helm-charts}

If you have internet access to `https://helm.astronomer.io`, run the following command on the machine where you want to install Astronomer Software:

```sh
helm repo add astronomer https://helm.astronomer.io/
helm repo update
```

If you don't have internet access to `https://helm.astronomer.io`, download the Astronomer Software Platform Helm chart file corresponding to the version of Astronomer Software you are installing or upgrading to from `https://helm.astronomer.io/astronomer-<version number>.tgz`. For example, for Astronomer Software v0.34.1 you would download `https://helm.astronomer.io/astronomer-0.34.1.tgz`. This file does not need to uploaded to an internal chart repository.

## Step 19: Create and customize upgrade.sh {#create-and-customize-upgradesh}

Create a file named `upgrade.sh` in your [platform-deployment project-directory](#platform-deployment-project-directory) containing the following script. Specify the following values at the beginning of the script:

- `CHART_VERSION`: Your Astronomer Software version, including patch and a `v` prefix. For example, `v0.34.1`.
- `RELEASE_NAME`: Your Helm release name. `astronomer` is strongly recommended.
- `NAMESPACE`: The namespace to install platform components into. `astronomer` is strongly recommended.
- `CHART_NAME`: Set to `astronomer/astronomer` if fetching platform images from the internet. Otherwise, specify the filename if you're installing from a file (for example `astronomer-0.34.1.tgz`).

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

The images and tags that are required for your Software installation depend on the version of Astronomer you want to install. To gather a list of exact images and tags required for your Astronomer version:

1. Configure your current session by setting the following environment variables locally:
  - `CHART_VERSION` - Your Astronomer Software version, including patch and a `v` prefix. For example, `v0.34.1`.
  - `CHART_NAME` - Set to `astronomer/astronomer` if fetching platform images from the internet. Otherwise, specify the filename if you're installing from a file (for example `astronomer-0.34.1.tgz`).

    ```bash
    CHART_VERSION=<v-prefixed version of the Astronomer Software platform chart>        
    CHART_NAME=<chart name>
    ```

2. Run the following command to template the Astronomer Helm chart and fetch all of its rendered image tags:
 
    ```bash
    helm template --version $CHART_VERSION $CHART_NAME --set global.dagOnlyDeployment.enabled=True --set global.loggingSidecar.enabled=True --set global.postgresqlEnabled=True --set global.authSidecar.enabled=True --set global.baseDomain=ignored | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq                           
    ```
    
    This command sets all possible Helm values that could impact which images are required for your installation. By fetching all images now, you save time by eliminating the risk of missing an image. 

4. Run the following command to template the Airflow Helm chart and fetch its rendered image tags:

    ```sh
    helm template --version $CHART_VERSION $CHART_NAME --set airflow.postgresql.enabled=false --set airflow.pgbouncer.enabled=true --set airflow.statsd.enabled=true --set airflow.executor=CeleryExecutor | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq
    ```

5. Copy these images to the container registry using the naming scheme you configured [when you set up a custom image registry](#use-a-custom-image-repository-for-platform-images).

:::tip

You can pass `-f/--values values.yaml` to `helm template` to only show images that apply to your specific configuration.

:::

## Step 21: Fetch Airflow/Astro Runtime updates {#fetch-airflow-updates}

By default, Astronomer checks for Airflow/Astro Runtime updates once a day at midnight by querying `https://updates.astronomer.io/astronomer-runtime`, which returns a JSON file with details about the latest available Astro Runtime versions. However, this URL is not accessible in an airgapped environment. There are several options for making these updates accessible in an airgapped environment:

- You can download the JSON and host it in a location that's accessible within your airgapped environment, for example:
    - AWS S3
    - Git
    - Nginx (example below)
- You can disable the update checks (not advised)

This setup assumes that the updates JSON will be manually downloaded and added to your environment. For guidance on how to automate this process, reach out to your Astronomer contact.

### Exposing Airflow updates using an Nginx endpoint

This procedure provides an example implementation for how to host the Airflow updates JSON files in your airgapped environment and then access them using an Nginx endpoint. Depending on your organization's platform and use cases, your own installation might vary from this setup.

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

    The updates JSON will be accessible by the service name from Pods in the Kubernetes cluster via `http://astronomer-releases.astronomer.svc.cluster.local/astronomer-certified.json`.

To validate if the updates JSON is accessible, you have several options:

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

After you have made the updates JSON accessible within your premises, you must configure `values.yaml` to fetch updates from the custom URL:

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

## Step 22: (OpenShift only) Apply OpenShift-specific configuration {#openshift-configuration}

If you're not installing Astronomer Software into an OpenShift Kubernetes cluster, skip this step.

Add the following values into `values.yaml`. You can do this manually or by placing the configuration as a new file, as well as [merge_yaml.py](#merge-yaml) in your project directory and running `python merge_yaml.py openshift.yaml values.yaml`.

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

Astronomer Software on OpenShift is only supported when using [a third-party ingress-controller](#elect-to-use-a-third-party-ingress-controller) and using the [logging sidecar](#configure-sidecar-logging) feature of Astronomer Software. The above configuration enables both of these items.

## Step 23: (Optional) Limit Astronomer to a namespace pool {#configure-namespace-pools}

By default, Astronomer Software automatically creates namespaces for each new Airflow Deployment.

You can restrict the Airflow management components of Astronomer Software to a list of predefined namespaces and configure it to operate without a ClusterRole by following the instructions in [Configure a Kubernetes namespace pool for Astronomer Software](namespace-pools.md) and setting `global.clusterRoles` to `false`. 

## Step 24: (Optional) Enable sidecar logging {#configure-sidecar-logging}

Running a logging sidecar to export Airflow task logs is essential for running Astronomer Software in a multi-tenant cluster.

By default, Astronomer Software creates a privileged DaemonSet to aggregate logs from Airflow components for viewing from within Airflow and the Astronomer Software UI.

You can replace this privileged Daemonset with unprivileged logging sidecars by following instructions in [Export logs using container sidecars](export-task-logs.md#export-logs-using-container-sidecars).

## Step 25: (Optional) Integrate an external identity provider {#integrate-an-external-identity-provider}

Astronomer Software includes integrations for several of the most popular OAUTH2 identity providers (IdPs), such as Okta and Microsoft Entra ID. Configuring an external IdP allows you to automatically provision and manage users in accordance with your organization's security requirements. See [Integrate an auth system](integrate-auth-system.md) to configure the identity provider of your choice in your `values.yaml` file. 

## Step 26: Create the load balancer {#creating-the-load-balancer}

Skip this step if you're using a third-party ingress controller or provisioning domain names for ingress objects using external DNS.

To install and function, Astronomer Software platform components require DNS entries to point to a load balancer associated with your ingress controller.

Perform a preliminary install of Astronomer Software to trigger your ingress controller to create the load balancer. This installation intentionally times out after 30 seconds, but it causes the ingress controller to still create the load balancer.

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

- `CHART_VERSION`: Your Astronomer Software version, including patch and a `v` prefix. For example, `v0.34.1`.
- `RELEASE_NAME`: Your Helm release name. `astronomer` is strongly recommended.
- `NAMESPACE`: The namespace to install platform components into. `astronomer` is strongly recommended.
- `CHART_NAME`: Set to `astronomer/astronomer` if fetching platform images from the internet. Otherwise, specify the filename, if you're installing from a file. For example `astronomer-0.34.1.tgz`.
  
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

Run `kubectl -n <astronomer platformm namespace> get service -l component=ingress-controller` and verify that a `service-type LoadBalancer` resource was created and that it received an External IP in a range that is accessible to your end-users, but **not** accessible to the general internet. For example:


```shell
$kubectl -n astronomer get service -l component=ingress-controller
NAME                       TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
astronomer-nginx           LoadBalancer   172.30.239.161   10.42.42.17     80:32697/TCP,443:30727/TCP   39m
astronomer-nginx-metrics   ClusterIP      172.30.245.154   <none>          10254/TCP                    39m
```

If you uninstall and re-install the Astronomer Software platform chart, the ingress controller almost always receives a new IP address, which requires updating the DNS entries.

In lower environments, you can set `nginx.loadBalancerIP` in `values.yaml` to the External-IP address:

```
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: "10.42.42.17"
```

This option allows the cluster to request the same Load Balancer IP at creation time. Rebuilds immediately following teardowns can almost always receive the same IP address, but issuance is not guaranteed and installations will fail if the IP address has been assigned elsewhere, or is otherwise not available. Therefore, this option should not be used in higher environments unless you have taken special measures to guarantee the same IP address is reissued.

## Step 27: Configure DNS for the integrated ingress controller {#integrated-ingress-controller-dns-configuration}

If you're using a third-party ingress controller, you can skip this step.

The Astronomer load balancer routes incoming traffic to your NGINX ingress controller. After you install Astronomer Software, the load balancer will spin up in your cloud provider account.

Run `$ kubectl get svc -n <astronomer platform namespace>`to view your load balancer's CNAME, located in the `EXTERNAL-IP` column for the `astronomer-nginx` service and look similar to the following:

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

Astronomer Software requires the following domain-names be registered and resolvable within the Kubernetes cluster and to Astronomer Software users:

- `app.<base-domain>` (required)
- `deployments.<base-domain>` (required)
- `houston.<base-domain>` (required)
- `prometheus.<base-domain>` (required)
- `grafana.<base-domain>` (required if using Astronomer Software's integrated grafana)
- `kibana.<base-domain>` (required if not using external elasticsearch)
- `registry.<base-domain>` (required if using Astronomer Software's integrated container-registry)
- `alertmanager.<base-domain>` (required if using Astronomer Software's integrated Alert Manager)
- `<base-domain>` (optional but recommended, provides a vanity re-direct to `app.<base-domain>`)
- `install.<base-domain>` (optional)

## Step 28: Install Astronomer Software using Helm {#install-astronomer-using-helm}

Install the Astronomer Software Helm chart using `upgrade.sh`, which is recommended for your first install, or directly from Helm.

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

## Step 29: Verify Pods creation {#verify-pods}

To verify all pods are up and running, run:

```sh
kubectl get pods --namespace <astronomer-platform-namespace>
```

All pods should be in Running status. For example, 

```command
$ kubectl get pods --namespace astronomer

NAME                                                       READY   STATUS              RESTARTS   AGE
astronomer-alertmanager-0                                  1/1     Running             0          24m
astronomer-astro-ui-7f94c9bbcc-7xntd                       1/1     Running             0          24m
astronomer-astro-ui-7f94c9bbcc-lkn5b                       1/1     Running             0          24m
<snip>
```

If all pods are not in running status, check the [guide on debugging your installation](debug-install.md) or contact [Astronomer support](https://support.astronomer.io) for additional configuration assistance.

## Step 30: Verify you can access the Software UI {#verify-software-ui}

Visit `https://app.<base-domain>` in your web-browser to view Astronomer Software's web interface.

Congratulations, you have configured and installed an Astronomer Software platform instance - your new Airflow control plane.

From the Astronomer Software UI, you'll be able to both invite and manage users as well as create and monitor Airflow Deployments on the platform.

## Additional information

The following topics include optional information about one or multiple topics in the installation guide.

### Merge configurations with `merge_yaml.py` {#merge-yaml}

When merging YAML configurations into `values.yaml`, you can merge manually or with a tool of your choosing.

You can use the following`merge_yaml.py` script to merge YAML excerpts into `values.yaml` automatically. This script requires both Python and the `ruamel.yaml` package, which you can install using `pip install ruamel.yaml`.
To run the program, ensure that `merge_yaml.py`, `values.yaml`, and the `yaml` file that contains the configuration you want to add are all in your project directory. Then, run:

```sh
python merge_yaml.py values-to-merge.yaml values.yaml
```

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
                                       
### Disable outbound email 

You can configure Astronomer Software to not send outbound email.

:::info

Setting `astronomer.houston.config.publicSignup: true` with `astronomer.houston.config.email.enabled: false` is only secure when all non-OIDC authentication backends are explicitly disabled and the OIDC provider provides sufficient user validation to prevent untrusted users from accessing Astronomer Software.

:::

To disable email transmission and email verision of users attempting to access the platform:

1. In your `values.yaml` file, set `astronomer.houston.config.email.enabled` to `false`.
2. Set `astronomer.houston.config.publicSignups` to `true`.
3. Remove the `EMAIL__SMTP_URL` list-item from `astronomer.houston.secret`.

### Configure Astronomer Software to trust private certificate authorities (CAs) {#configure-private-cas}

1. Store the CA's root public certificate to an [Opaque Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types) in the Astronomer namespace with a descriptive name, such as `private-root-ca`, by running the following command.

    :::tip
    
    Before you run this command, keep the following in mind:
    
     - The root certificate you specify should be the certificate of the authority that signed the Astronomer certificate. This is not the certificate associated with Astronomer or any other service.
    - The name of the secret file must be `cert.pem` for your certificate to be trusted properly.
    - The file must contain only a single certificate, it can't be a certificate bundle.
    
    :::


    ```sh
    kubectl -n astronomer create secret generic private-root-ca --from-file=cert.pem=./private-root-ca.pem
    ```



2. Add `<secret name>` to the list of secret names contained in `global.privateCaCerts` in `values.yaml`:
  
    ```yaml
    astronomer:
      privateCaCerts:
      - private-root-ca
    ```

### Add trusted certificate authorities (CAs) to Docker Desktop {#configure-desktop-container-solution-extra-cas}

If your users will deploy images to a container registry, including the integrated container registry, that uses a TLS certificate signed by a private CA, you need to configure Docker Desktop to trust the CA's public certificate. 

Obtain a copy of the CA's public certificate in pem format and place it in `/etc/docker/certs.d`:

```sh
mkdir -p /etc/docker/certs.d
cp privateCA.pem /etc/docker/certs.d/
```


