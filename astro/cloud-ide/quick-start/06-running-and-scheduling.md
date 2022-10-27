---
sidebar_label: Running and scheduling your pipeline
title: Running and scheduling your pipeline
id: running-scheduling
---

Now that you've completed your pipeline, you can run it from beginning to end to ensure it works properly. To do so, click on the **Run** button in the top right corner of the screen. Cells will be executed in order by dependencies. The graph view on the sidebar will show which cells have been executed and which are still pending.

![Run Pipeline](/img/cloud-ide/run-pipeline.png)

### Scheduling

Once you've verified that your pipeline works properly, you can schedule it to run on a regular basis. To do so, click on the **Schedule** icon in the right sidebar. You'll be presented with scheduling options. The Cloud IDE currently supports scheduling by cron string. You can also specify a start date and timezone for your pipeline.

You can either manually type in a cron string or use the cron builder to generate one. The cron builder is a simple UI that allows you to select the minute, hour, day of month, month, and day of week that you want your pipeline to run on. The cron string will be generated automatically for you.

![Schedule Pipeline](/img/cloud-ide/schedule-pipeline.png)

After configuring your schedule, click **Update Settings** to save your changes.

:::warning

Note that configuring your pipeline's schedule will not automatically run it. You must deploy your pipeline to Airflow for it to run. See the next section for more information on how to deploy your pipeline.

:::
