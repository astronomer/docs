---
sidebar_label: "astro deployment logs"
title: "astro deployment logs"
id: astro-deployment-logs
description: Show Airflow component logs for a Deployment.
hide_table_of_contents: true
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

:::info  

The behavior and format of this command differs depending on what Astronomer product you're using. Use the following tabs to change product contexts. 

:::

<Tabs
    defaultValue="astro"
    values={[
        {label: 'Astro', value: 'astro'},
        {label: 'Software', value: 'software'},
    ]}>
<TabItem value="astro">

Show [Airflow component logs](view-logs.md#view-airflow-component-logs-in-the-cloud-ui) over the last 24 hours for a given Deployment on Astro. These are the same logs that appear in the **Logs** tab of the Cloud UI.

## Usage

```sh
astro deployment logs
```

## Options

| Option              | Description                                                                              | Possible Values                        |
| ------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------- |
| `<deployment-id>`   | The ID of the Deployment to show logs for                                                | Any valid Deployment ID                |
| `--deployment-name` | The name of the Deployment to show logs for. Use as an alternative to `<deployment-id>`. | Any valid Deployment name              |
| `-e`,`--error`      | Show only logs with a log level of `ERROR`                                               | None                                   |
| `-w`,`--warn`       | Show only logs with a log level of `WARNING`                                             | None                                   |
| `-i`,`--info`       | Show only logs with a log level of `INFO`                                                | None                                   |
| `-c`,`--log-count`  | The number of log lines to show. The default is `500`                                    | Any integer less than or equal to 500. |
| `--workspace-id`    | Specify a Workspace to show logs for a Deployment outside of your current Workspace      | Any valid Workspace ID                 |

## Examples

```sh
$ astro deployment logs
# CLI prompts you for a Deployment to view logs for

$ astro deployment logs cl03oiq7d80402nwn7fsl3dmv
# View logs for a specific Deployment

$ astro deployment logs --deployment-name="My Deployment" --error --log-count=25
# Show only the last 25 error-level logs
```

</TabItem>

<TabItem value="software">

Show Airflow component logs over the last 24 hours for a given Deployment. These logs are the same logs that appear in the **Logs** tab of the Software UI.

## Usage

Run one of the following commands depending on which logs you want to stream:

```sh
astro deployment logs <deployment-id> scheduler
astro deployment logs <deployment-id> webserver
astro deployment logs <deployment-id> workers
astro deployment logs <deployment-id> triggerer
```

## Options

| Option                            | Description                                                        | Possible values                                         |
| --------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------- |
| `<deployment-id>` (_Required)     | The ID of the Deployment for which you want to view logs           | Any valid Deployment ID                                 |
| `<airflow-component>` (_Required) | The Airflow component for which you want to view logs              | `scheduler`, `webserver`, `workers`, or `triggerer`     |
| `--follow`                        | Subscribes to watch more logs                                      | None                                                    |
| `--search`                        | Searches for the specified string within the logs you're following | Any string                                              |
| `--since`                         | Limits past logs to those generated in the lookback window         | Lookback time in `h` or `m` (for example, `5m` or `2h`) |


## Examples

```sh
# Return logs for last five minutes of webserver logs.
$ astro deployment logs webserver example-deployment-uuid

# Return logs from airflow workers for the last 5 minutes with a given search term, and subscribe to view more as they are generated.
$ astro deployment logs workers example-deployment-uuid --follow --search "some search terms"

# Return logs from airflow webserver for last 25 minutes.
$ astro deployment logs webserver example-deployment-uuid --since 25m
```

</TabItem>
</Tabs>

## Related commands

- [`astro dev logs`](cli/astro-dev-logs.md)
- [`astro dev run`](cli/astro-dev-run.md)
- [`astro dev ps`](cli/astro-dev-ps.md)

