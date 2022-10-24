---
sidebar_label: 'Overview'
title: 'Astro CLI'
id: overview
description: Learn about every command that you can run with the Astro CLI.
hide_table_of_contents: true
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
  <LinkCard label="Built-in Astro project directory" description="An Astro project includes all of the files required to run Airflow, including dedicated folders for your DAGs, packages, and unit tests." />
  <LinkCard label="Advanced commands" description="Using the Astro CLI, you can run a local Airflow environment, apply code changes, and view logs for all Airflow components." />
  <LinkCard label="Example pytests and DAGs" description="The Astro CLI includes example DAGs which showcase important Airflow best practices and help your team learn quickly." />
  <LinkCard label="Browser-based authentication" description="Access browser-based authentication for Astro and Astronomer Software." />
  <LinkCard label="Astro Cloud UI compatible" description="A robust set of commands matches functionality in the Cloud UI, including Deployment creation and user management." />
  <LinkCard label="CI/CD" description="Configure Deployment API keys to automate CLI commands as part of CI/CD workflows." />
</LinkCardGrid>

## Featured CLI docs

<LinkCardGrid>
  <LinkCard truncate label="Release Notes" description="A record of all changes to the Astro CLI." href="/astro/cli/release-notes" />
  <LinkCard truncate label="Install the Astro CLI" description="Documentation for installing the CLI on all operating systems." href="/astro/cli/install-cli" />
  <LinkCard truncate label="Astro CLI command reference" description="Reference information about every available CLI command and option." href="/astro/cli/reference" />
</LinkCardGrid>

<AstroCard />