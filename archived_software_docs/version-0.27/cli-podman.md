---
sidebar_label: 'Run the CLI with Podman'
title: 'Run the Astronomer CLI in Podman Containers'
id: cli-podman
description: Use Podman instead of Docker to run specific Astronomer CLI commands.
---

## Overview

By default, the Astronomer CLI uses Docker to execute a few specific commands:

- `astro dev [...]`: For running an Airflow environment on your local machine
- `astro auth login`: For authenticating to Astronomer Software
- `astro deploy`: For pushing code to a Deployment

Alternatively, you can use Podman to execute these same commands.

## Prerequisites

To complete this setup, you need:

- Podman 3.1.0+ installed on your local machine.
- The Astronomer CLI.

## Linux Setup

1. Run the following command to start the Podman API service:

    ```sh
    podman system service -t 0 &
    ```

    :::danger
    Avoid running this command from a directory containing a Dockerfile.
    :::

2. Run the following command to create a new Astronomer project:

    ```sh
    astro dev init
    ```

3. Run the following command to specify Podman as the CLI's primary container engine:

    ```sh
    astro config set container.engine podman
    ```

4. Run `astro dev start` to confirm that Podman is running the containers for your local Airflow environment.

## Mac Setup

To set up Podman for an Astronomer project:


1. Run the following commands to start Podman:

    ```sh
    $ podman machine init
    $ podman machine start
    ```

2. Run the following command to pick up the Identity and connection URI for your `podman-machine-default`:

    ```sh
    podman system connection ls
    ```

    The output should look like the following:

    ```text
    podman-machine-default*      /Users/user/.ssh/podman-machine-default  ssh://core@localhost:54523/run/user/1000/podman/podman.sock
    podman-machine-default-root  /Users/user/.ssh/podman-machine-default  ssh://root@localhost:54523/run/podman/podman.sock
    ```

    Copy the `Identity` and `URI` from `podman-machine-default*` for the next two steps.

2. Run the following command to export the Podman Identity as a system environment variable:

    ```sh
    export CONTAINER_SSHKEY=<your-podman-identity>
    ```

3. Run the following command to set the connection URI from the Astronomer CLI:

    ```sh
    astro config set podman.connection_uri <your-podman-uri>
    ```

4. Enable [Remote Login](https://support.apple.com/en-gb/guide/mac-help/mchlp1066/mac#:~:text=Set%20up%20Remote%20Login%20on,Sharing%20%2C%20then%20select%20Remote%20Login.&text=Select%20the%20Remote%20Login%20tickbox,access%20for%20remote%20users%E2%80%9D%20checkbox.) on your Mac.

5. In a separate terminal window, complete the following set of commands and configurations to mount your local Airflow project directory to the Podman machine:

    ```sh
    $ podman machine --log-level=debug ssh -- exit 2>&1 | grep Executing
    # copy ssh command from above output for the next command, for example:
    # 49671 core@localhost

    $ ssh -i /Users/user/.ssh/podman-machine-default -R 10000:$(hostname):22 -p <ssh-command>
    $ ssh-keygen -t rsa
    $ ssh-copy-id -p 10000 <user>@127.0.0.1
    $ sudo mkdir -p airflow-dir
    $ sudo chown core:core airflow-dir
    $ sudo vi /etc/fuse.conf # uncomment the user_allow_other line and save the file
    $ sshfs -p 10000 -o allow_other <user>@127.0.0.1:<local_airflow_dir_path> airflow-dir

    # check if sshfs is working fine or not
    $ cd airflow-dir
    $ ls # you should be able to see all the files present in your local airflow directory
    $ pwd

    #keep the session running
    ```

    Copy the output of `pwd` for step 7.

6. Open a new terminal window. In an empty directory, run the following commands to create a new Astronomer project, set Podman as your primary container engine, and generate a `pod-config.yml` file for your project:

    ```sh
    $ astro dev init
    $ astro config set container.engine podman
    $ astro dev start
    ```

7. In the `pod-config.yml` file, replace the default configuration with the following values:

    ```yaml
    volumes:
      - hostPath:
          path: <pwd-output>/dags
          type: Directory
        name: airflow-dags-dir
      - hostPath:
          path: <pwd-output>/plugins
          type: Directory
        name: airflow-plugins-dir
      - hostPath:
          path: <pwd-output>/include
          type: Directory
        name: airflow-include-dir
    ```

You can now run the Astronomer CLI in Podman containers for this Astronomer project.

## Switch Between Using Docker and Podman

Once you set up the Astronomer CLI to use Podman on your local machine, the CLI will automatically run Podman containers whenever you run a command that requires them. To revert back to default behavior and run CLI commands in Docker containers, run the following command:

```sh
astro config set container.engine docker
```

If you need to switch back to using Podman again, run the following command:

```sh
astro config set container.engine podman
```
