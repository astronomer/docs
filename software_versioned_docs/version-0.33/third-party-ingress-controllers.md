---
title: 'Use a third-party ingress controller'
sidebar_label: 'Third-Party ingress controllers'
id: third-party-ingress-controllers
description: Use a pre-existing ingress controller on Astronomer Software.
---

By default, Astronomer comes with an ingress controller to service Kubernetes ingress objects. The default Astronomer ingress controller can co-exist with any other ingress controllers on the cluster.

While using the default ingress controller is the best choice for most organizations, you might need to exclusively use a pre-existing ingress controller due to complex regulatory and compliance requirements. This guide provides steps for configuring your own ingress controller for use with the Astronomer platform.

## Prerequisites

To complete this setup, you need to supply your own ingress controller. Astronomer fully supports the following types of ingress controllers:

- kong
- haproxy
- ingress-nginx
- traefik
- contour

If you want to use an ingress controller that isn't listed here, please contact your Astronomer representative.

Additionally, all of the following must be true:

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

### Additional prerequisites for private certificate authorities

If the certificates of the third-party ingress controller presents are signed by a private certificate authority:

- The third-party ingress controller must be configured to trust your private CA (as per the documentation of your ingress controller).
- The CA's public certificate must be stored as a Kubernetes secret in the Astronomer namespace.

If a private certificate authority is used to sign the certificate contained in the `global.tlsSecret` value in your `config.yaml` file, the third-party ingress controller must recognize the CA signing `global.tlsSecret` as valid. Typically, this is done by either:

- Signing the secret used in `global.tlsSecret` with a private CA that's already trusted by the custom ingress controller (typically the same CA used to sign the certificates being used by the ingress controller).
- Explicitly configuring your custom ingress controller to trust the CA used when generating the certificate contained in `global.tlsSecret`.

## Step 1: Complete platform installation steps

If you are installing Astronomer for the first time, complete your Astronomer platform installation up until the "Configure your Helm chart" step. If this configuration is part of an existing installation, you can skip to Step 2 or complete the following optional setup.

### Optional: Share a certificate between Astronomer and your ingress controller

If you want the Astronomer platform and your ingress controller to share a certificate, the contents of the certificate will almost always need to be stored twice: Once as a Kubernetes TLS secret in the Astronomer Platform namespace (as during a standard install), and again as specified by your ingress controller's documentation.

Kubernetes prevents accessing secrets from another namespace, so an individual Kubernetes secret cannot be directly shared between the Astronomer Platform and the third-party ingress controller. Instead, create a separate copy of the certificate in the ingress controller's namespace. Alternatively, you can use `kubed` to replicate the Astronomer's `astronomer-tls` secret into the ingress controller's namespace using the following commands:

```bash
# namespace containing your custom ingress controller
$ INGRESS_CONTROLLER_NAMESPACE=some-namespace
# name of the secret in the Astronomer Platform namespace
$ SECRET_NAME=astronomer-tls
# label the namespace containing your ingress controller
$ kubectl label namespace/${INGRESS_CONTROLLER_NAMESPACE} "network.openshift.io/policy-group=ingress"
# annotate the astronomer-tls secret with that as a sync target
$ kubectl annotate secret/${SECRET_NAME} kubed.appscode.com/sync="platform-release=astronomer"
# confirm secret replicated
$ kubectl -n ${INGRESS_CONTROLLER_NAMESPACE} get secret ${SECRET_NAME}
```

## Step 2: Configure Your Helm chart

To install your existing ingress controller and disable the default one, add the following to your `config.yaml` file:

```yaml
global:
  # Disable the default ingress controller
  nginxEnabled: false
  # valid tlsSecret still required to be present in the Astronomer Software Platform namespace
  tlsSecret: astronomer-tls
  # Specify your CA's public certificate here if using a private CA
  globalPrivateCaCerts:

  extraAnnotations:
    # if not using Astronomers built-in ingress controller, you MUST
    # explicitly set kubernetes.io/ingress.class here
    kubernetes.io/ingress.class: <ingressClass-name>

  authSidecar:  
    enabled: true
    repository: nginxinc/nginx-unprivileged # In airgapped installations, change this to specify your private registry
    tag: stable
```

If you use an Nginx, Traefik or Contour ingress controller, you need to configure additional values in your chart. For more information, read the following subsections.

### Required configuration for nginx

If you're using an nginx ingress controller, add the following configuration to your `config.yaml` file:

```yaml
global:
  extraAnnotations:
    nginx.ingress.kubernetes.io/proxy-body-size: 0
```

This setting disables Nginx's maximum allowed upload size, which prevents HTTP 413 (Request Entity Too Large) error and allows the Astro CLI to properly deploy DAGs to Astronomer Software's internal registry.

### Required configuration for traefik

If you're using a traefik ingress controller, add the following configuration to your `config.yaml` file:

```yaml
global:
  extraAnnotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
    traefik.ingress.kubernetes.io/router.tls: "true"
```

> **Note:** Depending on the version of Traefik, upgrading from using the default ingress controller to a Traefik controller might cause issues. If you are upgrading a platform that used the built-in ingress controller, manually delete the Astronomer Platform Ingress objects in the Astronomer Platform namespace before updating your `config.yaml` file. You can do so using the following commands:
>
>    ```sh
>    $ kubectl -n <your-platform-namespace> delete ingress -l release=<your-platform-release-name>
>    $ helm upgrade --install -f config.yaml --version=<your-platform-version> --namespace=<your-platform-namespace> <your-platform-release-name> astronomer/astronomer
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

> **Note:** Depending on the version of Contour, upgrading from using the default ingress controller to a Contour controller might cause issues. If you are upgrading a platform that used the built-in ingress controller, manually delete the Astronomer Platform Ingress objects in the Astronomer Platform namespace before updating your `config.yaml` file. You can do so using the following commands:
>
>    ```sh
>    $ kubectl -n <your-platform-namespace> delete ingress -l release=<your-platform-release-name>
>    $ helm upgrade --install -f config.yaml --version=<your-platform-version> --namespace=<your-platform-namespace> <your-platform-release-name> astronomer/astronomer

## Step 3: Apply Changes With Helm

If this is an existing installation, apply your updated configuration using the following command:

```bash
helm upgrade --install -f config.yaml --version=<your-platform-version> --namespace=<your-platform-namespace> <your-platform-release-name> astronomer/astronomer
```

If this is a new installation, continue through the standard installation steps to install this Helm chart.

## Configuration notes for OpenShift

OpenShift clusters with multitenant isolation enabled will need to explicitly allow traffic from the ingress controller's namespace to services associated with ingresses in other namespaces.

This is typically done by labeling the namespace containing your ingress controller with the `network.openshift.io/policy-group=ingress` label, but this may vary based on the specific policy and configuration on your cluster. For example, you might run the following:

```sh
kubectl label namespace/<ingress namespace> network.openshift.io/policy-group=ingress
```

For more information, see the [OpenShift documentation](https://docs.openshift.com/container-platform/4.1/networking/configuring-networkpolicy.html) on configuring network policy.

To allow traffic from multiple namespaces, you must also configure OpenShift's default route admission policy. To do so, run the following command:

```sh
kubectl -n openshift-ingress-operator patch ingresscontroller/default --patch '{"spec":{"routeAdmission":{"namespaceOwnership":"InterNamespaceAllowed"}}}' --type=merge
```

For more information about security implications for multi-tenant clusters, see the [Openshift Ingress operator documentation](https://docs.openshift.com/container-platform/4.9/networking/ingress-operator.html).
