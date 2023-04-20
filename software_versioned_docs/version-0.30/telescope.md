---
title: 'Observe Airflow environments with Telescope'
id: telescope
description: Use the Telescope CLI to collect Airflow metrics and usage data for Astronomer.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import {siteVariables} from '@site/src/versions';

[Telescope](https://github.com/astronomer/telescope) is a CLI developed by Astronomer for generating additional metrics from your Airflow environments. It connects directly to Airflow and generates snapshots of your usage and configurations at different times. This information can help Astronomer support diagnose and resolve issues in  your environments.

Telescope assumes your current permissions whenever you run a command. If you have the correct permissions, Telescope can observe your Airflow environments for a specific period and then generate a report that you can share with Astronomer support.

Astronomer recommends that you observe your Deployments with Telescope at least once a month. When required to assist with troubleshooting, you can observe local projects running with the Astro CLI.

## Prerequisites

To observe a local project with Telescope, you need:

- `docker exec` permissions.
- Access to `docker.sock`.
- Python 3.8.

To observe Software Deployments on Kubernetes with Telescope, you need:

- kubectl.
- Permission to list nodes and exec into Pods.
- Airflow 1.15+ or an equivalent version of Astro Runtime or Astronomer Certified.
- An Airflow metadata db using Postgresql, Mysql, or Sqlite.

To observe a standalone Airflow environment with Telescope, you need:

- An Airflow environment running on a machine with SSH enabled.
- Airflow 1.15+ or an equivalent version of Astro Runtime or Astronomer Certified.


## Install the Telescope CLI

Depending on where you want to run Telescope, install the CLI on a machine that has permissions for either Docker or your Software Kubernetes cluster.

<Tabs
    defaultValue="binary"
    groupId= "install-the-telescope-cli"
    values={[
        {label: 'Binary', value: 'binary'},
        {label: 'Pip', value: 'pip'},
    ]}>
<TabItem value="binary">

Go to the [**Releases** page of the Telescope GitHub repository](https://github.com/astronomer/telescope/releases). Based on the operating system and CPU architecture of your machine, download one of the `.zip` files for the latest available version of Telescope and make it an executable.

For example, to install Telescope on a Linux machine with x86_64 CPU architecture, you would run:

```sh
wget https://github.com/astronomer/telescope/releases/latest/download/telescope-linux-x86_64
chmod +x telescope-linux-x86_64
```

</TabItem>
<TabItem value="pip">

To install Telescope using pip, run the following command:

```sh
pip install telescope --find-links https://github.com/astronomer/telescope/releases/latest
```

</TabItem>
</Tabs>

## Observe deployed environments

In your Kubernetes cluster, run the following command:

```sh
telescope --kubernetes --organization-name <your-organization-name>
```

This command observes all scheduler containers in the cluster and outputs the results of the observation to a file named `<observation-date>.<your-organization-name>.data.json`.

:::info

By default, Telescope only observes Pods with the label `component=scheduler`. If your Deployments use an alternative label to denote scheduler Pods, use  `--label-selector` in your command. For example, if your label for scheduler pods is `role=scheduler`, you would run.  

```sh
--kubernetes --organization-name <your-organization> --label-selector "role=scheduler"
```

:::

## Observe local environments running with the Astro CLI

Open your Astro project and run the following command:

```sh
telescope --docker --organization-name <your-organization-name>
```

This command observes scheduler containers on Docker and outputs the results of the observation to a file named `<observation-date>.<your-organization-name>.data.json`.

## Observe standalone Airflow environments

You can use Telescope to observe both Apache Airflow environments and standalone Astronomer Certified environments. This setup assumes you have two machines:

- A remote machine running Airflow.
- A local machine that you use to connect to your remote machine.

1. On the remote machine running Airflow, create a file named `~/.ssh/config` and then open it.
2. Add the following configuration to the file:

    ```yaml
    Host <your-machine-hostname>
        User <your-username> # Specify the username for logging into the machine
        Port <your-connection-port> # Chose any available port on the machine
    ```

3. Optional. Add additional configurations, such as an SSH key. See [Linuxize](https://linuxize.com/post/using-the-ssh-config-file/).
4. Optional. Repeat steps 1 through 3 for any additional remote machines that you want to observe with Telescope.
5. On your local machine, create a file named `hosts.yaml` and open it.
6. Add the following configuration to the file:

    ```yaml
    ssh:
      - host: <your-machine-hostname>
      - host: <your-machine-hostname-2> # Optional
    ```

7. Run the following command to observe Airflow on the remote machine:

    ```sh
    telescope -f hosts.yaml --organization-name <your-organization-name>
    ```

    This command observes the Airflow scheduler and outputs the results of the observation to a file named `<observation-date>.<your-organization-name>.data.json`.

## Telescope report data

After Telescope observes an Airflow environment, it generates a file ending in `data.json` with information about the environment. The report can include the following details:

- Airflow version
- Provider packages and versions
- Airflow configurations
- The names of Airflow variables, connections, and settings
- DAG and task-level configurations
- Task run usage

Telescope never collects the DAG codes or the contents of Airflow configurations such as variables and connections. To hide DAG names, use the `--dag-obfuscation` flag in your Telescope command.

For all report details and functions, see the [Telescope GitHub repository](https://github.com/astronomer/telescope/).

## Send Telescope reports to Astronomer support

1. In the [Astronomer support portal](https://support.astronomer.io/), create a ticket named `<Organization-name>: Telescope Results`
2. Attach the `data.json` file that Telescope generated to the ticket.

## Advanced configuration

Telescope includes advanced settings for customizing your reports and observing Airflow environments running in containers with custom names. For more information about these settings, see [Telescope README](https://github.com/astronomer/telescope) or run `telescope --help`.
