---
sidebar_label: 'Overview'
title: 'Astro CLI'
id: overview
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
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

## Astro CLI features

With the Astro CLI, you can:

- Run Airflow on your local machine in minutes.
- Parse, debug, and test DAGs in a dedicated testing environment.
- Manage your Astro resources, including Workspaces and Deployments.

## Get started

<LinkCardGrid>
  <LinkCard truncate label="Astro CLI Quickstart" description="Start a new Airflow project with just a few commands." href="/astro/cli/get-started-cli" />
  <LinkCard truncate label="Release notes" description="Review the latest changes to the Astro CLI." href="/astro/cli/release-notes" />
  <LinkCard truncate label="Command reference" description="Learn about all available Astro CLI commands." href="/astro/cli/reference" />
</LinkCardGrid>