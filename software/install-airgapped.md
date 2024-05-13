---
title: "Install Astronomer Software"
sidebar_label: "Install Astronomer Software"
description: "Install Astronomer Software in a multi-tenant, airgapped environment with all recommended security and networking configurations"
id: install-airgapped
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This guide describes the steps to install Astronomer Software, which allows you to deploy and scale any number of Apache Airflow deployments.

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

## Step 1: Choose a base domain

All Astronomer services will be tied to a base domain under which you will need the ability to add and edit DNS records.

Once created, your Astronomer base domain will be linked to a variety of sub-services that your users will access via the internet to manage, monitor, and run Airflow on the platform.

For the base domain `astro.mydomain.com`, for example, here are some corresponding URLs that your users would be able to reach:

- Software UI: `app.astro.mydomain.com`
- Airflow Deployments: `deployments.astro.mydomain.com/deployment-release-name/airflow`
- Grafana Dashboard: `grafana.astro.mydomain.com`
- Kibana Dashboard: `kibana.astro.mydomain.com`

Save your chosen base domain name for use in Step 6. For the full list of subdomains under the base domain, see Step 3.

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

Request a TLS certificate and private key from your enterprise security team. This certificate needs to be valid for the `BASEDOMAIN` your organization uses for Astronomer, as well as your subdomains. You should be given two `.pem` files:

- One for your encrypted certificate
- One for your private key

To confirm that your enterprise security team generated the correct certificate, run the following command using the `openssl` CLI:

```sh
openssl x509 -in  <your-certificate-filepath> -text -noout
```

This command will generate a report. If the `X509v3 Subject Alternative Name` section of this report includes either a single `*.BASEDOMAIN` wildcard domain or all subdomains, then the certificate creation was successful.

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

## Step 4: Create a Kubernetes TLS Secret

If you received a globally trusted certificate or created a self-signed certificate, create a Kubernetes TLS secret using the following command and then proceed to the next step:

```sh
kubectl -n <astronomer platform namespace>> create secret tls astronomer-tls --cert <fullchain-pem-filepath> --key <your-private-key-filepath>
```

E.g.
```
kubectl -n astronomer create secret tls astronomer-tls --cert fullchain.pem --key server_private_key.pem
```

If not using Astronomer's bundled ingress-controller, additionally annotate the secret and set `"astronomer.io/commander-sync` to `platform=<astronomer platform release name>`, e.g.:
```
kubectl -n <astronomer platfomr namespace> annotate secret astronomer-bootstrap "astronomer.io/commander-sync"="platform=astronomer"
```

## Step TBD: Configuring a Private Certificate Authority

If you received a certificate from a private CA, follow these steps instead:

1. Add the root certificate provided by your security team to an [Opaque Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types) in the Astronomer namespace by running the following command:

    ```sh
    kubectl create secret generic private-root-ca --from-file=cert.pem=./<your-certificate-filepath> -n astronomer
    ```

    > **Note:** The root certificate which you specify here should be the certificate of the authority that signed the Astronomer certificate, rather than the Astronomer certificate itself. This is the same certificate you need to install with all clients to get them to trust your services.

    > **Note:** The name of the secret file must be `cert.pem` for your certificate to be trusted properly.

2. Note the value of `private-root-ca` for when you configure your Helm chart in Step 8. You'll need to additionally specify the `privateCaCerts` key-value pair with this value for that step.

## Step 5: Configure Outbound SMTP Email


Astronomer Software requires the ability to send email to:
* notifying users of certain errors (e.g. users that try to deploy mis-matched Airflow image versions)
* sending and accepting email invites from Astronomer
* sending certain platform alerts (in the default configuration, configurable)

Astronomer Software sends all outbound email via SMTP.

::info

If evaluating Astronomer Software in an environment where outbound SMTP is not available, follow instructions in `Appendix: Configuring Astronomer Software To Not Send Outbound Email` and then skip the rest of this section.

::

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

## Step 6: Retrieve the Astronomer platform Helm chart

Starting in the next step, you might need to modify Astronomer's Helm chart to customize your Astronomer installation to your use case. Making changes to the Astronomer Helm chart is the primary method for customizing the Astronomer Software platform. 

To download a templated Helm chart for your installation, run the following command:

```bash
helm template --version <your-astronomer-version> astronomer/astronomer --set global.dagOnlyDeployment.enabled=True --set global.loggingSidecar.enabled=True --set global.postgresqlEnabled=True --set global.authSidecar.enabled=True --set global.baseDomain=<your-basedomain> | grep "image: " | sed -e 's/"//g' -e 's/image:[ ]//' -e 's/^ *//g' | sort | uniq                           
```

Save the chart in a file named `values.yaml`.

## Step 7: Configure the database

Astronomer requires a central Postgres database that acts as the backend for Astronomer's Houston API and will host individual metadata databases for all Airflow Deployments spun up on the platform.

:::info

If, while evaluating Astronomer Software, you need to create a temporary environment where Postgres is not available, locate the `global.postgresqlEnabled` option already present in your `values.yaml` and set it to `true` then skip the remainder of this step.

Setting `global.postgresqlEnabled` to `true` is an *unsupported* configuration and *must* not be used on any development, staging, or production environment.

:::


:::info

If using Azure Database for PostgreSQL or another Postgres instance that does not enable the `pg_trgm` by default, you *must* enable the `pg_trgm` extension prior to installing Astronomer Software. If `pg_trgm` is not enabled, the install will fail. `pg_tgrm` is enabled by default on Amazon RDS and Google CLoud SQL for PostgresQL. For instructions on enabling the `pg_trgm` extension for Azure Flexible Server, see [PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions).

:::

Create a Kubernetes Secret named `astronomer-bootstrap` that points to your database. You must URL encode any special characters in your Postgres password.

To create this secret, run the following command replacing the astronomer platform namespace, username, password, database hostname, and database port with their respective values (username and password must be url-encoded if they contain special-characters):

```bash
kubectl --namespace <astronomer platform namespace> create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://<url-encoded username>:<url-encoded password>@<database hostname>:<database port>"
```

e.g. For a username named `bob` with password `abc@abc` at hostname `some.host.internal`:
```bash
kubectl --namespace astronomer create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://bob:abc%40abc@some.host.internal:5432"
```

Additional requirements apply to the following databases:
- AWS RDS:
  * [t2 medium](https://aws.amazon.com/rds/instance-types/) is the minimum RDS instance size.
- Azure Flexible Server:
  * you must enable the `pg_trgm` extension as per the advisory earlier in this section
  * `global.ssl.sslmode` must be set to `prefer` in your `values.yaml` (set during Step 8, and already set if using the Azure on AKS config provided there).

## Step 8: Confirm the base configuration for your Helm chart

Your `values.yaml` file will store a set of values for Astronomer Software that specify everything from user role definitions to the Airflow images you want to support. You'll continually modify this file and apply it to your platform you grow with Astronomer Software and want to take advantage of new features.

Your `values.yaml` file should include the following configurations alongside the configurations you copied in Step 6. For more example configuration files, see the [Astronomer GitHub](https://github.com/astronomer/astronomer/tree/master/configs).


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
### Astronomer global configuration
#################################
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: astro.mydomain.com

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
### Astronomer global configuration
#################################
global:
  # Base domain for all subdomains exposed through ingress
  baseDomain: astro.mydomain.com

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
### Astronomer global configuration
#################################
global:
  # Enables default values for Azure installations
  azure:
    enabled: true

  # Base domain for all subdomains exposed through ingress
  baseDomain: astro.mydomain.com

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
  baseDomain: astro.mydomain.com

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

## Step 9: Configure a private Docker registry

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

## Step 10: Fetch images from Astronomer's Helm template

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

:::info

If you have already enabled or disabled Astronomer platform components in your `values.yaml`, you can pass `-f/--values values.yaml` to `helm template` to print a list specific to your `values.yaml` configuration.

:::

## Step 11: Add images to your values.yaml file

Regardless of whether you choose to mirror or manually pull/push images to your private registry, the returned images and/or tags must be made accessible within your network.

To make these images accessible to Astronomer, specify your organization's private registry in the `global` section of your `values.yaml` file like in the following example:

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

## Step 12: Fetch Airflow Helm charts

* If you have internet accces to `https://helm.astronomer.io` run the following command on the machine you will be installing Astronomer Software on:
```
helm repo add astronomer https://helm.astronomer.io/
helm repo update
```
* If you do not have internet access to `https://helm.astronomer.io` download the Astronomer Software Platform helm chart file corresponding to the version of Astronomer Software they are installing or upgrading to from `https://helm.astronomer.io/astronomer-<version number>.tgz`. 
  * e.g. if installing Astronomer Software v0.34.1 download `https://helm.astronomer.io/astronomer-0.34.1.tgz`.
  * This file does not need to uploaded to an internal chart-repository.


## Step 13: Fetch Airflow updates

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

## Step 14: Configure namespace pools

Dedicated namespace pools are strongly recommended for the security of any Astronomer Software installation. They allow you to grant Astronomer Software permissions at the namespace level and limit cluster-level permission.

See [Configure a Kubernetes namespace pool for Astronomer Software](namespace-pools.md) to learn how to configure pre-created namespaces in your `values.yaml` file. When you decide on a namespace pool implementation, apply the required changes to your cluster and `values.yaml` file. 

Do not apply the configuration to your cluster yet as described in the linked documentation - you'll be applying your complete platform configuration all at once later in this setup.

Most third-party ingress-controllers require the public certificate additionally be available in the namespace of the various airflow instances. If using a third-party ingress-controller, run the following command to mark the secret for automatic-replication into astronomer-managed Airflow namespaces, substituting both instances of `<astronomer platform namespace>` with the name of the Astronomer Software platform namespace:

Astronomer Software is its most secure when you supply a pre-existing ingress controller that meets your organization's strict security standards. Follow the steps in [Use a third-party ingress controller](third-party-ingress-controllers.md) to configure your `values.yaml` file to host your third-party ingress controller. 

Do not apply the configuration to your cluster yet as described in the linked documentation - you'll be applying your complete platform configuration all at once later in this setup.

## Step 16: Configure sidecar logging

Running a logging sidecar to export Airflow task logs is essential for running Astronomer Software in a multi-tenant cluster. See [Export logs using container sidecars](export-task-logs.md#export-logs-using-container-sidecars) to learn how to configure logging sidecars in your `values.yaml` file. 

Do not apply the configuration to your cluster yet as described in the linked documentation - you'll be applying your complete platform configuration all at once later in this setup.

## Step 17: Integrate an external identity provider

Astronomer Software includes integrations for several of the most popular identity providers (IdPs), such as Okta and Microsoft Entra ID. Configuring an external IdP allows you to automatically provision and manage users in accordance with your organization's security requirements. See [Integrate an auth system](integrate-auth-system.md) to configure the identity provider of your choice in your `config.yaml` file. 

Do not apply the configuration to your cluster yet as described in the linked documentation - you'll be applying your complete platform configuration all at once later in this setup.

## Step 18: Install Astronomer using Helm

Before completing this step, ensure that you made Astronomer's Docker images, Airflow Helm chart, and updates JSON accessible inside your network.

After this check, you can install the Astronomer Helm chart by running the following commands, making sure to replace `<your-image-tag>` with the version of Astronomer that you want to install:

```bash
curl -L https://github.com/astronomer/astronomer/archive/v<your-image-tag>.tar.gz -o astronomer.tgz

# Alternatively, use helm pull to pull the latest version of Astronomer
helm pull astronomer/astronomer

# ... If necessary, copy to a place where you can access Kubernetes ...
helm install astronomer -f values.yaml -n astronomer astronomer.tgz
```

## Step 19: Verify Pods are up

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

## Step 20: Configure DNS

The Astronomer load balancer routes incoming traffic to your NGINX ingress controller. After you install Astronomer Software, the load balancer will spin up in your cloud provider account.

Run `$ kubectl get svc -n astronomer` to view your load balancer's CNAME, located under the `EXTERNAL-IP` column for the `astronomer-nginx` service. It should look similar to the following:

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

## Step 21: Verify you can access the Software UI

Go to `app.BASEDOMAIN` to see the Software UI.

Consider this your new Airflow control plane. From the Software UI, you'll be able to both invite and manage users as well as create and monitor Airflow Deployments on the platform.

## Step 22: Verify your TLS setup

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

If you missed these steps during installation, follow the steps in [Apply a config change](apply-platform-config.md) to add them after installation. If you are using a base image such as CoreOS that does not permit values to be changed, or you otherwise can't modify `values.yaml`, contact [Astronomer support](https://support.astronomer.io) for additional configuration assistance.


## Appendix: Configuring Astronomer Software To Not Send Outbound Email

::info
Setting `astronomer.houston.config.publicSignups` to `true` is only secure when all non-OIDC authentication backends are explicitly disabled.
::

set `astronomer.houston.config.email.enabled` to `false`, remove the `EMAIL__SMTP_URL` list-item from `astronomer.houston.secret`, and 

 
