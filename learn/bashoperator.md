---
title: "Using the BashOperator"
id: bashoperator
sidebar_label: BashOperator
description: "Learn how to use the BashOperator to run bash commands and bash scripts. Review examples of how to run scripts in other languages than Python."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import bash_two_commands_example_dag from '!!raw-loader!../code-samples/dags/bashoperator/bash_two_commands_example_dag.py';
import bash_script_example_dag from '!!raw-loader!../code-samples/dags/bashoperator/bash_script_example_dag.py';
import print_ISS_info_dag from '!!raw-loader!../code-samples/dags/bashoperator/print_ISS_info_dag.py';

The [BashOperator](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator) is one of the most commonly used operators in Airflow. It executes bash commands or a bash script from within your Airflow DAG.

In this guide you'll learn:

- When to use the BashOperator.
- How to use the BashOperator and `@task.bash` decorator.
- How to use the BashOperator including executing bash commands and bash scripts.
- How to run scripts in non-Python programming languages using the BashOperator.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Airflow operators. See [Operators 101](what-is-an-operator.md).
- Airflow decorators. See [Introduction to the TaskFlow API and Airflow decorators](airflow-decorators.md).
- Basic bash commands. See the [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html).

## How to use the BashOperator and `@task.bash` decorator

The [BashOperator](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator) is part of core Airflow and can be used to execute a single bash command, a set of bash commands, or a bash script ending in `.sh`. The `@task.bash` decorator can be used to create bash statements using Python functions and is available as of Airflow 2.9.

<Tabs
    defaultValue="traditional"
    groupId="how-to-use-bashoperator"
    values={[
        {label: 'Traditional syntax', value: 'traditional'},
        {label: 'TaskFlow API', value: 'taskflow'},
    ]}>
<TabItem value="traditional">

```python
# from airflow.operators.bash import BashOperator

bash_task = BashOperator(
    task_id="bash_task",
    bash_command="echo $MY_VAR",
    env={"MY_VAR": "Hello World"}
)
```

</TabItem>
<TabItem value="taskflow">

```python
# from airflow.decorators import task

@task.bash(env={"MY_VAR": "Hello World"})
def bash_task():
    return "echo $MY_VAR"  # the returned string is executed as a bash command

bash_task()
```

</TabItem>
</Tabs>

The following parameters can be provided to the operator and decorator:

- `bash_command`: Defines a single bash command, a set of commands, or a bash script to execute. This parameter is required.
- `env`: Defines environment variables in a dictionary for the bash process. By default, the defined dictionary overwrites all existing environment variables in your Airflow environment, including those not defined in the provided dictionary. To change this behavior, you can set the `append_env` parameter. If you leave this parameter blank, the BashOperator inherits the environment variables from your Airflow environment.
- `append_env`: Changes the behavior of the `env` parameter.  If you set this to `True`, the environment variables you define in `env` are appended to existing environment variables instead of overwriting them. The default is `False`.
- `output_encoding`: Defines the output encoding of the bash command. The default is `utf-8`.
- `skip_exit_code`: Defines which bash exit code should cause the BashOperator to enter a `skipped` state. The default is `99`.
- `cwd`: Changes the working directory where the bash command is run. The default is `None` and the bash command runs in a temporary directory.

The behavior of a BashOperator task is based on the status of the bash shell:

- Tasks succeed if the whole shell exits with an exit code of 0.
- Tasks are skipped if the exit code is 99 (unless otherwise specified in `skip_exit_code`).
- Tasks fail in case of all other exit codes.

:::tip

If you expect a non-zero exit from a sub-command you can add the prefix `set -e;` to your bash command to make sure that the exit is captured as a task failure.

:::

Both the `bash_command` and the `env` parameter can accept [Jinja templates](templating.md). However, the input given through Jinja templates to `bash_command` is not escaped or sanitized. If you are concerned about potentially harmful user input you can use the setup shown in the [BashOperator documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html).

## When to use the BashOperator

The following are common use cases for the BashOperator and `@task.bash` decorator in Airflow DAGs:

- Creating and running bash commands based on complex Python logic.
- Running a single or multiple bash commands in your Airflow environment.
- Running a previously prepared bash script.
- Running scripts in a programming language other than Python.
- Running commands to initialize tools that lack specific operator support. For example [Soda Core](soda-data-quality.md).

## Example: Using Python to create bash commands

In Airflow 2.9+, you can use `@task.bash` to create bash statements using Python functions. This decorator is especially useful when you want to run bash commands based on complex Python logic, including inputs from upstream tasks. The following example demonstrates how to use the `@task.bash` decorator to conditionally run different bash commands based on the output of an upstream task.

```python
# from airflow.decorators import task

@task
def upstream_task():
    dog_owner_data = {
        "names": ["Trevor", "Grant", "Marcy", "Carly", "Philip"],
        "dogs": [1, 2, 2, 0, 4],
    }

    return dog_owner_data

@task.bash
def bash_task(dog_owner_data):
    names_of_dogless_people = []
    for name, dog in zip(dog_owner_data["names"], dog_owner_data["dogs"]):
        if dog < 1:
            names_of_dogless_people.append(name)

    if names_of_dogless_people:
        if len(names_of_dogless_people) == 1:
            # this bash command is executed if only one person has no dog
            return f'echo "{names_of_dogless_people[0]} urgently needs a dog!"'
        else:
            names_of_dogless_people_str = " and ".join(names_of_dogless_people)
            # this bash command is executed if more than one person has no dog
            return f'echo "{names_of_dogless_people_str} urgently need a dog!"'
    else:
        # this bash command is executed if everyone has at least one dog
        return f'echo "All good, everyone has at least one dog!"'

bash_task(dog_owner_data=upstream_task())
```

## Example: Execute two bash commands using one BashOperator

The BashOperator can execute any number of bash commands separated by `&&`.

In this example, you run two bash commands in a single task:

- `echo Hello $MY_NAME!` prints the environment variable `MY_NAME` to the console.
- `echo $A_LARGE_NUMBER | rev  2>&1 | tee $AIRFLOW_HOME/include/my_secret_number.txt` takes the environment variable `A_LARGE_NUMBER`, pipes it to the `rev` command which reverses any input, and saves the result in a file called `my_secret_number.txt` located in the `/include` directory. The reversed number will also be printed to the console.

The second command uses an environment variable from the Airflow environment, `AIRFLOW_HOME`. This is only possible because `append_env` is set to `True`.

<CodeBlock language="python">{bash_two_commands_example_dag}</CodeBlock>

It is also possible to use two separate BashOperators to run the two commands, which can be useful if you want to assign different dependencies to the tasks.

## Example: Execute a bash script

The BashOperator can also be provided with a bash script (ending in `.sh`) to be executed.

For this example, you run a bash script which iterates over all files in the `/include` folder and prints their names to the console.

```bash
#!/bin/bash

echo "The script is starting!"
echo "The current user is $(whoami)"
files = $AIRFLOW_HOME/include/*

for file in $files
do
    echo "The include folder contains $(basename $file)"
done

echo "The script has run. Have an amazing day!"
```

Make sure that your bash script (`my_bash_script.sh` in this example) is available to your Airflow environment. If you use the Astro CLI, you can make this file accessible to Airflow by placing it in the `/include` directory of your Astro project.

It is important to make the bash script executable by running the following command before making the script available to your Airflow environment:

```bash
chmod +x my_bash_script.sh
```

If you use the Astro CLI, you can run this command before running `astro dev start`, or you can add the command to your project's Dockerfile with the following `RUN` command:

```docker
RUN chmod +x /usr/local/airflow/include/my_bash_script.sh
```

Astronomer recommends running this command in your Dockerfile for production builds such as Astro Deployments or in production CI/CD pipelines.

After making the script available to Airflow, you only have to provide the path to the script in the `bash_command` parameter. Be sure to add a space character at the end of the filepath, or else the task will fail with a Jinja exception!

<CodeBlock language="python">{bash_script_example_dag}</CodeBlock>

## Example: Run a script in another programming language

Using the BashOperator is a straightforward way to run a script in a non-Python programming language in Airflow. You can run a script in any language that can be run with a bash command.

In this example, you run some JavaScript to query a public API providing the [current location of the international Space Station](http://open-notify.org/Open-Notify-API/ISS-Location-Now/). The query result is pushed to XCom so that a second task can extract the latitude and longitude information in a script written in R and print the data to the console.

The following setup is required:

- Install the JavaScript and R language packages at the OS level.
- Write a JavaScript file.
- Write a R script file.
- Make the scripts available to the Airflow environment.
- Execute the files from within a DAG using the BashOperator.

If you use the Astro CLI, the programming language packages can be installed at the OS level by adding them to the `packages.txt` file of your Astro project.

```text
r-base
nodejs
```

The following JavaScript file contains code for sending a GET request to the `/iss-now` path at `api.open-notify.org` and returning the results to `stdout`, which will both be printed to the console and pushed to XCom by the BashOperator.

```javascript
// specify that a http API is queried
const http = require('http');

// define the API to query
const options = {
  hostname: 'api.open-notify.org',
  port: 80,
  path: '/iss-now',
  method: 'GET',
};

const req = http.request(options, res => {
  // log the status code of the API response
  console.log(`statusCode: ${res.statusCode}`);

  // write the result of the GET request to stdout
  res.on('data', d => {
    process.stdout.write(d);
  });
});

// in case of an error print the error statement to the console
req.on('error', error => {
  console.error(error);
});

req.end();
```


The second task runs a script written in R that uses a regex to filter and print the longitude and latitude information from the API response.

```r
# print outputs to the console
options(echo = TRUE)

# read an argument provided to the R script from the command line
myargs <- commandArgs(trailingOnly = TRUE)

# split a string using : as a separator
set <- strsplit(myargs, ":")

# use regex to extract the lat/long information and convert them to numeric
longitude <- as.numeric(gsub(".*?([0-9]+.[0-9]+).*", "\\1", set[3]))
latitude <- as.numeric(gsub(".*?([0-9]+.[0-9]+).*", "\\1", set[5]))

# print lat/long information in a sentence.
sprintf("The current ISS location: lat: %s / long: %s.", latitude, longitude)
```

To run these scripts using the BashOperator, ensure that they are accessible to your Airflow environment. If you use the Astro CLI, you can place these files in the `/include` directory of your Astro project.

The DAG uses the BashOperator to execute both files defined above sequentially.

<CodeBlock language="python">{print_ISS_info_dag}</CodeBlock>