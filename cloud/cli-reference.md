---
sidebar_label: 'CLI Command Reference'
title: 'Astronomer Cloud CLI Command Reference'
id: cli-reference
description: Learn about every command that you can run with the Astronomer Cloud CLI.
---

import {siteVariables} from '@site/src/versions';

## Overview

The Astronomer Cloud CLI is the easiest way to run Apache Airflow on your local machine. From the CLI, you can run a local Apache Airflow environment with a dedicated Webserver, Scheduler and Postgres Database. If you're an Astronomer Cloud user, you can also create and manage users, Workspaces, Deployments, and more.

This document contains information about all commands and settings available in the Astronomer Cloud CLI, including examples and flags. To install the Astronomer Cloud CLI, see [Install the CLI](install-cli.md).

## Core Commands

We expect that you'll use these commands most often when managing your Astronomer projects and Deployments:

- [`astrocloud auth login`](cli-reference/astrocloud-auth-login.md)
- [`astrocloud dev init`](cli-reference/astrocloud-dev-init.md)
- [`astrocloud dev start`](cli-reference/astrocloud-dev-start.md)
- [`astrocloud dev stop`](cli-reference/astrocloud-dev-stop.md)
- [`astrocloud deploy`](cli-reference/astrocloud-deploy.md)

Each of these commands has a dedicated documentation page with additional notes and examples. As we expand functionality for the Astronomer Cloud CLI, new commands will be listed here.

## Global Options

The Astronomer Cloud CLI has one global flag that can be used with any command:

- `-h`, `--help`: Output more information about a given command to the CLI.
