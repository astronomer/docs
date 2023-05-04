---
sidebar_label: 'FAQ'
title: 'Astronomer Software FAQ'
description: Commonly asked questions and answers for Astronomer Software.
---

## Networking

### Do ports or services need to be configured when installing Astronomer Software? Do I need to provide an IP address?

Yes. You must provide an IP for the NAT gateway to access the Astronomer and Airflow user interfaces, and also to interact with the platform with the astro-cli tool. Reviewing our Terraform scripts and installation guides are helpful to better understand this requirement.

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

You can find a list of all components used by the platform in the [Astronomer Platform - Docker images](https://docs.google.com/spreadsheets/d/1jE8EA4YapKEghVvk0-4K_MdwoVe6-O7v4uCI03ke6yg/edit#gid=0) Google Sheet.

## System-level access requirements

### Does the platform need root access to the Kubernetes cluster?

No. Astronomer makes use of Kubernetes cluster-level features (including K8s RBAC) by design. These features include creating / deleting namespaces, daemonsets, roles, cluster-roles, service-accounts, resource-quotas, limit-ranges, etc. Additionally, Astronomer dynamically creates new airflow instances in separate namespaces, which protects data engineer users from noisy neighbors.

* Roles
  * [Houston](https://github.com/astronomer/astronomer/blob/master/charts/astronomer/templates/houston/api/houston-bootstrap-role.yaml)
  * [NGINX](https://github.com/astronomer/astronomer/blob/master/charts/nginx/templates/nginx-role.yaml)
  * [Commander](https://github.com/astronomer/astronomer/blob/master/charts/astronomer/templates/commander/commander-role.yaml)
  * [Fluentd](https://github.com/astronomer/astronomer/blob/master/charts/fluentd/templates/fluentd-clusterrole.yaml)
  * [Prometheus](https://github.com/astronomer/astronomer/blob/master/charts/prometheus/templates/prometheus-role.yaml)
  * [Grafana](https://github.com/astronomer/astronomer/blob/master/charts/grafana/templates/grafana-bootstrap-role.yaml)
  * [Kubestate](https://github.com/astronomer/astronomer/blob/master/charts/kube-state/templates/kube-state-role.yaml)
  * [Tiller](https://github.com/astronomer/astronomer/blob/master/charts/astronomer/templates/commander/commander-role.yaml)

### How can we restrict the application from getting full access?

Astronomer defines the required Roles or ClusterRoles. The default mode requires a ClusterRole that has access to create namespaces and other objects for new Airflow deployments.

### What are the default usernames and passwords?

When you install Astronomer Software, the root user `root@<your-basedomain>` with all permissions is automatically created. The password is stored as a Kubernetes secret on your installation. See [Manage the root user](https://docs.astronomer.io/software/0.31/manage-root-user#log-in-as-the-root-user). There are no other default users or passwords. 

### Are there separate credentials or accesses that Astronomer provisions?

No. Review the [Astronomer Helm chart repo](https://github.com/astronomer/astronomer) to learn more about Astronomer Software default configurations. 

## Deployment

### What scripts are used for deployment?

The default method for installing and upgrading Astronomer Software is using the Astronomer Helm chart located at `https://helm.astronomer.io`. See the Astronomer Software installation guides ([AWS](install-aws-standard.md), [GCP](install-gcp-standard.md), and [Azure](install-azure-standard.md)) and [Upgrade Astronomer](upgrade-astronomer.md).

## Authentication

### How can we get multi-factor auth?

Astronomer provides an [authentication front end](integrate-auth-system.md) with pre-built integrations for Google Auth, Okta, Auth0, and others.

### How can implement RBAC with this solution?

Astronomer has [built-in Airflow RBAC support](workspace-permissions.md).

## Continuous vulnerability assessment and remediation

### If the platform is scanned by a vulnerability scanner, virus scanners, will there be any ill effects that we need to be aware of?

No. Astronomer continuously scans all code and Docker images with vulnerability assessment software. Issues can occur when your software blocks critical pods from launching.

## Malware defenses

### How does Astronomer handle malformed or otherwise unexpected input?

The Astronomer and Airflow UIs sanitize and verify inputs according to modern standards.

## User sessions

### Does Astronomer allow for encrypted sessions?

Yes. The Transport Layer Security (TLS) encryption protocol is configured automatically with Astronomer setup scripts.

### Is there a session limitation?

Yes. Sessions are terminated after 24 hours of inactivity for both Astronomer Software and CLI by default.

### How can we turn on SSL and use our own CA?

Astronomer Software uses the Secure Sockets Layer (SSL) encryption protocol by default. During installation, you must provide either a wildcard certificate or a certificate for the following domains:

- `BASEDOMAIN`
- `app.BASEDOMAIN`
- `deployments.BASEDOMAIN`
- `registry.BASEDOMAIN`
- `houston.BASEDOMAIN`
- `grafana.BASEDOMAIN`
- `kibana.BASEDOMAIN`
- `install.BASEDOMAIN`
- `alertmanager.BASEDOMAIN`
- `prometheus.BASEDOMAIN`

## External monitoring

### Does the platform produce event logs that we could consume in our monitoring systems?

Yes. All logs are sent to ElasticSearch through FluentD by default. You can customize the FluentD configuration to send logs to other destinations, or route logs from Elasticsearch to your monitoring systems.

### Does Astronomer generate any email-based traffic/alerts?

Yes. Airflow supports email alerting features for DAG failures, and Astronomer supports email alerting for infrastructure issues.

## Restricting access

### Can we restrict the web UI to access from the internet?

The platform API and web UI are served over a single highly available AWS load balancer. By using an internal load balancer, the entire platform will only be accessible in a private network.

## Auditing

### What level of auditing is natively available? What logs/audit artifacts are produced?

Logs from each Astronomer service are accessible to you through your cloud provider. Astronomer does not generate audit logs for the Astronomer platform.

### What kind of management is available for security logs?

All platform components and Airflow deployment logs are retained within the platform’s logging stack for 15 days. This is useful for searching recent logs using the Kibana interface to ElasticSearch. For log backup to comply with policy, container stdout and stderr logs may also be collected in AWS CloudWatch and can be persisted according to your CloudWatch logs retention policy. For AWS API security and auditing, Astronomer recommends enabling AWS CloudTrail.

### How do we manage application and system logs?

Astronomer's Software offering has a robust logging structure sitting atop Airflow. See [Kibana logging on Astronomer Software](kibana-logging.md).

## Updating

### How are security updates handled on Astronomer? How are users notified of a critical update?

You can upgrade your Airflow Deployments separately from your platform upgrades. Astronomer recommends updating your Deployment's Airflow versions and the platform frequently so that your organization is always using a supported version. See [Astronomer Software and lifecycle policy](release-lifecycle-policy.md).

### How does patching work for this setup?

Kubernetes and node upgrades are typically managed by your organization. Platform version upgrades are performed with Helm and with the assistance of Astronomer support when required. See [Upgrade Astronomer](upgrade-astronomer.md).
