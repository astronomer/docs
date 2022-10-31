---
sidebar_label: Create pipeline
title: Create a pipeline
id: create-pipeline
---

:::caution

<!-- id to make it easier to remove: cloud-ide-preview-banner -->

The Cloud IDE is currently in _Public Preview_. This means that it is available to all Astro customers, but is still undergoing heavy development and features are subject to change. Using the Cloud IDE has no impact to your deployments or pipelines running in production. If you have any feedback, please submit it [here](https://portal.productboard.com/75k8qmuqjacnrrnef446fggj).

:::

Now that you've created your project, you can create your first pipeline. To do so, click on the **Create Pipeline** button in the top right corner of the screen.

![Create Pipeline](/img/cloud-ide/create-pipeline.png)

Fill in a name and optional description for your pipeline, then click **Create**. Note that the name of your pipeline must be unique within the project, and it must also be a Python identifier (i.e. it must not contain spaces or special characters). The pipeline name specified here will correspond to your Airflow DAG's name.

After clicking **Create**, you'll be taken to the pipeline editor. This is where you'll write your pipeline code.

![Empty Pipeline Editor](/img/cloud-ide/empty-pipeline-editor.png)

Next, let's write some tasks!
