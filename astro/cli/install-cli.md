---
sidebar_label: 'Install the CLI'
title: 'Install the Astro CLI'
id: install-cli
description: "Instructions for installing, upgrading, and uninstalling the Astro command-line interface (CLI)."
toc_max_heading_level: 2
toc_min_heading_level: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

This document explains all of the possible ways to install, upgrade, and uninstall the Astro CLI. Install the Astro CLI to start running Airflow locally or to manage Astro from your terminal.

:::info

If you can't install the Astro CLI on your local machine, you can still run Astro CLI commands and deploy to Astro using [GitHub Actions](first-dag-github-actions.md).

:::

## Install the Astro CLI

<Tabs
    defaultValue="mac"
    groupId= "install-the-astro-cli"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows with winget', value: 'windowswithwinget'},
        {label: 'Windows (Manual)', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

Install the Astro CLI on Mac OS with a single command.

### Prerequisites

- [Homebrew](https://brew.sh/)
- A container service like [Docker Desktop](https://docs.docker.com/get-docker/) (v18.09 or higher)

By default, the Astro CLI uses Docker as its container management engine for running Airflow locally. However, if your organization uses Podman to run and manage containers, you can configure the Astro CLI to use it instead. See [Run the Astro CLI with Podman](https://docs.astronomer.io/astro/cli/use-podman?tab=mac#configure-the-astro-cli-to-use-podman) for prerequisites and configuration steps.

### Installation

To install the latest version of the Astro CLI, run the following command:

```sh
brew install astro
```

To install a specific version of the Astro CLI, specify the version you want to install at the end of the command. For example, to install Astro CLI version {{CLI_VER_LATEST}}, you would run the following command:

```sh
brew install astro@{{CLI_VER_LATEST}}
```

If you specify only a major version, this command installs the latest minor or patch version available for the major version. For a list of all available versions, see the [CLI release notes](/astro/cli/release-notes.md).

### Confirmation

To verify that the correct Astro CLI version was installed, run:

```sh
astro version
```

### Resolve installation issues

Follow this procedure when Homebrew fails to install the latest Astro CLI version or the error `No formulae or casks found for astro@<major.minor.patch-version>` appears. To troubleshoot other Homebrew issues, see [Common Issues](https://docs.brew.sh/Common-Issues) in the Homebrew documentation.

1. If the install process is not working, run the following command to update Homebrew and all package definitions (formulae):

    ```sh
    brew update
    ```

2. Re-run the installation again:

    ```sh
    brew install astro
    ```

3. If this is the first time you're installing the CLI and updating Homebrew doesn't work, check to see if `astronomer/tap` is in your [Homebrew tap list](https://docs.brew.sh/Taps):

    ```sh
    brew tap astronomer/tap
    ```

    If `astronomer/tap` is in your tap list and you still can't install the Astro CLI, you might be experiencing a different issue. See [Common Issues](https://docs.brew.sh/Common-Issues) in the Homebrew documentation.

4. Run the following command to install the Astronomer CLI:

   ```sh
   brew install astro
   ```

</TabItem>

<TabItem value="windowswithwinget">

Starting with Astro CLI version 1.6, you can use the Windows Package Manager winget command-line tool to install the Astro CLI. To install an older version of the Astro CLI, you'll need to follow the [alternate Windows installation process](https://docs.astronomer.io/astro/cli/install-cli?tab=windows#install-the-astro-cli).

The winget command line tool is supported on Windows 10 1709 (build 16299) or later, and is bundled with Windows 11 and modern versions of Windows 10 by default as the App Installer. If you're running an earlier version of Windows 10 and you don't have the App Installer installed, you can download it from the [Microsoft Store](https://apps.microsoft.com/store/detail/app-installer/9NBLGGH4NNS1?hl=en-ca&gl=ca). If you've installed the App Installer previously, make sure you're using the latest version before running commands.

### Prerequisites

- Microsoft Hyper-V enabled. See [Install Hyper-V On Windows]( https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v) or [Step-By-Step: Enabling Hyper-V on Windows 11](https://techcommunity.microsoft.com/t5/educator-developer-blog/step-by-step-enabling-hyper-v-for-use-on-windows-11/ba-p/3745905).
- The latest version of the Windows [App Installer](https://apps.microsoft.com/store/detail/app-installer/9NBLGGH4NNS1?hl=en-ca&gl=ca).
- Windows 10 1709 (build 16299) or later or Windows 11.
- A container service, like [Docker Desktop](https://docs.docker.com/get-docker/) (v18.09 or higher).

By default, the Astro CLI uses Docker as its container management engine for running Airflow locally. However, if your organization uses Podman to run and manage containers, you can configure the Astro CLI to use it instead. See [Run the Astro CLI with Podman](https://docs.astronomer.io/astro/cli/use-podman?tab=mac#configure-the-astro-cli-to-use-podman) for prerequisites and configuration steps.

### Installation

1. Open Windows PowerShell as an administrator and then run the following command:

    ```sh
    winget install -e --id Astronomer.Astro
    ```

    To install a specific version of the Astro CLI, specify the version you want to install at the end of the command. For example, running the following command specifies the latest available version of the Astro CLI:

    ```sh
    winget install -e --id Astronomer.Astro -v {{CLI_VER_LATEST}}
    ```

1. Run the following command to access the location of the CLI executable:

    ```sh
    $env:path.split(";")
    ```

    From the text that appears, copy the path for the Astro CLI executable. It should be similar to `C:\Users\myname\AppData\Local\Microsoft\WinGet\Packages\Astronomer.Astro_Microsoft.Winget.Source_8wekyb3d8bbwe`.

2. Paste the path into File Explorer or open the file path in terminal, then rename the Astro executable to `astro.exe`.

3. Run `astro version` to confirm the Astro CLI is installed properly.

### Resolve installation issues

If an error message appears indicating that the term winget is not recognized as an internal or external command when you attempt to run winget commands, see this [troubleshooting document](https://github.com/microsoft/winget-cli/tree/master/doc/troubleshooting#common-issues) provided by Microsoft.

If you're still struggling to install the Astro CLI with winget, retry the install using the alternative instructions in [Windows (Manual)](https://docs.astronomer.io/astro/cli/install-cli?tab=windows#install-the-astro-cli).

</TabItem>

<TabItem value="windows">

Manually installing the Astro CLI to Windows is recommended only if you're upgrading from Astro CLI version 1.5.1 or earlier to version 1.6.0 or later. Starting with Astro CLI version 1.6.0, Astronomer recommends using Windows Package Manager winget command-line tool to install the Astro CLI. See [Windows with winget](install-cli.md?tab=windows%20with%20winget#install-the-astro-cli).

### Prerequisites

- Microsoft Hyper-V enabled. See [Install Hyper-V On Windows]( https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v) or [Step-By-Step: Enabling Hyper-V on Windows 11](https://techcommunity.microsoft.com/t5/educator-developer-blog/step-by-step-enabling-hyper-v-for-use-on-windows-11/ba-p/3745905).
- Windows 10 or Windows 11.
- A container service like [Docker Desktop](https://docs.docker.com/desktop/windows/install/).

By default, the Astro CLI uses Docker as its container management engine. However, if your organization uses Podman to run and manage containers, you can configure the Astro CLI to use it instead. See [Run the Astro CLI with Podman](https://docs.astronomer.io/astro/cli/use-podman?tab=mac#configure-the-astro-cli-to-use-podman) for prerequisites and configuration steps.

### Installation

1. Go to the [Releases page](https://github.com/astronomer/astro-cli/releases) of the Astro CLI GitHub repository, scroll to a CLI version, and then download the `.exe` file that matches the CPU architecture of your machine.

    For example, to install v1.18.2 of the Astro CLI on a Windows machine with an AMD 64 architecture, download `astro_1.18.2_windows_amd64.exe`.

2. Rename the file to `astro.exe`.

3. Add the filepath for the directory containing the new `astro.exe` as a PATH environment variable. For example, if `astro.exe` is stored in `C:\Users\username\astro.exe`, you add `C:\Users\username` as your PATH environment variable. To learn more about configuring the PATH environment variable, see [How do I set or change the PATH system variable?](https://www.java.com/en/download/help/path.html).

4. Restart your machine.

</TabItem>

<TabItem value="linux">

### Prerequisites

- (Optional) [Docker Desktop](https://docs.docker.com/get-docker/) (v18.09 or higher).

By default, the Astro CLI uses Docker as its container management engine for running Airflow locally. However, if your organization uses Podman to run and manage containers, you can configure the Astro CLI to use it instead. See [Run the Astro CLI with Podman](https://docs.astronomer.io/astro/cli/use-podman?tab=mac#configure-the-astro-cli-to-use-podman) for prerequisites and configuration steps.

### Installation

Run the following command to install the latest version of the Astro CLI directly to `PATH`:

```sh
curl -sSL install.astronomer.io | sudo bash -s
```

To install a specific version of the CLI, specify the version number as a flag at the end of the command. For example, to install the most recent release of the CLI, you would run:

```sh
curl -sSL install.astronomer.io | sudo bash -s -- v{{CLI_VER_LATEST}}
```

If you specify only a major version, this command installs the latest minor or patch version available for the major version. If you specify only a major version, this command installs the latest minor or patch version available for the major version. For a list of all available versions, see the [CLI release notes](cli/release-notes.md).

</TabItem>

</Tabs>

## Upgrade the Astro CLI

The Astro CLI contains no breaking changes between minor versions within the same major version. Therefore, Astronomer recommends always using the latest minor version of the Astro CLI with in your major version.

<Tabs
    defaultValue="mac"
    groupId= "upgrade-the-cli"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows with winget', value: 'windowswithwinget'},
        {label: 'Windows (Manual)', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

Run the following command to upgrade the Astro CLI to the latest version:

```sh
brew upgrade astro
```

</TabItem>

<TabItem value="windowswithwinget">

Starting with Astro CLI version 1.6, you can use the winget command line tool to upgrade the Astro CLI. To upgrade the Astro CLI to the latest version, open Windows PowerShell as an administrator and run the following command:

```sh
winget install -e --id Astronomer.Astro
```

Note that if you're upgrading from Astro CLI version 1.5.1 or earlier to a later Astro CLI version, you still need to [install the upgrade version manually](https://docs.astronomer.io/astro/cli/install-cli?tab=windows#upgrade-the-cli).

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

## Uninstall the Astro CLI

<Tabs
    defaultValue="mac"
    groupId= "uninstall-the-cli"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows with winget', value: 'windowswithwinget'},
        {label: 'Windows (Manual)', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

To uninstall the Astro CLI on Mac, run:

```sh
brew uninstall astro
```

</TabItem>

<TabItem value="windowswithwinget">

Starting with Astro CLI version 1.6, you can use the winget command line tool to uninstall the Astro CLI. To uninstall an older version of the Astro CLI, you'll need to follow the [alternate Windows uninstall process](https://docs.astronomer.io/astro/cli/install-cli?tab=windows#uninstall-the-cli).

To uninstall the Astro CLI, open Windows PowerShell as an administrator and run the following command:

```sh
winget uninstall -e --id Astronomer.Astro
```

</TabItem>

<TabItem value="windows">

To uninstall the Astro CLI on Windows:

1. Delete the filepath for `astro.exe` from your Windows PATH environment variable.
2. Delete `astro.exe`.

</TabItem>

<TabItem value="linux">

Run the following command to uninstall the Astro CLI on Linux:

```sh
sudo rm /usr/local/bin/astro
```

</TabItem>

</Tabs>
