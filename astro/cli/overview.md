---
sidebar_label: 'Overview'
title: 'Astro CLI'
id: overview
hide_table_of_contents: true
---

<head>
  <meta name="description" content="Learn more about the Astro command-line interface (CLI) and the commands that you can run. The Astro CLI lets you get started with Apache Airflow quickly." />
  <meta name="og:description" content="Learn more about the Astro command-line interface (CLI) and the commands that you can run. The Astro CLI lets you get started with Apache Airflow quickly." />
</head>

import LinkCardGrid from '@site/src/components/LinkCardGrid';
import LinkCard from '@site/src/components/LinkCard';
import AstroCard from '@site/src/components/AstroCard';

<p class="DocItem__header-description">The Astro CLI is the command line interface for data orchestration. It's the easiest way to get started with Apache Airflow and can be used with all Astronomer products.</p>

:::highlight
__Install the CLI__

To install with Homebrew, run:

```sh
brew install astro
```

For alternative installation steps, see [Install the Astro CLI](install-cli.md).

:::
 
The Astro CLI is open source and built for data practitioners everywhere. The binary is maintained in the public [Astro CLI GitHub repository](https://github.com/astronomer/astro-cli), where pull requests and GitHub issues are welcome.

## Astro CLI features

With the Astro CLI, you can:

- Run Airflow on your local machine in minutes.
- Parse, debug, and test DAGs in a dedicated testing environment.
- Manage your Astro resources, including Workspaces and Deployments.

## Core commands

- [`astro dev init`](cli/astro-dev-init.md): Create an Astro project.
- [`astro dev start`](cli/astro-dev-start.md): Run Airflow locally.
- [`astro dev restart`](cli/astro-dev-restart.md): Rebuild your Astro project.
- [`astro deploy`](cli/astro-deploy.md): Deploy your code to Astro.
