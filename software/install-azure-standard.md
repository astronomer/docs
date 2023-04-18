---
sidebar_label: 'Azure'
title: 'Install Astronomer Software on Azure AKS'
id: install-azure
description: Install Astronomer Software on Azure Kubernetes Service (AKS).
sidebar_custom_props: { icon: 'img/azure.png' }
---

Install Astronomer Software on Azure to deploy and scale [Apache Airflow](https://airflow.apache.org/) on a [Microsoft Azure Kubernetes Service](https://azure.microsoft.com/en-us/services/kubernetes-service/) (AKS) cluster.

## Prerequisites

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
* [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* A compatible version of Kubernetes and PostgreSQL as described in Astronomer's [Version compatibility reference](version-compatibility-reference.md)
* [Helm (minimum v3.6)](https://helm.sh/docs/intro/install)
* SMTP service and credentials. For example, Mailgun or Sendgrid.
* Permission to create and modify resources on AKS
* Permission to generate a certificate (not self-signed) that covers a defined set of subdomains
* PostgreSQL superuser permissions
* If your organization uses Azure Database for PostgreSQL as the database backend, you need to enable the `pg_trgm` extension using the Azure portal or the Azure CLI before you install Astronomer Software. If you don't enable the `pg_trgm` extension, the install will fail. For more information about enabling the `pg_trgm` extension, see [PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions).

:::caution

Astronomer Software is not compatible with Azure Single Server.

:::

## Step 1: Choose a base domain

All Astronomer services will be tied to a base domain of your choice, under which you will need the ability to add and edit DNS records.

Once created, your Astronomer base domain will be linked to a variety of sub-services that your users will access in a browser to manage, monitor and run Airflow on the platform.

For the base domain `astro.mydomain.com`, for example, here are some corresponding URLs that your users would be able to reach:

* Software UI: `app.astro.mydomain.com`
* Airflow Deployments: `deployments.astro.mydomain.com/uniquely-generated-airflow-name/airflow`
* Grafana Dashboard: `grafana.astro.mydomain.com`
* Kibana Dashboard: `kibana.astro.mydomain.com`

For the full list of subdomains, see Step 4.

## Step 2: Configure Azure for Astronomer Deployment

The steps below will walk you through how to:

- Create an Azure Resource Group
- Create an AKS Cluster
- Authenticate with your AKS Cluster

You can view Microsoft Azure's Web Portal at https://portal.azure.com/.

> Note: Each version of Astronomer Software is compatible with only a particular set of Kubernetes versions. For more information, refer to Astronomer's [Version compatibility reference](version-compatibility-reference.md).

### Create an Azure resource group

A resource group is a collection of related resources for an Azure solution. Your AKS cluster will reside in the resource group you create. Learn more about resource groups [here](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview#resource-groups).

Login to your Azure account with the `az` CLI:

```
az login
```

Your active Azure subscriptions will print to your terminal.  Set your preferred Azure subscription:

```
az account set --subscription <subscription_id>
```

Confirm your preferred subscription is set:

```
az account show
```

Create a resource group:
```
az group create --location <location> --name <my_resource_group>
```
> **Note:** For a list of available locations, run `$ az account list-locations`.

### Create an AKS cluster

Once you've created an Azure Resource Group, you can create an AKS cluster using the Azure CLI, Azure PowerShell, or Azure Portal. For instructions, see [Microsoft documentation](https://docs.microsoft.com/en-us/azure/aks/).
You can create a cluster with any machine type, but Astronomer recommends using larger nodes and not smaller nodes.

Verify your Kubernetes version is supported by Astronomer Software:
```
az aks get-versions --location <your-region> --output table
```

The Kubernetes version returned must be supported by Astronomer Software. See [Version compatibility reference](version-compatibility-reference.md).

Create and autoscale your Kubernetes cluster:
```
az aks create --name <name_of_cluster> --resource-group <your_resource_group> --kubernetes-version <X.X.X> --node-vm-size Standard_D8s_v3 --node-count 3 --enable-cluster-autoscaler --min-count 3 --max-count 10
```

You may need to increase your resource quota in order to provision these nodes.

> **Note:** If you work with multiple Kubernetes environments, `kubectx` is an incredibly useful tool for quickly switching between Kubernetes clusters. Learn more [here](https://github.com/ahmetb/kubectx).

### Authenticate with your AKS cluster

Run the following command to set your AKS cluster as current context in your kubeconfig. This will configure `kubectl` to point to your new AKS cluster:

```
az aks get-credentials --resource-group <my_resource_group> --name <my_cluster_name>
```

## Step 3: Create a Kubernetes namespace

Create a [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) called `astronomer` to host the core Astronomer platform:

```sh
kubectl create namespace astronomer
```

Once Astronomer is running, each Airflow Deployment that you create will have its own isolated namespace.

## Step 4: Configure TLS

Astronomer recommends running Astronomer Software on a dedicated domain (`BASEDOMAIN`) or subdomain (`astro.BASEDOMAIN`).

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

* **Option 1:** Obtain a TLS certificate from Let's Encrypt. Astronomer recommends this option for smaller organizations where your DNS administrator and Kubernetes cluster administrator are either the same person or on the same team.
* **Option 2:** Request a TLS certificate from your organization's security team. Astronomer recommends this option for large organizations with their own  protocols for generating TLS certificates.

> **Note:** Private CAs support on Azure is only available for clusters running containerd 1.5+, which is available on Kubernetes 1.22+.

### Option 1: Create TLS certificates using Let's Encrypt

[Let's Encrypt](https://letsencrypt.org/) is a free and secure certificate authority (CA) service that provides TLS certificates that renew automatically every 90 days. Use this option if you are configuring Astronomer for a smaller organization without a dedicated security team.

To set up TLS certificates this way, follow the guidelines in [Automatically Renew TLS Certificates Using Let's Encrypt](renew-tls-cert.md#automatically-renew-tls-certificates-using-lets-encrypt). Make note of the certificate you create in this setup for Step 5.

### Option 2: Request a TLS certificate from your security team

If you're installing Astronomer for a large organization, you'll need to request a TLS certificate and private key from your enterprise security team. This certificate needs to be valid for the `BASEDOMAIN` your organization uses for Astronomer, as well as the subdomains listed at the beginning of Step 4. You should be given two `.pem` files:

- One for your encrypted certificate
- One for your private key

To confirm that your enterprise security team generated the correct certificate, run the following command using the `openssl` CLI:

```sh
openssl x509 -in  <your-certificate-filepath> -text -noout
```

This command will generate a report. If the `X509v3 Subject Alternative Name` section of this report includes either a single `*.BASEDOMAIN` wildcard domain or the subdomains listed at the beginning of Step 4, then the certificate creation was successful.

Depending on your organization, you may receive either a globally trusted certificate or a certificate from a private CA. The certificate from your private CA may include a domain certificate, a root certificate, and/or intermediate certificates, all of which need to be in proper certificate order. To verify certificate order, follow the guidelines below.

#### Confirm certificate chain order

If your organization is using a private certificate authority, you'll need to confirm that your certificate chain is ordered correctly. To determine your certificate chain order, run the following command using the `openssl` CLI:

```sh
openssl crl2pkcs7 -nocrl -certfile <your-certificate-filepath> | openssl pkcs7 -print_certs -noout
```

The command generates a report of all certificates. Verify the order of the certificates is as follows:

- Domain
- Intermediate (optional)
- Root

If the certificate order is correct, proceed to step 5.

## Step 5: Create a Kubernetes TLS Secret

If you received a globally trusted certificate, such as one generated by Let's Encrypt, simply run the following command and proceed to Step 6:

```sh
kubectl create secret tls astronomer-tls --cert <your-certificate-filepath> --key <your-private-key-filepath> -n astronomer
```

If you received a certificate from a private CA, follow these steps instead:

1. Add the root certificate provided by your security team to an [Opaque Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types) in the Astronomer namespace by running the following command:

    ```sh
    kubectl create secret generic private-root-ca --from-file=cert.pem=./<your-certificate-filepath> -n astronomer
    ```

    > **Note:** The root certificate which you specify here should be the certificate of the authority that signed the Astronomer certificate, rather than the Astronomer certificate itself. This is the same certificate you need to install with all clients to get them to trust your services.

    > **Note:** The name of the secret file must be `cert.pem` for your certificate to be trusted properly.

2. Note the value of `private-root-ca` for when you configure your Helm chart in Step 8. You'll need to additionally specify the `privateCaCerts` key-value pair with this value for that step.

## Step 6: Configure your SMTP URI

An SMTP service is required for sending and accepting email invites from Astronomer. If you're running Astronomer Software with `publicSignups` disabled (which is the default), you'll need to configure SMTP as a way for your users to receive and accept invites to the platform through an email invitation. To integrate your SMTP service with Astronomer, fetch your SMTP service's URI and store it in a Kubernetes secret:

```sh
kubectl create secret generic astronomer-smtp --from-literal connection="smtp://USERNAME:PASSWORD@HOST/?requireTLS=true" -n astronomer
```

In general, an SMTP URI will take the following form:

```text
smtps://USERNAME:PASSWORD@HOST/?pool=true
```

The following table contains examples of what the URI will look like for some of the most popular SMTP services:

| Provider          | Example SMTP URL                                                                               |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| AWS SES           | `smtp://AWS_SMTP_Username:AWS_SMTP_Password@email-smtp.us-east-1.amazonaws.com/?requireTLS=true` |
| SendGrid          | `smtps://apikey:SG.sometoken@smtp.sendgrid.net:465/?pool=true`                                   |
| Mailgun           | `smtps://xyz%40example.com:password@smtp.mailgun.org/?pool=true`                               |
| Office365         | `smtp://xyz%40example.com:password@smtp.office365.com:587/?requireTLS=true`                   |
| Custom SMTP-relay | `smtp://smtp-relay.example.com:25/?ignoreTLS=true`                                      |

If your SMTP provider is not listed, refer to the provider's documentation for information on creating an SMTP URI.

> **Note:** If there are `/` or other escape characters in your username or password, you may need to [URL encode](https://www.urlencoder.org/) those characters.

## Step 7: Configure the database

If you're connecting to an external database, you will need to create a secret named `astronomer-bootstrap` to hold your database connection string:

```sh
kubectl create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://USERNAME:$PASSWORD@host:5432" \
  --namespace astronomer
```

> **Note:** You must URL encode any special characters in your Postgres password.

A few additional configuration notes:
- If you provision an external database, `postgresqlEnabled` should be set to `false` in Step 8.
- If your organization uses Azure Database for PostgreSQL as the database backend, you need to enable the `pg_trgm` extension using the Azure portal or the Azure CLI before you install Astronomer Software. If you don't enable the `pg_trgm` extension, the install will fail. For more information about enabling the `pg_trgm` extension, see [PostgreSQL extensions in Azure Database for PostgreSQL - Flexible Server](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions).
- If you provision Azure Database for PostgreSQL - Flexible Server, it enforces TLS/SSL and requires that you set `sslmode` to `prefer` in your `config.yaml`.

## Step 8: Configure Your Helm chart

:::info 

To use a third-party ingress controller for Astronomer, see [Third-Party Ingress Controllers](third-party-ingress-controllers.md).

:::

As a next step, create a file named `config.yaml` in an empty directory.

For context, this `config.yaml` file will assume a set of default values for our platform that specify everything from user role definitions to the Airflow images you want to support. As you grow with Astronomer and want to customize the platform to better suit your team and use case, your `config.yaml` file is the best place to do so.

In the newly created file, copy the example below and replace `baseDomain`, `private-root-ca`, `/etc/docker/certs.d`, and `astronomer.houston.secret` with your own values. For more example configuration files, see the [Astronomer GitHub](https://github.com/astronomer/astronomer/tree/master/configs).

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
  postgresqlEnabled: false # Keep True if deploying a database on your AKS cluster.

# SSL support for using SSL connections to encrypt client/server communication between database and Astronomer platform. Enable SSL if provisioning Azure Database for PostgreSQL - Flexible Server as it enforces SSL. Change the setting with respect to the database provisioned.
  ssl:
    enabled: true
    mode: "prefer"

# Settings for database deployed on AKS cluster.
# postgresql:
#  replication:
#    enabled: true
#    slaveReplicas: 2
#    synchronousCommit: "on"
#    numSynchronousReplicas: 1

#################################
### Nginx configuration
#################################
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: ~
  # Dict of arbitrary annotations to add to the nginx ingress. For full configuration options, see https://docs.nginx.com/nginx-ingress-controller/configuration/ingress-resources/advanced-configuration-with-annotations/
  ingressAnnotations:
    # required for azure load balancer post Kubernetes 1.22
    service.beta.kubernetes.io/azure-load-balancer-health-probe-request-path: "/healthz"

astronomer:
  houston:
    config:
      publicSignups: false # Users need to be invited to have access to Astronomer. Set to true otherwise
      emailConfirmation: true # Users get an email verification before accessing Astronomer
      deployments:
        manualReleaseNames: true # Allows you to set your release names
      email:
        enabled: true
        reply: "noreply@astronomer.io" # Emails will be sent from this address
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

>> **Note:** If there are `/` or other escape characters in your username or password, you may need to [URL encode](https://www.urlencoder.org/) those characters.

These are the minimum values you need to configure for installing Astronomer. For information on additional configuration, read [What's Next](install-azure-standard.md#whats-next).

:::info

If you are installing Astronomer in an airgapped environment without access to the public internet, complete all of the setup in [Install in an Airgapped Environment](install-airgapped.md) and then skip directly to Step 10 in this document.

:::

## Step 9: Install Astronomer

<!--- Version-specific -->

Now that you have an AKS cluster set up and your `config.yaml` defined, you're ready to deploy all components of our platform.

First, run:

```
helm repo add astronomer https://helm.astronomer.io/
```

Then, run:

```sh
helm repo update
```

This ensures that you pull the latest image from the Astronomer Helm repository. Now, run:

```sh
helm install -f config.yaml --version=0.31 --namespace=astronomer <your-platform-release-name> astronomer/astronomer
```

This command installs the most recent patch version of Astronomer Software. To install a different patch version, add the `--version=` flag and use the format `0.31.x`.  For example, to install Astronomer Software v0.31.0, you specify `--version=0.31.0`. For more information about the available patch versions, see the [Software Release Notes](release-notes.md).

When you're defining `<your-platform-release-name>`, Astronomer recommends limiting the name to 12 characters to avoid operational issues.

After you run the previous commands, a set of Kubernetes pods are generated in your namespace. These pods power the individual services required to run the Astronomer platform, including the Software UI and Houston API.

### Alternative ArgoCD installation

You can install Astronomer with [ArgoCD](https://argo-cd.readthedocs.io/en/stable/), which is an open source continuous delivery tool for Kubernetes, as an alternative to using `helm install`. 

Because ArgoCD doesn't support sync wave dependencies for [app of apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern) structures, installing Astronomer requires some additional steps compared to the standard ArgoCD workflow:

1. Under the `global` section of your `config.yaml` file, add `enableArgoCDAnnotation: true`.
   
2. Create a new ArgoCD app. When creating the app, configure the following:

    - **Path**: The filepath of your `config.yaml` file
    - **Namespace**: The namespace you want to use for Astronomer
    - **Cluster**: The Kubernetes cluster in which you're installing Astronomer 
    - **Repository URL**: `https://helm.astronomer.io`

3. Sync the ArgoCD app with every component of the Astronomer platform selected. See [Sync (Deploy) the Application](https://argo-cd.readthedocs.io/en/stable/getting_started/#7-sync-deploy-the-application).
   
4. Stop the sync when you see that `astronomer-houston-db-migrations` has completed in the Argo UI. 
   
5. Sync the application a second time, but this time clear `astronomer-alertmanager` in the Argo UI while keeping all other components selected. Wait for this sync to finish completely.
   
6. Sync the ArgoCD app a third time with all Astronomer platform components selected.


## Step 10: Verify all pods are up

To verify all pods are up and running, run:

```
kubectl get pods --namespace astronomer
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

Now that you've successfully installed Astronomer, a new Load Balancer will have spun up in your Azure account. This Load Balancer routes incoming traffic to our NGINX ingress controller.

Run `kubectl get svc -n astronomer` to view your Load Balancer's External IP Address, located under the `EXTERNAL-IP` column for the `astronomer-nginx` service.

```
$ kubectl get svc -n astronomer
NAME                                          TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)                                      AGE
astronomer-alertmanager                       ClusterIP      10.0.184.29    <none>          9093/TCP                                     6m48s
astronomer-astro-ui                           ClusterIP      10.0.107.212   <none>          8080/TCP                                     6m48s
astronomer-cli-install                        ClusterIP      10.0.181.211   <none>          80/TCP                                       6m48s
astronomer-commander                          ClusterIP      10.0.201.246   <none>          8880/TCP,50051/TCP                           6m48s
astronomer-elasticsearch                      ClusterIP      10.0.47.56     <none>          9200/TCP,9300/TCP                            6m48s
astronomer-elasticsearch-exporter             ClusterIP      10.0.130.79    <none>          9108/TCP                                     6m48s
astronomer-elasticsearch-headless-discovery   ClusterIP      None           <none>          9300/TCP                                     6m48s
astronomer-elasticsearch-nginx                ClusterIP      10.0.218.244   <none>          9200/TCP                                     6m48s
astronomer-grafana                            ClusterIP      10.0.42.156    <none>          3000/TCP                                     6m48s
astronomer-houston                            ClusterIP      10.0.57.247    <none>          8871/TCP                                     6m48s
astronomer-kibana                             ClusterIP      10.0.15.226    <none>          5601/TCP                                     6m48s
astronomer-kube-state                         ClusterIP      10.0.132.0     <none>          8080/TCP,8081/TCP                            6m48s
astronomer-kubed                              ClusterIP      10.0.254.39    <none>          443/TCP                                      6m48s
astronomer-nginx                              LoadBalancer   10.0.146.24    20.185.14.181   80:30318/TCP,443:31515/TCP,10254:32454/TCP   6m48s
astronomer-nginx-default-backend              ClusterIP      10.0.132.182   <none>          8080/TCP                                     6m48s
astronomer-postgresql                         ClusterIP      10.0.0.252     <none>          5432/TCP                                     6m48s
astronomer-postgresql-headless                ClusterIP      None           <none>          5432/TCP                                     6m48s
astronomer-prometheus                         ClusterIP      10.0.128.170   <none>          9090/TCP                                     6m48s
astronomer-prometheus-blackbox-exporter       ClusterIP      10.0.125.142   <none>          9115/TCP                                     6m48s
astronomer-prometheus-node-exporter           ClusterIP      10.0.2.116     <none>          9100/TCP                                     6m48s
astronomer-registry                           ClusterIP      10.0.154.62    <none>          5000/TCP                                     6m48s
```

You will need to create a new A record through your DNS provider using the external IP address listed above. You can create a single wildcard A record such as `*.astro.mydomain.com`, or alternatively create individual A records for the following routes:

```
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

## Step 12: Verify you can access the Software UI

Go to `app.BASEDOMAIN` to see the Software UI.

Consider this your new Airflow control plane. From the Software UI, you'll be able to both invite and manage users as well as create and monitor Airflow Deployments on the platform.

## Step 13: Verify your TLS setup

To check if your TLS certificates were accepted, log in to the Software UI. Then, go to `app.BASEDOMAIN/token` and run:

```
curl -v -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"
```

Verify that this output matches with that of the following command, which doesn't look for TLS:

```
curl -v -k -X POST https://houston.BASEDOMAIN/v1 -H "Authorization: Bearer <token>"
```

Next, to make sure the registry is accepted by Astronomer's local docker client, try authenticating to Astronomer with the Astro CLI:

```sh
astro auth login <your-astronomer-base-domain>
```

If you can log in, then your Docker client trusts the registry. If Docker does not trust the Astronomer registry, run the following and restart Docker:

```
$ mkdir -p /etc/docker/certs.d
$ cp privateCA.pem /etc/docker/certs.d/
```

Finally, try running `$ astro deploy` on a test deployment. Create a deployment in the Software UI, then run:
```sh
$ mkdir demo
$ cd demo
$ astro dev init --use-astronomer-certified
$ astro deploy -f
```
Check the Airflow namespace. If pods are changing at all, then the Houston API trusts the registry.

If you have Airflow pods in the state "ImagePullBackoff", check the pod description. If you see an x509 error, ensure that you added the `privateCaCertsAddToHost` key-value pairs to your Helm chart. If you missed these during installation, follow the steps in [Apply a config change](apply-platform-config.md) to add them after installation.

## What's next

To help you make the most of Astronomer Software, Astronomer recommends reviewing the following topics:

* [Renew TLS Certificates on Astronomer Software](renew-tls-cert.md)
* [Integrating an Auth System](integrate-auth-system.md)
* [Configuring Platform Resources](configure-platform-resources.md)
* [Managing Users on Astronomer Software](manage-platform-users.md)

### Astronomer support team

If you have feedback or need help during the installation process, here are some recommended resources:

* [Community Forum](https://forum.astronomer.io): General Airflow + Astronomer FAQs
* [Astronomer Support Portal](https://support.astronomer.io/hc/en-us/): Platform or Airflow issues

For guidelines on contacting Astronomer Support, see [Submit a support request](support.md).
