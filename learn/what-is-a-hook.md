---
title: "Airflow hooks"
sidebar_label: "Hooks"
id: what-is-a-hook
---

<head>
  <meta name="description" content="Learn about hooks and how they should be used in Apache Airflow. See an example of implementing two different hooks in a DAG." />
  <meta name="og:description" content="Learn about hooks and how they should be used in Apache Airflow. See an example of implementing two different hooks in a DAG." />
</head>

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import CodeBlock from '@theme/CodeBlock';
import hook_tutorial_taskflow from '!!raw-loader!../code-samples/dags/what-is-a-hook/hook_tutorial_taskflow.py';
import hook_tutorial_traditional from '!!raw-loader!../code-samples/dags/what-is-a-hook/hook_tutorial_traditional.py';

A hook is an abstraction of a specific API that allows Airflow to interact with an external system. Hooks are built into many operators, but they can also be used directly in DAG code.

In this guide, you'll learn about using hooks in Airflow and when you should use them directly in DAG code. You'll also implement two different hooks in a DAG.

[Over 200 hooks](https://registry.astronomer.io/modules/?types=hooks%2CHooks&page=2) are available in the Astronomer Registry. If a hook isn't available for your use case, you can write your own and share it with the community.

## Assumed knowledge

To get the most out of this guide, you should have an understanding of:

- Basic Airflow concepts. See [Introduction to Apache Airflow](intro-to-airflow.md).
- Basic Python. See the [Python Documentation](https://docs.python.org/3/tutorial/index.html).

## Hook basics

Hooks wrap around APIs and provide methods to interact with different external systems. Hooks standardize how Astronomer interacts with external systems and using them makes your DAG code cleaner, easier to read, and less prone to errors.

To use a hook, you typically only need a connection ID to connect with an external system. For more information about setting up connections, see [Manage your connections in Apache Airflow](connections.md).

All hooks inherit from the [BaseHook class](https://github.com/apache/airflow/blob/main/airflow/hooks/base.py), which contains the logic to set up an external connection with a connection ID. On top of making the connection to an external system, individual hooks can contain additional methods to perform various actions within the external system. These methods might rely on different Python libraries for these interactions. For example, the [`S3Hook`](https://registry.astronomer.io/providers/amazon/modules/s3hook) relies on the [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library to manage its Amazon S3 connection.  

The `S3Hook` contains [over 20 methods](https://github.com/apache/airflow/blob/main/airflow/providers/amazon/aws/hooks/s3.py) to interact with Amazon S3 buckets. The following are some of the methods that are included with `S3Hook`:

- `check_for_bucket`: Checks if a bucket with a specific name exists.
- `list_prefixes`: Lists prefixes in a bucket according to specified parameters.
- `list_keys`: Lists keys in a bucket according to specified parameters.
- `load_file`: Loads a local file to Amazon S3.
- `download_file`: Downloads a file from the Amazon S3 location to the local file system.

## When to use hooks

Since hooks are the building blocks of operators, their use in Airflow is often abstracted away from the DAG author. However, there are some cases when you should use hooks directly in a Python function in your DAG. The following are some general guidelines for using hooks in Airflow:

- Hooks should always be used over manual API interaction to connect to external systems.
- If you write a custom operator to interact with an external system, it should use a hook.
- When an operator with built-in hooks exists for your specific use case, you should use the operator instead of manually setting up a hook.
- If you regularly need to connect to an API and a hook is not available, write your own hook and share it with the community.

## Example implementation

The following example shows how you can use the hooks ([S3Hook](https://registry.astronomer.io/providers/amazon/modules/s3hook) and [SlackHook](https://registry.astronomer.io/providers/slack/modules/slackhook)) to retrieve values from files in an Amazon S3 bucket, run a check on them, post the result of the check on Slack, and then log the response of the Slack API.

For this use case, you'll use hooks directly in your Python functions because none of the existing Amazon S3 operators can read data from multiple files within an Amazon S3 bucket. Also, none of the existing Slack operators can return the response of a Slack API call, which you might want to log for monitoring purposes.

The source code for the hooks used in this example can be found in the following locations: 

- [S3Hook source code](https://github.com/apache/airflow/blob/main/airflow/providers/amazon/aws/hooks/s3.py)
- [SlackHook source code](https://github.com/apache/airflow/blob/main/airflow/providers/slack/hooks/slack.py)

### Prerequisites

Before running the example DAG, make sure you have the necessary Airflow providers installed. If you are using the Astro CLI, add the following packages to your `requirements.txt` file:

```text
apache-airflow-providers-amazon
apache-airflow-providers-slack
```
### Create the connections

1. In the Airflow UI, go to **Admin** > **Connections** and click the plus (+) icon to add a new connection.
2. In the **Connection Id** field, enter a unique name for the connection.
3. In the **Connection Type** list, select **Amazon S3** as the connection type for the Amazon S3 bucket. If the **Amazon S3** connection type isn't available, make sure you installed the provider correctly.
4. Enter your AWS access key ID in the **Login** field.
5. Enter your AWS secret access key in the **Password** field. To retrieve your AWS access key ID and AWS secret access key, see [AWS Account and Access Keys](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html).
6. Click **Save**.
7. Repeat steps 1 to 6 to create a new connection for Slack. Select **Slack Webhook** as the connection type and enter your [Bot User OAuth Token](https://api.slack.com/authentication/oauth-v2) in the **Password** field. To obtain the token, go to **Features** > **OAuth & Permissions**  on `api.slack.com/apps`.

### Run the example DAG

The following example DAG uses [Airflow Decorators](https://docs.astronomer.io/learn/airflow-decorators) to define tasks and [XCom](https://docs.astronomer.io/learn/airflow-passing-data-between-tasks) to pass information between Amazon S3 and Slack. The name of the Amazon S3 bucket and the names of the files that the first task reads are stored as environment variables for security purposes.

The following example DAG completes the following steps:

- A Python task with a manually implemented `S3Hook` reads three specific keys from Amazon S3 with the `read_key` method and then returns a dictionary with the file contents converted to integers.
- A second Python task completes a simple sum check using the results from the first task. 
- The SlackHook `call` method posts the sum check results to a Slack channel and returns the response from the Slack API.

<Tabs
    defaultValue="taskflow"
    groupId= "run-the-example-dag"
    values={[
        {label: 'TaskFlow API', value: 'taskflow'},
        {label: 'Traditional syntax', value: 'traditional'},
    ]}>

<TabItem value="taskflow">

<CodeBlock language="python">{hook_tutorial_taskflow}</CodeBlock>

</TabItem>

<TabItem value="traditional">

<CodeBlock language="python">{hook_tutorial_traditional}</CodeBlock>

</TabItem>
</Tabs>