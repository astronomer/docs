---
sidebar_label: 'Command Reference'
title: 'Astro CLI Command Reference'
id: reference
description: Learn about every command that you can run with the Astro CLI.
---

## Overview

This document contains information about all commands and settings available in the Astro CLI, including examples and flags. To install the Astro CLI, see [Quickstart](cli/quickstart.md).

:::info

All reference documentation is based on the latest available version of the Astro CLI. To see the differences across various CLI versions, see the [Astro CLI Release Notes](cli/release-notes.md).

:::

## Core Commands

We expect that you'll use these commands most often when managing your Astro projects and Deployments:

- [`astro login`](cli/astro-login.md)
- [`astro dev init`](cli/astro-init.md)
- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev stop`](cli/astro-dev-stop.md)
- [`astro deploy`](cli/astro-deploy.md)

Each of these commands has a dedicated documentation page with additional notes and examples.

## Global Options

The Astro CLI has the following global flags that can be used with any command:

- `-h`, `--help`: Output more information about a given command to the CLI.
- `--verbosity <string>`: Specify the log level to expose for each CLI command. Possible values are `debug`, `info`, `warn`, `error`, `fatal`, and `panic`.
