---
sidebar_label: 'Deploy a dbt project'
title: 'Deploy dbt projects to Astro'
id: deploy-dbt-project
description: Learn how to deploy and run dbt projects with Apache Airflow on Astro.
---

import HostedBadge from '@site/src/components/HostedBadge';

<HostedBadge/>

To orchestrate dbt jobs with Apache Airflow, you need to deploy your dbt project to Astro alongside your DAGs and the rest of your Airflow code. Astro supports a range of options when it comes to adding your dbt project your Airflow deployment.

Depending on your organization's software development lifecycle, your dbt project might live in the same Git repository as your Airflow code or in a different repository. Astronomer supports both methods, but recommends having a dedicated Git repository [Option 2](#option-2-use-dbt-deploys-to-independently-ship-dbt-code) for your dbt code that is separate from your Airflow code. This means your teams working in dbt can remain separate from your teams managing Airflow DAGs.

This guide covers the options along with their pros and cons, so you can choose the best option for your team.

## Feature overview

Astro supports two basic dbt code deployment strategies. You can:

1. **Include dbt code to your Astro runtime image**: make dbt code directly available in Astro project runtime image. This approach works best for small teams just starting out integrating dbt code inside of Astro
2. **Use dbt Deploys to independently ship dbt code**: independently deploy bundles of dbt code directly to Astro. Astronomer recommends this approach for teams that have dbt code in separate locations other than their Astro project

## Best practice guidance

Depending on your organization's structure and needs, Astronomer recommends either including dbt code in your image builds or using dbt Deploys. Regardless of your dbt code deployment strategy, we recommend using [Astronomer Cosmos](https://www.astronomer.io/cosmos/), the open-source standard for combining dbt code and Airflow.

### Prerequisites

- An Astro Deployment
- An Astro project
- A dbt project
- The [Astro CLI v1.28 or greater](https://www.astronomer.io/docs/astro/cli/install-cli)

### Option 1: Include dbt code in your Astro runtime image

The most direct way to set up dbt on Astro is by including dbt code in your runtime image. To accomplish this, Astronomer recommends adding the directory `/dbt` to the top-level of your Astro project and including individual dbt projects inside of this directory.

:::tip
To see an example of this pattern in action, check out the demo repo of [Astronomer Cosmos](https://github.com/astronomer/cosmos-demo).
:::

Finally, to push your new dbt code to your Deployment, perform a deploy with the Astro CLI by running:

```bash
astro deploy
```

While this is the quickest way to get dbt code in your deployment, there can be downsides as your team makes more frequent changes to dbt code or uses more advanced CI/CD. Some of these downsides include:

1. Slower build times when changing only dbt code
2. dbt code must live in the same place as your Astro project
3. Multiple teams developing Airflow and dbt separately must re-deploy the entire Astro project for each iteration

If these downsides become applicable to your team, try Option 2.

### Option 2: Use dbt Deploys to independently ship dbt code

:::privatepreview
:::

dbt Deploys allow you to easily deploy your dbt project to Astro without needing complex processes to incorporate your two sets of code. When you use a dbt Deploy, Astro bundles all files in your dbt project and pushes them to Astro, where they are mounted on your Airflow containers so that your DAGs can access them. This allows you to deploy dbt code without requiring you to use a full Astro image deploy.

#### Step 1: (Optional) Deploy your full Astro image

In order to first deploy a dbt project to Astro, Astronomer recommends that you have an Astro project already running on your Deployment with DAGs that need to read from dbt. That way, your dbt project will be read and used when you deploy it.

If you are using a new Deployment, first deploy your Astro project with the Astro CLI by running:

```bash
astro deploy
```

#### Step 2: Deploy your dbt project

Next, navigate to the directory of your dbt project. This directory should include the `dbt_project.yml` file, such as the [classic dbt jaffle shop](https://github.com/dbt-labs/jaffle-shop-classic?tab=readme-ov-file) example shown below:

![Jaffle shop project structure](/img/docs/reset-password.png)

From the CLI, run the following command to deploy your dbt project. The command prompts you to choose the Deployment that you want to deploy your dbt project to.

```bash
astro dbt deploy
```

By default, this command attaches the dbt code to the default path of `/usr/local/airflow/dbt/<dbt-project-name>`.

See [`astro dbt deploy`](https://www.astronomer.io/docs/astro/cli/astro-dbt-deploy) for more information about this command.

:::tip

If your dbt code is accessed at a different path or folder than the default path, specify a custom mount path with the following flag:

```bash
astro dbt deploy --mount-path /usr/local/airflow/dbt/example-dbt-project
```

:::

Congrats, you've added your dbt code to your deployment! Check the Astro UI to see more information about your dbt Deploy.

![Astro UI with dbt Deploys](/img/docs/reset-password.png)

#### Delete your dbt project

If you want to remove dbt code from your deployment, you can also delete the dbt project from the Airflow environments where you deployed it. This command does not delete your dbt project source files, it only removes it from the Airflow containers where it was mounted. When you run this command, you will be prompted to choose the Deployment that you want to remove the project from.

```bash
astro dbt delete
```

See [`astro dbt delete`](https://www.astronomer.io/docs/astro/cli/astro-dbt-delete) for more information about this command.
