---
title: 'Generate self-signed TLS certificates'
sidebar_label: 'Generate self-signed certificates'
id: self-signed-certificate
description: Generate a self-signed certificate to use with Astronomer Software.
---

This guide describes the steps to generate a self-signed certificate to use with Astronomer Software. You might want to complete this setup as part of [installing Astronomer Software on AWS](install-aws-standard.md).

Self-signed certificates are ideal for privately hosted internal applications, as well as in development and testing environments. Avoid using self-signed certificates in installations where the trust and identity of the certificate issuer are important.

## Prerequisites

- [openssl](https://www.openssl.org/). You can install it through [Homebrew](https://formulae.brew.sh/formula/openssl@1.1) on MacOs, [Windows installer](http://gnuwin32.sourceforge.net/packages/openssl.htm) on Windows, or [`apt-get`](https://www.misterpki.com/how-to-install-openssl-on-ubuntu/) on Linux.

## Setup

Run the following set of commands, and answer the questions when prompted.

1. Run the following command to create a private key:

    ```bash
    openssl genrsa -aes256 -passout pass:gsahdg -out server.pass.key 4096
    ```

2. Run the following command to make a password-less second key based on the first key you created:

    ```bash
    openssl rsa -passin pass:gsahdg -in server.pass.key -out server.key
    ```

3. Run the following command to delete the first key: 

    ```bash
    rm server.pass.key
    ```

4. Run the following command to create a certificate signing request using the password-less private key.
   You will be asked to provide information to sign the certificate. 
   Make sure the `Common Name` matches your DNS record, for example `*.astro.example.com`. 

    ```bash
    openssl req -new -key server.key -out server.csr
    ```

    When openssl asks for a challenge password, press Enter to leave the password empty. Kubernetes does not natively support challenge passwords for certificates stored as Secrets.

5. Run the following command to create the certificate from your private key and signing request:

    ```bash
    openssl x509 -req -sha256 -days 365 -in server.csr \
    -signkey server.key -out server.crt \
    -extfile <(printf "subjectAltName=DNS:*.astro.<your-basedomain>,DNS:astro.<your-basedomain>")
    ```

    Make sure the Subject Alternative Name matches the required domain and subdomains. To generate a wildcard certificate, both the base domain and the wildcard domain must be included. To generate a limited multi-domain certificate, add individual SAN entries for each subdomain.

The certificate file `server.crt` and private key file `server.key` can now be used in your Astronomer Software installation.

## Inspect your self-signed certificate

Run the following command to inspect your self-signed certificate:

```bash
openssl x509 -in server.crt -text -noout
```

Confirm that the `X509v3 Subject Alternative Name` section of the certificate includes your Astronomer base domain (`<your-basedomain>`) as well as the wildcard domain (`*.<your-basedomain>`).

