---
sidebar_label: 'AWS'
title: 'Install Astronomer Software on AWS EKS'
id: install-aws
description: Install Astronomer Software on Amazon Web Services (AWS).
sidebar_custom_props: { icon: 'img/aws.png' }
---

This guide describes the steps to install Astronomer Software on Amazon Web Services (AWS), which allows you to deploy and scale [Apache Airflow](https://airflow.apache.org/) within an AWS [Elastic Kubernetes Service](https://aws.amazon.com/eks/) (EKS) cluster.

## Prerequisites

To install Astronomer on EKS, you'll need access to the following tools and permissions:

* The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).
* A compatible version of Kubernetes and PostgreSQL as described in the Astronomer [Version Compatibility Reference](version-compatibility-reference.md).
* The [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
* The [OpenSSL CLI](https://www.openssl.org/docs/man1.0.2/man1/openssl.html)
* [Helm (minimum v3.6)](https://helm.sh/docs/intro/install).
* An SMTP service and credentials. For example, Mailgun or Sendgrid.
* Permission to create and modify resources on AWS.
* Permission to generate a certificate (not self-signed) that covers a defined set of subdomains.
* PostgreSQL superuser permissions.
* An AWS Load Balancer Controller for the IP target type is required for all private Network Load Balancers (NLBs). See [Installing the AWS Load Balancer Controller add-on](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html).  
* If you use Kubernetes version 1.23 or later, the [Amazon EBS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html).
* Optional. [`eksctl`](https://eksctl.io/) for creating and managing your Astronomer cluster on EKS.

## Step 1: Choose a base domain

All Astronomer services will be tied to a base domain of your choice, under which you will need the ability to add and edit DNS records.

Once created, your Astronomer base domain will be linked to a variety of sub-services that your users will access via the internet to manage, monitor and run Airflow on the platform.

For the base domain `astro.mydomain.com`, for example, here are some corresponding URLs that your users would be able to reach:

* Software UI: `app.astro.mydomain.com`
* Airflow Deployments: `deployments.astro.mydomain.com/deployment-release-name/airflow`
* Grafana Dashboard: `grafana.astro.mydomain.com`
* Kibana Dashboard: `kibana.astro.mydomain.com`

For the full list of subdomains, see Step 4.

## Step 2: Spin up the EKS control plane and a Kubernetes cluster

To proceed with the installation, you'll need to spin up an [EKS control plane](https://aws.amazon.com/eks/) as well as worker nodes in your Kubernetes cluster by following [this AWS guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html).

EKS is built off of Amazon's pre-existing EC2 service, so you can manage your Kubernetes nodes the same way you would manage your EC2 nodes.

As you follow the guide linked above, keep in mind:

* Each version of Astronomer Software is compatible with only a particular set of Kubernetes versions. For more information, see the Astronomer [Version Compatibility Reference](version-compatibility-reference.md).
* Astronomer recommends running the EKS control plane in a single security group. The worker nodes you spin up should have the same setup as the EKS control plane.
* All security and access settings needed for your worker nodes should be configured in your Cloud Formation template.
* Astronomer recommends configuring [Autoscaling](https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html) to automatically scale your resources up or down based on changing usage.
* If you create an EKS cluster from the UI, `kubectl` access will be limited to the user who created the cluster by default.
    * To give more users `kubectl` access, you'll have to do so manually.
    * [This post](https://web.archive.org/web/20190323035848/http://marcinkaszynski.com/2018/07/12/eks-auth.html) goes through how IAM plays with EKS.
* Expect to see each of your underlying nodes in the EC2 console.
    * The default Astronomer resource requests are ~11 CPUs and ~40GB of memory. Astronomer recommends using either six m5.xlarge or three m5.2xlarge [instances](https://aws.amazon.com/ec2/instance-types/) for your cluster. To modify Astronomer default resource requests, see step 8.

> **Note:** If you work with multiple Kubernetes environments, `kubectx` is an incredibly useful tool for quickly switching between Kubernetes clusters. Learn more [here](https://github.com/ahmetb/kubectx).

## Step 3: Create a namespace

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

To obtain a TLS certificate, complete one of the following setup options:

* **Option 1:** Obtain a TLS certificate from Let's Encrypt. Astronomer recommends this option for smaller organizations where the DNS administrator and Kubernetes cluster administrator are the same person or on the same team.
* **Option 2:** Request a TLS certificate from your organization's security team. Astronomer recommends this option for large organizations with their own protocols for generating TLS certificates.
* **Option 3:** Use the AWS Certificate Manager as the certificate provider.

### Option 1: Create TLS certificates using Let's Encrypt

[Let's Encrypt](https://letsencrypt.org/) is a free and secure certificate authority (CA) service that provides TLS certificates that renew automatically every 90 days. Use this option if you are configuring Astronomer for a smaller organization without a dedicated security team.

To set up TLS certificates this way, follow the guidelines in [Automatically Renew TLS Certificates Using Let's Encrypt](renew-tls-cert.md#automatically-renew-tls-certificates-using-lets-encrypt). Make note of the certificate you create in this setup for Step 5.

### Option 2: Request a TLS certificate from your security team

If you're installing Astronomer for a large organization, you'll need to request a TLS certificate and private key from your enterprise security team. This certificate needs to be valid for the `BASEDOMAIN` your organization uses for Astronomer, as well as the subdomains listed at the beginning of Step 4. You should be given two `.pem` files:

* One for your encrypted certificate
* One for your private key

To confirm that your enterprise security team generated the correct certificate, run the following command using the `openssl` CLI:

```sh
openssl x509 -in  <your-certificate-filepath> -text -noout
```

This command will generate a report. If the `X509v3 Subject Alternative Name` section of this report includes either a single `*.BASEDOMAIN` wildcard domain or the subdomains listed at the beginning of Step 4, then the certificate creation was successful.

Depending on your organization, you may receive either a globally trusted certificate or a certificate from a private CA. The certificate from your private CA may include a domain certificate, a root certificate, and/or intermediate certificates, all of which need to be in proper certificate order. To verify certificate order, follow the guidelines below.

### Option 3: Use the AWS Certificate Manager as the certificate provider

AWS Certificate Manager (ACM) terminates TLS at the Load Balancer level and does not encrypt the internal traffic inside the cluster. The ACM ingress controller requires an `astronomer-tls` secret with a certificate and private key to encrypt internal traffic. 

Because ACM relies on annotations attached to Kubernetes resources and does not issue certificates or private key files, you must complete one of the following options to create the `astronomer-tls` secret:
 
- Create a [self-signed certificate](self-signed-certificate.md). Self-signed certificates are ideal for privately hosted internal applications, as well as in development and testing environments. Avoid using self-signed certificates in installations where the trust and identity of the certificate issuer are important.
- Create a certificate with [AWS Certificate Manager Private CA](https://aws.amazon.com/blogs/containers/setting-up-end-to-end-tls-encryption-on-amazon-eks-with-the-new-aws-load-balancer-controller/).
- Create a certificate with [Let's Encrypt](renew-tls-cert.md#automatically-renew-tls-certificates-using-lets-encrypt).

After you create the certificate, add the following configuration block to your Helm chart in Step 8, making sure to replace the `<ACM-Certificate-ARN>` field with the ARN of your ACM certificate.

    ```yaml
    nginx:
      loadBalancerIP: ~
      privateLoadBalancer: true  # this does affect aws-load-balancer-type: external 
      ingressAnnotations:
        service.beta.kubernetes.io/aws-load-balancer-type: external
        service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: ip
        service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "\"true\""
        service.beta.kubernetes.io/aws-load-balancer-ssl-cert: <ACM-Certificate-ARN>
        service.beta.kubernetes.io/aws-load-balancer-backend-protocol: ssl
    ```

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

## Step 5: Create a Kubernetes TLS Secret

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

## Step 6: Configure your SMTP URI

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

> **Note:** If there are `/` or other escape characters in your username or password, you may need to [URL encode](https://www.urlencoder.org/) those characters.

## Step 7: Configure the database

By default, Astronomer requires a central Postgres database that will act as the backend for Astronomer's Houston API and will host individual metadata databases for all Airflow Deployments spun up on the platform.

While you're free to configure any database, most AWS users on Astronomer run [Amazon RDS for PostgreSQL](https://aws.amazon.com/rds/postgresql/). For production environments, Astronomer recommends a managed Postgres solution.

> **Note:** If you're setting up a development environment, this step is optional. Astronomer can be configured to deploy the PostgreSQL helm chart as the backend database with the following set in your `config.yaml`:
>
> ```yaml
> global:
>   postgresqlEnabled: true
> ```

To connect to an external database to your EKS cluster, create a Kubernetes Secret named `astronomer-bootstrap` that points to your database.

```bash
kubectl create secret generic astronomer-bootstrap \
  --from-literal connection="postgres://USERNAME:$PASSWORD@host:5432" \
  --namespace astronomer
```

> **Note:** You must URL encode any special characters in your Postgres password.

> **Note:** Astronomer recommends using a [t2 medium](https://aws.amazon.com/rds/instance-types/) as the minimum RDS instance size.

## Step 8: Configure your Helm chart

:::info 

To use a third-party ingress controller for Astronomer, see [Third-Party Ingress Controllers](third-party-ingress-controllers.md).

:::

As a next step, create a file named `config.yaml` in an empty directory.

For context, this `config.yaml` file will assume a set of default values for our platform that specify everything from user role definitions to the Airflow images you want to support. As you grow with Astronomer and want to customize the platform to better suit your team and use case, your `config.yaml` file is the best place to do so.

Copy and paste the following example into the `config.yaml` file. Replace `baseDomain`, `private-root-ca`, `/etc/containerd/certs.d`, `astronomer.houston.secret`, and `ssl.enabled` with your own values. Additional example configurations are available in the [Astronomer GitHub configs repository](https://github.com/astronomer/astronomer/tree/master/configs).

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
  privateCaCerts:
  - private-root-ca

  # Enable privateCaCertsAddToHost only when your nodes do not already
  # include the private CA in their docker trust store.
  # Most enterprises already have this configured,
  # and in that case 'enabled' should be false.
  privateCaCertsAddToHost:
    enabled: true
    hostDirectory: /etc/containerd/certs.d
  # For development or proof-of-concept, you can use an in-cluster database
  postgresqlEnabled: false

  # Enables using SSL connections to
  # encrypt client/server communication
  # between databases and the Astronomer platform.
  # If your database enforces SSL for connections,
  # change this value to true. Incluster postgres only supports 
  # sslmode.enabled = false.
  ssl:
    enabled: false
#################################
### Nginx configuration
#################################
nginx:
  # IP address the nginx ingress should bind to
  loadBalancerIP: ~
  #  Set to 'true' when deploying to a private EKS cluster.
  privateLoadBalancer: false
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
        manualReleaseNames: true # Allows you to set your release names
        serviceAccountAnnotationKey: eks.amazonaws.com/role-arn # Flag to enable using IAM roles (don't enter a specific role)
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

These are the minimum values you need to configure for installing Astronomer. For information on additional configuration, read [What's Next](install-aws-standard.md#whats-next).

:::info

If you are installing Astronomer in an airgapped environment without access to the public internet, complete all of the setup in [Install in an Airgapped Environment](install-airgapped.md) and then skip directly to Step 10 in this document.

:::

## Step 9: Install Astronomer

<!--- Version-specific -->

Now that you have an EKS cluster set up and your `config.yaml` file defined, you're ready to deploy all components of our platform.

First, run:

```sh
helm repo add astronomer https://helm.astronomer.io/
```

Then, run:

```sh
helm repo update
```

This ensures that you pull the latest image from the Astronomer Helm repository. Now, run:

```sh
helm install -f config.yaml --version=0.32 --namespace=astronomer <your-platform-release-name> astronomer/astronomer
```

This command installs the most recent patch version of Astronomer Software. To install a different patch version, add the `--version=` flag and use the format `0.32.x`.  For example, to install Astronomer Software v0.32.0, you specify `--version=0.32.0`. For more information about the available patch versions, see the [Software Release Notes](release-notes.md).

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

## Step 10: Verify Pods are up

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

If you are seeing issues here, check out our [guide on debugging your installation](debug-install.md/).

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

## Step 12: Verify you can access the Software UI

Go to `app.BASEDOMAIN` to see the Software UI.

Consider this your new Airflow control plane. From the Software UI, you'll be able to both invite and manage users as well as create and monitor Airflow Deployments on the platform.

## Step 13: Verify your TLS setup

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
