---
title: "Install the Astro CLI"
sidebar_label: "Install the CLI"
id: install-cli
description: Establish a local testing environment and deploy to Astronomer Software from the CLI.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

## Overview

This guide provides instructions for how to install the Astro CLI.

The Astro CLI is the easiest way to run Apache Airflow on your machine. From the Astro CLI, you can run a local Apache Airflow environment with a dedicated Webserver, Scheduler and Postgres Database. Once you create an Astronomer Software project, you can customize it (for example, add Python or OS-level packages or add plugins) and test it on your local machine.

You can also use the CLI to:

- Authenticate to Astronomer Software.
- List the Astro Workspace and Deployments you can access.
- Deploy a project to Software.

## Install the Astro CLI

<Tabs
    defaultValue="mac"
    values={[
        {label: 'Mac', value: 'mac'},
        {label: 'Windows', value: 'windows'},
        {label: 'Linux', value: 'linux'},
    ]}>
<TabItem value="mac">

#### Prerequisites

To use the Astro CLI on Mac, you must have:

- [Homebrew](https://brew.sh/)
- [Docker Desktop](https://docs.docker.com/get-docker/) (v18.09 or higher).

#### Installation

To install the latest version of the Astro CLI, run the following command:

```sh
brew install astronomer/tap/astro
```

:::caution

If you are on Software version 0.29, you should install version 0.29 of the Astro CLI as a bridge release between version 0.28 and version 1.0. To install this release run the following command:  

```sh
brew install astronomer/tap/astro@0.29.0
```

:::

To install a specific version of the Astro CLI, specify the version you want to install at the end of the command:

```sh
brew install astronomer/tap/astro@<major.minor.patch-version>
```

If you specify only a major version, this command installs the latest minor or patch version available for the major version.

</TabItem>

<TabItem value="windows">

#### Prerequisites

To use the Astro CLI on Windows, you must have:

- [Docker Desktop](https://docs.docker.com/desktop/windows/install/) for Windows.
- [Docker Engine](https://docs.docker.com/engine/install/) (v0.13.1 or higher).
- [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) enabled on your local machine.
-  Windows 10 or Windows 11.

#### Installation

1. Go to the [**Releases** page of the Astro CLI GitHub repository](https://github.com/astronomer/astro-cli/releases). Based on your desired CLI version and the CPU architecture of your machine, download one of the `.zip` files available on this page.

    For example, to install v1.0.0 of the Astro CLI on a Windows machine with an AMD 64 architecture, download `astro_1.0.0-converged_windows_amd64.zip`.

  :::caution

  If you are on Software version 0.29, you should install version 0.29 of the Astro CLI as a bridge release between version 0.28 and version 1.0. To install this release, download a `.zip` file that includes `astro_0.29.0`.

  :::

2. If the `.zip` file does not automatically unzip, run the following command to unzip the executable:

    ```sh
    tar -xvzf .\astrocli.tar.gz
    ```

3. Add the filepath for the directory containing `astro.exe` as a PATH environment variable. For example, if `astro.exe` was stored in `C:\Users\username\astrocloud.exe`, you would add `C:\Users\username` as your PATH environment variable. To learn more about configuring the PATH environment variable, see [Java documentation](https://www.java.com/en/download/help/path.html).

4. Restart your machine.

</TabItem>

<TabItem value="linux">

#### Prerequisites

To use the Astro CLI on Linux, you must have:

- [Docker Engine](https://docs.docker.com/engine/install/) (v0.18.9 or higher).

#### Installation

Run the following command to install the latest version of the Astro CLI directly to `PATH`:

```sh
curl -sSL install.astronomer.io | sudo bash -s
```

:::caution

If you are on Software version 0.29, you should install version 0.29 of the Astro CLI as a bridge release between version 0.28 and version 1.0. To install this release run the following command:  

```sh
curl -sSL install.astronomer.io | sudo bash -s -- v0.29.0
```

:::

To install a specific version of the CLI, specify the version number as a flag at the end of the command. For example, to install v1.0.0 of the CLI, you would run:

```sh
curl -sSL install.astronomer.io | sudo bash -s -- v1.0.0
```

If you specify only a major version, this command installs the latest minor or patch version available for the major version.

</TabItem>

</Tabs>

## Confirm the Install

To confirm the CLI was installed properly, run the following CLI command:

```
astro version
```

If the installation was successful, you should see the following output:

<pre><code parentName="pre">{`% astro version
Astro CLI Version: ${siteVariables.cliVersion}`}</code></pre>
