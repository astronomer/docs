---
sidebar_label: 'FAQ'
title: 'Astronomer Software FAQ'
id: faq
---

## Networking

### Does Astronomer require any ports/services to be configured in order to operate? Does it require us to provide an IP?

Yes. You must provide an IP for the NAT gateway to access the Astronomer and Apache Airflow® user interfaces, and also to interact with the platform with the astro-cli tool. Reviewing our Terraform scripts and installation guides are helpful to better understand this requirement.

### Does Astronomer accept inbound connections? Do those connections have to be secured or is that something we need to configure?

Yes. Inbound traffic routes through the NAT gateway. TLS is utilized throughout, and is configured automatically with our setup scripts.

### Will Astronomer suffer any ill effects if it has to operate in a sandbox or behind a firewall?

Yes. The `commander` component would require a special build if operating in an air-gapped environment.

### Are there known external connections required to operate Astronomer? Are there specs on what expected inbound/outbound traffic patterns will look like?

Yes. Connecting to your data and data systems require networking outside of the Kubernetes cluster that Airflow is running within. These connections can be made either through the public internet or through private networking that you have configured.

### Are there known domains which Astronomer connects to?

Yes. Airflow deployments check for updates and security fixes to updates.astronomer.io.  This feature is effectively disabled in air-gapped deployments.

Beyond that, the platform does not need to connect to outside domains for routine execution of the platform. External connections are only required by Airflow in the execution of specific workflows.


## Docker

### What are the components of the Astronomer platform, with their respective Docker image versions?

You can find a list of all components used by the platform in the [Astronomer Platform - Docker Images](https://docs.google.com/spreadsheets/d/1jE8EA4YapKEghVvk0-4K_MdwoVe6-O7v4uCI03ke6yg/edit#gid=0) Google Sheet.

### What Docker version is used for deployment?

* AWS: Astronomer prefers to use the EKS-optimized AMIs provided by AWS. These will automatically include the latest, stable Docker version tested by Amazon with EKS. We recommend [looking up the AMI ID](https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html) to find the image appropriate for your Kubernetes version and AWS region. You may have additional requirements that necessitate building your own AMI. You might build these with Packer, in which case you may want to reference the EKS [optimized Packer configuration](https://github.com/awslabs/amazon-eks-ami). Assuming that you are using Kubernetes 1.14, it looks like AWS is using Docker version 18.09 for the [latest release of the EKS AMI](https://github.com/awslabs/amazon-eks-ami/blob/da2d05a60929f9d258355b8a597f2917c35896f4/eks-worker-al2.json#L17).
* GKE: has a similar set up to EKS where they provide an optimized machine image that is ideal for running in their managed kubernetes service. For Astronomer, we are making use of these GKE images, using Kubernetes 1.14. This is also using Docker version 18.09. [This page includes the release notes](https://cloud.google.com/container-optimized-os/docs/release-notes) for the GKE optimized machine images (called ‘container optimized OS’ or ‘COS’ for short). This page indicates the [release notes for GKE in general](https://cloud.google.com/kubernetes-engine/docs/release-notes). GKE has a nice feature introduced last year called “Release channels” that are nice for automatically upgrading Kubernetes version. GKE also has [a few other machine images besides COS](https://cloud.google.com/kubernetes-engine/docs/concepts/node-images).

## System-Level Access Requirements

### Does the platform need root access to the Kubernetes cluster?

No. Astronomer makes use of Kubernetes cluster-level features (including K8s RBAC) by design. These features include creating / deleting namespaces, daemonsets, roles, cluster-roles, service-accounts, resource-quotas, limit-ranges, etc. Additionally, Astronomer dynamically creates new airflow instances in separate namespaces, which protects data engineer users from noisy neighbors.

* Roles
  * [Houston](https://github.com/astronomer/astronomer/blob/master/charts/astronomer/templates/houston/api/houston-bootstrap-role.yaml)
  * [Kubed](https://github.com/astronomer/astronomer/blob/master/charts/kubed/templates/kubed-clusterrole.yaml)
  * [NGINX](https://github.com/astronomer/astronomer/blob/master/charts/nginx/templates/nginx-role.yaml)
  * [Commander](https://github.com/astronomer/astronomer/blob/master/charts/astronomer/templates/commander/commander-role.yaml)
  * [Fluentd](https://github.com/astronomer/astronomer/blob/master/charts/fluentd/templates/fluentd-clusterrole.yaml)
  * [Prometheus](https://github.com/astronomer/astronomer/blob/master/charts/prometheus/templates/prometheus-role.yaml)
  * [Grafana](https://github.com/astronomer/astronomer/blob/master/charts/grafana/templates/grafana-bootstrap-role.yaml)
  * [Kubestate](https://github.com/astronomer/astronomer/blob/master/charts/kube-state/templates/kube-state-role.yaml)
  * [Tiller](https://github.com/astronomer/astronomer/blob/master/charts/astronomer/templates/commander/commander-role.yaml)

### How can we restrict the application from getting full access?

We have defined the exact Roles or ClusterRoles that we need for the platform to function. The default mode requires a ClusterRole that has access to create namespaces and other objects for new Airflow deployments.

###  Are there default settings we need to be aware of (including user names and passwords)?

No. The first user that signs into the platform once it is deploys is given SystemAdmin (highest-level) access.

### Are there separate credentials or accesses that Astronomer provisions?

No. We’d recommend you review the default Terraform to understand every detail of a standard deployment.


## Deployment

### What scripts are used for deployment?

We provide [a terraform module](https://registry.terraform.io/modules/astronomer/astronomer-enterprise/aws/) that deploys the infrastructure on AWS (optionally network, DB, EKS), then installs Astronomer on top of that. This also supports deploying a DB and EKS into existing subnets created by the customer. We have some Terraform available for GKE as well, which we can dig into if we go that path.

You may have special requirements of your infrastructure such that you want to set up Kubernetes on your own, then install Astronomer with Helm. In that case, you can use the Helm chart. The [latest stable version](https://github.com/astronomer/astronomer) is v0.10.3.


## Authentication

### How can we integrate with LDAP?

See [Integrate Auth System](integrate-auth-system.md)

### How can we get multi-factor auth?

Astronomer has a flexible [auth front end](integrate-auth-system.md), with pre-built integrations for Google Auth, Okta, Auth0, and others.

If you choose to use Google Auth, we have [documentation available](integrate-auth-system.md).

### How can implement RBAC with this solution?

Astronomer has [built-in Airflow RBAC support](workspace-permissions.md).


## Continuous Vulnerability Assessment and Remediation

### If the platform is scanned by a vulnerability scanner, virus scanners, will there be any ill effects that we need to be aware of?

No. We continuously scan all code and Docker images with modern vulnerability assessment software. Only if your software blocks critical pods from launching would there be any concerns.


## Malware Defenses

### How does Astronomer handle malformed or otherwise unexpected input?

The Astronomer and Airflow UIs sanitize and verify inputs according to modern standards.


## User Sessions

### Does Astronomer allow for encrypted sessions?

Yes. TLS is utilized throughout, and is configured automatically with our setup scripts.

### Is there a session limitation?

Yes. Sessions are terminated after 24 hours of inactivity for both the web UI and CLI.

### How can we turn on SSL and use our own CA?

Astronomer platform uses SSL throughout by default. During installation, a wildcard certificate for the base domain must be provided. See https://www.astronomer.io/docs/ee-installation-base-domain/


## External Monitoring

### Does the platform produce event logs that we could consume in our monitoring systems?

Yes. All logs are sent to ElasticSearch via FluentD. You could customize the FluentD configuration to send logs to other destinations, or configure something to route logs from Elasticsearch to your monitoring systems.

### Can we have a detailed account of log codes and what they mean?

No. We have not compiled this for system logs yet, we’ll try to make it available soon. However, the majority of logs in an Airflow system are user-generated.

### Does Astronomer generate any email-based traffic/alerts?

Yes. Airflow has email alerting features for DAG failures, and Astronomer has email alerting features for infrastructure issues.


## Restricting access

### Can we restrict the web UI to access from the internet?

The platform API and web UI are served over a single highly available AWS load balancer. By using an internal load balancer, the entire platform will only be accessible in a private network.


## Auditing

### What level of auditing is natively available? What logs/audit artifacts are produced?

Logs from each service are accessible to you through your cloud provider. A global, user-friendly audit logging feature has not been added to the platform yet, however it is on our short-term roadmap.

### What kind of management is available for security logs?

All platform components and Airflow deployment logs are retained within the platform’s logging stack for 15 days. This is useful for searching recent logs using the Kibana interface to ElasticSearch. For log backup to comply with policy, container stdout and stderr logs may also be collected in AWS CloudWatch and can be persisted according to your CloudWatch logs retention policy. For AWS API security and auditing, Astronomer recommends enabling AWS CloudTrail.

### How do we manage application and system logs?

Astronomer's Software offering has a robust logging structure sitting atop Airflow. See https://www.astronomer.io/docs/ee-logging/


## Updating

### How are security updates handled on Astronomer? how are users notified of a critical update required?

Updates to individual Airflow deployments can be made asynchronously from the platform updates. We recommend updating the platform and Airflow 2-3 times per year.

Minor bugfix/CVE patches are applied to individual releases for 18 months.

### How does patching work for this setup?

Kubernetes and node upgrades are generally managed by the customer. Platform version upgrades are performed with Helm, assisted by Astronomer support team if required. See [Upgrade to a Stable or Patch Version](upgrade-astronomer.md).
