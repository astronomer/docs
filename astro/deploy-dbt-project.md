---
sidebar_label: 'Deploy a dbt project'
title: 'Deploy dbt projects to Astro'
id: deploy-dbt-project
description: Learn how to deploy and run dbt projects with Apache Airflow on Astro.
---

import HostedBadge from '@site/src/components/HostedBadge';

<HostedBadge/>

:::privatepreview
:::

To orchestrate dbt jobs with Apache Airflow, you need to deploy your dbt project to Astro alongside your DAGs and the rest of your Airflow code.

Astro supports a range of options when it comes to adding your dbt project your Airflow deployment.

This guide covers the options along with their pros and cons, so you can choose the best option for your team.

## Feature overview

Astro supports two basic dbt code deployment strategies. You can:

1. **Include dbt code to your Astro runtime image**: Astronomer recommends this approach for small teams that have a monorepo with their dbt code inside of their Astro project
2. **Use dbt Deploys to independently ship dbt code**: independently deploy bundles of dbt code directly to Astro. Astronomer recommends this approach for teams that have dbt code in a separate (or in multiple) locations other than their Astro project

## Best practice guidance

Depending on your organization's structure and needs, Astronomer recommends either including dbt code in your image builds or using dbt Deploys. In addition to your dbt code deployment strategy, we recommend using [Astronomer Cosmos](https://www.astronomer.io/cosmos/), the open-source standard for combining dbt code and Airflow.

### Prerequisites

- An Astro Deployment
- An Astro project
- A dbt project
- The [Astro CLI v1.28 or greater](https://www.astronomer.io/docs/astro/cli/install-cli)

### Option 1: Include dbt code in your Astro runtime image

The most simple way to set up dbt on Astro is by including your dbt code in your image during image builds.

To accomplish this, Astronomer recommends adding the directory `/dbt` to the top-level of your Astro project, and including individual dbt project directories inside of this home directory.

:::tip
To see an example of this pattern in action, check out the demo repo of [Astronomer Cosmos](https://github.com/astronomer/cosmos-demo).
:::

To learn more about running dbt core or dbt Cloud with Apache Airflow, see [Orchestrate dbt Core jobs with Airflow](https://www.astronomer.io/docs/learn/airflow-dbt).

### Option 2: Use dbt Deploys to independently ship dbt code

:::privatepreview
:::

#### Step 1: (Optional) Deploy your full Astro image

In order to first deploy a dbt project to Astro, Astronomer recommends that you have an Astro project already running on your Deployment with DAGs that need to read from dbt. That way, your dbt project will be read and used when you deploy it.

If you are using a new Deployment, first deploy your Astro project with the Astro CLI by running:

```bash

astro deploy
```

#### Step 2: Deploy your dbt project

Next, navigate to the directory of your dbt project. This directory should include the `dbt_project.yml` file, such as the [classic dbt jaffle shop](https://github.com/dbt-labs/jaffle-shop-classic?tab=readme-ov-file) example shown below:

![Jaffle Shop directory](/img/docs/reset-password.png)

From the CLI, run the following command to deploy your dbt project. This will deploy your code to the The command prompts you to choose the Deployment that you want to deploy your dbt project to.

```bash

astro dbt deploy
```

By default, this command will attach the dbt code to the default path of `/usr/local/airflow/dbt/<dbt-project-name>`.

See [`astro dbt deploy`](https://www.astronomer.io/docs/astro/cli/astro-dbt-deploy) for more information about this command.

:::tip

If your dbt code is accessed at a different path or folder than the default path, specify the mount path.

```bash

astro dbt deploy --mount-path /usr/local/airflow/dbt/example-dbt-project
```

:::

Congrats, you've added your dbt code to your deployment! Check the Astro UI to see more information about your

#### Delete your dbt project

If you want to remove your dbt code from your deployment, you can also delete the dbt project from the Airflow environments where you deployed it. This command does not delete your dbt project source files, it only removes it from the Airflow containers where it was mounted. When you run this command, you will be prompted to choose the Deployment that you want to remove the project from.

```bash

astro dbt delete
```

See [`astro dbt delete`](https://www.astronomer.io/docs/astro/cli/astro-dbt-delete) for more information about this command.
