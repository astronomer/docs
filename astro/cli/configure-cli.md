---
sidebar_label: 'Configure the CLI'
title: 'Configure the Astro CLI'
id: configure-cli
description: Install, upgrade, and manage settings for the Astro CLI.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

This is where you'll find information about installing, upgrading, and uninstalling the Astro CLI.

<Tabs
    defaultValue="mac"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

## Install the Astro CLI

This is where you'll find information about installing the Astro CLI on a Mac operating system.

#### Prerequisites

To use the Astro CLI on Mac, you must have:

- [Homebrew](https://brew.sh/)
- [Docker Desktop](https://docs.docker.com/get-docker/) (v18.09 or higher).

#### Installation

To install the latest version of the Astro CLI, run the following command:

```sh
brew install astro
```

To install a specific version of the Astro CLI, specify the version you want to install at the end of the command:

```sh
brew install astro@<major.minor.patch-version>
```

If you specify only a major version, this command installs the latest minor or patch version available for the major version.

</TabItem>

<TabItem value="windows">

## Install the Astro CLI

This is where you'll find information about installing the Astro CLI on a Windows operating system.

#### Prerequisites

To use the Astro CLI on Windows, you must have:

- [Docker Desktop](https://docs.docker.com/desktop/windows/install/) for Windows.
- [Docker Engine](https://docs.docker.com/engine/install/) (v1.13.1 or higher).
- [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) enabled on your local machine.
-  Windows 10 or Windows 11.

#### Installation

1. Go to the [**Releases** page of the Astro CLI GitHub repository](https://github.com/astronomer/astro-cli/releases). Based on your desired CLI version and the CPU architecture of your machine, download one of the `.zip` files available on this page.

    For example, to install v1.0.0 of the Astro CLI on a Windows machine with an AMD 64 architecture, download `astro_1.0.0-converged_windows_amd64.zip`.

2. If the `.zip` file does not automatically unzip, run the following command to unzip the executable:

    ```sh
    tar -xvzf .\astrocli.tar.gz
    ```

3. Add the filepath for the directory containing `astro.exe` as a PATH environment variable. For example, if `astro.exe` was stored in `C:\Users\username\astro.exe`, you would add `C:\Users\username` as your PATH environment variable. To learn more about configuring the PATH environment variable, see [Java documentation](https://www.java.com/en/download/help/path.html).

4. Restart your machine.

</TabItem>

<TabItem value="linux">

## Install the Astro CLI

This is where you'll find information about installing the Astro CLI on Linux.

#### Prerequisites

To use the Astro CLI on Linux, you must have:

- [Docker Engine](https://docs.docker.com/engine/install/) (v1.13.1 or higher).

#### Installation

Run the following command to install the latest version of the Astro CLI directly to `PATH`:

```sh
curl -sSL install.astronomer.io | sudo bash -s
```

To install a specific version of the CLI, specify the version number as a flag at the end of the command. For example, to install v1.1.0 of the CLI, you would run:

```sh
curl -sSL install.astronomer.io | sudo bash -s -- v1.1.0
```

If you specify only a major version, this command installs the latest minor or patch version available for the major version.

</TabItem>

</Tabs>


## Upgrade the CLI

<Tabs
    defaultValue="mac"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

To upgrade the Astro CLI to the latest version, you can run the same command as you did to install the CLI for the first time:

```sh
brew install astro
```

</TabItem>

<TabItem value="windows">

To upgrade the Astro CLI on Windows:

1. Delete the existing `astro.exe` file on your machine.

2. Go to the [**Releases** page of the Astro CLI GitHub repository](https://github.com/astronomer/astro-cli/releases). Based on the version of the CLI you want and your CPU architecture, download one of the `.zip` files available on this page.

     For example, to upgrade to v1.0.0 of the Astro CLI on a Windows machine with an AMD 64 architecture, you download `astro_1.0.0-converged_windows_amd64.zip`.

3. If the `.zip` file does not automatically unzip, run the following command to unzip the executable:

    ```sh
    tar -xvzf .\astrocli.tar.gz
    ```

4. Add the filepath for the directory containing the new `astro.exe` as a PATH environment variable. For example, if `astro.exe` was stored in `C:\Users\username\astro.exe`, you would add `C:\Users\username` as your PATH environment variable. To learn more about configuring the PATH environment variable, see [Java documentation](https://www.java.com/en/download/help/path.html).

5. Restart your machine.

</TabItem>

<TabItem value="linux">

To upgrade to the latest version of the Astro CLI, run:

```sh
curl -sSL install.astronomer.io | sudo bash -s
```

</TabItem>

</Tabs>

## Uninstall the CLI

<Tabs
    defaultValue="mac"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

To uninstall the Astro CLI on Mac, run:

```sh
brew uninstall astro
```

</TabItem>

<TabItem value="windows">

To uninstall the Astro CLI on Windows:

1. Delete the filepath for `astro.exe` from your Windows PATH environment variable.
2. Delete `astro.exe`.

</TabItem>

<TabItem value="linux">

To uninstall the Astro CLI on Linux, run the following command:

```sh
sudo rm /usr/local/bin/astro
```

</TabItem>

</Tabs>

## Migrate from `astrocloud` to `astro`

A new `astro` executable for the Astro CLI is now available. Complete this migration if all of the following are true:

- You are an Astro user.
- You're currently using the `astrocloud` CLI executable.

For more information on Astro CLI v1.0.0, see [Astro CLI Release Notes](cli/release-notes.md).

### Step 1: Uninstall `astrocloud`

<Tabs
    defaultValue="mac"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

To uninstall `astrocloud` on Mac, run:

```sh
brew uninstall astronomer/cloud/astrocloud
```

</TabItem>

<TabItem value="windows">

To uninstall `astrocloud` on Windows:

1. Delete the filepath for `astrocloud.exe` from your Windows PATH environment variable.
2. Delete `astrocloud.exe` from your machine.

</TabItem>

<TabItem value="linux">

To uninstall `astrocloud` on Linux:

1. Delete the filepath for `astrocloud.exe` from your Linux PATH environment variable.
2. Delete `astrocloud.exe` from your machine.

</TabItem>

</Tabs>

### Step 2: Install Astro CLI v1.0+

Once you've uninstalled the `astrocloud` executable, install the latest version of `astro` on your machine.

For instructions, see [Install the CLI](cli/configure-cli.md#install-the-cli).

### Step 3: Migrate existing Astro projects

In order to run and deploy your existing Astro projects using the `astro` executable, you need to populate these projects with a new `.astro` directory of files. For any existing Astro projects on your machine:

1. In your terminal, open your Astro project.
2. Run `astro dev init` to generate a new `.astro` directory in your project. This subdirectory might be hidden in graphical file browsers. You can show hidden files using `⌘ + Shift + .` on Mac or by selecting **View > Hidden items** in Windows file explorer.

    If the CLI prompts you about whether you want to create a project in a non-empty directory, enter `Yes`. The CLI will only create files that aren't yet in your directory. In this case, the only files that it creates are `./astro/test_dag_integrity_default.py` and `.astro/config.yaml`.

### Step 4: Migrate project configurations (_Optional_)

If you manually updated the `.astrocloud/config.yaml` file of an existing Astro project:

1. In your terminal, open your Astro project.
2. Copy the contents from `.astrocloud/config.yaml` into `.astro/config.yaml`.
3. Delete `.astrocloud/config.yaml` from your project.

### Step 5: Update CI/CD pipelines (_Optional_)

If you have an existing [CI/CD](ci-cd.md) pipeline using the old `astrocloud` executable, update it to use `astro`. For example, in a GitHub Actions CI/CD pipeline you would update the following:

```yaml
# Before:
    - name: Deploy to Astro
      run: |
        brew install astronomer/cloud/astrocloud
        astrocloud deploy ${{ secrets.DEPLOYMENT_ID }}

# After:
    - name: Deploy to Astro
      run: |
        curl -sSL install.astronomer.io | sudo bash -s
        astro deploy ${{ secrets.DEPLOYMENT_ID }}
```
