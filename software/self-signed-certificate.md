---
title: 'Generate self-signed TLS certificates'

sidebar_label: 'Generate self-signed certificates'
id: self-signed-certificate
description: Generate a self-signed certificate to use with Astronomer Software.
---

This guide describes the steps to generate a self-signed certificate to use with Astronomer Software.

## Prerequisites

- [openssl](https://www.openssl.org/). You can install it through [Homebrew](https://formulae.brew.sh/formula/openssl@1.1) on MacOs, [Windows installer](http://gnuwin32.sourceforge.net/packages/openssl.htm) on Windows, or [`apt-get`](https://www.misterpki.com/how-to-install-openssl-on-ubuntu/) on Linux.

## Setup

Run the following commands to generate a self-signed certificate:
To create a self-signed SSL certificate, we need a private key and certificating signing request. 

> ⚠️When the `openssl req` command asks for a "challenge password", press return to leave the password empty. Kubernetes does not natively support challenge passwords for certificates stored as Secrets.

Run the following set of commands, and answer the questions when prompted. The `Common Name` must match the DNS chosen for the site at Step 1 above, such as (for example) `*.astro.example.com`. 

Create a private key. By default, a password must be provided. 
```bash
openssl genrsa -aes256 -passout pass:gsahdg -out server.pass.key 4096
```

Create a password-less second key based on the first key.
```bash
openssl rsa -passin pass:gsahdg -in server.pass.key -out server.key
```

Remove the first key file. 
```bash
rm server.pass.key
```

Create a Certificate Signing Request using the password-less private key.
```bash
openssl req -new -key server.key -out server.csr
```

The self-signed SSL certificate is generated from the private key (`server.key`) and certificate signing request (`server.csr`) files.

Make sure to add the appropriate `Subject Alternative Name` (SAN) in the extfile. 
SAN records must match the DNS entries for the base domain chosen at Step 1 above, such as (for example) `*.astro.example.com`.

```bash
openssl x509 -req -sha256 -days 365 -in server.csr \
-signkey server.key -out server.crt \
-extfile <(printf "subjectAltName=DNS:*.astro.example.com,DNS:astro.example.com")
```

The certificate file `server.crt` and private key file `server.key` can now be used to configure Astronomer Software.

# Inspect the generated self-signed certificate
Once the certificate is created, you can inspect its content with the following command:

```bash
openssl x509 -in  server.crt -text -noout
```

Make sure that the `X509v3 Subject Alternative Name` section of this report includes your Astronomer domain (`my-domain.com`) as well as the wildcard domain (`*.my-domain.com`).
If you are not using a wildcard domain, add SAN entries for all related Astronomer subdomains.