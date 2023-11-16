---
sidebar_label: 'Command reference'
title: 'Astro CLI command reference'
id: reference
---

<head>
  <meta name="description" content="This is where you’ll find all of the available Astro command-line interface (CLI) commands and settings." />
  <meta name="og:description" content="This is where you’ll find all of the available Astro command-line interface (CLI) commands and settings." />
</head>

This document contains information about all commands and settings available in the Astro CLI, including examples and flags. To get started with the Astro CLI, see [Get Started](cli/install-cli.md).

All reference documentation is based on the latest available version of the Astro CLI. To see the differences across various CLI versions, see the [Astro CLI Release Notes](cli/release-notes.md).

The Astronomer product you're using determines the behavior and format of commands. The documentation identifies commands that are specific to Astro or Astronomer Software, or when specific behavior is product dependent.

## Core Commands

- [`astro login`](cli/astro-login.md)
- [`astro dev init`](cli/astro-dev-init.md)
- [`astro dev start`](cli/astro-dev-start.md)
- [`astro dev restart`](cli/astro-dev-restart.md)
- [`astro deploy`](cli/astro-deploy.md)

## Global Options

### Global flags

The Astro CLI has the following global flags that can be used with any command:

- `-h`, `--help`: Output more information about a given command to the CLI.
- `--verbosity <string>`: Specify the log level to expose for each CLI command. Possible values are `debug`, `info`, `warn`, `error`, `fatal`, and `panic`.

### Global configuration options

- `g`, `--global`: You set global configurations for the Astro CLI by running `astro config --global`. See [Configure the CLI](configure-cli.md#global-configuration-options) for more information.
