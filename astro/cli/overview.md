---
sidebar_label: 'Overview'
title: 'Astro CLI'
id: overview
description: Learn about every command that you can run with the Astro CLI.
---
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
 
## Astro CLI Features

<LinkCardGrid>
  <LinkCard label="Built-in Astro project directory" description="Includes all the files required to run Airflow, including dedicated folders for your DAGs, packages, and unit tests." />
  <LinkCard label="Advanced commands" description="Using the CLI, you can run a local Airflow environment, apply code changes, and view logs for all Airflow components." />
  <LinkCard label="Example pytests and DAGs" description="Examples showcase important Airflow best practices and can help your team learn quickly and identify errors in your DAGs ahead of time." />
  <LinkCard label="Browser-based authentication" description="Easy and secure browser-based authentication for Astro and Astronomer Software." />
  <LinkCard label="Astro Cloud UI compatable" description="A robust set of commands to match functionality in the Cloud UI, including Deployment creation and environment variable modifications." />
  <LinkCard label="CI/CD" description="Support for Deployment API keys, which you can use to automate commands as part of CI/CD workflows." />
</LinkCardGrid>

## Featured CLI docs

<LinkCardGrid>
  <LinkCard truncate label="Release Notes" description="Astro CLI release notes" href="/astro/cli/release-notes" />
  <LinkCard truncate label="Install the Astro CLI" description="This is where you'll find information about installing, upgrading, and uninstalling the Astro CLI." href="/astro/cli/install-cli" />
  <LinkCard truncate label="Astro CLI command reference" description="This document contains information about all commands and settings available in the Astro CLI, including examples and flags. To get started with the Astro CLI, see Get Started." href="/astro/cli/reference" />
</LinkCardGrid>

<AstroCard />