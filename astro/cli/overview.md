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
 
## Core commands

- [`astro dev init`](cli/astro-dev-init.md): Create an Astro project.
- [`astro dev start`](cli/astro-dev-start.md): Run Airflow locally.
- [`astro dev restart`](cli/astro-dev-restart.md): Rebuild your Astro project.
- [`astro deploy`](cli/astro-deploy.md): Deploy your code to Astro.

## Astro CLI Features

<LinkCardGrid>
  <LinkCard label="Preconfigured project directory" description="An Astro project includes all of the files required to run Airflow, including dedicated folders for your DAGs, packages, and unit tests." />
  <LinkCard label="Local Airflow environment" description="Using the Astro CLI, you can run a local Airflow environment, apply code changes, and view logs for all Airflow components." />
  <LinkCard label="Example pytests and DAGs" description="The Astro CLI includes example DAGs which showcase important Airflow best practices and help your team learn quickly." />
  <LinkCard label="Browser-based authentication" description="Access browser-based authentication for Astro and Astronomer Software." />
  <LinkCard label="Astro Cloud UI compatible" description="A robust set of commands matches functionality in the Cloud UI, including Deployment creation and user management." />
  <LinkCard label="CI/CD" description="Configure Deployment API keys to automate CLI commands as part of CI/CD workflows." />
</LinkCardGrid>
