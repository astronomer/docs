---
title: 'Use a third-party ingress controller'
sidebar_label: 'Third-Party ingress controllers'
id: third-party-ingress-controllers
description: Use a pre-existing ingress controller on Astronomer Software.
---

By default, Astronomer comes with an ingress controller to service Kubernetes ingress objects. The default Astronomer ingress controller can co-exist with any other ingress controllers on the cluster.

Using the default ingress controller is the best choice for most organizations, but you might need to use a pre-existing ingress controller exclusively due to complex regulatory and compliance requirements. This guide provides steps for configuring your own ingress controller to use with the Astronomer platform.

## Step 1: Review general requirements for third-party ingress controllers

To use a third-party ingress-controller with Astronomer Software:

- Your ingress controller must service ingresses from the Astronomer Platform namespace, as well as all namespaces that host Airflow.
- Ingresses should work in newly created namespaces prior to installing Astronomer Software.
- Your third-party ingress controller must be able to resolve the DNS entries associated with your Software installation.
- Your third-party ingress controller must support SSL connections on port 443 and must present a certificate valid for all of the following hostnames:

    - BASE_DOMAIN
    - app.BASE_DOMAIN
    - deployments.BASE_DOMAIN
    - registry.BASE_DOMAIN
    - houston.BASE_DOMAIN
    - grafana.BASE_DOMAIN
    - kibana.BASE_DOMAIN
    - install.BASE_DOMAIN
    - prometheus.BASE_DOMAIN
    - alertmanager.BASE_DOMAIN

- Your ingresses must present valid SSL certificates.

If the certificates of the third-party ingress controller presents are signed by a private certificate authority:

- The third-party ingress controller must be configured to trust your private CA (as per the documentation of your ingress controller).
- The CA's public certificate must be stored as a Kubernetes secret in the Astronomer namespace.

If a private certificate authority is used to sign the certificate contained in the `global.tlsSecret` value in your `values.yaml` file, the third-party ingress controller must recognize the CA signing `global.tlsSecret` as valid. Typically, this is done by either:

- Signing the secret used in `global.tlsSecret` with a private CA that's already trusted by the custom ingress controller (typically the same CA used to sign the certificates being used by the ingress controller).
- Explicitly configuring your custom ingress controller to trust the CA used when generating the certificate contained in `global.tlsSecret`.

## Step 2: Verify your Ingress Controller is Supported

To complete this setup, you need to supply your own ingress controller. Astronomer fully supports the following types of ingress controllers:

- OpenShift
- Kong
- HAProxy
- Ingress-nginx
- Traefik
- Contour

If you want to use an ingress controller that isn't listed here, please contact your Astronomer representative.

## Step 3: (OpenShift Only) Perform required configuration to your Kubernetes environment {#required-environment-configuration-openshift}
If not using OpenShift, skip this step.


OpenShift's standard ingress controller restricts hostname use to a single namespace, which is not a compatible setting with Astronomer Software. You can disable this setting for the default IngressController instance using the following command:


```sh
kubectl -n openshift-ingress-operator patch ingresscontroller/default --patch '{"spec":{"routeAdmission":{"namespaceOwnership":"InterNamespaceAllowed"}}}' --type=merge
```

Alternatively, see [Use Openshift Ingress Sharding](https://docs.openshift.com/container-platform/4.15/networking/ingress-sharding.html) to create an additional Ingress instance with the required routeAdmission policy.
For more information, including information about security implications for multi-tenant clusters, see the [Openshift Ingress operator documentation](https://docs.openshift.com/container-platform/4.15/networking/ingress-operator.html).

OpenShift clusters with multi-tenant isolation enabled need to explicitly allow traffic from the ingress controller's namespace to services associated with ingresses in other namespaces.

Label the namespace containing your ingress controller with the `network.openshift.io/policy-group=ingress` label. The label can vary based on the specific policy and configuration on your cluster, however. For example, you might run the following:

```sh
kubectl label namespace/<ingress namespace> network.openshift.io/policy-group=ingress
```

For more information, see the [OpenShift documentation](https://docs.openshift.com/container-platform/4.15/networking/network_policy/about-network-policy.html) on configuring network policy.

## Step 4: Mark the astronomer-tls secret for replication

Most third-party ingress controllers require the `astronomer-tls` secret to be replicated into each Airflow namespace.

Annotate the secret and set `"astronomer.io/commander-sync"` to `platform=<astronomer platform release name>`. For example:
```sh
kubectl -n <astronomer platform namespace> annotate secret astronomer-tls "astronomer.io/commander-sync"="platform=astronomer"
```

## Step 5: Set required settings in values.yaml

Enable authSidecar and disable Astronomer's integrated ingress controller.

```yaml
global:
  nginxEnabled: false

  authSidecar:
    enabled: true
  # must be named exactly astronomer-tls when using a third-party ingress controller
    tlsSecret: astronomer-tls
```

## Step 6: Perform required configuration for your specific ingress controller

### Required configuration for nginx

If you're using an nginx ingress controller, add the following configuration to your `values.yaml` file:

```yaml
global:
  extraAnnotations:
    nginx.ingress.kubernetes.io/proxy-body-size: 0
```

This setting disables Nginx's maximum allowed upload size, which prevents HTTP 413 (Request Entity Too Large) error and allows the Astro CLI to properly deploy DAGs to Astronomer Software's internal registry.

### Required configuration for traefik

If you're using a traefik ingress controller, add the following configuration to your `values.yaml` file:

```yaml
global:
  extraAnnotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
    traefik.ingress.kubernetes.io/router.tls: "true"
```

> **Note:** Depending on the version of Traefik, upgrading from using the default ingress controller to a Traefik controller might cause issues. If you are upgrading a platform that used the built-in ingress controller, manually delete the Astronomer Platform Ingress objects in the Astronomer Platform namespace before updating your `values.yaml` file. You can do so using the following commands:
>
>    ```sh
>    $ kubectl -n <your-platform-namespace> delete ingress -l release=<your-platform-release-name>
>    $ helm upgrade --install -f values.yaml --version=<your-platform-version> --namespace=<your-platform-namespace> <your-platform-release-name> astronomer/astronomer
>    ```

### Required configuration for Contour

Contour ships with support for websockets disabled by default. To use a Contour ingress controller, explicitly enable WebSocket support for Houston's `/ws` prefix by creating an HTTPProxy object in the Astronomer platform namespace. To do so:

1. Create a file named `proxy.yaml` and add the following to it:

    ```yaml
    apiVersion: projectcontour.io/v1
    kind: HTTPProxy
    metadata:
      name: houston
      annotations:
        kubernetes.io/ingress.class: contour
    spec:
      virtualhost:
        fqdn: houston.<base-domain>
        tls:
          secretName: astronomer-tls
      routes:
        - conditions:
          - prefix: /ws
          enableWebsockets: true
          services:
            - name: astronomer-houston
              port: 8871
    ```

2. Apply the file to your platform namespace:

   ```bash
   kubectl apply -n <your-platform-namespace> -f proxy.yaml
   ```

:::info

Depending on the version of Contour, upgrading from using the default ingress controller to a Contour controller might cause issues. If you are upgrading a platform that used the built-in ingress controller, manually delete the Astronomer Platform Ingress objects in the Astronomer Platform namespace before updating your `values.yaml` file. You can do so using the following commands:

  ```sh
  $ kubectl -n <your-platform-namespace> delete ingress -l release=<your-platform-release-name>
  $ helm upgrade --install -f values.yaml --version=<your-platform-version> --namespace=<your-platform-namespace> <your-platform-release-name> astronomer/astronomer
  ```

### Required configuration Openshift Ingress Controller

See [Required Environment Configuration for OpenShift](#required-environment-configuration-openshift).

## Step 7: Apply Changes With Helm

If performing a new installation, skip this step and do not apply changes until the install guide instructs you to do so.

If this is an existing installation, apply your updated configuration using the following command:
```bash
helm upgrade --install -f values.yaml --version=<your-platform-version> --namespace=<your-platform-namespace> <your-platform-release-name> astronomer/astronomer
```
