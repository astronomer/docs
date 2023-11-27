---
sidebar_label: 'Platform requirements'
title: 'Astronomer Software platform requirements'
id: platform-requirements
description: Learn about the requirements and optional features for configuring Astronomer Software as an administrator
---

## Base requirements

### Kubernetes

Astronomer Software must be installed on a Kubernetes cluster. All Astronomer Software components, including your Airflow Deployments, run in Kubernetes Pods. Each Astronomer cluster requires at least 20 unallocated VCPUs and 64 unallocated GB of memory, while each Airflow Deployment requires an additional 4 VCPUs and 6GB of memory.

Each Astronomer Software version is compatible with a specific range of Kubernetes versions. For a complete reference of Kubernetes version compatibility, see [Kubernetes version support table and policy](https://docs.astronomer.io/software/version-compatibility-reference#kubernetes-version-support-table-and-policy).

:::info Multi-tenant cluster requirements

If you're installing Astronomer Software onto an existing cluster that also runs non-Astronomer workloads, you will have to configure additional components and features in order for Astronomer Software to work.

:::

### Database

You must provide your own Postgres database server instance for each Astronomer Software cluster you create. The database server instance has the following requirements:

- It is Postgres version 11+
- It can run on one of the following platforms:
    - Self-managed standard Postgres
    - Amazon RDS
    - Google CloudSQL for Postgres
    - Azure FlexibleDB for Postgres
- It must be allocated at least 2vCPUs and 4GB of memory.
- There is a dedicated administrative user within the instance that is used exclusively by Astronomer Software. This user requires privileges such as `CREATE DATABASE`, `CREATE ROLE`, and `GRANT`. 
- You must be able to authenticate to the database administrative user with a username and password.

### Networking

Adequate IP addresses must be available for Kubernetes nodes, Kubernetes Pods, cluster-internal services, and cluster-external load-balancers.

Generally speaking Astronomer Software cluster requires the following IP availability:

- 35 IP addresses within the cluster service-address space.
- 50 IP addresses within the Pod address space.
- 1 cluster-external IP, unless using a third-party ingress controller already accounted for elsewhere.

Each Airflow Deployment within a cluster requires the following additional IP availability:

- 12 IP addresses within the cluster service-address space.
- 15 IP addresses within the pod address space.
- Additional Pod address space as required for extra worker and scheduler Pods if you increase the capacity of your Deployments.

Note that these numbers can vary based on whether your Kubernetes Container Network Interface (CNI) assigns each Pod a cluster-external IP address or whether the IP addresses assigned to Pods exist exclusively within a Kubernetes-internal cluster-overlay network provided by your CNI.

#### DNS Requirements

- Kubernetes pods in the Astronomer platform namespace and astronomer-managed airflow namespaces must be able to resolve dns entries associated with:
    - the astronomer baseDomain
    - postgres server
    - platform registry
    - Kubernetes worker nodes must be able to resolve the dns entries associated with your Astronomer installation
- A DNS entry (or entries) must be created that points to the ingress controller providing service to astronomer. The following must be able to resolve this address:
    - kubernetes-external load-balancer
    - astro-cli users
    - web users Astronomer Software (including Airflow)
    - kubernetes worker nodes
    - pods in the astronomer platform namespace
    - pods in namespaces created by the astronomer platform
    - CICD systems deploying to astronomer
- See Kubernetes Requirements Section for additional requirements related to DNS resolution.

#### Exposing the Astronomer Software Cluster Outside Kubernetes

The Astronomer Software cluster must be exposed outside Kubernetes through one of the following three methods:
  
- Using Astronomer’s integrated ingress controller with service through a LoadBalancer provisioned via LoadBalancerController. Such load-balancers must be layer 2 or 3 and not terminate SSL.
- Using Astronomer’s integrated ingress controller with service through a NodePort in conjunction with external customer-provided load-balancing solution exposing the Astronomer Software service outside Kubernetes on ports 80 and 443. Running the NodePort directly on ports below 1000 is explicitly unsupported. Such load-balancing solution must be layer 2 or 3 and not terminate SSL.
- Service through a customer-provided ingress controller configured to meet all requirements set forth at https://docs.astronomer.io/software/third-party-ingress-controllers and explicitly listed as supported therein.

#### Ingress, Egress, and Routing Requirements

Kubernetes egress traffic from pods in the Astronomer platform namespace and astronomer-managed airflow namespaces must be able to communicate with the kubernetes-external IP address of the load balancer associated with the ingress associated with Astronomer.

Kubernetes worker nodes must be able to communicate with the kubernetes-external IP address of the load balancer associated with the ingress associated with Astronomer.

Kubernetes egress traffic from pods in the Astronomer platform namespaces must be able to communicate with the postgres server(s).

If using a customer-provided load-balancing solution in conjunction with a NodePort, the load-balancer must be able to connect to the NodePorts.

The kubernetes-external load-balancer address must be routable and accessible to all the following: astro-cli users, kubernetes worker nodes, pods in the astronomer platform namespace, pods in namespaces created by the astronomer platform, astro-cli users, houston-api users, CICD systems deploying to astronomer.

If email notifications are enabled, pods running within the kubernetes platform namespace must be able to communicate with the configured email server(s) via SMTP.

When airgapped mode is disabled, outbound https access to [astronomer.io](http://astronomer.io) and other domains is required from pods in the airflow and astronomer namespace.

Outbound https access to [quay.io](http://quay.io) from kubernetes worker nodes is required unless using a private platform registry or pull-through caching proxy.

When OIDC Authentication is enabled, pods in the astronomer platform namespace and airflow namespaces must be able to resolve and connect to the the OIDC server host(s).

### Credentials and permissions

## Recommended configurations

### Single sign-on

### SCIM 

### SMTP 

### CI/CD 

### Astro CLI