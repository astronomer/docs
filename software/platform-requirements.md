---
sidebar_label: 'Platform requirements'
title: 'Astronomer Software platform requirements'
id: platform-requirements
description: Learn about the requirements and optional features for configuring Astronomer Software as an administrator
---

## Base platform requirements

The following topics contain high level information about what system components and resources are required by Astronomer Software. Note that you might encounter additional requirements based on your system and security requirements. [What should a user do if they have more questions about this?]

### Kubernetes

Astronomer Software must be installed on a Kubernetes cluster. All Astronomer Software components, including your Airflow Deployments, run in Kubernetes Pods. Each Astronomer cluster requires at least 20 unallocated VCPUs and 64 unallocated GB of memory, while each Airflow Deployment requires an additional 4 VCPUs and 6GB of memory.

Each Astronomer Software version is compatible with a specific range of Kubernetes versions. For a complete reference of Kubernetes version compatibility, see [Kubernetes version support table and policy](https://docs.astronomer.io/software/version-compatibility-reference#kubernetes-version-support-table-and-policy).

:::info Multi-tenant cluster requirements

If you're installing Astronomer Software onto an existing cluster that also runs non-Astronomer workloads, you will have to configure additional components and features in order for Astronomer Software to work.

:::

### Database

You must provide your own Postgres database server instance for each Astronomer Software cluster you create. The Postgres database stores all data related to Astronomer, including task logs and metadata from your Airflow Deployments. The database server instance has the following requirements:

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

Generally speaking, your Astronomer Software cluster requires the following IP availability:

- 35 IP addresses within the cluster service-address space.
- 50 IP addresses within the Pod address space.
- 1 cluster-external IP, unless using a third-party ingress controller already accounted for elsewhere.

Each Airflow Deployment within a cluster requires the following additional IP availability:

- 12 IP addresses within the cluster service-address space.
- 15 IP addresses within the pod address space.
- Additional Pod address space as required for extra worker and scheduler Pods if you increase the capacity of your Deployments.

Note that these numbers can vary based on whether your Kubernetes Container Network Interface (CNI) assigns each Pod a cluster-external IP address or whether the IP addresses assigned to Pods exist exclusively within a Kubernetes-internal cluster-overlay network provided by your CNI.

Network communication between Astronomer Platform Pods and Deployment namespaces cannot be restricted in any way, such as through a network policy. 

### Docker registry access

The Astronomer Software cluster needs to be able to access Docker images both for Astronomer platform functionality and for individual Airflow Deployments. 

For platform images, Kubernetes worker nodes must be able to pull images directly from Astronomer’s public quay.io repository without restriction. Otherwise, you must provide and populate a registry or pull-through caching proxy accessible to the cluster. See [Configure a custom registry for Deployment images](custom-image-registry.md) to learn how to implement your own registry.

Note that if you're using a custom registry that requires authentication, your must store an `imagePullSecret` with sufficient pull privileges in the Astronomer platform namespace.

### Certificates and certificate authorities

Astronomer Software has different requirements based on how you manage your SSL certificates.

Astronomer Software includes a built-in ingress controller that manages public access to your Software cluster. If you use the built-in ingress controller, you must generate and maintain a valid certificate for the ingress that covers your company's base domain and its subsidiaries. This can be either a a wildcard cert or a cert that explicitly lists each of the required domain names. This certificate must be signed by either a public or private CA. See [Generate self-signed TLS certificates](self-signed-certificate.md) and [Renew a TLS certificate](renew-tls-cert.md).

If you use a private CA, Kubernetes nodes (kubelet) must be configured to trust the private CA. Please note this is explicitly prohibited by most current versions of AKS and all versions of AWS EKS on Fargate.

Your pem file must contain the complete certificate chain, including the root and all intermediate certificates. If a user looks at the file, they should see at least two certificate sections. Most modern browsers will work around broken certificate chains, so the Software UI might still be available if only the leaf certificate is provided, but the platform will be non-functional.

#### Exposing the Astronomer Software cluster outside of Kubernetes

The Astronomer Software cluster must be exposed outside Kubernetes through one of the following three methods:
  
- Using Astronomer’s built-in ingress controller with service through a LoadBalancer provisioned via LoadBalancerController. LoadBalancers must be layer 2 or 3 and not terminate SSL.
- Using Astronomer’s built-in ingress controller with service through a NodePort in conjunction with external customer-provided load-balancing solution exposing the Astronomer Software service outside Kubernetes on ports 80 and 443. Running the NodePort directly on ports below 1000 is explicitly unsupported. LoadBalancers must be layer 2 or 3 and not terminate SSL.
- Using a custom ingress controller configured to meet all requirements as described in [Third-party ingress controllers](https://docs.astronomer.io/software/third-party-ingress-controllers).

## Recommended configurations

Though not explicitly required, Astronomer strongly recommends setting up the following tools and integrations to get the most out of Astronomer Software. 

### Single sign-on

Astronomer Software includes tools to integrate with popular identity providers (IdPs) such as Okta, Microsoft Entra ID, and Auth0. Astronomer strongly recommends integrating your current SSO provider to allow teammates to quickly onboard to the platform. Using an identity provider provides the following benefits:

- You can manage Astronomer Software users directly from your IdP using SCIM.
- You can create templates of permissions to apply when onboarding new users.
- Users can log in to Astronomer Software directly from your IdP.

See [Integrate an auth system](integrate-auth-system.md) for setup steps for each supported IdP.

### SCIM 

Astronomer Software supports integration with the open standard System for Cross-Domain Identity Management (SCIM). Using the SCIM protocol with Astronomer Software allows you to automatically provision and deprovision users and Teams based on templates for access and permissions. It also provides better observability through your identity provider for when users and Teams are created or modified across your organization.

After you configure your identity provider, follow the steps in [Manage users and Teams with SCIM](integrate-auth-system.md#manage-users-and-teams-with-scim) to set up SCIM for Astronomer Software. 

### SMTP 

Astronomer requires access to a SMTP server to:

- Send automated notifications about Airflow Deployments.
- Invite new users to the platform. Note that SMTP is not required for inviting users through an IdP.

See [Airflow alerts](airflow-alerts.md) for steps to integrate a couple of the most common SMTP servers with Astronomer Software. 

### CI/CD 

Astronomer recommends developing a CI/CD pipeline for your data engineers to push DAGs and other code-level configurations to Astronomer Software. You can use service accounts to authorize CI/CD tools, such as GitHub Actions, to access Astronomer Software and deploy code you your Deployments.

See [CI/CD](ci-cd.md) for steps to set up a service account, as well as CI/CD templates for popular CI/CD tools.

### Astro CLI

All users on Astronomer Software should install and have access to the Astro CLI. This open source command line tool includes functionality for managing Astronomer Software, as well as testing Airflow code locally before your push code. See the [Astro CLI documentation](https://docs.astronomer.io/astro/cli/overview) for installation steps and command references. 