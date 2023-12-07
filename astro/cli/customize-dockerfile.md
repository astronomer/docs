---
sidebar_label: 'Customize your Astro project Dockerfile'
title: 'Customize your Dockerfile'
id: customize-dockerfile
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';


By default, the Astro project Dockerfile only includes a `FROM` statement that specifies your Astro Runtime version. However, you can extend your Dockerfile to use a different distribution or run additional buildtime arguments. Use this document to learn which Dockerfile customizations are supported both locally and on Astro.

## Prerequisites

- An [Astro project](develop-project.md#create-an-astro-project)

## Use an alternative Astro Runtime distribution

Starting with Astro Runtime 9, each version of Astro Runtime has a separate distribution for each currently supported Python version. Use an alternative Python distribution if any of your dependencies require a Python version other than the [default Runtime Python version](runtime-image-architecture.md#python-versioning).

To use a specific Python distribution, update the first line in your Astro project `Dockerfile` to reference the required distribution:

```text
FROM quay.io/astronomer/astro-runtime:<runtime-version>-python-<python-version>
```

For example, to use Python 3.10 with Astro Runtime version 9.0.0, you update the first line of your Dockerfile to the following:

```text
FROM quay.io/astronomer/astro-runtime:9.0.0-python-3.10
```

## Run commands on build

To run additional commands as your Astro project is built into a Docker image, add them to your `Dockerfile` as `RUN` commands. These commands run as the last step in the image build process.

For example, if you want to run `ls` when your image builds, your `Dockerfile` would look like this:

<pre><code parentName="pre">{`FROM quay.io/astronomer/astro-runtime:${siteVariables.runtimeVersion}
RUN ls
`}</code></pre>

This is supported both on Astro and in the context of local development.

## Add a CA certificate to an Astro Runtime image

If you need your Astro Deployment to communicate securely with a remote service using a certificate signed by an untrusted or internal certificate authority (CA), you need to add the CA certificate to the trust store inside your Astro project's Docker image.

1. In your Astro project `Dockerfile`, add the following entry below the existing `FROM` statement which specifies your Astro Runtime image version:

    ```docker
    USER root
    COPY <internal-ca.crt> /usr/local/share/ca-certificates/<your-company-name>/
    RUN update-ca-certificates
    USER astro
    ```
    
2. Optional. Add additional `COPY` statements before the `RUN update-ca-certificates` stanza for each CA certificate your organization is using for external access.

3. [Restart your local environment](cli/develop-project.md#restart-your-local-environment) or deploy to Astro. See [Deploy code](deploy-code.md).
