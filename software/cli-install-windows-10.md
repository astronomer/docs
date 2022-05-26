---
sidebar_label: 'Windows 10'
title: 'Astro CLI Installation for Windows 10'
id: cli-install-windows-10
description: Install the Windows-based CLI or the Unix-based CLI a Windows Subsystem for Linux (WSL).
---

To install the Astro CLI on Windows, you have the following options:

- Install the Unix-based CLI on Windows Subsystem for Linux (WSL).
- Install the Windows-based CLI.

> **Note:** Both options require Windows 10 or later.

## Astro CLI on Windows Subsystem for Linux

Before you start the setup and configuration process for the Astro CLI on the WSL, make sure:
 - You're running the bash terminal
 - You have [WSL enabled](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
 - You're running Windows 10 version 2004 or later (Build 19041 or later) or Windows 11

**Note:** Astronomer recommends using Ubuntu as your linux distribution for WSL.

The complete WSL installation guide is available here: [Install WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

### Step 1. Install Docker CE for Windows

See [Docker for Windows Install Guide](https://docs.docker.com/docker-for-windows/install/).

After finishing the installation, use the distro shell or a Windows Terminal to open a new WSL session. Run `docker run hello-world` in your WSL instance to ensure everything works as expected.

When you run Docker-compose up, go to `/c/Users/name/dev/myapplication` first, or your volume won't work. Don't access `/mnt/c` directly.

### Step 2. CLI Install

Finish the installation and start the deployment DAGs. See [CLI Quickstart Guide](cli-quickstart.md).

## Astro CLI on Windows 10 (PowerShell)

Use the following instructions to install a Windows adapted version of the Astro CLI.

### Prerequisites

Make sure you have the following installed:

- Windows 10
- [Docker](https://docs.docker.com/docker-for-windows/install/)

### Step 2. Enable WSL-2 Based Docker Engine or Hyper-V (legacy)

Make sure that the WSL 2 based engine is enabled in Docker Settings (preferred). If this is not possible, enable Hyper-V (legacy). This is required to run Docker and Linux Containers.

If you have any issues with Docker, see [Docker's Troubleshooting Guide for Windows](https://docs.docker.com/docker-for-windows/troubleshoot/).

### Step 3. Download the Astro CLI


You can download the latest version of the CLI on the [Astronomer GitHub](https://github.com/astronomer/astro-cli/releases/). Select an asset that includes windows_386.zip in the filepath.

### Step 4. Extract the contents

You should now have a zip file on your computer that contains the following:

- CHANGELOG
- README
- LICENSE
- A file titled `astro.exe`

Move `astro.exe` to a location where it can't be deleted.

### Step 5. Add Executable to Path
Add the location of `astro.exe` to your %PATH% environment variable. See [How to Add to Windows PATH Environment Variable](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/).

### Step 6. Final Command

Open your Terminal or PowerShell console and run the following:

```
C:\Windows\system32>astro version
Astro CLI Version: 0.8.2
Git Commit: f5cdab8f832da3c6184a7ac167b491e3bac3c022
```

If you receive a response similar to what is shown, your set up is complete.

## Potential Postgres Error

The following error might appear when you run `astro dev start` on your newly created workspace:

```
Sending build context to Docker daemon  8.192kB
Step 1/1 : FROM quay.io/astronomer/ap-airflow:latest-onbuild
# Executing 5 build triggers
 ---> Using cache
 ---> Using cache
 ---> Using cache
 ---> Using cache
 ---> Using cache
 ---> f28abf18b331
Successfully built f28abf18b331
Successfully tagged hello-astro/airflow:latest
INFO[0000] [0/3] [postgres]: Starting
Pulling postgres (postgres:10.1-alpine)...
panic: runtime error: index out of range
goroutine 52 [running]:
github.com/astronomer/astro-cli/vendor/github.com/Nvveen/Gotty.readTermInfo(0xc4202e0760, 0x1e, 0x0, 0x0, 0x0)
....
```

This is an issue pulling Postgres. To correct it, run:

```
Docker pull postgres:10.1-alpine
```
