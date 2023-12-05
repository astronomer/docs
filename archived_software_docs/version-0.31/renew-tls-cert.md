---
title: 'Renew TLS certificates on Astronomer Software'
sidebar_label: 'Renew a TLS certificate'
id: renew-tls-cert
description: Update and auto-renew your organization's TLS certificate for Astronomer Software.
---

After you set up a transport layer security (TLS) certificate for Astronomer, you'll need to establish a process for periodically renewing the certificate. The following methods are available for certificate renewal:

* **Automatic renewal**: Let's Encrypt provides a service that automatically renews your TLS certificate every 90 days. Astronomer recommends this option for smaller organizations where the DNS administrator and cluster administrator are either the same person or on the same team.
* **Manual renewal**: Manual renewal works similarly to the initial certificate creation process, except that you replace your existing certificate by creating a new certificate. Astronomer recommends this method for large organizations that have their own processes for issuing certificates.

:::warning

By default, [Certbot](https://certbot.eff.org/) uses Elliptic Curve Digital Signature Algorithm (ECDSA) keys to sign certificates. If you're using Certbot to renew your TLS certificate, you must include `-key-type rsa --rsa-key-size 2048` in your command to sign your certificate with an RSA key. If you don't use RSA keys, deploys fail and error messages appear in the registry and Houston logs. For example, you can run the following command to sign your certificate with an RSA key:

```sh
sudo certbot certonly --manual --preferred-challenges=dns -d -d *. --key-type=rsa
```

:::

## Automatically renew TLS certificates Using Let's Encrypt

[Let's Encrypt](https://letsencrypt.org/) is a certificate authority that provides free, 90-day certificates using the ACME protocol. You can use the Cert Manager project for Kubernetes to automatically renew certificates. When you renew a TLS certificate with Let's Encrypt, you must specify the RSA key type to sign certificates or your deploys will fail and error messages will appear in the registry and Houston logs.

1. Install the Kubernetes Cert Manager by following [the official installation guide](https://cert-manager.io/docs/installation/).

2. If you're running Astronomer on AWS, grant your nodes access to Route 53 by adding the following CloudFormation snippet to your nodes' Instance Profile (if you don't use AWS, complete whatever setup is necessary to authenticate Cert Manager to your DNS):

    ```yaml
    Type: "AWS::IAM::Role"
    Properties:
      RoleName: instance-profile-role
      Policies:
        - PolicyName: instance-profile-policy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action: route53:GetChange
                Resource: arn:aws:route53:::change/*
              - Effect: Allow
                Action:
                  - route53:ChangeResourceRecordSets
                  - route53:ListResourceRecordSets
                # Use the second Resource format if you're updating this through the AWS UI
                Resource: !Sub arn:aws:route53:::hostedzone/${HostedZoneIdLookup.HostedZoneId}
              - Effect: Allow
                Action: route53:ListHostedZonesByName
                Resource: '*'
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: "Allow"
            Principal:
              Service:
                - "ec2.amazonaws.com"
            Action:
              - "sts:AssumeRole"
    ```

    For more information on how to complete this setup, refer to [AWS documentation](https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html).

3. Create a "ClusterIssuer" resource that declares how requests for certificates will be fulfilled. To do so, first create a `clusterissuer.yaml` file with the following values:

    ```yaml
    apiVersion: cert-manager.io/v1
    kind: ClusterIssuer
    metadata:
        name: letsencrypt-prod
    spec:
        acme:
            email: <your-email>
            server: https://acme-v02.api.letsencrypt.org/directory
            privateKeySecretRef:
                name: cert-manager-issuer-secret-key
            solvers:
            - selector: {}
              dns01:
                 route53:
                    region: <your-server-region>
    ```

    Then, create the ClusterIssuer by running the following command:

    ```sh
    kubectl apply -f clusterissuer.yaml -n astronomer
    ```

4. Create a "Certificate" resource that declares the type of certificate you'll request from Let's Encrypt. To do so, first create a `certificate.yaml` file, replacing `BASE_DOMAIN` with yours:

    ```yaml
    apiVersion: cert-manager.io/v1
    kind: Certificate
    metadata:
        name: acme-crt
    spec:
        secretName: astronomer-tls
        dnsNames:
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
        issuerRef:
            name: letsencrypt-prod
            kind: ClusterIssuer
            group: cert-manager.io
    ```

    Then, create the certificate by running the following command and waiting a few minutes:

    ```sh
    kubectl apply -f certificate.yaml -n astronomer
    ```

5. Ensure that the certificate was created by running:
   ```sh
   kubectl get certificates -n astronomer
   ```

6. Note your certificate name for when you create a Kubernetes TLS secret and push it to your Software configuration as described in the Software installation guide ([AWS](install-aws-standard.md#step-5-create-a-kubernetes-tls-secret)/[GCP](install-gcp-standard.md#step-5-create-a-kubernetes-tls-secret)/[AKS](install-azure-standard.md/#step-5-create-a-kubernetes-tls-secret)).

## Manually renew TLS certificates

Use a manual process to renew TLS certificates when your organization has its own process for requesting and renewing TLS certificates. When you renew a TLS certificate with Let's Encrypt, you must specify the RSA key type to sign certificates or your deploys will fail and error messages will appear in the registry and Houston logs.

1. Delete your current TLS certificate by running the following command:
   ```sh
   kubectl delete secret astronomer-tls -n astronomer
   ```

2. Follow the instructions for requesting a TLS certificate from your organization's security team as described in [Step 4: Configure TLS](install-aws-standard.md#step-4-configure-tls). The linked guide is written for users installing Astronomer on AWS, but this step is the same regardless of which service you use.

3. Restart your Houston, nginx, and registry pods to begin using the new certificate by running the following commands:
   ```sh
   kubectl rollout restart deployments -n astronomer
   kubectl rollout restart statefulsets -n astronomer
   ```
