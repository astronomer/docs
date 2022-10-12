---
sidebar_label: 'Install the CLI'
title: 'Install the Astro CLI'
id: install-cli
description: Install and run the Astro CLI
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

This is where you'll find information about installing, upgrading, and uninstalling the Astro CLI.

## Install the Astro CLI

<Tabs
    defaultValue="mac"
    groupId= "install-the-astro-cli"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

Install the Astro CLI on a Mac operating system with a single command.

#### Prerequisites

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

If you specify only a major version, this command installs the latest minor or patch version available for the major version. For a list of all available versions, see the [CLI release notes](cli/release-notes.md). If you specify only a major version, this command installs the latest minor or patch version available for the major version. For a list of all available versions, see the [CLI release notes](cli/release-notes.md).

</TabItem>

<TabItem value="windows">

This is where you'll find information about installing the Astro CLI on a Windows operating system.

#### Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/windows/install/) for Windows.
- [Docker Engine](https://docs.docker.com/engine/install/) (v1.13.1 or higher).
- [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) enabled on your local machine.
-  Windows 10 or Windows 11.

#### Installation

1. Go to the [Releases page](https://github.com/astronomer/astro-cli/releases) of the Astro CLI GitHub repository, scroll to a CLI version, and then download the `.exe` file that matches the CPU architecture of your machine.

    For example, to install v1.0.0 of the Astro CLI on a Windows machine with an AMD 64 architecture, download `astro_1.0.0-converged_windows_amd64.exe`.

2. Rename the file to `astro.exe`.

3. Add the filepath for the directory containing the new `astro.exe` as a PATH environment variable. For example, if `astro.exe` is stored in `C:\Users\username\astro.exe`, you add `C:\Users\username` as your PATH environment variable. To learn more about configuring the PATH environment variable, see [How do I set or change the PATH system variable?](https://www.java.com/en/download/help/path.html).

4. Restart your machine.

</TabItem>

<TabItem value="linux">

This is where you'll find information about installing the Astro CLI on Linux.

#### Prerequisites

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

If you specify only a major version, this command installs the latest minor or patch version available for the major version. If you specify only a major version, this command installs the latest minor or patch version available for the major version. For a list of all available versions, see the [CLI release notes](cli/release-notes.md).

</TabItem>

</Tabs>


## Upgrade the CLI

<Tabs
    defaultValue="mac"
    groupId= "upgrade-the-cli"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

To upgrade the Astro CLI to the latest version, run the following command:

```sh
brew install astro
```

</TabItem>

<TabItem value="windows">

1. Delete the existing `astro.exe` file on your machine.

2. Go to the [Releases page](https://github.com/astronomer/astro-cli/releases) of the Astro CLI GitHub repository, scroll to a CLI version, and then download the `.exe` file that matches the CPU architecture of your machine.

     For example, to upgrade to v1.0.0 of the Astro CLI on a Windows machine with an AMD 64 architecture, you download `astro_1.0.0-converged_windows_amd64.exe`.

3. Rename the file to `astro.exe`.

4. Add the filepath for the directory containing the new `astro.exe` as a PATH environment variable. For example, if `astro.exe` was stored in `C:\Users\username\astro.exe`, you would add `C:\Users\username` as your PATH environment variable. To learn more about configuring the PATH environment variable, see [Java documentation](https://www.java.com/en/download/help/path.html).

5. Restart your machine.

</TabItem>

<TabItem value="linux">

To upgrade the Astro CLI to the latest version, run the following command:

```sh
curl -sSL install.astronomer.io | sudo bash -s
```

</TabItem>

</Tabs>

## Uninstall the CLI

<Tabs
    defaultValue="mac"
    groupId= "uninstall-the-cli"
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

The `astrocloud` executable is no longer maintained by Astronomer. Complete this migration if all of the following are true:

- You are an Astro user.
- You're currently using the `astrocloud` CLI executable.

For more information on Astro CLI version 1.0.0, see [Astro CLI Release Notes](cli/release-notes.md).

### Step 1: Uninstall `astrocloud`

<Tabs
    defaultValue="mac"
    groupId= "step-1-uninstall-astrocloud"
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

Install the latest version of `astro` on your machine. See [Install the CLI](cli/install-cli.md).

### Step 3: Migrate existing Astro projects

To run and deploy your existing Astro projects using the `astro` executable, you need to populate these projects with a new `.astro` directory.

1. In your terminal, go to the location of your Astro project.
2. Run `astro dev init` to generate a new `.astro` directory in your project. This subdirectory might be hidden in graphical file browsers. You can show hidden files using `⌘ + Shift + .` on Mac or by selecting **View > Hidden items** in Windows file explorer.

    If a prompt appears asking you about whether you want to create a project in a directory that isn't empty, enter `Yes`. The CLI only creates files that aren't in your directory. In this case, the only files that it creates are `./astro/test_dag_integrity_default.py` and `.astro/config.yaml`.

### Step 4: Migrate project configurations (_Optional_)

If you manually updated the `.astrocloud/config.yaml` file of an existing Astro project:

1. In your terminal, go to the location of your Astro project.
2. Copy the contents from `.astrocloud/config.yaml` into `.astro/config.yaml`.
3. Delete `.astrocloud/config.yaml` from your project.

### Step 5: Update CI/CD pipelines (_Optional_)

If you have an existing [CI/CD](ci-cd.md) pipeline that uses the `astrocloud` executable, update it to use `astro`. For example, in a GitHub Actions CI/CD pipeline you would update the following:

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
