---
sidebar_label: 'Private Python packages'
title: 'Install Python packages from private sources'
id: private-python-packages
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Python packages can be installed into your image from both public and private sources. To install packages listed on private PyPI indices or a private git-based repository, you need to complete additional configuration in your project.

Depending on where your private packages are stored, use one of the following setups to install these packages to an Astro project by customizing your Runtime image.

:::info

Deploying a custom Runtime image with a CI/CD pipeline requires additional configurations. For an example implementation, see the GitHub Actions CI/CD templates for [Astro](https://www.astronomer.io/docs/astro/ci-cd-templates/github-actions-template?tab=custom#setup) and [Software](https://www.astronomer.io/docs/software/ci-cd#github-actions-cicd).

:::

## Setup

<Tabs
    defaultValue="github"
    groupId= "install-python-packages-from-private-sources"
    values={[
        {label: 'Private GitHub Repo', value: 'github'},
        {label: 'Private PyPi Index', value: 'pypi'},
    ]}>
<TabItem value="github">

#### Install Python packages from private GitHub repositories

This topic provides instructions for building your Astro project with Python packages from a private GitHub repository.

Although GitHub is used in this example, you should be able to complete the process with any hosted Git repository.

:::info

The following setup has been validated with only a single SSH key. You might need to modify this setup when using more than one SSH key per Docker image.

:::

#### Prerequisites

- The [Astro CLI](cli/overview.md)
- An [Astro project](cli/develop-project.md#create-an-astro-project).
- Custom Python packages that are [installable with pip](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- A private GitHub repository for each of your custom Python packages
- A [GitHub SSH private key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) authorized to access your private GitHub repositories

This setup assumes that each custom Python package is hosted within its own private GitHub repository. Installing multiple custom packages from a single private GitHub repository is not supported.

:::warning

If your organization enforces SAML single sign-on (SSO), you must first authorize your key to be used with that authentication method. See [Authorizing an SSH key for use with SAML single sign-on](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-an-ssh-key-for-use-with-saml-single-sign-on).

:::

#### Step 1: Specify the private repository in your project

To add a Python package from a private repository to your Astro project, specify the Secure Shell (SSH) URL for the repository in a new `private-requirements.txt` file. Use the following format for the SSH URL:

```
git+ssh://git@github.com/<your-github-organization-name>/<your-private-repository>.git
```

For example, to install `mypackage1` and `mypackage2` from `myorganization`, add the following to your `private-requirements.txt` file:

```
git+ssh://git@github.com/myorganization/mypackage1.git
git+ssh://git@github.com/myorganization/mypackage2.git
```

This example assumes that the name of each of your Python packages is identical to the name of its corresponding GitHub repository. In other words,`mypackage1` is both the name of the package and the name of the repository.

#### Step 2: Update Dockerfile

1. (Optional) Copy and save any existing build steps in your `Dockerfile`.

2. Add the following to your `packages.txt` file:

    ```bash
    openssh-client
    git
    ```

3. In your Dockerfile, add the following instructions:

    ```docker
    USER root
    RUN mkdir -p -m 0700 ~/.ssh && \
        echo "github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl" >> ~/.ssh/known_hosts

    COPY private-requirements.txt .
    RUN --mount=type=ssh,id=github pip install --no-cache-dir --requirement private-requirements.txt
    USER astro

    ENV PATH="/home/astro/.local/bin:$PATH"
    ```

    In order, these instructions:

    - Switch to `root` user for SSH setup and installation from private repo
    - Add the fingerprint for GitHub to `known_hosts`
    - Copy your `private-requirements.txt` file into the image
    - Install Python-level packages from your private repository as specified in your `private-requirements.txt` file. This securely mounts your SSH key at build time, ensuring that the key itself is not stored in the resulting Docker image filesystem or metadata.
    - Switch back to `astro` user
    - Add the user bin directory to `PATH`

  :::info

  See GitHub's documentation for all available [SSH key fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints).

  If your repository isn't hosted on GitHub, replace the fingerprint with one from where the package is hosted. Use `ssh-keyscan` to generate the fingerprint.

  :::

#### Step 3: Build a custom Docker image

1. Run the following command to automatically generate a unique image name:

    ```sh
    image_name=astro-$(date +%Y%m%d%H%M%S)
    ```

2. Run the following command to create a new Docker image from your `Dockerfile`. Replace `<ssh-key>` with your SSH private key file name.

    ```sh
    DOCKER_BUILDKIT=1 docker build -f Dockerfile --progress=plain --ssh=github="$HOME/.ssh/<ssh-key>" -t $image_name .
    ```

3. (Optional) Test your DAGs locally. See [Restart your local environment](cli/run-airflow-locally.md#restart-a-local-airflow-environment).

4. Deploy the image to Astro using the Astro CLI:

    ```sh
    astro deploy --image-name $image_name
    ```

Your Astro project can now utilize Python packages from your private GitHub repository.

</TabItem>

<TabItem value="pypi">

#### Install Python packages from a private PyPI index

Installing Python packages on Astro from a private PyPI index is required for organizations that deploy a [private PyPI server (`private-pypi`)](https://pypi.org/project/private-pypi/) as a secure layer between pip and a Python package storage backend, such as GitHub, AWS, or a local file system or managed service.

To complete this setup, you’ll specify your privately hosted Python packages in `requirements.txt`, create a custom Docker image that changes where pip looks for packages, and then build your Astro project with this Docker image.

#### Prerequisites

- An [Astro project](cli/develop-project.md#create-an-astro-project)
- A private PyPI index with a corresponding username and password

#### Step 1: Add Python packages to your Astro project

To install a Python package from a private PyPI index, add the package name and version to the `requirements.txt` file of your Astro project. If you don’t specify a version, the latest version is installed. Use the same syntax that you used when you added public packages from [PyPI](https://pypi.org). Your `requirements.txt` file can contain both publicly accessible and private packages.

:::caution

Make sure that the name of any privately hosted Python package doesn’t conflict with the name of other Python packages in your Astro project. The order in which pip searches indices might produce unexpected results.

:::

#### Step 2: Define your extra index URL

Create a new file called `indexurl.txt` that contains the extra index URL used to access your private PuPI index. For example:

```text
https://myuser:example.com/api/pypi/pypi/simple
```

Ensure that this file is accessible from your Astro project. You will mount this value as a secret when you build your Astro project image.

#### Step 3: Update Dockerfile

1. (Optional) Copy and save any existing build steps in your `Dockerfile`.

2. In your `Dockerfile`, add the following to the `FROM` line which specifies your Runtime image. For example, if you use Runtime X.Y.Z, your `FROM` line is:

    ```text
    FROM quay.io/astronomer/astro-runtime:X.Y.Z-base
    ```

   :::info

   If you use the default distribution of Astro Runtime, replace your existing image with its corresponding `-base` image. The `-base` distribution is built to be customizable and does not include default build logic. For more information on Astro Runtime distributions, see [Distributions](runtime-image-architecture.mdx#distribution).

   :::

3. After the `FROM` line specifying your Runtime image, add the following configuration:

    ```docker
    # Install OS-Level packages
    COPY packages.txt .
    USER root
    RUN apt-get update && cat packages.txt | xargs apt-get install -y

    # Install Python packages
    COPY requirements.txt .
    RUN --mount=type=secret,id=indexurl \
        pip install --no-cache-dir --root-user-action=ignore -r requirements.txt --index-url=$(cat /run/secrets/indexurl)

    USER astro
    COPY --chown=astro:0 . .
    ```

    In order, these commands:

    - Install any OS-level packages specified in `packages.txt`.
    - Add `PIP_EXTRA_INDEX_URL` as an environment variable that contains authentication information for your private PyPI index.
    - Install public and private Python-level packages from your `requirements.txt` file.


#### Step 4: Build a custom Docker image

1. Run the following command to test your DAGs locally with your privately installed packages:

    ```sh
    astro dev start --build-secrets id=indexurl,env=INDEX_URL_ENV_VAR
    ```

2. (Optional) Run the following command to deploy to Astro:

    ```sh
    astro deploy --build-secrets id=indexurl,env=INDEX_URL_ENV_VAR
    ```

Your Astro project can now use Python packages from your private PyPi index.

</TabItem>
</Tabs>